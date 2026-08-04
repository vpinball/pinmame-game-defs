' JP's IronMan 2 Armored Adventures v3.0
' Based on The Stern table from 2007

Option Explicit

Randomize

Const BallSize = 50
Const BallMass = 1.7

Dim DesktopMode:DesktopMode = Table1.ShowDT
Dim UseVPMDMD:UseVPMDMD = DesktopMode

On Error Resume Next
ExecuteGlobal GetTextFile("controller.vbs")
If Err Then MsgBox "You need the controller.vbs in order to run this table, available in the vp10 package"
On Error Goto 0

LoadVPM "01560000", "sam.vbs", 3.10

'********************
'Standard definitions
'********************

Const cGameName = "im_186ve" 'vault edition rom
'Const cGameName = "im_186" 'iron man 2 rom

Const UseSolenoids = 1
Const UseLamps = 0
Const UseSync = 0
Const HandleMech = 0

'Standard Sounds
Const SSolenoidOn = "fx_solenoidon"
Const SSolenoidOff = "fx_solenoidoff"
Const SFlipperOn = ""
Const SFlipperOff = ""
Const SCoin = "fx_coin"

'Variables
Dim bsTrough, PlungerIM, Mag1, Mag2, x

'************
' Table init.
'************

Sub Table1_Init
    vpminit Me
    With Controller
        .GameName = cGameName
        If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
        .SplashInfoLine = "Iron-Man 2 (Stern 2007)"
        .HandleKeyboard = 0
        .ShowTitle = 0
        .ShowDMDOnly = 1
        .ShowFrame = 0
        .HandleMechanics = 1
        .Hidden = DesktopMode
        On Error Resume Next
        .Run GetPlayerHWnd
        If Err Then MsgBox Err.Description
    End With

    On Error Goto 0

    Controller.Switch(53) = 1 'sandman down

    'Trough
    Set bsTrough = New cvpmBallStack
    bsTrough.InitSw 0, 21, 20, 19, 18, 0, 0, 0
    bsTrough.InitKick BallRelease, 90, 8
    bsTrough.InitExitSnd "ballrelease", "Solenoid"
    bsTrough.Balls = 4

    ' Magnets
    Set mag1 = New cvpmMagnet
    With mag1
        .InitMagnet Magnet1, 30
        .GrabCenter = False
        .solenoid = 3
        .CreateEvents "mag1"
    End With

    Set mag2 = New cvpmMagnet
    With mag2
        .InitMagnet Magnet2, 30
        .GrabCenter = False
        .solenoid = 4
        .CreateEvents "mag2"
    End With

    'Nudging
    vpmNudge.TiltSwitch = swTilt
    vpmNudge.Sensitivity = 5
    vpmNudge.TiltObj = Array(Bumper1, Bumper2, Bumper3, LeftSlingshot, RightSlingshot)

    'Main Timer init
    PinMAMETimer.Interval = PinMAMEInterval
    PinMAMETimer.Enabled = 1

    'Impulse Plunger
    Const IMPowerSetting = 55 ' Plunger Power
    Const IMTime = 1.1        ' Time in seconds for Full Plunge
    Set plungerIM = New cvpmImpulseP
    With plungerIM
        .InitImpulseP swPlunger, IMPowerSetting, IMTime
        .Switch 23
        .Random 1.5
        .InitExitSnd "fx_popper", "fx_popper"
        .CreateEvents "plungerIM"
    End With

    ' walls
    ClaneUpPost.Isdropped = true
    UpPost.Isdropped = true
    mongerframe.isdropped = 1
    sw5.isdropped = 1
    sw4.isdropped = 1
    sw6.isdropped = 1

'Fast Flips
	On Error Resume Next 
	InitVpmFFlipsSAM
	If Err Then MsgBox "You need the latest sam.vbs in order to run this table, available with vp10.5"
	On Error Goto 0

    RealTime.Enabled = 1

	'Load LUT
	LoadLUT
End Sub

'**********
' Keys
'**********

Sub Table1_KeyDown(ByVal Keycode)
    If keycode = LeftTiltKey Then Nudge 90, 5:PlaySound "fx_nudge", 0, 1, -0.1, 0.25:MongerShake2
    If keycode = RightTiltKey Then Nudge 270, 5:PlaySound "fx_nudge", 0, 1, 0.1, 0.25:MongerShake2
    If keycode = CenterTiltKey Then Nudge 0, 6:PlaySound "fx_nudge", 0, 1, 0, 0.25:MongerShake2
    If keycode = LeftMagnaSave Then bLutActive = True
    If keycode = RightMagnaSave Then 
		If bLutActive Then NextLUT: End If
	End If
    If vpmKeyDown(Keycode) Then Exit Sub
    If keycode = PlungerKey Then PlaySound "fx_PlungerPull", 0, 1, 0.1, 0.25:Plunger.Pullback
