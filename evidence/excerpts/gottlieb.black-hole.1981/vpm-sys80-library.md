# VPinMAME sys80.vbs — System 80 constants and key handlers

Source: `sys80.vbs` ("Last Updated in VBS v3.61", 144 lines, SHA-256
`5e14a206222039389c220aac40bf410e35fd7c730786bb6686d1b8ab6494de8c`), the VPinMAME System 80 script library the retained
Black Hole table loads with `LoadVPM "00990300", "sys80.VBS", 2.33`, copied byte for byte from the contributor's
working Visual Pinball `Scripts` installation into the working root's `review-artifacts/vpm-script-libs/`. It executes
the `core.vbs` retained beside it. Lines quoted verbatim with their numbers, tabs normalized to spaces.

```vbscript
 18: ' SYS80 Data
 19: '-------------------------
 20: ' Flipper Solenoid
 21: Const GameOnSolenoid = 10
 22: 'Cabinet Switches
 23: Const swTest = 07
 24: Const swCoin1 = 17
 25: Const swCoin2 = 27
 26: Const swCoin3 = 37
 27: Const swStartButton = 47
 28: Const swTilt = 57
 29: Const swSlamTilt = -1
 30:
 31: Const swLRFlip = 112
 32: Const swLLFlip = 114
 33: Const swURFlip = 113
 34: Const swULFlip = 115
 82: Function vpmKeyDown(ByVal keycode)
 83: vpmKeyDown = True ' assume we handle the key
 84: With Controller
 85: Select Case keycode
 86: Case LeftFlipperKey
 87: .Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
 88: If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
 89: vpmFlips.FlipUL True
 90: If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
 91: End If
 92: Case RightFlipperKey
 93: .Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
 94: If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
 95: vpmFlips.FlipUR True
 96: If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
 97: End If
 98: Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
 99: Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
100: Case keyInsertCoin1 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
101: Case keyInsertCoin2 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
102: Case keyInsertCoin3 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
103: Case StartGameKey .Switch(swStartButton) = True
104: Case keySelfTest .Switch(swTest) = True
105: Case keySlamDoorHit .Switch(swSlamTilt) = True
106: Case keyBangBack vpmNudge.DoMechTilt
107: Case keyVPMVolume vpmVol
108: Case Else vpmKeyDown = False
109: End Select
110: End With
111: End Function
113: Function vpmKeyUp(ByVal keycode)
114: vpmKeyUp = True ' assume we handle the key
115: With Controller
116: Select Case keycode
117: Case LeftFlipperKey
118: .Switch(swLLFlip) = False : vpmKeyUp = False : vpmFlips.FlipL False
119: If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
120: vpmFlips.FlipUL False
121: If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
122: End If
123: Case RightFlipperKey
124: .Switch(swLRFlip) = False : vpmKeyUp = False : vpmFlips.FlipR False
125: If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
126: vpmFlips.FlipUR False
127: If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
128: End If
129: Case StagedLeftFlipperKey vpmFlips.FlipUL False : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
130: Case StagedRightFlipperKey vpmFlips.FlipUR False : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
131: Case StartGameKey .Switch(swStartButton) = False
132: Case keySelfTest .Switch(swTest) = False
133: Case keySlamDoorHit .Switch(swSlamTilt) = False
134: Case keyShowOpts .Pause = True : vpmShowOptions : .Pause = False
135: Case keyShowKeys .Pause = True : vpmShowHelp : .Pause = False
```
