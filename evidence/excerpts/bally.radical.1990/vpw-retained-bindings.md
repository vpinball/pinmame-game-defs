# Retained VPW1.0.1 mechanism and dome bindings

Line numbers are retained; trailing whitespace and final blank lines are normalized.

Exact script SHA256 17c0f0141b07ee83b3911150e3597e0cba26f83d0e735e4b81946500e582a7eb. Source table SHA256 3ea276adc2a39ae3fbc05695a2925eefb3f77a52bdee4ad2811ed547312b595f. Acquisition: 2026-11-06T08:50:19.346143Z from https://vpuniverse.com/files/file/6523-radical-bally-1990-prototype-vpw-mod/. Attribution: JPSalas, 32assassin, VPinWorkshop and credited contributors. No redistribution license established; only relevant script fragments retained. Method: exact numbered source extraction, reviewed by primary curator, 2026-11-06.

This table is a descendant of the older JPSalas geometry. It supplies its own modeled bulb/dome/mechanism locations, not independent corroboration. Script-selected object centers are normalized by the shared helper. The default upper-sling option and forced2500ms popper ejection are table behavior; neither proves factory timing. ObjLevel1/2 both belong to public32; Flasherbase objects are dome bases, not the similarly named glow sprites.

## Lines 143-194

```vb
143:     vpmNudge.Sensitivity = 3
144:     vpmNudge.TiltObj = Array(Bumper1, Bumper2, Bumper3, Bumper4, LeftSlingshot, RightSlingshot, RightSlingshot1)
145:     ' Trough
146:     Set bsTrough = New cvpmBallStack
147:     With bsTrough
148:         .InitSw 10, 11, 12, 0, 0, 0, 0, 0
149:         .InitKick BallRelease, 80, 6
150:         '.InitEntrySnd "fx_drain", "fx_Solenoid"
151:         .InitExitSnd SoundFX("fx_ballrel", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
152:         .Balls = 2
153:     End With
154:
155:     ' Visible Lock
156:     Set bsLock = new cvpmVLock
157:     With bsLock
158:         .InitVLock Array(sw40, sw39), Array(sw40k, sw39k), Array(40, 39)
159:         .InitSnd SoundFX("fx_kicker", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
160:         .ExitDir = 0
161:         .ExitForce = 21
162:         .CreateEvents "bsLock"
163:     End With
164:
165:     ' Top Eject Hole 'Not available in the latest ROMs, we activate it manually
166:     Set bsTP = New cvpmBallStack
167:     With bsTP
168:     .InitSw 0, 16, 0, 0, 0, 0, 0, 0
169:     .InitKick sw16, 0, 55
170: 	.KickZ = 1.5
171:     .InitExitSnd SoundFX("fx_popper", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
172:     End With
173:
174:     ' Drop Middle targets
175:     set dtbankM = new cvpmdroptarget
176:     With dtbankM
177:         .initdrop array(sw22, sw23, sw24), array(22, 23, 24)
178:         .initsnd SoundFX("", DOFDropTargets), SoundFX("fx_resetdrop", DOFContactors)
179:         .CreateEvents "dtbankM"
180:     End With
181:
182:     ' Drop Top targets
183:     set dtbankT = new cvpmdroptarget
184:     With dtbankT
185:         .initdrop array(sw30, sw31, sw32), array(30, 31, 32)
186:         .initsnd SoundFX("", DOFDropTargets), SoundFX("fx_resetdrop", DOFContactors)
187:         .CreateEvents "dtbankT"
188:     End With
189:
190:     ' Impulse Plunger used for kickback
191:     Const IMPowerSetting = 42 'Plunger Power
192:     Const IMTime = 0.3        ' Time in seconds for Full Plunge
193:     Set plungerIM = New cvpmImpulseP
194:     With plungerIM
```

## Lines 304-333

