# VPinMAME script library GTS3.VBS

Source: `gts3.vbs` ("Last Updated in VBS v3.61"), retained byte for byte as
`review-artifacts/vpm-script-libs/gts3.vbs` (SHA-256 `66c329fa86e97d2f10a8036a9a6527be6a67ce59bb3591962aa1c8a9da101314`)
from the contributor's Visual Pinball `Scripts` installation; it executes the retained `core.vbs` (SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Both retained Stargate tables load it
(`LoadVPM ..., "GTS3.VBS", ...`). Line numbers are the file's; leading whitespace is dropped.

| Line | Text |
| --- | --- |
| 21 | `Const GameOnSolenoid = 32` |
| 23-26 | `Const swCoin1 = 00` · `Const swCoin2 = 01` · `Const swCoin3 = 02` · `Const swCoin4 = 03` |
| 27-29 | `Const swDiagnostic = -8` · `Const swTilt = -7` · `Const swSlamTilt = -6` |
| 31-34 | `Const swLRFlip = 141` · `Const swLLFlip = 143` · `Const swURFlip = 145` · `Const swULFlip = 147` |
| 69 | `If swStartButton = 4 Or Err Then swStartButtonX = 4 Else swStartButtonX = swStartButton` |
| 75-76 | `Case LeftFlipperKey` · `.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True` |
| 77-79 | `If keycode = StagedLeftFlipperKey Then` · `vpmFlips.FlipUL True` · `If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True` |
| 81-82 | `Case RightFlipperKey` · `.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True` |
| 83-85 | `If keycode = StagedRightFlipperKey Then` · `vpmFlips.FlipUR True` · `If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True` |
| 89-92 | `Case keyInsertCoin1 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'"` and the same for coins 2-4 |
| 93-95 | `Case StartGameKey .Switch(swStartButtonX) = True` · `Case keySelfTest .Switch(swDiagnostic) = True` · `Case keySlamDoorHit .Switch(swSlamTilt) = True` |
| 107-123 | `vpmKeyUp` writes the same addresses back to False |

Both retained table scripts also write matrix switches 81 and 82 from the flipper keys before calling
`vpmKeyDown`/`vpmKeyUp`; the library's 141/143 are the addresses PinMAME copies into 81/82.
