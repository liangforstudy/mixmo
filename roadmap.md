# Roadmap

A procedural character and locomotion sandbox: build multi-limbed characters from parts, animate them
with procedural gaits, IK footstep planning and scrubbable multi-part transitions (morphs), and export
the results. Every motion comes from parameters, so the same settings always give the same result.

Long-term goals:

- A Mixamo-style tool: export skeletons and animations from the procedural system.
- A 3D JavaScript game built on the same engine.
- Import and export models as GLB and .blend.
  - GLB is the working format inside the app. A .blend file can only be read properly by Blender itself, so .blend
    files go through Blender (convert to GLB on the way in; open the GLB and save as .blend on the way out).
- Water physics inside transparent, rigged characters (pooltoy characters): water sloshes inside the body as it moves.
  - Going with faked slosh, drawn with the body as a mask: a world-level water surface, water shown only inside the
    body and below that surface. Springs tilt and wobble the surface; a fill slider sets the amount; the water line
    moves up or down so the amount stays the same when the body tilts. Flips pour the water to the lower end for free.
    No splashes; small extras (bubbles, a ripple on landing) can go on top. Best built once the renderer is three.js (Stage 4).
  - For rendering and export to Blender: real water particles. In the app, rendered frame by frame (not real time),
    the particles collide with a simple inside shape that follows the bones (capsules), and are drawn as one smooth
    water surface. For Blender, export the animated character plus that inside shape so Blender's own fluid
    simulation can fill it.
  - Output either as game-ready models and animations, or as rendered frames: frame by frame in the app, or in an
    external renderer such as Blender.

Constraint throughout: everything stays a single HTML file that runs on iPhone (Claude app preview and
w3schools) and on desktop browsers (mouse, trackpad and keyboard). Downloads only work from w3schools.

---

Contents: Plan at a glance; Part 1 Tracks (G, M, C, A, F, P); Part 2 Stages 0-9; Part 3 Rules and decisions;
Part 4 Log (finished work, dated); Part 5 Handoff (files, tests, where code lives).

---

## Plan at a glance (planner, updated 2026-11-11)

The one place to see what's done and what's next. Details live in the track sections below; keep this list in step
with them whenever something is finished or reordered.

