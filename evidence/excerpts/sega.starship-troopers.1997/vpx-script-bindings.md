# Starship Troopers — controller bindings in the retained table's embedded script

Every non-comment line of the embedded script of `Starship Troopers (Sega 1997) VPW Mod v2.0.vpx` (extracted
`script.vbs`, SHA-256 `e97088ef82faf82205fbb080dac0f8489370ec03364cedc7d5b3f26bd5b03c3a`, byte-identical to the
`jsm174/vpx-standalone-scripts` corpus file `Starship Troopers (Sega 1997) VPW Mod v2.0.vbs.original` at
`15d112648a1b94b9f59eb8b3c335d57283653c50`) that names the controller, a ball stack, saucer, magnet or mech, a switch
write, a solenoid callback or handler, a lamp or G.I. assignment, a flasher collection it switches or a toy it moves
from a solenoid or the mech, quoted verbatim with its line number. Selected with a fixed pattern over the whole file;
whole-line comments are left out, trailing comments kept. Tabs are kept as in the file; trailing whitespace is trimmed.

```text
  207: ExecuteGlobal GetTextFile("controller.vbs")
  208: If Err Then MsgBox "You need the Controller.vbs file in order to run this table (installed with the VPX package in the scripts folder)"
  211: LoadVPM "01560000", "sega.vbs", 3.57
  213: Const UseSolenoids = 15
  214: Const UseLamps = 0
  231: Const cGameName = "startrp2"
  234: Dim bsTrough, mBug, bsSuperVUK, bsLeftVUK, FlippersEnabled, mLeftMagnet, mRightMagnet
  237: Set GICallback = GetRef("UpdateGI")
  246:     With Controller
  247:         .GameName = cGameName
  248:         If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
  250:         .Games(cGameName).Settings.Value("rol") = 1 'set it to 1 to rotate the DMD to the left
  255:         .HandleMechanics = 0
  269: 		vpmNudge.TiltSwitch = 56
  276:         .InitSw 0, 15, 14, 13, 12, 0, 0, 0
  277:         .InitKick BallRelease, 80, 11
  279:         .Balls = 4
  280:         .IsTrough = 1
  286:         .InitSw 0, 46, 0, 0, 0, 0, 0, 0
  287:         .InitKick sw46, 182, 72 '42
  297:         .InitKicker sw45, 45, 131, 15, 15
  306:         .InitMagnet LeftMagnet, 30
  308: 		.Solenoid = 5
  314:         .InitMagnet RightMagnet, 30
  316: 		.Solenoid = 6
  325: 		.MType=vpmMechStepSol+vpmMechTwoDirSol+vpmMechStopEnd+vpmMechLinear+vpmMechFast
  326: 		.Sol1=17
  327: 		.Length=600 '150 'Time duration for mech trip
  328: 		.Steps=222 '222 '120 'primitive trans -110 to +10 'scaled prim trans -110 to +93.5 + 18.5 = 222
  329: 		.AddSw 34,0,1 'Add switch 34, start 0 end 1
  330: 		.AddSw 33,221,222 '33,119,120
  331: 		.Callback=GetRef("UpdateWarriorBug")
  335:  	sw38.IsDropped=1
  336:  	sw38a.IsDropped=1
  339: 	for each xx in BWalls:xx.isDropped = 1:Next
  387: Sub table1_Paused:Controller.Pause = 1:End Sub
  388: Sub table1_unPaused:Controller.Pause = 0:End Sub
  389: Sub table1_exit():Controller.Pause = False:Controller.Stop:End Sub
  463:     If KeyCode = MechanicalTilt Then vpmTimer.PulseSw vpmNudge.TiltSwitch: Exit Sub: End if
  474:     If KeyCode = RightMagnaSave OR KeyCode = LockbarKey Then
  475: 		Controller.Switch(88) = 1
  476: 		If FlippersEnabled Then SolRFlipperS True
  517:     If KeyCode = RightMagnaSave OR KeyCode = LockbarKey Then
  519: 		Controller.Switch(88) = 0
  538: 		Plunger.Fire
  573:     x = LoadValue(cGameName, "LUTImage")
  579:     SaveValue cGameName, "LUTImage", LUTImage
  606: SolCallback(1) = "SolRelease"
  607: SolCallback(2) = "SolAutolaunch"
  609: SolCallback(3) = "SolLeftVuk"
  610: SolCallback(4) = "bsSupervuk.SolOut"
  611: SolCallback(5) = "SolLeftMagnet"
  612: SolCallback(6) = "SolRightMagnet"
  613: SolCallBack(7) = "SolBrainBug"
  614: SolCallBack(8)= "SolKnocker"
  615: SolCallBack(15)= "FlippersEnabled="
  616: SolCallBack(23) = "SetLamp 123," 	'flash brainbug
  617: SolCallBack(25) = "Sol25" 	'Flash Red
  618: SolCallBack(26) = "Sol26"	'Flash Yellow
  619: SolCallBack(27) = "Sol27"	'Flash Green
  620: SolCallBack(28) = "Sol28"	'Flash Blue
  621: SolCallBack(29) = "SetLamp 129," 'F5 WarBugSled Flasher X4
  622: SolCallBack(30) = "SetLamp 130," 'F6 Left Ramp Flasher X4
  623: SolCallBack(31) = "SetLamp 131," 'F7 Right Ramp Flasher X4
  624: SolCallBack(32) = "SetLamp 132," 'F8 Pop Bumpers Flasher X2
  627: Sub sol25(enabled): If enabled then FlashBlinkingRed:Else FlashoffRed:End if:End Sub
  628: Sub sol26(enabled): If enabled then FlashBlinkingYellow:Else FlashoffYellow:End if:End Sub
  629: Sub sol27(enabled): If enabled then FlashBlinkingGreen:Else FlashoffGreen:End if:End Sub
  630: Sub sol28(enabled): If enabled then FlashBlinkingBlue:Else FlashoffBlue:End if:End Sub
  633: Sub SolKnocker(Enabled) : If enabled Then KnockerSolenoid : End If : End Sub 'Add knocker position object
  641: Sub SolRelease(Enabled)
  643:         If bsTrough.Balls > 0 Then bsTrough.ExitSol_On
  648: Sub SolAutoLaunch(Enabled)
  650: 		Plunger.Autoplunger = True
  651: 		Plunger.Fire
  652: 		PlaySound SoundFX("fx_AutoPlunger", DOFContactors)
  654: 		Plunger.Autoplunger = False
  665: Sub SolLeftVuk(Enabled)
  668: 		bsleftvuk.exitSol_on
  695: Sub SolBrainBug(Enabled)
  699: 			if InRect(b.x,b.y,545,871,472,1054,633,1126,714,944) then
  705: 		BrainBugflipper.rotatetoend
  707: 		sw38.isDropped = 0
  708: 		sw38a.isDropped = 0
  710: 		Controller.Switch(37) = True
  711: 		Controller.Switch(39) = True
  714: 		BrainBugFlipper.rotatetostart
  716: 		sw38.isDropped = 1
  717: 		sw38a.isDropped = 1
  719: 		Controller.Switch(37) = False
  720: 		Controller.Switch(39) = False
  727: Sub sw38_timer: vpmTimer.PulseSw 38:Me.TimerEnabled = 0:End Sub
  775: Sub UpdateWarriorBug(NewPos, aSpeed, LastPos)
  777: 	For each WarriorBugStuff in WarriorBugGroup: WarriorBugStuff.TransZ = NewPos-111:next '-110 -1 difference to starting point
  781:     Position = NewPos * 23 / 222 '120 steps in original (from -110 to 10)
  784: 	BugWalls(LastPosition).IsDropped=1
  786: 	BugWalls(Position).IsDropped=0
  791: Sub BWalls_Hit(idx):vpmTimer.PulseSw 35:ShakeTarget:End Sub 'fx_switch
  813: Sub sw10_Hit:vpmTimer.PulseSw 10: vpmTimer.AddTimer 1800, "SuperVukAddBall'":Me.Enabled = 0:Me.TimerEnabled = 1: End Sub
  844: 	Public Sub AddPulseSwNew(aSwNo, aInterval, aStart, aEnd)
  845: 		If Controller.Version >= "01200000" Then
  855: 		With Controller
  871: 	Public Property Get Position : Position = Controller.GetMech(mMechNo) : End Property
  872: 	Public Property Get Speed    : Speed = Controller.GetMech(-mMechNo)   : End Property
  877: 		currPos = Controller.GetMech(mMechNo)
  878: 		speed = Controller.GetMech(-mMechNo)
  889: Sub SolLeftMagnet(Enabled):if enabled then PlaySoundAt "fx_magnet", Leftmagnet:Else:StopSound "fx_magnet":End if:End Sub
  890: Sub SolRightMagnet(Enabled):if enabled then PlaySoundAt "fx_magnet", Rightmagnet:Else:StopSound "fx_magnet":End if:End Sub
  898: SolCallback(sLRFlipper) = "SolRFlipper"
  899: SolCallback(sLLFlipper) = "SolLFlipper"
  905: Sub SolLFlipper(Enabled)
  908: 		LF.Fire  'leftflipper.rotatetoend
  917: 		LeftFlipper.RotateToStart
  926: Sub SolRFlipper(Enabled)
  929: 		RF.Fire 'rightflipper.rotatetoend
  938: 		RightFlipper.RotateToStart
  947: Sub SolRFlipperS(Enabled)
  950:         RFs.fire 'RightFlipper.RotateToEnd
  953:         RightFlipperS.RotateToStart
  972:     vpmTimer.PulseSw 59
  991:     vpmTimer.PulseSw 62
 1010: Sub Bumper1_Hit:vpmTimer.PulseSw 49 : RandomSoundBumperTop Bumper1 : End Sub
 1011: Sub Bumper2_Hit:vpmTimer.PulseSw 51 : RandomSoundBumperMiddle Bumper2 : End Sub
 1012: Sub Bumper3_Hit:vpmTimer.PulseSw 50 : RandomSoundBumperBottom Bumper3 : End Sub
 1017: Sub sw16_Hit:Controller.Switch(16) = 1:sw16p.RotX = 70: BIPL=1 : End Sub
 1018: Sub sw16_UnHit:Controller.Switch(16) = 0:sw16p.RotX = 90: BIPL=0 : End Sub
 1020: Sub sw41_Hit:Controller.Switch(41) = 1:sw41p.RotX = 70:End Sub
 1021: Sub sw41_UnHit:Controller.Switch(41) = 0:sw41p.RotX = 90:End Sub
 1023: Sub sw42_Hit:Controller.Switch(42) = 1:sw42p.RotX = 70:End Sub
 1024: Sub sw42_UnHit:Controller.Switch(42) = 0:sw42p.RotX = 90:End Sub
 1026: Sub sw43_Hit:Controller.Switch(43) = 1:sw43p.RotX = 70:End Sub
 1027: Sub sw43_UnHit:Controller.Switch(43) = 0:sw43p.RotX = 90:End Sub
 1029: Sub sw57_Hit:Controller.Switch(57) = 1:sw57p.RotX = 70:End Sub
 1030: Sub sw57_UnHit:Controller.Switch(57) = 0:sw57p.RotX = 90:End Sub
 1032: Sub sw58_Hit:Controller.Switch(58) = 1:sw58p.RotX = 70: activeball.vely=activeball.vely*0.8: activeball.angmomz=0: End Sub
 1033: Sub sw58_UnHit:Controller.Switch(58) = 0:sw58p.RotX = 90:End Sub
 1035: Sub sw61_Hit:Controller.Switch(61) = 1:sw61p.RotX = 70: activeball.vely=activeball.vely*0.8: activeball.angmomz=0: End Sub
 1036: Sub sw61_UnHit:Controller.Switch(61) = 0:sw61p.RotX = 90:End Sub
 1038: Sub sw60_Hit:Controller.Switch(60) = 1:sw60p.RotX = 70:End Sub
 1039: Sub sw60_UnHit:Controller.Switch(60) = 0:sw60p.RotX = 90:End Sub
 1042: Sub sw47_Hit:Controller.Switch(47)= 1:End Sub
 1043: Sub sw47_UnHit:Controller.Switch(47) = 0:End Sub
 1045: Sub sw48_Hit:Controller.Switch(48)= 1:End Sub
 1046: Sub sw48_UnHit:Controller.Switch(48) = 0:End Sub
 1052: Sub sw9_Hit:Controller.Switch(9)= 1:RandomSoundHole:WireRampOff:End Sub
 1053: Sub sw9_UnHit:Controller.Switch(9) = 0:End Sub
 1061: Sub sw40_Hit:Controller.Switch(40)= 1:PlaySoundAtBall "fx_tedhit":End Sub
 1062: Sub sw40_UnHit:Controller.Switch(40) = 0:End Sub
 1066: Sub T17_Hit:vpmTimer.pulseSw 17: T17p.RotX = T17p.RotX +4:Me.TimerEnabled = 1:End Sub
 1069: Sub T18_Hit:vpmTimer.pulseSw 18: T18p.RotX = T18p.RotX +4:Me.TimerEnabled = 1:End Sub
 1072: Sub T19_Hit:vpmTimer.pulseSw 19: T19p.RotX = T19p.RotX +4:Me.TimerEnabled = 1:End Sub
 1075: Sub T20_Hit:vpmTimer.pulseSw 20: T20p.RotX = T20p.RotX +4:Me.TimerEnabled = 1:End Sub
 1078: Sub T21_Hit:vpmTimer.pulseSw 21: T21p.RotX = T21p.RotX +4:Me.TimerEnabled = 1:End Sub
 1081: Sub T22_Hit:vpmTimer.pulseSw 22: T22p.RotX = T22p.RotX +4:Me.TimerEnabled = 1:End Sub
 1084: Sub T23_Hit:vpmTimer.pulseSw 23: T23p.RotX = T23p.RotX +4:Me.TimerEnabled = 1:End Sub
 1087: Sub T24_Hit:vpmTimer.pulseSw 24: T24p.RotX = T24p.RotX +4:Me.TimerEnabled = 1:End Sub
 1090: Sub T27_Hit:vpmTimer.pulseSw 27: T27p.RotX = T27p.RotX +4:Me.TimerEnabled = 1:End Sub
 1093: Sub T28_Hit:vpmTimer.pulseSw 28: T28p.RotX = T28p.RotX +4:Me.TimerEnabled = 1:End Sub
 1096: Sub T29_Hit:vpmTimer.pulseSw 29: T29p.RotX = T29p.RotX +4:Me.TimerEnabled = 1:End Sub
 1099: Sub T30_Hit:vpmTimer.pulseSw 30: T30p.RotX = T30p.RotX +4:Me.TimerEnabled = 1:End Sub
 1102: Sub T31_Hit:vpmTimer.pulseSw 31: T31p.RotX = T31p.RotX +4:Me.TimerEnabled = 1:End Sub
 1105: Sub T32_Hit:vpmTimer.pulseSw 32: T32p.RotX = T32p.RotX +4:Me.TimerEnabled = 1:End Sub
 1109: Sub sw25_Hit:vpmTimer.PulseSW 25: End Sub
 1110: Sub sw52_Hit:vpmTimer.PulseSW 52: End Sub
 1111: Sub sw53_Hit:vpmTimer.PulseSW 53: End Sub
 1113: Sub sw26_Hit:vpmTimer.PulseSW 26: WireRampOff: End Sub
 1155: Sub UpdateGi(no, enabled)
 1159: 				SetLamp 200, enabled
 1227: 	for each bulb in StrobeFlashersLRed
 1229: 	for each fbulb in StrobeFlashersFRed
 1237: 	for each bulb in StrobeFlashersLGreen
 1239: 	for each fbulb in StrobeFlashersFGreen
 1247: 	for each bulb in StrobeFlashersLYellow
 1249: 	for each fbulb in StrobeFlashersFYellow
 1257: 	for each bulb in StrobeFlashersLBlue
 1259: 	for each fbulb in StrobeFlashersFBlue
 1309: 	for each fbulb in StrobeFlashersFRed
 1311: 	for each bulb in StrobeFlashersLRed
 1323: 	for each fbulb in StrobeFlashersFRed
 1325: 	for each bulb in StrobeFlashersLRed
 1340: 	for each fbulb in StrobeFlashersFGreen
 1342: 	for each bulb in StrobeFlashersLGreen
 1354: 	for each fbulb in StrobeFlashersFGreen
 1356: 	for each bulb in StrobeFlashersLGreen
 1371: 	for each fbulb in StrobeFlashersFYellow
 1373: 	for each bulb in StrobeFlashersLYellow
 1385: 	for each fbulb in StrobeFlashersFYellow
 1387: 	for each bulb in StrobeFlashersLYellow
 1401: 	for each fbulb in StrobeFlashersFBlue
 1403: 	for each bulb in StrobeFlashersLBlue
 1415: 	for each fbulb in StrobeFlashersFBlue
 1417: 	for each bulb in StrobeFlashersLBlue
 1507:     chgLamp = Controller.ChangedLamps
 1519:     lampm 1, l1
 1520:     lampm 1, l1b
 1521:     flash 1, lf1
 1522:     lampm 2, l2
 1523:     lampm 2, l2b
 1524:     flash 2, lf2
 1525:     lampm 3, l3
 1526:     lampm 3, l3b
 1527:     flash 3, lf3
 1528:     lampm 4, l4
 1529:     lampm 4, l4b
 1530:     flash 4, lf4
 1531:     lampm 5, l5
 1532:     lampm 5, l5b
 1533:     flash 5, lf5
 1534:     lampm 6, l6
 1535:     lampm 6, l6b
 1536:     flash 6, lf6
 1537:     lampm 7, l7
 1538:     lampm 7, l7b
 1539:     flash 7, lf7
 1540:     lampm 8, l8
 1541:     lampm 8, l8b
 1542:     flash 8, lf8
 1543:     lampm 9, l9
 1544:     lampm 9, l9b
 1545:     flash 9, lf9
 1546:     lampm 10, l10
 1547:     lampm 10, l10b
 1548:     flash 10, lf10
 1550: 	lampm 11, l11
 1551: 	lampm 11, l11b
 1552: 	flash 11, lf11
 1553:     lampm 12, l12
 1554:     lampm 12, l12b
 1555:     flash 12, lf12
 1556:     lampm 13, l13a
 1557:     lampm 13, l13b
 1558:     flash 13, lf13
 1559:     lampm 14, l14a
 1560:     lampm 14, l14b
 1561:     flash 14, lf14
 1562:     lampm 15, l15a
 1563:     lampm 15, l15b
 1564:     flash 15, lf15
 1565:     lampm 16, l16a
 1566:     lampm 16, l16b
 1567:     flash 16, lf16
 1568:     lampm 17, l17
 1569:     flash 17, lf17
 1570:     lampm 18, l18
 1571:     lampm 18, l18b
 1572:     flash 18, lf18
 1573:     lampm 19, l19
 1574:     flash 19, lf19
 1575:     lampm 20, l20
 1576:     lampm 20, l20b
 1577:     flash 20, lf20
 1578:     lampm 21, l21
 1579:     flash 21, lf21
 1580:     lampm 22, l22
 1581:     flash 22, lf22
 1582:     lampm 23, l23
 1583:     flash 23, lf23
 1584:     lampm 24, l24
 1585:     flash 24, lf24
 1586:     lampm 25, l25
 1587:     lampm 25, l25b
 1588:     flash 25, lf25
 1589:     lampm 26, l26
 1590:     lampm 26, l26b
 1591:     flash 26, lf26
 1592:     lampm 27, l27
 1593:     lampm 27, l27b
 1594:     flash 27, lf27
 1596:     lampm 28, l28
 1597:     lampm 28, l28b
 1599:     lampm 29, l29
 1600:     lampm 29, l29b
 1602:     lampm 30, l30
 1603:     lampm 30, l30b
 1606:     lampm 31, l31
 1607:     flash 31, lf31
 1608:     lampm 32, l32
 1609:     lampm 32, l32b
 1610:     flash 32, lf32
 1612:     lampm 35, l35
 1613:     flashm 35, fl35
 1614:     flash 35, fl35a
 1615:     lampm 36, l36
 1616:     flashm 36, fl36
 1617:     flash 36, fl36a
 1618:     lampm 37, l37
 1619:     lampm 37, l37b
 1620:     flashm 37, lf37s
 1621:     flash 37, lf37
 1622:     lampm 38, l38
 1623:     lampm 38, l38b
 1624:     flashm 38, lf38s
 1625:     flash 38, lf38
 1626:     lampm 39, l39
 1627:     flashm 39, fl39
 1628:     flash 39, fl39a
 1631:     lampm 40, l40
 1632:     lampm 40, l40a
 1633:     lampm 40, l40b
 1634:     flashm 40, lf40
 1635:     flash 40, lf40a
 1637:     lampm 41, l41
 1638:     lampm 41, l41b
 1639:     flash 41, lf41
 1640:     lampm 42, l42
 1641:     lampm 42, l42b
 1642:     flash 42, lf42
 1643:     lampm 43, l43
 1644:     flash 43, lf43
 1645:     lampm 44, l44
 1646:     lampm 44, l44b
 1647:     flash 44, lf44
 1648:     lampm 45, l45
 1649:     lampm 45, l45b
 1650:     flash 45, lf45
 1651:     lampm 46, l46
 1652:     lampm 46, l46b
 1653:     flash 46, lf46
 1655:     lampm 47, l47
 1656:     lampm 47, l47b
 1657:     flash 47, fl47
 1658:     lampm 48, l48
 1659:     lampm 48, l48b
 1660:     flash 48, fl48
 1661:     flash 49, l49
 1662:     flash 50, l50
 1663:     flash 51, l51
 1664:     flash 52, l52
 1665:     flash 53, l53
 1666:     flash 54, l54
 1667:     flash 55, l55
 1669:     flash 57, l57
 1670:     flash 58, l58
 1671:     flash 59, l59
 1672:     flash 60, l60
 1673:     flash 61, l61
 1674:     flash 62, l62
 1675:     flash 63, l63
 1677:     flash 65, l65
 1678:     flash 66, l66
 1679:     flash 67, l67
 1680:     flash 68, l68
 1681:     flash 69, l69
 1682:     flash 70, l70
 1683:     flash 71, l71
 1685:     flash 73, l73
 1686:     flash 74, l74
 1687:     flash 75, l75
 1688:     flash 76, l76
 1689:     flash 77, l77
 1690:     flash 78, l78
 1691:     flash 79, l79
 1693:     lampm 56, l56
 1694:     lampm 56, l56b
 1695:     flash 56, lf56
 1697:     lampm 64, l64
 1698:     lampm 64, l64b
 1699:     flash 64, lf64
 1701:     lampm 72, l72
 1702:     lampm 72, l72b
 1703:     flash 72, lf72
 1705:     lampm 80, l80
 1706:     lampm 80, l80b
 1707:     flash 80, lf80
 1711: 	lampm 123, l123a
 1712: 	lampm 123, l123b
 1715: 	lampm 129, l129
 1716: 	lampm 129, l129a
 1717: 	lampm 129, l129b
 1718: 	flashm 129, f129s
 1719: 	flashm 129, lf129
 1720: 	flash 129, lf129b
 1724: 	lampm 130, l130b
 1725: 	lampm 130, l130c
 1726: 	lampm 130, l130d
 1727: 	lampm 130, l130e
 1728: 	flashm 130, f130a
 1729: 	flashm 130, f130b
 1730: 	flashm 130, f130c
 1731: 	flash 130, f130d
 1734: 	lampm 131, l131b
 1735: 	lampm 131, l131c
 1736: 	lampm 131, l131d
 1737: 	lampm 131, l131e
 1738: 	flashm 131, f131a
 1739: 	flashm 131, f131b
 1740: 	flashm 131, f131c
 1741: 	flash 131, f131d
 1743: 	lampm 132, l132
 1744: 	flash 132, lf132
 1747: 	lampm 200, Light001
 1748: 	lampm 200, Light002
 1749: 	lampm 200, Light003
 1750: 	lampm 200, Light004
 1751: 	lampm 200, Light005
 1752: 	lampm 200, Light006
 1753: 	lampm 200, Light007
 1754: 	lampm 200, Light008
 1755: 	lampm 200, Light009
 1756: 	lampm 200, Light010
 1757: 	lampm 200, Light011
 1758: 	lampm 200, Light012
 1759: 	lampm 200, Light013
 1760: 	lampm 200, Light014
 1761: 	lampm 200, Light015
 1762: 	lampm 200, Light016
 1763: 	lampm 200, Light017
 1764: 	lampm 200, Light018
 1765: 	lampm 200, Light019
 1766: 	lampm 200, Light020
 1767: 	lampm 200, Light021
 1768: 	lampm 200, Light022
 1769: 	lampm 200, Light023
 1770: 	lampm 200, Light024
 1771: 	lampm 200, Light025
 1772: 	lampm 200, Light026
 1773: 	lampm 200, Light027
 1774: 	lampm 200, Light028
 1775: 	flashm 200, GIFL1
 1776: 	flashm 200, lfgi001
 1777: 	flashm 200, lfgi002
 1778: 	flashm 200, lfgi003
 1779: 	flash 200, lfgi004
 1799: Sub SetLamp(nr, value) ' 0 is off, 1 is on
 2412:                 Flipper.RotateToEnd
 2623: Function InRect(px,py,ax,ay,bx,by,cx,cy,dx,dy)
 2631:                 InRect = True
 2633:                 InRect = False
 3421: Sub KnockerSolenoid()
```

Collections the quoted lines use, from the table's `collections.json`:

- `StrobeFlashersLRed` = `l125b`, `l125a`, `l125c`, `l125d`; `StrobeFlashersLYellow` = `l126b`, `l126d`, `l126c`,
  `l126a`; `StrobeFlashersLGreen` = `l127d`, `l127a`, `l127c`, `l127b`; `StrobeFlashersLBlue` = `l128d`, `l128b`,
  `l128c`, `l128a`. The matching `StrobeFlashersF*` collections hold the flasher overlays (`f125`, `fl125a`-`fl125e`
  in four layers, `f125s1`-`f125s4`, and so on for 126-128).
- `BWalls` = `BWall1` to `BWall24` (the warrior bug's 24 hit walls, one raised at a time by `UpdateWarriorBug`);
  `WarriorBugGroup` = `WarriorBugAssembly002` to `WarriorBugAssembly005`; `BrainBugGroup` = `BrainBugCageGlass`,
  `BrainBugCage`, `BrainBug`.
- `GILamps` = `Light001` to `Light028`.
