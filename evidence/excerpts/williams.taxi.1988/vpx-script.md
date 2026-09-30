# Retained Taxi VPX script contract

Exact local filename Taxi (Williams 1988)1.2.vpx; embedded metadata names Taxi (Williams), author 32assassin, version 2.0. Filename version is not metadata version. Embedded script SHA-256 937b1ab632c4e5071f43702d554c414525738a193b8db14bdb5e4d5f964417c3. No same-basename VBS sidecar was found. Exact table was retained after title, ROM taxi_l4 and physical artwork/topology checks. It was not launched during curation; this excerpt records its implemented behavior.

Complete solenoid callback and GI/flipper section (lines 27..88):

```vb
SolCallback(1) = "bsTrough.SolIn"
SolCallback(2) = "bsTrough.SolOut"
SolCallback(3) = "b3.SolOut"
SolCallback(4) = "dtC.SolDropUp"
SolCallback(5) = "bsJoyRide.SolOut"
SolCallback(6) = "dtR.SolDropUp"
SolCallback(7) = "bsSpinOut.SolOut"
SolCallback(8) = "bsLock.SolOut"
SolCallback(9) = "vpmSolWall TopGate, 0, " 'Top ball Gate
SolCallback(13) = "vpmSolSound ""fx_bellring"","
SolCallback(14) = "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"
SolCallback(23) = "vpmNudge.SolGameOn"

'GI
'SolCallback(10) = 'Insert Gen Illumin Relay aka backglass GI
SolCallback(11) = "PFGI" 'PF GI

'Flahsers
SolCallback(15) ="vpmFlasher Flasher15," 'Jackpot Flasher
SolCallback(16) ="vpmFlasher Flasher16," 'Joyride Flasher
SolCallback(25) ="vpmFlasher Flasher25,"
SolCallback(26) ="vpmFlasher Flasher26,"
SolCallback(27) ="vpmFlasher Flasher27,"
SolCallback(28) ="vpmFlasher Flasher28,"
SolCallback(29) ="vpmFlasher Flasher29,"
SolCallback(30) ="vpmFlasher array(Flasher30,Flasher30a)," 'Left Ramp Flasher
SolCallback(31) ="vpmFlasher array(Flasher31,Flasher31a)," 'Right Ramp Flasher
SolCallback(32) ="vpmFlasher array(Flasher32,Flasher32a)," 'Spinout Flasher


SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"

Sub SolLFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):LeftFlipper.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):LeftFlipper.RotateToStart
     End If
  End Sub

Sub SolRFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):RightFlipper.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):RightFlipper.RotateToStart
     End If
End Sub
'**********************************************************************************************************

'Playfield GI
Sub PFGI(Enabled)
	If Enabled Then
		dim xx
		For each xx in GI:xx.State = 0: Next
        PlaySound "fx_relay"
	Else
		For each xx in GI:xx.State = 1: Next
        PlaySound "fx_relay"
	End If
 End Sub

```

Complete ball stack and drop-bank construction (lines 122..155):

```vb
    Set bsTrough = New cvpmBallStack
		bsTrough.InitSw 10, 11, 12, 0, 0, 0, 0, 0
		bsTrough.InitKick BallRelease, 60, 6
		bsTrough.Balls = 2
		bsTrough.InitExitSnd SoundFX("ballrelease",DOFContactors), SoundFX("Solenoid",DOFContactors)

    Set bsLock = New cvpmBallStack
		bsLock.InitSaucer RightLock, 36, 180, 20
		bsLock.InitExitSnd SoundFX("Popper",DOFContactors), SoundFX("Solenoid",DOFContactors)

    Set bsJoyRide = New cvpmBallStack
		bsJoyRide.InitSaucer JoyrideEject, 13, 170, 20
		bsJoyRide.InitExitSnd SoundFX("Popper",DOFContactors), SoundFX("Solenoid",DOFContactors)

    Set b3 = New cvpmBallStack
		b3.InitSaucer Catapult, 35, 0, 140
		b3.KickZ = 1
		b3.InitExitSnd SoundFX("Popper",DOFContactors), SoundFX("Solenoid",DOFContactors)

    Set bsSpinout = New cvpmBallStack
		bsSpinout.InitSw 0, 43, 0, 0, 0, 0, 0, 0
		bsSpinout.InitKick SpinoutKicker, 330, 35
		bsSpinout.KickAngleVar = 2
		bsSpinout.KickForceVar = 3
		bsSpinout.InitExitSnd SoundFX("Popper",DOFContactors), SoundFX("Solenoid",DOFContactors)

    Set dtR = New cvpmDropTarget
		dtR.InitDrop Array(sw30,sw31,sw32),Array(30,31,32)
		dtR.InitSnd  SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

    Set dtC = New cvpmDropTarget
		dtC.InitDrop Array(sw27,sw28,sw29),Array(27,28,29)
		dtC.InitSnd  SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

```

Ball and switch event section (lines 174..261):

