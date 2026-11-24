#!/usr/bin/env python3
# RNcom_publish_docx v01: GUI publisher for RUBBERNAUT: The Thalia Journals — pick one or
#   more .docx journal pages (system Open dialog, batch or single, any order), each named
#   'Rn+yyyy.mmdd-hhmm - Title.docx'; converts them to site posts in <site>/_journal/, extracts
#   embedded images to <site>/resources/ named by the story stamp (minutes +1 per extra image,
#   any old .ss seconds slot chopped off), and stamps postdate as the current UTC yyyy.mmdd-hhmm.
#   Docx parsing uses only the standard library (a .docx is a zip of XML); PySide6 is used for
#   the GUI only — the conversion core (parse_docx_name / docx_to_markdown / publish) is importable
#   and testable without it.
# (c) 2026 by AtaraxiA — All rights reserved.

import os
import re
import sys
import zipfile
import datetime
import xml.etree.ElementTree as ET

APP_VERSION = "v01"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "RNcom_publish_docx.config.txt")

NAME_RE = re.compile(
    r"^(?P<sni>[A-Za-z]{1,6}\+)"
    r"(?P<y>\d{4})\.(?P<mo>\d{2})(?P<d>\d{2})-"
    r"(?P<h>\d{2})(?P<mi>\d{2})"
    r"(?P<ss>\.\d+)?"                      # optional legacy seconds slot — chopped off
    r" - (?P<title>.+?)"
    r"\.docx$",
    re.IGNORECASE,
)

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def parse_docx_name(filename):
    """Validate 'Rn+yyyy.mmdd-hhmm[.ss] - Title.docx'. Returns (sni, stamp, title) or raises ValueError."""
    base = os.path.basename(filename)
    m = NAME_RE.match(base)
    if not m:
        raise ValueError("filename must be 'Rn+yyyy.mmdd-hhmm - Title.docx' (SNI + stamp + ' - ' + title)")
    y, mo, d, h, mi = (int(m.group(k)) for k in ("y", "mo", "d", "h", "mi"))
    try:
        datetime.datetime(y, mo, d, h, mi)
    except ValueError:
        raise ValueError("stamp is not a real date/time (yyyy.mmdd-hhmm, 24-hour clock)")
    stamp = "%04d.%02d%02d-%02d%02d" % (y, mo, d, h, mi)   # seconds slot (m['ss']) deliberately dropped
    sni = m.group("sni")
    if sni.lower() != sni[:2].lower() + "+":  # keep the canonical 'Xx+' shape
        sni = sni[0].upper() + sni[1:]
    return sni, stamp, m.group("title").strip()


def stamp_to_dt(stamp):
    return datetime.datetime.strptime(stamp, "%Y.%m%d-%H%M")


def dt_to_stamp(dt):
    return dt.strftime("%Y.%m%d-%H%M")


def bump_minutes(stamp, n):
    return dt_to_stamp(stamp_to_dt(stamp) + datetime.timedelta(minutes=n))


