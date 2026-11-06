# Bally.vbs v3.61

The generic ball-roll-tilt constant2 does not override Xenon release-stack switch2. Constants and both key handlers:

```vb
Const swTilt           =  7
Const swBallRollTilt   =  2
Const swSlamTilt       = 16
Const swCoin3          =  9
Const swCoin2          = 10
Const swCoin1          = 11
Const swStartButton    =  6

Const swLRFlip         = 82
Const swLLFlip         = 84
Const swURFlip         = 81
Const swULFlip         = 83

' Help Window
vpmSystemHelp = "Bally -17/-35 keys:" & vbNewLine &_
  vpmKeyName(keyInsertCoin1) & vbTab & "Insert Coin #1"   & vbNewLine &_
  vpmKeyName(keyInsertCoin2) & vbTab & "Insert Coin #2"   & vbNewLine &_
  vpmKeyName(keyInsertCoin3) & vbTab & "Insert Coin #3"   & vbNewLine &_
  vpmKeyName(keySelfTest)    & vbTab & "Self Test"        & vbNewLine &_
  vpmKeyName(keyCPUDiag)     & vbTab & "Cpu Diagnostic"   & vbNewLine &_
  vpmKeyName(keySoundDiag)   & vbTab & "Sound Diagnostic" & vbNewLine &_
  vpmKeyName(keySlamDoorHit) & vbTab & "Slam Tilt"

' Dip Switch / Options Menu
Private Sub ballyShowDips
	If Not IsObject(vpmDips) Then ' First time
		Set vpmDips = New cvpmDips
	End With
End Function

Function vpmKeyUp(ByVal keycode)
	vpmKeyUp = True ' Assume we handle the key
	With Controller
		Select Case keycode
			Case LeftFlipperKey
				.Switch(swLLFlip) = False : vpmKeyUp = False : vpmFlips.FlipL False
				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
					vpmFlips.FlipUL False
					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
				End If
			Case RightFlipperKey
				.Switch(swLRFlip) = False : vpmKeyUp = False : vpmFlips.FlipR False
				If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
					vpmFlips.FlipUR False
					If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
				End If
			Case StagedLeftFlipperKey vpmFlips.FlipUL False : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
			Case StagedRightFlipperKey vpmFlips.FlipUR False : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
			Case StartGameKey    .Switch(swStartButton) = False
			Case keySelfTest     .Switch(swSelfTest)    = False
			Case keyCPUDiag      .Switch(swCPUDiag)     = False
			Case keySoundDiag    .Switch(swSoundDiag)   = False
			Case keySlamDoorHit  .Switch(swSlamTilt)    = False
			Case keyShowOpts     .Pause = True : vpmShowOptions : .Pause = False
			Case keyShowKeys     .Pause = True : vpmShowHelp : .Pause = False
			Case keyAddBall      .Pause = True : vpmAddBall  : .Pause = False
			Case keyShowDips     If IsObject(vpmShowDips) Then .Pause = True : vpmShowDips : .Pause = False
			Case keyReset        .Stop : BeginModal : .Run : vpmTimer.Reset : EndModal
			Case keyFrame        .LockDisplay = Not .LockDisplay
			Case keyDoubleSize   .DoubleSize  = Not .DoubleSize
			Case Else            vpmKeyUp = False
		End Select
	End With
End Function
```
