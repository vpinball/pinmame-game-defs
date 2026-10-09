# Black Hole — Runtime bindings quoted from the retained table script

Source: the embedded script of the retained `Black Hole (Gottlieb 1981) vpx 1.1.vpx` by cyberpez (extracted with
vpxtool 0.33.3 to `script.vbs`, 3182 lines, Windows line endings). The lines below are quoted verbatim with their line
numbers, tabs and trailing spaces normalized to single spaces, so a reader can check every binding the definition
takes from the script without holding the table. Only lines that bind a controller address or decide what an address
drives are quoted; options, physics, sounds and animation are omitted.

## ROM selection and controller setup

```vbscript
  78: '1 "blckhole" ' Gottlieb Rev.1 - blckhole
  79: '2 "blkhole2" ' Gottlieb Rev.2 - blkhole2
  80: '3 "bhol_ltd" ' Gottlieb Limitied Edition - bhol_ltd working????? acts CRAZY
  81: '4 "blkholea" ' Gottlieb Sound Only - blkholea
  82:
  83: '5 "blkhole7" ' Gottlieb 7-digit - blkhole7
  84: '6 "blkhol7s" ' Gottlieb Sound Only 7-digit - blkhol7s
  85:
  86: RomSet = 5
 104: LoadVPM "00990300", "sys80.VBS", 2.33
 110: If RomSet = 1 then cGameName="blckhole":DisplayTimer6.Enabled = true End If
 111: If RomSet = 2 then cGameName="blkhole2":DisplayTimer6.Enabled = true End If
 112: If RomSet = 3 then cGameName="bhol_ltd":DisplayTimer6.Enabled = true End If
 113: If RomSet = 4 then cGameName="blkholea":DisplayTimer6.Enabled = true End If
 114: If RomSet = 5 then cGameName="blkhole7":DisplayTimer7.Enabled = true End If
 115: If RomSet = 6 then cGameName="blkhol7s":DisplayTimer7.Enabled = true End If
 121: Const cCredits="Black Hole",UseSolenoids=1,UseLamps=0,UseGI=1,UseSync=1
 154: vpmNudge.TiltSwitch=26
 155: vpmNudge.Sensitivity=3
 156: vpmNudge.TiltObj = Array(Bumper1,Bumper2,Bumper3,Bumper4,Bumper5,Bumper6,Sling1,Sling2,Sling3,Sling8)
 157:
 158: CheckSolenoid 16,0 ' Initialize Upper Playfield Relay
 159:
 160: controller.switch(25) = true
```

## Solenoid constants and callbacks

```vbscript
 191: Const sSaucer=12
 192: Const sRT=13
 193: Const sKnocker=8
 194: Const sGate=17
 195: Const sCLo=18
 196: Const sEnable=19
 197: const sdtLeftLower = 5
 198: const sdtRightLower = 6
 199: const sdtRightUpper = 1
 200: const sdtLeftUpper = 2
 201: const sOutHole = 9
 202:
 203: SolCallBack(sSaucer)="bsSaucer.SolOut"
 204: SolCallback(sKnocker)="vpmSolSound SoundFX(""knocker"",DOFKnocker),"
 205: SolCallback(sGate)="vpmSolDiverter Flipper1,True,"
 206: SolCallback(sEnable)="vpmNudge.SolGameOn"
 207: SolCallback(42) = "bsLKick.SolOut"
 208: solcallback(sdtLeftUpper)="BlackTargetsUp"
 209: solcallback(sdtRightLower)="WhiteTargetsUp"
 210: solcallback(sdtRightUpper)="HoleTargetsUp"
 211: solcallback(sdtLeftLower)="YellowTargetsUp"
 212: SolCallback(sLRFlipper) = "SolRFlipper"
 213: SolCallback(sLLFlipper) = "SolLFlipper"
 214: SolCallback(sOutHole) = "SolOuthole"
```

## Lamp-driven devices (CheckSolenoid, called from the ChangedLamps loop)