End Sub

Sub Table1_KeyUp(ByVal Keycode)
    If keycode = LeftMagnaSave Then bLutActive = False
    If vpmKeyUp(Keycode) Then Exit Sub
    If keycode = PlungerKey Then PlaySound "fx_plunger", 0, 1, 0.1, 0.25:Plunger.Fire
End Sub

'*********
'   LUT
'*********

Dim bLutActive, LUTImage

Sub LoadLUT
	bLutActive = False
    x = LoadValue(cGameName, "LUTImage")
    If(x <> "") Then LUTImage = x Else LUTImage = 0
	UpdateLUT
End Sub

Sub SaveLUT
    SaveValue cGameName, "LUTImage", LUTImage
End Sub

Sub NextLUT: LUTImage = (LUTImage +1 ) MOD 9: UpdateLUT: SaveLUT: End Sub

Sub UpdateLUT
Select Case LutImage
Case 0: table1.ColorGradeImage = "LUT0"
Case 1: table1.ColorGradeImage = "LUT1"
Case 2: table1.ColorGradeImage = "LUT2"
Case 3: table1.ColorGradeImage = "LUT3"
Case 4: table1.ColorGradeImage = "LUT4"
Case 5: table1.ColorGradeImage = "LUT5"
Case 6: table1.ColorGradeImage = "LUT6"
Case 7: table1.ColorGradeImage = "LUT7"
Case 8: table1.ColorGradeImage = "LUT8"
End Select
End Sub

'Solenoids
SolCallback(1) = "solTrough"
SolCallback(2) = "solAutofire"
' SolCallback(3) Monger Magnet
' SolCallback(4) Whiplash Magnet
SolCallback(5) = "WMKick"
SolCallback(6) = "OrbitPost"
'SolCallback(7) = "Gate3.open ="
'SolCallback(8) = "Gate6.open ="

SolCallback(12) = "ClanePost"

SolCallback(15) = "SolLFlipper"
SolCallback(16) = "SolRFlipper"

SolCallback(19) = "SolMonger"

'Flashers
SolCallback(20) = "SetLamp 120,"
SolCallback(21) = "SetLamp 121,"
SolCallback(22) = "SetLamp 122,"
SolCallback(23) = "SetLamp 123,"
SolCallback(25) = "SetLamp 125,"
SolCallback(26) = "SetLamp 126,"
SolCallback(27) = "SetLamp 127,"
SolCallback(28) = "SetLamp 128,"
SolCallback(29) = "SetLamp 129,"
SolCallback(30) = "SetLamp 130,"
SolCallback(31) = "SetLamp 131,"
SolCallback(32) = "SetLamp 132,"

'************************
' Shake Whiplash when hit
'************************

Dim WhiplashPos

Sub ShakeWhiplash
    WhiplashPos = 12
    WhiplashShakeTimer.Enabled = 1
End Sub

Sub WhiplashShakeTimer_Timer
    Whiplash.TransX = WhiplashPos
    If WhiplashPos = 0 Then WhiplashShakeTimer.Enabled = 0:Exit Sub
    If WhiplashPos < 0 Then
        WhiplashPos = ABS(WhiplashPos) - 1
    Else
        WhiplashPos = - WhiplashPos + 1
    End If
End Sub

'****************
' Shake IronMan
'****************

Dim IronManPos

Sub ShakeIronMan
    IronManPos = 12
    IronManShakeTimer.Enabled = 1
End Sub

Sub IronManShakeTimer_Timer
    IronMan.TransX = IronManPos
    If IronManPos = 0 Then IronManShakeTimer.Enabled = 0:Exit Sub
    If IronManPos < 0 Then
        IronManPos = ABS(IronManPos) - 1
    Else
        IronManPos = - IronManPos + 1
    End If
End Sub

Sub iManShakeTrigger_Hit: ShakeIronMan: End Sub

'******************
'Solenoid Functions
'******************

Sub solTrough(Enabled)
    If Enabled Then
        bsTrough.ExitSol_On
        vpmTimer.PulseSw 22
    End If
End Sub

Sub solAutofire(Enabled)
    If Enabled Then
        PlungerIM.AutoFire
    End If
End Sub

Sub ClanePost(Enabled)
    If Enabled Then
        ClaneUpPost.Isdropped = false
    Else
        ClaneUpPost.Isdropped = true
    End If
