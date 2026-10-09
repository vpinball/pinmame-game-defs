# Data East The Who's Tommy Pinball Wizard (1994) - flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, extracted from `The Who's Tommy Pinball Wizard (Data East 1994) VPWMod 1.2.1.vpx`, SHA-256 `c6d74cb6fafd0aad6c12129272a3cd0a4f5086b2f75c7f6f8d00850e555717d1`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256 `8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`) and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 105 loads the library, line 130 selects the ROM, and lines 284-285 leave keyboard and mechanics handling to the script:

```vbscript
LoadVPM "02000000", "de.vbs", 3.5
Const cGameName = "tomy_500"	'Custom rom by Soren - better scoring/rules and more blinder!
		.HandleMechanics = 0
		.HandleKeyboard = 0
```

Line 129 keeps the factory set as a commented alternative: `'Const cGameName = "tomy_400"	'Less bugs, but not as fun`.

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

`de.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys, and `vpmKeyUp` (line 94) clears them the same way with `= False`:

```vbscript
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
```

The same functions write the upper constant 88 only from a staged left flipper key and only while `vpmFlips.FlipperSolNumber(2)` is non-zero (`de.vbs` lines 68-70 and 78 in `vpmKeyDown`, 100-102 and 110 in `vpmKeyUp`):

```vbscript
				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
```

`core.vbs` line 2090 sets the default solenoid numbers and lines 2862-2865 define them:

```vbscript
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The table overrides the upper-left number at line 279, right after `vpminit me`:

```vbscript
	vpmFlips.FlipperSolNumber(2) = 47
```

The table's key handling (lines 145-264). `Tommy_KeyDown` sets `Controller.Switch(8)` from keycode 3 (line 147) and clears it in `Tommy_KeyUp` (line 212); with the table option `Const StagedFlipper = 0` (line 34) the left flipper key moves both `LeftFlipper` and the upper `LeftFlipper1` in the table itself (`FlipperActivate LeftFlipper1, LFPress1` and `SolULFlipper True`); both subs end by handing the key to the library:

```vbscript
	If vpmKeyDown(keycode) Then Exit Sub   ' line 207
	If vpmKeyUp(keycode) Then Exit Sub   ' line 264
```

The solenoid callbacks the flippers use (lines 495 and 504-507; line 505 is commented out):

```vbscript
SolCallback(23) = "SolEnableFlips"										'Flipper Board
SolCallback(46) = "SolRFlipper"                         				'Right Flipper
'SolCallback(47) = "SolULFlipper"                        				'Upper Left Flipper
SolCallback(48) = "SolLFlipper"                         				'Left Flipper
SolCallback(51) = "BlinderMove"                         				'Blinder Motor
```

`SolLFlipper` and `SolRFlipper` fire the table flippers only while `bFlippersEnabled`, which `SolEnableFlips` copies from solenoid 23 (lines 1494-1532).

The table never writes `Controller.Switch(63)` or `Controller.Switch(64)`, never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, and never defines `cSingleLFlip` or `cSingleRFlip`.
