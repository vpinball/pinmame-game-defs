# Black Hole — Playfields "controlled" solenoids and illumination (printed page 44)

Source: the Scribd copy of the Gottlieb *Black Hole Instruction Manual* (document 223467608), viewer page 46 (printed
page 44), headed "PLAYFIELDS "CONTROLLED" SOLENOIDS AND ILLUMINATION". The sheet is a fold-out scanned at letter width,
so its right edge is cut off: the lamp descriptions end mid-word at the margin (completed in brackets below only where
the same text is printed whole on pages 40 and 42) and the title block is lost. Read from the 904 x 1160 page image,
enlarged in four crops. Wire colours are the boxed three-digit codes ("[XXX] INDICATES WIRE COLOR").

## Solenoid drivers and fuses (left half, upper playfield)

| Driver output | Wire | Through | Load | Fuse |
| --- | --- | --- | --- | --- |
| A3J4-8 "SOLENOID #9" | 244 | | OUTHOLE | F15 1 AMP SLO-BLO, wire 211 |
| A3J4-7 "SOLENOID #1" | 266 | A9J2/A9P2 5, return A9P2/A9J2 7 | 4 POS. BANK | F14 2 AMP SLO-BLO, wire 788 |
| A3J4-13 "SOLENOID #2" | 200 | A9J3/A9P3 6, return A9P3/A9J3 9 | 5 POS. BANK | F14 2 AMP SLO-BLO |
| A10P4-1 "FROM LIGHTBOX A10J4" | 022 | | LIGHTBOX TILT LAMP (6.3V AC) | |
| A3J3-A (pin printed with an overbar) | 288 | | GAME OVER RELAY | |
| A3J3-B (pin printed with an overbar) | 277 | | TILT RELAY | |
| A3J3-23, remote transistor Q2 "(L15)" 2N5875 | 133 | collector wire 188 | BALL GATE (CARDHOLDER) | F16 1 AMP SLO-BLO, wire 233 |
| A3J3-24, remote transistor Q1 "(L13)" 2N5875 | 111 | collector wire 200 | HOLE KICKER | |
| A3J3-13 "(L16)" | 144 | | U RELAY | |
| A3J3-16 "(L18)" | 166 | | WIREFORM BALL GATE | |

## Solenoid drivers and fuses (dashed block "LOCATED ON LOWER PLAYFIELD")

| Driver output | Wire | Through | Load | Fuse |
| --- | --- | --- | --- | --- |
| A3J4-6 "SOLENOID #5" | 211 | A9J8/A9P8 7 | 4 POS. BANK | F18 2 AMP SLO-BLO, wire 488 |
| A3J4-12 "SOLENOID #6" | 233 | A9J8/A9P8 8 | 3 POS. BANK | F20 1 AMP SLO-BLO, wire 377 |
| A10P4-6 "FROM LIGHTBOX A10J4", remote transistor Q3 "(L8)" 2N5875 | 544 | A9J8/A9P8 4 | BALL GATE | F19 1 AMP SLO-BLO, wire 588 |
| A3J3-25, remote transistor Q4 "(L12)" 2N5875 | 100 | A9J8/A9P8 1 | HOLE KICKER | |
| A3J3-22, remote transistor Q5 "(L14)" 2N5875 | 122 | A9J8/A9P8 2, collector wire 255 | BALL LIFT KICKER | F17 6 1/4 AMP SLO-BLO, wire 344 |
| A3J3-14 "(L17)" | 155 | A9J8/A9P8 3 | L RELAY | |

The +24V DC bus (wire 222) feeds the coils through the fuses; the lower block takes it through A9J8/A9P8 12, and its
ground bus through A9P8/A9J8 15. The remote transistors are drawn with a 2N5875 pin view (E, B, C); a handwritten "6/5 ="
beside it is an owner's annotation.

## Lamps (right half)

