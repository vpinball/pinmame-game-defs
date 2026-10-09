# VPinMAME sega.vbs — Whitestar constants and key handlers

Quoted verbatim from `sega.vbs` ("Last Updated in VBS v3.61", SHA-256
`d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924`), the library the retained table loads with
`LoadVPM "01560000", "sega.VBS", 3.10`. It was copied byte for byte from the contributor's Visual Pinball `Scripts`
folder, beside the `core.vbs` it executes (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`).
Line numbers are the file's own.

## Constants (lines 20-39)

```text
  20: ' Sega / Stern Whitestar Data
  21: '----------------------------
  22: ' Flipper Solenoid
  23: Const GameOnSolenoid = 15
  24: ' Cabinet switches
  25: Const swBlack         =  0 'DED 8
  26: Const swGreen         = -1 'DED 7
  27: Const swRed           = -2 'DED 6
  28: Const swMemoryProtect = -3 'Coin door memory protect switch
  29: Const swStartButton   = 54
  30: Const swTilt          = 56
  31: Const swSlamTilt      = 55
  32: Const swCoin3         =  4
  33: Const swCoin1         =  5
  34: Const swCoin2         =  6
  35:
  36: Const swLRFlip        = 82
  37: Const swLLFlip        = 84
  38: Const swURFlip        = 81
  39: Const swULFlip        = 83
```

`swSlamTilt = 55` is generic Whitestar: on The Sopranos the grid prints 55 as TOURNAMENT START and the optional
slam tilt at 53. `swURFlip = 81` and `swULFlip = 83` name the right and left end-of-stroke inputs; the key handlers
write them only when an upper flipper solenoid is registered.

## Country DIP form (lines 52-69)

```text
  52: ' Dip Switch / Options Menu
  53: Private Sub segaShowDips
  54: 	If Not IsObject(vpmDips) Then ' First time
  55: 		Set vpmDips = New cvpmDips
  56: 		With vpmDips
  57: 			.AddForm 100, 240, "DIP Switches"
  58: 			.AddFrame 0, 0, 80, "Country", &H0f,_
  59: 			  Array("Austria",&H01, "Belgium", &H02, "Brazil",      &H0d,_
  60: 			        "Canada", &H03, "France",  &H06, "Germany",     &H07,_
  61: 			        "Italy",  &H08, "Japan",   &H09, "Netherlands", &H04,_
  62: 			        "Norway", &H0a, "Sweden",  &H0b, "Switzerland", &H0c,_
  63: 			        "UK",     &H05, "UK (New)",&H0e, "USA",         &H00)
  64: 		End With
  65: 	End If
  66: 	vpmDips.ViewDips
  67: End Sub
  68: Set vpmShowDips = GetRef("segaShowDips")
  69: Private vpmDips
```

## Key handlers (lines 71-139)

```text
  71: ' Keyboard handlers
  72: Function vpmKeyDown(ByVal keycode)
  73: 	vpmKeyDown = True ' Assume we handle the key
  74: 	With Controller
  75: 		Select Case keycode
  76: 			Case LeftFlipperKey
  77: 				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
  78: 				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
  79: 					vpmFlips.FlipUL True
  80: 					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
  81: 				End If
  82: 			Case RightFlipperKey
  83: 				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
  84: 				If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
  85: 					vpmFlips.FlipUR True
  86: 					If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
  87: 				End If
  88: 			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
  89: 			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
  90:
  91: 			Case keyInsertCoin1  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  92: 			Case keyInsertCoin2  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  93: 			Case keyInsertCoin3  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  94: 			Case StartGameKey    .Switch(swStartButton) = True
  95: 			Case keyBlack        .Switch(swBlack)       = True
  96: 			Case keyGreen        .Switch(swGreen)       = True
  97: 			Case keyRed          .Switch(swRed)         = True
  98: 			Case keySlamDoorHit  .Switch(swSlamTilt)    = True
  99: 			Case keyCoinDoor     If toggleKeyCoinDoor Then .Switch(swMemoryProtect) = Not .Switch(swMemoryProtect) Else .Switch(swMemoryProtect) = Not inverseKeyCoinDoor
 100: 			Case keyBangBack     vpmNudge.DoMechTilt
 101: 			Case keyVPMVolume    vpmVol
 102: 			Case Else            vpmKeyDown = False
 103: 		End Select
 104: 	End With
 105: End Function
 106:
 107: Function vpmKeyUp(ByVal keycode)
 108: 	vpmKeyUp = True ' Assume we handle the key
 109: 	With Controller
 110: 		Select Case keycode
 111: 			Case LeftFlipperKey
 112: 				.Switch(swLLFlip) = False : vpmKeyUp = False : vpmFlips.FlipL False
 113: 				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
 114: 					vpmFlips.FlipUL False
 115: 					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
 116: 				End If
 117: 			Case RightFlipperKey
 118: 				.Switch(swLRFlip) = False : vpmKeyUp = False : vpmFlips.FlipR False
 119: 				If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
 120: 					vpmFlips.FlipUR False
 121: 					If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
 122: 				End If
 123: 			Case StagedLeftFlipperKey vpmFlips.FlipUL False : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
 124: 			Case StagedRightFlipperKey vpmFlips.FlipUR False : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
 125:
 126: 			Case StartGameKey    .Switch(swStartButton) = False
 127: 			Case keyBlack        .Switch(swBlack)       = False
 128: 			Case keyGreen        .Switch(swGreen)       = False
 129: 			Case keyRed          .Switch(swRed)         = False
 130: 			Case keySlamDoorHit  .Switch(swSlamTilt)    = False
 131: 			Case keyCoinDoor     If toggleKeyCoinDoor = False Then .Switch(swMemoryProtect) = inverseKeyCoinDoor
 132: 			Case keyShowOpts     .Pause = True : vpmShowOptions : .Pause = False
 133: 			Case keyShowKeys     .Pause = True : vpmShowHelp : .Pause = False
 134: 			Case keyShowDips     If IsObject(vpmShowDips) Then .Pause = True : vpmShowDips : .Pause = False
 135: 			Case keyAddBall      .Pause = True : vpmAddBall  : .Pause = False
 136: 			Case keyReset        .Stop : BeginModal : .Run : vpmTimer.Reset : EndModal
 137: 			Case keyFrame        .LockDisplay = Not .LockDisplay
 138: 			Case keyDoubleSize   .DoubleSize  = Not .DoubleSize
 139: 			Case Else            vpmKeyUp = False
```
