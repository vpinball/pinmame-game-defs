# The Sopranos — controller bindings in the retained table's embedded script

Every non-comment line of `Sopranos, The (Stern 2005).vbs` (SHA-256 `56262b8bb13d295504abe54f0f586a5e6d288cb4f4b55963889d13c7ba57de08`,
the script embedded in the retained 1.0.2 table and identical to its `extracted-vpxtool/script.vbs`) that names the
controller, a ball stack, a switch handler, a solenoid callback or a lamp fader, quoted verbatim with its line number.
Selected with a fixed pattern over the whole file; whole-line comments are left out, trailing comments kept.

```text
  13: Const cGameName="sopranos",UseSolenoids=1,UseLamps=0,UseGI=0,SSolenoidOn="SolOn",SSolenoidOff="SolOff", SCoin="coin"
  15: LoadVPM "01560000", "sega.VBS", 3.10
  34: SolCallback(1)  = "solTrough"
  35: SolCallback(2)  = "solAutofire"
  36: SolCallback(3)  = "bsTEject.SolOut"
  37: SolCallback(4)  = "SolCenterLock"
  38: SolCallBack(5)  = "SolGateL"
  39: SolCallBack(6)  = "SolGateR"
  40: SolCallback(7)  = "dtSingle.SolHit 1,"
  41: SolCallback(8)  = "SolSafe"
  42: SolCallback(14) = "dtSingle.SolDropUp"
  43: SolCallback(17) = "SolFish"
  44: SolCallback(18) = "Strippers"
  45: SolCallBack(21) = "bsRScoop.SolOut"
  46: SolCallback(22) = "SolBoatLock"
  47: SolCallback(23) = "SolBingLock"
  48: SolCallback(30) = "SolSafeLatch"
  50: SolCallback(19) = "SetLamp 119," 'PF light
  51: SolCallback(20) = "SetLamp 120," 'PF light
  52: SolCallback(25) = "SetLamp 125," 'Fish eyes
  53: SolCallback(26) = "SetLamp 126," 'stage Yellow Dome
  54: SolCallback(27) = "SetLamp 127," 'left sling Yellow Dome
  55: SolCallback(28) = "SetLamp 128," 'right sling Yellow Dome
  56: SolCallback(29) = "SetLamp 129," 'pop bumper Red Dome  X2
  57: SolCallback(31) = "SetLamp 131," 'right spotlight
  58: SolCallback(32) = "SetLamp 132,"
  60:  SolCallback(sLRFlipper) = "SolRFlipper"
  61:  SolCallback(sLLFlipper) = "SolLFlipper"
  63: Sub SolLFlipper(Enabled)
  65:          PlaySound SoundFX("fx_Flipperup",DOFContactors):LeftFlipper.RotateToEnd
  67:          PlaySound SoundFX("fx_Flipperdown",DOFContactors):LeftFlipper.RotateToStart
  71: Sub SolRFlipper(Enabled)
  73:          PlaySound SoundFX("fx_Flipperup",DOFContactors):RightFlipper.RotateToEnd
  75:          PlaySound SoundFX("fx_Flipperdown",DOFContactors):RightFlipper.RotateToStart
  83: Sub solTrough(Enabled)
  86: 		vpmTimer.PulseSw 22
  90: Sub solAutofire(Enabled)
  96: Sub SolCenterLock(Enabled)
  98:         CenterPost.IsDropped = 1
 102: 		CenterPost.IsDropped = 0
 107: Sub SolGateL(Enabled)
 109:         sol5.Open=1
 112:         sol5.Open=0
 116: Sub SolGateR(Enabled)
 118:         sol6.Open=1
 121:         sol6.Open=0
 125: Sub SolFish(Enabled)
 127:         fishf.RotateToEnd
 130:         fishf.RotateToStart
 134: Sub SolBoatLock(Enabled)
 136:         BoatPost.IsDropped = 1 'Drop the post
 140: 		BoatPost.IsDropped = 0
 145: Sub SolBingLock(Enabled)
 147:         BingPost.IsDropped = 1 'Drop the post
 150: 		BingPost.IsDropped = 0
 156: Sub Strippers(Enabled)
 158: 		strippert.Enabled = 1
 160: 		strippert.Enabled = 0
 175: Sub SolSafe(Enabled)
 176:     If Latch = 1 Then
 177: 		prisonstate = false
 181: 		prisonstate = false
 183: 		prisonstate = true
 190: Sub SolSafeLatch(Enabled)
 192:         Latch = 1
 194:         Latch = 0
 202: prisonstate = False
 204: 	If prisonstate = True then 'Opening
 212: 			Controller.Switch(10) = 1
 214: 		sw21.isdropped = true
 215: 		sw24.isdropped = true
 225: 			Controller.Switch(10) = 0
 227: 		sw21.isdropped = false
 228: 		sw24.isdropped = false
 235: set GICallback = GetRef("UpdateGI")
 237: Sub UpdateGI(no, Enabled)
 258: 		.GameName = cGameName
 259: 		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
 261: 		.HandleMechanics=0
 267: 		.Games(cGameName).Settings.Value("sound") = RomSounds
 277:     vpmNudge.TiltSwitch = -7
 282: 		bsTrough.InitSw 0, 14, 13, 12, 11, 0, 0, 0
 283: 		bsTrough.InitKick BallRelease, 90, 7.5
 285: 		bsTrough.Balls = 4
 288:         bsTEject.InitSaucer sw28, 28, 54, 15
 293:         bsRScoop.InitSaucer sw17, 17, 180, 10
 298: 		dtSingle.InitDrop sw26,26
 310: 	If Keycode = StartGameKey Then Controller.Switch(16) = 1
 316: 	If Keycode = StartGameKey Then Controller.Switch(16) = 0
 324:         .InitImpulseP swplunger, IMPowerSetting, IMTime
 326: 		.Switch 16
 334: Sub Drain_Hit:bsTrough.addball me : playsound"drain" : End Sub
 335: Sub sw17_Hit:bsRScoop.AddBall Me : playsound "popper_ball": End Sub
 336: Sub sw28_Hit:bsTEject.AddBall 0 : playsound "popper_ball": End Sub
 339: Sub sw26_Dropped:dtSingle.Hit 1:End Sub
 342: Sub sw19_Hit  : Controller.Switch(19) = 1 : playsound"rollover" : End Sub
 343: Sub sw19_UnHit: Controller.Switch(19) = 0: End Sub
 344: Sub sw20_Hit  : Controller.Switch(20) = 1 : playsound"rollover" : End Sub
 345: Sub sw20_UnHit: Controller.Switch(20) = 0: End Sub
 348: Sub sw31_Hit  : Controller.Switch(31) = 1: End Sub
 349: Sub sw31_UnHit: Controller.Switch(31) = 0: End Sub
 350: Sub sw32_Hit  : Controller.Switch(32) = 1: End Sub
 351: Sub sw32_UnHit: Controller.Switch(32) = 0: End Sub
 354: Sub sw21_Hit  : vpmTimer.PulseSw 21:sw21.TimerEnabled = 1:sw21p.TransX = -4: playsound"Target": End Sub
 356: Sub sw24_Hit  : vpmTimer.PulseSw 24:sw24.TimerEnabled = 1:sw24p.TransX = -4: playsound"Target": End Sub
 360: Sub sw22_Hit:Controller.Switch(22) = 1:End Sub
 361: Sub sw22_UnHit:Controller.Switch(22) = 0:End Sub
 362: Sub sw23_Hit:Controller.Switch(23) = 1:End Sub
 363: Sub sw23_UnHit:Controller.Switch(23) = 0:End Sub
 366: Sub sw9_Hit: vpmTimer.PulseSw 9: End Sub
 367: Sub sw18_Hit: vpmTimer.PulseSw 18: End Sub
 368: Sub sw29_Hit: vpmTimer.PulseSw 29: End Sub
 369: Sub sw33_Hit: vpmTimer.PulseSw 33: End Sub
 372: Sub sw25_Spin:vpmTimer.PulseSw 25 : playsound"fx_spinner" : End Sub
 373: Sub sw27_Spin:vpmTimer.PulseSw 27 : playsound"fx_spinner" : End Sub
 376: Sub sw38_Hit  : Controller.Switch(38) = 1 : playsound"rollover" : End Sub
 377: Sub sw38_UnHit: Controller.Switch(38) = 0: End Sub
 378: Sub sw39_Hit  : Controller.Switch(39) = 1 : playsound"rollover" : End Sub
 379: Sub sw39_UnHit: Controller.Switch(39) = 0: End Sub
 380: Sub sw40_Hit  : Controller.Switch(40) = 1 : playsound"rollover" : End Sub
 381: Sub sw40_UnHit: Controller.Switch(40) = 0: End Sub
 382: Sub sw57_Hit  : Controller.Switch(57) = 1 : playsound"rollover" : End Sub
 383: Sub sw57_UnHit: Controller.Switch(57) = 0: End Sub
 384: Sub sw58_Hit  : Controller.Switch(58) = 1 : playsound"rollover" : End Sub
 385: Sub sw58_UnHit: Controller.Switch(58) = 0: End Sub
 386: Sub sw60_Hit  : Controller.Switch(60) = 1 : playsound"rollover" : End Sub
 387: Sub sw60_UnHit: Controller.Switch(60) = 0: End Sub
 388: Sub sw61_Hit  : Controller.Switch(61) = 1 : playsound"rollover" : End Sub
 389: Sub sw61_UnHit: Controller.Switch(61) = 0: End Sub
 392: Sub sw34_Hit  : vpmTimer.PulseSw 34: End Sub
 393: Sub sw35_Hit  : vpmTimer.PulseSw 35: End Sub
 394: Sub sw36_Hit  : vpmTimer.PulseSw 36: End Sub
 395: Sub sw37_Hit  : vpmTimer.PulseSw 37: End Sub
 398: Sub Bumper1_Hit : vpmTimer.PulseSw(49) : playsound SoundFX("fx_bumper1",DOFContactors): End Sub
 399: Sub Bumper2_Hit : vpmTimer.PulseSw(50) : playsound SoundFX("fx_bumper1",DOFContactors): End Sub
 400: Sub Bumper3_Hit : vpmTimer.PulseSw(51) : playsound SoundFX("fx_bumper1",DOFContactors): End Sub
 429:     chgLamp = Controller.ChangedLamps
 440: 		NFadeL 1, l1
 441: 		NFadeL 2, l2
 442: 		NFadeL 3, l3
 443: 		NFadeL 4, l4
 444: 		NFadeL 5, l5
 445: 		NFadeL 6, l6
 446: 		NFadeL 7, l7
 447: 		NFadeL 8, l8
 448: 		NFadeL 9, l9
 449: 		NFadeL 10, l10
 450: 		NFadeL 11, l11
 451: 		NFadeL 12, l12
 452: 		NFadeL 13, l13
 453: 		NFadeL 14, l14
 454: 		NFadeL 15, l15
 455: 		NFadeL 16, l16
 456: 		NFadeL 17, l17
 457: 		NFadeL 18, l18
 458: 		NFadeL 19, l19
 459: 		NFadeL 20, l20
 460: 		NFadeL 21, l21
 461: 		NFadeL 22, l22
 462: 		NFadeL 23, l23
 463: 		NFadeL 24, l24
 464: 		NFadeL 25, l25
 465: 		NFadeL 26, l26
 466: 		NFadeL 27, l27
 467: 		NFadeL 28, l28
 468: 		NFadeL 29, l29
 469: 		NFadeL 30, l30
 470: 		NFadeL 31, l31
 471: 		NFadeL 32, l32
 472: 		NFadeL 33, l33
 473: 		NFadeL 34, l34
 474: 		NFadeL 35, l35
 475: 		NFadeL 36, l36
 476: 		NFadeL 37, l37
 477: 		NFadeL 38, l38
 478: 		NFadeL 39, l39
 479: 		NFadeL 40, l40
 480: 		NFadeL 41, l41
 481: 		NFadeL 42, l42
 482: 		NFadeL 43, l43
 483: 		NFadeL 44, l44
 484: 		NFadeL 45, l45
 485: 		NFadeL 46, l46
 486: 		NFadeL 47, l47
 487: 		NFadeL 48, l48
 488: 		NFadeL 49, l49
 489: 		NFadeL 50, l50
 490: 		NFadeL 51, l51
 491: 		NFadeL 52, l52
 492: 		NFadeL 53, l53
 493: 		NFadeL 54, l54
 494: 		NFadeL 55, l55
 495: 		NFadeL 56, l56
 496: 		NFadeL 57, l57
 497: 		NFadeL 58, l58
 498: 		NFadeL 59, l59
 499: 		NFadeL 60, l60
 500: 		NFadeL 61, l61
 506: 	Flash 65, l65
 507: 	Flash 66, l66
 508: 	Flash 67, l67
 509: 	Flash 68, l68
 510: 	Flash 69, l69
 511: 	Flash 70, l70
 512: 	Flash 71, l71
 513: 	Flash 72, l72
 516:     NFadeObjm 73, l73, "bulbcover1_yellowOn", "bulbcover1_yellow"
 517: 	Flash 73, F73
 518:     NFadeObjm 74, l74, "bulbcover1_yellowOn", "bulbcover1_yellow"
 519: 	Flash 74, F74
 520:     NFadeObjm 75, l75, "bulbcover1_yellowOn", "bulbcover1_yellow"
 521: 	Flash 75, F75
 522:     NFadeObjm 76, l76, "bulbcover1_yellowOn", "bulbcover1_yellow"
 523: 	Flash 76, F76
 524:     NFadeObjm 77, l77, "bulbcover1_yellowOn", "bulbcover1_yellow"
 525: 	Flash 77, F77
 528: 	NFadeL 78, l78
 534: 	NFadeL 119, L119
 536: 	NFadeL 120, L120
 538: 	Flashm 125, f125a
 539: 	Flash 125, f125b
 541: 	NFadeObjm 126, P126, "dome2_0_yellowOn", "dome2_0_yellow"
 542: 	NFadeL 126, L126
 544: 	NFadeObjm 127, P127, "dome2_0_yellowOn", "dome2_0_yellow"
 545: 	NFadeL 127, f127
 547: 	NFadeObjm 128, P128, "dome2_0_yellowOn", "dome2_0_yellow"
 548: 	NFadeL 128, f128
 550: 	NFadeObjm 129, P129a, "dome2_0_redOn", "dome2_0_red"
 551: 	NFadeObjm 129, P129b, "dome2_0_redOn", "dome2_0_red"
 552: 	NFadeLm 129, L29a
 553: 	NFadeL 129, L29b
 555: 	NFadeL 131, L131
 557: 	NFadeLm 132, L32a
 558: 	NFadeL 132, L32b
 593: Sub NFadeL(nr, object)
 600: Sub NFadeLm(nr, object) ' used for multiple lights
 637: Sub NFadeObjm(nr, object, a, b)
 727: Sub RightSlingShot_Slingshot
 728: 	vpmTimer.PulseSw 62
 729:     PlaySound SoundFX("right_slingshot",DOFContactors), 0,1, 0.05,0.05 '0,1, AudioPan(RightSlingShot), 0.05,0,0,1,AudioFade(RightSlingShot)
 745: Sub LeftSlingShot_Slingshot
 746: 	vpmTimer.PulseSw 59
 747:     PlaySound SoundFX("left_slingshot",DOFContactors), 0,1, -0.05,0.05 '0,1, AudioPan(LeftSlingShot), 0.05,0,0,1,AudioFade(LeftSlingShot)
```
