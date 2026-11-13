# Breakshot — pinned PinMAME source

Transcribed from `vpinball/pinmame` at `46e1a01a0f73dc5ce163d98db1ae435883ecc450` (the managed source
checkout `pinmame-46e1a01a`). Every quoted line is copied verbatim; `...` marks omitted lines.

## `src/wpc/capgames.c`

Line 8, the flipper declaration every Capcom game uses:

```c
#define FLIP(x) (FLIP_SWNO(5,6) + FLIP_SOL(x))
```

Lines 29-32 and 37, the per-game inverted-switch masks of the Breakshot drivers (game numbers 5-8) and
Pool Player (13); the comment on line 23 reads `// sw. row number:  0   1     2     3     4     5     6     7     8`:

```c
#define capInvSw5  {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
#define capInvSw6  {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
#define capInvSw7  {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
#define capInvSw8  {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
...
#define capInvSw13 {0, 0x00, 0x00, 0x38, 0x00, 0x30, 0x00, 0x01}
```

Lines 44-47 and 52, the flipper sets:

```c
#define capFlip5  FLIP(FLIP_L | FLIP_UR)
#define capFlip6  FLIP(FLIP_L | FLIP_UR)
#define capFlip7  FLIP(FLIP_L | FLIP_UR)
#define capFlip8  FLIP(FLIP_L | FLIP_UR)
...
#define capFlip13 FLIP(FLIP_L | FLIP_UR)
```

Lines 54-56 and 81-86, the two game macros (the fourth `hw` field is `custSol`, 0 and 1):

```c
#define INITGAME(name, gameno, disp, balls, sb, lamps) \
	CC_INPUT_PORTS_START(name, balls) CC_INPUT_PORTS_END \
	static core_tGameData name##GameData = {GEN_CAPCOM,disp,{capFlip##gameno,0,lamps,0,sb,0,gameno},NULL,{"", capInvSw##gameno}}; \
...
#define INITGAMEFF(name, gameno, disp, balls, sb, lamps, fastflipaddr) \
   CC_INPUT_PORTS_START(name, balls) CC_INPUT_PORTS_END \
   static int name##_getsol(int solNo) { \
      return (memory_region(REGION_CPU1)[fastflipaddr] > 0); \
   } \
   static core_tGameData name##GameData = {GEN_CAPCOM,disp,{capFlip##gameno,0,lamps,1,sb,0,gameno,0, name##_getsol},NULL,{"", capInvSw##gameno}}; \
```

Lines 205-258, the Breakshot drivers (ROM lines omitted):

```c
/ Breakshot (05/96)                    (manual says BREAKSHOT or Breakshot, game says Break Shot, art implies BreakShot)
...
//Version 1.3
INITGAMEFF(bsv103, 5, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1, 0xa7da)
...
CORE_GAMEDEFNV(bsv103,"Breakshot (1.3)",1996,"Capcom",cc1,0)

//Version 1.2
INITGAME(bsv102, 5, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
...
CORE_CLONEDEFNV(bsv102, bsv103,"Breakshot (1.2)",1996,"Capcom",cc1,0)

//Redemption Version 1.0I
INITGAME(bsv100r, 6, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
...
CORE_CLONEDEFNV(bsv100r,bsv103,"Breakshot (Redemption 1.0)",1996,"Capcom",cc1,0)
//Redemption Version 1.2I
INITGAME(bsv102r, 7, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
...
CORE_CLONEDEFNV(bsv102r,bsv103,"Breakshot (Redemption 1.2)",1996,"Capcom",cc1,0)
//Beta Version 1.5
INITGAME(bsb105, 8, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
...
CORE_CLONEDEFNV(bsb105,bsv103,"Breakshot (Beta 1.5)",1996,"Capcom",cc1,0)
```

