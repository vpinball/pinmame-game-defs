# Retained Mata Hari VPX bindings

Allknowing2012, with JPSalas VP9 lineage and JimmyFingers' saucer
simulation credited in both embedded scripts. Both set
`cGameName` to `matahari` and load `Bally.vbs`. Both use
`vpmMapLights InsertLights`, where each member's TimerInterval
is its address. The collections agree by membership. Matching
coordinates are shared-derived observations.

| Script binding | Objects or effect |
| --- | --- |
| 1 | Saucer release, Kicker1, host switch 32 |
| 2–5 | Chimes at 10/100/1000/10000 |
| 6 | Knocker sound |
| 7 | Outhole stack, Drain and BallRelease, host switch 8 |
| 13, 15 | Left and right bank resets, timer delay 500 ms |
| Lower flipper callbacks | Rotate RightFlipper / LeftFlipper |
| 19 | GameOn gates simulated nudge and switches visual GILights |
| 17–20 | Target6–Target9 (right, top to bottom in VPX geometry) |
| 21–24 | Target1–Target4 (left, bottom to top) |
| 25/26, 28–31, 33/34 | Named rollover trigger closures and releases |
| 27 | Two upper slingshot-style wall triggers |
| 35/36 | Lower RightSlingShot / LeftSlingShot events |
| 37/38/39/40 | Bumper4 / Bumper1 / Bumper3 / Bumper2 |

The lower bumpers and slings have VPX-native motion upon ball contact.
The physical output identities come from the isolated stock ROM run
and the factory driver sheet. The factory orders the right switches
17 through 20 from bottom to top. The tables assign the same sequence
from top to bottom. The physical positions follow FO 579, using
Target9/8/7/6 respectively. The upper rebound walls are contact
surrogates for the parallel 10-point switches and have no physical
slingshot coils. Umagnet is a virtual approximation of the saucer
lip. BallRelease is a hidden feed proxy upstream of the native VPX
manual plunger.

The stock backglass lamps' `Light1`–`Light4b` and `B1`–`B4`
are desktop proxies in player-view coordinates. `BumpLight1` and
`BumpLight4` are both in InsertLights at 41. `BumpLight4` is the
right bottom fixture and `BumpLight1` is the left bottom fixture
whose factory binding is 57. The table's `BumpLight3` has timer 57
but belongs to GILights, and its upper right position is a different
fixture. `BumpLight2` is also in GILights, with timer 20. Their timers
do not bind either upper bumper to the ROM matrix.

The pinned `sverrewl/vpxtable_scripts` script
`Mata Hari (Bally 1978) v2.0.0.vbs` at
`0c036bb61b4b4e8c778c37559f6795df8cd1521e` pulses switch 38 for
bumper 3 (lower left) and 37 for bumper 4 (lower right) at
lines 1210–1211. Its `l41_animate` uses one light's intensity
to fade both assemblies at lines 3737–3742. Stock three-ball
gameplay publishes both 41 and 57 on the first A/B completion.
For factory behavior, bind the right lower cap to 41 and the
left lower cap to 57. [Native run](native-runs.md)

`L22` has timer 2 and occupies the 5K bonus insert. `L22a` has
timer 22 and occupies the A/B 2K insert. Several same-timer
insert overlays share an outline or paint different parts of one
artwork region. Neither object count nor glow center measures a
socket. The 1977 and 1978 source checks cover the full extraction,
then recompute admitted object anchors from the retained gameitems.
