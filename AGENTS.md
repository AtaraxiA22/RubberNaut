# AGENTS.md — Working Notes for AI Agents on RubberNaut

This file is read at the start of every session. Keep it short and durable. Sessions
can end without warning, so anything the next agent must know should live in this
file, the README, the git history, or a PR description — never only in chat. Commit
important things to the repo.

## About Jack (the human partner)

- Jack (GitHub user AtaraxiA22) is nearly 80 and has mild cognitive issues. Be gentle,
  patient, and plain-spoken. Short sentences, no jargon, no surprises.
- He is NOT a coder and does not know Python. He prefers a GUI whenever possible, does
  not do "surgery" on scripts, but can copy/paste simple terminal commands into the
  Vibe chat. He uses only the web interface of Vibe — he does not use a command line
  himself.
- He knows GitHub only for simple things: uploading, downloading, and editing files
  in the web interface. **Standing rule: the agent handles ALL deeper GitHub
  mechanics** — branches, pull requests, merges, conflicts, commit messages. Keep
  Jack's side to upload/download/edit only. When GitHub work is needed, the agent
  does it and then tells Jack the result in one simple sentence with the link.
- He prefers NOT to see code snippets or code boxes except in rare cases. When
  explaining a problem or a fix, use brief, simple narrative — plain English, as if
  telling a short story — to avoid cognitive overload.
- When asking Jack a multiple-choice question, ALWAYS include an "Other" option so he
  can answer in his own words.
- He is slightly color-tone blind, so be careful with anything that depends on
  telling colors apart (for example the orange PostDate text on the site).
- The author signature is always "AtaraxiA" — never "Ataraxia". Never "correct" this
  spelling anywhere: file headers, copyright lines, page text.

## The site (short version — full details in README.md)

- RubberNaut is a static Jekyll site on GitHub Pages with the custom domain
  rubbernaut.com. There is no server and no login. Commit and push, and the site
  rebuilds by itself.
- Site version: the `rncom_version` setting in the site config (currently v03.00).
  Bump the second number by 1 for each group of changes, so the live build is always
  visible in the page footer.
- Journal pages live in the posts folder as files named like
  `Rn+yyyy.mmdd-hhmm - Page Title.md`. "Rn+" is the internal story marker and is never
  shown to visitors; visitors see `yyyy.mmdd-hhmm - Page Title`. Any old seconds part
  (like `-1430.05`) is chopped off. The Table of Contents page builds itself from
  these files on every site build — no manual editing of the TOC.
- New pages are added with the publisher script `RNcom_publish_docx.v01.py`, which is
  a GUI app. **If Jack ever needs the script file, ALWAYS give the RAW download link
  (raw.githubusercontent.com), never the GitHub web-page link** — a saved web page
  will not run. The full script is too big for copy/paste, so a download link is the
  only way to hand it over.
- The agent's sandbox has no screen, so GUI apps cannot be clicked or tested here.
  Scripts are verified with compile checks and headless (non-GUI) tests only; any GUI
  behaviour is labelled "awaiting Jack's test" until he confirms it on his computer.
- If anything here would affect another AI chat that Jack relays to (he copy/pastes
  between chats), do not try to message that chat directly — prepare a short,
  paste-ready note for Jack instead, say so plainly, and log the note.

## Delivery

- Do the work on a branch named `vibe/<short-name>-<hash>`, push it, and open ONE draft
  PR to `main`. Update that same PR in place if anything changes — never delete the
  branch or open a replacement PR. Report the PR URL to Jack in plain words.
- End a PR body with `Closes #<number>` only if the PR resolves a tracked GitHub issue.
  (There are none — the README is the record.)