```vbscript
 216: '********************
 217: ' Black Hole used lamps to activate solenoids, CheckSolenoid is called when lamps are changed and looks for those assigned to solenoid actions
 218: '********************
 219:
 220: Sub CheckSolenoid(lnum,lstate)
 221: Select Case lnum
 222: Case 8:
 223: If lstate = 1 then ' Lower Playfield Trough Gate
 224: sw53.kick 60, 5
 225: controller.Switch(53) = 0
 226: End If
 227: Case 12: ' Lower Playfield kicker
 228: If lstate = 1 then
 229: sw42.kick -30,4
 230: controller.Switch(42) = 0
 231: SoundFX "kicker",DOFContactors
 232: If controller.Lamp(17) Then
 233: If BlackLightMultiball = 1 then
 234: StartBlackLightMultiball
 235: End If
 236: End If
 237: End If
 238: Case 13: ' Upper Playfield kicker
 239: If lstate = 1 then
 240: sw05.kickZ 175,10,0,5
 241: controller.Switch(5) = 0
 242: SoundFX "kicker",DOFContactors
 243: sw05.timerenabled = true
 244: End If
 245: Case 14: ' Lower Playfield Tube Kicker
 246: If lstate = 1 then
 247: sw43.kick 180,40,0.5
 248: controller.Switch(43) = 0
 249: SoundFX "kicker",DOFContactors
 250: End If
 251: Case 15: ' Shooter Lane Ball Release
 252: If lstate = 1 then
 253: ReleaseBall
 254: End If
 255: Case 16: ' Upper Playfield Relay
 256: if lstate = 0 then
 257: SetUpperGI(1)
 258: Setflash 101, 1
 259: SetLamp 101, 1
 260: BlackHole.ColorGradeImage = "ColorGrade_on"
 261: Else
 262: SetUpperGI(0)
 263: Setflash 101, 0
 264: SetLamp 101, 0
 265: BlackHole.ColorGradeImage = "ColorGrade_off"
 266: End If
 267: Case 17: ' Lower Playfield Relay
 268: if lstate = 1 then
 269: SetLowerGIOn
 270: LowerGIBuzz.enabled = True
 271: Woosh.enabled = True
 272: else
 273: SetLowerGIOff
 274: LowerGIBuzz.enabled = False
 275: LowerGIBuzzStep = 0
 276: Woosh.enabled = false
 277: StopSound "Woosh"
 278: WooshStep = 0
 279: end if
 280: Case 18: ' Re-Entry Tube Gate
 281: if lstate = 1 then
 282: Flipper1.rotatetoEnd
 283: SetLamp 138, 1
 284: SetFlash 138, 1
 285: SetLamp 139, 0
 286: SetFlash 139, 0
 287: else
 288: Flipper1.rotatetoStart
 289: SetLamp 138, 0
 290: SetFlash 138, 0
 291: SetLamp 139, 1
 292: SetFlash 139, 1
 293: end if
 294: End Select
 295: End Sub
```

## Lower playfield trough, kicker and tube switches

```vbscript
 302: Sub LowerStage_Hit():If Controller.Switch(53) = 0 Then LowerStage.kick 60, 5:End If:End Sub
 303:
 304: Sub sw53_Hit():Controller.Switch(53)=1:End Sub
 305: Sub sw53_UnHit():If LowerStage.BallCntOver = 1 Then LowerStage.kick 60, 5:End If:End Sub
 306:
 307: Sub sw42_Hit():playsound "kicker_enter":controller.Switch(42)=1:End Sub
 308: Sub sw43_Hit():playsound "kicker_enter":controller.Switch(43)=1:SetLamp 123, 1:End Sub
 309:
 310: Sub ReEnrtyTubeExit_hit():SetLamp 123, 0:End Sub
```

## Upper playfield trough and drain

```vbscript
 317: Sub Kicker6_Hit():UpdateTrough:End Sub
 318: Sub Kicker5_Hit():UpdateTrough:End Sub
 319: Sub Kicker4_Hit():UpdateTrough:End Sub
 320: Sub Kicker3_Hit():Controller.Switch(25) = 1:UpdateTrough:End Sub
 321: Sub Kicker3_UnHit():Controller.Switch(25) = 0:End Sub
 350: Sub Drain_Hit()
 351: PlaySound "drain"
 352: Controller.Switch(15) = 1
 353: End Sub
 354:
 355: Sub SolOuthole(enabled)
 356: If enabled Then
 357: Drain.kick 70,10
 358: PlaySound SoundFX(SSolenoidOn,DOFContactors)
 359: controller.switch(15) = false
 360: End If
 361: End Sub
 362:
 363: Sub ReleaseBall
 364: PlaySound SoundFX("BallRelease2",DOFContactors)
 365: Kicker1.Kick 70,5
 366: UpdateTrough
 367: End Sub
 374: Sub sw05_Hit():playsound "kicker_enter":controller.Switch(5)=1:End Sub
```

