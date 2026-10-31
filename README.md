# RubberNaut — The Thalia Journal

An epistolary journal of the RubberNaut (Thalia / Rn+) stories, published as
single-image pages in chronological order. Live at **https://rubbernaut.com**
(GitHub Pages, custom domain).

© 2026 by AtaraxiA under Creative Commons BY-SA.

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