The two redemption drivers load a fourth sound ROM, `u30_v10i.bin`, through `CAPCOMS_SOUNDROM2a`; the
others load `u24_v11.bin`, `u28_v11.bin` and `u29_v11.bin` (`bsb105`: `u24_v11.bin` and `bsu28_b1.2`).

Lines 372-382, Pool Player (ROM lines omitted):

```c
/ Pool Player (Illinois Pinball, 2000)
/-------------------------------------------------------------------*/
INITGAME(pp100, 13, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 1)
...
CORE_CLONEDEFNV(pp100,bsv103,"Pool Player (1.0)",2000,"Illinois Pinball",cc1,0)
```

`pp100` is not a Breakshot driver variant here: it is curated as its own physical machine,
`illinois-pinball.pool-player.2000`, which carries its own transcription of these lines.

## `src/wpc/capcom.c`

Lines 106-107:

```c
// Breakshot has a modified hardware with a single lamp matrix (B), the hardware of the other lamp matrix being used as a switch matrix, allowing to spare the switch board
#define HAS_SWITCH_BOARD (core_gameData->hw.lampCol > 1)
```

Lines 109-117:

```c
// Mirror of the flipper coils to PinMAME's flipper outputs (see io_w): 0 (default) mirrors them to the matching side, as
// tables expect (SolCallback(sLRFlipper) is the right flipper); 1 restores the mapping of the 3.7 development builds,
// solenoids 9/10/11/12 to the lower right/lower left/upper right/upper left outputs (PinMAME 3.6 reported none of them).
// In all Capcom games 9 is the left flipper and 10 the right (the solenoid tests' names); 11 is the upper right flipper
// in Breakshot, Pool Player and Big Bang Bar, while in Flipper Football 11 is the upper left and 12 the upper right (its
// flipper descriptors in ROM), see MACHINE_INIT(cc). 11/12 are only mirrored where capgames.c declares the upper flipper
#ifndef CAPCOM_LEGACY_FLIPPER_SWAP
#define CAPCOM_LEGACY_FLIPPER_SWAP 0
#endif
```

Lines 119-123:

```c
// Flipper strength, the duty of the power stroke, reported as the flipper outputs' value while on. Newer firmware (Kingpin,
// Flipper Football) keeps the strength adjustment as a RAM byte, n of 32 slots; older firmware (Pinball Magic, Airborne,
// Breakshot, Big Bang Bar, Pool Player) writes the adjustment (2..16) as a 16 slot pattern into the coil's RAM descriptor, n bits set
#define CC_FLIP_BYTE32    1
#define CC_FLIP_PATTERN16 2
```

Lines 235-237 and 273-277, the CPU port lines that reach connector J3 (the port A read masks `parallelA`
with `0xCF` and returns these bits as last written; nothing in the file maps them to a switch, solenoid or
lamp):

```c
//PA0   - J3 - Pin 7 - Token/Coin Meter/Printer Interface Board(Unknown purpose)
//PA1   - J3 - Pin 8 - Token/Coin Meter/Printer Interface Board(Unknown purpose)
//PA2   - J3 - Pin 9 - Token/Coin Meter/Printer Interface Board(Unknown purpose)
...
//PB2 OR IACK5 - J3 - Pin 13 - Token/Coin Meter/Printer Interface Board - SW3(Unknown Purpose)(Output Only)
//PB3 OR IACK6 - J3 - Pin 12 - Token/Coin Meter/Printer Interface Board - SW4(Unknown Purpose)(Output Only)
//PB4 OR IRQ2  - ZERO CROSS IRQ (Input)
//PB5 OR IRQ3  - NOT USED?
//PB6 OR IRQ5  - J3 - Pin 11 - Token/Coin Meter/Printer Interface Board - SW6(Unknown Purpose)(Output Only)
```

Lines 211-219, the keyboard switch update:

