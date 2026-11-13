# Pool Player — pinned PinMAME source

Transcribed from `vpinball/pinmame` at `46e1a01a0f73dc5ce163d98db1ae435883ecc450` (the managed source
checkout `pinmame-46e1a01a`). Every quoted line is copied verbatim; `...` marks omitted lines.

## `src/wpc/capgames.c`

Line 8, the flipper declaration every Capcom game uses:

```c
#define FLIP(x) (FLIP_SWNO(5,6) + FLIP_SOL(x))
```

Lines 29 and 37, the inverted-switch masks of Breakshot's root driver (game number 5) and of Pool Player (13):

```c
#define capInvSw5  {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
...
#define capInvSw13 {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
```

Lines 44 and 52, their flipper sets:

```c
#define capFlip5  FLIP(FLIP_L | FLIP_UR)
...
#define capFlip13 FLIP(FLIP_L | FLIP_UR)
```

Lines 369-382, the Pool Player driver:

```c
// games by other manufacturers below

/*-------------------------------------------------------------------
/ Pool Player (Illinois Pinball, 2000)
/-------------------------------------------------------------------*/
INITGAME(pp100, 13, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
CC_ROMSTART_2(pp100, "u1l-v1_0.bin", CRC(cb14635e) SHA1(8d7bb25fdc7ee7f38eaf3cad6326cf678a81b85f),
                     "u1h-v1_0.bin", CRC(9839ff76) SHA1(79c3a9700d2e68ed7d83e669b2df543bcabf7164))
//I'm told BS can run with the U24 from FF
CAPCOMS_SOUNDROM2("u24_v11.bin", CRC(d46212f4) SHA1(50f1279d995b597c468805b323e0252800b28274),
				  "u28_v11.bin", CRC(b076ad2e) SHA1(1be8e3bda2890545253f6f7e4825d2db1d925255),
				  "u29_v11.bin", CRC(b251a27c) SHA1(bc30791cb9b5497c11f1cff06c89a729a07b5d4a))
CC_ROMEND
CORE_CLONEDEFNV(pp100,bsv103,"Pool Player (1.0)",2000,"Illinois Pinball",cc1,0)
```

## What this record takes from it

- `pp100` is the only Pool Player driver. PinMAME declares it a clone of Breakshot's `bsv103`, with Breakshot's
  three sound ROMs (`u24_v11.bin`, `u28_v11.bin`, `u29_v11.bin`) and its own game ROM pair.
- Game number 13's switch inversion mask and flipper set equal game number 5's, and plain `INITGAME` publishes no
  game-on solenoid 51. So PinMAME routes `pp100` exactly as it routes Breakshot.
- That shared routing says nothing about the cabinet the firmware ran in. The machine's own sources describe
  differences from Breakshot that this file cannot settle (`identity.md`).
