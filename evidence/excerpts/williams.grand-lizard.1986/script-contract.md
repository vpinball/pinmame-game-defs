# Grand Lizard: retained VPX runtime contract

Source: exact retained `Grand Lizard (Williams 1986).vpx` embedded `script.vbs`
(header V1.3; table metadata V1.39), SHA256
`13576dd5caaf0e356d8a752ca055a0b35c57caaf0417a7bd4e283899fda4af35`.
The pinned corpus `Grand Lizard (Williams 1986) V1.8.5.vbs` at
`sverrewl/vpxtable_scripts` revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`
agrees on the controller mappings summarized here but is not byte-identical.
Authors: 3rdaxis and Slydog43; credits include JP Salas, Rosve and G5K.
Method: curator read of the controller-facing code. This excerpt describes the
code's behavior, not proof of every physical part or socket.

The script loads `S11.VBS`, chooses `cGameName = "grand_l4"`, disables
controller keyboard and mechanism handling, and initializes three trough balls.

| Public solenoid | Code consuming the output |
| ---: | --- |
| 1 | `bsTrough.SolIn` |
| 2 | `dt3B.SolDropUp`, targets 25,26,27 |
| 3 | `dt4L.SolDropUp`, targets 20,21 |
| 4 | `dt4R.SolDropUp`, targets 22,23 |
| 5 | `LockKick`, kicking object `sw34` |
| 6 | `SetFlasher68`, lock-area effect |
| 7 | `SetFlasher69`, left Magna-Save effect |
| 8 | `bsTrough.SolOut` |
| 9 | `mLeftMagnet.Solenoid`, object `LeftMagnet` |
| 10 | `mRightMagnet.Solenoid`, object `RightMagnet` |
| 11 | `PFGI`, inverse state: enabled darkens GI |
| 12 | `SetFlasher67`, three-target-bank effect |
| 13 | `SetFlasher66`, lizard-eye effect |
| 14 | knocker sound |
| 15 | bell sound |
| 17 | slingshot sound |
| 18 | slingshot sound |
| 19 | `SetFlasher70`, right Magna-Save effect |
| `sLRFlipper` / `sLLFlipper` | `RFlipper` / `LFlipper` |

`bsTrough.InitSw 10,12,13,14,0,0,0,0` uses outhole 10 and three trough
positions 12-14. Its output kicker is `BallRelease`. A drain hit adds a ball to
the stack; physical ball movements must provide the corresponding switch states.
The left pair of targets initializes as `Array(sw20,sw21)`, the right pair as
`Array(sw22,sw23)`, and the rear three as `Array(sw25,sw26,sw27)`.
Each drop-target hit handler invokes that bank's `Hit` method.

Switch 11 follows shooter-lane hit/unhit; 15-19 and 29-31 pulse their respective
handlers; spinner 28 pulses on `Spin`; 32-34 follow hit/unhit; 42 pulses on hit;
43 and 44 pulse on left/right slingshot action. Lock output 5 ejects from the
last lock position, object `sw34`; it is not a direct electrical action on any
of the lock switches 32-34.

The table's keys also write matrix 47 (left flipper), 48 (right flipper),
45 (left Magna-Save), and 46 (right Magna-Save), then pass keys to
`vpmKeyDown`/`vpmKeyUp`. The S11 library writes the actual PinMAME flipper
column 84/82. Matrix 48 is consequently overwritten by the core's copy of 82;
the extra table write is redundant. Matrix 47 stays independently writable because
the driver's left `FLIP_SWNO` argument is zero, but both factory switch lists
explicitly mark 47 Not Used. That table write establishes no fitted left lane-change
contact and must not be reproduced as one without separate evidence.

The `Lights()` assignment block binds public lamps 2,7-50,52-64 to same-numbered
`Light` objects. Assignments 1,3,4,5,6 and 51 are commented out, so their absence
from this table's light array says nothing about fitment. Flasher callbacks drive
several glow sprites and helper lights per output; their count does not establish
physical bulb count. `PFGI` drives the `GI` collection plus GI_13/GI_2/GI_14
and changes many render materials; collection members alone are not a wiring list.

The older `GrandLizardV1.5.vbs` credits the same collaboration and shares these
mechanism abstractions. Its pinned corpus header says `Table not verified yet`.
It is supplementary evidence and not an independent layout corroboration.
