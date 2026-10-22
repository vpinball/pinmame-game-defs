# Retained Kiwi 1.0.5 runtime bindings

Exact `script.vbs` SHA-256 `a4206e78394fa2405493a1f26c694e7f934d33a4701e75013894c2242af0181e`; table SHA-256 `50458a3ec79586a307a2cd576efc5d176cb0f3f540ab28f2a197006c32cf6f27`. Direct source read by curator. This factual inventory covers the machine-specific script regions, including the addresses that have no direct Hit sub.

Initialization (125-241): de2.VBS; cGameName baywatch; HandleMechanics=0 and HandleKeyboard=0. Five-ball bsTrough uses InitSw 0,14,13,12,11,10,0,0. bsTroughUp is a separate saucer at BallRelease, switch 15. bsUpVUK uses sw44/44; bsSSScoop sw56/56; bsLowSVuk sw46/46. The drop bank uses sw22/sw23/sw24 and addresses 22/23/24. Plunger1, LaserKick and UpBLaunch are pulled back initially; Botola is closed and RampLG collision helpers select its normal route.

Switch handlers (332-566): ball launch key/lockbar writes 50; front key writes 8. Left/right keys write matrix 63/64 and then pass to de2.vbs, which supplies effective buttons 84/82. Bumper1/2/3 pulse 41/42/43; left/right sling handlers and their optional collision-flipper alternatives pulse 61/62. Drain feeds bsTrough. sw44/56/46 feed their separate ball stacks. sw52 spinner pulses 52. Gate25 and Gate28 pulse 25 and 28; the similarly numbered trigger at 28 is commented out. Rollovers 16,26,30,33,38,39,40,45,47,49,54,55,57,58,59,60 write their own address on Hit and clear on UnHit (16 delays release). Stand-ups 9,17-21,31,32,36,37,48,53 pulse their own address. The drop bank latches its three switches through cvpmDropTarget, not a momentary stand-up callback.

Complete solenoid map (581-606 and 784-785):

| Public address | Callback | Effect |
| --- | --- | --- |
| 1 | TroughLock | Release one bsTrough ball; create/feed the BallRelease bsTroughUp ball |
| 2 | bsTroughUpSolOut | Eject trough up-kicker after table timer delay |
| 3 | AutoBallLaunch | Plunger1.Fire / Pullback |
| 4 | UpBallLaunch | UpBLaunch.Fire / Pullback |
| 5 | bsUpVUKSolOut | Eject bsUpVUK and animate VUKArm |
| 6 | bsLowSVukSolOut | Eject bsLowSVuk |
| 7 | bsSSScoopSolOut | Eject bsSSScoop |
| 8 | KnockerSound | Cabinet knocker sound |
| 9 | UpperG | UpperGate.Open 1/0 |
| 10 | [commented LRABRelay] | Muxing belongs to the controller |
| 11 | GIRelay | Invert Enabled into local SetLamp 200 |
| 12 | LockTrap | Open/close Botola; swap RampLG1/2/3/6 collision routes |
| 13 | AutoFlipper | Both LeftFlipper1 and RightFlipper1 to end/start |
| 14 | LowerG | LowerGate.Open 1/0 |
| 15 | [absent] | No machine callback |
| 16 | dtcbank | Reset three drops, hide the three drop-target GI glow helpers |
| 17-21 | [absent local callbacks] | Bumper/sling geometry responds on its hit; ROM supplies outputs |
| 22 | LaserkickBack | LaserKick.Fire / Pullback |
| 23 | SolRun | Game-on and nudge enable |
| 25-32 | setlamp 191 through setlamp 198 | Eight script-local flasher states |
| 46 (sLRFlipper) | SolRFlipper | RightFlipper and RightFlipper1 |
| 48 (sLLFlipper) | SolLFlipper | LeftFlipper and LeftFlipper1 |

Complete lamp binding inventory (881-1130): NFadeL binds l1-l5, l9, l10, l14-l24, l26-l32 and l36-l63 to their matching matrix number. Number 25 binds both lL25 and lR25. FlashDL drives physical bulb primitives BulboF6, BulboF11, BulboF12, BulboF13, BulboF33, BulboF34, BulboF35; associated f6/f11/f12/f13/f33/f34/f35 are sprites, not extra bulbs. Cabinet lamps 7/8/64 have no playfield binding.

Local 200 drives the G.I. objects: lgi1/lgi2, paired GIBulb1-33 variants, GIBumb2/3, and fgit/fbb effects. GIBulb13gt22/23/24 are target glows at a shared point and are additionally hidden/shown when drops reset/fall. They are not three G.I. sockets. Physical bulb selection keeps one member per GIBulb family (the show_bulb_mesh member where present), plus GIBumb2/3. Backglass fbb1-33 are never playfield emitters.

Local 191 uses f191/f191a and backglass f1r/f1ra. 192 uses l192/l192a/l192b and backglass f2r/f2ra. 193 uses l193/l193a, f193/f193a, DomeBW193 and backglass f3r/f3ra. 194 uses l194, f194 variants, DomeBW194/DomeBW194a and backglass f4r. 195 has only f195a/f195b and backglass f5r/f5ra. 196 has f196 variants, DomeBW196 and backglass f6r/f6ra. 197 uses l197a/l197b/l197c and backglass f7r. 198 uses l198, f198 variants, DomeBW198 and backglass f8r/f8ra. A sprite binding identifies a circuit effect, not a surveyed bulb origin; the missing physical socket objects stay missing.
