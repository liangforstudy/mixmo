# mixmo
The curious gait of a 3 legged sergal

Mixmo (first called the Gait Workshop) is a single-file web app for procedural walk cycles: the three-legged sergal OC, a regular sergal, a six-limbed robot with creature skins, and imported GLB models that copy his moves. It runs in the browser with a 2D view and a three.js 3D view, on iPhone and on desktop.

## Live pages

- **[liangforstudy.github.io/mixmo](https://liangforstudy.github.io/mixmo/)**: the newest Mixmo on `main`.
- **[…/mixmo/pooltoy/](https://liangforstudy.github.io/mixmo/pooltoy/)**: the newest Mixmo on `pooltoy`; the Water Lab is at [`…/pooltoy/pooltoy-water-lab.html`](https://liangforstudy.github.io/mixmo/pooltoy/pooltoy-water-lab.html).
- **[…/mixmo/body-move-sketcher/body-move-sketcher.html](https://liangforstudy.github.io/mixmo/body-move-sketcher/body-move-sketcher.html)**: the body move sketcher.
- **[…/mixmo/viewer/viewer.html](https://liangforstudy.github.io/mixmo/viewer/viewer.html)**: the history viewer. It shows Mixmo as it was at any commit, on any branch: step through versions with ◀ ▶, tap a dot on the timeline, switch branches, and read each commit's description. Links like `…/viewer/viewer.html?v=98bf05e` open one version directly.

Every branch gets a folder like `pooltoy/` with its newest pages. `.github/workflows/viewer.yml` rebuilds the site on every push to main, every 6 hours (that's when pushes to the other branches show up) and when run by hand from the Actions tab.

## Files

- `Mixmo.html`: the app. Open it in a browser.
- `tests/`: anti-regression tests (Python 3 + Playwright + Chromium). See `tests/README.md`.
- `roadmap.md`: the plan, the robot rules and hand-off notes.
- `skills/golden-frame-check/`: how to run and re-record the golden-frame tests.
- `viewer/`: the history viewer (`viewer.html`), the script that builds its version list (`build_index.py`) and the one that lays out the site (`build_site.py`).

## Branches

- `main`: Mixmo, from the early walk-cycle editor (October 2026) to the Gait Workshop as published on 13 November 2026.
- `pooltoy`: merging the Pooltoy Water Lab into Mixmo (14 November). The lab's own earlier history isn't here yet.
- `body-move-sketcher`: a separate keyframe editor for the robot's body and legs from 3 October.

## About this history

Mixmo was built across many chats with Claude, each publishing new versions of the artifact. This history was put together from the git exports of six of those chats. Where a chat's step-by-step versions weren't kept, one commit carries that stretch of work and says so in its message. Commit dates are when each version was made or handed over, as far as the exports record it.

## Licence

MIT, see `LICENSE`.
