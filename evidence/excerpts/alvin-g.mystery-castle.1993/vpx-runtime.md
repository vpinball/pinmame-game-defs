# Retained v2.1.0 runtime bindings

AgentEighty6, March2020. Complete selected initialization,callback and event-handler regions. Whitespace-only normalization expands tabs to four spaces and removes trailing whitespace; code, comments and source line ranges are preserved. Whole-line commented callbacks remain comments. vpmMapLights reads TimerInterval and collection membership; names alone do not bind lamps.

## script.vbs:98-119

```vb
'Const cGameName = "mystcast"
Const SSolenoidOn="Solenoid",SSolenoidOff="SolenoidOff", SCoin="coin_in"
Const UseSolenoids  = 1
Const UseLamps      = 1
Const UseSync       = 1
Const HandleMech    = 0
Const UseGI         = 0


'*************************************************

LoadVPM "02904245","alvinG.VBS",3.10

Dim bsTrough, DTRBank1, DTRBank2, bsKickerMegaMode
Dim DesktopMode : DesktopMode = MC.ShowDT

Sub MC_Init
    vpmInit me
    With Controller
       .GameName=cGameName
       If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description : Exit Sub
       .SplashInfoLine="Mystery Castle, Alvin G 1993"
```

## script.vbs:137-176

```vb
   'Trough
    Set bsTrough=New cvpmBallStack
        with bsTrough
            '.InitSw 0,18,0,0,0,0,0,0
            .InitSw 17, 18, 0, 0, 0, 0, 0, 0
            .InitKick BallRelease,90,5
            .InitExitSnd Soundfx("BallRelease",DOFContactors), Soundfx("Solenoid",DOFContactors)
            .Balls=2
        End With

    'Kickers
    Set bsKickerMegaMode= New cvpmBallStack
    With bsKickerMegaMode
        .InitSw 0, 24, 0, 0, 0, 0, 0, 0
        .InitKick sw24, 170 , 18
        .InitExitSnd Soundfx("scoopexit",DOFContactors), Soundfx("solenoid",DOFContactors)
    End With

    'DropTargets
    set DTRBank1 = new cvpmDropTarget
        with DTRBank1
             .InitDrop Array(sw33,sw34,sw35), Array(33,34,35)
             .InitSnd  Soundfx("droptarget",DOFDropTargets), Soundfx("droptargetreset",DOFContactors)
    End With

    set DTRBank2 = new cvpmDropTarget
        with DTRBank2
             .InitDrop Array(sw36,sw37,sw38), Array(36,37,38)
             .InitSnd  Soundfx("droptarget",DOFDropTargets), Soundfx("droptargetreset",DOFContactors)
    End With

    AutoPlunger.PullBack
    CatapultPlunger.PullBack
    SecretDoorPlunger.PullBack

    DisplayTimer.Enabled = DesktopMode

    RampLT.visible = DesktopMode
    RampRT.visible = DesktopMode

```

## script.vbs:198-215

```vb

    vpmMapLights AllLights

    dim xx
    For each xx in LowerGILights
        xx.intensity = xx.intensity * DynamicGIIntensity
    Next
    dim yy
    For each yy in UpperGILights
        yy.intensity = yy.intensity * DynamicGIIntensity
    Next
    dim zz
    For each zz in AllLights
        zz.intensity = zz.intensity * DynamicLampIntensity
    Next

    Init_Flashers

```

## script.vbs:221-275

