# VPinMAME wpc.vbs flipper keys

Quoted from `wpc.vbs` (SHA-256 `1a290886eb2c2fd2c13f82e5f8a1961fdc95238122096642d32fddf1cfbb1a8d`, 169 lines, "Last Updated in VBS v3.56"), the VPinMAME library the table loads through LoadVPM "WPC.VBS". Only the 30 non-comment lines matching the same binding patterns are kept, with their line numbers; they include the flipper switch constants and the vpmKeyDown/vpmKeyUp writes.

```vbscript
   58: Const swLRFlip = 112
   59: Const swLLFlip = 114
   60: Const swURFlip = 116
   61: Const swULFlip = 118
  102:                 .Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
  105:                     If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
  108:                 .Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
  111:                     If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
  113:             Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
  114:             Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
  115:             Case keyInsertCoin1  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  116:             Case keyInsertCoin2  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  117:             Case keyInsertCoin3  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  118:             Case keyInsertCoin4  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin4'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
  119:             Case StartGameKey     swCopy = swStartButtonX : .Switch(swCopy) = True
  120:             Case keyCancel         swCopy = swCancel :       .Switch(swCopy) = True
  121:             Case keyDown         swCopy = swDown :           .Switch(swCopy) = True
  122:             Case keyUp             swCopy = swUp :           .Switch(swCopy) = True
  123:             Case keyEnter         swCopy = swEnter :           .Switch(swCopy) = True
  124:             Case keySlamDoorHit     swCopy = swSlamTiltX :       .Switch(swCopy) = True
  125:             Case keyCoinDoor     swCopy = swCoinDoorX :       If toggleKeyCoinDoor Then .Switch(swCopy) = Not .Switch(swCopy) Else .Switch(swCopy) = Not inverseKeyCoinDoor
  139:                 .Switch(swLLFlip) = False : vpmKeyUp = False : vpmFlips.FlipL False
  142:                     If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
  145:                 .Switch(swLRFlip) = False : vpmKeyUp = False : vpmFlips.FlipR False
  148:                     If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
  150:             Case StagedLeftFlipperKey vpmFlips.FlipUL False : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = False
  151:             Case StagedRightFlipperKey vpmFlips.FlipUR False : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = False
  152:             Case keyCancel         swCopy = swCancel :       .Switch(swCopy) = False
  153:             Case keyDown         swCopy = swDown :           .Switch(swCopy) = False
  154:             Case keyUp             swCopy = swUp :           .Switch(swCopy) = False
  155:             Case keyEnter         swCopy = swEnter :           .Switch(swCopy) = False
  156:             Case keySlamDoorHit     swCopy = swSlamTiltX :       .Switch(swCopy) = False
  157:             Case StartGameKey     swCopy = swStartButtonX : .Switch(swCopy) = False
  158:             Case keyCoinDoor     swCopy = swCoinDoorX :       If toggleKeyCoinDoor = False Then .Switch(swCopy) = inverseKeyCoinDoor
```
