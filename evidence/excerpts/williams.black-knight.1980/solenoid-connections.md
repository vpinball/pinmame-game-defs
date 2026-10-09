# Williams Black Knight (game 500) - Table 4. Solenoid Connections

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf`, PDF page 16 (Instruction Booklet 16P-500-103). Printed page number: no number is visible on this PDF page's scan; counting from the sequence (PDF page 18 is printed page 13) it is printed page 11, and the operator's handbook second printing (`Williams_1980_Black_Knight_Operators_Handbook.pdf`, page 11) carries the same table. Heading, italic centred above the table, verbatim: `Table 4. Solenoid Connections`.

Orientation: the page is upright (no rotation). Read from the 300 dpi render `render\man300-16.png` at 1.8x zoom in four vertical tiles per column group (`crops2\sol-*.png`, `crops2\solN-*.png`); cross-checked cell by cell against the 400 dpi handbook render `render\hb400-11.png` (`crops2\hb11-*.png`).

Normalization: none to wording. Where the scan prints a comma between the two connector references (`2P11-4, 8P3-1`) it is transcribed as a comma; the scan renders some commas as full stops, which I read as commas. In `*DRIVER TRANS.` the two transistor references are printed with a small separator mark that scans as a mid-dot, slash, colon or nothing, varying from row to row (see the uncertainty list). I normalise it to `Q15 / Q7` style only in the "Driver Trans. as printed" column below; the raw reading of each is described in the notes.

Column headings, verbatim: `SOL. NO.` | `FUNCTION` | `WIRE COLOR` | `CONNECTIONS` | `*DRIVER TRANS.` | `SOLENOID PART NO.`

## Rows (22 numbered rows plus 4 flipper rows = 26 rows)

`*` before a solenoid number is printed in the SOL. NO. column exactly as shown (`*09`, `*10`, `*17`-`*22`); a bare `*` is printed on three of the four flipper rows (no number).

| SOL. NO. | FUNCTION | WIRE COLOR | CONNECTIONS | *DRIVER TRANS. (first Q / second Q) | SOLENOID PART NO. |
|---|---|---|---|---|---|
| 01 | Ball Release | GRY-BRN | 2P11-4, 8P3-1 | Q15 / Q7 | SA-23-850-DC |
| 02 | Lower Left 3-Bank Drop Target Reset | GRY-RED | 2P11-5, 8P3-2 | Q17 / Q8 | SA3-23-850-DC |
| 03 | Lower Right 3-Bank Drop Target Reset | GRY-ORN | 2P11-7, 8P3-3 | Q19 / Q9 | SA3-23-850-DC |
| 04 | Upper Left 3-Bank Drop Target Reset | GRY-YEL | 2P11-8, 8P3-4 | Q21 / Q10 | SA3-23-750-DC |
| 05 | Upper Right 3-Bank Drop Target Reset | GRY-GRN | 2P11-9, 8P3-5 | Q23 / Q11 | SA3-23-750-DC |
| 06 | Ball Ramp Thrower | GRY-BLU | 2P11-3, 8P3-6 | Q25 / Q14 | SG-23-750-DC |
| 07 | Multi-Ball Release | GRY-VIO | 2P11-2, 8P3-7 | Q27 / Q15 | SG-23-750-DC |
| 08 | Lower Eject Hole | GRY-BLK | 2P11-1, 8P3-8 | Q29 / Q16 | SG-23-750-DC |
| *09 | Right Magnet Relay | BRN-BLK | 2P9-9, 10P3-9 | Q31 / Q13 | SM-35-4000-DC |
| *10 | Left Magnet Relay | BRN-RED | 2P9-7, 10P3-10 | Q33 / Q12 | SM-35-4000-DC |
| 11 | Special Relay | BRN-ORN | 2P9-1, 10P3-11 | Q35 / Q17 | SA-24-750-DC |
| 12 | Not Used | BRN-YEL | 2P9-2, 10P3-12 | Q37 / Q18 | - (a dash; handbook: `-`) |
| 13 | Not Used | BRN-GRN | 2P9-3, 10P3-13 | Q39 / Q19 | (blank in the booklet scan; handbook prints `-`) |
| 14 | Not Used | BRN-BLU | 2P9-4, 7P1-16 | Q41 / Q20 | (blank in the booklet scan; handbook prints `-`) |
| 15 | Bell | BRN-VIO | 2P9-5, 7P1-17 | Q43 / Q21 | SM29-1000-DC |
| 16 | Coin Lockout | BRN-GRY | 2P9-6, 7P1-18, 7P2-4 | Q45 / Q22 | SM-35-4000-DC |
| *17 | Left Kicker | BLU-BRN | 2P12-7, 8P3-17 | Q2 / Q1 | SG-23-850-DC |
| *18 | Right Kicker | BLU-RED | 2P12-4, 8P3-18 | Q4 / Q5 | SG-23-850-DC |
| *19 | Jet Bumper | BLU-ORN | 2P12-3, 8P3-19 | Q6 / Q4 | SG-23-850-DC |
| *20 | Not Used | BLU-YEL | 2P12-6, 8P3-20 | Q8 / Q6 | (a faint dot only in both scans) |
| *21 | Not Used | BLU-GRN | 2P12-8, 8P3-21 | Q10 / Q2 | (blank in the booklet scan; handbook prints `-`) |
| *22 | Not Used | BLU-BLK | 2P12-9, 8P3-22 | Q12 / Q3 | (blank in both scans) |
| * | Lower Right Flipper | BLU-VIO | 7P1-8, 8P3-3 | (blank in the booklet scan; handbook prints `-`) | SFL-19-400 / 30-750-DC |
| (none, no `*`) | Upper Right Flipper | BLK-YEL | 7P1-31, 8P3-5 | `-` (printed in both) | SFL-19-400 / 30-750-DC |
| * | Lower Left Flipper | BLU-GRY | 7P1-10, 8P3-4 | (blank in the booklet scan; handbook prints `-`) | SFL-19-400 / 30 -7 50-DC |
| * | Upper Left Flipper | BLK-GRY | 7P1-30, 8P3-9 | (blank in both scans) | SFL-19-400 / 30-750-DC |

Notes on the cells:

- Sol. no. `11` is printed with the characters scanning as `I I` / `l1`; read as `11` (matches the table order 10, 11, 12).
- `*DRIVER TRANS.` is printed as two transistor references per row (`Q15 Q7`). Between them there is a faint separator mark that scans as a mid-dot, comma, colon or slash depending on the row (row 02 looks like a slash, rows 14 and 15 show only a gap). I read it as one separator of unknown glyph [uncertain: `-` or `/` that is faint in the scan]; in the table above it is written ` / `. The first reference is for the D7997 (earlier) driver board and the second for the D8341 driver board, per note 1.
- Flipper rows' `SOLENOID PART NO.` is two lines: `SFL-19-400` on the first line and an indented second line `30-750-DC` (printed `30 -7 50-DC` with odd letterspacing on the Lower Left Flipper row; I read it as `30-750-DC` with scan spacing artefact [uncertain: `30-750-DC`]). The same two-line form is in the handbook.
- The `Upper Right Flipper` row has no `*` in the SOL. NO. column and the other three flipper rows have a bare `*`. Same in the handbook.
- Row `16 Coin Lockout` CONNECTIONS has three references (`2P9-6, 7P1-18, 7P2-4`).
- Solenoid numbers 01-08 are the first group (wire colours GRY-xxx), 09-16 the second group (BRN-xxx) and 17-22 the third group (BLU-xxx), flipper rows BLU-VIO / BLK-YEL / BLU-GRY / BLK-GRY.

## *NOTES (verbatim)

```
*NOTES:
1. First reference no. for D7997 (earlier) Driver Board; 2nd is
   for D8341 Driver Board.