| Driver output | Wire | Lamp | Description as printed |
| --- | --- | --- | --- |
| A3J3-C (overbar) | 588 | L3 | SHOOT AGAIN |
| A10P4-5 from lightbox A10J4 | 533 | L7 | LEFT SPINNING TARGE[T] |
| A3J3-20 | 311 | L21 | "B" DROP TARGET LIGH[T] |
| A3J3-18 | 322 | L22 | "L" DROP TARGET LIGH[T] |
| A3J3-19 | 333 | L23 | "A" DROP TARGET LIGH[T] |
| A3J3-9 | 344 | L24 | "C" DROP TARGET LIGH[T] |
| A3J3-10 | 355 | L25 | "K" DROP TARGET LIGH[T] |
| A3J3-12 | 366 | L26 | "H" DROP TARGET LIGH[T] |
| A3J3-11 | 377 | L27 | "O" DROP TARGET LIG[HT] |
| A3J3-Y | 500 | L28 | "L" DROP TARGET LIG[HT] |
| A3J3-X | 511 | L29 | "E" DROP TARGET LIG[HT] |
| A3J3-V | 522 | L30 | 2X MULTIPLIER |
| A3J3-W | 533 | L31 | 3X MULTIPLIER |
| A3J3-5 | 544 | L32 | 4X MULTIPLIER |
| A3J3-6 | 555 | L33 | 5X MULTIPLIER |
| A3J3-K | 566 | L34 | TOP LANE #1 (10,00[0]) |
| A3J3-7 | 577 | L35 | TOP LANE #2 (EXTRA [BALL]) |
| A3J3-4 | 744 | L40 | RIGHT SIDE ROLLOVER |
| A3J3-3 | 755 | L41 | #1 TOP ROLLOVER |
| A3J3-T | 766 | L42 | #2 TOP ROLLOVER |
| A3J3-2 | 777 | L43 | #3 TOP ROLLOVER |
| A3J3-E | 844 | L48 | #1 SPOT TARGET LIG[HT] |
| A3J3-H | 855 | L49 | #2 SPOT TARGET LIG[HT] |
| A3J3-R | 866 | L50 | #3 SPOT TARGET LIG[HT] |
| A3J3-N | 877 | L51 | #4 SPOT TARGET LIG[HT] |
| A3J4-1 | 700 | L36 | TOP LANE #3 (SPEC[IAL]) |
| A3J4-2 | 711 | L37 | TOP HOLE #1 (CAPT[IVE]) |
| A3J4-4 | 722 | L38 | TOP HOLE #2 (EXTR[A BALL]) |
| A3J4-3 | 733 | L39 | RIGHT RETURN ROLL[OVER] |

Lower-playfield lamps (dashed block), through A9J6/A9P6:

| Driver output | A9J6/A9P6 | Wire | Lamp | Description as printed |
| --- | --- | --- | --- | --- |
| A10P4-2 from lightbox A10J4 | 3 | 500 | L4 | 3 POS. BANK SPECIA[L] |
| A10P4-3 from lightbox A10J4 | 4 | 511 | L5 | "+1X" SCORING (L) |
| A10P4-4 from lightbox A10J4 | 5 | 522 | L6 | "+1X" SCORING (R) |
| A3J3-15 | 1 | 177 | L19 | HOLE LIGHTS (ARRO[WS]) |
| A3J3-21 | 2 | 300 | L20 | LOOP LIGHTS (ARRO[WS]) |
| A3J3-D | 6 | 800 | L44 | #1 DROP TARGET LI[GHT] |
| A3J3-F | 7 | 811 | L45 | #2 DROP TARGET LI[GHT] |
| A3J3-P | 8 | 822 | L46 | #3 DROP TARGET L[IGHT] |
| A3J3-M | 9 | 833 | L47 | #4 DROP TARGET L[IGHT] |

## Notes and coil table

Notes as printed: "1. ALL DIODES ARE 1N4004. 2. LAMPS L32 THRU L43 ARE DRIVEN BY MPS-A13'S; ALL OTHER LAMPS ARE DRIVEN
BY MPS-U45'S. 3. UNLESS OTHERWISE SPECIFIED; ALL LAMPS ARE #44. GROUND WIRE COLOR IS 54, 18GA. 4. [XXX] INDICATES WIRE
COLOR."

"COILS USED":

| Part no. | Description | Part no. | Description |
| --- | --- | --- | --- |
| A-16570 | OUTHOLE | A-18102 | 3 POS. BANK (L) |
| A-18318 | 4 POS. BANK (U) | A-16570 | BALL GATE (L) |
| A-17891 | 5 POS. BANK (U) | A-16570 | HOLE KICKER (L) |
| A-16890 | GAME OVER RELAY | A-4893 | BALL LIFT KICKER (L) |
| A-16890 | TILT RELAY | A-16890 | LOWER RELAY (L) |
| A-16570 | BALL GATE | A-1496 | KICKING RUBBER (6) |
| A-16570 | HOLE KICKER (U) | A-17875 | FLIPPERS (6) |
| A-16890 | UPPER RELAY (U) | A-5194 | KICKING TARGET |
| A-17564 | WIREFORM BALL GATE | A-1496 | POP BUMPERS (6) |
| A-18318 | 4 POS. BANK (L) | | |
