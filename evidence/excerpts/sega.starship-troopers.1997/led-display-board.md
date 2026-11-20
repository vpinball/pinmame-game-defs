# Starship Troopers — 4X 7-Segment Display Board

Read from `Sega_1997_Starship_Troopers_Manual.pdf` (IPDB 4341), PDF page 130, printed Section 5, Chapter 4 page 116,
"4X 7-Segment Display Board Schematic" and "4X 7-Segment Display Board Component Layout & Parts", from a 400 dpi render
of the scan.

## CN1 (15X1 header)

| CN1 pin | Wire | Signal as printed |
| --- | --- | --- |
| 1 | N/C | |
| 2 | KEY | |
| 3 | N/C | |
| 15 | RED/VIO | Lamp Row 7 (Q39) J12-P8 |
| 12 | RED/GRY | Lamp Row 8 (Q40) J12-P9 |
| 14 | RED/WHT | Lamp Row 9 (Q41) J12-P10 |
| 13 | RED | Lamp Row 10 (Q42) J12-P11 |
| 8 | YEL/BRN | Lamp Col 1 (U17) J13-P9 |
| 9 | YEL/RED | Lamp Col 2 (U16) J13-P8 |
| 4 | YEL/ORG | Lamp Col 3 (U15) J13-P7 |
| 10 | YEL/BLK | Lamp Col 4 (U14) J13-P6 |
| 11 | YEL/GRN | Lamp Col 5 (U13) J13-P5 |
| 6 | YEL/BLU | Lamp Col 6 (U12) J13-P4 |
| 7 | YEL/VIO | Lamp Col 7 (U11) J13-P3 |
| 5 | BLK (GND) | |

The pins are listed in the order the schematic draws them. Each column line passes through a 1N914 diode (D1-D7) and a
220 Ω 1/4W resistor (R1-R7) to the segment anodes; R8-R14 are 120 Ω 1/4W. Each lamp row goes to one display's
cathode.

## Displays

| Display | Row line | Cathode | Seg-A | Seg-B | Seg-C | Seg-D | Seg-E | Seg-F | Seg-G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DISP1 | Lamp Row 7 | Pin-14 | Pin-1 (Lamp 49) | Pin-13 (Lamp 50) | Pin-10 (Lamp 51) | Pin-8 (Lamp 52) | Pin-7 (Lamp 53) | Pin-2 (Lamp 54) | Pin-11 (Lamp 55) |
| DISP2 | Lamp Row 8 | Pin-14 | Pin-1 (Lamp 57) | Pin-13 (Lamp 58) | Pin-10 (Lamp 59) | Pin-8 (Lamp 60) | Pin-7 (Lamp 61) | Pin-2 (Lamp 62) | Pin-11 (Lamp 63) |
| DISP3 | Lamp Row 9 | Pin-14 | Pin-1 (Lamp 65) | Pin-13 (Lamp 66) | Pin-10 (Lamp 67) | Pin-8 (Lamp 68) | Pin-7 (Lamp 69) | Pin-2 (Lamp 70) | Pin-11 (Lamp 71) |
| DISP4 | Lamp Row 10 | Pin-14 | Pin-1 (Lamp 73) | Pin-13 (Lamp 74) | Pin-10 (Lamp 75) | Pin-8 (Lamp 76) | Pin-7 (Lamp 77) | Pin-2 (Lamp 78) | Pin-11 (Lamp 79) |

Each display is captioned "7-SEGMENT DISPLAY ( MTN4126-CHR )". Beside each, a 2×2 position key shades one quarter:
DISP1 top left, DISP2 top right, DISP3 bottom left, DISP4 bottom right.

## Parts list

| Item | Qty | Part number | Ref-designator | Description |
| --- | --- | --- | --- | --- |
| — | 1 | 520-5166-00 | 4X 7-Segment Display Bd. | Complete PCB Assembly |
| 1 | 7 | 121-5014-00 | R1>R7 | 220 Ω 1/4W Res. |
| 2 | 7 | 121-5030-00 | R8>R14 | 120 Ω 1/4W Res. |
| 3 | 7 | 112-5014-00 | D1>D7 | 1N914, Diode |
| 4 | 4 | 165-5040-00 | DISP1, DISP2, DISP3, DISP4 | 1" 7-Seg. Red Disp (MTN4126-CHR) |
| 5 | 4 | 045-5160-24 | DISP1, DISP2, DISP3, DISP4 | 24-Pin Socket .6"w X .3"h (SPC SP-242T) |
| 6 | 1 | 045-5161-15 | CN1 | 15X1 Reverse-Mount .156" Hdr. |

Solder-side note: "Trace shown bold from CN1 Pin-12 through CN1 Pin-15 to DISP1 through DISP4 Socket Pin-14, Cathode,
respectively." Read literally, "respectively" pairs pin 12 with DISP1, while the schematic's pin list and the segment
lamp numbers put Lamp Row 7 (pin 15) on DISP1; the lamp numbers are what the controller sees.

DR. 5 (PDF page 7) adds, under "TYPICAL 7-SEGMENT ADDRESS": "NOTE: This Game features a 4-Digit 7-Segment Display
(located over the Flippers). Each segment is wired into the Lamp Matrix Grid (see previous page)."