End Sub

Sub OrbitPost(Enabled)
	If Enabled Then
		UpPost.Isdropped=false
	Else
		UpPost.Isdropped=true
	End If
 End Sub

Sub WMKick(enabled)
    If enabled Then
        PlaySoundAt "ballhit", sw10
        sw10.Kick 180, 30
        controller.switch(10) = false
    End If
End Sub

'Drains
Sub drain_Hit():PlaysoundAt "fx_drain", Drain:bsTrough.AddBall Me:End Sub

' Slings
Dim LStep, RStep

Sub LeftSlingShot_Slingshot
    PlaySoundAt SoundFX("fx_slingshot", DOFContactors), Lemk
    LeftSling4.Visible = 1
    Lemk.RotX = 26
    LStep = 0
    vpmTimer.PulseSw 26
    LeftSlingShot.TimerEnabled = 1
'ShakeLeftSpider
End Sub

Sub LeftSlingShot_Timer
    Select Case LStep
        Case 1:LeftSLing4.Visible = 0:LeftSLing3.Visible = 1:Lemk.RotX = 14
        Case 2:LeftSLing3.Visible = 0:LeftSLing2.Visible = 1:Lemk.RotX = 2
        Case 3:LeftSLing2.Visible = 0:Lemk.RotX = -10:LeftSlingShot.TimerEnabled = 0
    End Select
    LStep = LStep + 1
End Sub

Sub RightSlingShot_Slingshot
    PlaySoundAt SoundFX("fx_slingshot", DOFContactors), Remk
    RightSling4.Visible = 1
    Remk.RotX = 26
    RStep = 0
    vpmTimer.PulseSw 27
    RightSlingShot.TimerEnabled = 1
'ShakeRightSpider
End Sub

Sub RightSlingShot_Timer
    Select Case RStep
        Case 1:RightSLing4.Visible = 0:RightSLing3.Visible = 1:Remk.RotX = 14
        Case 2:RightSLing3.Visible = 0:RightSLing2.Visible = 1:Remk.RotX = 2
        Case 3:RightSLing2.Visible = 0:Remk.RotX = -10:RightSlingShot.TimerEnabled = 0
    End Select
    RStep = RStep + 1
End Sub

'Bumpers
Sub Bumper1_Hit:vpmTimer.PulseSw 30:PlaySoundAt SoundFX("fx_bumper", DOFContactors), Bumper1:End Sub
Sub Bumper2_Hit:vpmTimer.PulseSw 31:PlaySoundAt SoundFX("fx_bumper", DOFContactors), Bumper2:End Sub
Sub Bumper3_Hit:vpmTimer.PulseSw 32:PlaySoundAt SoundFX("fx_bumper", DOFContactors), Bumper3:End Sub

'Lower Lanes
Sub sw24_Hit:Controller.Switch(24) = 1:PlaySoundAt "fx_sensor", sw24:End Sub
Sub sw24_UnHit:Controller.Switch(24) = 0:End Sub
Sub sw25_Hit:Controller.Switch(25) = 1:PlaySoundAt "fx_sensor", sw25:End Sub
Sub sw25_UnHit:Controller.Switch(25) = 0:End Sub
Sub sw28_Hit:Controller.Switch(28) = 1:PlaySoundAt "fx_sensor", sw28:End Sub
Sub sw28_UnHit:Controller.Switch(28) = 0:End Sub
Sub sw29_Hit:Controller.Switch(29) = 1:PlaySoundAt "fx_sensor", sw29:End Sub
Sub sw29_UnHit:Controller.Switch(29) = 0:End Sub

'Upper Lanes
Sub sw7_Hit:Controller.Switch(7) = 1:PlaySoundAt "fx_sensor", sw7:End Sub
Sub sw7_UnHit:Controller.Switch(7) = 0:End Sub
Sub sw9_Hit:Controller.Switch(9) = 1:PlaySoundAt "fx_sensor", sw9:End Sub
Sub sw9_UnHit:Controller.Switch(9) = 0:End Sub
Sub sw38_Hit:Controller.Switch(38) = 1:PlaySoundAt "fx_sensor", sw38:End Sub
Sub sw38_UnHit:Controller.Switch(38) = 0:End Sub
Sub sw39_Hit:Controller.Switch(39) = 1:PlaySoundAt "fx_sensor", sw39:End Sub
Sub sw39_UnHit:Controller.Switch(39) = 0:End Sub

