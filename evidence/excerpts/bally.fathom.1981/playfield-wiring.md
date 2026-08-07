# Bally Fathom — Playfield wiring diagram (W-1192-30)

Source: `Bally_1981_Fathom_Schematics.pdf`, PDF page 11. Title block reads `WIRING DIAGRAM
PLAYFIELD` / `FATHOM` / `# 1233` / `W-1192-30`, sheet `2`. Transcribed by hand from a 400 dpi render.

Notes printed on the sheet:

1. `INDICATES NOT USED`
2. `N/U = NOT USED ON PLAYFIELD`
3. `* INDICATES AID TEST POINT`
4. `COIL DIODES ARE IN4004, (E-587-6) SWITCH DIODES ARE IN 4148, (E-587-14) ALL CAPACITORS ARE .05 MFD. (E-586-80)`
5. `GERMANY ONLY - CAPACITOR .01 MFD. @ 500V. (E-586-65)`

The playfield block is labelled `PLAYFIELD A6`.

## Switch matrix

Eight return lines and six strobe lines, drawn as a grid of switch contacts each with a series
diode. Wire number, then MPU connector:

| return | wire | MPU pin |
| --- | --- | --- |
| `I 0` | 54 | `A4J2-8` |
| `I 1` | 63 | `A4J2-9` |
| `I 2` | 57 | `A4J2-10` |
| `I 3` | 78 | `A4J2-11` |
| `I 4` | 60 | `A4J2-12` |
| `I 5` | 56 | `A4J2-13` |
| `I 6` | 65 | `A4J2-14` |
| `I 7` | 52 | `A4J2-15` |

| strobe | wire | MPU pin |
| --- | --- | --- |
| `ST 0` | 51 | `A4J2-1` |
| `ST 1` | 70 | `A4J2-2` |
| `ST 2` | 93 | `A4J2-3` |
| `ST 3` | 53 | `A4J2-4` |
| `ST 4` | 31 | `A4J2-5` |
| `ST 5` | 72 | `A4J4-8` |

Five strobes come off `A4J2`; the sixth, `ST 5`, comes off a different MPU connector, `A4J4` pin 8.
On the A3 solenoid driver sheet, `A4J4` pin 8 is the same MPU line as continuous output `CONT 3`,
`PB7`. That is why one continuous solenoid address on this machine carries a switch-column strobe
rather than a coil.

The grid's switch names, read column by column (`ST 0` first) and row by row (`I 0` first), agree
position for position with the printed Switch Assembly Self-Test Display Numbers table in the
manual, on every position that table fills in. `ST 0` column, `I 0`..`I 7`: `OUTHOLE`,
`#1 LEFT OF OUTHOLE`, `#2 LEFT AND #1 RIGHT OF OUTHOLE`, `TOP SAUCER`, `RIGHT SAUCER`,
(`I 5` blank on the playfield sheet, `CREDIT BUTTON` in the manual's table because it is a door
switch), `RIGHT FLIPPER BUTTON`, (`I 7` blank). A note beside the playfield diagram in the manual
reads `NOTE: CABINET: 15, 16, 07` and `DOOR: 06, 09`, which is why several matrix positions are not
drawn on the playfield sheet.

## Solenoid coils, wire numbers and driver-board connector

| coil, printed name | wire | connector |
| --- | --- | --- |
| `LEFT FLIPPER` | 40 | `A3J1-8` |
| `RIGHT FLIPPER` / `UPPER RIGHT FLIPPER` | 70 | `A3J1-9` |
| `OUTHOLE KICKER` | 95 | `A3J1-5` |
| `LEFT THUMPER BUMPER` | 85 | `A3J5-10` |
| `RIGHT THUMPER BUMPER` | 78 | `A3J5-11` |
| `BOTTOM THUMPER BUMPER` | 80 | `A3J5-12` |
| `LEFT SLINGSHOT` | 71 | `A3J5-9` |
| `RIGHT SLINGSHOT` | 74 | `A3J5-15` |
| `RIGHT INLINE DROP TARGET RESET` | 91 | `A3J2-11` |
| `2ND BLUE INLINE DROP TARGET` / `RT. SAUCER` | 83 | `A3J5-14` |
| `3RD BLUE INLINE DROP TARGET` | 18 | `A3J5-8` |
| `1ST BLUE INLINE DROP TARGET` / `TOP SAUCER` | 67 | `A3J5-13` |
| the three green in-line drop coils paired with the three bank-reset coils | 71, 78, 74 | `A3J2-10`, `A3J2-9`, `A3J2-4` |

