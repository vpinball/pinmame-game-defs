# SlugFest factory I/O tables

Source: Williams April 1991 Operations Manual, retained original SHA-256
`94d1bce9eaca3dd1b8df72d66050edba3310afdffd86a2a8927ceffb86b9820a`.
Transcribed and visually checked against PDF pages 96-101 (printed 2-36–2-41).
Spacing is normalized; table labels, wire order and meaningful blank cells are retained.
The matrix and location tables are separate readings, not independent corroboration.

## Switch matrix — PDF 98 / printed 2-38

Columns 1–8: Green-Brown, Green-Red, Green-Orange, Green-Yellow, Green-Black,
Green-Blue, Green-Violet, Green-Gray. Schematic J20 pins 1,2,3,4,5,6,7,8
(top header appears J20; the board connector is J206). Rows 1–8: White-Brown,
White-Red, White-Orange, White-Yellow, White-Green, White-Blue, White-Violet,
White-Gray, J208 pins 1–8. Table heading: White → switch → Green.

| Row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Not Used | 21 Slam Tilt | 31 Pinch Hit | 41 Target Panel - L. | 51 Back-Row Trough | 61 Left Bleacher | 71 Not Used | 81 Not Used |
| 2 | 12 Not Used | 22 Coin Door Closed | 32 Fast Ball Pitch | 42 Target Panel - 2L. | 52 Strike Trough | 62 Middle Bleacher | 72 Not Used | 82 Not Used |
| 3 | 13 Not Used | 23 Dispenser Prize | 33 Changeup Pitch | 43 Target Panel - 3L. | 53 Not Used | 63 Right Bleacher | 73 Not Used | 83 Not Used |
| 4 | 14 Not Used | 24 Always Closed | 34 Curve Pitch | 44 Target Panel - M. | 54 Pitch Home | 64 Not Used | 74 Not Used | 84 Not Used |
| 5 | 15 Not Used | 25 Steal Base/Run | 35 Screw Ball Pitch | 45 Target Panel - 3R. | 55 Ramp Switch | 65 Not Used | 75 Not Used | 85 Not Used |
| 6 | 16 Not Used | 26 Bat Switch | 36 Throw Out Runner | 46 Target Panel - 2R. | 56 Playfield Tilt 1 | 66 Not Used | 76 Not Used | 86 Not Used |
| 7 | 17 Not Used | 27 Dispenser Low | 37 Start Player 1 | 47 Target Panel - R. | 57 Playfield Tilt 2 | 67 Not Used | 77 Not Used | 87 Not Used |
| 8 | 18 Not Used | 28 Dispenser Unjammed | 38 Start Player 2 | 48 Not Used | 58 Not Used | 68 Not Used | 78 Not Used | 88 Not Used |

Dedicated grounded switches: D1 Orange-Brown Left Coin Chute; D2 Orange-Red
Center Coin Chute; D3 Orange-Black Right Coin Chute; D4 Orange-Yellow 4th Coin
Chute; D5 Orange-Green Service Credits / Escape; D6 Orange-Blue Volume Down /
Down; D7 Orange-Violet Volume Up / Up; D8 Orange-Gray Begin Test / Enter.

## Switch locations — PDF 99 / printed 2-39

An asterisk marks “An Opto Switch Assembly”. The first eight rows 11–18 are
each explicitly Not Used. 48,53,58 are also explicitly Not Used. Blank part
numbers in those rows are genuinely blank.

