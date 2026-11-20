# Last Action Hero (Data East 1993) - flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, extracted from `Last Action Hero (Data East 1993) VPW v1.1.vpx`, SHA-256 `1038027da4bdabe7a447d96df6eb79bb3830b2af18a17330d709feb4eaa139e5`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256 `8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`) and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files; the table script is Windows-1252 text with CRLF line ends.

Quoted lines are verbatim except for whitespace: the trailing space of `script.vbs` line 356 is dropped so that the excerpt passes Git's whitespace check, and the indentation is shown as the script prints it. The retained script's SHA-256 above stays authoritative.

`script.vbs` line 58 loads the library, line 64 selects the ROM, and lines 120 and 124 leave keyboard and mechanics handling to the script:

```vbscript
LoadVPM "01000200", "DE.VBS", 3.46
Const cGameName = "lah_113"
        .HandleKeyboard = 0
        .HandleMechanics = 0
```

`de.vbs` lines 21-36 (cabinet switches and flipper switches):

```vbscript
Const GameOnSolenoid = 23
' Cabinet switches
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
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same functions write the upper constants 86 and 88 only from a staged flipper key and only while `vpmFlips.FlipperSolNumber(3)` or `(2)` is non-zero (`de.vbs` lines 68-70, 74-76, 78-79 in `vpmKeyDown`, 100-102, 106-108, 110-111 in `vpmKeyUp`):

```vbscript
			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
```

`core.vbs` line 2090 sets the default solenoid numbers, lines 2854-2855 route the script's handlers to the library, and lines 2862-2865 define the numbers:

```vbscript
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The table's key handling (`script.vbs` lines 325-365). The flipper keys only start the table's own flipper physics (`FlipperActivate` / `FlipperDeActivate`) before the key reaches `vpmKeyDown` (line 349) or `vpmKeyUp` (line 364); the plunger key writes matrix switches 8 and 62 and the lock-bar key writes 62:

```vbscript
	If keycode = PlungerKey Then
		Controller.Switch(8) = 1
		Controller.Switch(62) = 1  'smart bomb
	End If
	If keycode = LeftFlipperKey Then FlipperActivate LeftFlipper, LFPress
	If keycode = RightFlipperKey Then FlipperActivate RightFlipper, RFPress
	If keycode = LockBarKey Then Controller.Switch(62) = 1
    If vpmKeyDown(keycode) Then Exit Sub
	If keycode = LeftFlipperKey Then FlipperDeActivate LeftFlipper, LFPress
	If keycode = RightFlipperKey Then FlipperDeActivate RightFlipper, RFPress
	If keycode = LockBarKey Then Controller.Switch(62) = 0
	If keycode = PlungerKey Then
		Controller.Switch(8) = 0
		Controller.Switch(62) = 0  'smart bomb
	End If
	If vpmKeyUp(keycode) Then Exit Sub
```

These are lines 340-346 and 349 of `Table1_KeyDown` and lines 353-359 and 364 of `Table1_KeyUp`.

The solenoid callbacks the flippers use (`script.vbs` lines 413-414); the subs they call (`SolLFlipper` from line 418, `SolRFlipper` from line 436) fire the flipper with `LF.Fire` / `RF.Fire` while the solenoid is on and `RotateToStart` when it is off:

```vbscript
SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

The table never writes `Controller.Switch` 63, 64 or 81-88 itself, never references `vpmFlips`, never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, and never defines `cSingleLFlip` or `cSingleRFlip`.