'Ramp switches
Sub sw12_Hit:Controller.Switch(12) = 1:PlaySoundAt "fx_sensor", sw12:End Sub
Sub sw12_UnHit:Controller.Switch(12) = 0:End Sub
Sub sw37_Hit:Controller.Switch(37) = 1:End Sub
Sub sw37_UnHit:Controller.Switch(37) = 0:End Sub
Sub sw43_Hit:Controller.Switch(43) = 1:PlaySoundAt "fx_sensor", sw43:End Sub
Sub sw43_UnHit:Controller.Switch(43) = 0:End Sub
Sub sw49_Hit:Controller.Switch(49) = 1:PlaySoundAt "fx_sensor", sw49:End Sub
Sub sw49_UnHit:Controller.Switch(49) = 0:End Sub

'Spinners
Sub sw11_Spin:vpmTimer.PulseSw 11:PlaySoundAt "fx_spinner", sw11:End Sub
Sub sw13_Spin:vpmTimer.PulseSw 13:PlaySoundAt "fx_spinner", sw13:End Sub
Sub sw14_Spin:vpmTimer.PulseSw 14:PlaySoundAt "fx_spinner", sw14:End Sub

'Targets
Sub sw33_Hit:vpmTimer.PulseSw 33:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw34_Hit:vpmTimer.PulseSw 34:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw35_Hit:vpmTimer.PulseSw 35:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw36_Hit:vpmTimer.PulseSw 36:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw40_Hit:vpmTimer.PulseSw 40:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw41_Hit:vpmTimer.PulseSw 41:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw42_Hit:vpmTimer.PulseSw 42:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw44_Hit:vpmTimer.PulseSw 44:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw45_Hit:vpmTimer.PulseSw 45:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw46_Hit:vpmTimer.PulseSw 46:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub
Sub sw47_Hit:vpmTimer.PulseSw 47:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):ShakeWhiplash:End Sub
Sub sw48_Hit:vpmTimer.PulseSw 48:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):ShakeWhiplash:End Sub
Sub sw50_Hit:vpmTimer.PulseSw 50:PlaySoundAtBall SoundFX("fx_target", DOFDropTargets):End Sub

'kickers
Sub sw10_Hit():controller.switch(10) = true:PlaySoundAt "fx_kicker_enter",sw10:End Sub

'Monger
Sub sw4_Hit:vpmTimer.PulseSw 4:PlaySoundAtBall "fx_target":MongerShake:End Sub
Sub sw5_Hit:vpmTimer.PulseSw 5:PlaySoundAtBall "fx_target":MongerShake:End Sub
Sub sw6_Hit:vpmTimer.PulseSw 6:PlaySoundAtBall "fx_target":MongerShake:End Sub

'*******************
' Flipper Subs v3.0
'*******************

Sub SolLFlipper(Enabled)
    If Enabled Then
        PlaySoundAt SoundFX("fx_flipperup", DOFFlippers), LeftFlipper
        LeftFlipper.EOSTorque = 0.75:LeftFlipper.RotateToEnd
    Else
        PlaySoundAt SoundFX("fx_flipperdown", DOFFlippers), LeftFlipper
        LeftFlipper.EOSTorque = 0.1:LeftFlipper.RotateToStart
    End If
End Sub

Sub SolRFlipper(Enabled)
    If Enabled Then
        PlaySoundAt SoundFX("fx_flipperup", DOFFlippers), RightFlipper
        RightFlipper.EOSTorque = 0.75:RightFlipper.RotateToEnd
    Else
        PlaySoundAt SoundFX("fx_flipperdown", DOFFlippers), RightFlipper
        RightFlipper.EOSTorque = 0.1:RightFlipper.RotateToStart
    End If
End Sub

Sub LeftFlipper_Collide(parm)
    PlaySound "fx_rubber_flipper", 0, parm / 10, pan(ActiveBall), 0, Pitch(ActiveBall), 0, 0, AudioFade(ActiveBall)
End Sub

Sub RightFlipper_Collide(parm)
    PlaySound "fx_rubber_flipper", 0, parm / 10, pan(ActiveBall), 0, Pitch(ActiveBall), 0, 0, AudioFade(ActiveBall)
End Sub

'**********************************************************
'     JP's Flasher Fading for VPX and Vpinmame v3.0
'       (Based on Pacdude's Fading Light System)
' This is a fast fading for the Flashers in vpinmame tables
'  just 4 steps, like in Pacdude's original script.
' Included the new Modulated flashers & Lights for WPC
'**********************************************************

Dim LampState(600), FadingState(600), FlashLevel(600)

InitLamps() ' turn off the lights and flashers and reset them to the default parameters

' vpinmame Lamp & Flasher Timers