## Flippers

```vbscript
 394: Sub SolLFlipper(Enabled)
 395: If Enabled Then
 396: PlaySound SoundFx("FlipperUp",DOFFlippers)
 397: if Controller.Lamp(16) = 0 Then
 398: LeftFlipper.RotateToEnd
 399: LeftFlipper2.RotateToEnd
 400: Else
 401: LeftFlipper.RotateToStart
 402: LeftFlipper2.RotateToStart
 403: End If
 404: If Controller.Lamp(17) Then
 405: FlipperLL.RotateToEnd
 406: Else
 407: FlipperLL.RotateToStart
 408: End If
 409: Else
 410: PlaySound SoundFx("FlipperDown",DOFFlippers)
 411: LeftFlipper.RotateToStart
 412: LeftFlipper2.RotateToStart
 413: FlipperLL.RotateToStart
 414: End If
 415: End Sub
 416:
 417: Sub SolRFlipper(Enabled)
 418: If Enabled Then
 419: PlaySound SoundFx("FlipperUp",DOFFlippers)
 420: if Controller.Lamp(16) = 0 Then
 421: RightFlipper.RotateToEnd
 422: RightFlipper2.RotateToEnd
 423: Else
 424: RightFlipper.RotateToStart
 425: RightFlipper2.RotateToStart
 426: End If
 427: If Controller.Lamp(17) Then
 428: FlipperLR.RotateToEnd
 429: Else
 430: FlipperLR.RotateToStart
 431: End If
 432: Else
 433: PlaySound SoundFx("FlipperDown",DOFFlippers)
 434: RightFlipper.RotateToStart
 435: RightFlipper2.RotateToStart
 436: FlipperLR.RotateToStart
 437: End If
 438: End Sub
```

## Lamp bindings

```vbscript
 499: Sub Gate_TopLeft_Hit:vpmTimer.PulseSw(24):End Sub ' OK! switch 0
 500: Sub Spinner1_Spin:vpmTimer.PulseSw (16):End Sub
 501:
 502:
 503: 'Confirmed Lights
 504:
 505: Set Lights(3)=L3
 506: Set Lights(4)=L4
 507: Set Lights(5)=L5
 508: Set Lights(7)=L7
 509: Set Lights(19)=L19a
 510: Set Lights(20)=L20a
 511: Set Lights(21)=L21
 512: Set Lights(22)=L22
 513: Set Lights(23)=L23
 514: Set Lights(24)=L24
 515: Set Lights(25)=L25
 516: Set Lights(26)=L26
 517: Set Lights(27)=L27
 518: Set Lights(28)=L28
 519: Set Lights(29)=L29
 520: Set Lights(30)=L30
 521: Set Lights(31)=L31
 522: Set Lights(32)=L32
 523: Set Lights(33)=L33
 524: Set Lights(34)=L34
 525: Set Lights(35)=L35
 526: Set Lights(36)=L36
 527: Set Lights(37)=L37
 528: Set Lights(38)=L38
 529: Set Lights(39)=L39c
 530: Set Lights(40)=L40
 531: Set Lights(41)=L41
 532: Set Lights(42)=L42
 533: Set Lights(43)=L43
 534: Set Lights(44)=L44
 535: Set Lights(45)=L45
 536: Set Lights(46)=L46
 537: Set Lights(48)=L48
 538: Set Lights(49)=L49
 539: Set Lights(50)=L50
 540: Set Lights(51)=L51
 541: Set Lights(138)=L39b
 542: Set Lights(139)=L39c
```

## Rollover, target and drop-target switches

