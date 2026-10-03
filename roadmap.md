# Roadmap

A procedural character and locomotion sandbox: build multi-limbed characters from parts, animate them
with procedural gaits, IK footstep planning and scrubbable multi-part transitions (morphs), and export
the results. Every motion comes from parameters, so the same settings always give the same result.

Long-term goals:

- A Mixamo-style tool: export skeletons and animations from the procedural system.
- A 3D JavaScript game built on the same engine.

Constraint throughout: everything stays a single HTML file that runs on iPhone (Claude app preview and
w3schools). Downloads only work from w3schools.

---

## Now: the editor (`tripod-walk-editor.html`)

Done so far:

- Two characters: the three-legged sergal and the six-limbed robot, each with their own modes.
- Procedural gaits (loops), mode blends, and morphs (90° / 180° / skid, Over, Ceiling, Rise). Spin is a toggled loop, not a morph.
- IK footstep planning, foothold search, thigh spring, head steadiness, terrain (hills, bumpy, steps).
- Robot skins (boxes, sergal, dinosaur, kangaroo), body segments, spine flex.
- Frame-by-frame stepping and scrubbing of loops and morphs, LOOP / MORPH status line, morph part markers.
- Full Playwright test of every mode pair, turn and move, forwards and backwards.
- Robot rules enforced (see "Robot rules" below): no squashed bones, no sliding paws, ceiling respects gravity.
- Ceiling: the front (red-paw) end reaches up and grabs; the ends swap jobs, as in Over. Drop is the reverse.
- Spin pivots round the middle of the body; long-bodied modes spin slower so planted paws can keep up.
- Robot legs turn and tilt at the hip (not only swing), so a planted paw stays put while the body turns.
- Robot look panel: "Bone stretch allowed" slider (0-30%, default 0%) and a "Bone check" debug button.

## Robot rules (must never be broken)

- Bones never squash or stretch beyond the "Bone stretch allowed" slider (default 0%).
  - Limbs are blended bone by bone (direction turns, length kept), never by averaging joint positions.
  - Splay turns the leg at the hip; a toe kept off the ground tips up instead of stretching.
  - Exempt: the kangaroo's curled tail, and any limb while it swaps places with that tail.
  - The sergal is not covered by this rule.
- A planted paw never slides, including while spinning or turning.
- The ceiling respects gravity: the robot hangs, planted legs nearly straight, free limbs hanging down.

## Next: make morphs editable

- Morphs get their own sliders (timing, height, lean, part lengths), like loops have now.

---

## Stage 0: safety net (done)

- Keep the full Playwright test.
- Add "golden frames": record the exact pose of each character at set frames in every mode, and compare
  after every refactor.

## Stage 1: characters as data (mostly done: registry, sergal shape as data, whole-character save/load)

- A character definition format (JSON):
  - body: segments, lengths, thickness;
  - limbs: attachment point, role (leg / arm / neck / tail), 180° flip, length;
  - skins and colours;
  - gaits (slider values per mode);
  - morphs (parts, timing, which are allowed).
- Rewrite the sergal and the robot as two definition files. A new character is a new file, not new code.

## Stage 2: one generic rig (started: both characters now share one footstep planner, leg solver, body-height maths and heading code)

- Merge the sergal and robot rigs into one rig that builds any character from its definition.
- Must match the golden frames exactly.

## Stage 3: engine separate from the editor

- `create(character)` → `update(time, input)` → `getPose()`, with no UI inside.
- Owns position, heading, gait blending, footstep planning, springs and morphs.

## Stage 4: renderer as a swappable layer

- The current canvas renderer reads the pose.
- A three.js renderer later reads the same pose.

## Stage 5: editor built from the definition

- Sliders generated from the character file.
- Save / load whole characters as text (copy and paste), and as files on w3schools.

## Stage 6: export (Mixamo-style)

- Bake loops and morphs into keyframes and export a GLB with the skeleton and animation clips.
  - Loops become looping clips; morphs become one-shot clips.