Sub LampTimer_Timer()
    Dim chgLamp, num, chg, ii
    chgLamp = Controller.ChangedLamps
    If Not IsEmpty(chgLamp)Then
        For ii = 0 To UBound(chgLamp)
            LampState(chgLamp(ii, 0)) = chgLamp(ii, 1)       'keep the real state in an array
            FadingState(chgLamp(ii, 0)) = chgLamp(ii, 1) + 3 'fading step
            If chgLamp(ii, 0) = 105 Then GiUpdate 0, chgLamp(ii, 1)
        Next
    End If
    UpdateLamps
End Sub

Sub UpdateLamps()
    Lamp 3, l3
    Lamp 4, l4
    Lamp 5, l5
    Lamp 6, l6
    Lamp 7, l7
    Lamp 8, l8
    Lamp 9, l9
    Lamp 10, l10
    Lamp 11, l11
    Lamp 12, l12
    Lamp 13, l13
    Lamp 14, l14
    Lamp 15, l15
    Lamp 16, l16
    Lamp 17, l17
    Lamp 18, l18
    Lamp 19, l19
    Lamp 20, l20
    Lamp 21, l21
    Lamp 22, l22
    Lamp 23, l23
    Lamp 24, l24
    Lamp 25, l25
    Lamp 26, l26
    Lamp 27, l27
    Lamp 28, l28
    Lamp 29, l29
    Lamp 30, l30
    Lamp 31, l31
    Lamp 32, l32
    Lamp 33, l33
    Lamp 34, l34
    Lamp 35, l35
    Lamp 36, l36
    Lamp 37, l37
    Lamp 38, l38
    Lamp 39, l39
    Lamp 40, l40
    Lamp 41, l41
    Lamp 42, l42
    Lamp 43, l43
    Lampm 44, l44a
    Lamp 44, l44
    Lampm 45, l45a
    Lamp 45, l45
    Lampm 46, l46a
    Lamp 46, l46
    Lampm 47, l47a
    Lamp 47, l47
    Lampm 48, l48a
    Lamp 48, l48
    Lamp 49, l49
    Lamp 50, l50
    Lamp 51, l51
    Lamp 52, l52
    Lamp 53, l53
    Lamp 54, l54
    Lamp 55, l55
    Lamp 56, l56
    Lamp 57, l57
    Lamp 58, l58
    Lamp 59, l59
    Lampm 60, Bumper1L
	Flash 60, Flasher1
    Lampm 61, Bumper2L
	Flash 61, Flasher2
    Lampm 62, Bumper3L
	Flash 62, Flasher3
    Lamp 63, l63

'Flashers
Lamp 120, f20
Flashm 121, f21a
Flash 121, f21
Lamp 122, f22
Flashm 125, f25b
Flash 125, f25
Flashm 126, f26a
Flash 126, f26
Lampm 127, f27a
Lampm 127, f27b
Lamp 127, f27c
Flash 123, f23
If MongerPos = 198 Then
	Flash 128, f28
Else
	f28.IntensityScale = 0
End If
Lampm 129, f29a
Lamp 129, f29b
Flash 130, f30
Flashm 131, f31a
Flashm 131, f31b
Flashm 131, f31c
Flashm 131, f31d
Flashm 131, f31e
Flash 131, f31
Flashm 132, f32a
Flashm 132, f32b
Flash 132, f32

End Sub

' div lamp subs

' Normal Lamp & Flasher subs

Sub InitLamps()
    Dim x
    LampTimer.Interval = 40 ' flasher fading speed
    LampTimer.Enabled = 1
    For x = 0 to 600
        LampState(x) = 0
        FadingState(x) = 3 ' used to track the fading state
        FlashLevel(x) = 0
    Next
End Sub

Sub SetRGBLamp(MyLight, R, G, B)
    If TypeName(MyLight) = "Light" Then
        MyLight.Color = RGB(R / 10, G / 10, B / 10)
        MyLight.ColorFull = RGB(R, G, B)
        MyLight.State = 1
    ElseIf TypeName(MyLight) = "Flasher" Then
        MyLight.Color = RGB(R, G, B)
    End If
End Sub

Sub SetLamp(nr, value) ' 0 is off, 1 is on
    FadingState(nr) = abs(value) + 3
End Sub

' Lights: used for VPX standard lights, the fading is handled by VPX itself, they are here to be able to make them work together with the flashers

Sub Lamp(nr, object)
    Select Case FadingState(nr)
        Case 4:object.state = 1:FadingState(nr) = 0
        Case 3:object.state = 0:FadingState(nr) = 0
    End Select
End Sub

