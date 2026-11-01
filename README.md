# RubberNaut — The Thalia Journal

An epistolary journal of the RubberNaut (Thalia / Rn+) stories, published as
single-image pages in chronological order. Live at **https://rubbernaut.com**
(GitHub Pages, custom domain).

© 2026 by AtaraxiA under Creative Commons BY-SA.

## Version

The site calls itself **RNcom** and shows its version in the lower-left corner of the
left menu (`rncom_version` in `_config.yml`, currently `v01.01`). Bump the second
number by 1 with every group of changes (e.g. `v01.02`), so you can always see at
a glance which build is live.

## About this site

This site is intended to remain online permanently and unattended. It is a
static site (GitHub Pages + Jekyll): no server, no logins, nothing to maintain.
The journal index on the home page is generated automatically from the dated
pages in `_posts/`, so new pages slot into the story timeline by themselves —
no manual menu editing.

## How pages are added

Each story page is a file in `_posts/` named `YYYY-MM-DD-slug.md` with a small
front-matter header (title, date, stamp, image) and the journal entry as the
body. The matching image lives in `assets/img/` named with the `Rn+` story
stamp, e.g. `Rn+2019.1031-2137.webp`. Commit and push — the site rebuilds.

## Site structure (v2)

- `home.md` — the title page at `/` (big "RubberNaut — The Thalia Journal" + [Enter the journal] button; no sidebar).
- `journal.md` — the journal index at `/journal.html` (sidebar menu on the left).
- `tags.md` — browse-by-tag page at `/tags.html`.
- `_layouts/default.html` — shell with the left menu: header "RubberNaut — The Thalia Journal",
  a filter box that searches TITLES and FULL TEXT as you type (× clears; Esc clears; a "No journal
  entries match …" message appears when nothing matches; a 'fold all' button closes every month block),
  entries grouped into collapsible month blocks (newest month open; month blocks auto-open while
  filtering and re-close when the filter is cleared).
- `_layouts/post.html` — one story page: title, stamp (+ "added to the site <date>"), image,
  anecdote, tag links, and back / index / forward arrows at the bottom.
- Editing pages: any plain-text editor works (the pages are simple Markdown with a
  short header block). Just keep the `title:` value in double quotes and keep the
  `date:` line — a broken header fails the whole site build (that happened once).
  Tip: edit one page at a time and push, so a mistake is easy to spot.