```vb
304: Sub RightSlingShot1_Slingshot
305:     if DisableUpperSling = 0 Then
306: 		PlaySound SoundFX("fx_slingshot", DOFContactors), 0, 1, 0.05, 0.05
307: 		r6.Visible = 1
308: 		Remk1.RotX = 26
309: 		RStep1 = 0
310: 		vpmTimer.PulseSw 49
311: 		RightSlingShot1.TimerEnabled = 1
312: 	end if
313: End Sub
314:
315: Sub RightSlingShot1_Timer
316:     Select Case RStep1
317:         Case 1:r6.Visible = 0:r4.Visible = 1:Remk1.RotX = 14
318:         Case 2:r4.Visible = 0:r3.Visible = 1:Remk1.RotX = 2
319:         Case 3:r3.Visible = 0:Remk1.RotX = -20:RightSlingshot1.TimerEnabled = 0
320:     End Select
321:     RStep1 = RStep1 + 1
322: End Sub
323:
324: ' Bumpers
325: Sub Bumper1_Hit:vpmTimer.PulseSw 52:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, -0.05:End Sub
326: Sub Bumper2_Hit:vpmTimer.PulseSw 50:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, -0.02:End Sub
327: Sub Bumper3_Hit:vpmTimer.PulseSw 54:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, -0.05:End Sub
328: Sub Bumper4_Hit:vpmTimer.PulseSw 53:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, -0.02:End Sub
329:
330: ' Drain & Saucers
331: Sub Drain_Hit:Playsound "fx_drain":bsTrough.AddBall Me:End Sub
332: Sub sw16a_Hit:PlaySound "fx_hole_enter", 0, 1, -0.02:bsTP.AddBall Me:vpmTimer.AddTimer 2500, "EjectBall":End Sub
333: Sub EjectBall(swno):PlaySound "fx_popper", 0, 1, -0.05:bsTP.ExitSol_On:End Sub
```

## Lines 423-505

```vb
423: SolCallback(1) = "bsTrough.SolIn"
424: SolCallback(2) = "bsTrough.SolOut"
425: SolCallback(3) = "bsTP.SolOut" 'Not used in the latest ROMs
426: SolCallback(4) = "dtBankT.SolDropUp"
427: SolCallback(6) = "dtBankM.SolDropUp"
428: SolCallback(5) = "VpmSolSound SoundFX(""fx_knocker"",DOFKnocker),"
429: SolCallback(7) = "SolRampDiv"
430: SolCallback(8) = "bsLock.SolExit" 'vlock
431: SolCallback(10) = "SolGI"
432: SolCallback(13) = "vpmSolToggleWall RightDiverter2,RightDiverter1,""fx_diverter"","
433: SolCallback(14) = "SolKickBack"
434: SolCallback(23) = "vpmNudge.SolGameOn"
435:
436: ' flashers
437: SolCallback(9) = "FlashPurpleMiddleRight" '"SetLamp 90,"
438: SolCallback(16) = "SetLamp 116,"
439: SolCallback(25) = "FlashPurpleLeftBottom"'"SetLamp 125,"
440: SolCallback(26) = "FlashGreenLeftBottom"'126
441: SolCallback(27) = "FlashPurpleMiddleLeft"'"SetLamp 127,"
442: SolCallback(28) = "FlashGreenLeftTop" '"SetLamp 128,"
443: SolCallback(29) = "FlashWhiteBack" '"SetLamp 129,"
444: SolCallback(30) = "FlashPurpleMiddleTop"'"SetLamp 130,"
445: SolCallback(31) = "FlashGreenTop" '"SetLamp 131,"
446: SolCallback(32) = "FlashGreenRight" '"SetLamp 132,"
447:
448:
449: Sub FlashGreenRight(flstate)
450: 	If Flstate Then
451: 		Objlevel(1) = 1 : FlasherFlash1_Timer
452: 		Objlevel(2) = 1 : FlasherFlash2_Timer
453: 	End If
454: End Sub
455:
456: Sub FlashGreenTop(flstate)
457: 	If Flstate Then
458: 		Objlevel(3) = 1 : FlasherFlash3_Timer
459: 	End If
460: End Sub
461:
462: Sub FlashGreenLeftTop(flstate)
463: 	If Flstate Then
464: 		Objlevel(4) = 1 : FlasherFlash4_Timer
465: 	End If
466: End Sub
467:
468: Sub FlashGreenLeftBottom(flstate)
469: 	If Flstate Then
470: 		Objlevel(5) = 1 : FlasherFlash5_Timer
471: 	End If
472: End Sub
473:
474: Sub FlashPurpleLeftBottom(flstate)
475: 	If Flstate Then
476: 		Objlevel(6) = 1 : FlasherFlash6_Timer
477: 	End If
478: End Sub
479:
480: Sub FlashPurpleMiddleLeft(flstate)
481: 	If Flstate Then
482: 		Objlevel(7) = 1 : FlasherFlash7_Timer
483: 	End If
484: End Sub
485:
486: Sub FlashPurpleMiddleTop(flstate)
487: 	If Flstate Then
488: 		Objlevel(8) = 1 : FlasherFlash8_Timer
489: 	End If
490: End Sub
491:
492: Sub FlashPurpleMiddleRight(flstate)
493: 	If Flstate Then
494: 		Objlevel(9) = 1 : FlasherFlash9_Timer
495: 	End If
496: End Sub
497:
498: Sub FlashWhiteBack(flstate)
499: 	If Flstate Then
500: 		Objlevel(10) = 1 : FlasherFlash10_Timer
501: 	End If
502: End Sub
503:
504: 'Solenoid Subs
505:
```