Sub Lampm(nr, object) ' used for multiple lights, it doesn't change the fading state
    Select Case FadingState(nr)
        Case 4:object.state = 1
        Case 3:object.state = 0
    End Select
End Sub

' Flashers: 4 is on,3,2,1 fade steps. 0 is off

Sub Flash(nr, object)
    Select Case FadingState(nr)
        Case 4:Object.IntensityScale = 1:FadingState(nr) = 0
        Case 3:Object.IntensityScale = 0.66:FadingState(nr) = 2
        Case 2:Object.IntensityScale = 0.33:FadingState(nr) = 1
        Case 1:Object.IntensityScale = 0:FadingState(nr) = 0
    End Select
End Sub

Sub Flashm(nr, object) 'multiple flashers, it doesn't change the fading state
    Select Case FadingState(nr)
        Case 4:Object.IntensityScale = 1
        Case 3:Object.IntensityScale = 0.66
        Case 2:Object.IntensityScale = 0.33
        Case 1:Object.IntensityScale = 0
    End Select
End Sub

' Desktop Objects: Reels & texts (you may also use lights on the desktop)

' Reels

Sub Reel(nr, object)
    Select Case FadingState(nr)
        Case 4:object.SetValue 1:FadingState(nr) = 0
        Case 3:object.SetValue 2:FadingState(nr) = 2
        Case 2:object.SetValue 3:FadingState(nr) = 1
        Case 1:object.SetValue 0:FadingState(nr) = 0
    End Select
End Sub

Sub Reelm(nr, object)
    Select Case FadingState(nr)
        Case 4:object.SetValue 1
        Case 3:object.SetValue 2
        Case 2:object.SetValue 3
        Case 1:object.SetValue 0
    End Select
End Sub

'Texts

Sub Text(nr, object, message)
    Select Case FadingState(nr)
        Case 4:object.Text = message:FadingState(nr) = 0
        Case 3:object.Text = "":FadingState(nr) = 0
    End Select
End Sub

Sub Textm(nr, object, message)
    Select Case FadingState(nr)
        Case 4:object.Text = message
        Case 3:object.Text = ""
    End Select
End Sub

' Modulated Subs for the WPC tables

Sub SetModLamp(nr, level)
    FlashLevel(nr) = level / 150 'lights & flashers
End Sub

Sub LampMod(nr, object)          ' modulated lights used as flashers
    Object.IntensityScale = FlashLevel(nr)
    Object.State = 1             'in case it was off
End Sub

Sub FlashMod(nr, object)         'sets the flashlevel from the SolModCallback
    Object.IntensityScale = FlashLevel(nr)
End Sub

'Walls and mostly Primitives used as 4 step fading lights
'a,b,c,d are the images used from on to off

Sub FadeObj(nr, object, a, b, c, d)
    Select Case FadingState(nr)
        Case 4:object.image = a:FadingState(nr) = 0 'fading to off...
        Case 3:object.image = b:FadingState(nr) = 2
        Case 2:object.image = c:FadingState(nr) = 1
        Case 1:object.image = d:FadingState(nr) = 0
    End Select
End Sub

Sub FadeObjm(nr, object, a, b, c, d)
    Select Case FadingState(nr)
        Case 4:object.image = a
        Case 3:object.image = b
        Case 2:object.image = c
        Case 1:object.image = d
    End Select
End Sub

Sub NFadeObj(nr, object, a, b)
    Select Case FadingState(nr)
        Case 4:object.image = a:FadingState(nr) = 0 'off
        Case 3:object.image = b:FadingState(nr) = 0 'on
    End Select
End Sub

Sub NFadeObjm(nr, object, a, b)
    Select Case FadingState(nr)
        Case 4:object.image = a
        Case 3:object.image = b
    End Select
End Sub

'************************************
' Diverse Collection Hit Sounds v3.0
'************************************

Sub aMetals_Hit(idx):PlaySoundAtBall "fx_MetalHit":End Sub
Sub aMetalWires_Hit(idx):PlaySoundAtBall "fx_MetalWire":End Sub
Sub aRubber_Bands_Hit(idx):PlaySoundAtBall "fx_rubber_band":End Sub
Sub aRubber_LongBands_Hit(idx):PlaySoundAtBall "fx_rubber_longband":End Sub
Sub aRubber_Posts_Hit(idx):PlaySoundAtBall "fx_rubber_post":End Sub
Sub aRubber_Pins_Hit(idx):PlaySoundAtBall "fx_rubber_pin":End Sub
Sub aRubber_Pegs_Hit(idx):PlaySoundAtBall "fx_rubber_peg":End Sub
Sub aPlastics_Hit(idx):PlaySoundAtBall "fx_PlasticHit":End Sub
Sub aGates_Hit(idx):PlaySoundAtBall "fx_Gate":End Sub
Sub aWoods_Hit(idx):PlaySoundAtBall "fx_Woodhit":End Sub

