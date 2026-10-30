Source: `Stern_1980_Galaxy_Manual.pdf` (IPDB machine 980, "English Manual (may be incomplete, with paginated schematics shown in halves)", 35 pages, each a 300 dpi grayscale scan with no text layer), PDF page 31, drawing number `12B-431-S-114`, `LAMP DRIVER SCHEMATIC` `FOR GALAXY` (Stern Electronics Inc., `DATE 10-11-79`). The page is upright. The three connector blocks `J1`, `J2` and `J3` (drawn as dashed boxes between the SCR output lines on the left and the typed lamp list on the right) were read from crops at 600 dpi, and the doubtful rows at 1200 dpi, no rotation.

Each pin is drawn as an arrow with a hand-written pin number and the label of the SCR that drives it; a small filled triangle before a label (marked here with `T`) is the sheet's mark for an MCR106-1 part, the others have no triangle. Rows are in printed order, top to bottom. A block label `J1`, `J2` or `J3` is hand-written above each box and again to its right. Some SCRs appear on more than one pin (see the end).

### J1

| Pin | Triangle | SCR label | Notes |
| ---: | --- | --- | --- |
| 18 | | Q14 | |
| 19 | | Q12 | `Q12` is written with a loop that reads `Q|Z` |
| 17 | | Q13 | |
| 23 | T | Q8 | the `2` of `23` is large |
| 14 | T | Q9 | |
| 15 | T | Q10 | |
| 16 | | Q11 | |
| 28 | | Q4 | |
| 24 | T | Q1 | |
| 25 | T | Q2 | |
| 26 | T | Q3 | |
| 27 | | Q7 | |
| 1 | | Q29 | |
| 9 | | Q27 | |
| 8 | | Q28 | |
| 3 | T | Q35 | |
| 2 | T | Q34 | |
| 10 | T | Q22 | |
| 7 | | Q26 | |
| 6 | | Q25 | |
| `3`, `5` or `8` | T | Q24 | ambiguous, see below |
| 11 | T | Q17 | |
| 13 or 15 | | Q20 | ambiguous, see below |
| 14 | T | Q23 | duplicate of the pin on the `Q9` row, see below |
| 12 | T | Q21 | |

Ambiguous or duplicated rows of J1, in printed order after `Q25`:

- `Q24`: the pin number is a filled, blotted figure that can be read as `3`, `5` or `8`. Pin 3 is already printed on the `Q35` row. Not settled from the drawing alone.
- `Q20`: the pin number is `1` followed by a blotted digit that reads `3` or `5` (written like `13` with the second figure open on the left). Read as `13`, alternative `15`.
- `Q23`: the pin reads `14` (the `4` is written over a blob). The `Q9` row above also prints `14`, so pin 14 appears twice in this block. Not settled.

J1 pins 4, 5, 20, 21 and 22 carry no row in this block.

### J2

| Pin | Triangle | SCR label | Notes |
| ---: | --- | --- | --- |
| 21 | T | Q3 | |
| 13 | | Q7 | |
| 22 | T | Q16 | |
| 16 | T | Q5 | |
| 14 | | Q6 | |
| `8`, `3` or `6` | T | Q23 | the pin is a heavy blotted figure; read as `8`, alternatives `3` or `6` |
| 12 | | Q21 | |
| 23 | T | Q15 | the `3` is overwritten |
| 20 | | Q18 | |
| 15 | | Q19 | |
| 11 | T | Q33 | |
| 6 | | Q30 | |
| 2 | | Q31 | |
| 9 | T | Q40 | |
| 4 | | Q39 | |
| 5 | | Q52 | |
| 10 | T | Q47 | |
| 7 | | Q43 | |
| 1 | | Q45 | |
| `3`, `5` or `9` | | Q53 | the pin is a heavy blotted figure; read as `3`, alternatives `5` or `9` |

### J3

| Pin | Triangle | SCR label | Notes |
| ---: | --- | --- | --- |
| 26 | | Q36 | the label is overprinted (the digits run together); read as `Q36` |
| 29 | | Q38 | the `38` is overprinted and reads `Q38` |
| 19 or 15 | | Q44 | the second figure is open and blotted; read as `19`, alternative `15` |
| 17 | T | Q49 | |
| 16 | T | Q48 | |
| 23 | | Q37 | |
| 27 | | Q32 | |
| 21 | T | Q42 | |
| 20 | T | Q41 | |
| 22 | T | Q40 | |
| 24 | | Q39 | the `9` is overprinted |
| 1 | | Q57 | |
| 12 | | Q50 | |
| 15 | | Q51 | |
| 11 | T | Q54 | |
| 9 | T | Q55 | |
| 3 | | Q60 | |
| 4 | | Q59 | |
| 2 | | Q58 | |
| 10 | T | Q56 | |
| 18 | | Q46 | |
| 13 | | Q52 | |
| 14 | | Q53 | |

SCRs printed on more than one pin (blocks and pins as in the tables above): `Q3` (J1 26, J2 21), `Q7` (J1 27, J2 13), `Q21` (J1 12, J2 12), `Q23` (J1 14, J2 `8`), `Q39` (J2 4, J3 24), `Q40` (J2 9, J3 22), `Q52` (J2 5, J3 13), `Q53` (J2 `3`/`5`/`9`, J3 14).

J3 pin number 15 is printed on the `Q51` row; if the `Q44` row is `15`, that pin would also appear twice in J3.
