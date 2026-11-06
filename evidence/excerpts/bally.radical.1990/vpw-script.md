# VPW prototype script: selected lines

Line numbers are retained; trailing whitespace and final blank lines are normalized.

`Radical (Bally 1990) Prototype _VPWmod_v1.0.1.vbs`, corpus revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `04c23692dad50b977cc2ebc529a66248a4e31b38a1286f0b870bfb24c079b593`. Attribution: table and script authors; no redistribution license asserted. These fragments corroborate modeled runtime behavior, not playfield coordinates or physical timing.

```vb
25: ' Thalamus - added more randomness to kickers
26:
27: 'Disables the upper sling making the table more like the retail version instead of prototype
28: Const DisableUpperSling = 1
146:     ' Trough
147:     Set bsTrough = New cvpmBallStack
148:     With bsTrough
149:         .InitSw 10, 11, 12, 0, 0, 0, 0, 0
150:         .InitKick BallRelease, 80, 6
151:         '.InitEntrySnd "fx_drain", "fx_Solenoid"
152:         .InitExitSnd SoundFX("fx_ballrel", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
153:         .Balls = 2
154:     End With
155:
156:     ' Visible Lock
157:     Set bsLock = new cvpmVLock
158:     With bsLock
159:         .InitVLock Array(sw40, sw39), Array(sw40k, sw39k), Array(40, 39)
160:         .InitSnd SoundFX("fx_kicker", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
161:         .ExitDir = 0
162:         .ExitForce = 21
163:         .CreateEvents "bsLock"
164:     End With
165:
166:     ' Top Eject Hole 'Not available in the latest ROMs, we activate it manually
167:     Set bsTP = New cvpmBallStack
168:     With bsTP
169:     .InitSw 0, 16, 0, 0, 0, 0, 0, 0
170:     .InitKick sw16, 0, 55
171:     .KickZ = 1.5
172:     .InitExitSnd SoundFX("fx_popper", DOFContactors), SoundFX("fx_Solenoid", DOFContactors)
173:     .KickForceVar = 3
174:     .KickAngleVar = 3
175:     End With
303:     End Select
304:     RStep = RStep + 1
305: End Sub
306:
307: Sub RightSlingShot1_Slingshot
308:     if DisableUpperSling = 0 Then
309:     PlaySound SoundFX("fx_slingshot", DOFContactors), 0, 1, 0.05, 0.05
310:     r6.Visible = 1
311:     Remk1.RotX = 26
312:     RStep1 = 0
333: ' Drain & Saucers
334: Sub Drain_Hit:Playsound "fx_drain":bsTrough.AddBall Me:End Sub
335: Sub sw16a_Hit:PlaySound "fx_hole_enter", 0, 1, -0.02:bsTP.AddBall Me:vpmTimer.AddTimer 2500, "EjectBall":End Sub
336: Sub EjectBall(swno):PlaySound "fx_popper", 0, 1, -0.05:bsTP.ExitSol_On:End Sub
425:
426: SolCallback(1) = "bsTrough.SolIn"
427: SolCallback(2) = "bsTrough.SolOut"
428: SolCallback(3) = "bsTP.SolOut" 'Not used in the latest ROMs
429: SolCallback(4) = "dtBankT.SolDropUp"
430: SolCallback(6) = "dtBankM.SolDropUp"
431: SolCallback(5) = "VpmSolSound SoundFX(""fx_knocker"",DOFKnocker),"
432: SolCallback(7) = "SolRampDiv"
```
