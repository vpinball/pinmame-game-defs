# Haunted House: switch matrix and controlled outputs

Original: D. Gottlieb & Co., Haunted House game 669 instruction manual, SHA-256 `168a1bc2e2198b03154835d45471eb5b3910f1619930c5c3fd48f9b86ad8c21f`. PDF pages 41–43, printed 37–39, drawings E-21596 and E-21597.

Method: The independent transcriber transcribed the native scans; primary curator independently visually checked every retained cell against `sol-visual/pdf-041.png`, `pdf-042.png` and `pdf-043.png`. Names, leading zeroes, wire order and printed part numbers are retained. Line wrapping is normalized. These are schematic transcriptions: tabular columns organize drawn branches; repeated common rails are transcriber repetitions, not separately printed cells. A dash records no drawn branch or missing printed designation, never an invented ‘not used’ label. The partly illegible handwriting at SW45 is not used as evidence.

## Playfields switch matrix, PDF 41 / printed 37

Strobe rails, from A1 CONTROL BOARD: A1J6 pins 1–7 correspond respectively to STROBE 0–6, wires `400`, `411`, `422`, `433`, `444`, `455`, `466`. The lower playfield branch passes A9P2/A9J2 pins 1–7 respectively. The upstairs branch passes A9P5/A9J5 pins 1–5 for strobes 0–4. The page states `2. STROBE 7 NOT USED.`

Returns to A1 CONTROL BOARD, A1J6 pins 10–17: RETURN 0 `600`, 1 `611`, 2 `622`, 3 `633`, 4 `644`, 5 `655`, 6 `666`, 7 `677`. The lower return 0 and 1 pass A9P2/A9J2 pins 8 and 9. Upstairs return 2 passes A9P5/A9J5 pin 6; return 3 passes A9P6/A9J6 pin 3. Upstairs #1–#4 TARGET branches pass A9P6/A9J6 pins 4, 5, 6, 7 respectively; SW.43 branch passes A9J5/A9P5 pin 7. In the table the row/column number is the printed SW. label, with the row's common A1J6 strobe pin and column's common A1J6 return pin given above. `**` is printed by the four target diodes.

| SW. | location | printed switch label | branch wire | branch pin if printed |
|---|---|---|---|---|
|00|lower|#1 DROP TARGET|700|—|
|01|lower|POP BUMPER|500|—|
|02|upstairs|#1 DROP TARGET|100|—|
|03|upstairs|** #1 TARGET|122|A9P6/A9J6-4|
|04|main|LEFT RETURN ROLLOVER|333|—|
|05|main|#3 TARGET|344|—|
|06|main|#1 TROUGH|277|—|
|07|—|—|—|—|
|10|lower|#2 DROP TARGET|711|—|
|11|lower|KICKING TARGET|511|—|
|12|upstairs|#2 DROP TARGET|111|—|
|13|upstairs|** #2 TARGET|133|A9P6/A9J6-5|
|14|main|#1 KICKING TARGET|744|—|
|15|main|#4 TARGET|766|—|
|16|main|#2 TROUGH|288|—|
|17|—|—|—|—|
|20|lower|#3 DROP TARGET|722|—|
|21|lower|OUTSIDE ROLLOVER|522|—|
|22|upstairs|#3 DROP TARGET|122|—|
|23|upstairs|** #3 TARGET|166|A9P6/A9J6-6|
|24|main|#2 KICKING TARGET|755|—|
|25|main|#5 TOP KICKING TARGET|777|—|
|26|main|ROLLDOWN TARGET TROUGH|322|—|
|27|—|—|—|—|
|30|lower|#4 DROP TARGET|733|—|
|31|lower|UP KICKER|533|—|
|32|upstairs|#4 DROP TARGET|133|—|
|33|upstairs|** #4 TARGET|177|A9P6/A9J6-7|
|34|main|LEFT OUTSIDE ROLLOVER|011|—|
|35|main|ROLLUNDER|022|—|
|36|main|TRAP DOOR TROUGH|033|—|
|37|—|—|—|—|
|40|lower|#5 DROP TARGET|744|—|
|41|lower|HOLE|544|—|
|42|upstairs|10 POINT|144|—|
|43|upstairs|POP BUMPER|155|A9J5/A9P5-7|
|44|main|POP BUMPERS (2)|044|—|
|45|main|UP KICKER|055|—|
|46|main|TOP CENTER HOLE|066|—|
|47|—|—|—|—|
|50|lower|RIGHT TARGET|755|—|
|51|lower|10 POINT AND KICKING RUBBERS|566|—|
|52|—|—|—|—|
|53|—|—|—|—|
|54|main|RIGHT OUTSIDE ROLLOVER|100|—|
|55|main|RIGHT BOTTOM TARGET|111|—|
|56|—|—|—|—|
|57|main/cabinet tilt circuit|TILT|088|—|
|60|lower|LEFT TARGET|766|—|
|61|—|—|—|—|
|62|—|—|—|—|
|63|—|—|—|—|
|64|main|ROUNDABOUT|300|—|
|65|main|RIGHT SIDE KICKER|844|—|
|66|main|10 POINT AND KICKING RUBBER|355|—|
|67|main|OUTHOLE|155|—|

