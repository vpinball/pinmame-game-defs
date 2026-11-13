# No Fear: Dangerous Sports — retained known-working table script, runtime contract

Source: the script embedded in the retained table `No Fear (Williams 1995) VPW v1.1.1.vpx` (table_version 1.1 by VPW, saved 2026-01-25; table SHA-256 `3523285c6829c44068f8d81c5d886af8ab89156ed0e5aac18fbcfbf7a918d14f`), extracted with vpxtool 0.33.3 as `script.vbs` (4135 lines, SHA-256 `580749d770efe2e887fd92f7d05b3afa7f848f64e9f2736204986353b00817c5`). The blocks below quote its lines verbatim with their 1-based line numbers (CRLF line ends and trailing whitespace dropped, leading tabs kept); lines between the blocks are sound, shadow, physics-correction and option code the definition does not rely on. The script itself is not redistributed.

## Controller options and ROM

Lines 100-105:

```
 100  ' Standard Options
 101  Const UseVPMModSol = 2
 102  Const UseSolenoids = 2, UseLamps = 1, UseSync = 0, HandleMech = 0, SSolenoidOn = "", SSolenoidOff = "", SCoin = ""
 103
 104  ' Rom Name
 105  Const cGameName = "nf_23x"
```

## Controller start-up, nudge, lamp map and trough balls

Lines 299-378:

```
 299  Sub Table1_Init
 300  	vpmInit Me
 301  	With Controller
 302  		.GameName = cGameName
 303  		If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
 304  		.SplashInfoLine = "No Fear - Dangerous Sports (Williams 1995)" & vbNewLine & "VPW"
 305  		.HandleKeyboard = 0
 306  		.ShowTitle = 0
 307  		.ShowDMDOnly = 1
 308  		.ShowFrame = 0
 309  		.HandleMechanics = 0
 310  		.Hidden = DesktopMode	'Hide VPM DMD in Desktop Mode
 311  		On Error Resume Next
 312  		.Run GetPlayerHWnd
 313  		If Err Then MsgBox Err.Description
 314  		On Error Goto 0
 315  		.Switch(22) = 1			'close coin door
 316  		.Switch(24) = 1			'always closed
 317  	End With
 318
 319      ' Main Timer init
 320      PinMAMETimer.Interval = PinMAMEInterval
 321      PinMAMETimer.Enabled = 1
 322
 323      ' Nudging
 324      vpmNudge.TiltSwitch = 14
 325      vpmNudge.Sensitivity = 5
 326      vpmNudge.TiltObj = Array(sw27, sw28)
 327
 328  	vpmMapLights AllLamps
 329
 330      '************  Trough	**************************
 331
 332  	Set NFBall1 = sw32.CreateSizedballWithMass(Ballsize/2,Ballmass)
 333  	Set NFBall2 = sw33.CreateSizedballWithMass(Ballsize/2,Ballmass)
 334  	Set NFBall3 = sw34.CreateSizedballWithMass(Ballsize/2,Ballmass)
 335  	Set NFBall4 = sw35.CreateSizedballWithMass(Ballsize/2,Ballmass)
 336
 337  	gBOT = Array(NFBall1,NFBall2,NFBall3,NFBall4)
 338
 339  	Controller.Switch(32) = 1
 340  	Controller.Switch(33) = 1
 341  	Controller.Switch(34) = 1
 342  	Controller.Switch(35) = 1
 343
 344  	'Add balls to shadow dictionary
 345  	Dim xx: For Each xx in gBOT
 346  		bsDict.Add xx.ID, bsNone
 347  	Next
 348
 349  	' Auto Plunger
 350  	Set plungerIM = New cvpmImpulseP
 351  	With plungerIM
 352  		.InitImpulseP sw15, 65, 0.75
 353  		.Switch 15
 354  		.Random 0.05
 355  		.CreateEvents "plungerIM"
 356  	End With
 357
 358  	' Kickback
 359  	Set kickbackIM = New cvpmImpulseP
 360  	With kickbackIM
 361  		.InitImpulseP sw25, 65, 0.5
 362  		.Random 0.05
 363  	End With
 364
 365  	'Initialize slings
 366  	RStep = 0:sw28.Timerenabled=True
 367  	LStep = 0:sw27.Timerenabled=True
 368
 369  	f121.State = 0
 370  	f128.State = 0
 371
 372  	Select Case StrongerMagnets
 373  		Case 0
 374  			MagnetSpeed = 20
 375  		Case 1
 376  			MagnetSpeed = 30
 377  	End Select
 378
```

