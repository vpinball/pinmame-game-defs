# Breakshot — VPW table script and VPinMAME script libraries

Transcribed from the retained VPW table `Breakshot (Capcom 1996) VPW v1.1.vpx`, whose embedded script
was extracted with vpxtool as `script.vbs` (169,448 bytes, SHA-256
`4d231b5737073c4df944b495a7c9bfe3b175ff42420872edf437099f538a7178`), and from the two VPinMAME script
libraries it loads, retained from the contributor's Visual Pinball installation: `Capcom.vbs` (SHA-256
`03323ded224c5e67b0f7703978529889339e1fd7f73ebdd15002a4a6b794a95e`, "Last Updated in VBS v3.61") and
`core.vbs` (SHA-256 `d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72`). Lines are quoted
verbatim with their line numbers, trailing blanks removed; `...` marks omitted lines.

## Driver and library

```vbs
29: Const cGameName="bsv103", UseSolenoids=2, UseVPMModSol=2, UseLamps=1, UseGI=0, NTweens=23, SSolenoidOn="", SSolenoidOff="", SCoin=""
37: LoadVPM "03060000", "CAPCOM.VBS", 3.61
```

## Solenoid callbacks (lines 227-251)

```vbs
SolCallback(1)			= "SolTrough"			'Drain
SolCallback(2)			= "SolRelease"			'Ball Release
SolCallback(3)			= "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"
'4 Left Slingshot
'5 Right Slingshot
SolCallback(6)			= "Kickback"			'Left Outlane Kicker
SolCallback(7)			= "ResetDropsRight"		'Drop Targets Right
SolCallback(8)			= "RightSaucer"			'Right Saucer
SolCallback(sLRFlipper) = "SolLRFlipper"        '9 Left Flipper
SolCallback(sURFlipper) = "SolURFlipper"        '10 Right Flipper
SolCallback(sLLFlipper) = "SolLLFlipper"        '11 Upper Right Flippper
SolCallback(12)			= "PostUp"				'Center Post Up
SolCallback(13)			= "ResetDropsLeft"		'Drop Targets Left
SolCallback(14)			= "PostRelease"			'Center Post Release (also triggered while firing up)
SolCallback(15)			= "SolRightGate"		'Right Top Gate
SolCallback(16)			= "SolLeftGate" 		'Left Top Gate
'17-24 Not Used
SolCallback(25)			= "CLeftPocket"			'Center Pocket Left
SolCallback(26)			= "CenterPocket"		'Center Pocket Center
'27 Not Used
SolModCallback(28)	    = "FlashLight"			'Flasher Center Pocket
'29 Right Bumper
'30 Center Bumper
'31 Left Bumper
SolCallback(32)			= "CRightPocket"		'Center Pocket Right
```

```vbs
263: Sub FlashLight(p) : s128a.State = p : s128b.State = p : AdjustBulbTint s128a, BL_Flashers : End Sub
```

The three flipper subs move these objects: `Sub SolLLFlipper` (line 550) `LeftFlipper`, `Sub SolLRFlipper`
(line 572) `RightFlipper`, `Sub SolURFlipper` (line 594) `RightUpFlipper` (`596: RightUpFlipper.RotateToEnd`).
The symbolic numbers come from `core.vbs` (below): `sLRFlipper` 46, `sURFlipper` 34, `sLLFlipper` 48. The
comments beside them (`'9 Left Flipper`, `'10 Right Flipper`, `'11 Upper Right Flippper`) do not match the
subs they bind.

## Table_Init (lines 731-786)

