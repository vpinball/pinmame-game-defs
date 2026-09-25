# Data East Lethal Weapon 3 (1992) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`d6c42eb3bd059ccc8126aa2ba27972ff59beb77ec53cf2efca6c1a9f6a204f11`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 114 loads the library and line 336 leaves keyboard handling to the script:

```vbscript
LoadVPM "03060000", "DE.VBS", 3.36
.HandleKeyboard=0
```

`de.vbs` lines 33-36:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 86
Const swULFlip       = 88
```

`de.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys (lines 67 and 73), and `vpmKeyUp` (line 94) clears them the same way with `= False` (lines 99 and 105):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions also write the upper constants (86 and 88), but only from a staged flipper key and only while `vpmFlips` holds an upper flipper solenoid number (`de.vbs` lines 68-79 in `vpmKeyDown`; lines 100-111 repeat them with `= False` in `vpmKeyUp`):

```vbscript
				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
					vpmFlips.FlipUL True
					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
				End If
...
			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
```

`core.vbs` line 2090 sets those numbers by default, and lines 2061-2062 are the helpers a table calls to clear them:

```vbscript
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
Sub NoUpperLeftFlipper() : vpmFlips.FlipperSolNumber(2) = 0 : End Sub
Sub NoUpperRightFlipper() : vpmFlips.FlipperSolNumber(3) = 0 : End Sub
```

The table's key handling, with the flipper and library lines:

```vbscript
Sub Table1_KeyDown(ByVal KeyCode)   ' line 919
...
	If keycode = LeftFlipperKey Then Controller.Switch(15) = 1   ' line 928
	If keycode = RightFlipperKey Then Controller.Switch(16) = 1   ' line 929
...
	If vpmKeyDown(keycode) Then Exit Sub   ' line 947
End Sub   ' line 948
...
Sub Table1_KeyUp(ByVal KeyCode)   ' line 951
...
	If keycode = LeftFlipperKey Then Controller.Switch(15) = 0   ' line 960
	If keycode = RightFlipperKey Then Controller.Switch(16) = 0   ' line 961
...
	If vpmKeyUp(keycode) Then Exit Sub   ' line 969
End Sub   ' line 970
```

The trailing `' line NNNN` markers above are added here to give the location and are not in the script.

Those are the only lines in `script.vbs` that write `Controller.Switch(15)` or `Controller.Switch(16)` (lines 928, 929, 960, 961).

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
