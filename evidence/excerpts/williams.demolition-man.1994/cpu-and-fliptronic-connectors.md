# Demolition Man — CPU Board and Fliptronic II Board Connector Lists

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, read from the
rendered pages (308 dpi 1-bit scan), not from the OCR text:

- PDF page 133, printed `DEMOLITION MAN 3-29`, `A-12742-50028 CPU Board`: the board outline drawing and the
  connector lists J201-J212.
- PDF page 135, printed `DEMOLITION MAN 3-31`, `A-15472-1 Fliptronic II Board`: the board outline drawing and the
  connector lists J901-J907.

(PDF page 134 is the Dot Matrix Controller board and PDF page 132 the Sound Board; neither is transcribed here.)
Every pin line is transcribed with its literal text. `N/C` is printed as `N/C`. Ribbon-cable connectors are printed
as one line each. Spelling, capitalization and abbreviations (`sw.`, `ded.`, `col.`, `Brd`) are literal; the CPU
board list prints the coin-door destination as `Coin Door Brd J1-8` on some lines and `Coin Door J1-5` or `Coin
Door J3-2` on others, kept as printed.

## CPU Board A-12742-50028 (PDF page 133, printed 3-29)

| Pin | Printed text |
| --- | --- |
| J201 | 26-pin Ribbon Cable, data, To/from J602 |
| J202 | 34-pin Ribbon Cable, data, To/from J903; P1; J601 |
| J203 | Not Used |
| J204 | 26-pin Ribbon Cable, data To/from 8-Driver Board J1 |
| J205-1 | Orange-Brown, ded. sw. row 1, to Coin Door Brd J1-8 |
| J205-2 | Orange-Red, ded. sw. row 2, to Coin Door Brd J1-7 |
| J205-3 | Orange-Black, ded. sw. row 3, to Coin Door Brd J1-6 |
| J205-4 | Orange-Yellow, ded. sw. row 4, to Coin Door J1-5 |
| J205-5 | N/C |
| J205-6 | Orange-Green, ded. sw. row 5, to Coin Door Brd J1-4 |
| J205-7 | Orange-Blue, ded. sw. row 6, to Coin Door Brd J1-3 |
| J205-8 | Orange-Violet, ded. sw. row 7, to Coin Door Brd J1-2 |
| J205-9 | Orange-Gray, ded. sw. row 8, to Coin Door Brd J1-1 |
| J205-10 | Black, ground, to Coin Door Brd J1-10 |
| J205-11 | N/C |
| J205-12 | Orange-White, sw. enable, to Coin Door Brd J1-11 |
| J206-1 | N/C |
| J206-2 | N/C |
| J206-3 | N/C |
| J206-4 | N/C |
| J206-5 | N/C |
| J206-6 | N/C |
| J206-7 | N/C |
| J206-8 | N/C |
| J206-9 | N/C |
| J207-1 | Green-Brown, sw. col. 1, to playfield switches |
| J207-2 | Green-Red, sw. col. 2, to playfield/cabinet switches |
| J207-3 | Green-Orange, sw. col. 3, to playfield switches |
| J207-4 | Green-Yellow, sw. col. 4, to playfield switches |
| J207-5 | Green-Black, sw. col. 5, to playfield switches |
| J207-6 | Green-Blue, sw. col. 6, to playfield switches |
| J207-7 | Green-Violet, sw. col. 7, to playfield switches |
| J207-8 | N/C |
| J207-9 | Green-Gray, sw. col. 8, to playfield switches |
| J208-1 | N/C |
| J208-2 | N/C |
| J208-3 | N/C |
| J208-4 | N/C |
| J208-5 | N/C |
| J208-6 | N/C |
| J208-7 | N/C |
| J208-8 | N/C |
| J208-9 | N/C |
| J209-1 | White-Brown, sw. row 1, to playfield switches |
| J209-2 | White-Red, sw. row 2, to playfield switches |
| J209-3 | White-Orange, sw. row 3, to playfield switches |
| J209-4 | White-Yellow, sw. row 4, to playfield switches |
| J209-5 | White-Green, sw. row 5, to playfield switches |
| J209-6 | N/C |
| J209-7 | White-Blue, sw. row 6, to playfield switches |
| J209-8 | White-Violet, sw. row 7, to playfield switches |
| J209-9 | White-Gray, sw. row 8, to playfield switches |
| J210-1 | Black, ground, from Power Driver Brd J114-5,7 |
| J210-2 | N/C |
| J210-3 | Black, ground, from Power Driver Brd J114-5,7 |
| J210-4 | Gray, +5V,  from Power Driver Brd J114-3,4 |
| J210-5 | Gray, +5V, from Power Driver Brd J114-3,4 |
| J210-6 | Gray-Green, +12V, from Power Driver Brd J114-1,2 |
| J210-7 | Gray-Green, +12V, from Power Driver Brd J114-1,2 |
| J211 | 34-pin Ribbon Cable, data, To/from J113 |
| J212-1 | Green-Brown, sw. col. 1, to Coin Door Brd J3-1 |
| J212-2 | Green-Red, sw. col. 2, to Coin Door J3-2 |
| J212-3 | N/C |
| J212-4 | White-Brown, sw. row 1, to Coin Door Brd J3-3 |
| J212-5 | N/C |
| J212-6 | White-Red, sw. row 2, to Coin Door Brd  J3-4 |
| J212-7 | White-Orange, sw. row 3, Coin Door Brd J3-5 |
| J212-8 | White-Yellow, sw. row 4, to Coin Door Brd J3-6 |