```vb
'***********************************************************************************
Sub MC_KeyDown(ByVal keycode)
    If keycode = PlungerKey Then Controller.Switch(14) = True
    If keycode = LeftFlipperKey Then lfpress = 1
    If keycode = RightFlipperKey Then rfpress = 1
    If vpmKeyDown(keycode) Then Exit Sub
End Sub

Sub MC_KeyUp(ByVal keycode)
    If keycode = PlungerKey Then
       Controller.Switch(14) = False
       PlaySound Soundfx("plunger",DOFContactors)
    End If
    If keycode = LeftFlipperKey Then
        lfpress = 0
        leftflipper.eostorqueangle = EOSA
        leftflipper.eostorque = EOST
    End If
    If keycode = RightFlipperKey Then
        rfpress = 0
        rightflipper.eostorqueangle = EOSA
        rightflipper.eostorque = EOST
    End If
    If vpmKeyUp(keycode) Then Exit Sub
End Sub


'*******************************
'Solenoids
'*******************************
SolCallback(1) = "vpmSolAutoPlungeS SecretDoorPlunger, SoundFX(""fx_vuk_exit"", DOFContactors), 3,"
'SolCallback(2) = "vpmSolSound SoundFX(""fx_bumper1"",DOFContactors),"          'Bumper 1
'SolCallback(3) = "vpmSolSound SoundFX(""fx_bumper2"",DOFContactors),"          'Bumper 2
'SolCallback(4) = "vpmSolSound Soundfx(""slingL"",DOFContactors),"
'SolCallback(5) = "vpmSolSound Soundfx(""slingR"",DOFContactors),"
SolCallback(6) = "solKickerMegaMode"
SolCallback(9) = "vpmSolAutoPlungeS AutoPlunger, SoundFX(""fx_vuk_exit"", DOFContactors), 3,"
SolCallback(10) = "vpmSolAutoPlungeS CatapultPlunger, SoundFX(""fx_vuk_exit"", DOFContactors), 3,"
SolCallback(11) = "DTRBank1.SolDropUp"
SolCallback(12) = "DTRBank2.SolDropUp"
SolCallback(13) = "bsTrough.SolIn"                  'OutHole
SolCallback(14) = "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"

'Flasher Sols
SolCallback(16) = "solF16"                          'Playfield Lower GI Lights Relay
SolCallback(17) = "solF17"                          'Flasher Dungeon
SolCallback(18) = "solF18"                          'Flasher Bridge
SolCallback(19) = "solF19"                          'Flasher Tower
SolCallback(20) = "solF20"                          'Flasher Ballroom
SolCallback(21) = "solF21"                          'Flasher Secret
SolCallback(22) = "solF22"                          'Flasher Catwalk
SolCallback(23) = "solF23"                          'Flasher Lock
SolCallback(26) = "solF26"                          'Playfield Upper GI Lights Relay
SolCallback(27) = "solGameOn"                       'Flipper Relay
SolCallback(30)  = "bsTrough.SolOut"                'Kick to Playfield
```

## script.vbs:314-355

```vb
Sub solF16(enabled)  'Lower GI lighting
    If enabled Then
        LowerGiOFF
    Else
        LowerGiON
    End If
End Sub
'
Sub solF26(enabled) 'Upper GI lighting
    If enabled Then
        UpperGiOFF
    Else
        UpperGiON
    End If
End Sub

Sub solKickerMegaMode(Enabled)
    If Enabled Then
        PlaySoundAtVol SoundFX("scoopexit",DOFContactors), sw24, 1
        bsKickerMegaMode.ExitSol_On
    End If
End Sub

Sub solGameOn (enabled)
    vpmNudge.SolGameOn Enabled
End Sub

Sub solDiverterx (enabled)
    If enabled Then
        If Flipperdiverter.TimerEnabled = 0 Then PlaySound Soundfx("fx_flipperup",DOFContactors)
        Flipperdiverter.RotateToEnd
        Flipperdiverter.TimerInterval = 600
        Flipperdiverter.TimerEnabled = 1
    End If
End Sub

Sub Flipperdiverter_Timer
    PlaySound Soundfx("fx_flipperdown",DOFContactors)
    Flipperdiverter.RotateToStart
    Flipperdiverter.TimerEnabled = 0
End Sub

```

## script.vbs:360-525

