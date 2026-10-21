# Viking retained-script binding excerpts

Retained source SHA256 4ac500af726d5735a41e610630144287748ca384eaaa412b0e835bd0c96e138b. Header: bord v1.0; cGameName=vikingb; Bally.VBS3.21; user-local table. Code below has LF line endings and trailing horizontal whitespace removed; it is a runtime-binding artifact, not independent physical socket evidence. Known omissions include individual target trips, rebound33, and commented shoot-again11. No VPX play session was claimed by this contribution.

## script.vbs lines235-258

```vb
'************************************************
SolCallback(7) =    "bsTrough.SolOut"       'outhole kicker
'SolCallback(2) =   "Solknocker "               'knocker
SolCallback(8) =    "SolKickUpSaucer"       'kick up saucer
SolCallback(9) =    "SolKickDownSaucer"     'kick down saucer
'SolCallback(5) =   ""                  'left slingshot
'SolCallback(6) =   ""                  'right slingshot
SolCallback(1) =    "SolLeftTargetReset "           'in line drop target reset
SolCallback(2) =    "SolRightTargetReset "          '3 drop target reset
'SolCallback(9) =   "vpmSolSound "              'top left thumper bumper
'SolCallback(10) =  "vpmsolsound "              'top right thumper bumper
'SolCallback(11) =  "vpmSolSound "              'left side thumper bumper
'SolCallback(12) =  "vpmSolSound "              'right side thumper bumper
SolCallback(3) =    ""                  '3 drop target 1 (top)
SolCallback(4) =    ""                  '3 drop target 2
SolCallback(5) =    ""                  '3 drop target 3 (bottom)
'SolCallback(16) =  ""                  'coin lockout door
'SolCallback(17) =  ""                  'ki relay (flipper enable)
SolCallback(17) =   "SolTopSaucer"      'top saucer

SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"

Sub Table1_Init
```

## script.vbs lines283-308

```vb
'Trough
    Set bsTrough=New cvpmBallStack
    with bsTrough
        .InitSw 0,8,0,0,0,0,0,0
        .InitKick BallRelease,60,14
        .InitExitSnd Soundfx("fx_ballrel",DOFContactors), Soundfx("fx_solenoid",DOFContactors)
        .Balls=1
    end with

     ' Nudging
     vpmNudge.TiltSwitch = 7
     vpmNudge.Sensitivity = 3
     vpmNudge.TiltObj = Array(leftslingshot, rightslingshot, sw37, sw38, sw39, sw40)

    Set dtLeft=New cvpmDropTarget
        dtLeft.InitDrop Array(sw1,sw2,sw3,sw4),Array(1,2,3,4)
        dtLeft.InitSnd SoundFX("fx2_droptarget",DOFDropTargets),SoundFX("fx2_DTReset",DOFDropTargets)

    Set dtRight=New cvpmDropTarget
        dtRight.InitDrop Array(sw17,sw18,sw19),Array(17,18,19)
        dtRight.InitSnd SoundFX("fx2_droptarget2",DOFDropTargets),SoundFX("fx2_DTReset2",DOFDropTargets)
'
 End Sub

'**********************************************************************************************************
'Plunger code
```

## script.vbs lines389-460