How things are labelled (tidied 2026-11-09, because "step 2" meant four different things):
- Tracks (what's being built, Part 1): **G** Game, **M** Models (import), **C** Characters, **A** Animation soundboard,
  **F** Foot planting, **P** Pooltoys, **L** Looks. Items are numbered within their track: M2, C3, F5. The game's
  slices keep their letters: G-a to G-d.
- Stages (how the code is restructured, Part 2): always written "Stage 0" to "Stage 9". They are not steps of a track.
- Nothing else in this file uses bare numbers as names.

### Up next (in order)

1. [ ] **M4** Male sergal (no rig) fitted to the regular sergal's skeleton and weighted. (Models track)
2. [ ] **A1** Animation soundboard, robot flow. The game's action buttons will take over its job for the unusual
   animations. (Soundboard track) Its place before or after M4 is for the user to confirm.
3. [ ] **C2** Centaur: walk, gallop, idle, turns; the first character built mostly from shared pieces (Stage 2).
4. [ ] **C3** Sergal taur: horse or dog body; dragging his behind adds legs; walks like a horse, a dog or a centipede.

In progress / follow-ups:
- **M3** done 2026-11-11 (first version): Body preset Sergal / Fox on the regular sergal, with per-preset leg lengths.
  To review on the user's side: does the fox's run look lighter now? Not done: M2 tuning item 3 (hip roll and
  shoulder counter-twist), a plantigrade preset for fox_015, run on all fours.
- **M2** done 2026-11-09 (first version): imported models copy the regular sergal's moves. Parked by the user: run
  on all fours (the Female sergal should get it first, the fox later).
- **C1** Regular sergal (first version done 2026-11-09): still to do, the pull-apart hands over to him (each half after
  the split is exactly this character) and his own look (today he is the merged sergal's parts on two hips).

### Later (not ordered yet)

- [ ] **G-d** Game, shelved by the user (2026-11-08); order when resumed: seeded generated terrain, then pits, rivers
  (own simple water), crocodiles, flail / swim / dive animations; after rivers, the ceiling (tap to stick, a way down).
  Then Stage 9 (three.js game prototype).
- [ ] **F1-F5** Foot planting modes (agreed 2026-11-08): Off / Height only / Full plant, stride matched to speed, plant
  strength, plant only when slow, foot-slide readout.
- [ ] **L1** Fur: shell layers as a "3D look" option, a material that works on any body (parked 2026-11-08). With tubes
  built once, a shell is the same tube segments drawn again a little fatter and see-through, so it's cheap to add.
- [ ] **L2** Realistic (still cartoony) sergal with realistic hair: waiting for the go-ahead; L1 is the first step,
  the full look needs a sculpted body (Stage 7).
- [ ] **P1** Pooltoy water: faked slosh with a body mask; water particles for rendering and Blender export.
- [ ] **P2** Pooltoy characters: ring and no-ring pooltoys, inflating (garden hose, belly-button valve), deflated,
  packed into a box or bag.
- [ ] **C** ideas: gecko skeleton (walls and ceilings); colour-coded sergals; new creatures (snake, spider, bird,
  flying bird, bird humans, spider queen, mermaids).
- [ ] Editable morphs: sliders for timing, height, lean, part lengths.
- [ ] Animation soundboard rules written by the user (after A1).
- [ ] Stages: finish Stage 2; Stage 3 (engine separate from the editor); Stage 5 (editor built from the character
  definition); Stage 6 (export GLB with skeleton and animation clips); Stage 7 (import and retarget, sculpted bodies;
  M2-M4 are its first pieces); GLB / .blend export.

### Known issues

- [ ] Robot Walk on three: one 10-unit hip-turn step left (its swap happens while the paw is planted).
- [ ] Robot planted paw blocks sink about 2 units at the corners.
- [ ] Head-up 4/5-leg runs, "Swap ends": the head is hidden after the swap (temporary; user will look into it).
- [ ] Golden frames don't cover "Idle, third leg as a tail" or the regular sergal yet.
- [ ] Planted paws slide during turns (about 1 unit per frame at worst, 90° buttons and game steering alike) and up
  to about 1.7 mid-switch between animations; full.py doesn't test turns or switches (found 2026-11-08, see "Three ways
  to use the app"). The foot-slide readout F5 (Foot planting track) would show it live.

### Done

- [x] Two characters (sergal, six-limbed robot), procedural gaits, mode blends, morphs (90/180/skid, Over, Ceiling,
  Rise, Spin), IK footstep planning, terrain, robot skins and segments.
- [x] Robot rules enforced: no squashed bones, no sliding paws, ceiling respects gravity.
- [x] Lying 4/5/6-leg runs with swap-ends and turn-round 180s; robot dog run.
- [x] Desktop support: side-by-side layout, Auto/Touch/Desktop switch, wheel zoom, pan, wheel over dropdowns.
- [x] Stage 0 safety net (full.py, golden frames, rewind.py). Stage 1 characters as data (mostly).
- [x] Stage 2 so far: shared footstep planner, leg solver, blending, body pipeline.
- [x] Stage 4 started: three.js renderer from jsDelivr, 3D look panel (style, outlines, smooth limbs, real shadows,
  ground).
- [x] Sergal life cycle: grow the third leg, split the neck, pull apart; cycle order; inner-arm options; second idle;
  hidden ungrown leg and live drag readout (2026-11-08).
- [x] Scrubber shows 10 s on a phone, up to 30 s on desktop; exact step back/forward (2026-11-08).
- [x] Rewind by replay (last 30 s, scrubber over history); keeps the chosen animation on iPhone (2026-11-08).
- [x] Haptic tick on every button tap (iPhone label trick, Android vibrate); Haptic Lab. See "Haptic feedback" (Part 4).
- [x] Spin off winds down to the next 90° direction instead of stopping at an odd angle (2026-11-08).
- [x] Mode switch: Game / Animation player / Dev (started as a Dev on/off switch); advanced settings only in Dev
  (2026-11-08).
- [x] Game G-a to G-c (2026-11-08): steering with WASD (run), Shift or the arrows (walk); on a phone, drag in the
  left half of the view for a joystick, circle it to spin, flick it back for a 180; robot forms (walk, in-between
  dinosaur / kangaroo on Ctrl, run) and a T-pose emote; status line, timeline, pause / step and arrow-key stepping
  when paused.
- [x] C1 Regular sergal, first version (2026-11-09).
- [x] M1 GLB importer: load, show and read the rig; Baller Fox and Female sergal presets (2026-11-09).
- [x] Several imported models at once, each with its own settings (2026-11-09).
- [x] Fix: the small Timing chart above the gait sliders stopped updating after a character or animation switch (the
  slider panel is rebuilt, and the app kept drawing on the old chart). Found and fixed 2026-11-09.
- [x] M2 Imported models copy his moves: Statue / Copies his moves, in his place or beside him as a dance partner
  (2026-11-09).
- [x] M3 Fox preset: Body preset Sergal / Fox on the regular sergal, leg lengths per preset (2026-11-11).
- [x] Leg solver: the settings copy in `relStill` is made once per frame instead of ~60 times per leg (2026-11-10).
- [x] Three-legged sergal, Run (upright): new default leg timings from the user (tail leg 0.76, left 0.15, right
  0.51). Fix: leg and arm timings now blend the short way round the cycle when switching animations; before, walk or
  idle (tail leg 0) to run (0.76) ran the tail leg back through most of a step cycle (2026-11-11).
- [x] Three-legged sergal, Run (upright) heads (user's tuning at Happy, 2026-11-11): neck spread 22, head nod 2.5,
  heads glance 25 (were 28 / 6 / 3). Tired keeps its old values (22 / 6 / 1); the regular sergal's run (and its Fox
  preset) keeps 28 / 6 / 3.
- [x] Playback speed 1x / 1/2 / 1/4 (user, 2026-11-11): buttons at the right of the status line (`#rateSeg`,
  `PLAYRATE`). Slow motion for everything: the frame's time step is scaled, so motion, blends, turns, springs and the
  game slow together; touch-gesture timings stay in real time. Not remembered (a reload is normal speed); doesn't cut
  the rewind history. Checked: the cycle advances 0.41 / 0.20 / 0.10 per second in walk.
- [x] Fix (user's report, 2026-11-11): pressing and holding the step buttons did nothing until release. Now a tap
  steps one frame and a hold keeps stepping after 0.35 s, every 70 ms (`holdStep`); the release after a hold isn't an
  extra step. Long-press selection / callout turned off on those buttons. Checked in 2D: a 1.2 s hold = 13 steps.
  (In the cloud test browser, 3D is drawn in software at a few frames a second, which starves the repeat timer;
  use 2D for timing tests there.)
- [x] Fix (user's iPhone screenshots, 2026-11-11): Over on the robot, while rising onto the red end, the red paws
  floated and flailed (rise frames ~13-31). Cause: the switch Run on all six -> Walk on three tilts the body back up
  over 22 frames while the rise turns him over in 53, so for the first ~20 frames he tipped back towards the black end
  and the red paws went up to 43 off the ground. Now the rise's turn (`riseAng` in `buildRobot`) makes up whatever
  the switch hasn't: the tilt you see goes smoothly from lying to standing on the red end. Measured: the lowest red
  paw stays within 7.5 of the ground through the rise (was 43). Poses outside the rise unchanged.
- [x] Over, rise: all three red legs carry him (user, 2026-11-11: in the rise only one red paw was on the ground,
  lifting the whole body while the other two stepped). Each red leg now follows a plan (`riseLegPlan`): steps onto
  the ground where it is (0-15% of the rise), holds that spot, steps in towards the middle of the body as he comes up
  (one leg after another, 42-62%), holds again, then steps off into the walk (80-100%). Steps are arcs; each leg is
  bent to reach its spot with bone lengths kept (`reachChain`, FABRIK); the robot is lowered as far as the gripping
  legs need (`RISEDY`); toes lie flat, pointing outwards; forward travel stops while they grip (`riseTravel` in
  `perCycle`). Spots are kept on `FLIP.prints`. Measured: gripping paws move at most 0.07 a frame; paw blocks sink at
  most ~4 (the known corner sink); no pop at the end. Tried first and dropped: one spot per leg for the whole rise
  (by the end the spots were so far from his standing hips that he had to be lowered 70, then popped up).
- [x] Fix (user, 2026-11-11: "press Over 3 times after a factory reset"): the 2nd and 3rd Over went wrong. (1) The
  legs to plant were picked by paw colour, but the colours swap with every Over, so the 2nd Over planted the end being
  lifted; now it is always his top end in the build frame (`L.end==="T"`). (2) A spot further from its hip than the
  leg reaches dragged his hips to the ground; spots are now kept within 90% of the leg's length (sideways). (3) A leg
  folded tight (hip almost over its paw: the neck limb) put a knee or hock up to 29 under the ground; joints below are
  now lifted just above it and the leg re-bent from there (or the bend flipped). Checked with three Overs in a row from
  a fresh start: nothing sinks more than the usual paw-corner ~2-3 at any point; poses outside Over unchanged.
  Noticed, not changed: in the drop onto all six, the raised neck / arms swing down fast (up to ~20 a frame).
- [x] Power saving switch (2D and 3D) and a cheaper gait chart / status line (2026-11-08).
- [x] 2D debug picker "What's hiding it?" and camera readout; "3D debug, camera edition" (2026-11-08).
- [x] 2D renderer: robot box body sorted properly against hips, tail and legs (back face no longer covered) (2026-11-08).
- [x] "Start fresh" at the end of the editor: clears this app's saved settings and reloads as a first-time visit (2026-11-08).
- [x] 3D look switches no longer freeze playback: every shader is prepared in the background when three.js loads
  (2D keeps drawing until it's ready). Renderer switch now reads "3D (three.js) / 2D" (2026-11-08).
- [x] 3D tubes built once, bent on the graphics chip: 3D drawing about twice as fast (2026-11-08).
- [x] Fixes 2026-11-08: robot hip-turn pop, front legs stuck up in the dog run, gait chart redraw cost.

---

# Part 1: Tracks (what is being built, by topic)

## Game track (G): Three ways to use the app (user's plan, 2026-11-08)

Blockers check (2026-11-08): none. The engine already has a target heading and turn rate (`HEAD_T`, `OMEGA`) that
footstep planning uses (`predictFoot`), so free steering builds on what the 90° turns use. Keys: only Space is taken
(play / pause); WASD, the arrows and Shift are free. Things to watch: planted paws must not slide during free
steering (full.py's slide check); key presses while rewound must branch the history like clicks do; the 90° snapping
is for the turn buttons only (free steering faces any direction); joystick "up" should mean away from the camera.

- Game (the mini game; called "Simple player" at first): drive the character with a joystick instead of the turn buttons and the
  animation menu. Push the stick to walk that way, all the way to run; Ctrl and Shift change the sprint speed
  (keyboard). Generated terrain to roam.
- Animation player: today's player mode (animation menu, turn buttons, timeline and rewind, looks, terrain, power
  saving).
- Dev: today's Dev mode (everything else).
- Fits Stage 8 (game controls: speed and direction pick the gait, actions fire morphs) and Stage 9 (terrain, the
  first playable piece).
- G-a, done 2026-11-08:
  - "Mode: Game / Animation player / Dev" replaces the Dev on/off switch (remembered as `mixmoTier`; an old Dev "on"
    becomes Dev). "Advanced player" renamed "Animation player" (the Mixmo idea). Game hides the animation menu, turn
    buttons, timeline and status line (class `anim`), shows a controls tip (`#gameTip`), and keeps playing.
  - `gameInput` / `gameStep`: WASD = Run; with Shift = Walk; arrows = Walk; nothing pressed = Idle (mode switched via
    the animation menu's own code, so blends work as usual). Direction as seen from the camera (W away, D right; checked
    for both characters). Keys pressed while rewound branch the history. Ctrl / Cmd / Alt combos are ignored.
  - Turning: the turn rate eases in and out (at most 7 rad/s², up to 3.0 rad/s running / 2.2 walking, slowing as he
    nears the new direction). A sudden rate change made planted paws jump up to 13 units, because the footstep
    planner assumes the rate changes smoothly.
- Fix (user's screenshots): switching Mode left the view's picture at its old size (squashed or stretched) until the
  divider was dragged, because the view only resized on a window resize or a divider drag. Now the view watches its
  own size (ResizeObserver on the canvas) and resizes whenever it changes, whatever the cause.
- Known issue found on the way: in live playback, planted paws slide during turns. The worst single-frame slide is
  about 1 unit, both for the existing 90° buttons and for game steering. Mode switches from the menu slide up to about
  1.7 mid-blend. full.py only checks straight lines and spins after a switch has finished, so it never saw this.
  Worth a turning and blending slide check, then a fix.
- G-b, reworked 2026-11-08 (user's design): the round show/hide button is replaced by a touch control area, a
  translucent box over the left half of the view saying "Tap and drag here to move." Touching anywhere in it puts a
  joystick under the thumb (`#stickZone`, floating `#stick`). The box's tint and label disappear after the first
  touch (the area keeps working) and come back when the page is reloaded (not remembered). Shown in Game on the
  touch layout only; on the desktop layout the mouse orbits everywhere and the keys steer. The right half still
  orbits / zooms the camera. Tested: run at full push, walk at a small one, idle on release, camera unmoved by the
  stick, right-half drag turns the camera, label back after reload.
- Spin gesture made forgiving (user: thumb circles don't reach the edge, 2026-11-08): counts from 30% out (was 60%),
  and a dip towards the centre under 0.4 s keeps the count instead of starting over. Tested: small even, small wobbly
  and big wobbly circles all start the spin after 1.5-2 turns; tiny circles near the centre and steering back and
  forth don't.
- Reversal (user's report, 2026-11-08): flicking the stick (or the keys) to the opposite direction while walking or
  running now plays the 180 turn towards the new direction, with the skid when running fast, instead of steering
  round in a curve. "Flick" = the input pointed more than ~140° away within the last 0.3 s (`GHIST`), he faces more
  than ~115° away from it, and he's moving (walk / run, travel 40+). Setting off from standing or sweeping the stick
  slowly round still just steers. `startTurn(kind, exact)` turns by the exact angle for the game (the turn buttons
  still square up to a main direction). Tested both characters: run flick → skid 180, walk flick → 180 (178-179°),
  W then S → skid 180; set-off and slow sweep → no turn animation.
- Robot forms (user's idea, 2026-11-08): his other animations become choices in the game. Panel "Robot forms" under
  the view (Game, robot only; remembered, `mixmoForms`):
  - Walk: on three / on two, tail up. Between (an in-between speed): Off / Dinosaur / Kangaroo hop. Run: any of the
    eight runs (upright, tail up, dog, on four, the three five-leg runs, all six).
  - Joystick zones: under 50% walk, 50-82% the in-between form, 82%+ run. Keys: WASD run, Shift / arrows walk, Ctrl
    = the in-between form (user's choice). Ctrl+A / S / D are blocked from selecting / saving / bookmarking; Ctrl+W
    closes the tab on Windows and pages can't stop it (fine on a Mac), so the tip suggests Ctrl with the arrows.
  - T-pose is an emote: a "T-pose" action button in the view while he stands still (`EMOTE`); tap again or move to end.
  - Steering follows the way he actually travels: in a lying run that has swapped ends he travels backwards, so a
    flick back swaps ends and he heads off the new way. The flick 180 now works in any moving form.
  - Tested: zones give walk / dino / run; Kangaroo, walk on two and all six apply; all-six flick swaps ends and he
    travels toward the new direction; T-pose plays and ends on moving; Ctrl + arrow and Ctrl + D give the in-between
    form with no bookmark dialog; the panel and button hide for the sergal.
- Fix (user's screenshots, iPhone): the Robot forms panel and the long game tip sat in the top pane with the view, so
  opening the panel squeezed the view to nothing, and three.js then failed on the zero-sized view ("Script error." in
  the console: errors from a script loaded off another site are hidden that way). Both now sit at the top of the
  editor (bottom pane); the view keeps the top pane. Also, nothing is drawn while the view is under 8 px either way.
- Fix (user's report, 2026-11-09): after a 180 turn with the keys he jogged a bit before stopping. The game froze his
  speed while a turn played, so letting go mid-turn only took effect afterwards (he left the turn at travel 175 and
  drifted 54 units). Now his speed follows the input during a 180 turn too (steering still waits for the turn to end;
  during a Spin speed stays frozen, as the stick is out while circling). Tested: let go mid-turn -> standing still
  when it ends; holding S -> runs off the new way; a running reversal still skids.
- Game now also shows the status line (LOOP / MORPH, animation or morph part, frame) as debug info, and the timeline:
  Pause / Play, step back / forward and the scrubber (user, 2026-11-09). While the scrubber is being dragged the game
  controls are ignored (keys, joystick, steering), so the scrubber wins; after letting go, a key or the stick carries
  on from that moment (cuts the history there, like any change while rewound). Tested: W pressed mid-drag stays
  rewound; after release W goes live and runs.
- Left / right arrow keys = the step buttons (user, 2026-11-09). Animation player and Dev: always. Game: only while
  paused or rewound (playing, the arrows walk); WASD or Space carry on. A focused slider or menu keeps its own arrow
  keys (the scrubber excepted). Button tooltips and the game tip mention it. Tested in all three modes.
- G-b, first version (replaced):
  - A round button in the bottom-left of the view (Game only) shows / hides the joystick (remembered, `mixmoStick`);
    the game tip says it's there. Push a little = Walk, all the way (80%+) = Run, centre / let go = Idle; up = away
    from the camera, like the keys. The stick wins over the keys while held. Its touches never reach the view (no
    orbit, reset or hold flash), so a second finger can still orbit / zoom the camera.
  - Secret Spin: circle the stick about one and a half turns (pushed well out) to start a Spin; it keeps spinning while
    you keep circling, and winds down to a main direction once you stop or let go (`stickSpinStep`). The tip hints:
    "Psst: try spinning the joystick round."
  - Tested with pointer drags: walk / run / idle by push distance, camera unmoved, spin starts, keeps going while
    circling, ends square on.
- Decided (user, 2026-11-08):
  - Phones: an on-screen joystick, hidden by default; a tip tells the player it's there.
  - Desktop: both WASD and the arrow keys. WASD on their own = sprint. Shift = slow down (WASD + Shift = walking
    speed). The arrow keys are simply walking speed, i.e. the same as WASD + Shift (a little troll for players).
    Ctrl does nothing.
  - Spin: spin the joystick round (a "secret" move, like some games have).
  - Ceiling: when he's under a ceiling, tap (or click) the ceiling to make him stick to it; on desktop a tip says so.
    Getting back down on a phone: open question (ideas: tap the floor under him; a "Drop" button that only appears
    while he's on the ceiling; pull the joystick down hard).
  - Terrain ideas for ceilings (user, 2026-11-08): pits, rivers, or rivers with crocodiles under a ceiling, so he can't
    come down there and has to cross along the ceiling. Dropping over a hazard is allowed: he falls in, for a splash
    or a crocodile chase (user liked this, 2026-11-08).
  - River water: its own simpler water system, separate from the pooltoy water (user, 2026-11-08). The pooltoy water
    sloshes inside a body; a river only needs a moving surface, a splash and maybe swimming, so it can stay simple.
  - New animations this needs (user, 2026-11-08), for each character: flailing (falling, or in trouble in the water),
    swimming, and a dive (when the water below has no hazard in it, he dives in instead of falling).
  - The game's action buttons will cover the soundboard's job for the more unusual animations (an action button per
    unusual animation, offered when it fits).
  - Terrain: generated from a seed (the same seed gives the same world). Camera controls: the same as today.
  - More to come from the user.

## Models track (M): importing the user's models

One biped-with-a-tail character with presets, sergal and fox (user, 2026-11-09). In order:
- **M1** GLB importer: load a GLB, show it, read its rig; Baller Fox and Female sergal presets. Done 2026-11-09.
- **M2** The model walks with the app's gaits (the regular sergal's pose drives the mapped bones). Done 2026-11-09.
- **M3** A fox preset made from the Baller Fox's bone lengths (needs per-character leg lengths). Done 2026-11-11.
- **M4** The Male sergal (no rig) fitted to the sergal skeleton and weighted (Stage 7 non-rigged path).
Clothes come later as outfits (body-only first); cheap cloth = spring bones.

### M1: GLB importer (done 2026-11-09)

- User's choice: show the model first, walking later. Presets: Baller Fox (one preset), Female sergal (the second).
- Editor panel "Import a model (.glb)" (Animation player and Dev): choose a .glb (Files on a phone; nothing is uploaded,
  gone on reload). Loading three.js and the GLB reader happens on demand; in 2D the panel offers "Switch to 3D".
  Errors are shown in the panel (offline, a .gltf with separate files, a broken file); the rest of the app keeps going.
- Shown in the 3D view: "Beside him" (fixed in the world, 120 units to his right, facing his way) or "In his place"
  (stands where he is, turns with him, and he is hidden); scaled so its height matches his (156, ears included), with a
  size slider (25-200%); "Bones: Shown" draws the skeleton on top. "Remove" frees it.
- Info: file size, meshes, triangles, materials, textures, bones, face / shape keys, animations, height in file units;
  the rig: which preset it matched (or "guessed"), a part -> bone table (hips, spine, chest, neck, head, legs with
  toes, arms, tail chain), left-leg proportions as % of hip height (compare with his: hip 78, thigh 30, shin 30, foot
  22), the preset's notes, and the full bone tree.
- Bone names compared loosely (`boneKey`): Blender's glTF suffixes ("_090_98"), case, spaces and the characters
  three.js strips from names are ignored. Presets (`MPRESETS`) need a few key bones to match: Baller Fox (hips,
  headbone, thighl, shinl, footl, tailroot, lowerchest), Female sergal (hips, llegupper, lleglower, lfoot, ltoes,
  tail1, tailend, chest), fox_015 (hips, spine, thigh / shin / foot). Other rigs: `mdlGuess` (Blender, Mixamo,
  VRM-style names, prefixes like "mixamorig" stripped). Tested with made-up GLBs: a Baller-Fox-named rig (preset found,
  all parts), a Mixamo rig (all 15 parts guessed), a mesh without bones.
- Rigs read from the user's Blender files (2026-11-09):
  - Baller Fox: 111 bones. Hips -> spine -> Lowerchest -> upper chest -> neck -> HeadBone (jaw, eyes, ears 2 x 4, hair
    17, face fluff); shoulder / upper_arm / forearm / hand with fingers; thigh / shin / foot; TailRoot + tail1-10;
    breast and butt bones. Legs: hip 1.22 m, knee 0.73, ankle 0.06 (thigh 0.51, shin 0.71). T-pose.
  - Female sergal: 107 bones, in centimetres. Hips -> Spine -> Chest -> Neck -> Head (ears, hair chains); l/r
    Shoulder, ArmUpper, ArmLower, Hand with fingers; l/r LegUpper (hip 110), LegLower (knee 62), Foot (ankle 3.8),
    Toes; Tail1, Tail2, Tail2.001-.004, TailEnd. T-pose. 19 face shapes.
  - fox_015: Hips, Spine, thigh / shin / foot L / R (8 bones).
- GLB files exported for the user (2026-11-09, with the settings above, no animation): `fox\fox_015.glb` (11 MB:
  body, rig, eyes), `sergal\Female\female_sergal_body.glb` (26 MB: body, hair, jewels, no shirt / shorts / dress),
  `Baller Fox\baller_fox_body.glb` (8 MB: body, face, ears / tail; no socks or sweater dress). They couldn't be copied
  into the session (folder access was declined), so the real files are untested here.
- Fix 2026-11-09 (user's screenshots: the Female sergal lay on her back, tail hanging into the floor): her Blender rig's
  rest pose lies down and her standing pose is a pose (Hips turned 90°; the armature object is turned -90° and scaled
  100, left over from the Sketchfab import). Exported with "Use Rest Position" on, the GLB got the lying rest pose.
  Re-exported with it off (same file); the GLB's hips are now turned upright. The Baller Fox's export was already
  upright. The app now warns when a recognised model lies down (hips-to-head not pointing up) and says to export with
  "Use Rest Position" off. Rule from now on: export these Sketchfab-born rigs with "Use Rest Position" off.
- Fix: the bone overlay fanned out lines from the feet: Blender's glTF importer leaves zero-size "..._end" tip bones,
  which here sit at the origin. The overlay is now the app's own lines (bone to parent), skipping "_end" bones.
- The importer also shows in Game (user, 2026-11-09): choose / remove, where, size and the lying-down warning; the
  technical details (bones switch, counts, rig table, proportions, bone list) are for Animation player and Dev.
- Tested with the user's real files (attached to the chat, 2026-11-09): Baller Fox (111 bones, 70k triangles, preset
  found, textured: orange / white / black) and Female sergal (107 bones, 64k triangles, preset found, upright after
  the re-export). The Female's textures do load; her body texture is a plain mid-grey with dark claws (same in
  Blender's material preview), so she looks untextured.
- Fix (user: "when they turn 180 they turn round a point behind the legs"): models were centred on their bounding
  box, which the tail pulls back about 40 units. Now the turning point is between the feet (ankles and toes), or
  under the hips, or the box centre without a rig. Checked: both feet now sit either side of the turning point.
- Fix (user's iPhone screenshot, 2026-11-09): the iOS file picker greyed out .glb files (iOS has no file type for
  .glb, so the picker's filter matched nothing). On iPhone / iPad the filter is dropped and every file can be picked;
  the app then checks the file starts with "glTF" (or is a .gltf text file) and otherwise says it isn't a GLB.
  Desktop keeps the .glb / .gltf filter. Tested with an emulated iPhone 13: a .txt is refused with that message, the
  Baller Fox GLB loads.
- No haptic tick on "Choose a .glb file" (user, 2026-11-09): it opens the system file picker, which gives its own
  feedback. Any button can opt out of the tick with `data-nohaptic`.
- three.js now loads from jsDelivr's ESM build (`three@0.170.0/+esm`) so the GLB reader (`GLTFLoader.js/+esm`) shares
  the same copy of three.
- M2 plan (as written before it was built): drive the mapped bones from the regular sergal's pose: hips position and turn, spine lean, thigh /
  shin / foot angles (the rig's rest pose as the zero), arms from T-pose down to his arm angles, tail chain, head.
  Leg lengths differ, so feet are placed by IK on the model's own leg lengths. Then the presets' proportions feed the
  regular sergal (per-character leg lengths).

### M2: models copy his moves (done 2026-11-09)

- User's choices: a switch between a statue and copying his moves, both in his place and beside him ("dance
  partner"); run on all fours parked (Female sergal first, the fox later).
- Panel: "Pose: Statue / Copies his moves" (all tiers). Copies his moves needs the regular sergal; picking it switches
  to him, and with another character the model stands as a statue and the panel says why. While it moves the size
  slider is off: the model is sized so its hips are as high as his (that keeps the footprints the right size for its
  legs, so planted feet don't slide).
- How: the regular sergal's builder records his skeleton each frame (`REC`: body frame, each leg's hip / knee / hock /
  paw / toe, arms, neck and head frame, tail points; turned to his heading). `mdlDrive` then, from the model's rest
  pose each frame: hips take half his torso's turn and lean (spine 75%, chest all of it) and move so the thigh heads
  sit on his hip joints; if a footprint is out of reach the hips lower until it fits (as he crouches); each leg is a
  two-bone solve on the model's own thigh and shin lengths, ankle placed over his paw at the model's own ankle height
  (minus the toes' reach for the Female sergal), knee bent towards his knee; feet stay level, turned his way; upper
  arms and forearms point the way his do (out of the T-pose); the neck points along his neck and the head copies his
  head's turn and nod; his tail curve is laid along the model's tail bones by length. Set up once per model
  (`mdlMotionSetup`: rest pose, which way each bone points, leg lengths, ankle heights, tail fractions).
- Checked with the user's files: planted feet sit at the model's own ankle height (Baller Fox 3.9, Female sergal 3.0)
  and slide at most 0.05 in idle, walk and run (the app's own limit); before the hip-lowering the run slid 0.33.
  Screenshots: idle, walk, run from the side and three-quarter, dance partner walking and turning, spin in place,
  game run with W. Her head is tipped 3° from her statue pose, which is just how she's modelled.
- Known limits: the dance partner swings round him when he turns (its feet slide in turns); on hills the partner
  stands at his ground height, not its own; the Baller Fox's raised hock is inside her shin bone, so it can't bend on
  its own; hair, ears, face shapes and clothes don't move yet (spring bones later); run on all fours isn't tuned (the
  hands follow his, from a T-pose rig).

### M2 tuning, round 1 (2026-11-09, user's review)

- User's review: Baller Fox the clear winner; Female sergal's top leaned forward in idle; her walk looked like the
  "foot magnet"; running stiff for both; the fox should take longer strides when running (looks heavy). Order agreed:
  1 and 2 now, then 3 and 4 below.
- 1, done: posture. The neck used to copy his neck's angle (about 9 degrees forward), which suits the fox (her neck
  leans that much already) but pushed the Female sergal's upright neck forward. Now the neck turns by how far his neck
  moves from where it rests on his body. Measured: her neck 1.7 degrees back while copying his idle (1.5 as a
  statue); the fox's unchanged.
- 2, done: feet. They used to stay flat all the time. Now the ball of the foot sits on his footprint and the foot
  pivots on it: the heel lifts as the foot falls behind the hip (up to 35 degrees), the foot hangs toes-down in the
  air (up to 30), levelling as it lands; the Female sergal's toes stay flat while her heel lifts. The fox has no toe
  bone, so her ball of the foot is estimated (30% of the shin ahead of the ankle). Measured: the ball of the foot
  slides at most 0.05 in idle, walk and run, both models.
- 3, next: running loosened up: hip roll and shoulder counter-twist, so the upper body isn't one block.
- 4, next: the fox's longer, lighter run: a per-model stride setting (her legs are a little short for his run
  footprints, so her hips drop to reach them); first piece of her preset (M3).

### Leg timings blend the short way (fix 2026-11-11, user's report)

- User set new Run (upright) timings for the three-legged sergal (tail leg 0.76, left 0.15, right 0.51; now the
  defaults) and saw the tail leg animate strangely when switching walk / idle to run and back: the switch blended
  each setting in a straight line, so the tail leg's timing went 0 -> 0.76 through most of a cycle.
- Timings (`ph...`, `uPhase`, `lPhase`; `PHASEK`) are positions round the cycle, so the blend in `frame` now takes
  the shorter way (0 -> 0.76 is 0.24 back) and wraps into 0-1. Measured: the tail leg's timing moves 0.24 of a cycle
  during each of walk / idle <-> run (was 0.76). Poses outside switches unchanged except the new run defaults.

### M3: Fox preset (done 2026-11-11)

- The roadmap's decision (user, 2026-11-09): one biped-with-a-tail character with presets. So the regular sergal got
  a "Body preset" panel (Legs: Sergal / Fox), shown for him in every mode, remembered (`mixmoPreset2`), kept in Save &
  load (`preset`). Changing it rebuilds him like a character switch (same animation) and clears the rewind history.
- Measured from the Baller Fox GLB (2026-11-11, the user attached the body GLBs). Her rig: hip 1.22 m, knee 0.73,
  ankle at the ground. The raised hock is in the mesh, not the bones, so it was read off the leg's outline: hock at
  0.39 m (32% of hip height), ball of the foot at the ground. Thigh 0.51, shin (knee to hock) 0.50, raised foot (hock to
  ball) 0.38. Stance: thigh 14 deg forward, shin 48 back, foot 31 forward.
- Finding: in proportion, her leg is almost exactly his (30 / 30 / 22 = 0.51 : 0.51 : 0.37). What differs: her legs are
  longer for her upper body (hip to head bone 0.72 m against a hip height of 1.22; he has 73 to his hips and 58 more
  to his head), she stands more bent with the hock high, and copying him shrank her to his hip height.
- Fox preset: legs 40 / 39 / 32, toe 7, hips at 92 (his: 73). Stance per mode: idle 14 / 62 / 79 (thigh / knee /
  hock), walk 12 / 62 / 79, run 24 / 69 / 86, gallop 26 / 69 / 86. Gait scaled the usual way for longer legs: cycles
  per second x0.88, ground speed x1.14 (distance per cycle x1.3); less bounce (walk 2, run 4.5, gallop 2.5). Its own
  slider values (`DEF2F` / `PS2F`), separate from the sergal preset's.
- A model copying him is still sized so its hips are as high as his, now with the preset's legs (`mdlBase`). With Fox,
  the Baller Fox's head is level with his (before, her hips matched his and she came out smaller). Her file height
  (2.75 m) includes the raised tail and ears, so "height" numbers for her are bounding-box heights.
- The camera aims 9 higher for the fox preset (half his extra height, `camAim2`), in 2D and 3D.
- Ball of the foot for rigs with no toes bone: was 30% of the shin ahead of the ankle (0.21 m on the Baller Fox, past
  the tip of her paw at 0.14). Now half way to the paw's tip, read off the vertices the foot bone moves (`mdlFootTip`):
  0.074 m. The Female sergal has a toes bone and is unchanged.
- The model's card tips: the Baller Fox with the Sergal preset suggests Fox; the Female sergal with Fox suggests Sergal.
- Checked (test browser): Sergal preset and the other characters unchanged (4,416 poses identical). His planted paws on
  straight lines: worst 0.05 a frame with Fox legs (0.08 with the sergal's, as before). Turns not measured reliably by
  that test. Baller Fox copying him, hip drop (hips lowered to reach a footprint): idle -0.4, walk -0.2 avg / 1.9 max,
  run 2.2 / 4.3 (Sergal preset: 1.1, 1.3 / 2.7, 1.1 / 3.8). Run on all fours still crouches 40 (not tuned). Pose cost
  per frame unchanged.
- Not done: M2 tuning item 3 (hip roll, shoulder counter-twist); a plantigrade preset for fox_015; the fox's own look
  on his body (still the sergal's parts); run on all fours.

### Model warm-up for the GPU (2026-11-10, user's suggestion)

- User: "ask the GPU to load shaders once the GLB model is added, so the CPU doesn't have to wait when I pull down the
  drawer". Before, a new model's shaders were only built on the first frame that showed it, so showing the view
  froze for a moment. Now `mdlWarm` runs right after loading ("Getting ... ready for the GPU..."): it uploads the
  model's textures, builds its shaders in the background with and without the sun's real shadows (three.js
  compileAsync), then draws one frame with shadows on, which builds the shadow pass's shaders (compileAsync skips
  those). That frame goes to the screen, not off screen: tone mapping is part of a shader's recipe, so an off-screen
  frame built the wrong ones.
- Measured (test browser, view hidden while loading, then shown): the slowest frame when the view appears went from
  0.40 s to 0.02 s with the Female sergal, 0.13 s to 0.01 s with the Baller Fox. With no model, showing the view
  costs nothing either way.
- Fix (user, same day): the model's settings card only appeared after the warm-up finished; it now appears as soon as
  the model is unpacked, while "Getting ... ready for the GPU..." still shows.
- Fix (user's iPhone, same day): "Getting ... ready for the GPU..." never went away. The warm-up waits for the GPU to
  report every shader ready, which on the iPhone didn't happen (or never finishes). The wait is now capped at 4 s;
  after that the message goes and the warm-up carries on by itself. Tested with a warm-up that never finishes: the
  message clears after 4 s and the model's card and the add button work.
- Then made honest (user: "it should be honest about it"): instead of a fixed 4 s cap, the panel counts the model's
  shaders the GPU has confirmed ready ("Getting X ready for the GPU: 1 of 3 shaders confirmed..."). If they're all
  confirmed the message goes; if after 8 s some still aren't, it says so: "The GPU hasn't confirmed 2 of X's 3 shaders,
  and it may not say when. The model works; the first look at it may pause for a moment." It keeps checking for 2
  more minutes and clears that message if the GPU confirms them after all. Tested with a faked GPU that never
  confirms some shaders, and one that confirms late. With the test browser's GPU, every shader is confirmed at once.
- From the user's Safari timeline recording (iPhone, 2026-11-10, 56 s): added the Female sergal at 26 s (unpack and
  texture upload 0.16 s, expected), again at 38 s with "0 of 8 shaders confirmed", then pulled the drawer down at
  47 s: a 0.22 s freeze. Cause: Safari only really builds a shader the first time it draws with it and never reports
  one ready before that, and the warm-up's drawing step waited for that report, so on the iPhone it never ran. Fix:
  the warm-up now draws its two frames (sun shadows on, then off) straight away, without waiting. Test browser: the
  view-appears freeze stays at 0.02 s (was 0.41 s). To confirm on the iPhone: the count should now reach "8 of 8".
- Also seen in the recording: about 11% of the app's sampled time is copying the leg settings object in `relStill`,
  called many times a frame by the leg solver (`{...p}`) (the phone sat at about 30% CPU while walking).
  Fixed 2026-11-10: both leg solvers (sergal `buildRig`, shared `buildRobot`) copy it once per frame (`pStill`);
  `legChain` only reads it. Poses identical (4,416 frames: 3 characters, every animation, 4 terrains). The gain is
  hard to see on desktop Chrome; to confirm with a new Safari timeline recording on the iPhone.
- Found on the way: an old bug in `r3applyLook`, a code comment that swallowed `R.shadows.visible=!real;`, so the
  soft shadow spots never switched off when real shadows were on (both drawn at once). Fixed.

### Several models at once (2026-11-09)

- User asked to load more than one GLB character. The panel ("Import models (.glb)") now keeps a list: "Add a .glb
  file" (several files can be picked at once; they load one after another), and each model gets its own card with
  Remove, Where, Pose, Bones, Size and its details. At most one model stands in his place (choosing it for one moves
  the other back beside him); the others take turns either side of him: right, left, further right, further left
  (120 units apart). With more than three models the panel warns that it can be too much for a phone.
- Tested: Baller Fox, Female sergal and a Mixamo test rig loaded together; the fox and the female copy his moves on
  either side of him, the third stands as a statue; swapping who is in his place; removing one.

### The user's models: files, export settings, body checks (2026-11-09)

The user's model: `D:\Claude_Projects\Blender-5.2-LTS\Projects\sergal\Male\Male_sergal.blend` (Blender 5.2.2), checked
over the Blender connection:
- A regular sergal: one head, two legs, two arms, one tail. The regular sergal character now exists in the app
  (2026-11-09), so the mesh can be fitted onto his skeleton (M4).
- Contents: an empty "Sergal" with four meshes (Object_2-5, about 9,900 faces), one UV map each, custom normals;
  three materials, each a colour texture packed in the .blend (2048, 512, 512 px). mat2 / mat3 have an alpha cut-out
  (Math nodes: transparent below 15% opacity), which is how Blender imports glTF "mask" transparency; the exporter
  writes it back. No rig, shape keys, modifiers or animation. About 30 units tall (30 m in glTF); the app scales on
  import. Came from Sketchfab (originally glTF), so GLB is close to lossless.
- Export (File > Export > glTF 2.0): glTF Binary (.glb); Include: cameras and punctual lights off; +Y Up on; Mesh: UVs
  on, Normals on, Tangents off; Material: export, Images Automatic (PNG; not JPEG / WebP); Draco compression off
  (lossy, and needs a decoder); animation / shape keys / skinning: nothing to export.
- To check before it goes in the app: the model's licence on its Sketchfab page (CC BY needs credit to the author).
- Offered: run the export from Blender and verify it by loading the GLB back and comparing faces, UVs, normals,
  textures and transparency.

Female sergal (the rigged one), `...\sergal\Female\female_sergal_clothed.blend` (checked 2026-11-09):
- 107-bone rig (`Object_6`, fingers included; no constraints; all bones deform; bone display shape = Icosphere, not
  exported). Body in 7 skinned parts with 20 shape keys each ("target_0"-"target_18", the importer's names); the
  "Scene" action animates only those shape keys (400 frames). Skinned hair, shirt, shorts, dress (separate meshes:
  could become outfits). Max 4 bone influences per vertex (glTF's limit: nothing trimmed). Normal maps on shirt and
  shorts; the dress uses soft transparency; mouth / teeth / eyes have emissive textures. Armature parent empty is
  scaled 100 (centimetre-style import), harmless.
- Export: right-click "Sergal" > Select Hierarchy, Include > Selected Objects (skips camera, light, Icosphere);
  glb; +Y Up; UVs, Normals, Tangents on (normal maps); Material export, Images Automatic (PNG); Shape Keys on with
  Shape Key Normals; Skinning on, Use Rest Position on; Animation on with "Limit to Playback Range" OFF (400 > 250
  frames); Draco off.
- Fits Stage 7's rigged path (map her bone chains to roles), unlike the male model.

Baller Fox, `...\Baller Fox\baller_fox_006.blend` (checked 2026-11-09):
- 1.97 m (real scale). 111-bone rig (head, jaw, eyes, ears, face fluff, 17-bone hair chain, fingers, breasts, legs,
  10-bone tail); body, face, ears/tail, socks, sweater dress, all skinned, max 4 influences; no animation or shape keys.
  Every material multiplies its texture by a vertex colour that is plain white (no effect). The socks' opacity is 0
  (invisible, maybe intended: the root is named "Redux/No clothes"); the exporter keeps that.
- Leftovers: hidden Cube, a one-vertex junk mesh "Object_125.001", six importer "correction" empties with nothing
  attached, six lights.
- Export: Select Hierarchy on "Baller Fox (Redux/No clothes)", deselect Object_125.001, Include > Selected Objects;
  glb; +Y Up; UVs, Normals on, Tangents off; Vertex Color: None (all white); Material export, PNG; Skinning on, Use
  Rest Position on; Draco off.

Cartoon 4-legged fox, `...\Cartoon 4 legged fox\4 legged fox.blend` (checked 2026-11-09):
- Static, no rig: about 1.5 million faces / 900,000 vertices in 14 pieces (split at 65,532 vertices: glTF's 16-bit
  index limit), 0.84 x 0.80 x 0.73 m. One material: 4096 px colour, metal/roughness (already in glTF's channel
  layout) and normal map. 4 UV maps per piece: colour uses the first, metal/roughness the second, normal map the third
  (they look identical), the fourth is unused. .blend is 103 MB.
- Export (lossless master): Select Hierarchy on "Sketchfab Model", Include > Selected Objects; glb; +Y Up; UVs,
  Normals, Tangents on; Material export, PNG; Draco off. Expect a GLB around 100 MB.
- Too heavy for the app on a phone as it is (about 50x the others). For the app it needs a lighter copy (fewer
  faces, 2048 / 1024 px textures): lossy by nature, so keep the master. It also needs a four-legged skeleton (fits
  the dog / horse work for the taur).

User's own fox sculpt (work in progress), `...\Animal world\models\fox\fox_015.blend` (checked 2026-11-09):
- "Fox_Body": a sculpt, about 148,000 faces (around 15x the male sergal: fine on desktop, heavy-ish on a phone),
  1.06 x 0.83 x 1.24 m, flat-colour materials (orange, dark "sock"; eye white) that export exactly; its colour
  attribute is plain white (unused). "Fox_Body_PoseRig": 8 bones, legs and spine only (Hips, thigh / shin / foot
  L / R, Spine); no head, arm or tail bones yet. Eyes ("Fox_Eye.L/R") are separate and not attached to the rig, so
  they'd stay behind if the spine bends.
- Hidden: a primitive blockout (Fox_Blockout), cap / bandana clothes (not attached), a "WeightSnapshot" body copy;
  three reference-image empties (Refs).
- Before importing: attach the eyes to the Spine bone (select eye, then rig in Pose mode with Spine active,
  Ctrl+P > Bone) or weight them; the rig needs head / arm / tail bones for more than leg poses.
- Export: select Fox_Body, Fox_Body_PoseRig, Fox_Eye.L, Fox_Eye.R; Include > Selected Objects; glb; +Y Up; UVs,
  Normals on, Tangents off; Vertex Color: None; Material export; Skinning on, Use Rest Position on; Draco off.

Clothes (decided with the user, 2026-11-09): import the Female sergal and the Baller Fox body-only first. No need to
delete anything in Blender: the clothes are separate meshes, so the export simply leaves them out of the selection.
- The clothes aren't cloth-simulated now; they're skinned to the bones (move rigidly with the body), like most games.
  Weak spot: a dress or skirt cuts through the legs in a long stride.
- Later, cheapest first: (1) skinned as they are, fine for close-fitting clothes (tops, shorts, socks); (2) spring
  bones in the hem, hair or tail that lag and swing, same idea as the app's thigh spring / head steadiness, cheap
  enough for a phone (the Baller Fox already has a 17-bone hair chain); (3) real cloth simulation: heavy in a phone
  browser, better for frame-by-frame renders in Blender.
- Checked 2026-11-09: the Female sergal's body is complete under the clothes (looked at front, back, side with the
  shirt / shorts / dress hidden; no holes). The Baller Fox's body is complete too (checked the same way, 2026-11-09, with the sweater dress and socks hidden).
- Cheap cloth for phones (researched 2026-11-09, user asked): spring bones first. Short bone chains (hair, skirt
  hem, tails) that lag and spring back (stiffness, gravity, drag), with small sphere colliders on the thighs etc. that
  push them out of the way: the standard for anime-style / VRM avatars, costs a few dozen bones a frame. Build our
  own (the app already has springs; pixiv's three-vrm-springbone exists but is built around VRM). The Female's dress
  has no skirt bones: the app could add a ring of short chains round the hem with leg colliders; the Baller Fox's
  hair chain (17) and tail (10) could swing straight away. Later, if needed: a coarse proxy cloth (a few hundred
  simulated points the detailed dress follows). Full cloth on the real mesh (her dress ~15,000 vertices) is too heavy
  for a phone: Blender renders only. Sources: VRM spring bone guide (wiki.virtualcast.jp), three-vrm-springbone,
  80.lv on a Magica Cloth dress rig.
- In the app, the clothes become outfits to switch on and off.

Leg close-ups (user's screenshots, side view, 2026-11-09), for the skeleton and the fox preset:
- Baller Fox: clearly digitigrade. Thigh, shin and the long raised foot (hock to toes) are about the same length;
  she stands on her toes with the hock high.
- Female sergal: the hock sits low, near the ground, with long clawed toes; closer to a human-style lower leg.
- Male sergal: in between. A long foot angled down to the toes, heel lifted but not high.
- Fox sculpt (fox_015, user's screenshot, mirrored because a reference image was in the way): plantigrade, not
  digitigrade. A thick thigh and a fairly straight shin down to a flat foot (the dark "sock") with the heel on the
  ground, like a cartoon shoe. So the presets need a plantigrade option as well as the digitigrade fox.
- The app's legs share one set of lengths (thigh 30, shin 30, foot 22) and the foot is the short one, so it can't
  match the fox yet. Per-character (per-preset) leg lengths are needed for M3 (the fox preset),
  and the hock height / foot angle should be a preset setting too.

Summary (2026-11-09):
| Model | Rig | Ready for GLB | Before it suits the app |
|---|---|---|---|
| Male sergal | none | yes, lossless | fit to the regular sergal's skeleton (now in the app; Stage 7 non-rigged path) |
| Female sergal | 107 bones, 19 face shapes | yes, lossless | ready (Stage 7 rigged path) |
| Baller Fox | 111 bones | yes, lossless | ready (Stage 7 rigged path) |
| Cartoon 4-legged fox | none | yes, lossless (~100 MB) | lighter copy (faces + textures), a four-legged rig |
| Fox sculpt (fox_015) | 8 bones (legs, spine) | yes | attach the eyes; more bones (head, arms, tail) |

## Characters track (C)

- **C1** Regular sergal: one head, two legs, two arms, one tail ("Sergal (regular)"; the three-legged one is "Sergal
  (OC)"). First version 2026-11-09: Idle, Walk, Run (upright), Run on all fours; turns, spin and the game. Built on the
  sergal builder (see Stage 1). Follow-ups: the pull-apart hands over to him; his own look.
- **C2** Centaur (next character after the models).
- **C3** Sergal taur (below).
- Ideas: gecko skeleton (wall and ceiling climbing), new creatures, colour-coded sergals (below).

### C3: Sergal taur (idea, 2026-11-08, after the centaur plans)

- A sergal upper body on a horse or dog body. Dragging his behind adds more legs, without limit.
- Gaits: walks like a normal horse, a normal dog, and (with many legs) a centipede.

### Creature ideas (2026-11-08)

User's list (question marks are the user's own open questions):
- Snake: animations.
- Spider: animations.
- Bird; bird flying?
- Bird humans?
- Spider queen: like the centaur, but a humanoid woman's top half on a spider's body.
- Mermaids?

### Colour-coded sergals (idea, 2026-11-08)

- Each of the two sergals that make up the merged one gets its own colour, so you can tell which one is which.
- When merged, you see the two halves meet at the centre (the colour line runs down the middle).
- Maybe tan and grey by default; colours chosen with a colour picker.

## Animation soundboard track (A) ("soundboard" for animations)

- A panel of big buttons showing the recommended next animations from the current one, instead of picking from the
  dropdown.
- The suggestions come from a decision tree whose rules the user writes (for example: from "run on all six", suggest
  "Over", "180 swap ends" and "run on five, tail up"). Predetermined, not guessed by the app.
- Rules are part of the character data, so each skeleton has its own tree; a rules editor lives in the app.
- **A1** robot flow (user's design, 2026-11-08; `<~>` = suggested both ways, `<>` = a toggle button):
  - T-pose <~> Idle (upright) <~> Walk on three
  - Walk on three <> tail up / down toggle (= Walk on two, tail up)
  - Run (upright) <> tail up / down toggle (= Run upright, tail up)
  - "Probably the same for the other variants" (to confirm with the user; possible pairs from the current modes:
    Run on all six <> Run on five (back tail up); Run on five (front tail up) <> Run on four (both tails up)).
  - The user's note "(where the rest of the buttons:" was cut off; ask what it was meant to say.

## Foot planting track (F) (agreed 2026-11-08, not built yet)

From research on how games stop feet sliding (user asked whether studios snap feet to the ground or just speed the
walk cycle up with the movement). Finding: they do both, in layers. Matching the cycle to the ground speed removes most
sliding on flat ground; foot IK is a smaller layer on top for slopes and steps, and a clean-up for what's left.

Where the app is now:
- "Feet follow ground" on (default): the footstep planner pins each paw to a world spot during its stance and the leg
  solver reaches it there (`planFootstep`, `solveLegIK`). No sliding, but every leg is always IK-driven.
- Off: the legs just play their swing (`legChain` with `q.lt`) and the body rides at `ground(0,0)`. Stride swing and
  Ground speed are separate sliders and nothing ties them together, so the paws slide. Rough hand estimate with the
  default leg lengths and angles: in Walk the planted paw sweeps about 60 units while the body moves about 34; in Run
  about 93 against 49. So the paws slide backwards about twice as far as the body moves ("moonwalking"). Not measured
  in the app; ignores leg turn and splay.

Agreed plan (user chose to put it on the roadmap instead of building it now):
F1. Three modes instead of the on/off button:
   - Off: pure animation, no IK at all.
   - Height only: the paw is moved up or down to the ground, never pinned sideways. Handles hills and steps without
     the "magnet" feel. Lighter, and what many games use.
   - Full plant: today's behaviour (stays the default).
F2. Match stride to speed when paws aren't pinned (Off and Height only), with a choice of direction:
   - Speed follows legs: ground speed worked out from how far the paw sweeps while planted (like Unreal Lyra's "match
     play rate to speed").
   - Legs follow speed: the stride angle is scaled to fit the current ground speed (like Unreal's stride warping).
F3. "Plant strength" slider (0-1) instead of a hard switch: blends the animated pose with the pinned pose, so changing
   mode doesn't make the legs pop (how studios fade foot IK in and out).
F4. Plant only when slow (option): pin paws in idle and walk, let run and gallop use the animated legs, since the paws
   are mostly in the air there and the IK mainly adds a risk of knees flipping.
F5. Foot-slide readout in Dev mode: how far each planted paw slides per step, live, so the mismatch shows while tuning
   sliders. Can reuse the planted-paw test from `full.py` (a paw counts as planted below rest height 3.25).

Notes:
- Robot rule "a planted paw never slides" must still hold in the default mode; Off and Height only are opt-in looks
  that knowingly allow some slide (with stride matching keeping it small). full.py should keep testing Full plant, and
  could test the stride-matched modes with a looser limit.
- Digitigrade legs (sergal) are where plain two-bone IK struggles (three segments, knees can flip), so Off or Height
  only may look better on him than on the robot.
- Golden frames: Full plant must stay unchanged; the new modes need their own golden frames once they exist.
- Sources: Kovar, Schreiner & Gleicher, "Footskate Cleanup for Motion Capture Editing" (SCA 2002); Rune Skovbo
  Johansen, "Automated Semi-Procedural Animation for Character Locomotion" (2009 thesis, Unity); Unreal Engine Pose
  Warping docs (stride / orientation / slope warping); van den Heuvel et al., "The Right Foot in the Wrong Place"
  (Half-Life: Alyx, SIGGRAPH 2021 talk); Holden et al., "Phase-Functioned Neural Networks" (SIGGRAPH 2017).

## Pooltoys track (P) (ideas, 2026-11-08)

User's ideas:
- Water or air inside? (open question) Both could exist as amounts: air sets how full and round the body is,
  water adds the slosh (the faked-slosh plan in the long-term goals).
- Two pooltoy characters: one is a ring pooltoy (a hole through the middle of his body, like a swim ring); the other has
  no ring in the centre of his body.
- Inflating: connect a green garden hose to his mouth, or to a plastic valve on his belly button.
- A deflated state (open question): flat, crumpled, lying on the ground.
- Packing: deflated pool toys go into a box? a bag? a resealable plastic bag with a zip slider on top (like the ones
  IKEA sells)? (open question)

Notes for later (not decided): a garden hose suggests water rather than air, so the hose could fill him with water and a
pump (or blowing) with air; filling would be one amount from 0 (flat) to 1 (full) that drives the body's thickness,
with wrinkles when low. Packing could be a set of fold poses rather than a real cloth simulation.

Air vs water (discussed 2026-11-08):
- Air is not simulated as particles: it weighs almost nothing and evens out almost instantly, so it's one number per
  body (or per chamber): pressure = amount of air compared with the room inside. Water is the part that sloshes.
- What air shows comes from the skin: inflating puffs the body up; underfilled it wrinkles, sags and folds (a
  half-inflated leg buckles under his weight); pressing one part bulges another (the air has to go somewhere);
  the bounce and jiggle come from the springy skin; a leak slowly lets him slump (ties into the deflated state).
- Chambers: real pooltoys often have separate chambers (e.g. ring and body), each with its own pressure.
- With water and air both inside, the air is the space above the water line, plus bubbles when shaken or filling.
- Blender: its cloth simulation has a "Pressure" setting that inflates a closed mesh like a balloon, so an export
  could use that for the air instead of particles.

Why a big pooltoy fills unevenly (user remembered the far end filling late):
- Not air travel time (pressure evens out across 2 m in a few thousandths of a second). It's the material.
- Rubber (balloons): hard to stretch at first, then suddenly easier, so one bulge balloons out fully and travels
  along a long balloon.
- Vinyl / PVC plastic (most pooltoys): barely stretches; a flat toy unfolds instead. Parts near the valve open first;
  far parts lie folded under their own weight and creases pinch the air passages, so arms and legs flop open late,
  sometimes with a pop. Narrow joins inside (e.g. a thin neck between body and leg) slow it more. Once unfolded it
  stops growing and just gets firmer. Gravity matters a lot for vinyl.
- Possible app approach: each body part gets its own fill amount, reached later the further it is from the valve
  (mouth or belly button); pinched creases make it stop-start. No real air simulation needed.

Look: transparent tinted vinyl, 50-80% opaque (user's idea):
- A classic pooltoy look; doable in three.js: see-through tinted material with a shiny highlight; inside faces drawn
  first so the far wall shows through the near one. Shows the water line and bubbles through the skin.
- Tricky part: overlapping see-through parts (an arm in front of the body) can draw in the wrong order; needs care.
- The material only changes the look; inflating works the same as for opaque vinyl.

## Make morphs editable (see the planner for its place)

- Morphs get their own sliders (timing, height, lean, part lengths), like loops have now.

---

# Part 2: Stages (how the code is being restructured)

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
- 2026-11-09: the regular sergal was added as a registry entry (`sergal2`): his own two hips (`LEGS2`), settings
  (`DEF2`), modes and slider list, reusing the sergal builder through `buildSergal2`, which tells `buildRig` to draw
  one head, the upper arms and one centred tail. It still took a few lines of code (the builder picks his leg list;
  the rewind and save code know his legs), so "a new file, not new code" isn't reached yet.

## Stage 2: one generic rig (in progress)

Shared so far (both characters call the same code):
- footstep planner (`planFootstep`), two-angle leg solver (`solveLegIK`), bone-by-bone blending (`blendBones`), hip splay
  (`splayV`), turning to the heading (`faceHeading`);
- 2026-11-07: the body pipeline. `rigLean` (turn lift, slope and skid lean), `rigSway` (sway + banking), and the body
  height: `groundUnder` (ground under planted paws), `reachLimit` (crouch so a paw stays in reach), `bodyFloor`
  (body stays off the ground) and `rideHeight` (combines them with the thigh spring and ceiling hang). Golden frames:
  0 of 1,384 poses changed.

Still per character (they genuinely differ, and merging them would change the sergal's poses):
- leg solving (the robot's solver also turns and tilts the leg at the hip; the sergal's works in a fixed plane);
- toe on the ground (robot tips the toe up; sergal clamps it);
- floor guard (robot only), and all drawing (body, limbs, heads, tails, skins).
Plan: share these as they are rebuilt for the 3D look and the centaur; the centaur is the first character built
mostly from the shared pieces.

## Stage 3: engine separate from the editor

- `create(character)` → `update(time, input)` → `getPose()`, with no UI inside.
- Owns position, heading, gait blending, footstep planning, springs and morphs.

## Stage 4: renderer as a swappable layer (three.js) - STARTED 2026-11-07

Done: three.js renderer next to the built-in one, switch "Renderer: 3D (three.js) / Built-in" at the end of the editor
(default three.js, choice remembered). Loaded from jsDelivr (three@0.170.0 ES module, dynamic import); if it can't load,
an in-page message says so and the built-in renderer keeps drawing. It draws the same `prims` list (tubes as tapered
cylinders + spheres, balls, box-skin panels, shadows, ground/ceiling grids) with toon shading and back-face outlines,
using the same camera (yaw, pitch, zoom, pan) as the canvas, so poses and tests are unchanged. Code: `R3`, `r3load`,
`r3init`, `r3render` near the end of the script. Outlines only show on outer edges (not around every overlapping part).
2026-11-07, "3D look" panel (shown when the renderer is three.js, choices remembered; drawing only, never poses):
- Style: Cartoon (toon shading) / Soft (matte). Outlines: on / off.
- Limbs: Smooth (tubes that join end to end inside one part are swept as one curved tube through the joints, short
  tangents so bones stay straight and joints round off: `r3sweep`) / Capsules (separate pieces, as before).
- Shadows: Real (sun casts shadows onto the ground, also on hills) / Soft spots (the old blobs).
- Ground: Solid (a disc that follows the terrain) / Grid only (invisible ground that still catches real shadows).
Not done: sculpted per-part shapes; those come from the user's own sculpt / GLB import (Stage 7).
Next: see "Plan at a glance" at the top (geometry built once, then fur).

Notes from before:

Why: the current renderer is hand-made 3D on a 2D canvas. It draws flat capsules, circles and boxes and sorts whole
parts back to front by an estimated depth (with "sticky" ordering for near-equal depths to stop flicker).
- Pros: one small file, no download, instant and offline, works in the Claude preview and on w3schools; easy cartoon look.
- Cons: parts that overlap or sit inside each other can draw in the wrong order (e.g. the sergal's pale jaw needed a
  hand-made fix, `underOf`); no real lighting, shading or transparency; every new shape needs its own drawing and sort code.

Plan:
- The engine produces a pose; the canvas renderer and a three.js renderer both read the same pose.
- First step: draw the robot and the sergal with three.js alongside the current renderer, with a switch to flip between
  them. Poses and tests stay the same, so the two can be compared side by side.
- three.js gives per-pixel depth (no draw-order bugs), lighting, transparency (needed for the pooltoy water) and GLB
  import / export (Stages 6-7).
- Check first: three.js loads from a CDN link inside the single HTML file; fine on w3schools, but test the Claude app
  preview on iPhone before committing.
- Keep the cartoon look (outlines, flat colours) as a three.js material/outline option.

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
- Status 2026-11-09: G-a to G-c done (Game track); G-d (terrain, rivers, ceiling) shelved.

## Stage 9: three.js prototype

- Terrain, a follow camera, and characters driven by the controls: the first playable piece of the game.

---

# Part 3: Rules and decisions

## Robot rules (must never be broken)

- Bones never squash or stretch beyond the "Bone stretch allowed" slider (default 0%).
  - Limbs are blended bone by bone (direction turns, length kept), never by averaging joint positions.
  - Splay turns the leg at the hip; a toe kept off the ground tips up instead of stretching.
  - Exempt: the kangaroo's curled tail, and any limb while it swaps places with that tail.
  - The sergal is not covered by this rule.
- A planted paw never slides, including while spinning or turning.
- The ceiling respects gravity: the robot hangs, planted legs nearly straight, free limbs hanging down.

## Decided

- The sergal and the robot are two different skeletons. "One generic rig" means one shared builder that
  reads any skeleton description; it does not merge them.
- Moves belong to skeletons, not to one character: each skeleton description lists the moves it can do
  (for example, Ceiling is allowed for the robot now and for a future gecko skeleton).
- Planned future skeleton: gecko (wall and ceiling climbing).

- Imported models: both rigged and non-rigged.
- Engines: three.js now; Unreal and Godot later.
- Built-in models stay in the app and are exportable.

## Waiting for the go-ahead

- A realistic but still cartoony sergal with realistic hair. Not started; to be done when asked, in one of:
  - Blender (via Blender MCP), once the project moves there;
  - inside the app, as a new skin;
  - as its own standalone HTML file.

## Open questions

- Jump to the three.js prototype sooner, or tidy the structure first?
- Should the sergal get the robot's abilities (flips, limb roles), or keep each character's moves exclusive?
- Should old saved settings text keep loading after the data-format change?

---

# Part 4: Log (finished work, dated)

## Haptic feedback (how it works; gathered here 2026-11-09)

A tick on every button tap: Android vibrates; iPhone Safari has no vibrate(), so the app uses a trick with an iOS
switch control. Found with the Haptic Lab (2026-11-08).

- Android: `navigator.vibrate(8)` on each button tap (12 ms at the hold-and-drag in the view).
- iPhone, the trick: Safari's `<input type=checkbox switch>` is a real iOS toggle switch, and toggling it plays the
  system haptic tick. The app keeps a hidden one (`#hapSw`, label `#hapLb`) and clicks its label from code on every
  button tap.
- Haptic Lab results (2026-11-08, iPhone Safari iOS 18.5; identical as artifact, local file and w3schools, so the frame
  is not the blocker): clicking the LABEL of an iOS switch (`<input type=checkbox switch>`) buzzes, even when the switch
  is invisible or off-screen, but only straight after a quick tap: in a click handler, or on pointerup/touchend of a
  tap. Clicking the switch input itself does nothing. Finger-down, during a hold, and lifting after a 0.35 s hold all
  give nothing. vibrate() doesn't exist on iPhone. So a hold gesture can never buzz on iPhone; tap-based controls can.
  Side effect to avoid: the label click focuses the hidden switch and scrolls the page to it; keep the switch
  position:fixed inside the viewport.
- Every button tap in Gait Workshop now ticks (2026-11-08): a capture-phase click listener clicks the label of a hidden,
  position:fixed iOS switch (`#hapLb`), then hands focus back; Android vibrates 8 ms instead. Sliders and dropdowns don't tick. No tick when the tap does nothing
  (`tapDoesNothing`: disabled, a reset button already at its default, or a choice that is already selected).
- Hold-and-drag in the view (split / squash the sergal): Android vibrates at the hold; iPhone can't tick there (tried
  the hidden switch at the hold and at release: no tick on device), so everyone gets a visual cue instead: the view's
  border flashes and stays highlighted while dragging.
- Rewind: the hidden switch and its label are ignored by the branch check. Before that, the tick's label click counted
  as "a change while rewound" and cut the history (iPhone: stepping back after choosing an animation forgot it).
- Opt out: a button with `data-nohaptic` gives no tick ("Add a .glb file", since the system file picker gives its own
  feedback; user, 2026-11-09).
- Limits: tested on iOS 18.5 (the user's iPhone, 2026-11-09). Older iOS versions without the switch control get no
  tick.
- Not new (web search, 2026-11-09): WebKit added the switch's haptic in Dec 2023 (shipped in iOS 18); the label-click
  trick has been used since late 2024 (Ionic feature request, the ios-haptics library, a web-haptics polyfill); WebKit
  bug 285120 (fixed Jan 2025) made it need a real tap, which is what the Haptic Lab found.
- Watch out: Apple reportedly patched the trick in iOS 26.5 (ios-haptics says it works on iOS 17.4 to 26.4): from
  26.5 only a finger tapping the switch itself ticks, so clicking the label from code goes quiet. Not checked on a
  device here. If the user moves to 26.5+: put an invisible switch over each button instead (native look, opacity 0,
  hit area clipped to the button's shape with clip-path), pass the tap on to the button; one tick per tap only.
  Reported working after the patch by project-fathom (github.com/m1ckc3s/project-fathom) and
  haptics.kushagragolash.dev. Keep `data-nohaptic` and the no-tick rules.
- Built 2026-11-09 (user: "do the invisible switch on button"), ready for iOS 26.5+ while still working on 18.x:
  on iPhone / iPad every button carries an invisible native switch laid over it (`.hapOv`, added by `hapAdd`; a
  watcher re-adds it to new buttons and to buttons whose text is replaced). The finger taps the switch, iOS ticks by
  itself and the click bubbles on to the button. Taps that would do nothing (a disabled button, a choice already
  chosen, a reset button at its default) go through the switch (pointer-events:none), so no tick; `data-nohaptic`
  buttons get no switch. The label click stays as the backup and is skipped when a switch was hit, so 18.x never
  ticks twice. Focus goes back to the button (keys keep working); the rewind check treats a switch as its button.
  Desktop and Android: no switches (Android keeps vibrate).
- Tested in an emulated iPhone 13: 154 of 155 buttons got a switch (the GLB picker opts out); play / pause, 90 turn,
  renderer, Mode, step back / forward and the model cards all work with the tap landing on the switch, and no tap
  used the backup as well; a choice already chosen got no switch hit; stepping back and forth doesn't cut the rewind
  history (a first version did: a code comment swallowed a line of the rewind check; fixed); arrow keys still step.
  The tick itself can only be checked on the user's iPhone.

## What the editor does (summary)

Done so far:

- Three characters: the three-legged sergal, the regular sergal (one head, two legs, two arms, one tail; 2026-11-09)
  and the six-limbed robot, each with their own modes.
- Procedural gaits (loops), mode blends, and morphs (90° / 180° / skid, Over, Ceiling, Rise). Spin is a toggled loop, not a morph.
- IK footstep planning, foothold search, thigh spring, head steadiness, terrain (hills, bumpy, steps).
- Robot skins (boxes, sergal, dinosaur, kangaroo), body segments, spine flex.
- Frame-by-frame stepping and scrubbing of loops and morphs, LOOP / MORPH status line, morph part markers.
- Full Playwright test of every mode pair, turn and move, forwards and backwards.
- Robot rules enforced (see "Robot rules" below): no squashed bones, no sliding paws, ceiling respects gravity.
- Ceiling: the front (red-paw) end reaches up and grabs; the ends swap jobs, as in Over. Drop is the reverse.
- Robot lying flat on 4, 5 or 6 legs (run6, run5b, run5f, run4, run4dog, run5head): the 180 has two choices in Robot look.
  - Swap ends (default): he slows, stops and runs off with the other end leading (`DIR` = -1; `U6` turn). When moving fast
    (travel over 100) he skids first, sitting back on the rear end like the upright skid 180. The body never turns.
    A raised tail moves to the new back end during the turn (`LIMBSW`: tailUse and frontTail trade places), so run5b
    stays "back tail up". Takes a little longer for a longer body.
  - Swap ends, raised limbs stay put (variant, kept on purpose): same, but raised limbs stay at their own end, so it
    becomes a look-alike of the opposite 5-leg run (run5b turns into a run5f-style gait).
  - TEMPORARY (head-up modes run5head, run4dog, "Swap ends" option): a raised head can't move to the other end yet (only
    the front middle limb can be a neck), so once the ends have swapped the head is hidden (`headHide` in `buildRobot`);
    the raised neck stays. Swapping back shows it again. To be replaced by a proper method later (user will look into it).
    The "raised limbs stay put" variant still shows the head.
  - Turn round: the body swings round 180, slower than upright (1.8 cycles at body length 100, scaled by length 60-220%).
  - Leaving these modes while reversed eases back to forwards during the mode blend.
- Spin pivots round the middle of the body; long-bodied modes spin slower so planted paws can keep up.
- Robot legs turn and tilt at the hip (not only swing), so a planted paw stays put while the body turns.
- Interface switch (Auto / Touch / Desktop, remembered where storage works). Auto uses the main input: mouse or
  trackpad (`pointer: fine`) gives Desktop, a finger gives Touch. Desktop = compact controls, and on windows at least
  760px wide the 3D view sits left with the controls on the right (drag the divider; its position is kept separately
  for each layout). Touch = the original phone layout.
- Floor guard (robot): a lifted, tucked or half-planted limb that would dip into the ground swings up at the hip until
  it clears (a turn, so bone lengths are kept). Fixed the front middle limb clipping while blending into the lying modes,
  and the sergal-skin tail sinking 18-26 units into the floor in Walk on two. Planted paw blocks still sink about 2 units
  at the corners (the block is wider than the paw's height); not fixed yet.
- Spacebar always plays / pauses, even after clicking a button or dropdown (except while typing in a text box).
- Every slider has a reset button (faded at default, red once changed); Bone check reads On / Off.
- Desktop: the mouse wheel over a dropdown steps through its choices.
- Desktop 3D view: wheel (or trackpad pinch) zooms toward the mouse; right-drag, middle-drag or Shift+drag pans;
  left-drag orbits; double-click resets.
- Robot look panel: "Bone stretch allowed" slider (0-30%, default 0%) and a "Bone check" debug button.

## 2D debug picker (done 2026-11-08)

- User's idea: tap a shape in the 2D view to track it; while you move the camera, the app tells you what's drawn on
  top of it, so you know what's hiding it. For hunting draw-order bugs like the robot dog's back.
- Panel "2D debug: what's hiding it?" after 3D look (shown with the 2D renderer): Pick On / Off, Clear, and a live
  line, e.g. "Tracking: Body, box end face. Drawn 27 of 171; about 43% covered by: Back tail, box side face (20%);
  Right leg, box side face (6%)." Also says when the shape faces away (not drawn) or is gone (character/mode changed).
- How: every part is named as it's built (`PNAME` -> `nm` on each shape: "Left leg", "Body segment 2", "Neck and head
  A", "Tail 1" ...). The 2D renderer records the draw order (`DRAWN`). A tap (no drag) picks the topmost shape under
  the finger (`pickAt`); each frame `pickReport` finds it again, outlines it with a dashed red line, and tests sample
  points spread over it against every shape drawn later. Golden frames unaffected (they don't read names).
- The picker and other display-only switches (3D look, renderer, interface, Start fresh) no longer cut the rewind
  history when pressed while rewound.
- Camera readout (user's idea, 2026-11-08), in the 2D debug panel and in a new "3D debug, camera edition" panel
  (shown with the 3D renderer): yaw, pitch, zoom, pan; the point looked at; camera position relative to him and in
  the world; which way he faces; and which side he is seen from ("Seen from his back-right, from above"), checked
  against which legs/head are nearest the camera for both characters. 3D adds the field of view (`camReport`).

## 2D renderer: box body draw order (fix 2026-11-08)

- Bug (user's screenshots, robot dog seen from behind, low camera): the body's back face was hidden under the hips
  and tail roots. Cause: limbs are drawn whole, sorted by average depth; hips and tail start inside the body near its
  back end, so they counted as nearer and covered the back face (in 3D the face hides their roots).
- Fix (`render`): each box body segment is convex, so a piece on the outer side of one of the segment's visible faces
  can't be hidden by it. Pieces are placed just before the first segment (far to near) that would hide them, others
  after the body; limbs are still drawn whole within each slot. Body segments are marked with `bseg` in `buildRobot`.
  Box skin only; the sergal and the tube skins (sergal, dinosaur, kangaroo) sort as before. Checked against the 3D view
  (true depth) from behind, the side, above, below, upright, lying, 3 segments.

## Start fresh (2026-11-08)

- Fieldset at the end of the editor: "Reset to factory defaults", with an in-page "Sure?" (no browser dialogs).
  Removes only this app's keys (`mixmo*`, `tripod*`) from local and session storage, since on w3schools the storage
  is shared with the site, then reloads. Used to see the app as a first-time visitor (drawers, layout, choices).

## Sergal: grow, split the neck, pull apart (2026-11-07, before the centaur)

The life cycle (user's design): an ordinary two-legged sergal must grow a third leg before he can divide; dividing
starts at the neck and works down to the hips; the result is two two-legged sergals.
- "Grow the third leg" (0 = two-legged sergal, 1 = the usual three-legged one; idle only): the middle leg starts as a
  stubby tail behind him, lengthens (first half), then swings down and plants as a leg (second half). His second pair
  of arms and second tail grow in alongside it. A leg still growing doesn't hold the body up yet. (`GROW`/`GROWE`)
- "Squash the two heads into one" (`HMERGE`): in the cycle, the neck splits after the leg has grown.
- "Pull apart into two sergals" (idle only, needs the leg fully grown): unzips from the neck down: heads, shoulders and
  arms separate first (`SPLt`), hips, legs and tails last (`SPLb`). Each half keeps its outer leg; a copy of the middle
  leg swings round to become its inner leg; the upper arm stays outside, the lower arm moves to the inner side.
- Cycle order switch: "Head splits first" (default: neck 0-0.3, grow 0.3-1.3, unzip 1.3-2) or "Leg grows first"
  (grow 0-1, neck 1-1.3, unzip 1.3-2). `CYCORDER`, remembered.
- Holding in the view no longer selects text or shows the iOS magnifier. Haptics at the hold: Android only; everyone
  gets a visual cue (the view's border flashes and stays highlighted while dragging). See "Haptic feedback".
- In the view: press, hold, drag. On the body the drag runs the whole cycle as one value (`setCycle`, 0-2);
  right goes forward, left goes back. On the heads it only squashes the heads.
- Growth order from merged: the second tail grows first (`GT2`, first 35%), then the third leg (`GLEG`).
- "Inner arms when he divides" (`ARMOPT`, remembered): 1 Grow before (inner arms grow with the third leg, then move to
  the inner side as he splits); 2 Grow after (no inner arms until the two are fully apart, then they grow);
  3 Shoulder bridge (each half's inner arm reaches to the middle and joins the other's as they emerge; once apart it
  snaps and becomes one arm each). In 2 and 3 the bodies finish separating at 80% of the pull, the last 20% (`ARMT`)
  is for the inner arms. In 2 and 3 the merged sergal has only his two outer arms.
- Second idle, "Idle, third leg as a tail" (`idleTail`): same settings as Idle, but he stands on two legs and holds
  the third leg out behind as a full-length tail (`TAILE` eases it up/down when switching; the leg's own growth `GL`
  is capped at 0.5 = full tail). Pulling apart is off in this idle (the leg isn't planted). Growing and squashing work.
  Note: golden frames don't cover it yet (they build poses directly, without the easing).
- Everything eases back to the normal sergal outside the two idles.
- In a game: once fully split, the model would be swapped for two copies of an ordinary two-legged sergal.
  Next: make that two-legged sergal its own character (walk, run, idle, turns) so the split can hand over to it.
- Defaults draw exactly as before: golden frames unchanged.
- Fixes 2026-11-08 (user's notes):
  - "From a stubby tail" was not literal: an ungrown third leg is now completely hidden. It pops out as a small stub
    over the first 8% of its growth, lengthens as a tail, then swings down and plants.
  - Drag hint now reads "... Left: Merge them together!"
  - While dragging, the hint shows the current stage live ("Now: two heads, third leg growing out as a tail 15%"),
    because the new leg and second tail can be hidden behind him from some camera angles (`cycleStage`, `pullHint`).

## Robot dog run (2026-11-08)

- Run on four like a dog: straighter legs (knee 40, hock 34, thigh 20), less splay (6) and a lower paw lift (24) than
  on six, so the planted legs are nearly straight and the swing no longer flips the shin out. Golden frames
  re-recorded for this (only robot run4dog changed). The other 4/5-leg runs still use the six-leg settings.
- Fix (2026-11-08): switching from an upright mode into the dog run left the front legs stuck in the air ("flapping"):
  the leg solver starts from last frame's angles and got trapped with the paw pointing up. Now, if a planted paw ends
  more than 6 units off its target, the solver retries from fresh starting poses and keeps the closest
  (`solveFrom`/`miss` in `buildRobot`). Golden frames unchanged.

## Robot hip-turn pop fix (2026-11-08)

- Bug (old, also in earlier versions): in every upright robot gait each leg turned further and further inward at the
  hip (31, 37, 46 deg) then flipped to 39 deg the other way in one step (a 22-27 unit jump; user saw it at frames
  10-13 of Run upright). Cause: the solver has two hip turns that aim the leg at its paw and always took the smaller;
  when they swapped, the leg snapped across.
- Fix (`buildRobot`, hip yaw): still the smaller turn, but when the answer swaps by more than ~20 deg while the leg is in
  the air, it glides there (max 0.12 rad per build) instead of snapping. Planted paws keep the exact answer so they
  never slide. Tried and rejected: always following last frame's solution (legs drifted to the 69 deg limit and planted
  paws slid in the 4/5-leg runs).
- Result: biggest joint move per 1/96 cycle 4-6 units in run, run tail up, walk on two, dinosaur (was 22-27).
  Walk on three still has one 10-unit step (was 23): its swap happens while the paw is planted.
- Tests: full.py 0 failures (slide 0.036), golden unchanged.

## Performance (2026-11-08)

- Profiled per frame (phone-size browser, no graphics chip, so 3D numbers are on the high side): 3D drawing 3-4 ms
  (65-80%), gait chart + status 0.4-0.8 ms, pose 0.15-0.5 ms, rewind record < 0.1 ms, restore 0.1-0.4 ms.
- Gait chart now cached (`drawGaitOn`: bars drawn once into an offscreen picture keyed on character, size and leg
  timings; each frame copies it and draws the playhead; skipped when folded away). Pixel-identical; about 0.1 ms/frame.
- Done 2026-11-08: 3D tubes are built once. Before, the three.js renderer rebuilt every tube (thousands of points) in
  JavaScript each frame and re-uploaded them. Now there is one tube segment (14 points round, 7 rings along) built at
  start-up; every bone is a copy (instance) of it. Each frame sends only each bone's two ends, end directions, ring
  frame, radii and colours (`r3seg`), and a small vertex-shader function (`tubeEval`, patched into the stock three.js
  materials with `tubeMat`) bends the segment into place. Smooth limbs (`r3chain`): neighbouring segments share their
  end points and directions (Hermite curve) and carry the ring frame along, so a limb is still one curved tube with no
  twist. Capsules: straight segments plus end balls, as before. The outline is the same segments drawn fatter with
  back faces; real shadows use a patched depth material. Same look in all 32 "3D look" combinations.
- Result (same profiler): 3D drawing sergal 3.2-4.3 → 1.4-1.7 ms/frame, robot 3.0 → 2.0-2.3 ms/frame. What's left
  per frame in JavaScript: the ground disc following the terrain, grid lines, balls, robot box-skin panels.
- Fix 2026-11-08: pressing a "3D look" switch froze playback for a moment: three.js built new shaders on the spot
  (15 across one round of toggles). Now `r3warm` prepares them all with `compileAsync` on two hidden copies of the
  scene (sun casting shadows or not) right after three.js loads; the 3D view takes over only once that's done, and
  2D keeps drawing until then. Left: turning Real shadows back on rebuilds two tiny shadow shaders (a small blip).
- Not a "skinned mesh" in the Blender sense yet (that comes with GLB import/export, Stages 6-7), but the same idea:
  the shape is built once and the bones move it.

## Spin stops square on (fix 2026-11-08)

- Bug (old, user's report): turning Spin off stopped him at whatever angle he'd reached. Now he keeps spinning until
  he faces the next of the four main directions (a multiple of 90° in the world), then stops there (`SPIN.stopH`,
  `spinEnd`). The button goes dark at once; pressing Spin again during the wind-down keeps spinning. A 90° / 180°
  turn button still stops a spin at once (`toggleSpin(true)`). Works with rewind (the stop point is in the snapshot).
- Follow-up (user broke it with quick taps of Spin / 90 / 180): a 90 / 180 turn pressed during a spin stopped the spin
  at an odd angle and then turned 90 / 180 from there. Now every 90 / 180 turn aims for a main direction (exact 90 /
  180 when already square; from an odd angle, the nearest main direction that way). Spin pressed while a turn is
  playing is ignored (it used to make him jump when the turn ended). Robot lying with "Swap ends": that 180 doesn't
  turn the body, so pressed during a spin it lets the spin wind down to a main direction first, then swaps
  (`SPIN.then`). Stress test: 40 random quick tap sequences, all ended square on.
- full.py's spin check updated to the new rule: after Spin off he must stop, square on, within 0-90° more turning,
  then hold still. full.py: 0 failures, worst slide 0.036.

## Player / Dev mode (2026-11-08)

Superseded the same day: the Off / On switch below became "Mode: Game / Animation player / Dev" (`mixmoTier`; see
"Three ways to use the app"). Below, "player mode" means today's Animation player and "Dev mode" means Dev.

- User's idea: players explore the animations; the advanced settings that customise legs and gaits are for the author.
  Switch "Dev mode: Off / On" near the bottom (above Start fresh), off by default, remembered (`mixmoDev`). Anything
  with class `dev` is hidden unless `<html>` has `devmode`.
- Player mode shows: character and animation menus, turn buttons, the 3D view (camera, hold-and-drag split/squash on
  the sergal), timeline (play, step, scrubber, rewind), mood (Tired-Happy), terrain type, height and spacing, Robot look
  (skins, shape, body sliders, colours, top limb, six-leg gait, 180 choice, leaving six legs), power saving, renderer,
  3D look, and at the bottom Interface, Dev mode and Start fresh.
- Dev only: "Switch: by frame/instant", bone stretch and Bone check, sergal Show parts (heads/arms/tails, cycle order,
  inner arms, grow/split/squash sliders), terrain tuning (lean, thigh spring, head steadiness, feet follow ground),
  where each leg joins, leg colours, footfall chart and blend time, Editing + the gait sliders, Save & load, 2D debug
  picker, 3D camera debug.
- Decided with the user: Robot look = player; Show parts = dev; mood, renderer and 3D look = player; Interface and
  Start fresh at the bottom of player mode. My call (flagged to the user): terrain's tuning sliders went to dev.
- Sergal editor: 109 visible controls in dev, 14 in player; robot 76 / 25.
- Follow-up 2026-11-08 (user's notes):
  - The dev-only sections are now gathered in one block, "Dev mode" (`#devArea`), directly above the Dev mode switch:
    Show parts, where each leg joins, leg colours, footfall chart + blend time, Editing + sliders, Save & load, 2D
    debug, 3D camera debug. Small dev items stay inside their own sections (bone stretch / Bone check in Robot look,
    terrain tuning in Terrain, "Switch: by frame" by the timeline).
  - Turning Dev mode on or off keeps the switch where it was on screen (finds whichever panel scrolls in the current
    layout, adjusts it, and again two frames later after the chart has set its height); the options open above it.
  - Gait chart not appearing after Dev on: the chart only learns it's visible a moment after the switch is pressed;
    paused or with Power saving on, nothing redrew it after that. Now the size watcher redraws the chart itself and
    counts as a change for Power saving; Dev mode also makes the chart re-check its size.

## Power saving (2026-11-08)

- User's idea: 2D as a power-saving mode for iPhone; also one for three.js. Switch "Power saving: Off / On" above
  Renderer (remembered, `mixmoPower`). Works with both renderers:
  - at most 30 frames a second (the loop skips every other screen refresh; motion uses the real time step);
  - no redraw while the picture would come out the same (`powerSig`: shapes rounded to a quarter unit, camera, size,
    renderer, any tap / key / drag / slider (`PDIRTY`)). Paused, it settles to 0 redraws within about a second;
    dragging the camera or moving a slider while paused still redraws;
  - (tried and reverted at the user's request: normal instead of double-sharp pixels; it made models blurry and
    pixelated, so the view always draws at full sharpness);
  - 3D: real shadows become soft spots while on (the saved 3D look is kept; no shader rebuild, they're prepared).
- Measured (2D): 60 → 30 redraws a second while playing; 60 → 0 while paused.
- Safari doesn't tell pages the battery level, so it's a manual switch.
- Found on the way: the gait chart asked the page for its width and visibility every frame, right after the status
  text changed, which forced a full page layout each time (twice: main and mini chart). Now remembered and updated by a
  ResizeObserver; the status line, frame label and scrubber only write when their text / value changes (`setText`).
  Gait chart + labels: about 0.24 → 0.02-0.06 ms a frame.
- Fix: pressing Power saving (or any 3D look switch) when three.js hadn't loaded threw an error (`r3applyLook` read
  the 3D materials before checking they exist).

## Rewind by replay (done 2026-11-08)

- Rewinding no longer simulates anything backwards: it restores frames that already played.
- Every played frame is saved as a full snapshot (`hSnap`/`hRestore`): mode, blend, phase, position, heading, turn /
  flip / spin / Over / swap-ends state, springs, head springs, leg-solver warm starts (`L.ik`, `L.yaw`), split / grow /
  squash amounts, settings in use (`cur`, `from`). Last 30 s kept (`HMAX` 1800 frames).
- Back / forward buttons (`hStep`) move about one gait frame (1/24 of a cycle) through the recording; forward at "now"
  simulates one new frame. The scrubber runs over the whole history (left = 30 s ago, right = now; label "-1.2s"/"now").
- Play while rewound replays the recording until "now", then carries on live.
- A real change while rewound (any editor control, animation, turn, pull/squash drag) cuts the history there and
  continues live from that frame (`hBranch`). Changing character clears the history.
- While paused nothing new is recorded (only the newest frame is refreshed).
- Fix found on the way: the main loop passed the live settings object to the builders, which adjust it in place (skid
  lean, turn lift); it now builds from a copy.
- Tests: `rewind.py` (rewound poses match what played within 0.05, step back/forward symmetry, replay reaches now,
  branching). `full.py` now scrubs moves through the engine (`morphNow().set` / `scrubTo`), since the on-screen scrubber
  is the history.
- Fix (iPhone): stepping back after choosing an animation forgot it (the haptic tick cut the history; see "Haptic
  feedback").
- Scrubber window sized to fit (user's idea, 2026-11-08): about 20 px per second of recording, so 10 s on a phone
  (scrubber ~210 px) up to the full 30 s on desktop (~690 px). The window ends at "now"; stepping or playing past either
  end slides it along, and it stays put while you scrub inside it (`scrubWin`, `SW0`, width from a ResizeObserver).
  Tooltip says how many seconds it covers. Scrubber step made finer (0.001).
- "Switch: by frame / instant" checked under the history rules (user asked, 2026-11-08): it still works. By frame:
  while paused, picking an animation waits, and each step forward moves the switch on (0 → 0.07 → 0.15 ...).
  Instant: the switch plays out by itself over the blend time, even while paused. Fixed: stepping back after stepping
  forward through a switch skipped its first frame (the moment it was picked); steps forward taken at "now" are now
  remembered too (`NOWSTEPS`), so stepping back retraces them exactly. Saved steps are forgotten when playing on,
  branching, clearing, or when old frames drop off the 30 s history.
- Step buttons now retrace exactly: each step back remembers where it came from (`HSTEPS`), so back 5 then forward
  5 always lands on the same frame (before, uneven spacing of saved frames could leave it one frame off).
- Fix: the robot hip-yaw glide reads each leg's previous yaw, so snapshots now store the leg-solver state from
  before the frame was built (`hPre`), keeping rewound robot poses exact.

---

# Part 5: Handoff

## Handoff (files and tests; started 2026-10-03, updated 2026-11-09)

Files:

- `Mixmo.html`: the app (single file). Published as the Claude artifact "Mixmo" (2026-11-11):
  https://claude.ai/artifact/5EsTKhQTjt1cKm7gK9n1so. The artifact copy (`mixmo-artifact.html`) is `Mixmo.html` without
  the doctype/html/head/body wrapper tags (the artifact host adds its own) and with the title "Mixmo"; republish to
  that URL after changes.
- Older artifacts, kept on purpose as snapshots of how far the project has come (user, 2026-11-11): "Sergal Gait
  Workshop", 2026-10-02 (https://claude.ai/artifact/NsCZzDaLy68zyfCFdxYH5E); the earlier "Gait Workshop" link
  (https://claude.ai/artifact/FSxktjPPr1fGG5WYYUD9W8) isn't reachable from the user's current account.
- `Mixmo_edit.html`: standalone keyframe sketcher for the robot body and 6 legs (user has edited it).
- `roadmap.md`: this file.

Test scripts (they load `Mixmo.html` by default; run against `python3 -m http.server 8765` from the project folder):

- `full.py`: every mode pair, turns, spin, ceiling, over, leaving six; forwards, backwards and scrubbing. Also runs the bone
  check (fails above 3%) and the planted-paw slide check (fails above 0.05). Must report 0 failures; prints the worst bone
  change and worst slide. This is the one to run after large code changes.
- When to test: only after large code changes or refactors, not after small fixes (each test run takes 30-60 seconds).
- `slide.py` / `bones.py`: standalone versions, only for a detailed per-mode printout when hunting a problem.
  A paw counts as planted only at rest height (below 3.25), so the paw starting to lift is not counted as a slide.
- `golden.py` / `golden2.py`: golden frames. Re-recorded 2026-10-03 after the floor guard (only change: robot sergal skin,
  2 segments, Walk on two, whose tail no longer sinks into the floor).
- Keep the test scripts with the project files (an earlier set was lost when a session's scratch folder was cleared).

Test notes (2026-11-11): the pose comparison (old file against new, every character, animation and terrain)
must fill in `bobWave` when it builds from `P[mode]`; without it every position is NaN, which prints as null, and
two NaN poses compare equal. An earlier comparison script had that flaw; redone with real numbers on 2026-11-11,
same results (the leg solver fix and the Sergal preset change no poses). A pose with NaN shows as [null,null,null].
 jsDelivr is blocked in Claude's cloud workspace; tests there install three@0.170.0 with npm
and serve it in place of the jsDelivr URLs (Playwright route). With two models loaded, drawing in software is very
slow, so model tests pose the models without drawing (call `mdlPlace` instead of `render`). Build poses from `cur`,
not `P[mode]` directly: `bobWave` is filled in by the main loop and is missing otherwise (NaN body).

Results 2026-10-03: full.py 0 failures; worst bone change 0.00%; worst planted-paw slide 0.036 (same worst slide
after the spin fix, 2026-11-08). full.py and the golden frames cover the three-legged sergal and the robot only.

Where things live in the code:

- Shared engine: `planFootstep`, `predictFoot` (has a spin branch that rotates round `SPIN.pz`), `solveLegIK`,
  `blendBones`, `splayV`, `faceHeading`, `smaxFloor`, `softMinAll`, `smin`.
- Robot: `buildRobot` — plan, body height (with `hang` on the ceiling), limbs (IK + hip yaw/roll), flip blends
  (ends/rise and the ceiling grab), then the bone rule (`BONETOL`, `BONEBAD`, `BONESHOW`), then drawing.
- Spin: `toggleSpin` / `turnStep` (`SPIN = {p0, h0, len, ts, pz, W}`, `SPINSTEP` sets how far a paw is carried per stride).
- Flips: `startFlip` (Drop swaps ends at the start), `flipStep` (Ceiling swaps ends on landing).
- Debug globals: `ROBFEET`, `SEGDBG`, `LASTMID`, `LASTHIPS`.
- Sergal: `buildRig` (grow / split / squash via `GROWE`, `SPLITE`, `HMERGE`); the regular sergal is `buildSergal2`
  around it, with `LEGS2` / `DEF2` / `META2`. Body presets (M3): `SERGAL2_PRESETS`, `PRESET2`, `setPreset2`,
  `withLegs2` (swaps the leg lengths `L1` / `L2` / `L3` and `TOE` in while he is built), `DEF2F` / `PS2F` (fox gait),
  `preset2Params`, `camAim2`. Models: `mdlBase` (scale from the preset), `mdlFootTip` (ball of the foot). Characters: the `CHARACTERS` registry, `charDef()`.
- Game: `gameInput`, `gameStep`, joystick `STICK` / `#stickZone`, robot forms `FORMS`. Mode tiers: `TIER`, `devUI`.
- History: `hSnap` / `hRestore` / `hStep` / `hBranch`; `hLimbs()` lists every leg whose solver state is saved.

Next up: see "Plan at a glance" at the top of this file.
