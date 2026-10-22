# Star Wars identity and retained implementation readings

Method: manual transcription by the primary curator, checked against the
retained original HTML, script and library bytes on 2026-10-22. This is a
factual derivative, not a redistribution licence for those artifacts.

## Identity

Retained `ipdb-wayback.html`, SHA-256
`e7316dee4043faf4351180bb2f90a7466ea1a6acb9549cdf1378333eb632a893`.
Machine page https://www.ipdb.org/machine.cgi?id=2358; resolved unmodified capture
https://web.archive.org/web/20250108044008id_/https://www.ipdb.org/machine.cgi?id=2358.
Downloaded 2026-10-22, completed-file UTC LastWriteTime 15:17:50.
Attribution: Internet Pinball Database; rights NOASSERTION.

The page identifies Star Wars by Data East, IPD number 2358, manufactured
October 15, 1992, model 500-5524-01, four players, Data East/Sega Version 3
electronics. It describes two flippers, four pop bumpers, two slingshots,
five standup targets, two scoops, a three-bank drop target, a single bar/drop
target, a vertical upkicker and a cabinet shifter instead of a manual plunger.
It links an official 20th-anniversary software upgrade released December 24,
2012. That listing does not document EPROM socket fitting or establish every
later ROM's physical compatibility. The manual's game and assemblies agree
with this physical identity; the VPX header was not used as identity authority.

## VPW runtime implementation

Retained embedded `script.vbs`, SHA-256
`1d5252b9ef7d1d00646df732661a07b384d6d5cb14798ff86337a00de1c7d144`.
Attribution: VPW crew, Dids666 and DJRobX and the embedded contributors;
copyright retained, NOASSERTION. This is VPW v1.2.2, not the Bigus table.

Lines 114,127,165-174 select `stwr_107` (comment Patched), load DE.VBS, and
disable native keyboard and mechanics handling. The later harness uses the
authorized original CPU 1.03 instead; its diagnostics do not prove patched
gameplay or physical revision compatibility.

Complete output callback/declared special-output region, lines 481-518:

| Public output | Runtime assignment / declaration |
| --- | --- |
| 1 | bsTroughSolIn |
| 2 | bsTroughSolOut |
| 3 | SolAutoPlungerIM |
| 4 | SolLeftEject.SolOut |
| 5 | SolLeftPopper |
| 6 | ResetDrops |
| 7 | SolRightEject.SolOut |
| 9 | SolR2 |
| 11 | Sol11 |
| 12 | comment: Deathstar Entrance Bar Motor; cvpmMech.Sol1=12 |
| 13 | comment: Not Used |
| 14 | comment: Not Used |
| 15 | comment: R2D2-2 & Deathstar Rotation Motors; cvpmMech.Sol1=15 |
| 16 | SolKickback |
| 17 | comment: Top Turbo Bumper |
| 18 | comment: Left Turbo Bumper |
| 19 | comment: Right Turbo Bumper |
| 20 | comment: Bottom Turbo Bumper |
| 21 | comment: Left Slingshot |
| 22 | comment: Right Slingshot |
| 25 | Sol25 / Flasher 1R |
| 26 | SetLamp 126 / Flasher 2R |
| 27 | Sol27 / Flasher 3R |
| 28 | SetLamp 128 / Flasher 4R |
| 29 | Sol29 / Flasher 5R |
| 30 | Sol30 / Flasher 6R |
| 31 | Sol31 / Flasher 7R |
| 32 | SetLamp 132 / Flasher 8R |
| sLRFlipper | SolRFlipper |
| sLLFlipper | SolLFlipper |

There is no callback 8 in this region although SolKnocker is defined below it.
The factory knocker and ROM-named output 8 are not absent hardware.

Complete mechanism initialization regions, lines 180-241:

| Instance | Configuration and references |
| --- | --- |
| bsTrough | Size=4; InitSwitches Array(11,13,12,10); InitExit BallRelease,90,7; Balls=3; CreateEvents with Drain |
| plungerIM | InitImpulseP sw14,65,0.5; Switch14; Random0.05 |
| mechDeathStarDoor | vpmMechOneSol + vpmMechReverse; Sol1=12; Length220; Steps72; Acc30; Ret0; AddSw41 at0; AddSw42 at71; UpdateDeathStarDoor |
| mechDeathStar | Sol1=15; Linear+Circle+OneSol; Acc60; Ret2; Length220; Steps360; UpdateDeathStar |
| SolRightEject | InitSaucer sw33,33,220,85; KickZ1.2 |
| SolLeftEject | InitSaucer sw37,37,163,70; KickZ1.2 |
| Kickback | PullBack at initialization |

