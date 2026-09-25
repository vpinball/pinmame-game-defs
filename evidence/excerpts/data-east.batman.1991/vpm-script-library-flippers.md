# Data East Batman (1991) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`f78f6b40b92c6acef4febe659fd891620773aa6a18715d2ace0cfa6565c1c53b`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 182 loads the library and line 271 leaves keyboard handling to the script:

```vbscript
LoadVPM "01120100", "DE.VBS", 3.36
.HandleKeyboard = 0
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
Sub Table1_KeyDown(ByVal Keycode)   ' line 374
...
	If keycode = LeftFlipperKey Then FlipperActivate LeftFlipper, LFPress   ' line 436
	If keycode = RightFlipperKey Then FlipperActivate RightFlipper, RFPress   ' line 437
	'** nFozzy - end   ' line 438
	If vpmKeyDown(keycode) Then Exit Sub   ' line 439
End Sub   ' line 440
...
Sub Table1_KeyUp(ByVal Keycode)   ' line 443
...
	If keycode = LeftFlipperKey Then FlipperDeActivate LeftFlipper, LFPress   ' line 460
	If keycode = RightFlipperKey Then FlipperDeActivate RightFlipper, RFPress   ' line 461
	'** nFozzy - end   ' line 462
	If vpmKeyUp(keycode) Then Exit Sub   ' line 464
End Sub   ' line 465
```

The trailing `' line NNNN` markers above are added here to give the location and are not in the script.

The script never writes `Controller.Switch(15)` or `Controller.Switch(16)`.

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper` itself and never names a staged flipper key, but it defines `UseSolenoids` (line 188) and `cSingleLFlip`/`cSingleRFlip` (lines 192, 193) and calls `vpmInit` (line 264):

```vbscript
Const UseSolenoids = 2   ' line 188
Const cSingleLFlip = 0   ' line 192
Const cSingleRFlip = 0   ' line 193
vpmInit Me   ' line 264
```

`core.vbs` `vpmInit` calls `vpmFlips.Init` at line 2312. `cvpmFlips2.Init` leaves early only when `UseSolenoids` does not evaluate (lines 2101-2102), which it does here, and then clears the upper flipper numbers itself (lines 2106-2119). VBScript's `Not` is bitwise, so `Not 0` is -1 (True) and both calls run; only a constant defined as True (-1) skips one. With the numbers cleared, the staged-key lines above never write `swURFlip` or `swULFlip` on this table:

```vbscript
		On Error Resume Next 'If there's no usesolenoids variable present, exit
			call eval(UseSolenoids) : if err then exit Sub
...
		'Set Solenoid
		On Error Resume Next
			'For some WPC games (IJ) that reuse upper flipper
			'switch numbers, and legacy fast flip code, disable
			'flippers if cSinglexFlip is set.
			If not cSingleLFlip Then
				if err.number = 0 then NoUpperLeftFlipper
			End If
			err.clear
			If not cSingleRFlip Then
				if err.number = 0 then NoUpperRightFlipper
			End If
			err.clear
		On Error Goto 0
...
	vpmFlips.Init
```