```c
static SWITCH_UPDATE(cc) {
  if (inports) {
    CORE_SETKEYSW(inports[CORE_COREINPORT],0xcf,9);
    if (HAS_SWITCH_BOARD)
      CORE_SETKEYSW(inports[CORE_COREINPORT]>>8,0xff,0);
    else
      CORE_SETKEYSW(((inports[CORE_COREINPORT]>>8)<<4),0xf0,2);
  }
}
```

Lines 608-628, the switch read:

```c
    ////////////////////////////// SWITCH0 => Read cabinet switches (no address decoding) / strobed switches
    //Cabinet/Coin Door Switches OR 8 cabinet switches and 8 strobed switches for Breakshot (which does not have the switch board)
    case 0x400000:
      if (HAS_SWITCH_BOARD) {
        data = coreGlobals.swMatrix[0] << 8 | coreGlobals.swMatrix[9];
      } else {
        // Cabinet/Coin Door Switches are read as the lower byte on all switch reads
        data = coreGlobals.swMatrix[9];
        switch(locals.swCol) {
          case 0x80: data |= coreGlobals.swMatrix[1]<<8; break;
          case 0x40: data |= coreGlobals.swMatrix[2]<<8; break;
          case 0x20: data |= coreGlobals.swMatrix[3]<<8; break;
          case 0x10: data |= coreGlobals.swMatrix[4]<<8; break;
          case 0x08: data |= coreGlobals.swMatrix[5]<<8; break;
          case 0x04: data |= coreGlobals.swMatrix[6]<<8; break;
          case 0x02: data |= coreGlobals.swMatrix[7]<<8; break;
          case 0x01: data |= coreGlobals.swMatrix[8]<<8; break;
        }
      }
      data ^= 0xffff; //Switches are inverted
      break;
```

Lines 723-737, the solenoid write that carries 9-16 and 25-32 and the flipper mirror:

```c
    //Sols: 9-16 (hi byte) & 24-32 (lo byte)
    case 0x20000d:
      soldata = core_revword(data^0xffff);
      coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00FF00FFu) | ((UINT32)(soldata & 0x00ff)<<24) | (soldata & 0xff00);
      core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 24,  soldata       & 0xFF);
      core_write_pwm_output_8b(CORE_MODOUT_SOL0 +  8, (soldata >> 8) & 0xFF);
      // Mirror the flipper coils (solenoids 9..12) to PinMAME's flipper outputs, which tables (sLRFlipper etc.) and DOF use;
      // the coils stay on 9..12 too. Each goes to the power output locals.flipMirror (0: none, see CAPCOM_LEGACY_FLIPPER_SWAP)
      // and the hold output after it, as binary mode reports the hold coil on with either coil
      for (int i = 0; i < 4; i++)
        if (locals.flipMirror[i]) {
          core_write_pwm_output(CORE_MODOUT_SOL0 + locals.flipMirror[i] - 1, 1, (soldata >> (8 + i)) & 0x01);
          core_write_pwm_output(CORE_MODOUT_SOL0 + locals.flipMirror[i]    , 1, (soldata >> (8 + i)) & 0x01);
        }
      break;
```

Lines 796-809, output allocation in `MACHINE_INIT(cc)`:

