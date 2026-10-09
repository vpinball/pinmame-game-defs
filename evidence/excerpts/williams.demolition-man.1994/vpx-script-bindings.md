# Demolition Man — retained table script bindings

Quoted from `Demolition Man (Knorr-Kiwi) 1.3.1.vbs` (SHA-256 `0af7e1f50985d5a36d7b3f74ac1254a9d54594189c92934072a8951e7bf75e12`, 1641 lines), the embedded script of the retained Knorr/Kiwi 1.3.1 table extracted with vpxtool. Only the 288 non-comment lines that bind the controller are kept, each with its line number in the file: the ROM and library selection, the Controller settings, every Controller.Switch write and PulseSw, the ball stacks and mechs with their switches and solenoids, the SolCallback/SolModCallback table, the flipper and diverter subs, the lamp fader calls and the G.I. callback. Tabs are shown as four spaces; nothing else is changed.

```vbscript
   64:  LoadVPM "01560000", "WPC.VBS", 3.36
   72:  Const cGameName = "dm_lx4"
   82:  Set GiCallback2 = GetRef("UpdateGI")
  100:         .GameName = cGameName
  101:           If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
  102:          .Games(cGameName).Settings.Value("rol") = 0
  103:          .HandleKeyboard = 0
  107:          .HandleMechanics = 0
  114:          .Switch(22) = 1 'close coin door
  115:          .Switch(24) = 1 'and keep it close
  118:             vpmNudge.TiltSwitch = 14
  128:          .InitSw 0, 31, 32, 33, 34, 35, 0, 0
  129:          .InitKick BallRelease, 90, 10
  141:         .InitCaptive RetinaTrigger, RetinaWall, RetinaKicker, 345
  154:   .mtype =vpmmechtwodirsol + vpmmechstopend + vpmmechlinear
  155:   .sol1  =19
  156:   .sol2  =20
  157:   .length=Clawspeed
  158:   .steps = 147
  159:   .addsw 25,0,2
  160:   .addsw 26,140,147
  167:         .mtype = vpmMechOneSol + vpmMechReverse + vpmMechLinear
  168:         .Sol1 = 18
  169:         .Length = 15
  170:         .steps = 70
  171:         .addsw 67,0,2
  172:         .addsw 74,65,70
  184:     .InitSaucer sw73, 73, 182, 18
  197:         .InitSw 0, 76, 0, 0, 0, 0, 0, 0
  198:         .InitKick sw76, 58, 73
  210:     .InitSaucer sw66, 66, 180, 2
  222:         .InitCaptive OldsmobileTrigger, OldsmobileWall, OldsmobileKicker, 345
  237:     .CallBackL = "SolLflipper"    'Point these to flipper subs
  238:     .CallBackR = "SolRflipper"    '...
  246:     vpmNudge.TiltSwitch=1
  278:     CapKicker1.Kick 0,0
  280:     Controller.Switch(71) = 1
  292:     Controller.Switch(72) = 1
  300: Sub sw72_Hit:Controller.Switch(72) = 0:End Sub        'GMUltralite Restswitch
  301: Sub sw72_UnHit:Controller.Switch(72) = 1: End Sub
  303: Sub sw71_Hit:Controller.Switch(71) = 0:End Sub        'Oldsmobil Restswitch
  304: Sub sw71_UnHit:Controller.Switch(71) = 1: End Sub
  310: SolCallback(1) = "SolRelease"
  311: SolCallback(2) = "BottomPopper.SolOut"
  312: SolCallback(3) = "AutoPlunge"
  313: SolCallback(4) = "bsTopPopper.SolOut"
  314: SolCallback(15) = "DiverterRight"
  315: SolCallback(7) = "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"
  316: SolCallBack(14) = "bsEject.SolOut"
  317: SolCallBack(19) = "SolClawMotorLeft"
  318: SolCallback(33) = "ClawMagnetOn"
  320: SolCallBack(31) = "FastFlips.TiltSol"
  323: SolModCallback(17) = "Flash117"            'ClawFlasher
  324: SolModCallback(21) = "Flash121"            'JetsFlasher
  325: SolModCallback(22) = "Flash122"            'SideRampFlasher
  326: SolModCallback(23) = "Flash123"            'LeftRampUpFlasher
  327: SolModCallback(24) = "Flash124"            'LeftRampLwrFlasher
  328: SolModCallback(25) = "Flash125"            'CarChaseCntrFlasher
  329: SolModCallback(26) = "Flash126"            'CarChaseLwrFlasher
  330: SolModCallback(27) = "Flash127"            'RightRampFlasher
  331: SolModCallback(28) = "Flash128"            'EjectFlasher
  334: SolModCallback(51) = "Flash137"            'CarChaseUprFlasher
  335: SolModCallback(52) = "Flash138"            'LowerReboundFlasher
  336: SolModCallback(53) = "Flash139"            'EyeballFlasher
  337: SolModCallback(54) = "Flash140"            'CenterRampFlasher
  338: SolModCallback(55) = "Flash141"            'Elevator 2 Flasher
  339: SolModCallback(56) = "Flash142"            'Elevator 1 Flasher
  340: SolModCallback(57) = "Flash143"            'DiverterFlasher
  341: SolModCallback(58) = "Flash144"            'Rt.RampUpFlasher
  350:          vpmTimer.PulseSw 36
  401:     controller.Switch(74) = True
  402:     BallinClaw = True
  407:     If Enabled And BallinClaw = True Then
  417:     If BallinClaw = True then
  418:         if Claw.RotY >= 11 Then ClawKicker5.CreateSizedBall(25.5): ClawKicker5.Kick 185, 1:BallinClaw = False
  419:         if Claw.RotY <= 10.99 And Claw.RotY >= -9.99 Then ClawKicker4.CreateSizedBall(25.5): ClawKicker4.Kick 180, 1:BallinClaw = False
  420:         if Claw.RotY <= -10 And Claw.RotY >= -28.99 Then ClawKicker3.CreateSizedBall(25.5): ClawKicker3.Kick 161, 1:BallinClaw = False
  421:         if Claw.RotY <= -29 And Claw.RotY >= -52.99 Then ClawKicker2.CreateSizedBall(25.5): ClawKicker2.Kick 143, 1:BallinClaw = False
  422:         if Claw.Roty <= -53 And Claw.RotY >= -108.99 Then ClawKicker1.CreateSizedBall(25.5): ClawKicker1.Enabled = False: ClawKicker1.Kick 0, 1:BallinClaw = False
  481:     vpmTimer.PulseSw 81
  502:         vpmTimer.PulseSw vpmNudge.TiltSwitch
  506:     If KeyCode = LeftFlipperKey then FastFlips.FlipL True' :  FastFlips.FlipUL True
  507:     If KeyCode = RightFlipperKey then FastFlips.FlipR True' :  FastFlips.FlipUR True
  508:     If keycode = PlungerKey Then Controller.Switch(11) = 1: Controller.Switch(12) = 1
  510:     If keycode = keyFront Then Controller.Switch(23) = 1
  521:     If KeyCode = LeftFlipperKey then FastFlips.FlipL False' :  FastFlips.FlipUL False
  522:     If KeyCode = RightFlipperKey then FastFlips.FlipR False' :  FastFlips.FlipUR False
  526:      If keycode = PlungerKey Then Controller.Switch(11) = 0: Controller.Switch(12) = 0
  528:      If keycode = keyFront Then Controller.Switch(23) = 0
  541:  Sub SolLFlipper(Enabled)
  543:          PlaySound SoundFX("FlipperUpLeftBoth",DOFContactors):LeftFlipper.RotateToEnd:LeftFlipper1.RotateToEnd
  545:          PlaySound SoundFX("FlipperDown",DOFContactors):LeftFlipper.RotateToStart:LeftFlipper1.RotateToStart
  549:  Sub SolRFlipper(Enabled)
  567:         Kicker1.Kick 1,48
  584: Sub sw27_Hit:Controller.Switch(27) = 1:sw27wire.RotX = 15:PlaySound "metalhit_thin":End Sub        'shooterlane
  585: Sub sw27_UnHit:Controller.Switch(27) = 0:sw27wire.RotX = 0: End Sub
  586: Sub sw15_Hit:Controller.Switch(15) = 1:sw15wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'left outlane
  587: Sub sw15_UnHit:Controller.Switch(15) = 0:sw15wire.RotX = 0:End Sub
  588: Sub sw16_Hit:Controller.Switch(16) = 1:sw16wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'left inlane
  589: Sub sw16_UnHit:Controller.Switch(16) = 0:sw16wire.RotX = 0:End Sub
  590: Sub sw17_Hit:Controller.Switch(17) = 1:sw17wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'right inlane
  591: Sub sw17_UnHit:Controller.Switch(17) = 0:sw17wire.RotX = 0:End Sub
  592: Sub sw18_Hit:Controller.Switch(18) = 1:sw18wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'right outlane
  593: Sub sw18_UnHit:Controller.Switch(18) = 0:sw18wire.RotX = 0:End Sub
  594: Sub sw63_Hit:Controller.Switch(63) = 1:sw63wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'leftrollover
  595: Sub sw63_UnHit:Controller.Switch(63) = 0:sw63wire.RotX = 0:End Sub
  596: Sub sw64_Hit:Controller.Switch(64) = 1:sw64wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'centerrollover
  597: Sub sw64_UnHit:Controller.Switch(64) = 0:sw64wire.RotX = 0:End Sub
  598: Sub sw65_Hit:Controller.Switch(65) = 1:sw65wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'rightrollover
  599: Sub sw65_UnHit:Controller.Switch(65) = 0:sw65wire.RotX = 0:End Sub
  600: Sub sw48_Hit:Controller.Switch(48) = 1:sw48wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'Right freeway
  601: Sub sw48_UnHit:Controller.Switch(48) = 0:sw48wire.RotX = 0:End Sub
  602: Sub sw55_Hit:Controller.Switch(55) = 1:sw55wire.RotX = 15:PlaySound "metalhit_thin":End Sub     'leftloop
  603: Sub sw55_UnHit:Controller.Switch(55) = 0:sw55wire.RotX = 0:End Sub
  604: Sub sw86_Hit:Controller.Switch(86) = 1:End Sub         'upperleftflippergate
  605: Sub sw86_UnHit:Controller.Switch(86) = 0:End Sub
  606: Sub sw46_Hit:Controller.Switch(46) = 1:End Sub         'rightrampenter
  607: Sub sw46_UnHit:Controller.Switch(46) = 0:End Sub
  608: Sub sw47_Hit:Controller.Switch(47) = 1:End Sub         'rightrampexit
  609: Sub sw47_UnHit:Controller.Switch(47) = 0:End Sub
  610: Sub sw75_Hit:Controller.Switch(75) = 1: End Sub         'elevatorramp
  611: Sub sw75_UnHit:Controller.Switch(75) = 0:End Sub
  612: Sub sw53_Hit:Controller.Switch(53) = 1:End Sub         'centerramp
  613: Sub sw53_UnHit:Controller.Switch(53) = 0:End Sub
  614: Sub sw51_Hit:Controller.Switch(51) = 1:End Sub         'leftrampenter
  615: Sub sw51_UnHit:Controller.Switch(51) = 0:End Sub
  616: Sub sw52_Hit:Controller.Switch(52) = 1:End Sub         'leftrampexit
  617: Sub sw52_UnHit:Controller.Switch(52) = 0:End Sub
  618: Sub sw61_Hit:Controller.Switch(61) = 1:End Sub         'siderampenter
  619: Sub sw61_UnHit:Controller.Switch(61) = 0:End Sub
  620: Sub sw62_Hit:Controller.Switch(62) = 1:End Sub         'siderampexit
  621: Sub sw62_UnHit:Controller.Switch(62) = 0:End Sub
  624: Sub sw82_Hit:Controller.Switch(82) = 1:sw82wire.RotX = 75:PlaySound "metalhit_thin":End Sub        'Claw SuperJets
  625: Sub sw82_UnHit:Controller.Switch(82) = 0:sw82wire.RotX = 90: End Sub
  627: Sub sw83_Hit:Controller.Switch(83) = 1:sw83wire.RotX = 70:PlaySound "metalhit_thin":End Sub        'Claw PrisonBreak
  628: Sub sw83_UnHit:Controller.Switch(83) = 0:sw83wire.RotX = 90: End Sub
  630: Sub sw84_Hit:Controller.Switch(84) = 1:sw84wire.RotX = 75:PlaySound "metalhit_thin":End Sub        'Claw Freeze
  631: Sub sw84_UnHit:Controller.Switch(84) = 0:sw84wire.RotX = 90: End Sub
  633: Sub sw85_Hit:Controller.Switch(85) = 1:sw85wire.RotX = 75:PlaySound "metalhit_thin":End Sub        'Claw ACMAG
  634: Sub sw85_UnHit:Controller.Switch(85) = 0:sw85wire.RotX = 90: End Sub
  806:     NFadeLm 11,  l11a
  807:     NFadeLm 11,  l11b
  808:     NFadeLm 11,  l11c
  809:     NFadeLm 11,  l11d
  811:     NFadeLm 12,  l12
  812:     NFadeLm 12,  l12b
  813:     NFadeLm 13,  l13
  814:     NFadeLm 13,  l13b
  815:     NFadeLm 14,  l14
  816:     NFadeLm 14,  l14b
  817:     NFadeLm 15,  l15
  818:     NFadeLm 15,  l15b
  819:     NFadeLm 16,  l16
  820:     NFadeLm 16,  l16b
  821:     NFadeLm 17,  l17
  822:     NFadeLm 17,  l17b
  823:     NFadeLm 18,  l18
  824:     NFadeLm 18,  l18b
  826:     NFadeLm 21,  l21
  827:     NFadeLm 21,  l21b
  828:     NFadeLm 22,  l22
  829:     NFadeLm 22,  l22b
  830:     NFadeLm 23,  l23
  831:     NFadeLm 23,  l23b
  832:     NFadeLm 24,  l24
  833:     NFadeLm 24,  l24b
  834:     NFadeLm 25,  l25
  835:     NFadeLm 25,  l25b
  836:     NFadeLm 26,  l26
  837:     NFadeLm 26,  l26b
  838:     NFadeLm 27,  l27
  839:     NFadeLm 27,  l27b
  840:     NFadeLm 28,  l28
  841:     NFadeLm 28,  l28b
  843:     NFadeLm 31,  l31
  844:     NFadeLm 31,  l31b
  845:     NFadeLm 32,  l32
  847:     NFadeLm 33,  l33
  848:     NFadeLm 33,  l33b
  849:     NFadeLm 34,  l34
  850:     NFadeLm 34,  l34b
  851:     NFadeLm 35,  l35
  852:     NFadeLm 35,  l35b
  853:     NFadeLm 36,  l36
  854:     NFadeLm 36,  l36b
  855:     NFadeObjm 36, targetcars, "target1On", "target1"
  856:     NFadeLm 37,  l37
  858:     NFadeLm 38,  l38
  859:     NFadeLm 38,  l38b
  862:     NFadeLm 41,  l41
  863:     NFadeLm 41,  l41b
  864:     NFadeLm 42,  l42
  865:     NFadeLm 42,  l42b
  866:      NFadeLm 43,  l43
  867:      NFadeLm 43,  l43b
  868:     NFadeLm 44,  l44
  869:     NFadeLm 44,  l44b
  871:     NFadeLm 45,  l45
  872:     NFadeLm 45,  l45b
  873:     NFadeLm 46,  l46
  874:     NFadeLm 46,  l46b
  875:     NFadeLm 47,  l47
  876:     NFadeLm 47,  l47b
  878:     NFadeLm 48,  l48
  879:     NFadeLm 48,  l48b
  881:     NFadeLm 51,  l51
  882:     NFadeLm 51,  l51b
  883:     NFadeLm 52,  l52
  884:     NFadeLm 52,  l52b
  885:     NFadeLm 53,  l53
  887:     NFadeLm 54,  l54
  888:     NFadeLm 54,  l54b
  889:     NFadeLm 55,  l55
  890:     NFadeLm 55,  l55b
  891:     NFadeLm 56,  l56
  892:     NFadeLm 56,  l56b
  893:     NFadeLm 57,  l57
  894:     NFadeLm 57,  l57b
  895:     NFadeLm 58,  l58
  896:     NFadeLm 58,  l58b
  899:     Flash 61,    f61
  900:     NFadeLm 61,  l61
  901:     Flash 62,    f62
  902:     NFadeLm 62,  l62
  903:     Flash 63,    f63
  904:     NFadeLm 63,  l63
  905:     Flash 64,    f64
  906:     NFadeLm 64,  l64
  907:     Flash 65,     f65
  908:     NFadeLm 65,  l65
  910:     NFadeLm 66,  l66
  911:     NFadeLm 66,  l66b
  912:     NFadeLm 67,  l67
  913:     NFadeLm 67,  l67b
  914:     NFadeLm 68,  l68
  915:     NFadeLm 68,  l68b
  917:     Flash 71,    f71
  919:     Flash 72,    f72
  921:     Flash 73,    f73
  927:     NFadeLm 76,  l76
  929:     NFadeLm 77,  l77
  931:     NFadeLm 78,  l78
  932:     NFadeLm 78,  l78b
  933:     NFadeObjm 78, targetretina, "target2On", "target2"
  936:     NFadeLm 81,  l81
  937:     NFadeLm 81,  l81b
  938:     NFadeLm 82,  l82
  939:     NFadeLm 82,  l82a
  940:     NFadeLm 82,  l82b
  941:     NFadeLm 82,  l82c
  942:     NFadeLm 82,  l83
  943:     NFadeLm 82,  l83a
  944:     NFadeLm 82,  l83b
  945:     NFadeLm 82,  l83c
  946:     NFadeLm 84,  l84
  947:     NFadeLm 84,  l84b
  948:     NFadeLm 85,  l85
  949:     NFadeLm 85,  l85b
  969: Sub NFadeLm(nr, object) ' used for multiple lights
  976: Sub NFadeLmb(nr, object) ' used for multiple lights with blinking
 1011: Sub NFadeObjm(nr, object, a, b)
 1277:         DiverterR.rotatetoend
 1284:         DiverterR.rotatetostart
 1293: Sub Standup77_Hit: vpmTimer.pulseSw 77:Standup77p.RotX=Standup77p.RotX +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1296: Sub Standup87_Hit: vpmTimer.pulseSw 87:Standup87p.RotX=Standup87p.RotX +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1300: Sub Standup78_Hit: vpmTimer.pulseSw 78:Standup78p.RotZ=Standup78p.RotZ +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1303: Sub Standup38_Hit: vpmTimer.pulseSw 38:Standup38p.RotZ=Standup38p.RotZ +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1306: Sub Standup57_Hit: vpmTimer.pulseSw 57:Standup57p.RotZ=Standup57p.RotZ +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1309: Sub Standup58_Hit: vpmTimer.pulseSw 58:Standup58p.RotZ=Standup58p.RotZ +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1312: Sub Standup56_Hit: vpmTimer.pulseSw 56:Standup56p.RotZ=Standup56p.RotZ +15:Playsound SoundFX("target",DOFContactors):Me.TimerEnabled = 1: End Sub
 1324: Sub leftjetbumper_Hit:vpmTimer.PulseSw 43:Playsound SoundFX ("bumperleft",DOFContactors):Me.TimerEnabled = 1: End Sub
 1326: Sub rightjetbumper_Hit:vpmTimer.PulseSw 45:Playsound SoundFX ("bumperright",DOFContactors):Me.TimerEnabled = 1: End Sub
 1343:     vpmTimer.PulseSw 42
 1363:     vpmTimer.PulseSw 41
 1383:     vpmTimer.PulseSw 44
 1395:     vpmTimer.PulseSw 54
 1399:     vpmTimer.PulseSw 88
 1412: Sub UpdateGI(no, step)
 1421:         Case 1
 1422:             For each xx in GIString2:xx.IntensityScale = gistep * step:next
 1425:         Case 2
 1426:             For each xx in GIString3:xx.IntensityScale = gistep * step:next
 1429:         Case 3
 1430:             For each xx in GIString4:xx.IntensityScale = gistep * step:next
 1432:             For each xx in GIString4: if xx.IntensityScale = 0 then Table1.ColorGradeImage = "grade_1":End if:next
 1434:         Case 4
 1435:             For each xx in GIString5:xx.IntensityScale = gistep * step:next
 1437:             For each xx in GIString5: if xx.IntensityScale = 0 then Table1.ColorGradeImage = "grade_1":End if:next
```