Notes exactly as legible: `1. ALL DIODES ARE 1N270.` `2. STROBE 7 NOT USED.` Legend by diode: `** DIODES MOUNTED ON MAIN PLAYFIELD.` Dashed regions say `LOCATED ON LOWER PLAYFIELD` and `LOCATED ON UPSTAIRS PLAYFIELD`.

Handwriting: SW.31 has `LWR.` above UP KICKER. SW.45 has a struck-through handwritten word above UP KICKER and another handwritten word beneath; they appear to say `upper` and `main` respectively but neither is reliably legible; preserve image for exact strokes and do not treat the apparent words as settled. Header also bears a handwritten X-like mark. The CPU matrix diagram draws SW.36 open; the separately drawn `TRAP DOOR SW.` in the coil circuit is a different contact and is drawn normally closed.

## Printed 38 controlled-solenoid circuits

Table is transcribed from the schematic; each A3 connector, L label, printed wire and solenoid number is literal, `—` means no corresponding printed label. Pairs A9P/A9J refer to matching numbered plug/socket pins. Supply and transistor detail follows.

| A3 output | A9 connector/pin | wire(s) | printed output/label | location |
|---|---|---|---|---|
| A3J4-6 | A9P4/A9J4-7 | 211 | SOLENOID #5, 4 BANK | UPSTAIRS PLAYFIELD |
| A3J4-8 | — | 244 | SOLENOID #9, OUTHOLE | main |
| A3J4-7 | — | 266 | SOLENOID #1, TOP HOLE | main |
| A3J4-13 | — | 200 | SOLENOID #2, UP KICKER | main |
| A3J3-23 | — | 133 (L15); 477 after Q1 | RIGHT SIDE KICKER | main |
| A3J3-13 | — | 144 (L16); 266 after Q2 | TRAP DOOR | main |
| A3J3-14 | — | 155 (L17) | U RELAY | main/unspecified |
| A3J3-A bar | — | 288 | GAME OVER RELAY | unspecified |
| A3J3-B bar | — | 277 | TILT RELAY | unspecified |
| A3J4-12 | A9P1/A9J1-3 | 233 | SOLENOID #6, HOLE | LOWER PLAYFIELD |
| A3J3-25 | A9P1/A9J1-1 | 100 (L12) | K RELAY | LOWER PLAYFIELD |
| A3J3-24 | A9P1/A9J1-2 | 111 (L13); 266 after Q3 | 5 BANK | LOWER PLAYFIELD |

Upper 4 BANK supply: A9P4/A9J4-8 `255`, through F15 `2 AMP SLO-BLO`. Lower HOLE supply A9P1/A9J1-5 `255`. Lower connector pin 4 `244` is `SWITCHED +24V DC (FUSED)`; pin 15 `855` is `SWITCHED +24V DC`. Q1, Q2, Q3 are `2N5875 OR 2N5879`; R1, R2, R3 `4.7K 5% 1/4W`. F14 `2.5 AMP SLO-BLO`, wire `244`. TRAP DOOR SW. is shown with the normally closed symbol in the trap-door coil branch. Q1/Q2/Q3 transistor base inputs are the printed L15/L16/L13 lines, respectively; do not confuse these lamp-driver labels with bulbs.

## Controlled illumination, PDF 42–43 / printed 38–39

Controlled lamp branches are on printed 38; their common return continues across the page seam into printed 39, labeled `077` in the visible upstairs/common region. Exact other common returns should be traced on the joined source, rather than copied into every row. `—` means no A9 connector printed for that lamp, not a blank printed table cell. Text cut at the page seam is completed only when visibly continued in printed 39; no missing lettering has been invented.

