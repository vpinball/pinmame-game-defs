# Retained VPinMAME library behavior

Sources are the actual local `L:/Visual Pinball/Scripts/core.vbs` and `stern.vbs`, both headed `Last Updated in VBS v3.61`. Machine-neutral immutable copies are retained in `vpx-sources/shared/vpinmame-20261106/`; no complete library is redistributed in Git. Rights: NOASSERTION; attribution: VPinMAME script contributors.

| File | SHA-256 | Relevant source region |
| --- | --- | --- |
| core.vbs | a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69 | KeyDownHandler around2854 invokes platform vpmKeyDown; constants2862-2863 identify lower-right held46 and lower-left held48 |
| stern.vbs | b835ce5b0c11c6d268f58c92e534c1677e64cb47e103b33179b82c6c337be0e5 | Constants23-36; keydown73-84; keyup106-117 |

The platform library defines game-on output19, lower-right input82, lower-left84, upper-right81 and upper-left83. The keydown path writes the corresponding lower input True and invokes the flipper helper; keyup writes False. Upper inputs are written only for configured staged flippers. Cabinet start is6, coins1-3, tilt7, self-test-7, CPU diagnostic-6 and sound diagnostic-5.

Its generic `swSlamTilt = 8` constant and slam-key writes are not a machine-specific physical identification. Catacomb's own manual PDF18 labels matrix8 L. FLIPPER BUTTON and separately draws FRONT DOOR SLAM SW from MPU J4-13 B-O to SDU J2-7 Y-R. The cabinet schematic PDF2 draws that separate contact open at rest. PinMAME's generic keyboard name therefore does not establish that this hard-wired contact is address8. The modern 2.0.1 table asserts and clears matrix8 from `LeftFlipperKey`, agreeing with the manual; only the older archive table incorrectly uses `RightFlipperKey`. These software artifacts are documented without inventing a second matrix input.

Physical wiring is read from the retained Catacomb manual and corroborating cabinet sheet, not inferred from these library constants. Synthetic power/hold pairs are established by pinned PinMAME core and the retained traces; a library callback does not measure EOS timing or winding current.
