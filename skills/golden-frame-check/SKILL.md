---
name: golden-frame-check
description: Run, record or explain the golden-frame pose tests (golden.py / golden2.py) for tripod-walk-editor.html, including setup and dependencies.
---

# Golden-frame check for the walk editor

Golden frames record the exact pose of each character (sergal and robot) at set frames in every mode, and
compare later builds against that record. They are a standing regression test: run them after every change,
not only during refactors.

- `golden.py` + `golden.json`: 460 poses.
- `golden2.py` + `golden2.json`: 924 poses (wider set).

## Dependencies

- Python 3.
- Playwright with Chromium (it drives a hidden browser that loads the app):
  ```
  pip install playwright
  playwright install chromium
  ```
  (In a cloud session where Chromium is preinstalled, skip `playwright install`.)
- Runs on a computer, not on iPhone.

## Setup

1. Put `golden.py`, `golden2.py`, `golden.json`, `golden2.json` and `tripod-walk-editor.html` in one folder.
2. In that folder start a local server and leave it running:
   ```
   python3 -m http.server 8765
   ```
   If a run fails with ERR_CONNECTION_REFUSED, the server has stopped: start it again.

## Compare (after any change)

```
python3 golden.py compare
python3 golden2.py compare
```

- `changed: 0` means every pose matches.
- Otherwise it lists the poses that differ. Decide whether each difference was intended.

## Record (only after an intended change)

```
python3 golden.py record
python3 golden2.py record
```

Then run `compare` once to confirm `changed: 0`. Re-record only when every listed difference was meant to
happen; never to hide an unexplained change.

## Other address or file name

Add the full URL as an extra argument, e.g.
`python3 golden.py compare http://localhost:8765/my-copy.html`

## Workflow when changing the app

1. Before editing: run `compare` to confirm a clean baseline.
2. Pure refactor (tidy-up, no behaviour change): `compare` must stay at `changed: 0`.
3. Intended behaviour change: check that only the expected characters/modes changed, run the other tests
   (full.py: 0 failures; bones.py: all bones within 3%; slide.py: planted-paw drift under about 0.05),
   then `record` and deliver the new JSON files alongside the app.
4. Note in roadmap.md (Handoff section) whenever baselines are re-recorded and why.
