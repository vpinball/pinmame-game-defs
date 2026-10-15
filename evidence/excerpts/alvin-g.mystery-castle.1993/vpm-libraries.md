# Retained VPinMAME libraries

alvinG.vbs SHA-256 63a758ecb79e879924831f2140476a31531c5c9f90b116253356b2e856ba143d; core.vbs SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69. Cabinet routing,light mapping and assembly callbacks.

## alvinG.vbs:20-41

```vb
' Flipper Solenoid
Const GameOnSolenoid = 27 'not 100% on this!
' Cabinet Switches
Const swCoin1       =  1
Const swCoin2       =  2
Const swCoin3       =  3
Const swCoin4       =  4
Const swSlamTilt    =  5
Const swDiagnostic  = -7
Const swExitDiag    = -6
Const swVolUp       = 15
Const swVolDn       = 16
Const swStartButton =  9

Const swLRFlip      = 114
Const swLLFlip      = 116
Const swURFlip      = 115
Const swULFlip      = 117

' Help Window
vpmSystemHelp = "Alvin G keys" & vbNewLine &_
  vpmKeyName(keyInsertCoin1)  & vbTab & "Insert Coin #1" & vbNewLine &_
```

## alvinG.vbs:84-113

```vb
			Case keyInsertCoin1  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
			Case keyInsertCoin2  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
			Case keyInsertCoin3  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
			Case keyInsertCoin4  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin4'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
			Case StartGameKey    .Switch(swStartButton) = True
			Case keyCancel       .Switch(swDiagnostic)  = True
			Case keyDown         .Switch(swExitDiag)    = True
			Case keyUp           .Switch(swVolUp)       = True
			Case keyEnter        .Switch(swVolDn)       = True
			Case keySlamDoorHit  .Switch(swSlamTilt)    = True
			Case keyBangBack     vpmNudge.DoMechTilt
			Case keyVPMVolume    vpmVol
			Case Else            vpmKeyDown = False
		End Select
	End With
End Function

Function vpmKeyUp(ByVal keycode)
	vpmKeyUp = True ' assume we handle the key
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
```


## core.vbs:967-975

```vb
			mBalls = mBalls + 1 : mBallPos(mBalls) = conStackSw + 1 : NeedUpdate = True
		End If
		CorePlaySoundAt mAddSnd, mSoundKicker
	End Sub

	' A bug in the script engine forces the "End If" at the end
	Public Sub SolIn(aEnabled)	   : If aEnabled Then KickIn		: End If : End Sub
	Public Sub SolOut(aEnabled)	   : If aEnabled Then KickOut False : End If : End Sub
	Public Sub SolOutAlt(aEnabled) : If aEnabled Then KickOut True	: End If : End Sub
```

## core.vbs:1038-1047

```vb
	Public Sub InitSw(aEntry, aSw1, aSw2, aSw3, aSw4, aSw5, aSw6, aSw7)
		mEntrySw = aEntry : mSw(1) = aSw1 : mSw(2) = aSw2 : mSw(3) = aSw3 : mSw(4) = aSw4
		mSw(5) = aSw5 : mSw(6) = aSw6 : mSw(7) = aSw7 : mSw(8) = 0
		If Not IsObject(vpmTrough) Then Set vpmTrough = Me
	End Sub

	Public Sub InitSw8(aEntry, aSw1, aSw2, aSw3, aSw4, aSw5, aSw6, aSw7, aSw8)
		mEntrySw = aEntry : mSw(1) = aSw1 : mSw(2) = aSw2 : mSw(3) = aSw3 : mSw(4) = aSw4
		mSw(5) = aSw5 : mSw(6) = aSw6 : mSw(7) = aSw7 : mSw(8) = aSw8
		If Not IsObject(vpmTrough) Then Set vpmTrough = Me
```

## core.vbs:2607-2622

```vb
Sub vpmMapLights(aLights)
	Dim obj, str, ii, idx
	For Each obj In aLights
		idx = obj.TimerInterval
		If IsArray(Lights(idx)) Then
			str = "Lights(" & idx & ") = Array("
			For Each ii In Lights(idx) : str = str & ii.Name & "," : Next
			ExecuteGlobal str & obj.Name & ")"
		ElseIf IsObject(Lights(idx)) Then
			Lights(idx) = Array(Lights(idx),obj)
		Else
			Set Lights(idx) = obj
		End If
	Next
End Sub

```

## core.vbs:2860-2866

```vb

'-- Flipper solenoids (all games)
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36

```