```vb

'
Sub sw24_Hit
	set KickerBall = activeball
	Controller.Switch(24) = 1
End Sub

Sub sw24_unHit
	Controller.Switch(24) = 0
End Sub

dim kickstep1

Sub SolTopSaucer(enabled)
    if enabled then
        PlaySoundAtVol Soundfx("fx_ballrel",DOFContactors), sw24, VolKick
        PlaySoundAtVol Soundfx("fx_solenoid",DOFContactors), sw24, VolKick
		If sw24.ballcntover > 0 then
			KickBall KickerBall, 177, 18, 5, 30
		End If
		cupun2.rotx = -25
		k3step=0
		kicktoptimer.enabled=1
    end if
End Sub

Sub kicktoptimer_Timer
    Select Case K3Step
        Case 3:cupun2.rotx = -25
        Case 4:cupun2.rotx = -25
        Case 5:cupun2.rotx = -25
        Case 6:cupun2.rotx = -25
        Case 7:cupun2.rotx = -25
        Case 8:cupun2.rotx = -18
        Case 9:cupun2.rotx = -11
        Case 10:cupun2.rotx = 5
        Case 11:cupun2.rotx = 0:KickToptimer.Enabled = 0: if sw24.ballcntover > 0 then SolSaucer -1
    End Select
    k3Step = k3Step + 1
End Sub

Sub SolKickUpSaucer(enabled)
    if enabled then
        PlaySoundAtVol Soundfx("fx_ballrel",DOFContactors), sw32, VolKick
        PlaySoundAtVol Soundfx("fx_solenoid",DOFContactors), sw32, VolKick
        Controller.Switch(32) = false
        sw32.Kick  10, 24 + 5 * Rnd
		cupdeux2.rotx = 25
		k1step = 0
		KickUptimer.Enabled = 1
    end if
End Sub

Sub kickuptimer_Timer
    Select Case K1Step
        Case 3:cupdeux2.rotx = 25
        Case 4:cupdeux2.rotx = 25
        Case 5:cupdeux2.rotx = 25
        Case 6:cupdeux2.rotx = 25
        Case 7:cupdeux2.rotx = 25
        Case 8:cupdeux2.rotx = 18
        Case 9:cupdeux2.rotx = 11
        Case 10:cupdeux2.rotx = 5
        Case 11:cupdeux2.rotx = 0:KickUptimer.Enabled = 0
    End Select
    k1Step = k1Step + 1
End Sub

Sub SolKickDownSaucer(enabled)
    if enabled then
        PlaySoundAtVol Soundfx("fx_ballrel",DOFContactors), sw32, VolKick
        PlaySoundAtVol Soundfx("fx_solenoid",DOFContactors), sw32, VolKick
```

## script.vbs lines633-697

```vb
'-------------------------------------
Set Lights(1)  = l1
Set Lights(2)  = l2
Set Lights(3)  = l3
Set Lights(4)  = l4
Set Lights(5)  = l5
Set Lights(6)  = l6
Set Lights(7)  = l7
Set Lights(8)  = l8
Set Lights(9)  = l9
Lights(10) = Array(l10,l10a)
'Set Lights(11) = l11 'Shoot Again
Set Lights(12) = l12
'Set Lights(13) = l13 'Ball In Play
Set Lights(14) = l14
Set Lights(15) = l15
'Set Lights(16) = unused
Set Lights(17) = l17
Set Lights(18) = l18
Set Lights(19) = l19
Set Lights(20) = l20
Set Lights(21) = l21
Set Lights(22) = l22
Set Lights(23) = l23
Set Lights(24) = l24
Set Lights(25) = l25
Set Lights(26) = l26
'Set Lights(27) = l27 'LightMatch
Set Lights(28) = l28
'Set Lights(29) = l29 'LightHighScore
Set Lights(30) = l30
Set Lights(31) = l31
'Set Lights(32) = unused
Set Lights(33) = l33
Set Lights(34) = l34
Set Lights(35) = l35
Set Lights(36) = l36
Set Lights(37) = l37
Set Lights(38) = l38
Set Lights(39) = l39
Set Lights(40) = l40
Set Lights(41) = l41
Set Lights(42) = l42
Set Lights(43) = l43
Set Lights(44) = l44
'Set Lights(45) = l45 'LightGameOver
Set Lights(46) = l46
Set Lights(47) = l47
'Set Lights(48) = unused
Set Lights(49) = l49
Set Lights(50) = l50
Set Lights(51) = l51
Set Lights(52) = l52
Set Lights(53) = l53
Set Lights(54) = l54
Set Lights(55) = l55
Set Lights(56) = l56
Set Lights(57) = l57
Set Lights(58) = l58
Set Lights(59) = l59 'LightCredit
Set Lights(60) = l60
'Set Lights(61) = l61 'LightTilt
Set Lights(62) = l62
Set Lights(63) = l63

```
