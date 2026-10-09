# Diner (Williams 1990) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs` of `Diner VPX 1.2.vpx`, SHA-256
`df18744ca1550d20c2eba5e940b8723dd0fc0498d98f6a252d417bd5429e6162`) and the VPinMAME script library it loads,
retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, "Last Updated in VBS v3.61") and `core.vbs`
(SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files. The table asks
for library version 3.26; the retained library is newer, and the lines quoted below are the ones the table's
flipper keys reach.

`script.vbs` line 329 loads the library, and lines 407 and 411 leave the keyboard and mechanisms to the script:

```vbscript
LoadVPM "01560000", "S11.VBS", 3.26
			.HandleKeyboard = 0
			.HandleMechanics = 0
```

`s11.vbs` lines 37-40:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`s11.vbs` `vpmKeyDown` (line 69) sets the lower flipper switches from the cabinet keys (lines 73 and 79), and
`vpmKeyUp` (line 104) clears them the same way with `= False`:

```vbscript
			Case LeftFlipperKey
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
			Case RightFlipperKey
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions write the upper constants only from a staged flipper key and only while `vpmFlips` holds an
upper flipper solenoid number.

`script.vbs` lines 365-367 leave the synthetic flipper outputs unbound:

```vbscript
'*** flipper solenoids disabled for faster response in KeyDown ***
'SolCallback(sLRFlipper) = "SolRFlipper"
'SolCallback(sLLFlipper) = "SolLFlipper"
```

and `Diner_KeyDown` (line 874) and `Diner_KeyUp` (line 898) move the table's flippers from the keys while the
game-on output it binds with `SolCallback(23)="TiltSol"` (line 338) is on, then hand every key to the library
(lines 895 and 902):

```vbscript
	if keycode = LeftFlipperKey and FlippersEnabled Then SolLFlipper(True)
	if keycode = RightFlipperKey and FlippersEnabled Then SolRflipper(True)
...
	If vpmKeyDown(keycode) Then Exit Sub
...
	If vpmKeyUp(keycode) Then Exit Sub
```

No line of the script writes `Controller.Switch(57)` or `Controller.Switch(58)`, or any of `81-88` by number. The
script never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never names a staged flipper key, and never
defines `cSingleLFlip` or `cSingleRFlip`.