| A3 output | A9P/A9J pin | wire | label | printed description | dashed region |
|---|---|---|---|---|---|
| A3J3-C bar | — | 588 | L3 | SHOOT AGAIN | — |
| A3J3-20 | A9P4/A9J4-1 | 311 | L21 | DOUBLE SCORING | UPSTAIRS PLAYFIELD |
| A3J3-4 | A9P4/A9J4-2 | 744 | L40 | #2 TARGET | UPSTAIRS PLAYFIELD |
| A3J3-3 | A9P4/A9J4-3 | 755 | L41 | #3 TARGET | UPSTAIRS PLAYFIELD |
| A3J3-T | A9P4/A9J4-4 | 766 | L42 | #4 TARGET | UPSTAIRS PLAYFIELD |
| A3J3-D | A9P4/A9J4-5 | 800 | L44 | SPECIAL | UPSTAIRS PLAYFIELD |
| A3J3-16 | — | 166 | L18 | DOUBLE BONUS UPSTAIRS PLAYFIELD | main diagram |
| A3J3-15 | — | 177 | L19 | DOUBLE BONUS MAIN PLAYFIELD | main diagram |
| A3J3-21 | — | 300 | L20 | DOUBLE BONUS LOWER PLAYFIELD | main diagram |
| A3J3-18 | — | 322 | L22 | DOUBLE SCORING | main diagram |
| A3J3-11 | — | 377 | L27 | TOP LEFT HOLE | main diagram |
| A3J3-Y | — | 500 | L28 | TOP CENTER HOLE | main diagram |
| A3J3-X | — | 511 | L29 | TOP RIGHT HOLE | main diagram |
| A3J3-V | — | 522 | L30 | #1 KICKING TARGET | main diagram |
| A3J3-W | — | 533 | L31 | #2 KICKING TARGET | main diagram |
| A3J3-5 | — | 544 | L32 | #3 TARGET | main diagram |
| A3J3-6 | — | 555 | L33 | #4 TARGET | main diagram |
| A3J3-K | — | 566 | L34 | #5 TOP KICKING TARGET | main diagram |
| A3J3-7 | — | 577 | L35 | 1X | main diagram |
| A3J3-P | — | 822 | L46 | LEFT OUTSIDE ROLLOVER | main diagram |
| A3J3-M | — | 833 | L47 | ROUNDABOUT | main diagram |
| A3J3-N | — | 877 | L51 | ROLLDOWN TARGET | main diagram |
| A3J2-10 | — | 544 | L8 | EXTRA BALL | main diagram |
| A3J4-1 | — | 700 | L36 | 2X | main diagram |
| A3J4-2 | — | 711 | L37 | 3X | main diagram |
| A3J4-4 | — | 722 | L38 | 4X | main diagram |
| A3J4-3 | — | 733 | L39 | 5X | main diagram |
| A3J3-19 | A9P3/A9J3-1 | 333 | L23 | DOUBLE SCORING | LOWER PLAYFIELD |
| A3J3-9 | A9P3/A9J3-2 | 344 | L24 | #1 SEQUENCE | LOWER PLAYFIELD |
| A3J3-10 | A9P3/A9J3-3 | 355 | L25 | #2 SEQUENCE & LEFT TARGET | LOWER PLAYFIELD |
| A3J3-12 | A9P3/A9J3-4 | 366 | L26 | #3 SEQUENCE & RIGHT TARGET | LOWER PLAYFIELD |
| A3J3-F | A9P3/A9J3-5 | 811 | L45 | SPECIAL | LOWER PLAYFIELD |

Also drawn: A9P4/A9J4-6 and A9P3/A9J3-6 are common-side return pins; neither has a numeric wire code printed at that connector. Notes (printed 38): `1. ALL DIODES ARE 1N4004.` `2. LAMPS L32 THRU L43 ARE DRIVEN BY MPS-A13'S; ALL OTHER LAMPS ARE DRIVEN BY MPS-U45'S.` `3. UNLESS OTHERWISE SPECIFIED; ALL LAMPS ARE #44. GROUND WIRE COLOR IS 54, 18GA.` `4. [XXX in a wire box] INDICATES WIRE COLOR.`

## COILS USED, printed 38

The original is two adjacent part-number/description pairs; each row below preserves both halves. No blanks are visible in this table.

| PART NO. | DESCRIPTION | PART NO. | DESCRIPTION |
|---|---|---|---|
| A-18102 | 4 BANK (UPSTAIRS) | A-16570 | HOLE (LOWER) |
| A-5195 | OUTHOLE | A-20558 | K RELAY (LOWER) |
| A-16570 | TOP HOLE | A-17891 | 5 BANK (LOWER) |
| A-5194 | KICKING TARGET (LOWER) | A-21741 | UP KICKER (LOWER) |
| A-5194 | UP KICKER | A-5194 | KICKING TARGETS (2) |
| A-5195 | RIGHT SIDE KICKER | A-1496 | KICKING RUBBER (LOWER) |
| A-17875 | TRAP DOOR | A-17875 | FLIPPERS (8) |
| A-16890 | U RELAY | A-1496 | TOP KICKING TARGET |
| A-16890 | GAME OVER RELAY | A-5194 | KICKING RUBBER |
| A-16890 | TILT RELAY | A-1496 | POP BUMPERS (4) |