The last row is deliberately not split into three rows. The playfield sheet draws the six coils
`3RD GREEN INLINE DROP TARGET`, `3 MIDDLE DROP TARGET RESET`, `2ND GREEN INLINE DROP TARGET`,
`6 DROP TARGET RESET`, `1ST GREEN INLINE DROP TARGET` and `3 TOP DROP TARGET RESET` in one block
with the three wires 71, 78 and 74 entering it, and the retained scan does not make it unambiguous
which wire enters which coil pair. The A3 solenoid driver sheet states the pairing directly on its
own connector pins (`A3J2-9` = 3 Top reset or 1st Green in-line, `A3J2-4` = 6 Drop reset or 2nd
Green in-line, `A3J2-10` = 3 Middle reset or 3rd Green in-line) and is used for that instead.

The `+43 VDC` solenoid bus enters at `A2J1-7`, wire 60, through a `1A S.B.` fuse.

Five of these wires reach two coils each, and the pair is drawn with a ganged contact between them:
those are the coils the `SOLENOID EXPANDER RELAY` selects. The relay block is drawn beside them and
labelled `SOLENOID EXPANDER RELAY`, with wires 91 and 75 annotated. The `SOLENOID EXPANDER A15`
connector `J1` pinout is printed:

| A15 J1 pin | function | wire |
| --- | --- | --- |
| 1 | `SW. ILL. BUSS` | 20 |
| 2 | `SCR ANODE LAMP DRIVER` | 20 |
| 3 | `GND` | 80 |
| 4 | `N/U` | — |
| 5 | `75 SOL. BUSS` | 75 |
| 6 | `KEY` | — |
| 7 | `91 SOL. BUSS` | 91 |
| 8 | `N/U` | — |
| 9 | `43VDC SOL BUSS` | 30 |
| 10 | `N/U` | — |

A separate coil block labelled `SOLENOID EXPANDER LITE` is drawn below it.

## General illumination

| wire | connector |
| --- | --- |
| 10 | `A2J1-4` |
| 70 | `A2J1-1` |
| 40 | `A2J1-6` |
| 50 | `A2J1-3` |

annotated `5.9 VAC GEN. ILLUM. RET.`. Wire 20 goes to `A2J1-5 FEATURE LAMP BUS`. General
illumination on this machine is an unswitched transformer secondary, not a controller output.

## Lamp harness, playfield and back box

`A5J1` (`TO PLAYFIELD`), wire then pin then printed function:

| wire | pin | function |
| --- | --- | --- |
| 58 | `A5J1-18` | `50K RIGHT RETURN LANE` |
| 60 | `A5J1-19` | `1K BLUE BONUS` |
| 57 | `A5J1-17` | `5K BLUE BONUS` |
| 12 | `A5J1-23` | `9K BLUE BONUS` |
| 54 | `A5J1-14` | `3X BLUE BONUS` |
| 13 | `A5J1-15` | `1K GREEN BONUS` |
| 90 | `A5J1-16` | `5K GREEN BONUS` |
| 78 | `A5J1-28` | `9K GREEN BONUS` |
| 50 | `A5J1-24` | `3X GREEN BONUS` |
| 75 | `A5J1-25` | `"C" LANE` |
| 91 | `A5J1-26` | `N/U` |
| 53 | `A5J1-27` | `RIGHT THUMPER BUMPER` |
| 41 | `A5J1-1` | `RIGHT OUT SPECIAL` |
| 43 | `A5J1-9` | `2K BLUE BONUS` |
| 51 | `A5J1-8` | `6K BLUE BONUS` |
| 45 | `A5J1-3` | `10K BLUE BONUS` |
| 52 | `A5J1-2` | `4X BLUE BONUS` |
| 23 | `A5J1-10` | `2K GREEN BONUS` |
| 34 | `A5J1-7` | `6K GREEN BONUS` |
| 25 | `A5J1-6` | `10K GREEN BONUS` |
| 48 | `A5J1-5` | `4X GREEN BONUS` |
| 65 | `A5J1-11` | `"B" LANE` |
| 35 | `A5J1-4` | `N/U` |
| 61 | `A5J1-12` | `BOTTOM THUMPER BUMPER` |
| 96 | `A5J1-13` | `RELEASE LAGOON CAPTIVE BALL` |