```vbscript
1440: Sub Tri_TopLeft_Hit:Controller.Switch(0)=1:TWTri_TopLeft.transX = -5:End Sub
1441: Sub Tri_TopLeft_unHit:Controller.Switch(0)=0:TWTri_TopLeft.transX = 0:End Sub
1442:
1443:
1444: Sub Tri_TopMid_Hit:Controller.Switch(10)=1:TWTri_TopMid.transX = -5:End Sub
1445: Sub Tri_TopMid_unHit:Controller.Switch(10)=0:TWTri_TopMid.transX = 0:End Sub
1446:
1447:
1448: Sub Tri_TopRight_Hit:Controller.Switch(20)=1:TWTri_TopRight.transX = -5:End Sub
1449: Sub Tri_TopRight_unHit:Controller.Switch(20)=0:TWTri_TopRight.transX = 0:End Sub
1450:
1451:
1452: Sub Tri_MidRightLane_Hit:Controller.Switch(30)=1:TWTri_MidRightLane.transX = -5:End Sub
1453: Sub Tri_MidRightLane_unHit:Controller.Switch(30)=0:TWTri_MidRightLane.transX = 0:End Sub
1454:
1455:
1456: Sub Tri_BlackHole_Hit:Controller.Switch(33)=1:TWBlackHole.transX = -5:End Sub
1457:
1458: Sub Tri_BlackHole_unHit:Controller.Switch(33)=0:TWBlackHole.transX = 0:End Sub
1459:
1460:
1461: Sub Tri_LeftInlane_Hit:Controller.Switch(35)=1:TWLeftInlane.transX = -5:End Sub
1462: Sub Tri_LeftInlane_unHit:Controller.Switch(35)=0:TWLeftInlane.transX = 0:End Sub
1463:
1464:
1465: '''''' Lower
1466:
1467: Sub Tri_sw62_Hit:Controller.Switch(62)=1:End Sub
1468: Sub Tri_sw62_unHit:Controller.Switch(62)=0:End Sub
1469:
1470: Sub sw52_Hit:Controller.Switch(52)=1:End Sub
1471: Sub sw52_unHit:Controller.Switch(52)=0:End Sub
1480: Sub Tsw01_Hit:vpmTimer.PulseSw(1):PTarget1.TransY = -5:Tsw01Step = 1:PlaySound SoundFX("fx_target",DOFTargets):Me.TimerEnabled = 1:End Sub
1492: Sub Tsw11_Hit:vpmTimer.PulseSw(11):PTarget2.TransY = -5:Tsw11Step = 1:PlaySound SoundFX("fx_target",DOFTargets):Me.TimerEnabled = 1:End Sub
1503: Sub Tsw21_Hit:vpmTimer.PulseSw(21):PTarget3.TransY = -5:Tsw21Step = 1:PlaySound SoundFX("fx_target",DOFTargets):Me.TimerEnabled = 1:End Sub
1515: Sub Tsw31_Hit:vpmTimer.PulseSw(31):PTarget4.TransY = -5:Tsw31Step = 1:PlaySound SoundFX("fx_target",DOFTargets):Me.TimerEnabled = 1:End Sub
1536: Sub TargetB_Hit:vpmTimer.PulseSw 3:TargetB.IsDropped = true:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1540: Sub TargetL_Hit:vpmTimer.PulseSw 13:TargetL.IsDropped = true:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1544: Sub TargetA_Hit:vpmTimer.PulseSw 23:TargetA.IsDropped = true:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1548: Sub TargetC_Hit:vpmTimer.PulseSw 4:TargetC.IsDropped = true:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1552: Sub TargetK_Hit:vpmTimer.PulseSw 14:TargetK.IsDropped = true:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1570: Sub TargetH_Hit:vpmTimer.PulseSw 2:TargetH.IsDropped=True:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1574: Sub TargetO_Hit:vpmTimer.PulseSw 12:TargetO.IsDropped=True:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1578: Sub TargetL2_Hit:vpmTimer.PulseSw 22:TargetL2.IsDropped=True:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1582: Sub TargetE_Hit:vpmTimer.PulseSw 32:TargetE.IsDropped=True:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1599: Sub TargetLL40_Hit:vpmTimer.PulseSw 40:pDT_LL40.Z = 220:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1603: Sub TargetLL50_Hit:vpmTimer.PulseSw 50:pDT_LL50.Z = 210:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1607: Sub TargetLL60_Hit:vpmTimer.PulseSw 60:pDT_LL60.Z = 200:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1611: Sub TargetLL70_Hit:vpmTimer.PulseSw 70:pDT_LL70.Z = 190:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1628: Sub TargetLR41_Hit:vpmTimer.PulseSw 41:pDT_LL41.Z = 175:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1632: Sub TargetLR51_Hit:vpmTimer.PulseSw 51:pDT_LL51.Z = 180:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
1636: Sub TargetLR61_Hit:vpmTimer.PulseSw 61:pDT_LL61.Z = 185:Me.TimerEnabled = 1:PlaySound SoundFX("droptarget",DOFDropTargets):End Sub
```

