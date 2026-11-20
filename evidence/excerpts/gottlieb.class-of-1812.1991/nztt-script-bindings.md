# Class of 1812 VPX NZ&TT 1.0 (tom tower & ninuzzu): controller bindings

Source: `Class of 1812  - NZ&TT 1.0.vbs` in the pinned `sverrewl/vpxtable_scripts` corpus at revision
`0c036bb61b4b4e8c778c37559f6795df8cd1521e`, a 35,513-byte LF blob whose checkout is byte-identical, SHA-256
`b045899dfc7356c5c6c7a3cb19f89cdead062b48c86ce3b66a71c452ae3e3e65`: tom tower & ninuzzu's table script as patched by
Thalamus on 2018-07-23. The retained table embeds the script before that patch (SHA-256
`ff98cc7740b1b81cedf0322090034879fc66ce8906759f8d5e897c00e1ac1914`); compared with whitespace collapsed, it differs
only in `UseSolenoids = 1`, the absence of the `cSingleLFlip`/`cSingleRFlip` constants and of the four flipper-key
writes to switches 4 and 5, and blank lines, so both bind every playfield address to the same object. Line numbers
are the pinned file's. Leading whitespace is dropped, runs of spaces are collapsed, and a run of lines is joined with
" · ".

## Header and controller

| Line | Text |
| --- | --- |
| 39-41 | `'IPD No. 528 - 4 players` · `'© Gottlieb 1991` · `'VPX recreation by tom tower & ninuzzu` |
| 43-46 | `' Thalamus 2018-07-23` · `' This tables has already "Positional Sound Playback Functions" and "Supporting Ball & Sound Functions"` · `' Changed UseSolenoids=1 to 2` · `' No special SSF tweaks yet.` |
| 56-57 | `Const cSingleLFlip = 0` · `Const cSingleRFlip = 0` |
| 66 | `Const cGameName= "clas1812"` |
| 68 | `LoadVPM "02800000", "Class1812.VBS", 3.50` |
| 73-76 | `Const UseSolenoids = 2` · `Const UseLamps = 1` · `Const UseSync = 1` · `Const UseGI = 0` |
| 94 | `.HandleKeyboard = 0` |
| 98 | `.HandleMechanics = 0` |
| 112-114 | `vpmNudge.TiltSwitch = 151` · `vpmNudge.Sensitivity = 4` · `vpmNudge.TiltObj = Array(sw10, sw11, sw12, sw13, sw14)` |

## Saucers and drop banks (lines 116-147)

| Line | Text |
| --- | --- |
| 117-121 | `Set bsScoop = new cvpmSaucer` · `With bsScoop` · `.InitKicker Sw52, 52, 200, 25, 1` · `.InitSounds "fx_kicker_catch", SoundFX("CenterEject",DOFContactors), SoundFX("CenterEject",DOFContactors)` · `.CreateEvents "bsScoop", sw52` |
| 125-129 | `Set bsTK = new cvpmSaucer` · `With bsTK` · `.InitKicker Sw53k, 53, -30, 25, 0` · `.InitSounds "fx_metal_hit_1", SoundFX("LeftEject",DOFContactors), SoundFX("LeftEject",DOFContactors)` · `.CreateEvents "bsTK", sw53k` |
| 133-137 | `Set dtBankL = new cvpmDropTarget` · `With dtBankL` · `.InitDrop Array(sw16,sw26,sw36,sw46),Array(16,26,36,46)` · `.Initsnd SoundFX("CenterDropBankDown",DOFDropTargets), SoundFX("CenterDropBankUp",DOFDropTargets)` · `End With` |
| 140-144 | `Set dtBankR = new cvpmDropTarget` · `With dtBankR` · `.InitDrop Array(sw17,sw27,sw37,sw47),Array(17,27,37,47)` · `.Initsnd SoundFX("CenterDropBankDown",DOFDropTargets), SoundFX("CenterDropBankUp",DOFDropTargets)` · `End With` |
| 147 | `InitRolling:InitLamps:InitTrough:DiverterOn.IsDropped=1` |

## Keys (lines 155-170)

| Line | Text |
| --- | --- |
| 160-162 | `If keycode = LeftFlipperKey then Controller.switch(4)=1` · `If keycode = RightFlipperKey then Controller.switch(5)=1` · `If vpmKeyDown(keycode) Then Exit Sub` |
| 167-169 | `If keycode = LeftFlipperKey then Controller.switch(4)=0` · `If keycode = RightFlipperKey then Controller.switch(5)=0` · `if vpmKeyUp(keycode) Then Exit Sub` |