| Item | Part Number | Description |
| --- | --- | --- |
| 21 | 27-1066 | Slam Tilt |
| 22 | A-8630 | Coin Door Closed |
| 23 | A-14316* | Dispenser Prize |
| 24 | A-8630 | Always Closed |
| 25 | 20-9663-C-2 | Steal Base/Run |
| 26 | 20-9663-B-1 | Bat Switch |
| 27 | 5647-12693-01 | Dispenser Low |
| 28 | 5641-09312-00 | Dispenser Unjammed |
| 31 | 20-9663-C-1 | Pinch Hit |
| 32 | 20-9663-A-6 | Fast Ball Pitch |
| 33 | 20-9663-A-4 | Changeup Pitch |
| 34 | 20-9663-A-5 | Curve Pitch |
| 35 | 20-9663-A-3 | Screw Ball Pitch |
| 36 | 20-9663-C-3 | Throw Out Runner |
| 37 | 20-9663-A-1 | Start Player 1 |
| 38 | 20-9663-A-2 | Start Player 2 |
| 41 | A-14697 | Target Panel - L. |
| 42 | A-14697 | Target Panel - 2L. |
| 43 | A-14697 | Target Panel - 3L. |
| 44 | A-14697 | Target Panel - 3R. |
| 45 | A-14697 | Target Panel - M. |
| 46 | A-14697 | Target Panel - 2R. |
| 47 | A-14697 | Target Panel - R. |
| 51 | 5647-12133-08 | Back - Row Trough |
| 52 | 5647-12133-08 | Strike Trough |
| 54 | 14-7959 | Pitch Home |
| 55 | A-14693* | Ramp Switch |
| 56 | SW-1A-117 | Playfield Tilt - 1 |
| 57 | SW-1A-117 | Playfield Tilt - 2 |
| 61 | A-14447* | Left Grand Stand |
| 62 | A-14447* | Middle Grand Stand |
| 63 | A-14447* | Right Grand Stand |

The drawing labels the seven targets in left-to-right order 41,42,43,44,45,46,47.
Its table reverses M./3R. on 44/45 against the matrix. The retained script also
pulses `41 + targetIndex` from seven consecutive left-to-right contacts, settling
44 as center and 45 as the first target right of center. Pitch Home's part cell
names the motor rather than an opto; PDF 79/2-19 separately shows the timing cam
and opto bracket.

## Lamp matrix — PDF 96 / printed 2-36

Columns 1–8, J137 pins 1–8: Yellow-Brown, Yellow-Red, Yellow-Orange,
Yellow-Black, Yellow-Green, Yellow-Blue, Yellow-Violet, Yellow-Gray.
Rows 1–8, J133 pins 1,2,4,5,6,7,8,9: Red-Brown, Red-Black, Red-Orange,
Red-Yellow, Red-Green, Red-Blue, Red-Violet, Red-Gray. Heading Yellow (B+) →
lamp → Red. All cells transcribed, including the two blank final-column cells.

| Row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Left Bleacher Home Run | 21 Middle Bleacher Home Run | 31 Right Bleacher Home Run | 41 #32 | 51 #24 | 61 #16 | 71 #8 | 81 Pinch Hit |
| 2 | 12 Out (T.-L.) | 22 Single (M.-L.) | 32 Double (B.-2) | 42 #31 | 52 #23 | 62 #15 | 72 #7 | 82 Bat Ready |
| 3 | 13 Out (T.-2L.) | 23 Double (M.-2L.) | 33 Single (B.-2L.) | 43 #30 | 53 #22 | 63 #14 | 73 #6 | 83 Steal Base |
| 4 | 14 Out (T.-3L.) | 24 Single (M.-3L.) | 34 Triple (B.-3L.) | 44 #29 | 54 #21 | 64 #13 | 74 #5 | 84 Throw Out Runner |
| 5 | 15 Out (T.-M.) | 25 Sacrifice (M.-M.) | 35 Home Run (B.-M.) | 45 #28 | 55 #20 | 65 #12 | 75 #4 | 85 Player 1 Start |
| 6 | 16 Out (T.-3R.) | 26 Single (M.-2R.) | 36 Triple (B.-2R.) | 46 #27 | 56 #19 | 66 #11 | 76 #3 | 86 Player 2 Start |
| 7 | 17 Out (T.-2R.) | 27 Double (M.-1R.) | 37 Single (B.-1R.) | 47 #26 | 57 #18 | 67 #10 | 77 #2 | 87 [blank] |
| 8 | 18 Out (T.-R.) | 28 Single (M.-R.) | 38 Double (B.-R.) | 48 #25 | 58 #17 | 68 #1 | 78 #9 | 88 [blank] |

## Lamp locations — PDF 97 / printed 2-37

Complete No./Description/Bulb# table, including its separate right-hand block.

