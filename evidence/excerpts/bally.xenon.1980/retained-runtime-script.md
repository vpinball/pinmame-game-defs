# Xenon2.5.2 retained runtime regions

Exact embedded script SHA256 3a8e128c1c43ffbccb5f93ba6d8a4f8445e6ff360e1ddcccf6cd2576345ebc1c. One-based inclusive line ranges.

## Credits, lines1-21

```vb
'**********************
'  Xenon Bally(1980)
' original VPX table by: jpsalas
' modded in 2017 by: HauntFreaks, Bord, Borgdog
' modded lighting, graphics and layout by: HauntFreaks
' 3D ramps by: Bord
'**********************
' upgrade v2.0 (2023)
' graphics remastered, resampled by: HauntFreaks
' upgrades by: TastyWasps
'* nFozzy Physics
'* Fleep Sounds
'* Dynamic Ball Shadows
'* Hybrid VR Room
'**********************
' upgrade v2.5 (2024)
'* NEW Ramps/Tube/Textures by: Schlabber34
'* NEW Primitive Playfield Mesh by: Bord
'* NEW Saucer/Kicker code by: Apophis
'* Physical Measurements and Photos by: wrd1972
'**********************
```

## ROM/libraries, lines51-63

```vb
Const BallMass = 1

LoadVPM "01550000", "Bally.vbs", 3.26

Dim bsTrough, bsLeftHole, bsOuthole, dtRBank ',bsTopHole
Const cGameName = "Xenon"

Const UseSolenoids = 2
Const UseLamps = 0
Const UseGI = 0
Const UseSync = 0
Const HandleMech = 0
Const tnob = 5
```

## Stacks/targets, lines135-185

```vb
    Set bsTrough = New cvpmBallStack
    With bsTrough
        .InitSw 8, 2, 28, 0, 0, 0, 0, 0
        .InitKick ballrelease, 90, 4
        .InitEntrySnd "fx_Solenoid", "fx_Solenoid"
        .InitExitSnd SoundFX("BallRelease1", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
        .IsTrough = True
        .Balls = 1
    End With

    'Left hole
    Set bsLeftHole = New cvpmBallStack
    With bsLeftHole
        .InitSaucer sw33, 33, 100, 10
        .KickForceVar = 2
        .KickAngleVar = 2
        .InitExitSnd SoundFX("Saucer_Kick", DOFContactors), SoundFX("Saucer_Kick", DOFContactors)
        .InitAddSnd SoundFX("Saucer_Enter_1", DOFContactors)
    End With

'    'Right hole
'    Set bsTopHole = New cvpmBallStack
'    With bsTopHole
'        .InitSaucer sw34, 34, 165, 10
'        .KickForceVar = 2
'        .KickAngleVar = 2
'        .InitExitSnd SoundFX("Saucer_Kick", DOFContactors), SoundFX("Saucer_Kick", DOFContactors)
'        .InitAddSnd SoundFX("Saucer_Enter_1", DOFContactors)
'        .CreateEvents "bsTopHole", sw34
'    End With

    'Droptargets
    set dtRBank = new cvpmdroptarget
    With dtRBank
        .InitDrop Array(sw21,sw22,sw23,sw24), Array(21, 22, 23, 24)
        .Initsnd SoundFX("fx_droptarget", DOFContactors), SoundFX("fx_resetdrop", DOFContactors)
        '.CreateEvents "dtRBank" 'this doesn't work with the new droptargets
    End With

    'Main Timer init
    PinMAMETimer.Interval = PinMAMEInterval
    PinMAMETimer.Enabled = 1

    bsTrough.AddBall 1



	setup_backglass

End Sub

```

## Switches, lines289-358