## Solenoid callbacks (lines 180-219)

| Line | Text |
| --- | --- |
| 180 | `'(**) Used in backbox (translite)` |
| 182-186 | `'SolCallback(1) = "" '1 - Left Bumper` · `'SolCallback(2) = "" '2 - Right Bumper` · `'SolCallback(3) = "" '3 - Bottom Bumper` · `'SolCallback(4) = "" '4 - Left Slingshot` · `'SolCallback(5) = "" '5 - Right Slingshot` |
| 187-193 | `SolCallback(6) = "SolVUK" '6 - Bottom Scoop` · `SolCallback(7) = "bsTK.SolOut" '7 - Top Upkicker` · `SolCallback(8) = "dtBankL.SolDropUp" '8 - Left Bank Reset` · `SolCallback(9) = "dtBankR.SolDropUp" '9 - Right Bank Reset` · `SolCallback(10) = "SolDiv" '10 - Diverter` · `SolCallback(11) = "SolHeart" '11 - Heart` · `SolCallback(12) = "SolTeeth" '12 - Teeth` |
| 195-203 | `'SolCallback(13) = "setlamp 143," '13 - Flasher:Lightning (3) **` · `'SolCallback(14) = "setlamp 144," '14 - Flasher:Willie Wolf (2) **` · `'SolCallback(15) = "setlamp 145," '15 - Flasher:Belly LaGhost (2) **` · `'SolCallback(16) = "setlamp 146," '16 - Flasher:Vamp do Tramp (2) **` · `'SolCallback(17) = "setlamp 147," '17 - Flasher:Mumsy N. Law (2) **` · `'SolCallback(18) = "setlamp 148," '18 - Flasher:Zom McCoffin (2) **` · `'SolCallback(19) = "setlamp 149," '19 - Flasher:Zom McCoffin (2) **` · `'SolCallback(20) = "setlamp 150," '20 - Flasher:Grover Cleaever (2) **` · `'SolCallback(21) = "setlamp 151," '21 - Flasher:Peter PieceMeal (2) **` |
| 205-208 | `SolCallback(22) = "SetLamp 152," '22 - Flasher:Ramps #1 (2)` · `SolCallback(23) = "SetLamp 153," '23 - Flasher:Ramps #2 (2)` · `SolCallback(24) = "SetLamp 154," '24 - Flasher:Ramps #3 (2)` · `SolCallback(25) = "SetLamp 155," '25 - Flasher:Heart (2)` |
| 210-216 | `SolCallback(26) = "GIRelay" '26 - LightBox Relay` · `SolCallback(27) = "" '27 - Ticket/Coin Meter` · `SolCallback(28) = "ReleaseBall" '28 - Ball Release` · `SolCallback(29) = "SolOuthole" '29 - Outhole.` · `SolCallback(30) = "SolKnocker" '30 - Knocker` · `SolCallback(31) = "TiltRelay" '31 - Tilt Relay` · `SolCallback(32) = "vpmNudge.SolGameOn" '32 - Game Over Relay` |
| 218-219 | `SolCallback(sLRFlipper) = "SolRFlipper"` · `SolCallback(sLLFlipper) = "SolLFlipper"` |

## Trough (lines 226-274)

| Line | Text |
| --- | --- |
| 226-231 | `Sub InitTrough` · `Slot1.CreateSizedballWithMass Ballsize/2,Ballmass` · `Slot2.CreateSizedballWithMass Ballsize/2,Ballmass` · `Controller.Switch(44) = 1` · `Controller.Switch(54) = 0` · `End Sub` |
| 234-236 | `Sub Slot2_Hit():UpdateTrough:End Sub` · `Sub Slot1_Hit():Controller.Switch(44) = 1:UpdateTrough:End Sub` · `Sub Slot1_UnHit():Controller.Switch(44) = 0:UpdateTrough:End Sub` |
| 249-257 | `Sub Drain_Hit()` · `PlaySoundAt "fx_drain",Drain` · `UpdateTrough` · `Controller.Switch(54) = 1` · `End Sub` · `Sub Drain_UnHit()` · `Controller.Switch(54) = 0` · `End Sub` |
| 259-266 | `Sub SolOuthole(enabled)` · `If enabled Then` · `Drain.kick 60,20` · `PlaySoundAt SoundFX(SSolenoidOn, DOFContactors), Drain` · `Else` · `PlaySoundAt SSolenoidOff, Drain` · `End If` · `End Sub` |
| 268-274 | `Sub ReleaseBall(enabled)` · `If enabled Then` · `PlaySoundAt SoundFX("fx_ballrel",DOFContactors), Drain` · `Slot1.kick 60, 9` · `UpdateTrough` · `End If` · `End Sub` |

