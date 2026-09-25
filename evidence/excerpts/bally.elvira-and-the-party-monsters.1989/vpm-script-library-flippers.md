# Bally Elvira and the Party Monsters (1989) — VPinMAME script-library flipper constants

Source: the VPinMAME script library the retained table loads at runtime (`script.vbs` line 5
`ExecuteGlobal GetTextFile("controller.vbs")`, line 11 `LoadVPM "01560000", "S11.VBS", 3.26`),
retained from the contributor's working installation (`Visual Pinball/Scripts`) as `s11.vbs`
(SHA-256 `5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`) and `core.vbs`
(SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`s11.vbs` lines 10-14 load `core.vbs` and `VPMKeys.vbs`. Lines 37-40 define:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

Its `vpmKeyDown` (line 69) sets the flipper switches from the cabinet keys (lines 73-80):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

and `vpmKeyUp` (line 104) clears them the same way with `= False` (lines 108-115).

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

Its "Flipper solenoids (all games)" block (lines 2861-2865) defines:

```vbscript
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The retained table's `Table1_KeyDown` (script.vbs lines 208-213) and `Table1_KeyUp` (lines 215-220)
call the library before their own `Controller.Switch(57/58)` lines, and the table binds
`SolCallback(sLRFlipper)` and `SolCallback(sLLFlipper)`:

```vbscript
Sub Table1_KeyDown(ByVal KeyCode)
	If KeyDownHandler(keycode) Then Exit Sub
	If keycode = PlungerKey Then Plunger.Pullback:playsound"plungerpull"
    If keycode=RightFlipperKey Then Controller.Switch(57)=1
    If keycode=LeftFlipperKey Then Controller.Switch(58)=1
End Sub

Sub Table1_KeyUp(ByVal KeyCode)
	If KeyUpHandler(keycode) Then Exit Sub
	If keycode = PlungerKey Then Plunger.Fire:PlaySound"plunger"
    If keycode=RightFlipperKey Then Controller.Switch(57)=0
    If keycode=LeftFlipperKey Then Controller.Switch(58)=0
End Sub
```

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