```c
  // Initialize outputs
  coreGlobals.nLamps = 64 + core_gameData->hw.lampCol * 8; // Lamp Matrix A & B, +1 col for PWM diag LED
  core_set_pwm_output_type(CORE_MODOUT_LAMP0, coreGlobals.nLamps - 8, CORE_MODOUT_BULB_44_20V_DC_CC);
  core_set_pwm_output_type(CORE_MODOUT_LAMP0 + coreGlobals.nLamps - 8, 8, CORE_MODOUT_NONE); // Unused
  core_set_pwm_output_type(CORE_MODOUT_LAMP0 + coreGlobals.nLamps - 8, 1, CORE_MODOUT_LED); // CPU Board Diagnostic LED
  core_set_pwm_output_type(CORE_MODOUT_LAMP0 + coreGlobals.nLamps - 7, 1, CORE_MODOUT_LED); // Sound Board Diagnostic LED
  coreGlobals.nSolenoids = CORE_FIRSTCUSTSOL - 1 + core_gameData->hw.custSol;
  coreGlobals.hasModulatedFlippers = TRUE;
  core_set_pwm_output_type(CORE_MODOUT_SOL0, coreGlobals.nSolenoids, CORE_MODOUT_SOL_2_STATE);
  core_set_pwm_output_type(CORE_MODOUT_SOL0 + CORE_FIRSTCUSTSOL - 1, 1, CORE_MODOUT_SOL_CUSTOM); // GameOn solenoid for Fast Flips
  // Flipper outputs mirrored from solenoids 9..12 (see io_w): not fast on, which would write slot & 31 of solenoids2, the
  // lower flipper bits for 33..36; cc_vblank sets the flipper bits
  core_set_pwm_output_type(CORE_MODOUT_SOL0 + sURFlipPow - 1, 4, CORE_MODOUT_LEGACY_SOL_2_STATE);
  core_set_pwm_output_type(CORE_MODOUT_SOL0 + sLRFlipPow - 1, 4, CORE_MODOUT_LEGACY_SOL_2_STATE);
```

Lines 816-820:

```c
  // Flipper mirror: 9 left, 10 right, 11 upper right (Breakshot, Pool Player, Big Bang Bar), legacy swaps the lower ones
  locals.flipMirror[0] = CAPCOM_LEGACY_FLIPPER_SWAP ? sLRFlipPow : sLLFlipPow;
  locals.flipMirror[1] = CAPCOM_LEGACY_FLIPPER_SWAP ? sLLFlipPow : sLRFlipPow;
  locals.flipMirror[2] = sURFlipPow;
  locals.flipMirror[3] = sULFlipPow;
```

Lines 833-842, the Breakshot branch (also taken by Pool Player, whose root driver is `bsv103`):

```c
  else if (strncasecmp(gn, "bsv", 3) == 0) { // Breakshot (and its clone Pool Player)
    core_set_pwm_output_type(CORE_MODOUT_SOL0 + 28 - 1, 1, CORE_MODOUT_BULB_89_20V_DC_WPC); // Center pocket Flasher
    // core_set_pwm_output_type(CORE_MODOUT_SOL0 + 27 - 1, 5, CORE_MODOUT_BULB_89_20V_DC_WPC); // Plunger Flasher (appears in doc but was not kept in production)
    // "FLIPPER STRENGTH" and "U.R. FLIPPER STRENGTH" (2..16, factory 13) as the power pattern of the left/right and upper
    // right flipper descriptors; the beta 1.05 has them elsewhere, and one setting for all three
    if (strcmp(set, "bsb105") == 0)
      cc_set_flip_strength(CC_FLIP_PATTERN16, 0x3996, 0x39ae, 0x39c6, 0);
    else
      cc_set_flip_strength(CC_FLIP_PATTERN16, 0x39a2, 0x39ba, 0x39d2, 0);
  }
```

Lines 876-879:

```c
  // No mirror to an upper flipper the game doesn't declare (capgames.c): 11/12 drive other devices there
  for (int i = 2; i < 4; i++)
    if (!(core_gameData->hw.flippers & FLIP_SOL(locals.flipMirror[i] == sURFlipPow ? FLIP_UR : FLIP_UL)))
      locals.flipMirror[i] = 0;
```

Lines 1005-1011, matrix-to-public switch numbering:

```c
static int cc_m2sw(int col, int row) {
  // col 0..8 => 0 is cabinet switch, 1..8 is playfield matrix => 9..80
  if (col < 9)
     return 9 + row + col * 8;
  // col 9 => base cabinet switch (all games) => 1..8
  if (col == 9)
     return 1 + row;
```

## `src/wpc/capcom.h`

Lines 11-21 of the keyboard port `CC_COMPORTS`:

