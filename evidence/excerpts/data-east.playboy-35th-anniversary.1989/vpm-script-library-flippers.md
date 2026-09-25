# Data East Playboy 35th Anniversary (1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`83e632d397afbec660ea356b1820aadbd648d0a90d4affdce5bfc4e864bb0da5`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de2.vbs` (SHA-256
`96fc634c7d6529a0566c753e296b287a1402636b38aa9bef63afebbf49f20b04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 43 loads the library and line 109 leaves keyboard handling to the script:

```vbscript
LoadVPM "01210000", "de2.vbs", 3.1
.HandleKeyboard = 0
```

`de2.vbs` lines 33-36:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`de2.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys (lines 67 and 73), and `vpmKeyUp` (line 94) clears them the same way with `= False` (lines 99 and 105):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions also write the upper constants (81 and 83), but only from a staged flipper key and only while `vpmFlips` holds an upper flipper solenoid number (`de2.vbs` lines 68-79 in `vpmKeyDown`; lines 100-111 repeat them with `= False` in `vpmKeyUp`):

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
Sub table1_KeyDown(ByVal Keycode)   ' line 300
	If keycode = LeftFlipperKey Then   ' line 301
		FlipperActivate LeftFlipper, LFPress   ' line 302
		VR_CabFlipperLeft.x = VR_CabFlipperLeft.x +6   ' line 303
	End If   ' line 304
	If keycode = RightFlipperKey Then   ' line 306
		FlipperActivate RightFlipper, RFPress   ' line 307
		VR_CabFlipperRight.x = VR_CabFlipperRight.x -6   ' line 308
	End If   ' line 309
...
    If vpmKeyDown(keycode)Then Exit Sub   ' line 320
...
End Sub   ' line 328
Sub table1_KeyUp(ByVal Keycode)   ' line 330
	If keycode = LeftFlipperKey Then   ' line 331
		FlipperDeActivate LeftFlipper, LFPress   ' line 332
		VR_CabFlipperLeft.x = VR_CabFlipperLeft.x -6   ' line 333
	End If   ' line 334
	If keycode = RightFlipperKey Then   ' line 335
		FlipperDeActivate RightFlipper, RFPress   ' line 336
		VR_CabFlipperRight.x = VR_CabFlipperRight.x +6   ' line 337
	End If   ' line 338
    If vpmKeyUp(keycode)Then Exit Sub   ' line 339
```

The trailing `' line NNNN` markers above are added here to give the location and are not in the script.

The script never writes `Controller.Switch(15)` or `Controller.Switch(16)`.

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
