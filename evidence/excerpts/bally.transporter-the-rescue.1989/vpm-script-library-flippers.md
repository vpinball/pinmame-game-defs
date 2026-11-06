# Retained VPinMAME library and Transporter flippers

Method: manual source-code reading; initial mechanical inventory, checked against both retained files by the primary curator. These are runtime-library facts, not a physical coil-number chart.

The embedded VPW v1.05 script has SHA-256 `ac708574ef0cdd488f1ff4c63da2888d622e609fcf88b818448fd03a214756de` and loads `S11.VBS` version 1.91 with `UseSolenoids = 2`. The retained working-installation library is newer: `s11.vbs` (“Last Updated in VBS v3.61”), SHA-256 `5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`; `core.vbs`, SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.

| Source | Region | Literal or behavior |
| --- | --- | --- |
| s11.vbs | 22 | `GameOnSolenoid = 23` |
| s11.vbs | 24-28 | Advance -7, Up/Down -6, CPU Diagnostics -5, Sound Diagnostics -4, `swTilt = 1` |
| s11.vbs | 37-40 | `swLRFlip = 82`, `swLLFlip = 84`, `swURFlip = 81`, `swULFlip = 83` |
| s11.vbs | vpmKeyDown/vpmKeyUp, 69-130 | Lower keys write 84/82 and call FlipL/FlipR; the upper-key paths call FlipUL/FlipUR and conditionally write their library constants. |
| core.vbs | cvpmFlips2, 2086-2209 | Defaults are left 48, right 46, upper-left 36, upper-right 34. With UseSolenoids 2, Init uses GameOnSolenoid 23, saves the table's callbacks, and substitutes RomFlip wrappers. Flip updates ButtonState and calls the saved callback while enabled. |
| core.vbs | 2479 | Changes at the configured game-on address call TiltSol. |
| core.vbs | 2862-2864 | `sLRFlipper = 46`, `sLLFlipper = 48`, `sURFlipper = 34`. |

Consequently the table can move its upper-right flipper from the local fast-flipper wrapper without PinMAME publishing output 34. The pinned System 11 driver publishes no upper-flipper coil there. Library writes of 81/83 do not turn them into reachable machine inputs: the game's core flipper mask copies only 82/84 into 57/58. The legacy import's claim `swTilt=57` is incorrect for this retained library; the table's tilt helper uses physical plumb tilt 1.
