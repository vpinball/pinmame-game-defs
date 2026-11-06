# Retained local table runtime contract

Table version 1.0 (metadata June 2017), freneticamnesic and 32assassin.
Embedded script SHA-256 25d0c6e026437c706292eeae4b7908ad8312c27583029a1b0294d22b2d4b8c10.
Factual mapping transcription by Curator, checked against extracted script;
not an independent launch/playtest. Full script and line-numbered extraction
remain external. Coordinate convention: x left→right, y rear→front.

Initialization selects wwfr_103, loads de.vbs 2.34, sets UseSolenoids=1,
UseLamps=0, UseGI=0, HandleMechanics=0 and HandleKeyboard=0.

| Public solenoid | Handler / physical runtime action |
| --- | --- |
| 1 | bsTrough.SolOut, exits at kicker4 |
| 2 | SolBallRelease: clears switch 15 and kicks BallRelease when enabled |
| 3 | bsShooter.SolOut, Shooter saucer with switch 16 |
| 4 | bsRingKick.SolOut, sw28 saucer |
| 5 | bsSVUK.SolOut, capture sw20 / exit sw20a |
| 6 | bsVUK.SolOut, sw40; sw39 pulses200ms then inserts ball here |
| 7 | dtL.SolDropUp, targets sw21,sw22,sw23,sw24 |
| 8 | Knocker sound |
| 9 | dtT.SolDropUp, targets sw30,sw31,sw32 |
| 11 | PFGI: energized→collection GI off; released→on |
| 12 | SolBackDiverter: Flipper4 and RampDiverter 0/40 degrees |
| 13 | SolFlipperDiverter: Flipper3 and LeftDiverter 0/-35 degrees |
| 16 | ShakeTimer callback is commented out |
| 22 | SolRightDiv: enabled starts RightDivT; disabled does nothing |
| 25–32 | SetLamp125–132; these are private fading indices, not public lamps 125–132 |
| sLRFlipper=46 | Moves RightFlipper and RightFlipper1 together |
| sLLFlipper=48 | Moves LeftFlipper and LeftFlipper1 together |

RightDivT alternates divstate false/true, stepping RightDiverter's ObjRotZ up to45
or down to0. URFlip timer swaps TRDiv1/TRDiv2 dropped states. Startup sets
divstate=false and TRDiv2 dropped. Animation speed is not measured hardware timing.

The six-ball stack starts at six and maps contacts14,13,12,11,10,9; release15 is
separate. A captive ball is created separately at CapKicker. Target contacts latch
through cvpmDropTarget; the respective reset outputs raise their whole banks.

| Switch | Bound object / action |
| --- | --- |
| 1 | vpmNudge tilt |
| 9–14 | internal six-ball stack, no six distinct sensor objects |
| 15 | BallRelease |
| 16 | Shooter saucer; similarly named sw16 is not the saucer handler |
| 17,18,25,26,29,45,46,47,52–56 | corresponding sw-number Trigger hit/unhit |
| 19,27 | LeftSlingShot/RightSlingShot Slingshot event |
| 20 | sw20 capture kicker |
| 21–24,30–32 | corresponding HitTarget dropped events |
| 28 | sw28 saucer |
| 33–38 | corresponding standup HitTarget pulse |
| 39 | sw39 kicker destroys incoming ball then transfers to stack40 |
| 40 | sw40 capture kicker |
| 41–44,58 | corresponding Gate hit pulses; sw58s spinner is not the handler |
| 49,50,51 | Bumper1,Bumper2,Bumper3 hit pulses |
| 62 | Plunger and both MagnaSave keys assert1 on down,0 on up |
| 63,64 | Additional direct key writes; pinned core overwrites these copies |

ChangedLamps fills LampState/FadingLevel. UpdateLamps binds NFadeL1–12,14,17–26,
29–44,46,48–51,55,56,60–64 to matching Light objects. Public28 drives L28a and
L28b. Public13,45,47,52,53,54,57,58 drive matching bulb-cover primitives plus
Flasher sprites F13,F45,F47,F52,F53,F54,F57,F58. Public15,16,27,59 are omitted.
The solenoid-driven f125–f132 Light helpers do not enumerate all physical bulbs:
their per-circuit counts are3,2,2,1,2,3,1,2, unlike the complete physical inventory.
No Light, Flasher sprite or primitive origin is accepted as a socket by name alone.

The local VPinMAME libraries retain de.vbs column82/84 and unused staged86/88,
and core.vbs sLRFlipper46/sLLFlipper48. Their bytes are pinned separately.
