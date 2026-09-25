# Data East Secret Service (1988) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`b49f27dd97ad6a106a2f2bf4a0181bda86e58e31b0e88efe3663e614ace237e3`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 38 loads the library and line 220 leaves keyboard handling to the script:

```vbscript
LoadVPM "01530000","de.vbs",3.1
.HandleKeyboard=0
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
Sub table1_KeyDown(ByVal Keycode)   ' line 276
    If keycode = LeftTiltKey Then Nudge 90, 5:PlaySound SoundFX("fx_nudge", 0), 0, 1, -0.1, 0.25   ' line 277
    If keycode = RightTiltKey Then Nudge 270, 5:PlaySound SoundFX("fx_nudge", 0), 0, 1, 0.1, 0.25   ' line 278
    If keycode = CenterTiltKey Then Nudge 0, 6:PlaySound SoundFX("fx_nudge", 0), 0, 1, 0, 0.25   ' line 279
    If keycode = PlungerKey Then PlaySoundAtVol "fx_PlungerPull", Plunger, 1 :Plunger.Pullback   ' line 280
    If vpmKeyDown(keycode) Then Exit Sub   ' line 281
End Sub   ' line 282
Sub table1_KeyUp(ByVal Keycode)   ' line 284
    If keycode = PlungerKey Then PlaySoundAtVol "fx_plunger", Plunger, 1 : Plunger.Fire   ' line 285
    If vpmKeyUp(keycode) Then Exit Sub   ' line 286
End Sub   ' line 287
```

The trailing `' line NNNN` markers above are added here to give the location and are not in the script.

The script never writes `Controller.Switch(30)` or `Controller.Switch(31)`.

The table's script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
