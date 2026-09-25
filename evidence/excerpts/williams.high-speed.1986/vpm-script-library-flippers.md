# Williams High Speed (1986) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`149cab01a1fbe7657ffae87f72fa6982ed631653627b938186d5d8ed893195eb`) and the VPinMAME script library
it loads, retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, "Last Updated in VBS v3.61") and
`core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 783 loads the library and line 951 leaves keyboard handling to the script:

```vbscript
LoadVPM "01500000", "S11.VBS", 3.10
        .HandleKeyboard=0
```

`s11.vbs` lines 37-40:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`s11.vbs` `vpmKeyDown` (line 69) sets the lower flipper switches from the cabinet keys (lines 73-74 and 79-80),
and `vpmKeyUp` (line 104) clears them the same way with `= False` (lines 108-109 and 114-115):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions also write the upper constants, but only from a staged flipper key and only while
`vpmFlips` holds an upper flipper solenoid number (`s11.vbs` lines 75-86 in `vpmKeyDown`; lines 110-121 repeat
them with `= False` in `vpmKeyUp`):

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

`core.vbs` line 2855 routes the table's key-up handler to `vpmKeyUp`:

```vbscript
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

`script.vbs` `Table1_KeyDown` (line 1426) calls the library directly at line 1439, and `Table1_KeyUp`
(line 1447) calls `KeyUpHandler` at line 1455:

```vbscript
    If vpmKeyDown(keycode) Then Exit Sub
    If KeyUpHandler(keycode) Then Exit Sub
```

Neither handler writes `Controller.Switch(37)` or `Controller.Switch(38)`, and no other line of the script
writes either address or any of `81-88` by number.

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
