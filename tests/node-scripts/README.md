# Mixmo test scripts (2026-11-10 / 11)

Node + Playwright scripts written while working on Mixmo in Claude's cloud workspace. They are working tools,
not a finished test suite: no stored golden files, and they don't cover every turn and morph the way the old
`full.py` did.

## Setup

    npm install                 # playwright + three@0.170.0
    npx playwright install chromium

`lib.js` opens Mixmo in Chromium and serves the local `three@0.170.0` (from `node_modules`) in place of the
jsDelivr URLs, so the 3D renderer and GLB import work offline. It also has `addModel(page, path)` for loading a GLB.

Paths: scripts that take no file argument use `MIXMO` (default `./Mixmo.html`) and `MODELS` (default `./models`,
holding `baller_fox_body.glb` and `female_sergal_body.glb`). Run from the folder with Mixmo.html, or set them:

    MIXMO=../Mixmo.html MODELS=../models node foxtest.js ../Mixmo.html shots

## Scripts

| Script | What it checks | Usage |
|---|---|---|
| `cmp.js` | Pose comparison, old file vs new: every character, animation and terrain, 48 frames each (4,416 poses); reports any that differ and any NaN poses | `node cmp.js old.html new.html` |
| `bench.js` | Pose-building time per frame (sergal walk, regular sergal run, robot run on five), old vs new | `node bench.js old.html new.html` |
| `slide.js` | Planted-paw slide per frame for the regular sergal, Sergal and Fox presets, flat and hills; args 3-4: `1 1` adds 90/180 turns (turn numbers not reliable, see notes) | `node slide.js Mixmo.html [turns rot]` |
| `foxtest.js` | Baller Fox + Female sergal copying him, each preset and animation: model height, hip drop, leg stretch; optional screenshots | `node foxtest.js Mixmo.html [shotsDir]` |
| `over3x.js` | Factory-fresh robot, Over three times in a row: flags paw jumps > 10 a frame and anything sinking > 6 | `node over3x.js Mixmo.html` |
| `over3xb.js` | Same, flags anything sinking > 5 and names the part | `node over3xb.js Mixmo.html` |
| `over3.js` | One Over: each red paw's height and slide through the rise | `node over3.js Mixmo.html` |
| `over2.js` | Screenshots of the rise at chosen frames | `node over2.js Mixmo.html TAG 8,16,24` (writes `over/`) |
| `rel.js` | Rise end: worst red-paw slip and deepest sink from three start moments | `node rel.js` |
| `dropcheck.js` | Start of the Over drop at 8 press moments: lowest point | `node dropcheck.js Mixmo.html` |
| `walkcheck.js` | Robot walking 400 frames: lowest point | `node walkcheck.js Mixmo.html` |
| `blend.js` | Three-legged sergal: how far the tail leg's timing travels during walk/idle <-> run switches | `node blend.js Mixmo.html` |
| `rate.js` | Playback speed 1 / 1/2 / 1/4, tap and hold on the step buttons | `node rate.js` |
| `hold.js` | Hold-to-step event log (switches to 2D first) | `node hold.js` |
| `ui.js` | Body preset panel, remembered choice, Save & load, game run, 2D/3D screenshots | `node ui.js` (writes `ui/`) |
| `head.js` | His hip and head heights per preset | `node head.js Mixmo.html` |
| `measure.js` / `profile.js` / `dump.js` | Baller Fox rig and leg measurements (bones, side profile, mesh points to JSON) | `node measure.js`; `node profile.js file.glb`; `node dump.js file.glb out.json` |

Some scripts write screenshots into folders next to them (`over/`, `o3/`, `ui/`, `shots`): create them first
with `mkdir`.

## Notes (also in the roadmap's handoff)

- Build poses from `cur`, or fill in `bobWave`, when building from `P[mode]` directly; otherwise every position
  is NaN, prints as null, and two NaN poses compare equal (an early `cmp.js` had this bug; fixed).
- With two GLB models loaded, software 3D drawing is very slow: the model tests pose models with `mdlPlace` instead
  of `render`. Timer-based tests (hold-to-step) should switch to 2D.
- Most scripts stop the app's own loop (`requestAnimationFrame` stubbed) and call `frame(t)` themselves, so runs are
  repeatable. `over3x.js` lets the real loop run briefly first, so its very first frames vary between runs.
