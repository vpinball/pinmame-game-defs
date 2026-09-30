# Taxi spatial admission and remaining blockers

Extraction manifest: vpx-sources/williams/taxi/Taxi (Williams 1988)1.2/extraction-vpxtool-git-v0.33.3/manifest.json, SHA256 b23d0faa0bacef495223a65b6c79a209c2eaa628e6675abb98c0c404cea09363. Retained table SHA256 7c6f52b24e7fabc761611d33b7eab5de15b9025f954fb4e423f3219e09af9c40.

Exact table bounds: left0/top0/right952/bottom1974 VPX units. x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top), round to six places with repository pinmame_game_defs.spatial.extract_spatial_candidates / _round_point. Coordinate sources and controller-routing sources are separate; factory PDF60/62 leaders reconcile the projected assembly/site identities, without a manual pixel transform or invented frame fit.

| Device | Object | Extracted path | Method | x | y | Role |
| --- | --- | --- | --- | --- | --- | --- |
| switch.13 | JoyrideEject | gameitems/Kicker.JoyrideEject.json | center | 0.168928 | 0.134554 | sensor |
| switch.14 | sw14 | gameitems/Trigger.sw14.json | center | 0.381828 | 0.112842 | sensor |
| switch.15 | sw15 | gameitems/Trigger.sw15.json | center | 0.487395 | 0.117908 | sensor |
| switch.16 | sw16 | gameitems/Trigger.sw16.json | center | 0.598477 | 0.12576 | sensor |
| switch.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | sensor |
| switch.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | sensor |
| switch.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | sensor |
| switch.23 | sw23 | gameitems/Gate.sw23.json | center | 0.733665 | 0.166148 | sensor |
| switch.24 | sw24 | gameitems/HitTarget.sw24.json | position | 0.252626 | 0.136398 | sensor |
| switch.25 | sw25 | gameitems/Gate.sw25.json | center | 0.193533 | 0.415986 | sensor |
| switch.26 | sw26 | gameitems/Gate.sw26.json | center | 0.725053 | 0.421859 | sensor |
| switch.27 | sw29 | gameitems/HitTarget.sw29.json | position | 0.425158 | 0.385132 | sensor |
| switch.28 | sw28 | gameitems/HitTarget.sw28.json | position | 0.480173 | 0.373417 | sensor |
| switch.29 | sw27 | gameitems/HitTarget.sw27.json | position | 0.536633 | 0.361892 | sensor |
| switch.30 | sw30 | gameitems/HitTarget.sw30.json | position | 0.83469 | 0.530838 | sensor |
| switch.31 | sw31 | gameitems/HitTarget.sw31.json | position | 0.833246 | 0.555978 | sensor |
| switch.32 | sw32 | gameitems/HitTarget.sw32.json | position | 0.83167 | 0.581687 | sensor |
| switch.33 | sw33P | gameitems/Primitive.sw33P.json | world-space mesh bounds center | 0.212611 | 0.265196 | sensor |
| switch.34 | sw34P | gameitems/Primitive.sw34P.json | world-space mesh bounds center | 0.733085 | 0.228081 | sensor |
| switch.35 | Catapult | gameitems/Kicker.Catapult.json | center | 0.050566 | 0.589215 | sensor |
| switch.36 | RightLock | gameitems/Kicker.RightLock.json | center | 0.917146 | 0.303642 | sensor |
| switch.37 | sw37 | gameitems/Trigger.sw37.json | center | 0.059611 | 0.740502 | sensor |
| switch.38 | sw38 | gameitems/Trigger.sw38.json | center | 0.128414 | 0.718212 | sensor |
| switch.39 | sw39 | gameitems/Trigger.sw39.json | center | 0.852789 | 0.739932 | sensor |
| switch.40 | sw40 | gameitems/Trigger.sw40.json | center | 0.779129 | 0.714256 | sensor |
| solenoid.3 | Catapult | gameitems/Kicker.Catapult.json | center | 0.050566 | 0.589215 | effect |
| solenoid.4 | sw28 | gameitems/HitTarget.sw28.json | position | 0.480173 | 0.373417 | effect |
| solenoid.5 | JoyrideEject | gameitems/Kicker.JoyrideEject.json | center | 0.168928 | 0.134554 | effect |
| solenoid.6 | sw31 | gameitems/HitTarget.sw31.json | position | 0.833246 | 0.555978 | effect |
| solenoid.7 | SpinoutKicker | gameitems/Kicker.SpinoutKicker.json | center | 0.850053 | 0.112589 | effect |
| solenoid.8 | RightLock | gameitems/Kicker.RightLock.json | center | 0.917146 | 0.303642 | effect |
| solenoid.9 | TopGate | gameitems/Wall.TopGate.json | drag-point mean | 0.225696 | 0.06774 | effect |
| solenoid.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | effect |
| solenoid.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | effect |
| solenoid.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | effect |

