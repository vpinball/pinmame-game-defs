# Williams Earthshaker (1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`0c2bb47c3469e9b04d28a44f94469c3935050aa4975d31ee12e6fb344392eb72`) and the VPinMAME script library
it loads, retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, "Last Updated in VBS v3.61") and
`core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 52 loads the library, lines 54-55 clear both upper flipper solenoid numbers, and line 805
leaves keyboard handling to the script:

```vbscript
LoadVPM "01120100", "S11.VBS", 3.22
NoUpperLeftFlipper
NoUpperRightFlipper
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

`core.vbs` lines 2854-2855 route the table's handlers to them:

```vbscript
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

`script.vbs` `Table1_KeyDown` (line 878) writes the matrix addresses itself (lines 881-882) and hands the
key to the library at line 900; `Table1_KeyUp` (line 903) mirrors it with `= 0` at lines 907-908 and calls
`KeyUpHandler` at line 927:

```vbscript
	If keycode = LeftFlipperKey Then Controller.Switch(58)  = 1
	If keycode = RightFlipperKey Then Controller.Switch(57) = 1
	If KeyDownHandler(keycode) Then Exit Sub
	If keycode = LeftFlipperKey Then Controller.Switch(58)  = 0
	If keycode = RightFlipperKey Then Controller.Switch(57) = 0
	If KeyUpHandler(keycode) Then Exit Sub
```

Because lines 54-55 set both `FlipperSolNumber` entries to 0, the staged-key branches above never write
`swULFlip` or `swURFlip` on this table.