```vb
Sub Drain_Hit:playsound"drain":bsTrough.addball me:End Sub
Sub RightLock_Hit():bsLock.AddBall 0 : playsound "popper_ball": End Sub
Sub JoyrideEject_Hit():bsJoyRide.AddBall 0 : playsound "popper_ball": End Sub

'Dracula kicker
Sub Catapult_Hit():b3.AddBall 0: playsound "popper_ball": End Sub

Sub DracKickerIn_Hit()
    DracKickerIn.DestroyBall
    vpmCreateBall DracKickerOut
    DracKickerOut.Kick 15, 45
    Prim_Catapult.ObjRotX = 75
    Me.TimerEnabled = 1
End Sub
Sub DracKickerIn_timer : Prim_Catapult.ObjRotX = 0 : Me.TimerEnabled = 0 : End Sub

'Spinner Ramp
Sub SpinoutKicker1_Hit():SpinoutKicker1.DestroyBall:bsSpinOut.addball Me : StopSound "fx_launch" : PlaySound "fx_balldrop": End Sub
Sub SpinHelp_Hit():StopSound "fx_launch" :ActiveBall.VelY = 1.4 * ActiveBall.VelY:End Sub
Sub SpinoutTrigger_Hit():vpmTimer.pulsesw 44:End Sub
Sub Trigger7_Hit() : PlaySound "fx_turn_SSRamp" :End Sub
Sub Trigger8_Hit() : If ActiveBall.VelY < 0 Then Playsound "fx_launch" : Else StopSound "fx_launch" : End If : End Sub

'Drop Targets
 Sub Sw27_Dropped:dtC.Hit 1 :End Sub
 Sub Sw28_Dropped:dtC.Hit 2 :End Sub
 Sub Sw29_Dropped:dtC.Hit 3 :End Sub

 Sub Sw30_Dropped:dtR.Hit 1 :End Sub
 Sub Sw31_Dropped:dtR.Hit 2 :End Sub
 Sub Sw32_Dropped:dtR.Hit 3 :End Sub

'Bumpers
Sub Bumper1_Hit():vpmTimer.pulsesw 17 : playsound"fx_bumper1": End Sub
Sub Bumper2_Hit():vpmTimer.pulsesw 19 : playsound"fx_bumper2": End Sub
Sub Bumper3_Hit():vpmTimer.pulsesw 21 : playsound"fx_bumper3": End Sub

'Stand UP Target
Sub sw24_Hit():vpmTimer.PulseSwitch 24, 0, "":End Sub

'Wire Triggers
 Sub sw14_Hit():Controller.Switch(14)=1: playsound"rollover" : End Sub
 Sub sw14_Unhit():Controller.Switch(14)=0:End Sub
 Sub sw15_Hit():Controller.Switch(15)=1 : playsound"rollover" : End Sub
 Sub sw15_Unhit():Controller.Switch(15)=0:End Sub
 Sub sw16_Hit():Controller.Switch(16)=1 : playsound"rollover" : End Sub
 Sub sw16_Unhit():Controller.Switch(16)=0:End Sub
 Sub sw37_Hit():Controller.Switch(37)=1 : playsound"rollover" : End Sub
 Sub sw37_UnHit():Controller.Switch(37)=0:End Sub
 Sub sw38_Hit():Controller.Switch(38)=1 : playsound"rollover" : End Sub
 Sub sw38_UnHit():Controller.Switch(38)=0:End Sub
 Sub sw39_Hit():Controller.Switch(39)=1 : playsound"rollover" : End Sub
 Sub sw39_UnHit():Controller.Switch(39)=0:End Sub
 Sub sw40_Hit():Controller.Switch(40)=1 : playsound"rollover" : End Sub
 Sub sw40_UnHit():Controller.Switch(40)=0:End Sub
'Shooter Lane
 Sub sw22_Hit():Controller.Switch(22)=1 : playsound"rollover" : End Sub
 Sub sw22_Unhit():Controller.Switch(22)=0 : End Sub

'Gate Triggers
'Gorbie Lane Entry
Sub sw23_Hit():vpmTimer.PulseSwitch 23, 0, "":End Sub
'Left Ramp Entry
Sub sw25_Hit():vpmTimer.PulseSwitch 25, 0, "":End Sub
'Right Ramp Entry
Sub sw26_Hit():vpmTimer.PulseSwitch 26, 0, "":End Sub

'Right Ramp exit = enter wire ramp
Sub sw33_Hit():Controller.Switch(33) = 1 : sw33.timerenabled = 1 : playsound"rollover" : End Sub
Sub sw33_UnHit():Controller.Switch(33) = 0:End Sub
dim sw33Dir
sw33Dir = -1
Sub sw33_Timer()
	If sw33P.ObjRotZ = 240 then sw33Dir = 20
	If sw33P.ObjRotZ = 220 then sw33Dir = -20
	sw33P.ObjRotZ = sw33P.ObjRotZ - sw33Dir
	If sw33P.ObjRotZ = 220 then sw33.timerenabled = 0
End Sub

'Left Ramp exit = enter wire ramp
Sub sw34_Hit():Controller.Switch(34) = 1 : sw34.timerenabled = 1 : playsound"rollover" : End Sub
Sub sw34_UnHit():Controller.Switch(34) = 0:End Sub
dim sw34Dir
sw34Dir = -1
Sub sw34_Timer()
	If sw34P.ObjRotZ = 110 then sw34Dir = 20
	If sw34P.ObjRotZ = 130 then sw34Dir = -20
	sw34P.ObjRotZ = sw34P.ObjRotZ + sw34Dir
```

Bumper hit callbacks set public 17,19,21. The sling animation does not report 18/20 in this retained script; the factory switches are still fitted. Dracula transfer kickers and SpinoutKicker1 are simulation ball-transfer helpers, not extra physical coils. Flasher 15..32 Light objects paint illuminated regions; even L25.is_bulb_light is a rendering property, not proof of a visible socket. Do not map the lamp/flasher helper centers as additional bulbs.