## Solenoid routines (lines 281-368)

| Line | Text |
| --- | --- |
| 281-285 | `Sub SolKnocker(enabled)` · `If Enabled Then` · `PlaySoundAt SoundFX("Knocker",DOFKnocker), l82` · `End If` · `End Sub` |
| 309-318 | `Sub SolVUK(enabled)` · `If Enabled Then` · `sw52.timerinterval=500:sw52.timerEnabled=1` · `CenterHole.Enabled=0` · `bsScoop.ExitSol_On` · `sw52p.transZ=30` · `End If` · `End Sub` · `sub sw52_timer:me.timerEnabled=0:CenterHole.Enabled=1:sw52p.transZ=0:end Sub` |
| 323-337 | `Sub SolDiv(Enabled)` · `If Enabled Then` · `DiverterOff.IsDropped=1` · `DiverterOn.IsDropped=0` · `DiverterDir = -1` · `Diverter.Interval = 5:Diverter.Enabled = 1` · `PlaySoundAt SoundFX("DiverterOn",DOFContactors),DiverterP` · `Else` · `DiverterOff.IsDropped=0` · `DiverterOn.IsDropped=1` · `DiverterDir = +1` · `Diverter.Interval = 5:Diverter.Enabled = 1` · `PlaySoundAt SoundFX("DiverterOff",DOFContactors),DiverterP` · `End If` · `End Sub` |
| 339-343 | `Sub Diverter_Timer()` · `DiverterP.RotZ=DiverterP.RotZ+DiverterDir` · `If DiverterP.RotZ>5 AND DiverterDir=1 Then Me.Enabled=0:DiverterP.RotZ=5` · `If DiverterP.RotZ<-35 AND DiverterDir=-1 Then Me.Enabled=0:DiverterP.RotZ=-35` · `End Sub` |
| 346-359 | `Sub SolHeart(enabled)` · `If enabled Then` · `heartMove.enabled=1:PlaySoundAt SoundFX(SSolenoidOn,DOFContactors),heart` · `Else` · `PlaySoundAt SoundFX(SSolenoidOff,DOFContactors),heart` · `End If` · `End Sub` · `dim pump, heartD` · `sub heartMove_timer()` · `pump=pump+10` · `heartD=dsin(pump)` · `if pump>180 then pump=0:heart.size_y=1:Me.enabled=0` · `heart.size_y=(heartD/8)+1.2` · `end sub` |
| 362-368 | `Sub SolTeeth(enabled)` · `If enabled Then` · `BottomTeeth.RotX=0` · `Else` · `BottomTeeth.RotX=-25` · `End If` · `End Sub` |

## Switch writers (lines 375-468)

