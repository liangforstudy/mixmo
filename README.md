# mixmo
The curious gait of a 3 legged sergal

Mixmo (first called the Gait Workshop) is a single-file web app for procedural walk cycles: the three-legged sergal OC, a regular sergal, a six-limbed robot with creature skins, and imported GLB models that copy his moves. It runs in the browser with a 2D view and a three.js 3D view, on iPhone and on desktop.

## Files

- `Mixmo.html`: the app. Open it in a browser.
- `tests/`: anti-regression tests (Python 3 + Playwright + Chromium). See `tests/README.md`.
- `roadmap.md`: the plan, the robot rules and hand-off notes.
- `skills/golden-frame-check/`: how to run and re-record the golden-frame tests.

## Branches

- `main`: Mixmo, from the early walk-cycle editor (October 2026) to the Gait Workshop as published on 13 November 2026.
- `pooltoy`: merging the Pooltoy Water Lab into Mixmo (14 November). The lab's own earlier history isn't here yet.
- `body-move-sketcher`: a separate keyframe editor for the robot's body and legs from 3 October.

## About this history

Mixmo was built across many chats with Claude, each publishing new versions of the artifact. This history was put together from the git exports of six of those chats. Where a chat's step-by-step versions weren't kept, one commit carries that stretch of work and says so in its message. Commit dates are when each version was made or handed over, as far as the exports record it.

## Licence

MIT, see `LICENSE`.
