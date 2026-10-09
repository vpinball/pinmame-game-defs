# Pin-Bot (Williams 1986) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs` of `PinBot (Williams 1986).vpx`, SHA-256
`164eb3b24ae1be991ad2646d2b80292453712eb6f76658f06d9f936e35a23776`) and the VPinMAME script library it
loads, retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, "Last Updated in VBS v3.61") and
`core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.
The table asks for library version 3.26; the retained library is newer, and the lines quoted below are the
ones the table's flipper keys reach.

`script.vbs` line 13 loads the library, and lines 49-50 leave mechanisms and keyboard handling to the script:

```vbscript
LoadVPM "01560000", "S11.VBS", 3.26
		.HandleMechanics=0
		.HandleKeyboard=0
```

`s11.vbs` lines 37-40:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`s11.vbs` `vpmKeyDown` (line 69) sets the lower flipper switches from the cabinet keys (lines 73 and 79), and
`vpmKeyUp` (line 104) clears them the same way with `= False`:

```vbscript
			Case LeftFlipperKey
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
			Case RightFlipperKey
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions write the upper constants only from a staged flipper key and only while `vpmFlips`
holds an upper flipper solenoid number.

`core.vbs` lines 2854-2855 route the table's key handlers to the library:

```vbscript
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

`script.vbs` `Table1_KeyDown` calls `KeyDownHandler` at line 128 and `Table1_KeyUp` calls `KeyUpHandler` at
line 159:

```vbscript
	If KeyDownHandler(keycode) Then Exit Sub
	If KeyUpHandler(keycode) Then Exit Sub
```

Lines 209-210 bind the synthetic flipper outputs:

```vbscript
SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

No line of the script writes `Controller.Switch(10)` or `Controller.Switch(11)`, or any of `81-88` by number.
The script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and
never defines `cSingleLFlip` or `cSingleRFlip`.
