# Taxi spatial admission and remaining blockers

Extraction manifest: vpx-sources/williams/taxi/Taxi (Williams 1988)1.2/extraction-vpxtool-git-v0.33.3/manifest.json, SHA256 b23d0faa0bacef495223a65b6c79a209c2eaa628e6675abb98c0c404cea09363. Retained table SHA256 7c6f52b24e7fabc761611d33b7eab5de15b9025f954fb4e423f3219e09af9c40.

Exact table bounds: left0/top0/right952/bottom1974 VPX units. x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top), round to six places with repository pinmame_game_defs.spatial.extract_spatial_candidates / _round_point. Direct Kicker, Bumper and HitTarget centers only; no primitive local origin or bulb/helper light is admitted.

| Device | Object | Extracted path | Method | x | y | Role |
| --- | --- | --- | --- | --- | --- | --- |
| switch.13 | JoyrideEject | gameitems/Kicker.JoyrideEject.json | center | 0.168928 | 0.134554 | sensor |
| switch.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | sensor |
| switch.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | sensor |
| switch.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | sensor |
| switch.24 | sw24 | gameitems/HitTarget.sw24.json | position | 0.252626 | 0.136398 | sensor |
| switch.35 | Catapult | gameitems/Kicker.Catapult.json | center | 0.050566 | 0.589215 | sensor |
| switch.36 | RightLock | gameitems/Kicker.RightLock.json | center | 0.917146 | 0.303642 | sensor |
| solenoid.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | effect |
| solenoid.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | effect |
| solenoid.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | effect |

Factory locations PDF60/62 reconcile named jet bodies, saucers and standup to these modeled assemblies. Coil17/19/21 placements project the underplayfield actuator effect to its named ring center, justified by the jet assembly and script body. These are observed recreation anchors, not surveyed physical dimensions. No manual-derived pixel coordinate is mixed into this space and no frame fit is invented.

Remaining: trough and rollout sensors, both three-target banks, ramp switch centroids, sling effects, ball-gate and eject/feeder effects; every controlled physical lamp/flasher socket and complete GI population. Backbox and coin-door effects need quantities and routing even when playfield placement is not applicable. C1..C5 each1p+1i, C6/C7 each1p+1d, C8 two playfield, Jackpot1p+2i, Joyride1p from the wiring table. Dome PCB has F1..F4 designators; board capacity is not proof all sockets are populated. The exact installed population must be reconciled before output_semantics can be completed.

Escalation completed: full factory manual/schematics and preliminary manual acquired/OCRed; decisive native pages verified; exact retained VPX parsed; both pinned script corpora compared; pinned native source and runtime service outputs inspected; four legal ROM name tables inspected. Ghidra can resolve ROM behavior, but cannot establish unknown physical socket centers or prototype construction. Those physical gaps require a socket/underside or prototype-specific factory record, not speculative decompilation. The candidate remains partial.

Equal-authority factory disagreements are recorded separately as unresolved conflicts: Sol14 duplicate auxiliary pin, Sol17 downstream plug and Sol16 load type. They remain promotion blockers even when another source confirms public addresses.