'***************************************************************
'             Supporting Ball & Sound Functions v3.0
'  includes random pitch in PlaySoundAt and PlaySoundAtBall
'***************************************************************

Dim TableWidth, TableHeight

TableWidth = Table1.width
TableHeight = Table1.height

Function Vol(ball) ' Calculates the Volume of the sound based on the ball speed
    Vol = Csng(BallVel(ball) ^2 / 2000)
End Function

Function Pan(ball) ' Calculates the pan for a ball based on the X position on the table. "table1" is the name of the table
    Dim tmp
    tmp = ball.x * 2 / TableWidth-1
    If tmp> 0 Then
        Pan = Csng(tmp ^10)
    Else
        Pan = Csng(-((- tmp) ^10))
    End If
End Function

Function Pitch(ball) ' Calculates the pitch of the sound based on the ball speed
    Pitch = BallVel(ball) * 20
End Function

Function BallVel(ball) 'Calculates the ball speed
    BallVel = (SQR((ball.VelX ^2) + (ball.VelY ^2)))
End Function

Function AudioFade(ball) 'only on VPX 10.4 and newer
    Dim tmp
    tmp = ball.y * 2 / TableHeight-1
    If tmp> 0 Then
        AudioFade = Csng(tmp ^10)
    Else
        AudioFade = Csng(-((- tmp) ^10))
    End If
End Function

Sub PlaySoundAt(soundname, tableobj) 'play sound at X and Y position of an object, mostly bumpers, flippers and other fast objects
    PlaySound soundname, 0, 1, Pan(tableobj), 0.1, 0, 0, 0, AudioFade(tableobj)
End Sub

Sub PlaySoundAtBall(soundname) ' play a sound at the ball position, like rubbers, targets, metals, plastics
    PlaySound soundname, 0, Vol(ActiveBall), pan(ActiveBall), 0.4, 0, 0, 0, AudioFade(ActiveBall)
End Sub

'***********************************************
'   JP's VP10 Rolling Sounds + Ballshadow v3.0
'   uses a collection of shadows, aBallShadow
'***********************************************

Const tnob = 19   'total number of balls, 20 balls, from 0 to 19
Const lob = 0     'number of locked balls
Const maxvel = 42 'max ball velocity
ReDim rolling(tnob)
InitRolling

Sub InitRolling
    Dim i
    For i = 0 to tnob
        rolling(i) = False
    Next
End Sub

Sub RollingUpdate()
    Dim BOT, b, ballpitch, ballvol, speedfactorx, speedfactory
    BOT = GetBalls

    ' stop the sound of deleted balls and hide the shadow
    For b = UBound(BOT) + 1 to tnob
        rolling(b) = False
        StopSound("fx_ballrolling" & b)
        aBallShadow(b).Y = 3000
    Next

    ' exit the sub if no balls on the table
    If UBound(BOT) = lob - 1 Then Exit Sub 'there no extra balls on this table

    ' play the rolling sound for each ball and draw the shadow
    For b = lob to UBound(BOT)
        aBallShadow(b).X = BOT(b).X
        aBallShadow(b).Y = BOT(b).Y

        If BallVel(BOT(b))> 1 Then
            If BOT(b).z <30 Then
                ballpitch = Pitch(BOT(b))
                ballvol = Vol(BOT(b))
            Else
                ballpitch = Pitch(BOT(b)) + 25000 'increase the pitch on a ramp
                ballvol = Vol(BOT(b)) * 10
            End If
            rolling(b) = True
            PlaySound("fx_ballrolling" & b), -1, ballvol, Pan(BOT(b)), 0, ballpitch, 1, 0, AudioFade(BOT(b))
        Else
            If rolling(b) = True Then
                StopSound("fx_ballrolling" & b)
                rolling(b) = False
            End If
        End If

        ' rothbauerw's Dropping Sounds
        If BOT(b).VelZ <-1 and BOT(b).z <55 and BOT(b).z> 27 Then 'height adjust for ball drop sounds
            PlaySound "fx_balldrop", 0, ABS(BOT(b).velz) / 17, Pan(BOT(b)), 0, Pitch(BOT(b)), 1, 0, AudioFade(BOT(b))
        End If

        ' jps ball speed control
        If BOT(b).VelX AND BOT(b).VelY <> 0 Then
            speedfactorx = ABS(maxvel / BOT(b).VelX)
            speedfactory = ABS(maxvel / BOT(b).VelY)
            If speedfactorx <1 Then
                BOT(b).VelX = BOT(b).VelX * speedfactorx
                BOT(b).VelY = BOT(b).VelY * speedfactorx
            End If
            If speedfactory <1 Then
                BOT(b).VelX = BOT(b).VelX * speedfactory
                BOT(b).VelY = BOT(b).VelY * speedfactory
            End If
        End If
    Next
