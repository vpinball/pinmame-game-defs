# Radical flipper and ball-stack library contract

Retained machine-neutral libraries: `review-artifacts/vpm-script-libs/s11.vbs`, SHA256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, and `core.vbs`, SHA256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.
Attribution: VPinMAME contributors; original project license retained. Read from the retained
working installation libraries, not inferred from the table. Method: source-text extraction and
review by primary curator, 2026-11-06.

The Radical scripts load S11.vbs and hand cabinet keys to vpmKeyDown/vpmKeyUp.
S11.vbs lines37-40 defines lower right82, lower left84, upper right81, upper left83.
Its key-down handlers set the lower button switch True, and key-up handlers clear it.
core.vbs defines sLRFlipper46 and sLLFlipper48. The tables bind these to routines that move
both physical flippers on the respective side; this does not create independent upper CPU drives.

Pinned PinMAME reads82/84 into its cabinet-flipper fallback and overwrites matrix57/58 from
them. Consumers drive82/84, never the copied57/58. The library's upper switch constants81/83
do not make those positions ROM-readable on this generation. PinMAME publishes synthetic
45/46 and47/48 as pairs while enabled; these states do not identify physical EOS timing or
individual power/hold winding behavior.

The cvpmBallStack InitSw convention distinguishes its first outhole argument from the subsequent
trough positions. Radical's `InitSw 10,11,12,0,0,0,0,0` therefore means outhole10 plus trough11/12.
The separate popper stack uses `InitSw 0,16,0,0,0,0,0,0`. Its script injects the ball through
sw16a and returns it at the remote sw16 kicker; neither object name alone establishes a physical
coil or contact center.