```c
    COREPORT_BIT(     0x0040, "Start Game",KEYCODE_1) \
    COREPORT_BIT(     0x0001, "Coin #1",   KEYCODE_3) \
    COREPORT_BIT(     0x0002, "Coin #2",   KEYCODE_4) \
    COREPORT_BIT(     0x0004, "Coin #3",   KEYCODE_5) \
    COREPORT_BIT(     0x0008, "Coin #4",   KEYCODE_6) \
    COREPORT_BITTOG(  0x0080, "Coin Door", KEYCODE_7) \
...
    COREPORT_BIT(     0x0400, "Buy In",    KEYCODE_2) \
    COREPORT_BIT(     0x0200, "Tilt",      KEYCODE_INSERT) \
    COREPORT_BIT(     0x0100, "Slam Tilt", KEYCODE_HOME) \
    COREPORT_BIT(     0x0800, "Unused #1", KEYCODE_8) \
```

## `src/wpc/core.h` and `src/wpc/core.c`

`core.h` lines 299-301 and 311-318:

```c
#define CORE_FIRSTUFLIPSOL 33
#define CORE_FIRSTCUSTSOL  51
#define CORE_FIRSTLFLIPSOL 45
...
#define sLRFlip     (CORE_FIRSTLFLIPSOL+1)
#define sLRFlipPow  (CORE_FIRSTLFLIPSOL+0)
#define sLLFlip     (CORE_FIRSTLFLIPSOL+3)
#define sLLFlipPow  (CORE_FIRSTLFLIPSOL+2)
#define sURFlip     (CORE_FIRSTUFLIPSOL+1)
#define sURFlipPow  (CORE_FIRSTUFLIPSOL+0)
#define sULFlip     (CORE_FIRSTUFLIPSOL+3)
#define sULFlipPow  (CORE_FIRSTUFLIPSOL+2)
```

`core.c` lines 1832-1834, where the flipper column's button bits reach matrix switches 5 and 6:

```c
    /*-- set switches in matrix for non-fliptronic games --*/
    if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
    if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
```

## What the definition derives from these lines

- Switches. Breakshot has no switch board (`hw.lampCol` is 1). Public 1-8 are internal column 9, read
  as the low byte on every switch read; the strobed columns `swMatrix[1]`-`[8]` are public 17-80
  (`cc_m2sw`). Internal column 0, public 9-16, is never read, so those addresses are dead. The keyboard
  writes coins 1-4 to public 1-4, Start to 7 and the coin door to 8 (mask `0xcf`, so 5 and 6 are left to
  `core.c`'s flipper copy), and Slam Tilt, Tilt, Buy In and Unused #1 to internal column 2 bits 4-7,
  public 29-32. The read inverts every bit, so outside the `capInvSw` mask a public 1 is a closed
  contact. The mask's bits are column 3 `0x38` (public 36-38), column 5 `0x30` (53, 54) and column 7
  `0x01` (65): for those a public 1 is a blocked opto beam.
- Solenoids. `nSolenoids` is 50 plus `custSol`: 51 for `bsv103` (INITGAMEFF) and 50 for the others.
  Physical 9, 10 and 11 are mirrored to the power and hold addresses 47/48, 45/46 and 33/34; the
  upper-left mirror (35/36) is cleared because the Breakshot drivers declare only `FLIP_UR`. Addresses
  37-44 and 49-50 are never written. Public 28 is typed as a #89 bulb; public 27's plunger flasher
  typing is commented out.
- Lamps. `nLamps` is 64 + 1 × 8 = 72: one lamp matrix at 1-64, the CPU and sound board LEDs at 65 and 66,
  and 67-72 typed `CORE_MODOUT_NONE`.
- Dispenser interface. The J3 lines that run to the token/coin meter/printer interface board are kept as
  port bits only, so PinMAME publishes no ticket or token dispenser motor, solenoid, meter or notch switch.
