# Pooltoy tests (2026-11-14)

For the Pooltoy Water Lab (`pooltoy-water-lab.html`) and the Pooltoy inside Mixmo. They draw with three.js r170 from
disk: `npm i three@0.170.0`, then run with `THREE_DIR=node_modules/three` (default: `node_modules/three` here).

- `pt_sync.py lab.html Mixmo.html [--check]`: copy the pooltoy block from the lab into Mixmo (or only check it's in step).
  Edit the block only in the lab.
- `lab.py lab.html [--save t.json | --against toy_run.json]`: the lab's water checks (20; the P2-a version, see the
  roadmap). `lab.py Mixmo.html --mixmo --against toy_run.json`: the same, on the block inside Mixmo. Needs no three.js.
- `glb_check.py lab.html model.glb [--against glbrun_<model>.json]`: GLB water checks (both models: 0 failures).
  The models aren't in the zip: `baller_fox_body.glb`, `female_sergal_body.glb`.
- `glb-water-tests/glb_tests.py lab.html model.glb --three node_modules/three`: textures, normally and with the chat
  preview's limits faked.
- `pt_mixmo.py Mixmo.html outdir [model.glb]`: the Pooltoy character live in Mixmo (20 checks).
- `shots.py lab.html Mixmo.html outdir`: fixed pictures (lab toy, Capsule at Flat 0.5, Mixmo's three characters);
  compare with `m0-shots/` pixel for pixel.

Baselines: `toy_run.json` (the toy's Test run), `glbrun_baller_fox_body.json`, `glbrun_female_sergal_body.json`,
`m0-shots/`. Results on the files handed over 2026-11-14: all pass, all identical.