2. Contacts of solenoids 09 and 10 switch ground to magnets
   (Part No. 20-8991)
3. Special switch connections for solenoids 17 through 19 are as
   follows:
        17 -- ORN-BRN -- 2P13-5, 8P3-5
        18 -- ORN-RED -- 2P13-3, 8P3-6
        19 -- ORN-BLK -- 2P13-2, 8P3-7
4. Flipper button connections are as follows:
        Right -- ORN-VIO     2P12-1, 7P1-7
        Left -- ORN-GRY -- 2P12-2, 7P1-9
5. Typical wiring for solenoids and special switches:
```

Dash characters in the lists are as printed (they scan as short and long dashes of varying length): lines 17/18/19 have a dash after the solenoid number and a dash between the colour and the connections; the `Right` line has a dash after `Right` and only a gap before `2P12-1` (no dash printed there); the `Left` line has a dash after `Left` and a dash after the colour.

### Note 5 figure (typical wiring for solenoids and special switches)

Two small schematics to the right of the notes:

1. Upper: a horizontal line from the left, a solenoid coil symbol (four loops) with a diode in parallel across the coil. The diode is drawn below the coil, its triangle points to the right and its bar (cathode) is at the right end, which joins the right-hand wire. Right-hand line label: `RED (B+)`.
2. Lower: a horizontal line from the left, a switch symbol (blade drawn rising to the right, open: the blade tip is above and clear of the right terminal circle) with a resistor in series with a capacitor wired across the switch contacts (resistor on the left, capacitor on the right, `+` mark printed under the capacitor's right-hand plate area, below the resistor/capacitor junction). Right-hand line label: `BLK (GRD)`.

## Differences between the booklet scan and the handbook printing

- Wording, wire colours, connections, transistors, part numbers and the notes agree everywhere.
- The handbook (400 dpi) prints a `-` in the `SOLENOID PART NO.` column of rows 12, 13, 14 and 21 and in the `*DRIVER TRANS.` column of the Lower Right, Upper Right and Lower Left flipper rows; the 300 dpi booklet scan shows these dashes only for row 12 and the Upper Right Flipper row, the others scan as blank. I treat the dashes as printed (faded in the booklet scan): they mean "no entry".

## Observations (internal inconsistencies)

- Transistor numbers recur between rows, as printed: Q2 (row 17 first, row 21 second), Q4 (row 18 first, row 19 second), Q6 (row 19 first, row 20 second), Q8 (row 02 second, row 20 first), Q10 (row 04 second, row 21 first), Q12 (row 10 second, row 22 first), Q17 (row 02 first, row 11 second). Since note 1 says the two references belong to different driver boards, this is reuse of numbers between the two boards' numberings, not necessarily a misprint; flagged only for completeness.
- Sol. 19 `Jet Bumper`: Table 4 lists it as `*19` with special switch connection `ORN-BLK` in note 3.
- Sol. nos. 17-19 are marked `*` (special switch, note 3); 09 and 10 are marked `*` (magnet contacts, note 2); 20, 21, 22 are marked `*` even though `Not Used`.
- Solenoid 08 is `Lower Eject Hole`, 07 `Multi-Ball Release`: the same names as in the Figure 2 chart (page 15); function text agrees (see `solenoid-locations.md`).
- Sol. 11 `Special Relay`; the Power Wiring diagram carries the K1 SPECIAL RELAY (see `power-wiring.md`).
