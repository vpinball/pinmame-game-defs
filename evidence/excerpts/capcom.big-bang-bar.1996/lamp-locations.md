# Big Bang Bar — Cabinet, Playfield, & Backbox Lamps

Transcribed from `Capcom_1996_Big_Bang_Bar_Manual.pdf`, printed page 81 (PDF page 85), the
full address table (printed page 80 / PDF 84 is the companion numbered location diagram,
not a table). Rendered at 300 dpi first, then re-rendered at 600 dpi split into left/right
halves for exact digit-level confirmation of every row (111 rows including every "UNUSED"
row). PDF page number = printed page number + 4.

Title: "CABINET, PLAYFIELD, & BACKBOX LAMPS". Columns: `NO | SOFTWARE TEST REFERENCE C1-04 |
WIRE COLOR (COLUMN | ROW) | BULB | PART NUMBER`, printed as two column-blocks on the page
(left block NO 1-47 = matrix bank "A"; right block NO 48-111 = matrix bank "B" plus one
non-matrix entry).

**Addressing convention**: the "SOFTWARE TEST REFERENCE" column uses two-digit column/row
notation followed by a bank letter, e.g. `11A` = matrix column 1, row 1, bank A; `88B` =
column 8, row 8, bank B. This is the "2 x (8x8 Matrix) = 128 Lamps" structure the pinned
PinMAME driver source comments describe. The public PinMAME address is
`(column-1)*8+row` for bank A (1-64) and `64+(column-1)*8+row` for bank B (65-128); this was
independently confirmed against the retained script's own `Lampz.MassAssign(N)=L<N>`
bindings (e.g. test-ref `11A`, address 1, binds object `L01`; test-ref `21A`, address 9,
binds object `L9`). The `NO` column is a plain 1-111 sequence counter over only the
*populated* (non-"UNUSED") rows; it is not itself the address. Row 111 ("FLUORESCENT IN
BACKBOX") has no column/row/bank code at all and is wired directly (`WHT` / `WHT/BLK`, bulb
type `T8`) — a direct-wired fixture outside the CPU-multiplexed lamp matrix entirely, with
no PinMAME address.

Wire-color convention (confirmed against the companion schematic, sheets 9/10 of 12): bank-A
columns are `RED/<color>`, bank-A rows are `YEL/<color>`; bank-B columns are `ORG/<color>`,
bank-B rows are `BLU/<color>`.

## Bank A (NO 1-47, addresses 1-64)