def utc_postdate(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return now.strftime("%Y.%m%d-%H%M")


def yaml_quote(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fname_safe(title):
    return re.sub(r'[\\/:*?"<>|]', "-", title).strip()


def _local(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def docx_to_markdown(docx_path):
    """Parse a .docx (zip of XML) with the stdlib only.
    Returns (blocks, images) where blocks is a list of ('p'|'h1'..'h6'|'img', text, rid)
    in document order, and images maps rId -> (ext, bytes)."""
    with zipfile.ZipFile(docx_path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        rels = {}
        try:
            rel_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
            for rel in rel_root:
                if _local(rel.tag) == "Relationship":
                    rels[rel.get("Id")] = rel.get("Target")
        except KeyError:
            pass
        images = {}
        for rid, target in rels.items():
            if "/media/" in ("/" + target) or target.startswith("media/"):
                ext = os.path.splitext(target)[1].lstrip(".").lower() or "png"
                member = "word/" + target if not target.startswith("/") else target.lstrip("/")
                try:
                    images[rid] = (ext, z.read(member))
                except KeyError:
                    pass

        blocks = []
        body = None
        for child in doc:
            if _local(child.tag) == "body":
                body = child
                break
        if body is None:
            return [], images
        for p in body:
            if _local(p.tag) != "p":
                continue
            style = ""
            ppr = p.find(W_NS + "pPr")
            if ppr is not None:
                ps = ppr.find(W_NS + "pStyle")
                if ps is not None:
                    style = ps.get(W_NS + "val") or ""
            text = ""
            img_rids = []
            for r in p.findall(W_NS + "r"):
                rpr = r.find(W_NS + "rPr")
                bold = italic = False
                if rpr is not None:
                    for flag, is_bold in ((W_NS + "b", True), (W_NS + "i", False)):
                        el = rpr.find(flag)
                        if el is not None and el.get(W_NS + "val") not in ("0", "false", "off"):
                            if is_bold:
                                bold = True
                            else:
                                italic = True
                for el in r.iter():
                    lt = _local(el.tag)
                    if lt == "t":
                        t = el.text or ""
                        if bold:
                            t = "**" + t + "**"
                        if italic:
                            t = "*" + t + "*"
                        text += t
                    elif lt == "br":
                        text += "  \n"
                    elif lt == "blip":
                        rid = el.get(R_NS + "embed") or el.get(R_NS + "link")
                        if rid and rid in images:
                            img_rids.append(rid)
            text = text.strip()
            if img_rids and not text:
                for rid in img_rids:
                    blocks.append(("img", "", rid))
            elif img_rids:
                for rid in img_rids:
                    blocks.append(("img", text, rid))
                text = ""
            if text:
                sm = re.match(r"(?i)^heading(\d)$", style)
                if sm:
                    blocks.append(("h" + sm.group(1), text, None))
                elif style.lower() == "title":
                    blocks.append(("h1", text, None))
                else:
                    blocks.append(("p", text, None))
        return blocks, images


def liquid_guard(text):
    """Keep literal {{ or {% in journal prose from being read as Liquid."""
    if "{{" in text or "{%" in text:
        return "{% raw %}" + text + "{% endraw %}"
    return text


def build_post_md(sni, stamp, title, blocks, images, site_root, postdate):
    """Render the _journal/*.md content. Returns (post_text, image_files) where image_files
    maps rid -> (relpath_from_site_root, filename)."""
    image_files = {}
    lines = []
    for i, (kind, text, rid) in enumerate(blocks):
        if kind == "img":
            ext = images[rid][0]
            img_stamp = bump_minutes(stamp, sum(1 for k, _, r in blocks[:i + 1] if k == "img") - 1)
            name = "%s%s.%s" % (sni, img_stamp, ext)
            image_files[rid] = ("resources/" + name, name)
            alt = title if not text else text
            lines.append("![%s]({{ '/resources/%s' | relative_url }})" % (alt, name))
        elif kind.startswith("h"):
            n = int(kind[1])
            lines.append("#" * n + " " + liquid_guard(text))
        else:
            lines.append(liquid_guard(text))
    body = "\n\n".join(lines)
    dt = stamp_to_dt(stamp)
    date_line = dt.strftime("%Y-%m-%d %H:%M:%S +0000")
    image_line = ""
    if image_files:
        first = image_files[next(iter(image_files))]
        image_line = "image: %s\n" % yaml_quote("/" + first[0])
    fm = (
        "---\n"
        "layout: post\n"
        "title: %s\n" % yaml_quote(title) +
        "date: %s\n" % date_line +
        "storydate: %s\n" % yaml_quote(stamp) +
        "postdate: %s\n" % yaml_quote(postdate) +
        image_line +
        "permalink: /pages/%s.html\n" % stamp +
        "---\n"
    )
    return fm + "\n" + body + "\n", image_files


def publish(docx_path, site_root, postdate=None):
    """Convert one .docx into a site post + extracted images. Returns the post path."""
    sni, stamp, title = parse_docx_name(docx_path)
    blocks, images = docx_to_markdown(docx_path)
    postdate = postdate or utc_postdate()
    post_text, image_files = build_post_md(sni, stamp, title, blocks, images, site_root, postdate)
    posts_dir = os.path.join(site_root, "_journal")
    res_dir = os.path.join(site_root, "resources")
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    fname = "%s%s - %s.md" % (sni, stamp, fname_safe(title))
    post_path = os.path.join(posts_dir, fname)
    if os.path.exists(post_path):
        print("WARNING: overwriting existing post %s" % post_path)
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post_text)
    for rid, (relpath, name) in image_files.items():
        ext, data = images[rid]
        with open(os.path.join(site_root, relpath), "wb") as f:
            f.write(data)
    return post_path


# ---------------------------------------------------------------- GUI (PySide6, optional)

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLineEdit, QPlainTextEdit, QFileDialog, QLabel,
    )
    HAVE_QT = True
except Exception:
    HAVE_QT = False


def load_site_from_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("SITE:"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return ""


def save_site_to_config(site):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("SITE: %s\n" % site)


_WindowBase = QMainWindow if HAVE_QT else object


class PublisherWindow(_WindowBase):
    def __init__(self):
        if not HAVE_QT:
            raise RuntimeError("PySide6 is not installed; GUI unavailable")
        super().__init__()
        self.setWindowTitle("RNcom_publish_docx %s" % APP_VERSION)
        self.resize(720, 520)
        self.docx_files = []
        central = QWidget(self)
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)

        lay.addWidget(QLabel("Site folder (local clone of the site repo):"))
        row = QHBoxLayout()
        self.site_edit = QLineEdit(load_site_from_config())
        browse = QPushButton("Browse…")
        browse.clicked.connect(self.pick_site)
        row.addWidget(self.site_edit)
        row.addWidget(browse)
        lay.addLayout(row)

        pick = QPushButton("Choose .docx file(s)…")
        pick.clicked.connect(self.pick_docx)
        lay.addWidget(pick)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        lay.addWidget(self.log)

        btns = QHBoxLayout()
        self.conv_btn = QPushButton("Convert && publish to site")
        self.conv_btn.clicked.connect(self.convert)
        self.commit_btn = QPushButton("Commit && push site")
        self.commit_btn.clicked.connect(self.commit_push)
        btns.addWidget(self.conv_btn)
        btns.addWidget(self.commit_btn)
        lay.addLayout(btns)

    def say(self, msg):
        self.log.appendPlainText(msg)

    def pick_site(self):
        d = QFileDialog.getExistingDirectory(self, "Site folder")
        if d:
            self.site_edit.setText(d)
            save_site_to_config(d)

    def pick_docx(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Choose journal .docx files", "", "Word documents (*.docx)")
        if files:
            self.docx_files = files
            self.say("selected %d file(s):" % len(files))
            for f in files:
                self.say("  " + os.path.basename(f))

    def convert(self):
        site = self.site_edit.text().strip()
        if not site or not os.path.isdir(site):
            self.say("ERROR: set a valid site folder first.")
            return
        if not self.docx_files:
            self.say("ERROR: choose .docx file(s) first.")
            return
        for path in self.docx_files:
            try:
                post = publish(path, site)
                self.say("published: %s" % os.path.relpath(post, site))
            except ValueError as e:
                self.say("SKIPPED %s — %s" % (os.path.basename(path), e))

    def commit_push(self):
        import subprocess
        site = self.site_edit.text().strip()
        if not site or not os.path.isdir(os.path.join(site, ".git")):
            self.say("ERROR: site folder is not a git clone.")
            return
        for args in (["git", "add", "_journal", "resources"],
                     ["git", "commit", "-m", "RNcom: publish docx pages @%s" % utc_postdate()],
                     ["git", "push"]):
            r = subprocess.run(args, cwd=site, capture_output=True, text=True)
            self.say("$ %s" % " ".join(args))
            self.say((r.stdout + r.stderr).strip() or "(ok)")


def main():
    if not HAVE_QT:
        sys.exit("PySide6 is not installed — the conversion core (parse_docx_name, "
                 "docx_to_markdown, publish) is importable without it; the GUI needs PySide6.")
    app = QApplication(sys.argv)
    w = PublisherWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