## Cabinet keys

Lines 425-451:

```
 425  Sub Table1_KeyDown(ByVal Keycode)
 426  	If keycode = keyFront Then Controller.Switch(23) = 1		'buy-in
 427  	If Keycode = PlungerKey Then Controller.Switch(11) = 1 : LaunchButton.TransX = 5 : Flasher1.Y = 2317
 428  	If keycode = LeftFlipperKey Then FlipperActivate LeftFlipper, LFPress : VR_CabFlipperLeft.TransX = 5
 429  	If keycode = RightFlipperKey Then FlipperActivate RightFlipper, RFPress : VR_CabFlipperRight.TransX = -5
 430  	If keycode = LeftTiltKey Then Nudge 90, 1 : SoundNudgeLeft()
 431  	If keycode = RightTiltKey Then Nudge 270, 1 : SoundNudgeRight()
 432  	If keycode = CenterTiltKey Then Nudge 0, 1 : SoundNudgeCenter()
 433  	If keycode = StartGameKey then soundStartButton()
 434  	If keycode = keyInsertCoin1 or keycode = keyInsertCoin2 or keycode = keyInsertCoin3 or keycode = keyInsertCoin4 Then
 435  		Select Case Int(rnd*3)
 436  			Case 0: PlaySound ("Coin_In_1"), 0, CoinSoundLevel, 0, 0.25
 437  			Case 1: PlaySound ("Coin_In_2"), 0, CoinSoundLevel, 0, 0.25
 438  			Case 2: PlaySound ("Coin_In_3"), 0, CoinSoundLevel, 0, 0.25
 439  		End Select
 440  	End If
 441  	If Keycode = LockBarKey Then Controller.Switch(11) = 1
 442      If vpmKeyDown(keycode) Then Exit Sub
 443  End Sub
 444
 445  Sub Table1_KeyUp(ByVal Keycode)
 446  	If keycode = keyFront Then Controller.Switch(23) = 0		'buy-in
 447  	If keycode = LeftFlipperKey Then FlipperDeActivate LeftFlipper, LFPress : VR_CabFlipperLeft.TransX = 0
 448  	If keycode = RightFlipperKey Then FlipperDeActivate RightFlipper, RFPress : VR_CabFlipperRight.TransX = 0
 449  	If KeyCode = PlungerKey Then Controller.Switch(11) = 0 : LaunchButton.TransX = 0 : Flasher1.y = 2322
 450  	If Keycode = LockBarKey Then Controller.Switch(11) = 0
 451  	If vpmKeyUp(keycode) Then Exit Sub
```

## Ramp magnets

Lines 453-506:

```
 453
 454
 455  '*****************************************
 456  '      		MAGNETS
 457  '*****************************************
 458
 459  Dim MagnetBall
 460  Dim MagnetSnd: MagnetSnd = True
 461  Dim LmagEnabled: LmagEnabled = False
 462  Dim CmagEnabled: CmagEnabled = False
 463  Dim RmagEnabled: RmagEnabled = False
 464
 465  Sub CalmDown_hit: Activeball.VelY = MagnetSpeed-5 : End Sub
 466
 467  Sub Lmag(Enabled)
 468  	LmagEnabled = Enabled
 469  	If Enabled Then
 470  		If LeftMagnet.BallCntOver > 0 Then
 471  			If MagnetBall.VelX > 0 Then MagnetBall.VelX = MagnetSpeed
 472  		End If
 473  '	Debug.print "lmag enabled"
 474  	End If
 475  End Sub
 476
 477  Sub Cmag(Enabled)
 478  	CmagEnabled = Enabled
 479  	If Enabled Then
 480  		If CenterMagnet.BallCntOver > 0 Then
 481  			If MagnetBall.VelX > 0 Then MagnetBall.VelX = MagnetSpeed
 482  		End If
 483  '	Debug.print "cmag enabled"
 484  	End If
 485  End Sub
 486
 487  Sub Rmag(Enabled)
 488  	RmagEnabled = Enabled
 489  	If Enabled Then
 490  		If RightMagnet.BallCntOver > 0 Then
 491  			If MagnetBall.VelX > 0 Then MagnetBall.VelX = MagnetSpeed
 492  		End If
 493  '	Debug.print "rmag enabled"
 494  	End If
 495  End Sub
 496
 497  'Magnets
 498  Sub LeftMagnet_hit:   Set MagnetBall = activeball: End Sub
 499  Sub CenterMagnet_hit: Set MagnetBall = activeball: End Sub
 500  Sub RightMagnet_hit:  Set MagnetBall = activeball: End Sub
 501
 502  Sub RightMagnet_unhit
 503  	'Stop/slow the ball if center magnet enabled
 504  	If CmagEnabled And Not RmagEnabled And Activeball.velx > 0 Then MagnetBall.VelX = 0
 505  End Sub
 506
```

## Solenoid callback table and drop target coils

Lines 508-558:

```
 508  '      		Solenoids Mapping
 509  '*****************************************
 510  SolCallback(1)= "SubwayVUK" 					'1-Right Popper
 511  SolCallback(2)= "SolAutoPlungerIM"				'2-AutoPlunger
 512  SolCallback(3)= "Rmag"							'3-Right Magnet
 513  SolCallback(4)= "SolKickbackIM"					'4-KickBack
 514  SolCallback(5)= "Cmag"							'5-Center Magnet
 515  SolCallback(6)= "Lmag"							'6-Left Magnet
 516  SolCallback(7)= "SolKnocker"					'7-Knocker
 517  SolCallback(8)= "DropTargetDOWN" 				'8-Drop Target Down
 518  'SolCallback(9)= ""								'9-N.U.
 519  'SolCallback(10)= ""							'10-Right Sling
 520  'SolCallback(11)= ""							'11-Left Sling
 521  SolCallback(12)= "DropTargetUP"					'12-Drop Target Up
 522  'SolCallback(13)= ""							'13-N.U.
 523  SolCallback(14)= "ReleaseBall"					'14-Trough
 524  SolCallback(15)= "LeftKicker"					'15-Left Eject
 525  SolCallback(16)= "SolMouth"						'16-Skull Mouth
 526
 527  SolModCallback(17)= "FlashMod117"			'17-Flasher: Flipper Return (x2)
 528  SolModCallback(18)= "FlashMod118"			'18-Flasher: Spinner
 529  SolModCallback(19)= "FlashMod119"			'19-Flasher: No Fear (x2)
 530  SolModCallback(20)= "FlashMod120"			'20-Flasher: Right Ramp
 531  SolModCallback(21)= "FlashMod121"			'21-Flasher: Skull (x2)
 532  SolModCallback(22)= "FlashMod122"			'22-Flasher: BKBok EXPL
 533  SolModCallback(23)= "FlashMod123"			'23-Flasher: Left Ramp
 534  SolModCallback(24)= "FlashMod124"			'24-Flasher: Top Left
 535  SolModCallback(25)= "FlashMod125"			'25-Flasher: AutoFire (x2)
 536  SolModCallback(26)= "FlashMod126"			'26-Flasher: BKBok L Top
 537  SolModCallback(27)= "FlashMod127"			'27-Flasher: BKBok R Top
 538  SolModCallback(28)= "FlashMod128"			'28-Flasher: Right Popper
 539
 540  Sub DropTargetUP(enabled) ' Drop Target 51 Solenoid
 541  	If enabled Then
 542  		RandomSoundDropTargetReset BM_sw51p
 543  		DTRaise 51
 544  	End If
 545  End Sub
 546
 547  Sub DropTargetDOWN(enabled) ' Drop Target 51 Solenoid
 548  	If enabled Then
 549  		SoundDropTargetDrop BM_sw51p
 550  		DTDrop 51
 551  	End If
 552  End Sub
 553
 554  '*************************************************************
 555  'PWM Flasher Stuff
 556  '*************************************************************
 557
 558  f117_mayo1.intensityscale = 0
```