```vb
'Drains and Kickers

Sub Drain_Hit()
    'bsTrough.EntrySol_On
    bsTrough.AddBall Me
    PlaySound Soundfx("drain",DOFContactors)
End Sub

Sub sw21_Hit
    Controller.Switch(21) = true
End Sub
Sub sw21_UnHit
    Controller.Switch(21) = false
End Sub



Sub sw23hole_Hit
    PlaySoundAtVol "scoopenter",sw23, 1
    vpmtimer.pulsesw 23
End Sub
Sub sw23_Hit  'transfer thru subway to sw24
    sw23.destroyBall
    sw24.createBall
    sw24.kick 0,0
End Sub
'
Sub sw24_Hit
    PlaySoundAtVol "scoopenter", sw24, 1
    bsKickerMegaMode.EntrySol_On
    bsKickerMegaMode.addball Me
End Sub


Sub Bumper1_Hit()
   vpmTimer.PulseSw 25 'Left bumper
    PlaySoundAtBumperVol Soundfx("fx_bumper1",DOFContactors),Bumper1,1
End Sub


Sub Bumper2_Hit()
   vpmTimer.PulseSw 26 'Right bumper
    PlaySoundAtBumperVol Soundfx("fx_bumper2",DOFContactors),Bumper2,1
End Sub

Sub sw29_Hit  ' Catwalk Enter
   Controller.Switch(29) = true
End Sub
Sub sw29_UnHit
   Controller.Switch(29) = false
End Sub

Sub sw30_Hit  ' Catwalk Exit
   Controller.Switch(30) = true
End Sub
Sub sw30_UnHit
   Controller.Switch(30) = false
End Sub

Sub sw31_Hit  ' Tower Enter
   Controller.Switch(31) = true
End Sub
Sub sw31_UnHit
   Controller.Switch(31) = false
End Sub

Sub sw32_Hit    ' Tower Exit
   Controller.Switch(32) = true
End Sub
Sub sw32_UnHit
   Controller.Switch(32) = false
End Sub

Sub sw33_Hit:DropTargetHit:DTRBank1.Hit 1:sw33.isDropped=true:End Sub       'Drop Target
Sub sw34_Hit:DropTargetHit:DTRBank1.Hit 2:sw34.isDropped=true:End Sub       'Drop Target
Sub sw35_Hit:DropTargetHit:DTRBank1.Hit 3:sw35.isDropped=true:End sub       'Drop Target
Sub sw36_Hit:DropTargetHit:DTRBank2.Hit 1:sw36.isDropped=true:End Sub       'Drop Target
Sub sw37_Hit:DropTargetHit:DTRBank2.Hit 2:sw37.isDropped=true:End Sub       'Drop Target
Sub sw38_Hit:DropTargetHit:DTRBank2.Hit 3:sw38.isDropped=true:End sub       'Drop Target

Sub sw39_Hit
   Controller.Switch(39) = true
End Sub
Sub sw39_UnHit
   Controller.Switch(39) = false
End Sub

Sub sw41_Hit()
   vpmTimer.PulseSw 41 'T
End Sub

Sub sw42_Hit()
   vpmTimer.PulseSw 42 'R
End Sub

Sub sw43_Hit()
   vpmTimer.PulseSw 43 'A
End Sub

Sub sw44_Hit()
   vpmTimer.PulseSw 44 'P
End Sub

Sub sw45_Hit()
   vpmTimer.PulseSw 45 'Left returnlane
End Sub

Sub sw46_Hit()
   vpmTimer.PulseSw 46 'Left outlane
End Sub

Sub sw47_Hit()
   vpmTimer.PulseSw 47 'Right returnlane
End Sub

Sub sw48_Hit()
   vpmTimer.PulseSw 48 'Right outlane
End Sub

Sub sw49_Hit:vpmTimer.PulseSw(49):PlaySoundAtVol SoundFX("Target",DOFTargets), sw49, VolTarg:End Sub    'Statue top
Sub sw50_Hit:vpmTimer.PulseSw(50):PlaySoundAtVol SoundFX("Target",DOFTargets), sw50, VolTarg:End Sub    'Statue mid
Sub sw51_Hit:vpmTimer.PulseSw(51):PlaySoundAtVol SoundFX("Target",DOFTargets), sw51, VolTarg:End Sub    'Statue bottom

Sub sw52_Hit:vpmTimer.PulseSw(52):PlaySoundAtVol SoundFX("Target",DOFTargets), sw52, VolTarg:End Sub    'Change Item

Sub sw53_Hit 'Dungeon
   Controller.Switch(53) = true
End Sub
Sub sw53_UnHit
   Controller.Switch(53) = false
End Sub

Sub sw54_Hit 'Ballroom
   Controller.Switch(54) = true
End Sub
Sub sw54_UnHit
   Controller.Switch(54) = false
End Sub

Sub sw55_Hit 'Secret Door
   Controller.Switch(55) = true
End Sub
Sub sw55_UnHit
   Controller.Switch(55) = false
End Sub

'
'***********************************************************************************
'****                           Flippers                                        ****
'***********************************************************************************
SolCallback(sLRFlipper)="SolRightFlipper"
SolCallback(sLLFlipper)="SolLeftFlipper"

Sub SolLeftFlipper(Enabled)
    If Enabled Then
        LF.fire
        PlaySoundAtVol SoundFX("fx_flipperup",DOFFlippers), LeftFlipper, 1
        LeftFlipper1.RotateToEnd
    Else
        PlaySoundAtVol SoundFX("fx_flipperdown",DOFFlippers), LeftFlipper, 1
        LeftFlipper.RotateToStart
        LeftFlipper1.RotateToStart
    End If
End Sub

Sub SolRightFlipper(Enabled)
```