| NO | Test ref | Column wire | Row wire | Bulb | Part # |
| --- | --- | --- | --- | --- | --- |
| 1 | 11A COIN DOOR 1&2 | RED/BRN | YEL/BRN | 259 | LP00113 |
| 2 | 12A COIN DOOR 3&4 | RED/BLK | YEL/BRN | 259 | LP00113 |
| 3 | 13A START | RED/ORG | YEL/BRN | 555 | LP00100 |
| — | 14A-18A UNUSED | RED/YEL..RED/GRY | YEL/BRN | — | — |
| 4 | 21A 4-BANK G.I. 1 | RED/BRN | YEL/RED | 44 | LP00104 |
| 5 | 22A 4-BANK G.I. 2 | RED/BLK | YEL/RED | 44 | LP00104 |
| 6 | 23A 4-BANK G.I. 3 | RED/ORG | YEL/RED | 44 | LP00104 |
| 7 | 24A L. SLINGSHOT G.I. 1 | RED/YEL | YEL/RED | 44 | LP00104 |
| — | 25A UNUSED | RED/GRN | YEL/RED | — | — |
| 8 | 26A L. FLIPPER G.I. 1 | RED/BLU | YEL/RED | 44 | LP00104 |
| — | 27A-28A UNUSED | RED/VIO, RED/GRY | YEL/RED | — | — |
| 9 | 31A U.R. FLIPPER G.I. 1 | RED/BRN | YEL/ORG | 44 | LP00104 |
| 10 | 32A EJECT HOLE G.I. 1 | RED/BLK | YEL/ORG | 44 | LP00104 |
| 11 | 33A SPACESHIP G.I. 1 | RED/ORG | YEL/ORG | 44 | LP00104 |
| 12 | 34A SPACESHIP G.I. 2 | RED/YEL | YEL/ORG | 44 | LP00104 |
| 13 | 35A R. SLINGSHOT G.I. 1 | RED/GRN | YEL/ORG | 44 | LP00104 |
| 14 | 36A R. SLINGSHOT G.I. 2 | RED/BLU | YEL/ORG | 44 | LP00104 |
| 15 | 37A R. FLIPPER G.I. 1 | RED/VIO | YEL/ORG | 44 | LP00104 |
| 16 | 38A R. FLIPPER G.I. 2 | RED/GRY | YEL/ORG | 44 | LP00104 |
| 17 | 41A TUBE G.I. 1 | RED/BRN | YEL/BLK | 44 | LP00104 |
| 18 | 42A TUBE G.I. 2 | RED/BLK | YEL/BLK | 44 | LP00104 |
| 19 | 43A TUBE G.I. 3 | RED/ORG | YEL/BLK | 44 | LP00104 |
| 20 | 44A TUBE G.I. 4 | RED/YEL | YEL/BLK | 44 | LP00104 |
| 21 | 45A TUBE G.I. 5 | RED/GRN | YEL/BLK | 44 | LP00104 |
| 22 | 46A L. ORBIT CHASE 1 | RED/BLU | YEL/BLK | 44 | LP00104 |
| 23 | 47A L. ORBIT CHASE 2 | RED/VIO | YEL/BLK | 44 | LP00104 |
| 24 | 48A L. ORBIT CHASE 3 | RED/GRY | YEL/BLK | 44 | LP00104 |
| 25 | 51A HOOT G.I. 1 | RED/BRN | YEL/GRN | 44 | LP00104 |
| 26 | 52A HOOT G.I. 2 | RED/BLK | YEL/GRN | 44 | LP00104 |
| 27 | 53A HOOT G.I. 3 | RED/ORG | YEL/GRN | 44 | LP00104 |
| 28 | 54A HOOT G.I. 4 | RED/YEL | YEL/GRN | 44 | LP00104 |
| 29 | 55A ALIEN G.I. 1 | RED/GRN | YEL/GRN | 44 | LP00104 |
| 30 | 56A ALIEN G.I. 2 | RED/BLU | YEL/GRN | 44 | LP00104 |
| 31 | 57A ALIEN G.I. 3 | RED/VIO | YEL/GRN | 44 | LP00104 |
| 32 | 58A CAPTIVE G.I. 1 | RED/GRY | YEL/GRN | 44 | LP00104 |
| 33 | 61A R. ORBIT CHASE 1 | RED/BRN | YEL/BLU | 44 | LP00104 |
| 34 | 62A R. ORBIT CHASE 2 | RED/BLK | YEL/BLU | 44 | LP00104 |
| 35 | 63A R. ORBIT CHASE 3 | RED/ORG | YEL/BLU | 44 | LP00104 |
| 36 | 64A ALIEN LOCK LEFT | RED/YEL | YEL/BLU | 44 | LP00104 |
| 37 | 65A ALIEN LOCK RIGHT | RED/GRN | YEL/BLU | 44 | LP00104 |
| — | 66A-68A UNUSED | RED/BLU..RED/GRY | YEL/BLU | — | — |
| 38 | 71A ROLLOVER "B" | RED/BRN | YEL/VIO | 44 | LP00104 |
| 39 | 72A ROLLOVER "A" | RED/BLK | YEL/VIO | 44 | LP00104 |
| 40 | 73A ROLLOVER "R" | RED/ORG | YEL/VIO | 44 | LP00104 |
| 41 | 74A TUBE SIGN X-BALL | RED/YEL | YEL/VIO | 44 | LP00104 |
| 42 | 75A TUBE SIGN 10 MILL | RED/GRN | YEL/VIO | 44 | LP00104 |
| 43 | 76A TUBE SIGN JACKPOT | RED/BLU | YEL/VIO | 44 | LP00104 |
| — | 77A-78A UNUSED | RED/VIO, RED/GRY | YEL/VIO | — | — |
| 44 | 81A (ELECTRO) RAMP 1 | RED/BRN | YEL/GRY | 44 | LP00104 |
| 45 | 82A (ELECTRO) RAMP 2 | RED/BLK | YEL/GRY | 44 | LP00104 |
| 46 | 83A (ELECTRO) RAMP 3 | RED/ORG | YEL/GRY | 44 | LP00104 |
| — | 84A-85A (ELECTRO) UNUSED | RED/YEL, RED/GRN | YEL/GRY | — | — |
| 47 | 86A (ELECTRO) BLACK LIGHT | RED/BLU | YEL/GRY | 44 | LP00109 |
| — | 87A-88A (ELECTRO) UNUSED | RED/VIO, RED/GRY | YEL/GRY | — | — |

