LETTER TO THE @26.1124RN SESSION — build RNcom v03.00 in AtaraxiA22/RubberNaut from this spec
===========================================================================================

You are working in the `AtaraxiA22/RubberNaut` repo (Jekyll site on GitHub Pages,
custom domain rubbernaut.com, baseurl `/RubberNaut`). Your sandbox allows pushes to
this repo. Task: build site version RNcom v03.00 from scratch on a new branch
`vibe/rncom-v03-a90aa1`, purge the old test apparatus, push, open a draft PR to
`main`, and report the PR URL. Do NOT touch AtaraxiA22/Taggerist.

1. PURGE OLD TEST CONTENT on the branch
Delete everything currently in the repo except what you create: old `_posts/*`,
`home.md`, `journal.md`, `tags.md`, old `_layouts/*`, `assets/`, `README.md`,
`index.md`, `_config.yml`. (Per the Chief, all of that was test files.) Start fresh.

2. SITE CONCEPT — "RUBBERNAUT: The Thalia Journals"
An epistolary journal published as illustrated pages. Three page types:

- TITLE PAGE `/` (index.md, layout `title`): logo image, site title
  "RUBBERNAUT: The Thalia Journals", subtitle "An Epistolary Tale of Rubber Fetish
  Mysticism in the Winter of Life", "By AtaraxiA", the copyright line (EXACT form,
  per the @26.1128 regime — CC BY-SA is deprecated; year rolls at render time):
      <p class="copyright">&copy; {{ site.time | date: "%Y" }} by AtaraxiA - all rights reserved</p>
  and a [Table of Contents] link to /toc.html.

- TOC `/toc.html` (toc.md, layout `default`): banner + a scrollable 3-column table
  built from `site.posts` (Liquid loop; the TOC is regenerated from `_posts/` on
  every Pages build, so adding/renaming/deleting a post file updates it
  automatically — there is no separate TOC file):
  - col 1 header `StoryDate:` with ↓ (newest first) and ↑ (oldest first) buttons;
    rows show `post.storydate`
  - col 2 header `PostDate:` with ↓/↑ buttons; rows show `post.postdate`
  - col 3 title links (`post.url | relative_url`), soft-wrap at 80 chars
    (CSS: max-width:80ch; overflow-wrap:anywhere)
  - sorting is client-side JS re-ordering <tr> elements by data-story / data-pub
    attributes; the choice is stored in cookie `rncom_sort`
    (values story-asc|story-desc|pub-asc|pub-desc); default `story-desc`
    (StoryDate newest first); the active arrow button is highlighted
  - first line above the table: an [Open My last Read] link, shown ONLY if cookie
    `rncom_last` exists AND a row with that data-story still exists (protects
    against deleted/renamed posts); its href is that row's link
  - table container scrollable (max-height:70vh; overflow-y:auto);
    column widths ~17% / 17% / 66%

- JOURNAL (READER) PAGE (layout `post`): banner with logo + site title linking back
  to `/` (the title page); [Table of contents] links top AND bottom;
  <h1>{{ page.storydate }} – {{ page.title }}</h1>; meta line
  `posted {{ page.postdate }} UTC`; image if page.image; body.
  JS on each reader page: set cookie `rncom_last` = page storydate on every visit;
  save scroll position to cookie `rncom_pos` = `<storydate>:<scrollY>` (throttled
  scroll listener); on load, restore scroll if `rncom_pos` matches this page.
  All cookies: `path=/; max-age=31536000`.
  The banner appears on every page except the title page. Every page footer shows
  a small `RNcom.{{ site.rncom_version }}` corner version.

3. PAGE FILE STRUCTURE (simplified SNI scheme)
Each journal page is one file in `_posts/` named exactly:
    Rn+yyyy.mmdd-hhmm - Page Title.md
- `Rn+` is the internal StoryNameIndicator (SNI) — never shown to visitors;
  visitors see `yyyy.mmdd-hhmm - Page Title`.
- Stamp rule: 4-digit year, 2-digit everything, 24-hour clock, `yyyy.mmdd-hhmm`.
  If an old stamp has a seconds slot (`...-hhmm.ss`), chop it.
- Front matter (exactly these fields):
      ---
      layout: post
      title: "Page Title"
      date: yyyy-mm-dd hh:mm:ss +0000      # from the stamp, UTC (Jekyll needs this:
                                           # the filename has no YYYY-MM-DD prefix)
      storydate: "yyyy.mmdd-hhmm"
      postdate: "yyyy.mmdd-hhmm"           # UTC, when published to the site
      image: "/resources/Rn+yyyy.mmdd-hhmm.jpg"   # omit if no image
      permalink: /pages/yyyy.mmdd-hhmm.html
      ---