| Line | Text |
| --- | --- |
| 375-377 | `Sub sw10_Hit() : vpmTimer.PulseSw 10 : PlaySoundAt SoundFX("LeftJet",DOFContactors), ActiveBall: End Sub` · `Sub sw11_Hit() : vpmTimer.PulseSw 11 : PlaySoundAt SoundFX("RightJet",DOFContactors), ActiveBall: End Sub` · `Sub sw12_Hit() : vpmTimer.PulseSw 12 : PlaySoundAt SoundFX("BottomJet",DOFContactors), ActiveBall: End Sub` |
| 381-383 | `Sub sw13_Slingshot` · `PlaySoundAt SoundFX("LeftSlingShot",DOFContactors), ActiveBall` · `vpmTimer.PulseSw 13` |
| 386 | `sling1.TransZ = -20` |
| 400-402 | `Sub sw14_Slingshot` · `PlaySoundAt SoundFX("RightSlingShot",DOFContactors), ActiveBall` · `vpmTimer.PulseSw 14` |
| 405 | `sling2.TransZ = -20` |
| 420 | `Sub sw15_Spin: vpmtimer.pulsesw 15:End Sub` |
| 423-426 | `Sub sw16_dropped:dtBankL.Hit 1:End Sub` · `Sub sw26_dropped:dtBankL.Hit 2:End Sub` · `Sub sw36_dropped:dtBankL.Hit 3:End Sub` · `Sub sw46_dropped:dtBankL.Hit 4:End Sub` |
| 428-431 | `Sub sw17_dropped:dtBankR.Hit 1:End Sub` · `Sub sw27_dropped:dtBankR.Hit 2:End Sub` · `Sub sw37_dropped:dtBankR.Hit 3:End Sub` · `Sub sw47_dropped:dtBankR.Hit 4:End Sub` |
| 434-436 | `Sub Sw20_Hit():vpmTimer.PulseSw 20: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw30_Hit():vpmTimer.PulseSw 30: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw40_Hit():vpmTimer.PulseSw 40: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` |
| 438-440 | `Sub Sw21_Hit():vpmTimer.PulseSw 21: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw31_Hit():vpmTimer.PulseSw 31: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw41_Hit():vpmTimer.PulseSw 41: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` |
| 442-444 | `Sub Sw22_Hit():vpmTimer.PulseSw 22: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw32_Hit():vpmTimer.PulseSw 32: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` · `Sub Sw42_Hit():vpmTimer.PulseSw 42: PlaysoundAt SoundFX("fx_target",DOFTargets), ActiveBall: End Sub` |
| 447-452 | `Sub Sw23_Hit:Controller.Switch(23)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw23_UnHit:Controller.Switch(23)=0: End Sub` · `Sub Sw24_Hit:Controller.Switch(24)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw24_UnHit:Controller.Switch(24)=0: End Sub` · `Sub Sw25_Hit:Controller.Switch(25)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw25_UnHit:Controller.Switch(25)=0: End Sub` |
| 454-465 | `Sub Sw33_Hit:Controller.Switch(33)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw33_UnHit:Controller.Switch(33)=0: End Sub` · `Sub Sw34_Hit:Controller.Switch(34)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw34_UnHit:Controller.Switch(34)=0: End Sub` · `Sub Sw35_Hit:Controller.Switch(35)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw35_UnHit:Controller.Switch(35)=0: End Sub` · `Sub Sw43_Hit:Controller.Switch(43)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw43_UnHit:Controller.Switch(43)=0: End Sub` · `Sub Sw45_Hit:Controller.Switch(45)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw45_UnHit:Controller.Switch(45)=0: End Sub` · `Sub Sw55_Hit:Controller.Switch(55)=1: PlaysoundAt "fx_sensor", ActiveBall: End Sub` · `Sub Sw55_UnHit:Controller.Switch(55)=0: End Sub` |
| 466-468 | `'Optos` · `Sub Sw50_Hit():vpmTimer.PulseSw 50: PlaysoundAt "fx_plasticrolling", ActiveBall: End Sub` · `Sub Sw51_Hit():vpmTimer.PulseSw 51: PlaysoundAt "fx_plasticrolling", ActiveBall: End Sub` |

## General illumination (lines 474-500)

| Line | Text |
| --- | --- |
| 474-476 | `Sub GIRelay(enabled)` · `If Enabled Then` · `for each xx in GI:xx.State=0:Next` |
| 480-481 | `Else` · `for each xx in GI:xx.State=1:Next` |
| 488-490 | `Sub TiltRelay(enabled)` · `If Enabled Then` · `for each xx in GI:xx.State=0:Next` |
| 494-495 | `Else` · `for each xx in GI:xx.State=1:Next` |

## Lamps (lines 509-568)

