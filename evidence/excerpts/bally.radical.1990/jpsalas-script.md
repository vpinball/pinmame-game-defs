# JPSalas Radical table: selected script lines

Line numbers are retained; trailing whitespace and final blank lines are normalized.

Extracted `script.vbs`, SHA-256 `7e4e81501c8713589ce21c0d1b3b136122357145056cf62c4ecf5212c1b5e584`, from retained `Radical! (Bally 1990).vpx` via vpxtool. Line numbers refer to that extraction. Table authors retain copyright; no redistribution license asserted. These are relevant fragments, not the full script. The ROM selection comments are preserved literally and do not themselves prove physical compatibility.

```vb
17: Dim bsTrough, dtBankM, dtBankT, bsLock, bsTP, plungerIM, x
18:
19: Const cGameName = "radcl_l1" 'Latest rom
20: 'Const cGameName = "radcl_lg1" 'German
21: 'Const cGameName = "radcl_g1"  ' ?
22: 'Const cGameName = "radcl_p3"  'Prototype home
87:     Set bsTrough = New cvpmBallStack
88:     With bsTrough
89:         .InitSw 10, 11, 12, 0, 0, 0, 0, 0
90:         .InitKick BallRelease, 80, 6
91:         '.InitEntrySnd "fx_drain", "fx_Solenoid"
92:         .InitExitSnd SoundFX("fx_ballrel", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
93:         .Balls = 2
94:     End With
95:
96:     ' Visible Lock
97:     Set bsLock = new cvpmVLock
98:     With bsLock
99:         .InitVLock Array(sw40, sw39), Array(sw40k, sw39k), Array(40, 39)
100:         .InitSnd SoundFX("fx_kicker", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
101:         .ExitDir = 0
102:         .ExitForce = 21
103:         .CreateEvents "bsLock"
104:     End With
105:
106:     ' Drop Middle targets
107:     set dtbankM = new cvpmdroptarget
108:     With dtbankM
109:         .initdrop array(sw22, sw23, sw24), array(22, 23, 24)
110:         .initsnd SoundFX("", DOFDropTargets), SoundFX("fx_resetdrop", DOFContactors)
111:         .CreateEvents "dtbankM"
112:     End With
113:
114:     ' Drop Top targets
115:     set dtbankT = new cvpmdroptarget
116:     With dtbankT
117:         .initdrop array(sw30, sw31, sw32), array(30, 31, 32)
118:         .initsnd SoundFX("", DOFDropTargets), SoundFX("fx_resetdrop", DOFContactors)
119:         .CreateEvents "dtbankT"
120:     End With
123:     Const IMPowerSetting = 42 'Plunger Power
124:     Const IMTime = 0.3        ' Time in seconds for Full Plunge
125:     Set plungerIM = New cvpmImpulseP
126:     With plungerIM
127:         .InitImpulseP sw51, IMPowerSetting, IMTime
128:         .Random 0.3
129:         .switch 51
130:         .InitExitSnd "fx_Solenoid", "fx_Solenoid"
131:         .CreateEvents "plungerIM"
132:     End With
133:
134:     ' Init diverters
135:     DiverterDown.IsDropped = 1
136:     RightDiverter1.IsDropped = 1
217: Sub Drain_Hit:Playsound "fx_drain":bsTrough.AddBall Me:End Sub
253: ' Spinners
254: Sub Spinner1_Spin:vpmTimer.PulseSw 29:PlaySound "fx_spinner", 0, 1, 0.05:End Sub
255: Sub Spinner2_Spin:vpmTimer.PulseSw 17:PlaySound "fx_spinner", 0, 1, -0.05:End Sub
256:
257: 'Targets
258: Sub sw28_Hit:vpmTimer.PulseSw 28:PlaySound SoundFX("fx_target", DOFDropTargets), 0, 1, pan(ActiveBall):End Sub
259: Sub sw43_Hit:vpmTimer.PulseSw 43:PlaySound SoundFX("fx_target", DOFDropTargets), 0, 1, pan(ActiveBall):End Sub
260: Sub sw44_Hit:vpmTimer.PulseSw 44:PlaySound SoundFX("fx_target", DOFDropTargets), 0, 1, pan(ActiveBall):End Sub
261: Sub sw16_Hit:vpmTimer.PulseSw 16:PlaySound SoundFX("fx_target", DOFDropTargets), 0, 1, pan(ActiveBall):End Sub
276: SolCallback(1) = "bsTrough.SolIn"
277: SolCallback(2) = "bsTrough.SolOut"
278: SolCallback(3) = "bsTP.SolOut" 'Not used in the latest ROMs
279: SolCallback(4) = "dtBankT.SolDropUp"
280: SolCallback(6) = "dtBankM.SolDropUp"
281: SolCallback(5) = "VpmSolSound SoundFX(""fx_knocker"",DOFKnocker),"
282: SolCallback(7) = "SolRampDiv"
283: SolCallback(8) = "bsLock.SolExit" 'vlock
284: SolCallback(10) = "SolGI"
285: SolCallback(13) = "vpmSolToggleWall RightDiverter2,RightDiverter1,""fx_diverter"","
286: SolCallback(14) = "SolKickBack"
287: SolCallback(23) = "vpmNudge.SolGameOn"
288:
289: ' flashers
290: SolCallback(9) = "SetLamp 90,"
291: SolCallback(16) = "SetLamp 116,"
292: SolCallback(25) = "SetLamp 125,"
293: SolCallback(26) = "SetLamp 126,"
294: SolCallback(27) = "SetLamp 127,"
295: SolCallback(28) = "SetLamp 128,"
296: SolCallback(29) = "SetLamp 129,"
297: SolCallback(30) = "SetLamp 130,"
298: SolCallback(31) = "SetLamp 131,"
299: SolCallback(32) = "SetLamp 132,"
300:
301: 'Solenoid Subs
302:
303: Sub SolRampDiv(Enabled)
304:     If Enabled Then
305:         If DiverterDown.IsDropped Then
306:             Controller.Switch(20) = 1
307:             DiverterDown.IsDropped = 0
308:             DiverterUp.IsDropped = 1
309:         Else
310:             Controller.Switch(20) = 0
311:             DiverterDown.IsDropped = 1
312:             DiverterUp.IsDropped = 0
313:         End If
314:     End If
315: End Sub
316:
317: Sub SolKickBack(Enabled)
318:     If Enabled Then
319:         PlungerIM.AutoFire
320:     End If
321: End Sub
322:
323: Sub SolGi(enabled)
324:     If enabled Then
325:         GiOff
326:     Else
327:         GiOn
```