## script.vbs:536-558

```vb
'***********************************************************************************
'****                           Slingshot and walls                             ****
'***********************************************************************************
Dim SLLPos, SLRPos

Sub SlingLL_Slingshot()
    LLSling1.Visible = 0:LLSling2.Visible = 0:LLSling3.Visible = 0: LLSling4.Visible = 1: LLSling.TransZ = -27
    vpmTimer.PulseSw(27):PlaySoundAtVol SoundFX("SlingL",DOFContactors), LLSling, 1
    SLLPos = 0: Me.TimerInterval = 13:Me.TimerEnabled = 1:
End Sub

Sub SlingLL_Timer
    Select Case SLLPos
        Case 2: LLSling1.Visible = 0:LLSling2.Visible = 0:LLSling3.Visible = 1: LLSling4.Visible = 0: LLSling.TransZ = -17
        Case 3: LLSling1.Visible = 0:LLSling2.Visible = 1:LLSling3.Visible = 0: LLSling4.Visible = 0: LLSling.TransZ = -8
        Case 4: LLSling1.Visible = 1:LLSling2.Visible = 0:LLSling3.Visible = 0: LLSling4.Visible = 0: LLSling.TransZ = 0 :Me.TimerEnabled = 0
    End Select
    SLLPos = SLLPos + 1
End Sub

Sub SlingLR_Slingshot()
    LRSling1.Visible = 0:LRSling2.Visible = 0:LRSling3.Visible = 0: LRSling4.Visible = 1: LRSling.TransZ = -27
    vpmTimer.PulseSw(28):PlaySoundAtVol SoundFX("SlingR",DOFContactors), LRSling, 1
```

## script.vbs:567-579

```vb
    End Select
    SLRPos = SLRPos + 1
End Sub

Sub Slingshots_Init
    LLSling1.Visible = 1:LLSling2.Visible = 0:LLSling3.Visible = 0: LLSling4.Visible = 0: LLSling.TransZ = 0
    LRSling1.Visible = 1:LRSling2.Visible = 0:LRSling3.Visible = 0: LRSling4.Visible = 0: LRSling.TransZ = 0
End Sub

'***********************************************************************************
'****                           Misc                                            ****
'***********************************************************************************

```

## script.vbs:1388-1524

