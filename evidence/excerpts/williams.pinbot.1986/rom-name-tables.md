# Pin-Bot — ROM lamp, switch and coil name tables

Decoded by `tools/pinbot_rom_name_tables.py` from the user-authorized local ROM archives; no ROM bytes are
reproduced. Each table is a run of fixed 14-byte entries in the 32 KiB **U27** program ROM: seven characters for the
player 1 display followed by seven for the player 2 display, which is how the Single Lamps, Switch Levels and Coil
tests print them. A byte with bit 7 set is the character in its low seven bits followed by the display's period
segment. Entries are shown with the two halves joined by one space and padding trimmed. The lamp table ends where the
switch table begins, and the coil table follows the switch table directly.

| Driver | ROM member | Member SHA-256 | Lamp table | Switch table | Coil table |
| --- | --- | --- | --- | --- | --- |
| pb_l5 | pbot_u27.l5 | `272fec6c0628ebc12c8406ee45add12a1cdb99a2457f50fb5286edea439ac412` | 0x11cd | 0x154d | 0x18cd |
| pb_l5h | pbot_u27.l5 | `39083a9e5488d32ccb1bbe61b5645cd021a8b5bc3b3ce19c4ed3e4433699649b` | 0x11cd | 0x154d | 0x18cd |
| pb_l3 | u27-l3.rom | `4071566a5aab58f515a87bb49c546c366f9acf863ea017424b83b2fea904b329` | 0x11cd | 0x154d | 0x18cd |
| pb_l2 | u27-l2.rom | `6fe1eb7d9ed15e8d83428c771957a20f5e6909ea77cd3a89df9c311ea85ecd7d` | 0x11cd | 0x154d | 0x18cd |
| pb_l1 | u27-l1.rom | `69194b69c36e50d2e17af5e3ab1763456e6f3c546945fc44c81042fb9fa9d0dc` | 0x11cd | 0x154d | 0x18cd |
| pb_p4 | u27-p4.bin | `23ea5f593b3a9b661ca214efa5c23c5feb1e51abc92eb87c4a310b78e1f20524` | 0x11cd | 0x154d | 0x18cd |
| pb_j5 | PEMBOT_J5_U27.bin | `d8b10a1884a49296ad67ef4492170ef515d8999514b9d7cde6080cbb7dacad66` | 0x11a2 | 0x1522 | 0x18a2 |

Not read: `pb_j1`, `pb_j2` and `pb_j3`, whose archives are not in the local ROM corpus.

Every entry of all three tables is identical in all seven sets read. The tables below are the `pb_l5` text.

## Lamp table (public lamp address = entry number)

| Lamp | ROM text |
| --- | --- |
| 1 | GAME OVER |
| 2 | MATCH LAMP |
| 3 | BALL IN PLAY |
| 4 | MOUTH 1  LEFT |
| 5 | MOUTH 2 |
| 6 | MOUTH 3 |
| 7 | MOUTH 4 |
| 8 | MOUTH 5 RIGHT |
| 9 | BONUS 2X |
| 10 | BONUS 3X |
| 11 | BONUS 4X |
| 12 | BONUS 5X |
| 13 | S. EJECT 25K |
| 14 | S. EJECT 50K |
| 15 | S. EJECT 75K |
| 16 | S. EJECT EX. BALL |
| 17 | LEFT D.T. TIMER |
| 18 | ADVANCE PLANET |
| 19 | BONUS PLUTO |
| 20 | BONUS NEPTUNE |
| 21 | BONUS URANUS |
| 22 | BONUS SATURN |
| 23 | BONUS JUPITER |
| 24 | BONUS MARS |
| 25 | BONUS EARTH |
| 26 | BONUS VENUS |
| 27 | BONUS MERCURY |
| 28 | YELLOW TOP |
| 29 | YELLOW 2ND TOP |
| 30 | YELLOW MIDDLE |
| 31 | YELLOW 2ND BOT |
| 32 | YELLOW BOTTOM |
| 33 | SHOOT AGAIN |
| 34 | SCORE ENERGY |
| 35 | SCORE SOLAR |
| 36 | BLUE TOP |
| 37 | BLUE 2ND TOP |
| 38 | BLUE MIDDLE |
| 39 | BLUE 2ND BOT |
| 40 | BLUE BOTTOM |
| 41 | LEFT D.T. TOP |
| 42 | LEFT D.T. MIDDLE |
| 43 | LEFT D.T. BOTTOM |
| 44 | AMBER TOP |
| 45 | AMBER 2ND TOP |
| 46 | AMBER MIDDLE |
| 47 | AMBER 2ND BOT |
| 48 | AMBER BOTTOM |
| 49 | LEFT OUTLANE |
| 50 | LEFT RETURN |
| 51 | SPECIAL |
| 52 | GREEN TOP |
| 53 | GREEN 2ND TOP |
| 54 | GREEN MIDDLE |
| 55 | GREEN 2ND BOT |
| 56 | GREEN BOTTOM |
| 57 | RIGHT OUTLANE |
| 58 | RIGHT RETURN |
| 59 | NOT USED |
| 60 | RED TOP |
| 61 | RED 2ND TOP |
| 62 | RED MIDDLE |
| 63 | RED 2ND BOT |
| 64 | RED BOTTOM |