- Targets: three.js first; Unreal and Godot later (affects bone naming, axes, scale and frame rate,
  so keep the exporter's settings per engine).
- The built-in characters (sergal, robot and its skins) live in the app, so they export too:
  skeleton + animations, and their meshes.

## Stage 7: import and retarget

- Import a rigged GLB.
- List its bone chains, guess roles from names and positions, and let the user assign or fix each chain
  (leg, arm, neck, tail).
- Different bone counts: solve each chain so its tip reaches the planned target, spreading the bend
  along the chain; spread spine bend across however many spine bones the model has.
- Extra chains: rest pose, or spring "dangle" like a tail.
- Missing limbs: grey out gaits that need more legs than the model has.
- Both rigged and non-rigged models must be supported:
  - rigged GLB: map its bone chains to roles (above);
  - non-rigged mesh: auto-rig it first. Mark key points (hips, shoulders, each limb tip, heads, tails),
    build a skeleton from the character definition, then weight the mesh to it. Harder than retargeting,
    so it comes after rigged import works.

## Stage 8: game controls

- Player speed and direction pick the gait; actions fire morphs
  (for example, reversing while running triggers the skid 180).

## Stage 9: three.js prototype

- Terrain, a follow camera, and characters driven by the controls: the first playable piece of the game.

---

## Waiting for the go-ahead

- A realistic but still cartoony sergal with realistic hair. Not started; to be done when asked, in one of:
  - Blender (via Blender MCP), once the project moves there;
  - inside the app, as a new skin;
  - as its own standalone HTML file.

## Decided

- The sergal and the robot are two different skeletons. "One generic rig" means one shared builder that
  reads any skeleton description; it does not merge them.
- Moves belong to skeletons, not to one character: each skeleton description lists the moves it can do
  (for example, Ceiling is allowed for the robot now and for a future gecko skeleton).
- Planned future skeleton: gecko (wall and ceiling climbing).

- Imported models: both rigged and non-rigged.
- Engines: three.js now; Unreal and Godot later.
- Built-in models stay in the app and are exportable.

## Handoff (state at 2026-10-03)

Files:

- `tripod-walk-editor.html`: the app (single file). Deliver with a file send only; do not republish the artifact.
- `body-move-sketcher.html`: standalone keyframe sketcher for the robot body and 6 legs (user has edited it).
- `roadmap.md`: this file.

Test scripts (in the session scratchpad; run against `python3 -m http.server 8765` from the project folder):

- `full.py`: every mode pair, turns, spin, ceiling, over, leaving six; forwards, backwards and scrubbing. Must report 0 failures.
- `slide.py`: planted-paw drift per frame, walking straight and spinning, every robot mode. Should stay under about 0.05
  (a one-frame value at lift-off is not a slide).
- `bones.py`: bone lengths through every robot mode pair, ceiling, drop, over and spin. Must report "all bones within 3%"
  (currently under 0.1%). Not yet part of `full.py`.
- `golden.py` / `golden2.py`: golden frames. Out of date after the robot fixes; re-record the baseline before the next refactor.

Where things live in the code:

- Shared engine: `planFootstep`, `predictFoot` (has a spin branch that rotates round `SPIN.pz`), `solveLegIK`,
  `blendBones`, `splayV`, `faceHeading`, `smaxFloor`, `softMinAll`, `smin`.
- Robot: `buildRobot` — plan, body height (with `hang` on the ceiling), limbs (IK + hip yaw/roll), flip blends
  (ends/rise and the ceiling grab), then the bone rule (`BONETOL`, `BONEBAD`, `BONESHOW`), then drawing.
- Spin: `toggleSpin` / `turnStep` (`SPIN = {p0, h0, len, ts, pz, W}`, `SPINSTEP` sets how far a paw is carried per stride).
- Flips: `startFlip` (Drop swaps ends at the start), `flipStep` (Ceiling swaps ends on landing).
- Debug globals: `ROBFEET`, `SEGDBG`, `LASTMID`, `LASTHIPS`.

Next up:

- Add `bones.py` and `slide.py` checks into `full.py`, then re-record the golden frames.
- Then: editable morphs (sliders), or continue Stage 2 (merge the body builders), whichever the user picks.
- Waiting for the go-ahead: the realistic sergal.

## Open questions

- Jump to the three.js prototype sooner, or tidy the structure first?
- Should the sergal get the robot's abilities (flips, limb roles), or keep each character's moves exclusive?
- Should old saved settings text keep loading after the data-format change?
