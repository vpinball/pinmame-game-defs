# Black Rose — retained table script bindings

Quoted from `script.vbs` (SHA-256 `c860e49c2b8be296ce73a64b5e9715245e290b3c2a799f24640234534f799f25`, 4104 lines), the embedded script of the retained VPW v1.4 table extracted with vpxtool. Only the 339 non-comment lines that bind the controller are kept, each with its line number in the file: the ROM and library selection, the Controller settings, the trough's switches and solenoids, every Controller.Switch write and PulseSw, the SolCallback/SolModCallback table and the heads of the subs it names, the cannon, ramp and lockup routines' switch, kick and ball-creation lines, the flasher SetLamp calls, the Lampz and ModLampz light assignments and the G.I. callback. Tabs are shown as four spaces; nothing else is changed.

```vbscript
  134: Const cGameName = "br_l4"    'Black Rose ROM L4
  136: LoadVPM "01120100", "wpc.VBS", 3.26
  142: Const UseSolenoids = 2        'Enable fastflips for williams tables (1 disables)
  143: Const UseLamps = 0            'Use core.vbs script light support instead of the custom lamptimer scripts
  144: Const UseGI = 0                'Use core.vbs GI routine for older machines or machines with no GI
  182:         .GameName = cGameName
  183:         If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
  185:         .HandleKeyboard = 0
  189:         .HandleMechanics = 0
  197:     Set bsTrough = New cvpmTrough
  199:         .size = 3
  200:         .initSwitches Array(16, 17, 18)
  201:         .Initexit BallRelease, 55, 8
  202:         .Balls = 3
  203:         .EntrySw = 15
  211:     vpmNudge.TiltSwitch = 14
  215:     Controller.Switch(22) = 1    'Close coin door - High Power Mode On
  216:     Controller.Switch(63) = 0    'Lockup 1
  217:     Controller.Switch(64) = 0    'Lockup 2
  228: SolCallback(1) =     "RampSwordKicker"
  229: SolCallback(2) =    "bsTroughSolIn"
  230: SolCallback(3) =     "CannonMotor"
  231: SolCallback(4) =    "bsTroughSolOut"
  232: SolCallback(5) =     ""
  233: SolCallback(6) =     ""
  234: SolCallback(7) =     "SolKnocker"
  235: SolCallback(8) =     "FireCannon"
  236: SolCallback(9) =     "PiratesCoveKick"
  237: SolCallback(10) =    "RampUp"
  238: SolCallback(11) =    "RampDown"
  239: SolCallback(12) =     ""
  240: SolCallback(13) =     ""
  241: SolCallback(14) =     ""
  242: SolCallback(15) =     ""
  243: SolCallback(16) =     ""
  244: SolModCallback(17) = "Sol17"                'Left Bottom Flasher        'Top "Black" (Backglass)
  245: SolModCallback(18) = "Sol18"                'Left Top Flasher            'Lady Pirate Belly
  246: SolModCallback(19) = "Sol19"                'Right Bottom Flasher        'Man Pirate Right
  247: SolModCallback(20) = "Sol20"                'Right Top Flasher            'Right top
  248: SolModCallback(21) = "Sol21"                'Right Ramp Flasher            'Bottom "Rose"
  249: SolModCallback(22) = "Sol22"                'Left Ramp Flasher            'Bottom "Black"
  250: SolModCallback(23) = "Sol23"                'Locker Open Flasher        'Skull
  251: SolModCallback(24) = "Sol24"                'Left Sword Flasher            'Bottom of Skull
  252: SolModCallback(25) = "SetLamp 125,"            'Top Popper Flasher
  253: SolModCallback(26) = "SetLamp 126,"            'Cannon Flasher x2
  254: SolModCallback(27) = "Sol27"                'Fire Button Flasher        'Canon Flame
  255: SolModCallback(28) = "Sol28"                'Right Sword Flasher        'Middle Pirate
  257: SolCallback(sLRFlipper) = "SolRFlipper"            'Right Flipper
  258: SolCallback(sLLFlipper) = "SolLFlipper"            'Left Flipper
  259: SolCallback(sURFlipper) = "SolURFlipper"        'Upper Right Flipper
  262: Sub Sol17(Enabled)
  264:         SetLamp 117, 1
  272:         SetLamp 117, 0
  282: Sub Sol18(Enabled)
  284:         SetLamp 118, 1
  292:         SetLamp 118, 0
  302: Sub Sol19(Enabled)
  304:         SetLamp 119, 1
  312:         SetLamp 119, 0
  322: Sub Sol20(Enabled)
  324:         SetLamp 120, 1
  332:         SetLamp 120, 0
  342: Sub Sol21(Enabled)
  344:         SetLamp 121, 1
  352:         SetLamp 121, 0
  362: Sub Sol22(Enabled)
  364:         SetLamp 122, 1
  372:         SetLamp 122, 0
  382: Sub Sol23(Enabled)
  384:         SetLamp 123, 1
  392:         SetLamp 123, 0
  402: Sub Sol24(Enabled)
  404:         SetLamp 124, 1
  412:         SetLamp 124, 0
  422: Sub Sol27(Enabled)
  425:         SetLamp 127, 1
  441:         SetLamp 127, 0
  450: Sub Sol28(Enabled)
  452:         SetLamp 128, 1
  460:         SetLamp 128, 0
  482:     If keycode = PlungerKey Then Controller.Switch(34)=1:Plunger.PullBack: SoundPlungerPull
  531:     If keycode = PlungerKey Then Controller.Switch(34)=0: Plunger.Fire: SoundPlungerReleaseBall
  551:     vpmTimer.PulseSw(38)
  570:     vpmTimer.PulseSw(28)
  594: Sub SolRFlipper(Enabled)
  612: Sub SolLFlipper(Enabled)
  630: Sub SolURFlipper(Enabled)
  632:         RightFlipper1.RotateToEnd
  640:         RightFlipper1.RotateToStart
 1389:     Controller.Switch(25) = 1
 1393:     Controller.Switch(25) = 0
 1401: Sub bsTroughSolIn(Enabled)
 1403:         bsTrough.SolIn Enabled
 1407: Sub bsTroughSolOut(Enabled)
 1410:         bsTrough.SolOut Enabled
 1414: Sub SolKnocker(Enabled)
 1418: Sub RampDown(Enabled)
 1421:         Controller.Switch(54) = 1
 1422:         DaveyRampDown.Collidable = 1
 1423:         DaveyRampUp.Collidable = 0
 1429: Sub RampUp(Enabled)
 1432:         Controller.Switch(54) = 0
 1433:         DaveyRampDown.Collidable = 0
 1434:         DaveyRampUp.Collidable = 1
 1445:     If Controller.Switch(54) = True Then 'Down
 1465: Sub RampSwordKicker (Enabled)
 1466:     If (Enabled and Controller.Switch(55) = True) Then
 1468:         vpmCreateBall KickerSW55Upper
 1472:         KickerSW55Upper.kick 180,5
 1473:         Controller.Switch(55)=0
 1478: Sub FireCannon(Enabled)
 1479:     if Enabled and Controller.Switch(35) = True then
 1483:         vpmCreateBall CannonKicker
 1484:         cannonKicker.kick -1*discangle, 52
 1485:         Controller.Switch(35) = 0
 1491: Sub CannonMotor(Enabled)
 1493:         DiscTimer.Enabled = 1
 1496:         DiscTimer.Enabled = 0
 1515: Sub DiscTimer_Timer
 1532:     If DiscAngle => 45 then Dir = -1
 1533:     If DiscAngle =< -45 then Dir = 1
 1541: Sub Sw26_Hit:    Controller.Switch(26)=1: End Sub
 1542: Sub Sw26_UnHit:    Controller.Switch(26)=0: End Sub
 1543: Sub Sw27_Hit:    Controller.Switch(27)=1: End Sub
 1544: Sub Sw27_UnHit:    Controller.Switch(27)=0: End Sub
 1545: Sub Sw36_Hit:    Controller.Switch(36)=1: End Sub
 1546: Sub Sw36_UnHit:    Controller.Switch(36)=0: End Sub
 1547: Sub Sw37_Hit:    Controller.Switch(37)=1: End Sub
 1548: Sub Sw37_UnHit:    Controller.Switch(37)=0: End Sub
 1549: Sub Sw45_Hit:    Controller.Switch(45)=1: End Sub
 1550: Sub Sw45_UnHit:    Controller.Switch(45)=0: End Sub
 1551: Sub Sw56_Hit:    Controller.Switch(56)=1: End Sub
 1552: Sub Sw56_UnHit:    Controller.Switch(56)=0: End Sub
 1553: Sub Sw57_Hit:    Controller.Switch(57)=1: End Sub
 1554: Sub Sw57_UnHit:    Controller.Switch(57)=0: End Sub
 1555: Sub Sw58_Hit:    Controller.Switch(58)=1: End Sub
 1556: Sub Sw58_UnHit:    Controller.Switch(58)=0: End Sub
 1557: Sub Sw62_Hit:    Controller.Switch(62)=1: End Sub
 1558: Sub Sw62_UnHit:    Controller.Switch(62)=0: End Sub
 1561: Sub Bumper1_Hit:    vpmTimer.PulseSw(46): RandomSoundBumperTop Bumper1 : End Sub
 1562: Sub Bumper2_Hit:    vpmTimer.PulseSw(47): RandomSoundBumperMiddle Bumper2 : End Sub
 1563: Sub BumperSw48_Hit:    vpmTimer.PulseSw(48): RandomSoundBumperBottom BumperSw48: Dir=-1: BumperSw48.TimerEnabled=1: BumperSw48.TimerInterval=10: End Sub
 1572: Sub Sw31_Hit:    vpmTimer.PulseSw(31): End Sub
 1573: Sub Sw32_Hit:    vpmTimer.PulseSw(32): End Sub
 1574: Sub Sw33_Hit:    vpmTimer.PulseSw(33): End Sub
 1575: Sub Sw41_Hit:    vpmTimer.PulseSw(41): End Sub
 1576: Sub Sw42_Hit:    vpmTimer.PulseSw(42): End Sub
 1577: Sub Sw43_Hit:    vpmTimer.PulseSw(43): End Sub
 1578: Sub Sw51_Hit:    vpmTimer.PulseSw(51): End Sub
 1579: Sub Sw52_Hit:    vpmTimer.PulseSw(52): End Sub
 1580: Sub Sw53_Hit:    vpmTimer.PulseSw(53): End Sub
 1581: Sub Sw65_Hit:    vpmTimer.PulseSw(65): End Sub
 1584: Sub GateSw44_Hit:    vpmTimer.PulseSw(44): End Sub
 1585: Sub GateSw71_Hit:    vpmTimer.PulseSw(71): End Sub
 1586: Sub GateSw72_Hit:    vpmTimer.PulseSw(72): End Sub
 1587: Sub GateSw76_Hit:    vpmTimer.PulseSw(76): End Sub
 1590: Sub KickerSw63_Hit: Controller.Switch(63) = 1: KickerSw64.Enabled=1: End Sub
 1591: Sub KickerSw64_Hit: Controller.Switch(64) = 1: KickerSw64.Enabled=0: End Sub
 1593: Sub PiratesCoveKick (Enabled)
 1598:         If (Controller.Switch(64) = True) Then
 1600:             KickerSW64.kick 345, 40: SoundSaucerKick 1,Kickersw64
 1601:             Controller.Switch(64) = 0
 1603:         If (Controller.Switch (63) = True) Then
 1605:             KickerSW63.kick 345, 40: SoundSaucerKick 1,Kickersw64
 1606:             Controller.Switch(63) = 0
 1632:     vpmTimer.PulseSwitch 61, 0, ""
 1636:     vpmTimer.PulseSwitch 66, 0, ""
 1637:     Controller.Switch(35) = 1
 1645:     Controller.Switch(55) = 1
 2817:     Lampz.MassAssign(11)= l11
 2818:     Lampz.MassAssign(11)= h11
 2820:     Lampz.MassAssign(11)= l11a
 2821:     Lampz.MassAssign(11)= h11a
 2823:     Lampz.MassAssign(12)= l12
 2824:     Lampz.MassAssign(12)= h12
 2826:     Lampz.MassAssign(13)= l13
 2827:     Lampz.MassAssign(13)= h13
 2829:     Lampz.MassAssign(14)= l14
 2830:     Lampz.MassAssign(14)= h14
 2832:     Lampz.MassAssign(15)= l15
 2833:     Lampz.MassAssign(15)= h15
 2835:     Lampz.MassAssign(16)= l16
 2836:     Lampz.MassAssign(16)= h16
 2838:     Lampz.MassAssign(17)= l17
 2839:     Lampz.MassAssign(17)= h17
 2841:     Lampz.MassAssign(18)= l18
 2842:     Lampz.MassAssign(18)= h18
 2846:     Lampz.MassAssign(21)= l21
 2847:     Lampz.MassAssign(21)= h21
 2848:     Lampz.MassAssign(22)= l22
 2849:     Lampz.MassAssign(22)= h22
 2850:     Lampz.MassAssign(23)= l23
 2851:     Lampz.MassAssign(23)= h23
 2852:     Lampz.MassAssign(24)= l24
 2853:     Lampz.MassAssign(24)= h24
 2854:     Lampz.MassAssign(25)= l25
 2855:     Lampz.MassAssign(25)= h25
 2856:     Lampz.MassAssign(26)= l26
 2857:     Lampz.MassAssign(26)= h26
 2858:     Lampz.MassAssign(27)= l27
 2859:     Lampz.MassAssign(27)= h27
 2860:     Lampz.MassAssign(28)= l28
 2861:     Lampz.MassAssign(28)= h28
 2863:     Lampz.MassAssign(31)= l31
 2864:     Lampz.MassAssign(31)= h31
 2866:     Lampz.MassAssign(32)= l32
 2867:     Lampz.MassAssign(32)= h32
 2869:     Lampz.MassAssign(33)= l33
 2870:     Lampz.MassAssign(33)= h33
 2872:     Lampz.MassAssign(34)= l34
 2873:     Lampz.MassAssign(34)= h34
 2875:     Lampz.MassAssign(35)= l35
 2876:     Lampz.MassAssign(35)= h35
 2878:     Lampz.MassAssign(36)= l36
 2879:     Lampz.MassAssign(36)= h36
 2881:     Lampz.MassAssign(37)= l37
 2882:     Lampz.MassAssign(37)= h37
 2884:     Lampz.MassAssign(38)= l38
 2885:     Lampz.MassAssign(38)= h38
 2888:     Lampz.MassAssign(41)= l41
 2889:     Lampz.MassAssign(41)= h41
 2891:     Lampz.MassAssign(42)= l42
 2892:     Lampz.MassAssign(42)= h42
 2894:     Lampz.MassAssign(43)= l43
 2895:     Lampz.MassAssign(43)= h43
 2897:     Lampz.MassAssign(44)= l44
 2898:     Lampz.MassAssign(44)= h44
 2900:     Lampz.MassAssign(45)= l45
 2901:     Lampz.MassAssign(45)= h45
 2903:     Lampz.MassAssign(46)= l46
 2904:     Lampz.MassAssign(46)= h46
 2906:     Lampz.MassAssign(47)= l47
 2907:     Lampz.MassAssign(47)= h47
 2909:     Lampz.MassAssign(48)= l48
 2910:     Lampz.MassAssign(48)= h48
 2913:     Lampz.MassAssign(51)= l51
 2914:     Lampz.MassAssign(51)= h51
 2916:     Lampz.MassAssign(52)= l52
 2917:     Lampz.MassAssign(52)= h52
 2919:     Lampz.MassAssign(53)= l53
 2920:     Lampz.MassAssign(53)= h53
 2922:     Lampz.MassAssign(54)= l54
 2923:     Lampz.MassAssign(54)= h54
 2925:     Lampz.MassAssign(55)= l55
 2926:     Lampz.MassAssign(55)= h55
 2928:     Lampz.MassAssign(56)= l56
 2929:     Lampz.MassAssign(56)= h56
 2931:     Lampz.MassAssign(57)= l57
 2932:     Lampz.MassAssign(57)= h57
 2934:     Lampz.MassAssign(58)= l58
 2935:     Lampz.MassAssign(58)= h58
 2938:     Lampz.MassAssign(61)= l61
 2939:     Lampz.MassAssign(61)= h61
 2941:     Lampz.MassAssign(62)= l62
 2942:     Lampz.MassAssign(62)= h62
 2944:     Lampz.MassAssign(63)= l63
 2945:     Lampz.MassAssign(63)= h63
 2947:     Lampz.MassAssign(64)= l64
 2948:     Lampz.MassAssign(64)= h64
 2950:     Lampz.MassAssign(65)= l65
 2951:     Lampz.MassAssign(65)= h65
 2953:     Lampz.MassAssign(66)= l66
 2954:     Lampz.MassAssign(66)= h66
 2956:     Lampz.MassAssign(67)= l67
 2957:     Lampz.MassAssign(67)= h67
 2959:     Lampz.MassAssign(68)= l68
 2960:     Lampz.MassAssign(68)= h68
 2963:     Lampz.MassAssign(71)= l71
 2964:     Lampz.MassAssign(71)= h71
 2966:     Lampz.MassAssign(72)= l72
 2967:     Lampz.MassAssign(72)= h72
 2969:     Lampz.MassAssign(73)= l73
 2970:     Lampz.MassAssign(73)= h73
 2972:     Lampz.MassAssign(74)= l74
 2973:     Lampz.MassAssign(74)= h74
 2975:     Lampz.MassAssign(75)= l75
 2976:     Lampz.MassAssign(75)= h75
 2978:     Lampz.MassAssign(76)= l76
 2979:     Lampz.MassAssign(76)= h76
 2981:     Lampz.MassAssign(77)= l77
 2982:     Lampz.MassAssign(77)= h77
 2987:     Lampz.MassAssign(81)= l81
 2988:     Lampz.MassAssign(81)= h81
 2990:     Lampz.MassAssign(82)= l82
 2991:     Lampz.MassAssign(82)= h82
 2993:     Lampz.MassAssign(83)= l83
 2994:     Lampz.MassAssign(83)= h83
 2996:     Lampz.MassAssign(84)= l84
 2997:     Lampz.MassAssign(84)= h84
 2999:     Lampz.MassAssign(85)= l85
 3000:     Lampz.MassAssign(85)= h85
 3002:     Lampz.MassAssign(86)= l86                            'Jack
 3003:     Lampz.MassAssign(86)= h86
 3005:     Lampz.MassAssign(86)= l86a                            'Pot
 3006:     Lampz.MassAssign(86)= h86a
 3018:     Lampz.MassAssign(117)= f17a
 3019:     Lampz.MassAssign(117)= f17b
 3022:     Lampz.MassAssign(118)= f18a
 3023:     Lampz.MassAssign(118)= f18b
 3024:     Lampz.MassAssign(118)= f18c
 3026:     Lampz.MassAssign(119)= f19a
 3027:     Lampz.MassAssign(119)= f19b
 3028:     Lampz.MassAssign(119)= f19c        'Cannon
 3030:     Lampz.MassAssign(120)= f20a
 3031:     Lampz.MassAssign(120)= f20b
 3032:     Lampz.MassAssign(120)= f20c
 3034:     Lampz.MassAssign(121)= f21a
 3035:     Lampz.MassAssign(121)= f21b
 3036:     Lampz.MassAssign(121)= f21c
 3038:     Lampz.MassAssign(122)= f22a
 3039:     Lampz.MassAssign(122)= f22b
 3040:     Lampz.MassAssign(122)= f22c
 3041:     Lampz.MassAssign(122)= f22e        'Cannon
 3043:     Lampz.MassAssign(123)= f23
 3044:     Lampz.MassAssign(123)= fh23
 3047:     Lampz.MassAssign(124)= f24
 3048:     Lampz.MassAssign(124)= fh24
 3051:     Lampz.MassAssign(125)= f25a
 3052:     Lampz.MassAssign(125)= f25b
 3053:     Lampz.MassAssign(125)= f25c
 3054:     Lampz.MassAssign(125)= f25d
 3055:     Lampz.MassAssign(125)= f25e
 3056:     Lampz.MassAssign(125)= f25f
 3058:     Lampz.MassAssign(126)= f26a
 3059:     Lampz.MassAssign(126)= f26b
 3060:     Lampz.MassAssign(126)= f26c
 3061:     Lampz.MassAssign(126)= f26d
 3062:     Lampz.MassAssign(126)= f26e        'Cannon
 3064:     Lampz.MassAssign(127)= f27a
 3065:     Lampz.MassAssign(127)= f27b
 3066:     Lampz.MassAssign(127)= f27c        'Cannon
 3068:     Lampz.MassAssign(128)= f28
 3069:     Lampz.MassAssign(128)= fh28
 3082:     ModLampz.MassAssign(0)= ColToArray(GIstring1)            ' Jets & Back Ramp
 3083:     ModLampz.MassAssign(1)= ColToArray(GIstring2)             ' Top Playfield
 3084:     ModLampz.MassAssign(2)= ColToArray(GIstring3)             ' Bottom Playfield
 3085:     ModLampz.MassAssign(3)= ColToArray(GIstring4)             ' Backglass Gi String 1
 3086:     ModLampz.MassAssign(4)= ColToArray(GIstring5)            ' Backglass GI String 2
 3102: Set GICallback2 = GetRef("SetGI")
```
