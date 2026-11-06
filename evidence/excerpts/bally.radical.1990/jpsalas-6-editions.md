# JPSalas Radical 6.0.0 edition overlay

Line numbers are retained; trailing whitespace and final blank lines are normalized.

Source page https://www.vpforums.org/index.php?app=downloads&showfile=13694, file130225. Source table SHA2568684ab7b113a3fdc5cdfb104e0b6da847ca571b985052d06870909b56cc16a13; script SHA2562c2c2c26c6922c08c3d09a9f6633aa0712219a18a345c9864f0eb341ed28619a. Acquired2026-11-06T09:10:25.511776Z; JPSalas and credited original/redraw/ramp contributors retain copyright. Relevant factual script regions only. Extracted with vpxtool git:v0.33.3, manually reviewed by primary curator.

This later edit shares ancestry and bounds with the old JPSalas and VPW tables. It is supplementary geometry/edition evidence, not independent validation. The player option changes collision/visibility for the production target versus prototype receiver and sling; changing the option does not select a different ROM automatically. Popper entry and remote outlet are distinct objects. f16 is still a bulbless glow, not a physical socket.

## Lines 101-123

```vb
101:         .ExitDir = 0
102:         .ExitForce = 21
103:         .CreateEvents "bsLock"
104:     End With
105:
106:     ' Top Eject Hole 'Not available in the latest ROMs, we activate it manually
107:     Set bsTP = New cvpmBallStack
108:     With bsTP
109:         .InitSw 0, 16, 0, 0, 0, 0, 0, 0
110:         .InitKick sw16, 0, 55
111:         .KickZ = 1.5
112:         .InitExitSnd SoundFX("fx_popper", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
113:     End With
114:
115:     ' Drop Middle targets
116:     set dtbankM = new cvpmdroptarget
117:     With dtbankM
118:         .initdrop array(sw22, sw23, sw24), array(22, 23, 24)
119:         .initsnd SoundFX("fx_droptarget", DOFDropTargets), SoundFX("fx_resetdrop", DOFContactors)
120:         .CreateEvents "dtbankM"
121:     End With
122:
123:     ' Drop Top targets
```

## Lines 215-238

```vb
215:     vpmTimer.PulseSw 56
216:     RightSlingShot.TimerEnabled = 1
217: End Sub
218:
219: Sub RightSlingShot_Timer
220:     Select Case RStep
221:         Case 1:RightSLing4.Visible = 0:RightSLing3.Visible = 1:Remk.RotX = 14
222:         Case 2:RightSLing3.Visible = 0:RightSLing2.Visible = 1:Remk.RotX = 2
223:         Case 3:RightSLing2.Visible = 0:Remk.RotX = -20:RightSlingShot.TimerEnabled = 0
224:     End Select
225:     RStep = RStep + 1
226: End Sub
227:
228: Sub RightSlingShot1_Slingshot
229:     PlaySoundAt SoundFX("fx_slingshot", DOFContactors), Remk1
230:     r6.Visible = 1
231:     Remk1.RotX = 26
232:     RStep1 = 0
233:     vpmTimer.PulseSw 49
234:     RightSlingShot1.TimerEnabled = 1
235: End Sub
236:
237: Sub RightSlingShot1_Timer
238:     Select Case RStep1
```

## Lines 306-341

```vb
306: SolCallback(1) = "bsTrough.SolIn"
307: SolCallback(2) = "bsTrough.SolOut"
308: SolCallback(3) = "bsTP.SolOut" 'Not used in the latest ROMs
309: SolCallback(4) = "dtBankT.SolDropUp"
310: SolCallback(6) = "dtBankM.SolDropUp"
311: SolCallback(5) = "VpmSolSound SoundFX(""fx_knocker"",DOFKnocker),"
312: SolCallback(7) = "SolRampDiv"
313: SolCallback(8) = "bsLock.SolExit" 'vlock
314: SolCallback(10) = "SolGI"
315: SolCallback(13) = "vpmSolToggleWall RightDiverter2,RightDiverter1,""fx_diverter"","
316: SolCallback(14) = "SolKickBack"
317: SolCallback(23) = "vpmNudge.SolGameOn"
318:
319: ' flashers
320: If UseVPMModSol Then
321: SolModCallback(9) = "Flasher9"
322: SolModCallback(16) = "Flasher16"
323: SolModCallback(25) = "Flasher25"
324: SolModCallback(26) = "Flasher26"
325: SolModCallback(27) = "Flasher27"
326: SolModCallback(28) = "Flasher28"
327: SolModCallback(29) = "Flasher29"
328: SolModCallback(30) = "Flasher30"
329: SolModCallback(31) = "Flasher31"
330: SolModCallback(32) = "Flasher32"
331: Else
332: SolCallback(9) = "vpmFlasher f9a,"
333: SolCallback(16) = "vpmFlasher f16,"
334: SolCallback(25) = "vpmFlasher f25a,"
335: SolCallback(26) = "vpmFlasher f26a,"
336: SolCallback(27) = "vpmFlasher f27a,"
337: SolCallback(28) = "vpmFlasher f28a,"
338: SolCallback(29) = "vpmFlasher f29a,"
339: SolCallback(30) = "vpmFlasher f30a,"
340: SolCallback(31) = "vpmFlasher f31a,"
341: SolCallback(32) = "vpmFlasher Array(f32c,f32a),"
```

## Lines 1037-1070

```vb
1037:     ' Prototype table
1038:     x = Table1.Option("Prototype table", 0, 1, 1, 1, 0, Array("No", "Yes") )
1039:     If x Then
1040:         RightSlingshot2.IsDropped = 1
1041:         RightSlingshot1.IsDropped = 0
1042:         sw16b.Collidable = 0
1043:         sw16b.Visible = 0
1044:         sw16a.Enabled = 1
1045:         Ramp28.Visible = 1
1046:         Ramp30.Visible = 1
1047:         Ramp33.Visible = 1
1048:         Rubber12.Visible = 1
1049:         Rubber14.Visible = 1
1050:         Rubber2.Visible = 1
1051:         Rubber1.Visible = 1
1052:         Ramp27.Visible = 1
1053:     Else
1054:         RightSlingshot2.IsDropped = 0
1055:         RightSlingshot1.IsDropped = 1
1056:         sw16b.Collidable = 1
1057:         sw16b.Visible = 1
1058:         sw16a.Enabled = 0
1059:         Ramp28.Visible = 0
1060:         Ramp30.Visible = 0
1061:         Ramp33.Visible = 0
1062:         Rubber12.Visible = 0
1063:         Rubber14.Visible = 0
1064:         Rubber2.Visible = 0
1065:         Rubber1.Visible = 0
1066:         Ramp27.Visible = 0
1067:     End If
1068: End Sub
1069:
1070: Sub UpdateLUT
```