```vb
    End Select
    RStep = RStep + 1
End Sub

' Rubbers (switches)
Sub sw26_Hit():vpmTimer.PulseSw 26:End Sub
Sub sw26a_Hit():vpmTimer.PulseSw 26:End Sub

' Spinner
Sub sw5_Spin():vpmTimer.pulsesw 5:PlaySound "Spinner":End Sub

' Bumpers
Sub Bumper1_Hit:vpmTimer.PulseSw 40:RandomSoundBumperTop Bumper1:End Sub
Sub Bumper2_Hit:vpmTimer.PulseSw 39:RandomSoundBumperTop Bumper2:End Sub
Sub Bumper3_Hit:vpmTimer.PulseSw 38:RandomSoundBumperMiddle Bumper3:End Sub
Sub Bumper4_Hit:vpmTimer.PulseSw 37:RandomSoundBumperBottom Bumper4:End Sub

' Rollover & Ramp Switches
Sub sw1_Hit:Controller.Switch(1) = 1:End Sub
Sub sw1_UnHit:Controller.Switch(1) = 0:End Sub

Sub sw17_Hit:w17.IsDropped=1:Controller.Switch(17) = 1:End Sub
Sub sw17_UnHit:w17.IsDropped=0:Controller.Switch(17) = 0:End Sub

Sub sw18_Hit:w18.IsDropped=1:Controller.Switch(18) = 1:End Sub
Sub sw18_UnHit:w18.IsDropped=0:Controller.Switch(18) = 0:End Sub

Sub sw19_Hit:w19.IsDropped=1:Controller.Switch(19) = 1:End Sub
Sub sw19_UnHit:w19.IsDropped=0:Controller.Switch(19) = 0:End Sub

Sub sw20_Hit:w20.IsDropped=1:Controller.Switch(20) = 1:End Sub
Sub sw20_UnHit:w20.IsDropped=0:Controller.Switch(20) = 0:End Sub

Sub sw25_Hit:Controller.Switch(25) = 1:End Sub
Sub sw25_UnHit:Controller.Switch(25) = 0:End Sub

Sub sw27_Hit:Controller.Switch(27) = 1:WireRampOn True:End Sub
Sub sw27_UnHit:Controller.Switch(27) = 0:End Sub

Sub sw29_Hit:Controller.Switch(29) = 1:End Sub
Sub sw29_UnHit:Controller.Switch(20) = 0:End Sub

Sub sw30_Hit:Controller.Switch(30) = 1:End Sub
Sub sw30_UnHit:Controller.Switch(30) = 0:End Sub

Sub sw31_Hit:Controller.Switch(31) = 1:End Sub
Sub sw31_UnHit:Controller.Switch(31) = 0:End Sub

Sub sw32_Hit:Controller.Switch(32) = 1:End Sub
Sub sw32_UnHit:Controller.Switch(32) = 0:End Sub

' Standup Targets
Sub sw3_Hit:vpmTimer.PulseSw 3:End Sub
Sub sw4_Hit:vpmTimer.PulseSw 4:End Sub

' Drop Targets (Retro Baby)
Sub sw21_Hit:PlaySound SoundFX("fx_droptarget", DOFContactors), 0, 1, 0.1, 0.15:End Sub 'hit event only for the sound
Sub sw21_Dropped:dtRBank.hit 1: End Sub

Sub sw22_Hit:PlaySound SoundFX("fx_droptarget", DOFContactors), 0, 1, 0.1, 0.15:End Sub 'hit event only for the sound
Sub sw22_Dropped:dtRBank.hit 2: End Sub

Sub sw23_Hit:PlaySound SoundFX("fx_droptarget", DOFContactors), 0, 1, 0.1, 0.15:End Sub 'hit event only for the sound
Sub sw23_Dropped:dtRBank.hit 3: End Sub

Sub sw24_Hit:PlaySound SoundFX("fx_droptarget", DOFContactors), 0, 1, 0.1, 0.15:End Sub 'hit event only for the sound
Sub sw24_Dropped:dtRBank.hit 4: End Sub

' Drain & holes
Sub sw33_Hit():bsLeftHole.AddBall 0:End Sub
```

## Outputs, lines375-389

```vb
SolCallback(1) = "dtRBank.SolDropUp"
SolCallback(2) = "dtRBank.SolHit 4,"
SolCallback(3) = "dtRBank.SolHit 3,"
SolCallback(4) = "dtRBank.SolHit 2,"
SolCallback(5) = "dtRBank.SolHit 1,"
SolCallback(6) = "vpmsolsound SoundFX(""fx_knocker"",DOFKnocker),"
SolCallback(7) = "bsTrough.SolIn"
SolCallback(8) = "bsTrough.SolOut"
SolCallback(9) = "bsLeftHole.SolOut"
SolCallback(17) = "SolOutTopHole"
SolCallback(19) = "ACRelay"
'SolCallback(20) = "PowerOn"

'Solenoid Subs
Sub ACRelay(enabled)
```

## Top saucer, lines407-431

```vb
	kball.vely = sin(rangle)*kvel
End Sub


'Top Hole
Sub sw34_Hit
    set KickerBal34 = activeball
    Controller.Switch(34) = 1
    SoundSaucerLock
End Sub

Sub sw34_UnHit
    Controller.Switch(34) = 0
End Sub

Sub SolOutTopHole(Enabled)
    If Enabled then
		If Controller.Switch(34) <> 0 Then
			KickBall KickerBal34, 165+rnd*2, 9+rnd*2, 5, 10
			SoundSaucerKick 1, sw34
		Else
			SoundSaucerKick 0, sw34
		End If
	End If
End Sub
```

## Complete lamp dispatch, lines506-600