`A5J3` (`TO PLAYFIELD`):

| wire | pin | function |
| --- | --- | --- |
| 43 | `A5J3-26` | `LEFT OUT SPECIAL` |
| 36 | `A5J3-25` | `3K BLUE BONUS` |
| 67 | `A5J3-19` | `7K BLUE BONUS` |
| 13 | `A5J3-17` | `ADVANCE GREEN BONUS (2)` |
| 25 | `A5J3-16` | `5X BLUE BONUS` |
| 98 | `A5J3-23` | `3K GREEN BONUS` |
| 40 | `A5J3-27` | `7K GREEN BONUS` |
| 30 | `A5J3-21` | `5X GREEN BONUS` |
| 64 | `A5J3-20` | `"A" LANE` |
| 23 | `A5J3-22` | `SAME PLAYER SHOOT AGAIN` |
| 72 | `A5J3-24` | `LEFT THUMPER BUMPER` |
| 10 | `A5J3-1` | `50K LEFT RETURN LANE` |
| 21 | `A5J3-12` | `4K BLUE BONUS` |
| 53 | `A5J3-15` | `8K BLUE BONUS` |
| 20 | `A5J3-11` | `ADVANCE BLUE BONUS (2)` |
| 15 | `A5J3-9` | `55K BLUE BONUS` |
| 35 | `A5J3-13` | `CREDIT INDICATOR` |
| 14 | `A5J3-4` | `8K GREEN BONUS` |
| 95 | `A5J3-2` | `RELEASE CAVE CAPTIVE BALL` |
| 91 | `A5J3-10` | `55K GREEN BONUS` |
| 86 | `A5J3-18` | `A-B-C SPECIAL` |
| 81 | `A5J3-3` | `4K GREEN BONUS` |
| 84 | `A5J3-14` | `SPINNER` |

`A5J2` (`TO BACK BOX`, listed at the foot of the sheet under `TO W-1187-30`):

| wire | pin | function |
| --- | --- | --- |
| 20 | `A5J2-2` | `TO AUX. EXPANDER J1-2` |
| 12 | `A5J2-14` | `TOP SAUCER LANE ARROW` |
| 23 | `A5J2-15` | `RIGHT SAUCER ARROW` |
| 98 | `A5J2-20` | `TRIPLE PLAYFIELD SCORES` |
| 10 | `A5J2-6` | `IN SEQUENCE` |
| 91 | `A5J2-7` | `EXTRA BALL` |
| 60 | `A5J2-1` | `BONUS SPECIAL` |
| 34 | `A5J2-16` | `DOUBLE PLAYFIELD SCORES` |

The `A9` auxiliary lamp driver functions are printed vertically at the right edge of the sheet next
to the insert lamp sockets: `#2 SCAN ROLLOVER BUTTON`, `#5 BACK SCAN & 1ST LEFT LANE SCAN`,
`#1 SCAN ROLLOVER BUTTON`, `#3 SCAN ROLLOVER BUTTON`, `#4 BACK SCAN`, `#6 BACK SCAN & 2ND LEFT LANE
SCAN`, `#7 BACK SCAN & 3RD LEFT LANE SCAN`, with the connectors `A9J3-3`, `A9J3-15`, `A9J2-7`,
`A9J2-4`, `A9J2-8`, `A9J2-11`, `A9J2-14` and wire numbers 12, 13, 14, 10, 18, 20.