| Line | Text |
| --- | --- |
| 512 | `For i=0 To 200: Execute "Lights(" & i & ") = Array (L" & i & ",L" & i & "a)": Next` |
| 526-533 | `SwapTex 2, TopTeeth, "teeth", "teeth_on" 'teeth` · `SwapTex 2, BottomTeeth, "teeth", "teeth_on" 'teeth` · `AddLamp 2, Li2 'teeth` · `AddLamp 10, bulb9 'BAT-o-Meter "5.000"` · `AddLamp 11, bulb8 'BAT-o-Meter "10.000"` · `AddLamp 12, bulb7 'BAT-o-Meter "20.000"` · `AddLamp 13, bulb6 'BAT-o-Meter "EXTRA BALL"` · `AddLamp 14, bulb5 'BAT-o-Meter "SPECIAL"` |
| 535-539 | `AddLamp 10, Li10 'BAT-o-Meter "5.000"` · `AddLamp 11, Li11 'BAT-o-Meter "10.000"` · `AddLamp 12, Li12 'BAT-o-Meter "20.000"` · `AddLamp 13, Li13 'BAT-o-Meter "EXTRA BALL"` · `AddLamp 14, Li14 'BAT-o-Meter "SPECIAL"` |
| 541-545 | `AddLamp 36, bulb1 'Left Ramp Add Letter (Left)` · `AddLamp 37, bulb2 'Left Ramp Million (Right)` · `AddLamp 46, bulb3 'Right Ramp Add Letter (Left)` · `AddLamp 47, bulb4 'Right Ramp Million (Right)` · `AddLamp 67, bulb10 '"TO CRYPT"` |
| 547-554 | `AddLamp 152, domeYB 'Yellow Dome Bottom` · `AddLamp 152, F22` · `AddLamp 152, F22r1` · `AddLamp 152, F22r2` · `AddLamp 152, domeW 'White Dome` · `AddLamp 152, F22a` · `AddLamp 152, F22r3` · `AddLamp 152, F22r4` |
| 555-561 | `AddLamp 153, domeYT 'Yellow Dome Top` · `AddLamp 153, F22x` · `AddLamp 153, F22r1x` · `AddLamp 153, F22r2x` · `AddLamp 153, domeR 'Red Dome` · `AddLamp 153, F23` · `AddLamp 153, F23r` |
| 562-566 | `AddLamp 154, F24 'Under The Ramp` · `AddLamp 154, domeB 'Blue Dome` · `AddLamp 154, F24a` · `AddLamp 154, F24r1` · `AddLamp 154, F24r2` |
| 567-568 | `AddLamp 155, F25 'Flasher:Heart #1` · `SwapTex 155, heart, "hearttext", "hearttext" 'Flasher:Heart #2` |

## Ramp sounds (lines 769-788)

| Line | Text |
| --- | --- |
| 769-777 | `' Ball Drop & Ramp Sounds` · `' *********************************************************************` · `'left ramp` · `Sub LREnter_Hit():If ActiveBall.VelY < 0 Then PlaySoundAt "fx_rrenter", ActiveBall:End If:End Sub 'ball is going up` · `Sub LREnter_UnHit():If ActiveBall.VelY > 0 Then StopSound "fx_rrenter":End If:End Sub 'ball is going down` · `Sub LRHelp1_hit():PlaySoundAt "fx_rturn", ActiveBall:End Sub` · `Sub LRail_hit():StopSound "fx_plasticrolling":PlaySoundAt "fx_wireramp", ActiveBall:End Sub` · `Sub LRExit_Hit:StopSound "fx_wireramp":PlaysoundAt "fx_wireramp_exit", ActiveBall:Me.TimerInterval=200:Me.TimerEnabled=1:End Sub` · `Sub LRExit_timer:Me.TimerEnabled=0:PlaysoundAt "fx_balldrop", LRExit:End Sub` |
| 779-788 | `'right ramp` · `Sub RREnter_Hit():If ActiveBall.VelY < 0 Then PlaySoundAt "fx_rrenter", ActiveBall:End If:End Sub 'ball is going up` · `Sub RREnter_UnHit():If ActiveBall.VelY > 0 Then StopSound "fx_rrenter":End If:End Sub 'ball is going down` · `Sub RRHelp1_hit():PlaySoundAt "fx_rturn", ActiveBall:End Sub` · `Sub RRHelp2_hit():PlaySoundAt "fx_rh1", ActiveBall:End Sub` · `Sub RRHelp3_Hit:If ActiveBall.Z>80 Then PlaySoundAt "fx_rh2", ActiveBall:Me.TimerInterval=200:Me.TimerEnabled=1:End If:End Sub` · `Sub RRHelp3_timer:Me.TimerEnabled=0:PlaysoundAt "fx_balldrop", RRHelp2:End Sub` · `Sub RRail_Hit:StopSound "fx_plasticrolling":PlaySoundAt "fx_wireramp", ActiveBall:End Sub` · `Sub RRExit_Hit:StopSound "fx_wireramp":PlaysoundAt "fx_wireramp_exit", ActiveBall:Me.TimerInterval=200:Me.TimerEnabled=1:End Sub` · `Sub RRExit_timer:Me.TimerEnabled=0:PlaysoundAt "fx_balldrop", RRExit:End Sub` |

## Corroboration: the 3.0.21 update of the same table

`special_audiopan_and_audiofade_patched/Class of 1812 (Gottlieb 1991) v3.0.21.vbs` in the same corpus and revision,
190,387 bytes, SHA-256 `214ee041c554a2aedb61e7699a57fabf1e7869948d494a3a9f48d93041c83cd3`. It is a later version of
this table, so it corroborates and never independently confirms.