```vbs
739: 		.HandleKeyboard=0
...
751: 	vpmNudge.TiltSwitch		= 30
...
755: 	vpmMapLights AllLamps
...
758: 	Set BSBall1 = sw38.CreateSizedballWithMass(Ballsize/2,Ballmass)
759: 	Set BSBall2 = sw37.CreateSizedballWithMass(Ballsize/2,Ballmass)
760: 	Set BSBall3 = sw36.CreateSizedballWithMass(Ballsize/2,Ballmass)
761: 	Controller.Switch(38) = 1
762: 	Controller.Switch(37) = 1
763: 	Controller.Switch(36) = 1
...
766: 	Set CaptiveBall = CBKicker.CreateSizedballWithMass(Ballsize/2,Ballmass)
767: 	Set NewtonBall = NBKicker.CreateSizedballWithMass(Ballsize/2,Ballmass)
...
777: 	Set CenterPostBall = CenterPostKicker.CreateSizedballWithMass(28,Ballmass*2)
...
782: 	PlungerKB.PullBack
...
785: 	CenterPostIsDropped True
```

`AllLamps` holds the 62 lights `l3`-`l64`; each light's TimerInterval equals the number in its name, so
`vpmMapLights` binds lamp N to light `lN`.

## Keys (lines 812-831)

`Table1_KeyDown` handles the plunger, nudges, start sound and coin sounds, then ends with
`If KeyDownHandler(keycode) Then Exit Sub`; `Table1_KeyUp` ends with `If KeyUpHandler(keycode) Then Exit Sub`.
`core.vbs` lines 2841-2842 route those to the system file's handlers:

```vbs
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

## Switch bindings

Bumpers (lines 837-841, tweens and sounds omitted):

```vbs
Sub Bumper1_Hit   : vpmTimer.PulseSw(59) : RandomSoundBumperTop Bumper1 : ...
Sub Bumper2_Hit   : vpmTimer.PulseSw(58) : RandomSoundBumperTop Bumper2 : ...
Sub Bumper3_Hit   : vpmTimer.PulseSw(57) : RandomSoundBumperTop Bumper3 : ...
```

Rollovers and optos (lines 845-891): `SW43_Hit`/`_unHit` write switch 43, and likewise `SW44`, `SW45`, `SW46`,
`SW47`, `SW60`, `SW61`, `SW62`, `SW63`, `SW79`, `SW53`, `SW54` and `SW65`, each to its own number, for
example:

```vbs
845: Sub SW43_Hit:Controller.Switch(43)=1 : End Sub
846: Sub SW43_unHit:Controller.Switch(43)=0:End Sub
...
890: Sub SW65_Hit:Controller.Switch(65)=1 : End Sub
891: Sub SW65_unHit:Controller.Switch(65)=0:End Sub
```

Targets (lines 898-936):

```vbs
Sub sw51_Hit : STHit 51 : End Sub
...
Sub sw55_Hit : STHit 55 : End Sub
...
Sub sw76_Hit : STHit 76 : End Sub
...
Sub sw77_Hit : STHit 77 : End Sub
...
Sub sw78_Hit : STHit 78 : End Sub
...
Sub sw48_Hit : DTHit 48 : End Sub
Sub sw49_Hit : DTHit 49 : End Sub
Sub sw50_Hit : DTHit 50 : End Sub
Sub sw73_Hit : DTHit 73 : End Sub
Sub sw74_Hit : DTHit 74 : End Sub
Sub sw75_Hit : DTHit 75 : End Sub

Sub ResetDropsRight(enabled)
	If enabled Then
		RandomSoundDropTargetReset BM_RDT2
		DTRaise 48
		DTRaise 49
		DTRaise 50
	End If
End Sub

Sub ResetDropsLeft(enabled)
	If enabled Then
		RandomSoundDropTargetReset BM_LDT2
		DTRaise 73
		DTRaise 74
		DTRaise 75
	End If