The printed board drawing also labels the headers J201 (pins 1-26), J202 (1-34), J203 (1-3), J204 (1-26),
J205 (1-12), J206 (1-9), J207 (1-9), J208 (1-9), J209 (1-9), J210 (1-7), J211 (1-34) and J212 (1-8).

Observations: J205 prints eight dedicated rows (`ded. sw. row 1` through `row 8` on pins 1-4 and 6-9; J205-5 and
J205-11 are `N/C`); J207 prints sw. col. 1-7 on pins 1-7 and col. 8 on pin 9 (pin 8 is `N/C`); J209 prints sw. row
1-5 on pins 1-5, row 6 on pin 7, row 7 on pin 8 and row 8 on pin 9 (pin 6 is `N/C`). J207-2 alone is printed `to
playfield/cabinet switches`.

## Fliptronic II Board A-15472-1 (PDF page 135, printed 3-31)

| Pin | Printed text |
| --- | --- |
| J901-1 | White-Blue, 50VAC, from Power Driver Board J104-2 |
| J901-2 | White-Blue, 50VAC, loop from J901-1 |
| J901-3 | White-Blue, 50VAC, from Power Driver Board J104-1 |
| J901-4 | N/C |
| J901-5 | White-Blue, 50VAC, loop from J901-3 |
| J902-1 | Orange-Gray, holding, upper left flipper coil |
| J902-2 | N/C |
| J902-3 | Yellow-Gray, power, upper left flipper coil |
| J902-4 | Orange-Violet, holding, upper right flipper coil |
| J902-5 | N/C |
| J902-6 | Yellow-Violet, power, upper right flipper coil |
| J902-7 | Orange-Blue, holding, lower left flipper coil |
| J902-8 | N/C |
| J902-9 | Yellow-Blue, power, lower left flipper coil |
| J902-10 | N/C |
| J902-11 | Orange-Green, holding, lower right flipper coil |
| J902-12 | N/C |
| J902-13 | Yellow-Green, power, lower right flipper coil |
| J903 | 34-pin Ribbon Cable, data, To/from J202; J601; P1 |
| J904-1 | Gray, +5V, from Power Driver Board J114-3,4 |
| J904-2 | Gray-Green, +12V, from Power Driver Board J114-1,2 |
| J904-3 | N/C |
| J904-4 | Black, ground, from Power Driver Board J114-5,7 |
| J904-5 | Black, ground, from Power Driver Board J114-5,7 |
| J905-1 | Blue-Violet, F2, to right flipper opto switch board J1-1 |
| J905-2 | Blue-Gray, F4, to left flipper opto switch board J1-1 |
| J905-3 | Black-Yellow, F6, to right flipper opto switch board J1-2 |
| J905-4 | N/C |
| J905-5 | Black-Blue , F8, to left flipper opto switch board J1-2 |
| J905-6 | Orange, ground, to left flipper opto switch board J1-3 |
| J906-1 | Black-Green, F1, to lower right EOS switch |
| J906-2 | N/C |
| J906-3 | Black-Blue, F3, to lower left EOS switch |
| J906-4 | Black-Violet, F5, to upper right EOS switch (not used) |
| J906-5 | Black-Gray, F7, to upper left EOS switch |
| J906-6 | Orange, ground, to EOS switches |
| J907-1 | Red-Green, +50V, to lower right flipper coil |
| J907-2 | Red-Green, +50V, loop from J907-1 |
| J907-3 | N/C |
| J907-4 | Red-Blue, +50V to lower left flipper coil |
| J907-5 | Red-Blue, +50V loop from J907-4 |
| J907-6 | Red-Violet, +50V, to upper right flipper coil |
| J907-7 | Red-Violet, +50V, loop from J907-6 |
| J907-8 | Red-Gray, +50V, to upper left flipper coil |
| J907-9 | Red-Gray, +50V, loop from J907-8 |

The printed board drawing labels the headers J901 (pins 1-5), J902 (1-13), J903 (1-34), J904 (1-5), J905 (1-6),
J906 (1-6) and J907 (1-9).

Observations and internal disagreements (kept literal above, none resolved):

- J905-1 and J905-3 carry swapped wire colours against the Fliptronic II drawings and the flipper opto board
  lists: this list prints J905-1 `Blue-Violet, F2` and J905-3 `Black-Yellow, F6`; PDF pages 115, 117 and 118 print
  J905-1 `Black-Yellow` (F2) and J905-3 `Blue-Violet` (F6). Pins, F-numbers and destination boards agree.
- J906-4 / F5 (upper right end-of-stroke) is printed `(not used)`; J902-4 and J902-6 (the upper right hold and power
  drive) are listed as `upper right flipper coil` with no mention of the claw magnet here (the claw magnet note is on
  PDF pages 115 and 102, see `flipper-circuits.md`).
- J901-1 and J901-3 name Power Driver Board `J104-2` and `J104-1`; the Power Driver Board list (PDF page 136) prints
  `J104-1 ... to Fliptronic II Board J901-3` and `J104-2 ... to Fliptronic II Board J901-1`, which agrees.
- The CPU board list's J207 and J209 destination text is `to playfield switches` throughout; the cabinet and
  coin-door switches are reached through J212 (columns 1-2, rows 1-4) and the coin door interface board.