## Flasher callbacks

Lines 560-641:

```
 560  Sub FlashMod117(pwm)
 561  '	If DebugFlashers Then Debug.print "FlashMod117 level=" & pwm
 562  	f117a.State = pwm
 563  	f117b.State = pwm
 564  	f117_mayo1.intensityscale = pwm * 0.3
 565  	f117_mayo2.intensityscale = pwm * 0.3
 566  End Sub
 567
 568  dim DebugFlashers : DebugFlashers = true
 569  f118_mayo.intensityscale = 0
 570  Sub FlashMod118(pwm)
 571  '	If DebugFlashers Then Debug.print "FlashMod118 level=" & pwm
 572  	f118.State = pwm
 573  	f118_mayo.intensityscale = pwm * 1.5
 574  End Sub
 575
 576  f119_mayo.intensityscale = 0
 577  Sub FlashMod119(pwm)
 578  '	If DebugFlashers Then Debug.print "FlashMod119 level=" & pwm
 579  	f119.State = pwm
 580  	f119_mayo.intensityscale = pwm
 581  End Sub
 582
 583  Sub FlashMod120(pwm)
 584  '	If DebugFlashers Then Debug.print "FlashMod120 level=" & pwm
 585  	f120.State = pwm
 586  End Sub
 587
 588  f121_mayo.intensityscale = 0
 589  Sub FlashMod121(pwm)
 590  '	If DebugFlashers Then Debug.print "FlashMod121 level=" & pwm
 591  	f121.State = pwm
 592  	f121_mayo.intensityscale = pwm
 593  End Sub
 594
 595  Sub FlashMod122(pwm)
 596  '	If DebugFlashers Then Debug.print "FlashMod122 level=" & pwm
 597  	f122.State = pwm
 598  End Sub
 599
 600  Sub FlashMod123(pwm)
 601  '	If DebugFlashers Then Debug.print "FlashMod123 level=" & pwm
 602  	f123.State = pwm
 603  End Sub
 604
 605  f124_mayo.intensityscale = 0
 606  Sub FlashMod124(pwm)
 607  '	If DebugFlashers Then Debug.print "FlashMod124 level=" & pwm
 608  	f124.State = pwm
 609  	f124_mayo.intensityscale = pwm
 610  End Sub
 611
 612  f125_mayo001.intensityscale = 0
 613  f125_mayo002.intensityscale = 0
 614  Sub FlashMod125(pwm)
 615  '	If DebugFlashers Then Debug.print "FlashMod125 level=" & pwm
 616  	f125a.State = pwm
 617  	f125b.State = pwm
 618  	f125_mayo001.intensityscale = pwm * 0.5
 619  	f125_mayo002.intensityscale = pwm * 0.5
 620  End Sub
 621
 622  Sub FlashMod126(pwm)
 623  '	If DebugFlashers Then Debug.print "FlashMod126 level=" & pwm
 624  	f126.State = pwm
 625  End Sub
 626
 627  Sub FlashMod127(pwm)
 628  '	If DebugFlashers Then Debug.print "FlashMod127 level=" & pwm
 629  	f127.State = pwm
 630  End Sub
 631
 632  Sub FlashMod128(pwm)
 633  '	If DebugFlashers Then Debug.print "FlashMod128 level=" & pwm
 634  	f128.State = pwm
 635  End Sub
 636
 637
 638  '******************************************
 639  '				GI
 640  '******************************************
 641  'updategi 0,0 : updategi 1,0 : updategi 2,0
```

## General illumination

Lines 643-656:

```
 643  Set GiCallBack2 = GetRef("UpdateGi")
 644
 645  Sub UpdateGI(no, level) ' GI Strings with 9 intensity levels (0 to 8)
 646  	Dim xx
 647  	Select Case no
 648  		Case 0 : for each xx in GI_Top : xx.State = level : Next
 649  		Case 1 : for each xx in GI_Right : xx.State = level : Next
 650  		Case 2 : for each xx in GI_Left : xx.State = level : Next
 651  '		Case 3 : l143a.State = level
 652  	End Select
 653      'Debug.print "GI: " & no & "=>" & level
 654  End Sub
 655
 656  '******************************************
```

