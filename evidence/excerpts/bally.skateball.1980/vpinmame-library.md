# Skateball — retained VPinMAME library contract

Sources retained externally under `bally/skateball-1980/library`: `Bally.vbs` SHA-256 `d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c`, header Last Updated in VBS v3.61; `core.vbs` SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`. Source-code regions manually reviewed. VPinMAME contributors retain their respective rights; no license is asserted for these local files.

`Bally.vbs` cabinet constants: `GameOnSolenoid=19`, `swSelfTest=-7`, `swCPUDiag=-6`, `swSoundDiag=-5`, `swTilt=7`, `swBallRollTilt=2`, `swSlamTilt=16`, `swCoin3=9`, `swCoin2=10`, `swCoin1=11`, `swStartButton=6`, `swLRFlip=82`, `swLLFlip=84`, `swURFlip=81`, `swULFlip=83`.

The generic `swBallRollTilt=2` is not this game's hardware: Skateball assigns 2 to the middle-right drop target and combines its three tilt contacts at 7. The table's nudge setup explicitly uses 7. Coin-number labels are generic keyboard names; the game's physical table names 9 right coin III,10 left coin I,11 middle coin II.

In `vpmKeyDown` and `vpmKeyUp`, right and left flipper keys write 82 and 84 respectively. Staged upper keys can write81/83 when their upper solenoid is not zero. This driver's `FLIP_SW(FLIP_L)` consumes only lower buttons and its ROM never reads generic column 11; writes to the other bits do nothing. Start and service keys write their named constants; coin keys schedule a pulse after 750 ms. These keyboard delays are library behavior, not physical switch timing.

In `core.vbs`, `sLRFlipper=46`, `sLLFlipper=48`, `sURFlipper=34`, `sULFlipper=36`. `vpmFlips` supplies table callbacks using these constants. PinMAME's C core separately defines duplicate synthetic power states45/47; this is emulator-source evidence, not a library constant. A callback at25 is not a BY35 game-on output; PinMAME's actual flipper-enable relay is19.