| No. | Description | Bulb # |
| --- | --- | --- |
| 11 | Left Grand Home Run | 555 |
| 12 | Out (T. - L.) | 555 |
| 13 | Out (T. - 2L.) | 555 |
| 14 | Out (T. - 3L.) | 555 |
| 15 | Out (T. - M.) | 555 |
| 16 | Out (T. - 3R.) | 555 |
| 17 | Out (T. - 2R.) | 555 |
| 18 | Out (T. - R.) | 555 |
| 21 | Middle Grand Home Run | 555 |
| 22 | Single (M. - L.) | 555 |
| 23 | Double (M. - 2L.) | 555 |
| 24 | Single (M. - 3L.) | 555 |
| 25 | Sacrifice (M. - M.) | 555 |
| 26 | Single (M. - 2R.) | 555 |
| 27 | Double (M. - 1R.) | 555 |
| 28 | Single (M. - R.) | 555 |
| 31 | Right Grand Home Run | 555 |
| 32 | Double (B. - 2) | 555 |
| 33 | Single (B. - 2L.) | 555 |
| 34 | Tripple (B. - 3L.) | 555 |
| 35 | Home Run (B. - M.) | 555 |
| 36 | Tripple (B. - 2R.) | 555 |
| 37 | Single (B. - 1R.) | 555 |
| 38 | Double (B. - R.) | 555 |
| 41 | #32 | 555 |
| 42 | #31 | 555 |
| 43 | #30 | 555 |
| 44 | #29 | 555 |
| 45 | #28 | 555 |
| 46 | #27 | 555 |
| 47 | #26 | 555 |
| 48 | #25 | 555 |
| 51 | #24 | 555 |
| 52 | #23 | 555 |
| 53 | #22 | 555 |
| 54 | #21 | 555 |
| 55 | #20 | 555 |
| 56 | #19 | 555 |
| 57 | #18 | 555 |
| 58 | #17 | 555 |
| 61 | #16 | 555 |
| 62 | #15 | 555 |
| 63 | #14 | 555 |
| 64 | #13 | 555 |
| 65 | #12 | 555 |
| 66 | #11 | 555 |
| 67 | #10 | 555 |
| 68 | #1 | 555 |
| 71 | #8 | 555 |
| 72 | #7 | 555 |
| 73 | #6 | 555 |
| 74 | #5 | 555 |
| 75 | #4 | 555 |
| 76 | #3 | 555 |
| 77 | #2 | 555 |
| 78 | #9 | 555 |
| 81 | Pinch Hit | 555 |
| 82 | Bat Ready | 555 |
| 83 | Steal Base | 555 |
| 84 | Throw Out Runner | 555 |
| 85 | Player 1 Start | 555 |
| 86 | Player 2 Start | 555 |
| A | Gen. Illumination | 555 |
| B | Gen. Illumination | 555 |
| C | Gen. Illumination | 555 |
| D | Gen. Illumination | 555 |

The drawing puts 11/21/31 on the Bleachers Assy., 81–86 on the separate control
panel, and the other 53 controlled lamps on the playfield. The controlled count
is 62 =3+6+53; A–D are separate GI bulbs, not extra matrix addresses.

## Solenoid table — PDF 100 / printed 2-40

Literal wire abbreviations and order retained. NU is printed in the part column.
Power cell is genuinely blank on unused rows; it is not filled from neighbors.

