# VPW v1.05 runtime binding regions

Method: primary curator source-code reading of the exact retained embedded Windows-1252 stream, SHA-256 `ac708574ef0cdd488f1ff4c63da2888d622e609fcf88b818448fd03a214756de`. The table names `tsptr_l3`, uses `UseSolenoids = 2`, disables controller keyboard/mechanism handling and creates three balls in its manually modelled trough. VPW authors retain their rights; the following is a compact factual binding inventory.

| Solenoid | Callback / action |
| --- | --- |
| 1 | ballDrain: kicks Drain |
| 2 | BallKick: kicks BallRelease and clears switch 11 |
| 3 | dtLSolDropUp: raises targets 19, 20, 21 |
| 4 | dtRSolDropUp: raises targets 22, 23, 24 |
| 5 | LeftLockSol: fires LockLSol, timer pulls back |
| 6 | PopperSol: kicks SW15 and clears switch 15 |
| 7 | SolKnocker |
| 8 | RightLockSol: fires LockRSol, timer pulls back |
| 9 | SolGI: enabled means GI off; drives local Lampz 109 |
| 10 | GateOpen: GateSol10 opens at 1 and closes at 0 |
| 11 | Turn1Flash: Flupper flasher 6 |
| 14 | AutoFireSol: fires Kickback, timer pulls back |
| 15 | Turn2Flash: Flupper flasher 5 |
| 16 | Turn3Flash: Turn3Flasher |
| 25 | PF2XFlash: PF2XFlasher |
| 26 | BridgeFlash: BridgeFlasher |
| 27 | TopLeftFlash: Flupper flashers 1 and 2 |
| 28 | JetFlash: Flupper flashers 3 and 4 |
| 29 | BallLockFlash: BallLockFlasher and glow companions |
| 30 | SingleStandupFlash: SingleSUFlasher |
| 31 | BallPopperFlash: BallPopperFlasher and glow companions |
| 32 | PF3XFlash: PF3XFlasher |
| library sLLFlipper / sLRFlipper / sURFlipper | SolLFlipper / SolRFlipper / SolURFlipper: the library wraps the callbacks; upper-right 34 is local wrapper behavior. |

The five commented callbacks 17-21 are sound callbacks, not evidence of absent bumper/slingshot coils. Their physical mapping comes from the manual and the ROM's coil test.

Switch regions bind Drain 10, BallRelease 11, Trough2 12, Trough3 13; SW14/15/16/17; drop walls SW19-24 through DTHit; SW25-27; SW30; SW31; SW33/34; spinner SW35; SW37/39/40/59; Bumper1/2/3 to 60/61/62 and the two slingshots to 63/64. Ordinary occupied triggers assert 1 and release at 0; 16/30/35/60-64 pulse. SW31helper and SW31helper2 change ball velocity without publishing additional switches. Drop switches stay closed while down and clear when raised.

Lampz.MassAssign covers public lamps 1-17 and 19-40. L13/L13B, L14/L14B and L40/L40a are paired art-light objects; LightN companions are glows rather than extra physical lamps. The GI collection has 36 lights: 33 show their own bulb mesh; GI6, GI8 and GI10 are diffuse companions near the three bumper bulbs. Lampz 107/109 are local fade indexes, never additional public lamp addresses. A MassAssign object establishes a runtime binding; an insert overlay or glow does not establish a physical socket centre.
