# Data East Tales from the Crypt (1993) - flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, extracted from `Tales from the Crypt (Data East 1993)_VPW_V1.01.vpx`, SHA-256 `8dbbd3239aea2ae67362842e14e776b4866257898041012cc166809b8085db61`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256 `8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 264 loads the library and lines 1641-1642 leave keyboard and mechanics handling to the script:

```vbscript
LoadVPM "01120100", "de.vbs", 3.02
.HandleMechanics=0
.HandleKeyboard=0
```

`de.vbs` lines 21-36 (cabinet switches and flipper switches):

```vbscript
Const GameOnSolenoid = 23
Const swBlack        = -7
Const swGreen        = -6
Const swTilt         =  1
Const swBallRollTilt =  2
Const swStartButton  =  3
Const swCoin1        =  4
Const swCoin2        =  5
Const swCoin3        =  6
Const swSlamTilt     =  7

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

The table's key handling, with the library hand-off lines (the `' line NNNN` markers are added here to give the location and are not in the script):

```vbscript
Sub Table1_KeyDown(ByVal KeyCode)   ' line 1708
	If keycode = PlungerKey Or keycode = LockBarKey Then Controller.Switch(62) = 1   ' line 1712
...
	If keycode = LeftFlipperKey Then FlipperActivate LeftFlipper, LFPress   ' line 1720
...
	If KeyDownHandler(keycode) Then Exit Sub   ' line 1737
End Sub   ' line 1782
...
Sub Table1_KeyUp(ByVal KeyCode)   ' line 1788
	If keycode = PlungerKey Or keycode = LockBarKey Then   ' line 1792
		Controller.Switch(62) = 0   ' line 1793
...
	If KeyUpHandler(keycode) Then Exit Sub   ' line 1811
End Sub   ' line 1812
```

`core.vbs` line 2854 defines `Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function`, so the table's flipper keys reach `de.vbs` `vpmKeyDown`/`vpmKeyUp`, which write `swLRFlip = 82` and `swLLFlip = 84`.

The table never writes `Controller.Switch(63)` or `Controller.Switch(64)`. Its `Controller.Switch(62)` writes (lines 1712 and 1793) come from the plunger key and the lock-bar key. The table's flipper subs run from the ROM's solenoids: `SolCallback(sLRFlipper) = "SolRFlipper"` and `SolCallback(sLLFlipper) = "SolLFlipper"` (lines 297-298), and `SolRFlipper` rotates both `RightFlipper` and `RightFlipper1` (lines 650-664), so one right-hand solenoid moves the lower and the upper right flipper.

The table never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