| Line | Text |
| --- | --- |
| 12-20 | `' Version 3.0 by UnclePaulie 2023` · `' Table includes Hybrid VR/desktop/cabinet modes, enhanced playfield by Redbone, VPW physics, Fleep sounds, Lampz, 3D inserts, new GI,` · `' sling corrections, targets, saucers, playfield mesh, etc.` · `' Tomate created a VLM and UnclePaulie updated the script.` · `' Updated Version 2 by UnclePaulie, which was originally done by Tom Tower & Ninuzzu` · `' Complete implementation details and credits found at the bottom of the script.` · `' Version 3.0.15 by UnclePaulie and Tomate 2024` · `' Tomate did VLM baking, and UnclePaule incorporated the associated script and updates to pwm and VPW standards.` |
| 706-722 | `SolCallback(6) = "SolVUK" '6 - Bottom Scoop` · `SolCallback(7) = "SolSaucerUp" '7 - Top Upkicker` · `SolCallback(8) = "SolDtBankLeft" '8 - Left Bank Reset` · `SolCallback(9) = "SolDtBankRight" '9 - Right Bank Reset` · `SolCallback(10) = "SolDiv" '10 - Diverter` · `SolCallback(11) = "SolHeart" '11 - Heart` · `SolCallback(12) = "SolTeeth" '12 - Teeth` · `SolModCallback(22) = "DomeFlashWhite" '22 - Flasher:Ramps #1 (2) White dome and yellow dome bottom` · `SolModCallback(23) = "DomeFlashRed" '23 - Flasher:Ramps #2 (2) Red dome and yellow dome top` · `SolModCallback(24) = "DomeFlashBlue" '24 - Flasher:Ramps #3 (2) Blue dome and under ramp` · `SolModCallback(25) = "SolHeartFlash" '25 - Flasher:Heart (2)` · `SolModCallback(26) = "BGGI" '26 - LightBox Relay` · `SolCallback(28) = "ReleaseBall" '28 - Ball Release` · `SolCallback(29) = "SolOuthole" '29 - Outhole.` · `SolCallback(30) = "SolKnocker" '30 - Knocker` · `SolModCallback(31) = "PFGI" '31 - Playfield GI / Tilt Relay` |
| 728-741 | `'***********************************************` · `' *** Backglass Solenoid Controlled Flashers ***` · `'***********************************************` · `' THESE ARE OFF BY 1. 12--> 13; 13-->14, ETC. (manual starts at zero)` · `SolModCallback(13) = "SolFLamp12" '12 - Flasher:Lightning (3) **` · `SolModCallback(14) = "SolFLamp13" '13 - Flasher:Willie Wolf (2) **` · `SolModCallback(15) = "SolFLamp14" '14 - Flasher:Belly LaGhost (2) **` · `SolModCallback(16) = "SolFLamp15" '15 - Flasher:Vamp do Tramp (2) **` · `SolModCallback(17) = "SolFLamp16" '16 - Flasher:Mumsy N. Law (2) **` · `SolModCallback(18) = "SolFLamp17" '17 - Flasher:Zom McCoffin (2) **` · `SolModCallback(19) = "SolFLamp18" '18 - Flasher:Zom McCoffin (2) **` · `SolModCallback(20) = "SolFLamp19" '19 - Flasher:Grover Cleaever (2) **` · `SolModCallback(21) = "SolFLamp20" '20 - Flasher:Peter PieceMeal (2) **` |
| 787-791 | `'********************* TROUGH *************************` · `Sub Slot2_Hit():Controller.Switch(44) = 1:UpdateTrough:End Sub` · `Sub Slot2_UnHit():Controller.Switch(44) = 0:UpdateTrough:End Sub` · `Sub Slot1_UnHit():UpdateTrough:End Sub` |
| 4601-4611 | `'******** Revisions done on VR version 1.2 *********` · `' NOTE: THIS IS NO LONGER VALID. REAL FIX IS IN 1.3.1` · `' *** Updated two errors in original table. Sub Slot2 was originally Slot2_Hit(). That caused too many balls to be on table in tilt mode` · `' *** once that was changed, there was an issue that caused during the heartbeat multiball, the 2nd ball didn't come into outlane` · `' *** the issue was that the Slot1_Hit() updated the trough in the subroutine. Needed to remove UpdateTrough` · `'******** Revisions done on VR version 1.3 *********` · `' Animated the flashers on the backglass` · `'******** Revisions done on VR version 1.3.1 *********` · `' Finally fixed the trough issue, and the tilt issue, and the multiball issue. The issue was that slot1 and slot2 subroutines were reversed.` |
