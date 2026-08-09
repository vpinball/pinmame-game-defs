# Playboy 35th Anniversary coil, relay, flipper, and special-solenoid transcription

Source: PDF pages 29-30, printed pages 26-27. Both pages were decided from 400 dpi renders; the PDF text layer and OCR were locator/second-reading aids only.

## CPU-controlled coil/flash schematic

| Public / printed side | Printed device | Printed type or quantity |
| --- | --- | --- |
| 1 / SIDE L 01 | GROTTO 1 | NO.906 (1) |
| 25 / SIDE R 01 | OUTHOLE | 23-840 |
| 2 / SIDE L 02 | GROTTO 2 | NO.906 (2) |
| 26 / SIDE R 02 | TROUGH | 23-840 |
| 3 / SIDE L 03 | SPINNER 1 | NO.89 (3), NO.906 (1) |
| 27 / SIDE R 03 | VERTICAL UP KICKER | 23-800 |
| 4 / SIDE L 04 | SPINNER 2 | NO.89 (3), NO.906 (1) |
| 28 / SIDE R 04 | CHAMPAGNE KICKER | 22-600 |
| 5 / SIDE L 05 | SPINNER 3 | NO.89 (3), NO.906 (1) |
| 29 / SIDE R 05 | DROP TARGET RESET | `23-1200` as printed on the schematic |
| 6 / SIDE L 06 | MULTI BALL | NO.906 (2) |
| 30 / SIDE R 06 | GROTTO KICKING | 24-900 |
| 7 / SIDE L 07 | RAMP LEFT | NO.906 (1) |
| 31 / SIDE R 07 | no fitted branch printed | — |
| 8 / SIDE L 08 | no feature label printed | NO.89 (2), NO.906 (2) |
| 32 / SIDE R 08 | KNOCKER | 23-800 |
| 9 | PLAYBOY/FLASH | NO.89 (2), NO.906 (2) |
| 10 | LEFT/RIGHT COIL RELAY | K1 |
| 11 | GENERAL ILLUM. RELAY | K1 |
| 12 | INSERT 2 DROP FLASH | NO.89 (4) |
| 13 | RAMP RIGHT | NO.89 (1), NO.906 (4) |
| 14 | MANSION FLASH | NO.89 (3), NO.906 (1) |
| 15 | no feature label printed | NO.89 (2), NO.906 (2) |
| 16 | LASER KICKER | 23-800 |

## Printed coil/flash location drawing

Printed page 26 contains a playfield plan plus a separate `Backbox Flash lamps` inset. A 600-dpi render resolves `1L`, two `2L` callouts, `3L`, `4L`, `5L`, `6L`, `7L`, `8L`, `9`, `13`, `14`, `15`, `16`, `1R`-`4R`, two `5R` callouts, `6R`, and `SP1`-`SP5`; no `7R` or `8R` callout is visible. These are group/location callouts, not a promise that each circle represents one bulb.

The inset uses circled output numbers to identify backbox flash bulbs. The retained scan clearly supports these counts; uncertain small glyphs are not assigned:

| Public output | Clearly legible backbox symbols | Schematic total bulbs |
| --- | ---: | ---: |
| 3 | 3 | 4 |
| 4 | 3 | 4 |
| 8 | 2 | 4 |
| 9 | 2 | 4 |
| 12 | 4 | 4 |
| 14 | at least 3 | 4 |
| 15 | at least 1 | 4 |

Three further glyphs resemble `5`/`6`, and two resemble `13`/`16`, but the retained raster is not clear enough to assign them. Output 12's four clear backbox symbols equal its four-bulb schematic total. The plan is sufficient for physical-plane classification and broad feature location, but its grouped callouts and lack of a registered coordinate frame are insufficient for normalized socket centers.

The adjacent coil part-number chart separately prints:

| Quantity | Coil type | Assembly part number |
| --- | --- | --- |
| 8 | 23-800 | 090-5001-00 |
| 1 | 24-900 | 090-5002-00 |
| 2 | 23-840 | 090-5005-00 |
| 1 | 12-1200 | 090-5008-00 |
| 1 | 22-600 | 090-5017-00 |
| 2 | 22-800 | 090-5020-21 |

It prints one `12-1200` coil and no `23-1200` coil. That self-disagreement is preserved rather than corrected.

## Switch-triggered solenoids

| Printed special address | Printed description | Control / trigger | Transistor / coil |
| --- | --- | --- | --- |
| SP1 | Center Pop Bumper | BLU-ORN / ORN-BLK | Q8 / 23-800 |
| SP2 | Right Pop Bumper | BLU-RED / ORN-RED | Q9 / 23-800 |
| SP3 | Left Slingshot | BLU-YEL / ORN-YEL | Q10 / 23-800 |
| SP4 | Left Pop Bumper | BLU-BRN / ORN-BRN | Q11 / 23-800 |
| SP5 | Right Slingshot | BLU-GRN / ORN-GRN | Q12 / 23-800 |
| SP6 | NOT USED | — | Q13 / — |

## Flippers

The printed flipper table lists one left and one right dual-winding assembly, each with coil type `22-800`, and prints separate CPU, PPB, and power-line wires for the two sides.