| No. | Function | Type | Drive | Power | Connection | Transistor | Part / Flashlamp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Baseball Bat | High Power | Vio-Brn | Vio-Yel | J130-1 | Q82 | A-14499 |
| 02 | Magnet | High Power | Vio-Red | Vio-Yel | J130-2 | Q80 | B-20-9608 |
| 03 | Not Used | High Power | Vio-Orn | [blank] | J130-4 | Q78 | NU |
| 04 | Not Used | High Power | Vio-Yel | [blank] | J130-5 | Q76 | NU |
| 05 | Not Used | High Power | Vio-Grn | [blank] | J130-6 | Q64 | NU |
| 06 | Not Used | High Power | Vio-Blu | [blank] | J130-7 | Q66 | NU |
| 07 | Knocker | High Power | Vio-Blk | Vio-Yel | J130-8 | Q68 | AE-23-800 |
| 08 | Not Used | High Power | Vio-Gry | [blank] | J130-9 | Q70 | NU |
| 09 | Not Used | Low Power | Brn-Blk | [blank] | J127-1 | Q58 | NU |
| 10 | Not Used | Low Power | Brn-Red | [blank] | J127-3 | Q56 | NU |
| 11 | Not Used | Low Power | Brn-Orn | [blank] | J127-4 | Q54 | NU |
| 12 | Not Used | Low Power | Brn-Yel | [blank] | J127-5 | Q52 | NU |
| 13 | Not Used | Low Power | Brn-Grn | [blank] | J127-6 | Q50 | NU |
| 14 | Not Used | Low Power | Brn-Blu | [blank] | J127-7 | Q48 | NU |
| 15 | Not Used | Low Power | Brn-Vio | [blank] | J127-8 | Q46 | NU |
| 16 | Not Used | Low Power | Brn-Gry | [blank] | J127-9 | Q44 | NU |
| 17 | F.L. Left Bleacher Home Run | Flasher | Blk-Brn | Red-Wht | J125-1 | Q42 | #806 |
| 18 | F.L. Ctr. Bleacher Home Run | Flasher | Blk-Red | Red-Wht | J126-2 | Q40 | #806 |
| 19 | F.L. Rt. Bleacher Home Run | Flasher | Blk-Orn | Red-Wht | J126-3 | Q38 | #806 |
| 20 | F.L. Ramp Left | Flasher | Blk-Yel | Red-Wht | J126-4 | Q36 | #912 |
| 21 | Ramp Motor | [blank] | Blu-Grn | Vio-Orn | J126-6 | Q28 | 14-7960 |
| 22 | Fast Pitch | [blank] | Blu-Blk | Vio-Orn | J126-7 | Q30 | 14-7959 |
| 23 | Medium Pitch | [blank] | Blu-Vio | Vio-Orn | J126-8 | Q34 | 14-7959 |
| 24 | Slow Pitch | [blank] | Blu-Gry | Vio-Orn | J126-9 | Q32 | 14-7959 |
| 25 | F.L. Ramp Middle | Flasher | Blu-Brn | Red-Wht | J122-1 | Q26 | #912 |
| 26 | F.L. Ramp Right | Flasher | Blu-Red | Red-Wht | J122-2 | Q24 | #912 |
| 27 | Dispenser Motor | [blank] | Blu-Orn | Vio-Orn | J122-3 | Q22 | 14-7962 (card) |
| 28 | Dispenser Low Lamp | [blank] | Blu-Yel | Vio-Orn | J122-4 | Q20 | 20-9679 (card) |

General Illumination Circuits, same page:

| No. | Function | Type | Drive | Power | Connection | Transistor | Bulb |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | G.I. Infield Top | G.I. | Wht-Brn | Brn | J121-7 | Q18 | #555 |
| 02 | G.I. Backbox | G.I. | Wht-Org | Org | J120-8 | Q10 | #555 |
| 03 | G.I. Pitch Lamps | G.I. | Wht-Yel | Yel | J120-9 | Q14 | #555 |
| 04 | G.I. Outfield | G.I. | Wht-Grn | Grn | J121-11 | Q16 | #555 |
| 05 | G.I. Infield Bottom | G.I. | Wht-Vio | Vio | J120-11 | Q12 | #555 |

GI4's connector is J121-11; GI5's is J120-11. These are distinct headers.

## Solenoid locations — PDF 101 / printed 2-41

| Item | Part Number | Description |
| --- | --- | --- |
| 01 | A-14499 | Baseball Bat |
| 02 | B-20-9608 | Magnet |
| 03 | [blank] | Not Used |
| 04 | [blank] | Not Used |
| 05 | [blank] | Not Used |
| 06 | [blank] | Not Used |
| 07 | AE-23-800 | Knocker |
| 08 | [blank] | Not Used |
| 09 | [blank] | Not Used |
| 10 | [blank] | Not Used |
| 11 | [blank] | Not Used |
| 12 | [blank] | Not Used |
| 13 | [blank] | Not Used |
| 14 | [blank] | Not Used |
| 15 | [blank] | Not Used |
| 16 | [blank] | Not Used |
| 17 | #806 | F. L. Left Grand Home Run |
| 18 | #806 | F. L. Center Grand Home Run |
| 19 | #806 | F. L. Right Grand Home Run |
| 20 | #912 | F. L. Ramp Left |
| 21 | 14-7960 | Ramp Motor |
| 22 | 14-7959 | Fast Pitch |
| 23 | 14-7959 | Medium Pitch |
| 24 | 14-7959 | Slow Pitch |
| 25 | #912 | F. L. Ramp Middle |
| 26 | #912 | F. L. Ramp Right |
| 27 | 14-7962 | Dispenser Motor |
| 28 | 20-9679 | Dispenser Low |

It draws 17–19 across the bleachers at the rear,
20/25/26 under the home-run ramp, 21 at the center ramp, 22–24 at the pitcher,
2 below the field and 1 at the bat. Drawing positions are a physical regional
check, not measured coordinates or physical socket quantities.
