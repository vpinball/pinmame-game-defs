# Phantom of the Opera flipper input path

The retained table loads de.vbs at script line 68. Retained de.vbs SHA-256 8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04, core.vbs SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69; both are VPinMAME contributors' libraries, retained from the working installation. Direct code read, project curator, reviewed.

de.vbs lines 33-36 declares swLRFlip=82, swLLFlip=84, swURFlip=86, swULFlip=88. vpmKeyDown/vpmKeyUp set/clear 82 and 84 for the lower right/left keys. The table's KeyDownHandler/KeyUpHandler invoke that library path (core.vbs lines 2854-2855 dispatch); its direct writes 15/16 are overwritten by PinMAME's FLIP1516 copy. Drive 82/84.

core.vbs defines sLRFlipper=46 and sLLFlipper=48. These are the table's callbacks for the synthetic hold bits; core_updateSw synthesizes 45/46 and 47/48 as pairs while game-on 23 is enabled. The physical machine has two 23-900 flipper coils on its solid-state flipper board, not four driver-board outputs.

The table calls vpmInit and does not declare cSingleLFlip/cSingleRFlip or call NoUpperLeftFlipper/NoUpperRightFlipper. de.vbs can therefore write 86/88 on staged keys, but no upper flipper is fitted and the eight-bit Data East matrix-strobe read cannot reach that column. The unused flipper-column records explain the distinction.