```vb
Sub LampTimer_timer()
    Dim chgLamp, x
    chgLamp = Controller.ChangedLamps
    If Not IsEmpty(chgLamp) Then
        For x = 0 To UBound(chgLamp)
            LightState(chgLamp(x, 0) ) = chgLamp(x, 1) 'light state as set by the rom
        Next
    End If

	VRDisplayTimer

    ' Lights & Flashers
    LightX 2, l2
    LightX 3, l3
    LightX 4, l4
    LightXm 5, l5b
    LightXm 5, l5c
    LightX 5, l5
    LightX 6, l6
    LightX 7, l7
    LightX 8, l8
    LightX 9, l9
    Flashm 10, Diode1
    Flash 10, Diode2
    LightX 11, l11
    LightX 12, l12
    Flashm 14, Diode9
    Flash 14, Diode10
    LightX 15, l15
    LightX 17, l17
    LightX 18, l18
    LightX 19, l19
    LightX 20, l20
    LightXm 21, l21b
    LightXm 21, l21c
    LightX 21, l21
    LightX 22, l22
    LightX 23, l23
    LightX 24, l24
    LightX 25, l25
    LightXm 26, l26a
    LightX 26, l26
    LightX 28, l28
    Flashm 30, Diode7
    Flash 30, Diode8
    LightX 31, l31
    LightX 33, l33
    LightX 34, l34
    LightX 35, l35
    LightX 36, l36
    LightXm 37, l37b
    LightXm 37, l37c
    LightX 37, l37
    LightX 38, l38
    LightX 39, l39
    LightX 40, l40
    LightX 41, l41
    LightX 42, l42
    LightX 44, l44
    Flashm 46, Diode5
    Flash 46, Diode6
    LightX 47, l47
    LightX 49, l49
    LightX 50, l50
    LightX 51, l51
    LightXm 52, l52b
    LightX 52, l52
    LightXm 53, l53b
    LightXm 53, l53c
    LightX 53, l53
    LightX 54, l54
    LightX 55, l55
    LightX 56, l56
    LightX 57, l57
    LightX 58, l58
    LightX 59, l59
    LightX 60, l60
    Flashm 62, Diode3
    Flash 62, Diode4
    LightX 63, l63
    LightXm 69, l69a
    LightX 69, l69
    Flashm 199, f199
	Flash 199, f199a
End Sub

' div lamp subs

Sub InitFlashers()
    Dim x
    For x = 0 to 200
        LightState(x) = 0     	 ' light state: 0=off, 1=on, -1=no change (on or off)
        FlashSpeedUp(x) = 0.5    ' Fade Speed Up
        FlashSpeedDown(x) = 0.25 ' Fade Speed Down
        FlashMax(x) = 1          ' the maximum intensity when on, usually 1
```

## GI artifact, lines687-708

```vb
'Bally Xenon
'added by Inkochnito
Sub editDips
    Dim vpmDips:Set vpmDips = New cvpmDips
    With vpmDips
        .AddForm 700, 400, "Xenon - DIP switches"
        .AddChk 7, 10, 180, Array("Match feature", &H08000000)                                                                                                                                                       'dip 28
        .AddChk 205, 10, 115, Array("Credits display", &H04000000)                                                                                                                                                   'dip 27
        .AddFrame 2, 30, 190, "Maximum credits", &H03000000, Array("10 credits", 0, "15 credits", &H01000000, "25 credits", &H02000000, "40 credits", &H03000000)                                                    'dip 25&26
        .AddFrame 2, 106, 190, "Drop target 2X lite adjustment", &H00000020, Array("2X is off at start game", 0, "2X is on at start game", &H00000020)                                                               'dip 6
        .AddFrame 2, 152, 190, "Drop target tube exit value", &H00000040, Array("exit value does not step", 0, "exit value steps up 1", &H00000040)                                                                  'dip 7
        .AddFrame 2, 198, 190, "Drop target special lite", &H00000080, Array("lite steps to 25000", 0, "lite stays lit", &H00000080)                                                                                 'dip 8
        .AddFrame 2, 248, 190, "Outlanes and flipper feed lanes", &H00002000, Array("1 lite comes on then alternates", 0, "both lites come on", &H00002000)                                                          'dip 14
        .AddFrame 2, 298, 190, "Top saucer scoring and Xenon lite", 49152, Array("scores 5,000 and no lite advances", 0, "scores 10,000 and 1 lite advance", &H00004000, "scores 10,000 and 2 lite advances", 49152) 'dip 15&16
        .AddFrame 205, 30, 190, "Balls per game", &HC0000000, Array("2 balls", &HC0000000, "3 balls", 0, "4 balls", &H80000000, "5 balls", &H40000000)                                                               'dip 31&32
        .AddFrame 205, 106, 190, "Side saucer mota special lite", &H00100000, Array("special resets with the score", 0, "special will alternate", &H00100000)                                                        'dip 21
        .AddFrame 205, 152, 190, "Side saucer mota score lites", &H00200000, Array("any lite will reset to 5,000", 0, "any lite will come on for next ball", &H00200000)                                             'dip 22
        .AddFrame 205, 198, 190, "Side saucer mota lite advance", &H00400000, Array("mota lites advance 1 at a time", 0, "mota lites advance 2 times", &H00400000)                                                   'dip 23
        .AddFrame 205, 248, 190, "Side saucer mota 50K, 90K lite", &H00800000, Array("lites step to 50K only", 0, "lites step to 90K", &H00800000)                                                                   'dip 24
        .AddFrame 205, 298, 190, "Game over attract", &H10000000, Array("no voice", 0, "voice says: try me again", &H10000000)                                                                                       'dip 29
        .AddFrame 205, 348, 190, "Top saucer first 2X lites adjust", &H20000000, Array("not in memory", 0, "in memory", &H20000000)                                                                                  'dip 30
        .AddLabel 50, 400, 300, 20, "Set selftest position 17,18 and 19 to 03 for the best gameplay."
```