## Pop bumpers and slingshots

```vbscript
1656: Sub Bumper1_Hit:vpmTimer.PulseSw(6):bump1 = 1:PlaySound SoundFX("DR BumperL",DOFContactors):DOF 101, DOFPulse:End Sub
1657: Sub Bumper2_Hit:vpmTimer.PulseSw(6):bump2 = 1:PlaySound SoundFX("Bumper",DOFContactors):DOF 102, DOFPulse:End Sub
1658: Sub Bumper3_Hit:vpmTimer.PulseSw(6):bump3 = 1:PlaySound SoundFX("DR BumperR",DOFContactors):DOF 103, DOFPulse:End Sub
1659: Sub Bumper4_Hit:vpmTimer.PulseSw(6):bump4 = 1:PlaySound SoundFX("DR BumperL",DOFContactors):DOF 104, DOFPulse:End Sub
1660: Sub Bumper5_Hit:vpmTimer.PulseSw(71):bump5 = 1:PlaySound SoundFX("DR BumperL",DOFContactors):DOF 105, DOFPulse:End Sub
1661: Sub Bumper6_Hit:vpmTimer.PulseSw(71):bump6 = 1:PlaySound SoundFX("DR BumperR",DOFContactors):DOF 106, DOFPulse:End Sub
1751: Sub Sling3_Hit:vpmTimer.PulseSw(34) End Sub
1753: Sub Sling4_Hit:vpmTimer.PulseSw(34):Sling4Step = 0:Rubber9.Visible = False:LeafSwitch1b.ObjRotX = -3:Rubber9a.Visible = True:Me.TimerEnabled = true:End Sub
1757: Sub Sling5_Hit:vpmTimer.PulseSw(34):Sling5Step = 0:Rubber19.Visible = False:LeafSwitch2b.ObjRotX = -3:Rubber19a.Visible = True:Me.TimerEnabled = true:End Sub
1762: Sub Sling6_Hit:vpmTimer.PulseSw(34):Sling6Step = 0:Rubber10.Visible = False:LeafSwitch3b.ObjRotX = -3:Rubber10a.Visible = True:Me.TimerEnabled = true: End Sub
1764: Sub Sling9_Hit:vpmTimer.PulseSw(72) End Sub
1770: Sub Sling1_slingshot:vpmTimer.PulseSw(34):PlaySound SoundFX("slingshot2",DOFContactors):DOF 107, DOFPulse:Sling1a.visible = false:pSling1.TransZ = -8:Sling1b.visible = true:Sling1Step = 0:Me.TimerEnabled = 1:End Sub
1785: Sub Sling2_slingshot:vpmTimer.PulseSw(34):PlaySound SoundFX("slingshot1",DOFContactors):DOF 108, DOFPulse:Sling2a.visible = false:pSling2.TransZ = -8:Sling2b.visible = true:Sling2Step = 0:Me.TimerEnabled = 1:End Sub
1856: Sub Sling7_slingshot:vpmTimer.PulseSw(72):TSling7.timerEnabled = 0:Sling7Step2 = 0:Me.TimerEnabled = 1:End Sub
1898: Sub Sling8_slingshot:vpmTimer.PulseSw(72):PlaySound SoundFX("slingshot2",DOFContactors):DOF 111, DOFPulse:Sling8a.visible = false:pSling8.TransZ = -8:Sling8b.visible = true:Sling8Step = 0:Me.TimerEnabled = 1:End Sub
```

## ChangedLamps loop and lamp updates

