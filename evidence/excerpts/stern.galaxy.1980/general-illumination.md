Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF page 34, the right half of drawing `12B-16B-6`, title block `STERN ELECTRONICS INC.`, `1725 DIVERSEY BLVD. CHICAGO 60614`, `TRANSFORMER SCHEMATIC`, `FOR GENERAL USE`, `DATE 8-24-79`. The page is upright. Read from a 100 dpi render of the whole page.

The connector list at the right of the sheet, verbatim, in printed order (pin, wire colour, function); a pin with no text is printed bare:

`J2(CABINET)`

| Pin | Wire | Function |
| ---: | --- | --- |
| 6 | -Y- | A.C. POWER |
| 7 | -W- | A.C. RETURN |
| 2 | -G- | COIN LOCK-OUT & KNOCKER BUS |
| 1 | Y-B | GEN. ILL. BUS |
| 5 | G-R | GEN. ILL. RETURN |
| 9 | (blank) | (blank) |
| 10 | -G- | A.C. POWER GRD. |
| 3 | (blank) | (blank) |
| 4 | (blank) | (blank) |
| 8 | (blank) | KEY |

`J1 (PLAYFIELD)`

| Pin | Wire | Function |
| ---: | --- | --- |
| 5 | (blank) | (blank) |
| 8 | -W- | GEN. ILL. BUS |
| 6 | BLU-W | SOLENOID BUS |
| 4 | (blank) | KEY |
| 7 | -BLU- | FEATURE LAMP BUS |
| 1 | -R- | (blank) |
| 2 | (blank) | (blank) |
| 3 | (blank) | (blank) |

`J3 (BACK-BOX)`

| Pin | Wire | Function |
| ---: | --- | --- |
| 9 | -Y- | FLIPPER ENABLE RE. BUS |
| 12 | GREY | ZERO CROSSING INPUT |
| 13 | (blank) | (blank) |
| 10 | -O- | GEN. ILL. BUS |
| 11 | -R- | GEN. ILL. BUS |
| 6 | -BLU- | FEATURE LAMP BUS |
| 8 | -O- | 11.9 V.D.C. BUS |
| 5 | GREY | TO REG. 185VDC INPUT |
| 1 | -G- | GEN. ILL. RETURN |
| 2 | -W- | GEN. ILL. RETURN |
| 3 | R-B | LDA BOARD RETURN (braced over 3, 4 and 14) |
| 4 | W-R | (braced, see 3) |
| 14 | W-B | (braced, see 3) |
| 15 | W-BLU | SDU BOARD RETURN (REG. SECTION) (braced over 15 and 16) |
| 16 | B-BLU | (braced, see 15) |
| 17 | W-BRN | +5 FILTER RETURN |
| 18 | -W- | 175 V. FILTER RETURN |
| 19 | R-Y | SDU BOARD RETURN (braced over 19 and 20), with `(SOL.DR.SECTION)` below |
| 20 | W-O | (braced, see 19) |
| 7 | (blank) | KEY |

The general-illumination buses run from the transformer windings straight to these pins; the sheet labels supply lines `7.3 VAC`, `5.4 VDC`, `11.9 VDC` and `43 VDC`. No relay, relay contact or driver is drawn in any `GEN. ILL.` line on this sheet.