## Lines 1187-1198

```vb
1187: 'initialise the flasher color, you can only choose from "green", "red", "purple", "blue", "white" and "yellow"
1188: InitFlasher 1, "green"
1189: InitFlasher 2, "green"
1190: InitFlasher 3, "green"
1191: InitFlasher 4, "green"
1192: InitFlasher 5, "green"
1193: InitFlasher 6, "purple"
1194: InitFlasher 7, "purple"
1195: InitFlasher 8, "purple"
1196: InitFlasher 9, "purple"
1197: InitFlasher 10, "white"
1198:
```

## Lines 1215-1234

```vb
1215: Sub InitFlasher(nr, col)
1216: 	' store all objects in an array for use in FlashFlasher subroutine
1217: 	Set objbase(nr) = Eval("Flasherbase" & nr) : Set objlit(nr) = Eval("Flasherlit" & nr)
1218: 	Set objflasher(nr) = Eval("Flasherflash" & nr) : Set objlight(nr) = Eval("Flasherlight" & nr)
1219: 	' If the flasher is parallel to the playfield, rotate the VPX flasher object for POV and place it at the correct height
1220: 	If objbase(nr).RotY = 0 Then
1221: 		objbase(nr).ObjRotZ =  atn( (tablewidth/2 - objbase(nr).x) / (objbase(nr).y - tableheight*1.1)) * 180 / 3.14159
1222: 		objflasher(nr).RotZ = objbase(nr).ObjRotZ : objflasher(nr).height = objbase(nr).z + 60
1223: 	End If
1224: 	' set all effects to invisible and move the lit primitive at the same position and rotation as the base primitive
1225: 	objlight(nr).IntensityScale = 0 : objlit(nr).visible = 0 : objlit(nr).material = "Flashermaterial" & nr
1226: 	objlit(nr).RotX = objbase(nr).RotX : objlit(nr).RotY = objbase(nr).RotY : objlit(nr).RotZ = objbase(nr).RotZ
1227: 	objlit(nr).ObjRotX = objbase(nr).ObjRotX : objlit(nr).ObjRotY = objbase(nr).ObjRotY : objlit(nr).ObjRotZ = objbase(nr).ObjRotZ
1228: 	objlit(nr).x = objbase(nr).x : objlit(nr).y = objbase(nr).y : objlit(nr).z = objbase(nr).z
1229: 	objbase(nr).BlendDisableLighting = FlasherOffBrightness
1230: 	' set the texture and color of all objects
1231: 	select case objbase(nr).image
1232: 		Case "dome2basewhite" : objbase(nr).image = "dome2base" & col : objlit(nr).image = "dome2lit" & col :
1233: 		Case "ronddomebasewhite" : objbase(nr).image = "ronddomebase" & col : objlit(nr).image = "ronddomelit" & col
1234: 		Case "domeearbasewhite" : objbase(nr).image = "domeearbase" & col : objlit(nr).image = "domeearlit" & col
```