```vbscript
2123: Sub LampTimer_Timer()
2124: Dim chgLamp, num, chg, ii
2125: chgLamp = Controller.ChangedLamps
2126: If Not IsEmpty(chgLamp) Then
2127: For ii = 0 To UBound(chgLamp)
2128: LampState(chgLamp(ii, 0) ) = chgLamp(ii, 1)
2129: FadingLevel(chgLamp(ii, 0) ) = chgLamp(ii, 1) + 4
2130: FlashState(chgLamp(ii, 0) ) = chgLamp(ii, 1)
2131: CheckSolenoid chgLamp(ii, 0),chgLamp(ii, 1)
2132: Next
2133: End If
2134: UpdateLamps
2135: End Sub
2137: Sub UpdateLamps
2138:
2139: NFadeLm 2, BLight1b
2140: NFadeLm 2, BLight2b
2141: NFadeLm 2, BLight3b
2142: NFadeLm 2, BLight4b
2143: FadePri4m 2, PBumpCap1, BArrayDay
2144: FadePri4m 2, PBumpCap2, BArrayDay
2145: FadePri4m 2, PBumpCap3, BArrayDay
2146: FadePri4 2, PBumpCap4, BArrayDay
2147: FadePri4m 17, PBumpCap5, BArrayDay
2148: FadePri4 17, PBumpCap6, BArrayDay
2149:
2150: If TubeGlow = 1 then
2151: FadeDisableLighting 123, ReEnetryTube
2152: FadePri4 123, ReEnetryTube, ReEnetryTubeArray
2153: End If
2154:
2155: 'Upper playfield lights
2156:
2157: NFadeL 3, L3
2158: NFadeL 7, L7
2159: NFadeL 21, L21
2160: NFadeL 22, L22
2161: NFadeL 23, L23
2162: NFadeL 24, L24
2163: NFadeL 25, L25
2164: NFadeL 26, L26
2165: NFadeL 27, L27
2166: NFadeL 28, L28
2167: NFadeL 29, L29
2168: NFadeL 30, L30
2169: NFadeL 31, L31
2170: NFadeL 32, L32
2171: NFadeL 33, L33
2172: NFadeL 34, L34
2173: NFadeL 35, L35
2174: NFadeL 36, L36
2175: If CaptiveLight = 0 then
2176: Else
2177: NFadeLm 37, LCaptiveLight
2178: End If
2179: NFadeL 37, L37
2180: NFadeL 38, L38
2181: NFadeL 39, L39c
2182: NFadeL 40, L40
2183: NFadeL 41, L41
2184: NFadeL 42, L42
2185: NFadeL 43, L43
2186: '
2187: NFadeL 48, L48
2188: NFadeL 49, L49
2189: NFadeL 50, L50
2190: NFadeL 51, L51
2191: NFadeL 138, L39a
2192: NFadeL 139, L39b
2193:
2194:
2195:
2196:
2197:
2198: ' Lower playfield lights
2199:
2200: FadeFlash 4, L4, RedLight
2201: FadeFlash 5, L5, OrangeLight
2202: FadeFlash 6, L6, OrangeLight
2203: FadeFlashm 19, L19c, BlueLightL
2204: FadeFlashm 19, L19b, BlueLightL
2205: FadeFlash 19, L19a, BlueLightL
2206: FadeFlashm 20, L20c, BlueLightR
2207: FadeFlashm 20, L20b, BlueLightR
2208: FadeFlash 20, L20a, BlueLightR
2209: FadeFlash 47, L47, YellowLight
2210: FadeFlash 46, L46, YellowLight
2211: FadeFlash 45, L45, YellowLight
2212: FadeFlash 44, L44, YellowLight
2213:
2283: Sub FlasherTimer_Timer()
2284:
2285:
2286: '***GI
2287: Flashm 17, lgi1
2288: Flashm 17, lgi2
2289: Flashm 17, lgi3
2290: Flashm 17, lgi4
2291:
2292: Flashm 17, Flasher20
2293: Flashm 17, Flasher21
2294: Flashm 17, Flasher22
2295: Flashm 17, Flasher23
2296: Flashm 17, Flasher24
2297: Flashm 17, Flasher25
2298: Flashm 17, Flasher26
2299:
2300: Flash 17, Flasher27
```