## Projection classes and world geometry

Visible Trigger rollover wires14..16 and37..40 anchor wire-actuation sites; the contact bodies are below the playfield. Gates23/25/26 anchor the blade-actuated passage sites, not gate-home sensors. Kicker anchors13/35/36 record occupied holes; coil3/5/8 effects share the named catapult/eject assembly sites. Coil7 uses the scripted Spinout ejection site, not a separately measured coil mount or switch43 contact. Jet effects17/19/21 share the ring centers. Coil4/6 effects project the common reset assembly to its middle target face. Coil9 uses the four-vertex mean of the narrow TopGate collision wall, locating route opening rather than the coil mount.

Drop27..32 project the underplayfield opto sensing site to each raised face. Factory PDF62 parts/leader endpoints, ROM names and successful L4 display responses settle left/middle/right27/28/29 and top/middle/bottom30/31/32. The retained script153 binds sw27/sw28/sw29 directly, but the table faces are ordered sw29/sw28/sw27 from left to right. Use sw29 for physical27 and sw27 for physical29; this proven consumed-table defect belongs in notes, not machine conflicts.

World export: review-artifacts/taxi-1988/followup-1/luna-inventory/vpxtool-obj-vpu/Taxi (Williams 1988)1.2.obj, SHA256 dfb0965ef597f88e5c94bcb63cfbb6532a57394e15993707fe88a2dc6dc50cce; vpxtool git:v0.33.3 export obj --units vpu. Its x/y frame agrees with independently positioned sw14..16 wires and all six HitTargets; the export applies object transforms. Inverse rotation about the HitTarget position gives local XY bounds approximately[-20.9,20.9]/[-3.2,3.2] for all six targets. The -24deg middle-bank and90deg right-bank rotations leave their world pivots fixed; oblique AABB center offsets are at most0.041135 VPU and do not change target order. No primitive local position is admitted.

Ramp33/34 use modeled animated wire sw33P/sw34P world-mesh bounds centers, respectively(202.405365,523.496430) and(697.897130,450.231950) VPU. Their pivots and invisible Trigger centers differ; they are neither averaged nor substituted. These are projected resting wire-actuation sites on the crossed ramps, supported by factory leaders33/34 and separate script242..262 Hit/Unhit routing. The table wires do not survey the physical microswitch bodies. Full raw export and independent remeasurement are retained externally.

## Concrete rejected mechanical classes

Playfield tilt9: factory leader below the left apron; no retained contact object or established manual-to-table frame. Outhole10 and trough11/12: abstract stack occupancy, with Drain/BallRelease ball-transfer helpers and no individually modeled contacts. Shooter22: script handlers exist but no sw22 in the870-object extraction. Slings18/20: collision-edge walls and animation geometry do not locate paired leaf contacts or actuator pivots/strike sites. Spinout43: abstract stack occupancy and transfer/ejection helpers do not locate a microswitch. Spinout44: invisible triangular circulation trigger on Bol30; stored center is outside its drag-point triangle, so it cannot locate a physical wire/contact. Coils1/2: Drain/BallRelease do not establish outhole lever or feeder-crank locations. Each affected device carries its own limitation.

## Remaining physical and variant blockers

Every controlled physical lamp/flasher socket and complete GI population remains unproved. Backbox and coin-door effects need quantities and routing even when playfield placement is not applicable. C1..C5 each1p+1i, C6/C7 each1p+1d, C8 two playfield, Jackpot1p+2i, Joyride1p from the wiring table. Dome PCB F/L designator capacity is not installed population proof. No glow helper, bulb centroid or invented socket is admitted.

The35 observed recreation anchors do not earn author-ready credit. Prototype construction and full competition differences remain unresolved; only L3/L4/LG1/P5 archives are supplied. Acquired full factory manuals/OCR, exact VPX/script/world export, pinned source, legal ROM tables and successful retained traces settle the admitted claims. Ghidra cannot establish physical socket geometry or prototype construction.

Three equal-authority factory disagreements remain unresolved: Sol14 duplicate auxiliary pin, Sol17 downstream plug and Sol16 load type. They remain promotion blockers even when public addresses are proved.