- Body: markdown. Images referenced as `{{ '/resources/<file>' | relative_url }}`.

4. _config.yml
title: "RUBBERNAUT: The Thalia Journals"
description: "An Epistolary Tale of Rubber Fetish Mysticism in the Winter of Life"
author: AtaraxiA
rncom_version: "v03.00"
url: "https://rubbernaut.com"
baseurl: "/RubberNaut"
defaults: posts -> layout: post
No theme, no plugins. Black background / white text CSS in assets/css/style.css
(banner, title page, TOC table, reader page; PostDate column in orange #f90, as before).

5. resources/ DIRECTORY (with .gitkeep) at repo root
Docx-extracted images go here, named `Rn+<storydate>.<ext>`; if a page has several
images, increment the stamp MINUTES by 1 per extra image (-1432, -1433, … with
hour/day rollover).

6. PUBLISHER SCRIPT `RNcom_publish_docx.v01.py` at repo root
Self-contained, one file, versioned name; header: version note +
`# (c) 2026 by AtaraxiA — All rights reserved.` (script-file convention; the SITE's
visitor-facing © line is the rolling form in §2).
- PySide6 GUI; on start opens the system multi-select Open dialog for .docx files
  (batch or single, any order); a "site folder" box (local clone of this repo) with
  Browse, remembered in `RNcom_publish_docx.config.txt` (`SITE: <path>`, gitignored);
  a log pane; buttons [Convert && publish to site] and [Commit && push site]
  (the latter only if the site folder is a git clone: git add _posts resources,
  git commit, git push, output shown in the log).
- Filename check: regex ^([A-Za-z]{1,6}\+)\d{4}\.\d{2}\d{2}-\d{2}\d{2}(\.\d+)? - (.+)\.docx$
  (case-insensitive extension); validate real date/time (month/day/hour/minute
  ranges); the optional `.\d+` seconds slot is accepted and chopped. Non-matching
  files are logged and skipped.
- Docx parsing with STDLIB ONLY (zipfile + ElementTree): read word/document.xml +
  word/_rels/document.xml.rels; paragraphs -> markdown (Heading1..6 -> #…, Title ->
  #, bold/italic runs -> ** / *, line breaks); embedded images (a:blip r:embed)
  extracted in document order to resources/Rn+<stamp>.<ext> with minutes+1 per
  additional image, inserted as
  ![title]({{ '/resources/<name>' | relative_url }});
  guard literal {{ or {% in prose with {% raw %} ... {% endraw %}.
- Writes `_posts/Rn+<stamp> - <Title>.md` with the front matter from §3;
  postdate = current UTC yyyy.mmdd-hhmm; date from the stamp;
  permalink: /pages/<stamp>.html; overwrites an existing same-name post (log a
  warning line).
- Guard the PySide6 import (try/except) so the conversion core (parse_docx_name,
  docx_to_markdown, publish) is importable and testable without Qt.

7. LOGO
Layouts reference /assets/img/logo.webp. The Chief will supply the artwork — make
sure pages still render if the file is missing (alt text).

8. README.md
Short doc of the above: structure, naming rule, how to add pages with the script,
the RNcom.vXX.YY corner version. README's own © line uses the rolling form from §2.

9. VERIFY BEFORE PUSHING
- python3 -m py_compile RNcom_publish_docx.v01.py
- headless test: build a synthetic .docx (zip with word/document.xml,
  word/_rels/document.xml.rels, word/media/*), run parse_docx_name (valid + invalid
  names, .ss chop) and publish() into a temp site dir; assert: post written with
  correct front matter; two images extracted as -1430 / -1431; minute rollover
  works (-1459 + 1 -> -1500, and day rollover); overwrite logs a warning.
- YAML-parse _config.yml and every post front matter (fields present,
  permalink == /pages/<storydate>.html, image file exists); strip Liquid tags from
  layouts/toc and check HTML tag balance.

10. DELIVER
Branch vibe/rncom-v03-a90aa1 from main; commit; git push -u origin
vibe/rncom-v03-a90aa1; then:
  gh pr create --repo AtaraxiA22/RubberNaut --draft --head vibe/rncom-v03-a90aa1 \
    --base main --title "RNcom v03.00 (@26.1123): title page + sortable 3-col TOC + reader pages + docx publisher"
with a body summarizing the above. Report the PR URL.

OUT OF SCOPE (do not build): Blogger / Tumblr / Thunderbird-email publishing — the
.docx remains the master copy for those channels; only the GitHub-site leg is
automated.
===========================================================================================
END OF LETTER
 updated