## Flipper callbacks

Lines 658-719:

```
 658  '******************************************
 659
 660  SolCallback(sLRFlipper) = "SolRFlipper"
 661  SolCallback(sLLFlipper) = "SolLFlipper"
 662  SolCallback(sURFlipper) = "SolURFlipper"
 663
 664  Const ReflipAngle = 20
 665
 666  Sub SolLFlipper(Enabled)
 667  	If Enabled Then
 668  		LF.Fire  'LeftFlipper.RotateToEnd
 669  		If leftflipper.currentangle < leftflipper.endangle + ReflipAngle Then
 670  			RandomSoundReflipUpLeft LeftFlipper
 671  		Else
 672  			SoundFlipperUpAttackLeft LeftFlipper
 673  			RandomSoundFlipperUpLeft LeftFlipper
 674  		End If
 675  	Else
 676  		LeftFlipper.RotateToStart
 677  		If LeftFlipper.currentangle < LeftFlipper.startAngle - 5 Then
 678  			RandomSoundFlipperDownLeft LeftFlipper
 679  		End If
 680  		FlipperLeftHitParm = FlipperUpSoundLevel
 681      End If
 682   End Sub
 683
 684  Sub SolRFlipper(Enabled)
 685  	If Enabled Then
 686  		RF.Fire'RightFlipper.RotateToEnd
 687  		If rightflipper.currentangle > rightflipper.endangle - ReflipAngle Then
 688  			RandomSoundReflipUpRight RightFlipper
 689  		Else
 690  			SoundFlipperUpAttackRight RightFlipper
 691  			RandomSoundFlipperUpRight RightFlipper
 692  		End If
 693  	Else
 694  		RightFlipper.RotateToStart
 695  		If RightFlipper.currentangle > RightFlipper.startAngle + 5 Then
 696  			RandomSoundFlipperDownRight RightFlipper
 697  		End If
 698  		FlipperRightHitParm = FlipperUpSoundLevel
 699  	End If
 700  End Sub
 701
 702  Sub SolURFlipper(Enabled)
 703  	If Enabled Then
 704  		RightUpFlipper.RotateToEnd
 705  		If rightUpflipper.currentangle > rightupflipper.endangle - ReflipAngle Then
 706  			RandomSoundReflipUpRight RightupFlipper
 707  		Else
 708  			SoundFlipperUpAttackRight RightUpFlipper
 709  			RandomSoundFlipperUpRight RightUpFlipper
 710  		End If
 711  	Else
 712  		RightUpFlipper.RotateToStart
 713  		If RightUpFlipper.currentangle > RightUpFlipper.startAngle + 5 Then
 714  			RandomSoundFlipperDownRight RightUpFlipper
 715  		End If
 716  		FlipperRightHitParm = FlipperUpSoundLevel
 717  	End If
 718  End Sub
 719
```

## Auto plunger, kickback, skull mouth and knocker

Lines 753-811:

```
 753  Sub SolAutoPlungerIM(Enabled)
 754  	If Enabled Then
 755  		PlungerIM.AutoFire
 756  		SoundImpulsePlunger
 757  	End If
 758  End Sub
 759
 760  '************************************************************************
 761  '						 KICKBACK
 762  '************************************************************************
 763  Sub SolKickbackIM(Enabled)
 764  	If Enabled Then
 765  		KickBackIM.AutoFire
 766  		SoundKicker
 767  	End If
 768  End Sub
 769
 770  '************************************************************************
 771  '						SKULL MOUTH
 772  '************************************************************************
 773
 774  Sub SolMouth(enabled)
 775  	Dim BP
 776  	If enabled Then
 777  		FlipperJaw.RotateToEnd
 778  		PlaySoundAt SoundFX("solenoidOn",DOFContactors), BM_SkullJaw
 779  	Else
 780  		FlipperJaw.RotateToStart
 781  		PlaySoundAt SoundFX("solenoidOff", DOFContactors), BM_SkullJaw
 782  	End If
 783  End Sub
 784
 785  Sub FlipperJaw_Animate
 786  	Dim a : a = FlipperJaw.CurrentAngle
 787  	Dim BP : For Each BP in BP_SkullJaw : BP.RotX = a: Next
 788  End Sub
 789
 790  Sub SkullChomp_Hit
 791  	If SkullChompBallDrop = False Then
 792  		PlaySoundAt "ball_drop_playfield_1_delayed", SkullChomp
 793  		SkullChompBallDrop = True
 794  	End If
 795  End Sub
 796
 797  '******************************************************
 798  '					KNOCKER
 799  '******************************************************
 800
 801  Sub SolKnocker(Enabled)
 802  	If enabled Then
 803  		KnockerSolenoid 'Add knocker position object
 804  	End If
 805  End Sub
 806
 807  '************************************************************************
 808  '      					SWITCHES
 809  '************************************************************************
 810
 811  'Spinner
```

## Switch events, popper and eject kickers, trough

Lines 812-1049:

```
 812  Sub sw16_spin:vpmtimer.pulsesw 16:End Sub
 813
 814  Sub sw16_Animate
 815  	Dim spinangle:spinangle = sw16.currentangle
 816  	Dim BP : For Each BP in BP_sw16_Wire : BP.RotX = spinangle: Next
 817  End Sub
 818
 819  'rollover
 820  Sub sw17_hit:Controller.switch(17) = 1:End Sub
 821  Sub sw17_unhit:Controller.switch(17) = 0: End Sub
 822  Sub sw18_hit:Controller.switch(18) = 1:End Sub
 823  Sub sw18_unhit:Controller.switch(18) = 0: End Sub
 824
 825  Sub sw25_hit:Controller.switch(25) = 1: KickBackIM.AddBall ActiveBall : End Sub
 826  Sub sw25_unhit:Controller.switch(25) = 0: KickBackIM.RemoveBall ActiveBall : End Sub
 827  Sub sw26_hit:Controller.switch(26) = 1:End Sub
 828  Sub sw26_unhit:Controller.switch(26) = 0: End Sub
 829
 830  'Slingshots
 831
 832  Dim LStep, RStep
 833
 834  Sub sw28_Slingshot
 835  	RS.VelocityCorrect(Activeball)
 836  	vpmTimer.PulseSw(28)
 837  	RandomSoundSlingshotRight BM_REMK
 838  	RStep = 0 : sw28_Timer ' Initialize Step to 0
 839  	sw28.TimerInterval = 17
 840  	sw28.TimerEnabled = 1
 841  End Sub
 842
 843  Sub sw28_Timer
 844  	Dim BP
 845  	Dim x1, x2, y: x1 = True:x2 = False:y = 25
 846      Select Case RStep
 847          Case 2:x1 = False:x2 = True:y = 15
 848          Case 3:x1 = False:x2 = False:y = 0:sw28.TimerEnabled = 0
 849      End Select
 850
 851  	For Each BP in BP_RSling1 : BP.Visible = x1: Next
 852  	For Each BP in BP_RSling2 : BP.Visible = x2: Next
 853  	For Each BP in BP_REMK : BP.transx = y: Next
 854
 855      RStep = RStep + 1
 856  End Sub
 857
 858  Sub sw27_Slingshot
 859  	LS.VelocityCorrect(Activeball)
 860  	vpmTimer.PulseSw(27)
 861  	RandomSoundSlingshotLeft BM_LEMK
 862  	LStep = 0 : sw27_Timer ' Initialize Step to 0
 863  	sw27.TimerInterval = 17
 864  	sw27.TimerEnabled = 1
 865  End Sub
 866
 867  Sub sw27_Timer
 868  	Dim BP
 869  	Dim x1, x2, y: x1 = True:x2 = False:y = 25
 870      Select Case LStep
 871          Case 3:x1 = False:x2 = True:y = 15
 872          Case 4:x1 = False:x2 = False:y = 0:sw27.TimerEnabled = 0
 873      End Select
 874
 875  	For Each BP in BP_LSling1 : BP.Visible = x1: Next
 876  	For Each BP in BP_LSling2 : BP.Visible = x2: Next
 877  	For Each BP in BP_LEMK : BP.transx = y: Next
 878
 879      LStep = LStep + 1
 880  End Sub
 881
 882  'Subway Optos
 883  Sub sw37_hit:Controller.switch(37) = 1: End Sub
 884  Sub sw37_unhit:Controller.switch(37) = 0: End Sub
 885  Sub sw38_hit:Controller.switch(38) = 1: End Sub
 886  Sub sw38_unhit:Controller.switch(38) = 0: End Sub
 887  Sub sw42_hit:Controller.switch(42) = 1: End Sub
 888  Sub sw42_unhit:Controller.switch(42) = 0: End Sub
 889
 890
 891  'Magnet Optos
 892  Sub sw46_hit: vpmtimer.pulsesw 46: End Sub
 893  Sub sw47_hit: vpmtimer.pulsesw 47: End Sub
 894  Sub sw48_hit: vpmtimer.pulsesw 48: End Sub
 895
 896
 897  'Drop Target
 898  Sub sw51_hit:DTHit 51:End Sub
 899
 900  'Wire Ramp
 901  Sub sw54_hit:Controller.switch(54) = 1: End Sub
 902  Sub sw54_unhit:Controller.switch(54) = 0: End Sub
 903
 904  'Inner Loop
 905  Sub sw55_hit:vpmtimer.PulseSw 55:End Sub
 906
 907  'StandUp Targets
 908  Sub sw56_hit:STHit 56:End Sub
 909  Sub sw57_hit:STHit 57:End Sub
 910
 911  'Right Loop
 912  Sub sw58_hit:vpmtimer.PulseSw 58:End Sub
 913
 914  'Left Loop
 915  Sub sw62_hit:vpmtimer.PulseSw 62:End Sub
 916
 917  'Left Plastic Ramp
 918  Sub sw63_hit:vpmtimer.PulseSw 63 :End Sub
 919  Sub sw64_hit:vpmtimer.PulseSw 64 :End Sub
 920
 921  'Right Plastic Ramp
 922  Sub sw66_hit:vpmtimer.PulseSw 66 :End Sub
 923  Sub sw67_hit:vpmtimer.PulseSw 67 :End Sub
 924
 925  'Shooter lane
 926  Sub sw15_hit: Controller.Switch(15) = 1 : End Sub
 927  Sub sw15_unhit: Controller.Switch(15) = 0 : End Sub
 928
 929
 930
 931  '************************* VUKs *****************************
 932  Dim KickerBall41, KickerBall61
 933
 934  Sub KickBall(kball, kangle, kvel, kvelz, kzlift)
 935  	dim rangle
 936  	rangle = PI * (kangle - 90) / 180
 937
 938  	kball.z = kball.z + kzlift
 939  	kball.velz = kvelz
 940  	kball.velx = cos(rangle)*kvel
 941  	kball.vely = sin(rangle)*kvel
 942  End Sub
 943
 944  'Right Subway VUK
 945  Sub sw41_Hit
 946      set KickerBall41 = activeball
 947      Controller.Switch(41) = 1
 948      SoundSaucerLock
 949  End Sub
 950
 951  Sub sw41_UnHit
 952      Controller.Switch(41) = 0
 953  End Sub
 954
 955  Sub SubwayVUK(Enable)
 956      If Enable then
 957  		If Controller.Switch(41) <> 0 Then
 958  			KickBall KickerBall41, 135, 0, 50, 15
 959  			SoundSaucerKick 1, sw41
 960  			Controller.Switch(41) = 0
 961  		End If
 962  	End If
 963  End Sub
 964
 965  'Left Scoop
 966  Sub sw61_Hit
 967      set KickerBall61 = activeball
 968      Controller.Switch(61) = 1
 969      SoundSaucerLock
 970  '	sw61.timerinterval=10
 971  '	sw61.timerenabled=true
 972  End Sub
 973
 974  Sub sw61_UnHit
 975      Controller.Switch(61) = 0
 976  End Sub
 977
 978  'sub sw61_timer
 979  '	debug.print "vuk left: " & KickerBall61.z
 980  	'prevents ball wiggle in saucer
 981  '	KickerBall61.x=sw61.x
 982  '	KickerBall61.y=sw61.y
 983  '	KickerBall61.z=-9 'a bit higher so it wont touch the collidable bottom
 984  '	KickerBall61.angmomx=0
 985  '	KickerBall61.angmomy=0
 986  '	KickerBall61.angmomz=0
 987  '	KickerBall61.velx=0
 988  '	KickerBall61.vely=0
 989  '	KickerBall61.velz=0
 990  '	If Controller.Switch(61) = 0 Then me.timerenabled = false
 991  'end sub
 992
 993  Sub LeftKicker(Enable)
 994      If Enable then
 995  		If Controller.Switch(61) <> 0 Then
 996  			KickBall KickerBall61, 170, 20, 25, 15
 997  			SoundSaucerKick 1, sw61
 998  			End If
 999  			Controller.Switch(61) = 0
1000  	End If
1001  End Sub
1002
1003  '******************************************************
1004  '						TROUGH
1005  '******************************************************
1006
1007  Sub sw32_Hit():Controller.Switch(32) = 1:UpdateTrough:End Sub
1008  Sub sw32_UnHit():Controller.Switch(32) = 0:UpdateTrough:End Sub
1009  Sub sw33_Hit():Controller.Switch(33) = 1:UpdateTrough:End Sub
1010  Sub sw33_UnHit():Controller.Switch(33) = 0:UpdateTrough:End Sub
1011  Sub sw34_Hit():Controller.Switch(34) = 1:UpdateTrough:End Sub
1012  Sub sw34_UnHit():Controller.Switch(34) = 0:UpdateTrough:End Sub
1013  Sub sw35_Hit():Controller.Switch(35) = 1:UpdateTrough:End Sub
1014  Sub sw35_UnHit():Controller.Switch(35) = 0:UpdateTrough:End Sub
1015
1016  Sub UpdateTrough()
1017  	UpdateTroughTimer.Interval = 100
1018  	UpdateTroughTimer.Enabled = 1
1019  End Sub
1020
1021  Sub UpdateTroughTimer_Timer()
1022  	If sw32.BallCntOver = 0 Then sw33.kick 60, 9
1023  	If sw33.BallCntOver = 0 Then sw34.kick 60, 9
1024  	If sw34.BallCntOver = 0 Then sw35.kick 60, 9
1025  	UpdateTroughTimer.Enabled = 0
1026  End Sub
1027
1028  '******************************************************
1029  '					DRAIN & RELEASE
1030  '******************************************************
1031
1032  Sub Drain_Hit() 'Drain
1033  	RandomSoundDrain Drain
1034  	UpdateTrough
1035  	vpmTimer.AddTimer 500, "Drain.kick 60, 9'"
1036  End Sub
1037
1038  Sub ReleaseBall(enabled)
1039  	If enabled Then
1040  		RandomSoundBallRelease Drain
1041  		vpmtimer.pulsesw 31
1042  		sw32.kick 60, 12
1043  		UpdateTrough
1044  	End If
1045  End Sub
1046
1047  '******************************************************
1048  '	SWITCH ANIMATIONS
1049  '******************************************************
```

## Drop target and standup target helpers

Lines 2386-2400:

```
2386  Sub DTHit(switch)
2387  	Dim i
2388  	i = DTArrayID(switch)
2389
2390  	PlayTargetSound
2391  	DTArray(i).animate = DTCheckBrick(ActiveBall,DTArray(i).prim)
2392  	If DTArray(i).animate = 1 Or DTArray(i).animate = 3 Or DTArray(i).animate = 4 Then
2393  		DTBallPhysics ActiveBall, DTArray(i).prim.rotz, DTMass
2394  	End If
2395  	DoDTAnim
2396  End Sub
2397
2398  Sub DTRaise(switch)
2399  	Dim i
2400  	i = DTArrayID(switch)
```