## Bank B (NO 48-111, addresses 65-128)

| NO | Test ref | Column wire | Row wire | Bulb | Part # |
| --- | --- | --- | --- | --- | --- |
| 48 | 11B BONUS 2X | ORG/BRN | BLU/BRN | 44 | LP00104 |
| 49 | 12B BONUS 3X | ORG/RED | BLU/BRN | 44 | LP00104 |
| 50 | 13B MODE: UNDERGROUND | ORG/BLK | BLU/BRN | 44 | LP00104 |
| 51 | 14B MODE: BIG BANG | ORG/YEL | BLU/BRN | 555 | LP00100 |
| 52 | 15B MODE: BAR ROOM BRAWL | ORG/GRN | BLU/BRN | 555 | LP00100 |
| 53 | 16B MODE: RAY'S BALL BUSTERS | ORG/BLU | BLU/BRN | 555 | LP00100 |
| 54 | 17B MODE: LOOPED IN SPACE | ORG/VIO | BLU/BRN | 555 | LP00100 |
| 55 | 18B SHOOT AGAIN | ORG/GRY | BLU/BRN | 555 | LP00100 |
| 56 | 21B MODE: BABE SCANNER | ORG/BRN | BLU/RED | 44 | LP00104 |
| 57 | 22B MODE: CHASE WAITRESS | ORG/RED | BLU/RED | 44 | LP00104 |
| 58 | 23B SHOOT: COSMIC DARTZ | ORG/BLK | BLU/RED | 44 | LP00104 |
| 59 | 24B SPECIAL (OUTLANE R.) | ORG/YEL | BLU/RED | 555 | LP00100 |
| 60 | 25B INLANE RIGHT | ORG/GRN | BLU/RED | 555 | LP00100 |
| 61 | 26B BONUS 5X | ORG/BLU | BLU/RED | 44 | LP00104 |
| 62 | 27B BONUS 4X | ORG/VIO | BLU/RED | 555 | LP00100 |
| 63 | 28B MODE: TUBE DANCER | ORG/GRY | BLU/RED | 555 | LP00100 |
| 64 | 31B SHOOT: LEFT ORBIT | ORG/BRN | BLU/ORG | 555 | LP00100 |
| 65 | 32B SHOOT: BABE SCANNER | ORG/RED | BLU/ORG | 555 | LP00100 |
| 66 | 33B 4-BANK MARS | ORG/BLK | BLU/ORG | 555 | LP00100 |
| 67 | 34B 4-BANK PYTHOS | ORG/YEL | BLU/ORG | 555 | LP00100 |
| 68 | 35B 4-BANK VENUS | ORG/GRN | BLU/ORG | 555 | LP00100 |
| 69 | 36B 4-BANK MERCURY | ORG/BLU | BLU/ORG | 555 | LP00100 |
| 70 | 37B FREE SHOT (OUTLANE L.) | ORG/VIO | BLU/ORG | 44 | LP00104 |
| 71 | 38B INLANE LEFT | ORG/GRY | BLU/ORG | 44 | LP00104 |
| 72 | 41B MODE: COSMIC DARTZ | ORG/BRN | BLU/YEL | 44 | LP00104 |
| 73 | 42B MODE: TOUR DE BAR | ORG/RED | BLU/YEL | 44 | LP00104 |
| 74 | 43B MODE: MOSH A GO-GO | ORG/BLK | BLU/YEL | 44 | LP00104 |
| 75 | 44B MODE: HAPPY HOUR | ORG/YEL | BLU/YEL | 44 | LP00104 |
| 76 | 45B MODE: EXTRA BALL | ORG/GRN | BLU/YEL | 44 | LP00104 |
| 77 | 46B MODE: GET LUCKY | ORG/BLU | BLU/YEL | 44 | LP00104 |
| 78 | 47B MODE: LUNA PALOOZA | ORG/VIO | BLU/YEL | 44 | LP00104 |
| — | 48B UNUSED | ORG/GRY | BLU/YEL | — | — |
| 79 | 51B RAMP JACKPOT | ORG/BRN | BLU/GRN | 44 | LP00104 |
| 80 | 52B RAMP STANDUP LEFT | ORG/RED | BLU/GRN | 44 | LP00104 |
| 81 | 53B RAM STANDUP RIGHT [sic, printed "RAM"] | ORG/BLK | BLU/GRN | 44 | LP00104 |
| 82 | 54B RAMP STANDUP SIDE | ORG/YEL | BLU/GRN | 44 | LP00104 |
| 83 | 55B DOUBLE JACKPOT | ORG/GRN | BLU/GRN | 44 | LP00104 |
| 84 | 56B SHOOT: TOUR DE BAR | ORG/BLU | BLU/GRN | 555 | LP00100 |
| 85 | 57B SHOOT: UNDERGROUND 1 | ORG/VIO | BLU/GRN | 555 | LP00100 |
| 86 | 58B QUALIFY MODE | ORG/GRY | BLU/GRN | 44 | LP00104 |
| 87 | 61B CAPTIVE: LEFT 4 | ORG/BRN | BLU/BLK | 555 | LP00100 |
| 88 | 62B CAPTIVE: LEFT 3 | ORG/RED | BLU/BLK | 555 | LP00100 |
| 89 | 63B CAPTIVE: LEFT 2 | ORG/BLK | BLU/BLK | 555 | LP00100 |
| 90 | 64B CAPTIVE: LEFT 1 | ORG/YEL | BLU/BLK | 555 | LP00100 |
| 91 | 65B CAPTIVE: RIGHT 4 | ORG/GRN | BLU/BLK | 555 | LP00100 |
| 92 | 66B CAPTIVE: RIGHT 3 | ORG/BLU | BLU/BLK | 555 | LP00100 |
| 93 | 67B CAPTIVE: RIGHT 2 | ORG/VIO | BLU/BLK | 555 | LP00100 |
| 94 | 68B CAPTIVE: RIGHT 1 | ORG/GRY | BLU/BLK | 555 | LP00100 |
| 95 | 71B 3-BANK URANUS | ORG/BRN | BLU/VIO | 44 | LP00104 |
| 96 | 72B 3-BANK NEPTUNE | ORG/RED | BLU/VIO | 44 | LP00104 |
| 97 | 73B 3-BANK PLUTO | ORG/BLK | BLU/VIO | 44 | LP00104 |
| 98 | 74B SHOOT: RIGHT ORBIT | ORG/YEL | BLU/VIO | 555 | LP00100 |
| 99 | 75B D.J. EYES G.I. | ORG/GRN | BLU/VIO | 555 | LP00100 |
| 100 | 76B SHOOT: LUNA PALOOZA | ORG/BLU | BLU/VIO | 44 | LP00104 |
| 101 | 77B ISLAND: LOCK READY | ORG/VIO | BLU/VIO | 44 | LP00104 |
| 102 | 78B ISLAND: MODE READY | ORG/GRY | BLU/VIO | 44 | LP00104 |
| 103 | 81B SHOOT: UNDERGROUND 2 | ORG/BRN | BLU/GRY | 44 | LP00104 |
| 104 | 82B STAR BUMPER LEFT | ORG/RED | BLU/GRY | 555 | LP00100 |
| 105 | 83B STAR BUMPER MIDDLE | ORG/BLK | BLU/GRY | 555 | LP00100 |
| 106 | 84B STAR BUMPER RIGHT | ORG/YEL | BLU/GRY | 555 | LP00100 |
| 107 | 85B DANCE FLOOR | ORG/GRN | BLU/GRY | 44 | LP00104 |
| 108 | 86B SHOOT: EXTRA BALL | ORG/BLU | BLU/GRY | 555 | LP00100 |
| 109 | 87B SHOOT: BIG BANG | ORG/VIO | BLU/GRY | 555 | LP00100 |
| 110 | 88B U.R. FLIPPER G.I.2 | ORG/GRY | BLU/GRY | 44 | LP00104 |
| 111 | FLUORESCENT IN BACKBOX (no column/row/bank code; direct-wired) | WHT | WHT/BLK | T8 | LP00105 |

Only lamp 111 has no column/row/bank code. Every other slot in the 8x8x2=128-position
address space is either populated (110 addresses) or explicitly printed "UNUSED" (18
addresses: 14A-18A, 25A, 27A-28A, 66A-68A, 77A-78A, 84A-85A, 87A-88A, 48B — addresses 4-8,
13, 15-16, 46-48, 55-56, 60-61, 63-64, 96 by the column/row formula above). 110+18=128,
confirming the full matrix space is accounted for.
