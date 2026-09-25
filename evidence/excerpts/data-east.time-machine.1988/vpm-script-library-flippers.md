# Data East Time Machine (1988) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`1ab7a5cfd7c6e55652a1fc4f9a28e05fd55e24b732b897355e0daec1a5602ee1`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files. This script mixes CRLF line ends with bare CR characters; line numbers here count a bare CR as a line break, as the VPX script editor does, so a tool that splits on LF alone reports lower numbers.

`script.vbs` line 302 loads the library and line 438 leaves keyboard handling to the script:

```vbscript
LoadVPM "00990300", "DE.VBS", 3.10
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

`core.vbs` lines 2854-2855 route the table's handlers to them:

```vbscript
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

`core.vbs` lines 2862-2863 give the solenoid numbers the table's flipper callbacks bind (script lines 823-824 below):

```vbscript
Const sLRFlipper = 46
Const sLLFlipper = 48
```

The table's key handling, with the flipper and library lines:

```vbscript
Sub Table1_KeyDown(ByVal keycode)   ' line 716
	If keycode = LeftFlipperKey Then   ' line 717
		FlipperActivate LeftFlipper, LFPress   ' line 718
		PinCab_LeftFlipperButton.X = PinCab_LeftFlipperButton.X + 8   ' line 719
	End If   ' line 720
	If keycode = RightFlipperKey Then   ' line 721
		FlipperActivate RightFlipper, RFPress   ' line 722
		PinCab_RightFlipperButton.X = PinCab_RightFlipperButton.X - 8   ' line 723
	End If   ' line 724
...
	If KeyDownHandler(keycode)Then Exit Sub   ' line 761
End Sub   ' line 762
Sub Table1_KeyUp(byval Keycode)   ' line 764
	If keycode = LeftFlipperKey Then   ' line 765
		PinCab_LeftFlipperButton.X = PinCab_LeftFlipperButton.X - 8   ' line 766
	End If   ' line 767
	If keycode = RightFlipperKey Then   ' line 768
		PinCab_RightFlipperButton.X = PinCab_RightFlipperButton.X + 8   ' line 769
	End If   ' line 770
...
	If KeyUpHandler(keycode)Then Exit Sub   ' line 784
End Sub   ' line 785
...
SolCallback(sLRFlipper) = "SolRFlipper" 'Fastflips   ' line 823
SolCallback(sLLFlipper) = "SolLFlipper" 'Fastflips   ' line 824
...
Sub SolLFlipper(Enabled) 'Left flipper solenoid callback   ' line 939
	If Enabled Then   ' line 940
		LF.Fire  'leftflipper.rotatetoend   ' line 941
		Controller.Switch(15) = True   ' line 942
...
	Else   ' line 949
		FlipperDeActivate LeftFlipper, LFPress   ' line 950
		LeftFlipper.RotateToStart   ' line 951
		Controller.Switch(15) = False   ' line 952
...
Sub SolRFlipper(Enabled) 'Right flipper solenoid callback   ' line 960
	If Enabled Then   ' line 961
		RF.Fire 'rightflipper.rotatetoend   ' line 962
		Controller.Switch(16) = True   ' line 963
...
	Else   ' line 970
		FlipperDeActivate RightFlipper, RFPress   ' line 971
		RightFlipper.RotateToStart   ' line 972
		Controller.Switch(16) = False   ' line 973
```

The trailing `' line NNNN` markers above are added here to give the location and are not in the script.

Those are the only lines in `script.vbs` that write `Controller.Switch(15)` or `Controller.Switch(16)` (lines 942, 952, 963, 973).

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
