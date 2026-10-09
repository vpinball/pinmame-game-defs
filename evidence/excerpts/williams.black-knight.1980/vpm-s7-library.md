# VPinMAME System 7 script library (`s7.vbs`) as the retained table loads it

Source: `s7.vbs`, the VPinMAME script library the retained Black Knight table loads (its script's
line 102: `LoadVPM "01560000", "S7.VBS", 3.26`), copied from the operator's Visual Pinball
`Scripts` folder and retained at
`external:pinmame-vpx-sources/williams/black-knight-1980/vpinmame-scripts/s7.vbs` (144 lines, header
`'Last Updated in VBS v3.61`, SHA-256 `88e6f2500f75315b9f5ad01581d9f24a926ad12af43730af01d8bfab8e5cfe03`),
byte-identical to `scripts/s7.vbs` in `vpinball/vpinball` at commit
`6237ce52ef9cee9b9814881f6289d207bf9a3d2b`. Transcribed verbatim from the file; only the lines cited
are quoted.

Lines 20-38 (`S7 Data`):

```
' Flipper Solenoid
Const GameOnSolenoid = 25
' Cabinet switches
Const swAdvance      = -7
Const swUpDown       = -6
Const swCPUDiag      = -5
Const swSoundDiag    = -4
Const swTilt         =  1
Const swBallRollTilt =  2
Const swStartButton  =  3
Const swCoin3        =  4
Const swCoin2        =  5
Const swCoin1        =  6
Const swSlamTilt     =  7
Const swHSReset      =  8
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 83
Const swULFlip       = 81
```

From `vpmKeyDown` (the cabinet flipper keys):

```
			Case LeftFlipperKey
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
			Case RightFlipperKey
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

`swULFlip` (81) and `swURFlip` (83) are written only for the staged upper-flipper keys and only when
the table registers an upper-flipper solenoid (`vpmFlips.FlipperSolNumber(2/3) <> 0`), which the
Black Knight table does not: its upper flippers move from the same `SolLFlipper` / `SolRFlipper`
callbacks as the lower ones.

What this settles: a table running this library writes the left and right flipper buttons to public
switches 84 and 82, and takes the game-on (flipper enable) state from solenoid 25.