These speed, length and phase numbers are software parameters, not measured
physical specifications. Lines 246-276 consume entrance events 34/35 and direct
VUK arrival through AddVUK; its 200ms timer increments dsBalls and asserts 36.
SolLeftPopper, on output 5, kicks a ball and decrements the count, clearing 36
only when empty. Lines 279-352 rotate DeathStar, invoke UpdateR2Head, and move
R2Head/R2Body vertically from R2UpSol. UpdateDeathStarDoor maps bar height to
target 40 collidability. Output 9 lift and output 15 rotation are separate.

Lines 314-316 declare R2HeadDir=1, R2HeadMin=-80, R2HeadMax=60.
UpdateR2Head changes direction near those limits. These are VPW artwork
parameters, not measurements of physical head travel.

Complete key-handler region, lines 363-434 (all handled keys and side effects):

| Handler/key | Effect |
| --- | --- |
| KeyDown PlungerKey or LockBarKey | Sets both Controller.Switch(50) and (51) to 1 |
| KeyDown StartGameKey | SoundStartButton; DisableLUTSelector=1 |
| KeyDown LeftTiltKey | Nudge 90,5; SoundNudgeLeft |
| KeyDown RightTiltKey | Nudge 270,5; SoundNudgeRight |
| KeyDown CenterTiltKey | Nudge 0,3; SoundNudgeCenter |
| KeyDown LeftMagnaSave | Sets only Controller.Switch(51)=0; if LUT selector enabled, decrements LUTSet, wrapping below 0 to 16; optionally plays click or hyperdrive; SetLUT and ShowLUT |
| KeyDown RightMagnaSave | Sets only Controller.Switch(51)=1; if LUT selector enabled, increments LUTSet, wrapping above 16 to 0; optionally plays click or hyperdrive; SetLUT and ShowLUT |
| KeyDown LeftFlipperKey | FlipperActivate LeftFlipper,LFPress |
| KeyDown RightFlipperKey | FlipperActivate RightFlipper,RFPress |
| KeyDown AddCreditKey or AddCreditKey2 | Randomly selects Coin_In_1, Coin_In_2 or Coin_In_3 sound |
| End of KeyDown | Calls vpmKeyDown(keycode), exits if handled |
| KeyUp PlungerKey or LockBarKey | Clears both Controller.Switch(50) and (51) to 0 |
| KeyUp LeftFlipperKey | FlipperDeActivate LeftFlipper,LFPress |
| KeyUp RightFlipperKey | FlipperDeActivate RightFlipper,RFPress |
| End of KeyUp | Calls vpmKeyUp(keycode), exits if handled |

Neither Magna-Save key writes switch 50. Neither has a KeyUp branch here:
their switch 51 setting latches until another write, including the
Plunger/LockBar handler. The helpers above describe keyboard conveniences,
not a change to physical switch fitment.

Lines 556-569 call SetGI with solenoid 11. SetGI (1284 onwards) explicitly
labels True as GI off, sets local lamp 111 to zero and extinguishes the GI
collection. False turns it on. Lines 1172-1175 assign the GI collection and
callback to local Lampz111 and initialize that helper on. No native lamp 111
is published by the driver.

## VPinMAME DE.VBS library

Retained `review-artifacts/vpm-script-libs/de.vbs`, SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`;
`core.vbs`, SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.
Attribution: VPinMAME script-library contributors, retained installed VBS v3.61;
rights NOASSERTION. The table loads this library and calls vpmKeyDown/Up at
script lines 422/434.

Complete DE data constant region, lines 21-36:

| Constant | Value |
| --- | --- |
| GameOnSolenoid | 23 |
| swBlack | -7 |
| swGreen | -6 |
| swTilt | 1 |
| swBallRollTilt | 2 |
| swStartButton | 3 |
| swCoin1 | 4 |
| swCoin2 | 5 |
| swCoin3 | 6 |
| swSlamTilt | 7 |
| swLRFlip | 82 |
| swLLFlip | 84 |
| swURFlip | 86 |
| swULFlip | 88 |

The generic swBallRollTilt name is not game fitment; Star Wars uses fourth coin
at 2 and explicitly lacks ball-roll tilt. vpmKeyDown sets lower flipper 84/82
True and vpmKeyUp clears them. Green toggles its maintained state; Black is
True while pressed and False on release. Staged upper keys can write 88/86
only when vpmFlips has a nonzero upper solenoid number; this game's pinned
ROM cannot read that column and declares no upper button/EOS mask. Such writes
have no effect on fitted hardware.

## Native diagnostic readings

The complete 66 switch, 64 lamp and 29 named coil/flash phases are transcribed
in `tools/star_wars_runtime.json`, beside exact raw trace/frame hashes and
selection times. `evidence/runtime/data-east/star-wars-stwr_103-service-tests.json`
wraps them in the standard evidence schema. Names were visually checked against
the retained contact sheets; they are not OCR guesses. Source and artifact
roles, raw host stimuli, repeated pulse limitations and the unused software
names are explicitly distinguished there and in the knowledge note.