```vb
Sub Flasher17_Timer() ' with dome
    dim flashx3, matdim
    If not Flasher17.TimerEnabled Then
        Flasher17.TimerEnabled = True
        Flasher17.visible = 1
        Flasher17DomeOn.visible = 1
    End If
    flashx3 = FlashLevel17 * FlashLevel17 * FlashLevel17
    Flasher17.opacity = 1500 * flashx3
    Flasher17DomeOn.BlendDisableLighting = 10 * flashx3
    Flasher17Dome.BlendDisableLighting =  flashx3
    F17a.IntensityScale = flashx3
    F17b.IntensityScale = flashx3
    matdim = Round(10 * FlashLevel17)
    Flasher17DomeOn.material = "domelit" & matdim
    FlashLevel17 = FlashLevel17 * 0.9 - 0.01
    If FlashLevel17 < 0.15 Then
        Flasher17DomeOn.visible = 0
    Else
        Flasher17DomeOn.visible = 1
    end If
    If FlashLevel17 < 0 Then
        Flasher17.TimerEnabled = False
        Flasher17.visible = 0
    End If
End Sub

Sub Flasher18_Timer() ' without dome
    dim flashx3, matdim
    If not Flasher18.TimerEnabled Then
        Flasher18.TimerEnabled = True
    End If
    flashx3 = FlashLevel18 * FlashLevel18 * FlashLevel18
    F18a.IntensityScale = flashx3
    F18b.IntensityScale = flashx3
    FlashLevel18 = FlashLevel18 * 0.9 - 0.01
    If FlashLevel18 < 0 Then
        Flasher18.TimerEnabled = False
    End If
End Sub

Sub Flasher19_Timer() ' without dome
    dim flashx3, matdim
    If not Flasher19.TimerEnabled Then
        Flasher19.TimerEnabled = True
    End If
    flashx3 = FlashLevel19 * FlashLevel19 * FlashLevel19
    F19a.IntensityScale = flashx3
    F19b.IntensityScale = flashx3
    FlashLevel19 = FlashLevel19 * 0.9 - 0.01
    If FlashLevel19 < 0 Then
        Flasher19.TimerEnabled = False
    End If
End Sub

Sub Flasher20_Timer() ' with dome
    dim flashx3, matdim
    If not Flasher20.TimerEnabled Then
        Flasher20.TimerEnabled = True
        Flasher20.visible = 1
        Flasher20DomeOn.visible = 1
    End If
    flashx3 = FlashLevel20 * FlashLevel20 * FlashLevel20
    Flasher20.opacity = 1500 * flashx3
    Flasher20DomeOn.BlendDisableLighting = 10 * flashx3
    Flasher20Dome.BlendDisableLighting =  flashx3
    F20a.IntensityScale = flashx3
    F20b.IntensityScale = flashx3
    matdim = Round(10 * FlashLevel20)
    Flasher20DomeOn.material = "domelit" & matdim
    FlashLevel20 = FlashLevel20 * 0.9 - 0.01
    If FlashLevel20 < 0.15 Then
        Flasher20DomeOn.visible = 0
    Else
        Flasher20DomeOn.visible = 1
    end If
    If FlashLevel20 < 0 Then
        Flasher20.TimerEnabled = False
        Flasher20.visible = 0
    End If
End Sub

Sub Flasher21_Timer() ' with dome
    dim flashx3, matdim
    If not Flasher21.TimerEnabled Then
        Flasher21.TimerEnabled = True
        Flasher21.visible = 1
        Flasher21DomeOn.visible = 1
    End If
    flashx3 = FlashLevel21 * FlashLevel21 * FlashLevel21
    Flasher21.opacity = 1500 * flashx3
    Flasher21DomeOn.BlendDisableLighting = 10 * flashx3
    Flasher21Dome.BlendDisableLighting =  flashx3
    F21a.IntensityScale = flashx3
    F21b.IntensityScale = flashx3
    matdim = Round(10 * FlashLevel21)
    Flasher21DomeOn.material = "domelit" & matdim
    FlashLevel21 = FlashLevel21 * 0.9 - 0.01
    If FlashLevel21 < 0.15 Then
        Flasher21DomeOn.visible = 0
    Else
        Flasher21DomeOn.visible = 1
    end If
    If FlashLevel21 < 0 Then
        Flasher21.TimerEnabled = False
        Flasher21.visible = 0
    End If
End Sub

Sub Flasher22_Timer() ' without dome
    dim flashx3, matdim
    If not Flasher22.TimerEnabled Then
        Flasher22.TimerEnabled = True
    End If
    flashx3 = FlashLevel22 * FlashLevel22 * FlashLevel22
    F22a.IntensityScale = flashx3
    F22b.IntensityScale = flashx3
    FlashLevel22 = FlashLevel22 * 0.9 - 0.01
    If FlashLevel22 < 0 Then
        Flasher22.TimerEnabled = False
    End If
End Sub

Sub Flasher23_Timer() ' without dome
    dim flashx3, matdim
    If not Flasher23.TimerEnabled Then
        Flasher23.TimerEnabled = True
    End If
    flashx3 = FlashLevel23 * FlashLevel23 * FlashLevel23
    F23a.IntensityScale = flashx3
    F23b.IntensityScale = flashx3
    FlashLevel23 = FlashLevel23 * 0.9 - 0.01
    If FlashLevel23 < 0 Then
        Flasher23.TimerEnabled = False
    End If
End Sub

```