End Sub

'**********************
' Ball Collision Sound
'**********************

Sub OnBallBallCollision(ball1, ball2, velocity)
    PlaySound("fx_collide"), 0, Csng(velocity) ^2 / 2000, Pan(ball1), 0, Pitch(ball1), 0, 0, AudioFade(ball1)
End Sub
'******************
' RealTime Updates
'******************

Sub RealTime_Timer
    RollingUpdate
    LeftflipperTop.Rotz = LeftFlipper.CurrentAngle
    RightflipperTop.Rotz = RightFlipper.CurrentAngle
End Sub

'*************************
' GI - needs vpinmame 3
'*************************

Set GICallback = GetRef("GIUpdate")

Sub GIUpdate(no, Enabled)
    For each x in aGiLights
        x.State = ABS(Enabled)
    Next
End Sub

'******************
' Monger Animation
'******************

Dim MongerPos, MongerDir

' start with monger dropped.
MongerDir = -2:MongerPos = 0
Controller.Switch(1) = 0
Controller.Switch(3) = 1

Sub Solmonger(Enabled)
    If Enabled Then
        If MongerDir = 2 Then
            DropMonger
        Else
            RiseMonger
        End If
    End If
End Sub

Sub RiseMonger()
    PlaySound "fx_motor"
    MongerDir = 2
    Controller.Switch(1) = 0
    MongerTimer.Enabled = 1
End Sub

Sub DropMonger()
    PlaySound "fx_motor"
    MongerDir = -2
    Controller.Switch(3) = 0
    MongerTimer.Enabled = 1
End Sub

Sub MongerTimer_Timer
    MongerPos = MongerPos + MongerDir
    If MongerPos > 198 Then
        MongerPos = 198
        Me.Enabled = 0
        Controller.Switch(3) = 1
    Else
        If MongerPos < 0 Then
            MongerPos = 0
            Me.Enabled = 0
            Controller.Switch(1) = 1
        End If
    End If
    UpdateMonger
End Sub

Sub UpdateMonger
    MongerFrameP.TransZ = MongerPos
    MongerCage.TransZ = MongerPos
    Monger.TransZ = MongerPos
    If MongerPos > 140 Then
        sw4.IsDropped = 0
        sw5.IsDropped = 0
        sw6.IsDropped = 0
        mongerframe.IsDropped = 0
    End If
    If MongerPos < 20 Then
        sw4.IsDropped = 1
        sw5.IsDropped = 1
        sw6.IsDropped = 1
        mongerframe.IsDropped = 1
    End If
End Sub

'********************************************
' Monger Shake animations when hit or nudging
'********************************************

'captive ball for hit animations

Dim ccBall
Const cMod = .65 'percentage of hit power transfered to the 3 Bank of targets

InitCaptiveBall

Sub InitCaptiveBall
    Set ccBall = hball.CreateSizedBallWithMass(25, 1.6)
    hball.Kick 0, 0
End Sub

Sub MongerShake
    ccball.velx = activeball.velx * cMod
    ccball.vely = activeball.vely * cMod
    CaptiveTimer.enabled = True
    CaptiveTimer2.enabled = True
End Sub

Sub MongerShake2 'when nudging
    CaptiveTimer.enabled = True
    CaptiveTimer2.enabled = True
End Sub

Sub CaptiveTimer_Timer           'start animation
    Dim x, y
    x = (hball.x - ccball.x) / 4 'reduce the X axis movement
    y = (hball.y - ccball.y) / 2
    MongerFrameP.transy = x
    MongerFrameP.transx = - y
    MongerCage.transy = x
    MongerCage.transx = - y
    Monger.transy = x
    Monger.transx = - y
End Sub

Sub CaptiveTimer2_Timer 'stop animation
    MongerFrameP.transy = 0
    MongerFrameP.transx = 0
    MongerCage.transy = 0
    MongerCage.transx = 0
    Monger.transy = 0
    Monger.transx = 0
    CaptiveTimer.enabled = False
    CaptiveTimer2.enabled = False
End Sub