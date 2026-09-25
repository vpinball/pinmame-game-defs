# Bally Elvira and the Party Monsters (1989) — VPinMAME script-library flipper constants

Source: the VPinMAME script library the retained table loads at runtime (`script.vbs` line 5
`ExecuteGlobal GetTextFile("controller.vbs")`, line 11 `LoadVPM "01560000", "S11.VBS", 3.26`),
retained from the contributor's working installation (`Visual Pinball/Scripts`) as `s11.vbs`
(SHA-256 `5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`) and `core.vbs`
(SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`s11.vbs` lines 10-14 load `core.vbs` and `VPMKeys.vbs`. Lines 37-40 define:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

Its `vpmKeyDown` (line 69) sets the flipper switches from the cabinet keys (lines 73-80):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

and `vpmKeyUp` (line 104) clears them the same way with `= False` (lines 108-115).

`core.vbs` line 2854 routes the table's handler to it:
`Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function`.
Its "Flipper solenoids (all games)" block (lines 2861-2865) defines:

```vbscript
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The retained table's `Table1_KeyDown` calls `KeyDownHandler(keycode)` before its own
`Controller.Switch(57/58)` lines, and binds `SolCallback(sLRFlipper)` and `SolCallback(sLLFlipper)`.
