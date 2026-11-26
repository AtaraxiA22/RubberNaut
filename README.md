# RUBBERNAUT: The Thalia Journals

An epistolary tale of deep rubber fetishism in the winter of life, published as
illustrated journal pages. Live at **https://rubbernaut.com** (GitHub Pages + Jekyll,
custom domain). © 2026 by AtaraxiA — all rights reserved.

## Site layout (RNcom v03)

- `/` — **Title Page**: logo, title, subtitle, "By AtaraxiA", © 2026, and a
  [Table of Contents] link.
- `/toc.html` — **Table of Contents**: a scrollable table (12px font) generated from the
  `_journal/` collection. Each row starts with a 50×50 thumbnail of the page's first
  image, then StoryDate, PostDate (UTC, orange), and the title link (soft-wrap at 80
  characters, wrapped lines indented). Each date column header has ↓ (newest first) and
  ↑ (oldest first) arrows; clicking re-sorts the table live and remembers the choice in a
  cookie (default: StoryDate, newest first). If a "last read" cookie exists, an
  [Open My last Read] link appears above the table.
- `/pages/<storydate>.html` — **Journal pages** (the Reader): the first image is previewed
  at the top and again where it sits in the text; prev/next story pager top and bottom;
  [Table of contents] links top and bottom. Each visit stores the page's StoryDate (and
  scroll position) in cookies, which is what powers [Open My last Read].
- **Every page except the title page** has a sticky header (logo + site title + [Table of
  Contents] link at 12pt, always visible) and a ⚙ **Settings** button at the lower right
  (stored in localStorage): Light/Dark theme, reader font size (A−/A/A+), 1 or 2 columns
  in the reader, Standard (Verdana) or OpenDyslexic font, content width (Narrow 60ch /
  Standard 80ch / Wide 100ch), Prev/Next paging vs scroll only, and a Reset-to-defaults
  button. TOC links are not underlined (underline on hover) and each row's thumbnail
  opens the PostPage. PostPages page between stories with the ← / → keyboard arrow keys,
  and in 2-column reader mode the on-screen ← / → buttons page one screen of text at a
  time. The title page scales its logo to fit the browser window.

The TOC is generated from the `_journal/` collection at every site build, so adding,
renaming, or deleting a page file automatically updates the table on the next build —
there is no separate TOC file to edit. (The folder is `_journal/`, not `_posts/`, because
Jekyll only auto-collects date-prefixed filenames from `_posts/`; a collection accepts
our `Rn+…` names as-is.)

## Page files

Each journal page is one file in `_journal/` named:

    Rn+yyyy.mmdd-hhmm - Page Title.md

(`Rn+` is the internal StoryNameIndicator; visitors see only `yyyy.mmdd-hhmm - Page Title`.)
The stamp is always 4-digit year, 2-digit everything, 24-hour clock; any old seconds
slot (`.ss`) is chopped off. The front matter carries the machine fields:

    ---
    layout: post
    title: "Page Title"
    date: yyyy-mm-dd hh:mm:ss +0000      # Jekyll's internal date
    storydate: "yyyy.mmdd-hhmm"          # the StoryDate (from the filename stamp)
    postdate: "yyyy.mmdd-hhmm"           # the PostDate, UTC, when the page was published
    image: "/resources/Rn+yyyy.mmdd-hhmm.jpg"
    permalink: /pages/yyyy.mmdd-hhmm.html
    ---

Images extracted from .docx pages are stored in `resources/` named
`Rn+yyyy.mmdd-hhmm.<ext>` (minutes ticked up by 1 for each additional image:
`-1432`, `-1433`, …).

## Adding pages: Rn_pubdocx.v03.py

Run `python3 Rn_pubdocx.v03.py` (needs PySide6 and Pillow). The script is named
`Rn_pubdocx.vxx.py` — every new iteration increments the version number (if in doubt,
increment it). It opens the
system file picker; select one or more `.docx` files (batch or single, any order).
Each filename must be `Rn+yyyy.mmdd-hhmm - Title.docx` — files that don't match are
reported and skipped. For each valid file the script:

1. converts the .docx to a Markdown post in `<site>/_journal/Rn+yyyy.mmdd-hhmm - Title.md`
   (PostDate stamped as the current UTC `yyyy.mmdd-hhmm`),
2. extracts embedded images into `<site>/resources/` named by the story stamp, automatically
   optimized for the web (photos become JPEG quality 85, max side 1600px — typically ~10x
   smaller than a raw PNG; transparency is kept as optimized PNG),
3. logs everything in its window; the optional [Commit && push] button commits the
   new files in the site repo so the TOC picks them up after the next Pages build.

Point the script at the local clone of this repo once (the "site folder" box); it
remembers the path in `RNcom_publish_docx.config.txt` next to the script.

## Version

The site calls itself **RNcom** and shows its version in the footer of every
page (`rncom_version` in `_config.yml`, currently `v03.23`). Bump the second number with
every group of changes, so you can always see at a glance which build is live.