End Sub
```

Lines 2502-2507 and 2731-2735 bind those numbers to the target walls:

```vbs
Set DT48 = (new DropTarget)(sw48, sw48a, BP_RDT1, 48, False)
Set DT49 = (new DropTarget)(sw49, sw49a, BP_RDT2, 49, False)
Set DT50 = (new DropTarget)(sw50, sw50a, BP_RDT3, 50, False)
Set DT73 = (new DropTarget)(sw73, sw73a, BP_LDT1, 73, False)
Set DT74 = (new DropTarget)(sw74, sw74a, BP_LDT2, 74, False)
Set DT75 = (new DropTarget)(sw75, sw75a, BP_LDT3, 75, False)
...
Set ST51 = (new StandupTarget)(sw51, BP_sw51, 51)
Set ST55 = (new StandupTarget)(sw55, BP_sw55, 55)
Set ST76 = (new StandupTarget)(sw76, BP_sw76, 76)
Set ST77 = (new StandupTarget)(sw77, BP_sw77, 77)
Set ST78 = (new StandupTarget)(sw78, BP_sw78, 78)
```

`OnDTDropped` (line 2639) sets `Controller.Switch(DTArray(index).Sw) = 1`; a standup target's switch is set by
`STHit` (line 2785) and cleared by `OnSTBounced` (line 2791).

Trough, outhole and kickback (lines 942-991):

```vbs
Sub sw38_Hit():Controller.Switch(38) = 1:UpdateTrough:End Sub
Sub sw38_UnHit():Controller.Switch(38) = 0:UpdateTrough:End Sub
Sub sw37_Hit():Controller.Switch(37) = 1:UpdateTrough:End Sub
Sub sw37_UnHit():Controller.Switch(37) = 0:UpdateTrough:End Sub
Sub sw36_Hit():Controller.Switch(36) = 1:UpdateTrough:End Sub
Sub sw36_UnHit():Controller.Switch(36) = 0:UpdateTrough:End Sub

Sub sw35_Hit():Controller.Switch(35) = 1:UpdateTrough:RandomSoundDrain sw35:End Sub
Sub sw35_UnHit():Controller.Switch(35) = 0:UpdateTrough:End Sub
...
Sub UpdateTroughTimer_Timer
	If sw36.BallCntOver = 0 Then sw37.kick 60, 9
	If sw37.BallCntOver = 0 Then sw38.kick 60, 9
	Me.Enabled = 0
End Sub
...
Sub SolTrough(enabled)
	If enabled Then
		sw35.kick 57, 20
	End If
End Sub

Sub SolRelease(enabled)
	If enabled Then
		sw36.kick 60, 9
		RandomSoundBallRelease sw36
	End If
End Sub
...
Sub Kickback(Enabled)
	If Enabled Then
		SoundKicker
		PlungerKB.Fire
	Else
		PlungerKB.PullBack
	End If
End Sub
```

Centre post (lines 1000-1003 and 1015-1017):

```vbs
Sub PostUp(Enabled) : If Enabled Then CenterPostIsDropped False : Tween(0).Clear().TargetSpeed(30, 30.0/60.0).Run(GetRef("OnCenterPostUp")) : End If : End Sub
Sub PostRelease(Enabled) : If Enabled Then CenterPostIsDropped True : Tween(0).Clear().TargetSpeed(0, 37.0/180.0).Run(GetRef("OnCenterPostDown")) : End If : End Sub
Sub OnCenterPostUp(id, z) : Controller.Switch(66) = 1 : End Sub
Sub OnCenterPostDown(id, z) : Controller.Switch(66) = 0 : End Sub
...
		CenterPostWall001.IsDropped = dropped
		CenterPostWall002.IsDropped = dropped
		CenterPostWall003.IsDropped = dropped
```

Top gates (lines 1058-1106): `SolRightGate` sets `RightGate.Open = True` while enabled and `SolLeftGate`
sets `LeftGate.Open = True`; each closes its gate from the gate's own timer after the coil releases
(`' Filters out PWM not handled by PinMame`).

Saucer and centre pockets (lines 1110-1158), each kicking its ball only while its switch is set:

```vbs
Sub sw67_Hit : set KickerBall67 = activeball : Controller.Switch(67) = 1 : SoundSaucerLock : End Sub
Sub sw67_UnHit : Controller.Switch(67) = 0 : End Sub
Sub RightSaucer(Enable)
    If Enable then
		If Controller.Switch(67) <> 0 Then
			KickBall KickerBall67, 0, 0, 50, 0
...
Sub sw68_Hit : set KickerBall68 = activeball : Controller.Switch(68) = 1 : SoundSaucerLock : End Sub
...
Sub CLeftPocket(Enable)
    If Enable then
		If Controller.Switch(68) <> 0 Then
			KickBall KickerBall68, 0, 0, 15, 0
...
Sub CenterPocket(Enable)
    If Enable then
		If Controller.Switch(69) <> 0 Then
			KickBall KickerBall69, 0, 0, 15, 0
...
Sub CRightPocket(Enable)
    If Enable then
		If Controller.Switch(70) <> 0 Then
			KickBall KickerBall70, 0, 0, 15, 0
```

Slingshots (lines 1161-1200, animation lines omitted):

```vbs
Sub RightSlingShot_Slingshot
...
Sub RightSlingShotUpdate(id, step)
...
	Case 2: x1 = True  : x2 = False : y = 20 : Controller.Switch(41) = 1 ' Fully out
	Case 1: x1 = False : x2 = True  : y = 10 : Controller.Switch(41) = 1
	Case 0: x1 = False : x2 = False : y =  0 : Controller.Switch(41) = 0 ' Rest pose
...
Sub LeftSlingShot_Slingshot
...
Sub LeftSlingShotUpdate(id, step)
	Dim x, x1, x2, y : Select Case step
	Case 2: x1 = True  : x2 = False : y = 20 : Controller.Switch(42) = 1 ' Fully out
	Case 1: x1 = False : x2 = True  : y = 10 : Controller.Switch(42) = 1
	Case 0: x1 = False : x2 = False : y =  0 : Controller.Switch(42) = 0' Rest pose
```

No sub writes switches 21, 29, 33, 34, 52 or 71.

## `Capcom.vbs`

Lines 20-35:

```vbs
Const swCoin1       = 01
Const swCoin2       = 02
Const swCoin3       = 03
Const swCoin4       = 04
Const swDiagnostic  = 08
Const swStartButton = 07
Const swTilt        = 10
Const swSlamTilt    = 09
Const swBuyIn       = 11

Const swLRFlip      = 82
Const swLLFlip      = 84
Const swURFlip      = 81
Const swULFlip      = 83

Const GameOnSolenoid = 51
```

`vpmKeyDown`, lines 64-84 (the matching `vpmKeyUp` cases at lines 96-111 release the same switches):

```vbs
			Case LeftFlipperKey
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
			Case RightFlipperKey
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
				If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
					vpmFlips.FlipUR True
					If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
				End If
...
			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
			Case keyInsertCoin1  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
...
			Case StartGameKey    .Switch(swStartButton) = True
			Case keySelfTest     .Switch(swDiagnostic)  = NOT .Switch(swDiagnostic)
			Case keySlamDoorHit  .Switch(swSlamTilt)    = True
```

## `core.vbs`

Lines 2848-2852:

```vbs
'-- Flipper solenoids (all games)
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

`Class cvpmFlips2` (line 2066) is the fast-flip object behind `vpmFlips` when `UseSolenoids=2`. Line 2090 sets
its callbacks from those constants, and lines 2188-2201 flip a callback straight from a key while the ROM's
flipper circuit is on (the game-on solenoid, `GameOnSolenoid` 51):

```vbs
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
...
	Public Property Let Flip(aIdx, ByVal aEnabled) 'Key Flip: Indexed base flip... may keep may not
...
		If OnOff and FlippersEnabled or DebugOn then
			If Not cb is Nothing Then cb aEnabled
...
	Public Sub FlipUL(aEnabled): Flip(2)=aEnabled :End Sub : Public Sub FlipUR(aEnabled): Flip(3)=aEnabled :End Sub
```
