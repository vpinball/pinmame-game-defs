# VPinMAME script libraries Class1812.vbs and core.vbs

Source: `Class1812.vbs` ("Last Updated in VBS v3.50", "Similar to gts3.vbs except for some switches"), retained byte
for byte as `review-artifacts/vpm-script-libs/Class1812.vbs` (SHA-256
`61fd1d667b910cf003b7eef6f2aec5afefcbfd24dd46637242c7659c055e36e3`) from the contributor's Visual Pinball `Scripts`
installation, and the `core.vbs` it executes, retained as `review-artifacts/vpm-script-libs/core.vbs` (SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). The known-working script loads the first
(`LoadVPM "02800000", "Class1812.VBS", 3.50`, its line 68). Line numbers are each file's; leading whitespace is
dropped, runs of spaces are collapsed.

## Class1812.vbs

| Line | Text |
| --- | --- |
| 22 | `Const GameOnSolenoid = 32` |
| 24-26 | `Const swCoin1 = 00` · `Const swCoin2 = 01` · `Const swCoin3 = 02` |
| 28-32 | `Const swStartButton = 03` · `Const swLeftAdvance = 04` · `Const swRightAdvance = 05` · `Const swLRFlip = 141 '06` · `Const swLLFlip = 143 '07` |
| 34-36 | `Const swDiagnostic = -8` · `Const swTilt = -7` · `Const swSlamTilt = -6` |
| 39-47 | `vpmSystemHelp = "Class Of 1812 keys:" & vbNewLine &_` · `vpmKeyName(StartGameKey) & vbTab & "Start Game" & vbNewLine &_` · `vpmKeyName(keyInsertCoin1) & vbTab & "Left Coin Chute" & vbNewLine &_` · `vpmKeyName(keyInsertCoin2) & vbTab & "Right Coin Chute" & vbNewLine &_` · `vpmKeyName(keyInsertCoin3) & vbTab & "Center Coin Chute" & vbNewLine &_` · `vpmKeyName(keySelfTest) & vbTab & "Diagnostic" & vbNewLine &_` · `vpmKeyName(keyDown) & vbTab & "Left Advance Button" & vbNewLine &_` · `vpmKeyName(keyUp) & vbTab & "Right Advance Button" & vbNewLine &_` · `vpmKeyName(keySlamDoorHit) & vbTab & "Slam Tilt"` |
| 68-69 | `Case LeftFlipperKey .Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True : if keycode = StagedLeftFlipperKey then vpmFlips.FlipUL True` · `Case RightFlipperKey .Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True : if keycode = StagedRightFlipperKey then vpmFlips.FlipUR True` |
| 72-79 | `Case keyInsertCoin1 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin` · `Case keyInsertCoin2 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin` · `Case keyInsertCoin3 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin` · `Case StartGameKey .Switch(swStartButton) = True` · `Case keySelfTest .Switch(swDiagnostic) = True` · `Case keySlamDoorHit .Switch(swSlamTilt) = True` · `Case keyDown .Switch(swLeftAdvance) = True` · `Case keyUp .Switch(swRightAdvance) = True` |
| 91-99 | `Case LeftFlipperKey .Switch(swLLFlip) = False : vpmKeyUp = False : vpmFlips.FlipL False : if keycode = StagedLeftFlipperKey then vpmFlips.FlipUL False` · `Case RightFlipperKey .Switch(swLRFlip) = False : vpmKeyUp = False : vpmFlips.FlipR False : if keycode = StagedRightFlipperKey then vpmFlips.FlipUR False` · `Case StagedLeftFlipperKey vpmFlips.FlipUL False` · `Case StagedRightFlipperKey vpmFlips.FlipUR False` · `Case keyDown .Switch(swLeftAdvance) = False` · `Case keyUp .Switch(swRightAdvance) = False` · `Case StartGameKey .Switch(swStartButton) = False` · `Case keySelfTest .Switch(swDiagnostic) = False` · `Case keySlamDoorHit .Switch(swSlamTilt) = False` |

## core.vbs

| Line | Text |
| --- | --- |
| 1120 | `Public TiltSwitch` |
| 1130 | `If TiltSwitch <> 0 Then vpmTimer.PulseSw TiltSwitch` |
| 2862-2863 | `Const sLRFlipper = 46` · `Const sLLFlipper = 48` |
