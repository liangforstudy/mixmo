# GLB water tests (Pooltoy Water Lab)

`glb_tests.py` is the test from 2026-11-13, when GLB textures were fixed for the chat preview and the water
surface was trimmed to the model's real skin.

    npm i three@0.170.0
    pip install playwright
    python3 glb_tests.py pooltoy-water-lab.html baller_fox_body.glb --chrome /path/to/chrome

- PASS / FAIL: the fox's textures load normally **and** with the chat preview's limits simulated
  (`blob:` URLs broken, `fetch(data:)` refused, as the iPhone probe found).
- Screenshots of the GLB model from above, front-low and the tail go into `shots/`, named after the lab file.
  Run it on two copies of the lab to compare the water surface by eye.

The drawing runs in software in a test browser, so its frame rate means nothing; read the fps on the iPhone.

Not in here: `lab.py` (the lab's main water test). It lives in `mixmo-tests.zip` from earlier sessions.
Suggested: put this folder in that zip too.