## Switch table (public switch address = entry number)

| Switch | ROM text |
| --- | --- |
| 1 | PLUMB TILT |
| 2 | BALL TILT |
| 3 | CREDIT BUTTON |
| 4 | RIGHT COIN SW. |
| 5 | CENTER COIN SW. |
| 6 | LEFT COIN SW. |
| 7 | SLAM TILT |
| 8 | HISCORE RESET |
| 9 | PLAYFLD TILT |
| 10 | L. LANE CHANGE |
| 11 | R. LANE CHANGE |
| 12 | LEFT OUTLANE |
| 13 | LEFT RETURN |
| 14 | RIGHT RETURN |
| 15 | RIGHT OUTLANE |
| 16 | OUTHOLE |
| 17 | TROUGH 1 SW |
| 18 | TROUGH 2 SW |
| 19 | ADVANCE PLANET |
| 20 | SHOOTER SWITCH |
| 21 | 21 NOT USED |
| 22 | VORTEX 20K |
| 23 | VORTEX 100K |
| 24 | VORTEX EXIT |
| 25 | LEFT EJECT |
| 26 | RIGHT EJECT |
| 27 | 27 NOT USED |
| 28 | VISOR LEFT |
| 29 | VISOR LEFT 2 |
| 30 | VISOR CENTER |
| 31 | VISOR RIGHT 2 |
| 32 | VISOR RIGHT |
| 33 | R. 5BANK 1  TOP |
| 34 | R. 5BANK 2 |
| 35 | R. 5BANK 3  MID |
| 36 | R. 5BANK 4 |
| 37 | R. 5BANK 5  BOT |
| 38 | SINGLE EJECT |
| 39 | EXIT RAMP |
| 40 | ENTER RAMP |
| 41 | 41 NOT USED |
| 42 | 42 NOT USED |
| 43 | 43 NOT USED |
| 44 | RAMP DOWN |
| 45 | SCORE ENERGY |
| 46 | VISOR CLOSED |
| 47 | VISOR OPEN |
| 48 | LEFT JET |
| 49 | LEFT D.T. TOP |
| 50 | LEFT D.T. MIDDLE |
| 51 | LEFT D.T. BOTTOM |
| 52 | TOP JET |
| 53 | BOTTOM JET |
| 54 | LEFT SLING |
| 55 | RIGHT SLING |
| 56 | 10 PT SWITCH |
| 57 | 57 NOT USED |
| 58 | 58 NOT USED |
| 59 | 10 PT SWITCH |
| 60 | 10 PT SWITCH |
| 61 | 61 NOT USED |
| 62 | 62 NOT USED |
| 63 | 63 NOT USED |
| 64 | 64 NOT USED |

## Coil table (coil-test order)

The first sixteen entries alternate each switched A-side load with its C-side partner; each controlled and special
solenoid entry after them is followed by a blank 14-byte entry. The coil-test run pairs the 30 named entries, in this order,
with public solenoids 1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32 and 9-22.

| Entry | ROM text |
| --- | --- |
| 1 | OUTHOLE |
| 2 | KNOCKER |
| 3 | BALL RELEASE |
| 4 | UP.  F.L. TOP F.L.2 |
| 5 | SINGLE EJECT |
| 6 | BACKGLS. L. FLASH |
| 7 | DROP TARGET |
| 8 | BACKGLS. R. FLASH |
| 9 | RAISE RAMP |
| 10 | LOW. F.L. TOP F.L.1 |
| 11 | LOWER RAMP |
| 12 | ENERGY FLASH L. |
| 13 | LEFT EJECT |
| 14 | LEFT FLASH L. |
| 15 | RIGHT EJECT |
| 16 | SUN FLASH L. |
| 17 | BACKGLS. FACE |
| 18 | (blank) |
| 19 | R. VISOR G.I. |
| 20 | (blank) |
| 21 | BACKGLS G.I. |
| 22 | (blank) |
| 23 | PLAYFLD G.I. |
| 24 | (blank) |
| 25 | VISOR MOTOR |
| 26 | (blank) |
| 27 | A-C SELECT |
| 28 | (blank) |
| 29 | TOP F.L.3 |
| 30 | (blank) |
| 31 | TOP F.L.4 CENTER |
| 32 | (blank) |
| 33 | BOTTOM JET |
| 34 | (blank) |
| 35 | L. VISOR G.I. |
| 36 | (blank) |
| 37 | LEFT JET |
| 38 | (blank) |
| 39 | LEFT KICKER |
| 40 | (blank) |
| 41 | RIGHT KICKER |
| 42 | (blank) |
| 43 | TOP JET |
| 44 | (blank) |

The ROM's font has no glyph for `-` (the coil test displays `A-C SELECT` as `A C SELECT`) and draws `5`/`S` and `0`/`O` with
the same segments; the text above is the stored table text.
