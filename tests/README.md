# Mixmo tests (one folder, packed as mixmo-tests.zip)

Put Mixmo.html in this folder, start `python3 -m http.server 8765` here, then:

- `python3 full.py`: must print `failures: 0`.
- `python3 golden.py compare` and `python3 golden2.py compare`: must print `changed: 0` (baselines: golden.json, golden2.json,
  re-recorded 2026-11-11).
- `python3 rewind.py`: `rewound poses that differ: 0` for both characters.

`t/`: scripts for the robot's get-up (rise). Run from this folder, e.g. `python3 t/check.py http://localhost:8765/Mixmo.html`
(bones, planted-paw slide, lowest point through the rise, many starting animations); `t/regress.py old-url new-url`
compares every other animation between two builds (the first line, sergal/idle, differs by itself from run to run);
`t/shots.py` makes frame sheets; `t/live.py` plays the real page (desktop 3D, 2D, emulated iPhone).

`node-scripts/`: the Node + Playwright scripts from the 2026-11-10/11 session (models, playback speed buttons,
hold-to-step, its own Over checks). See node-scripts/README.md.
