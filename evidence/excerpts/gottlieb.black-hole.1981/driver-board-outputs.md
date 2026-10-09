# Black Hole — Driver board (A3) schematic, lamp and solenoid outputs (printed pages 25-26)

Source: the idoc.pub copy of the Gottlieb *Black Hole Instruction Manual* (document jlk9z9rz1545), viewer pages 27 and
28 (printed pages 25 and 26), drawing E-20915 "DRIVER BOARD (A3), SYSTEM 80", dated 12-12-80. The idoc copy is the
sharper scan of these two pages (1219 x 1562 and 1230 x 1562 page images); the Scribd copy has the same pages at viewer
27-28. Read from the page images directly.

Four lamp-data lines LD1-LD4 (P/O A3J1 pins 7, 6, 4, 5) feed twelve SN74175 quad latches Z1-Z12, each clocked by its
own strobe DS1-DS12 from A3J1. Note 4: "INTEGRATED CIRCUITS ARE SN74175N"; note 5: "TRANSISTOR TYPES MPS-A13 AND
MPS-U45 ARE NPN DARLINGTONS". Each latch output drives one transistor through a 1.0K resistor.

## Lamp latches (printed page 25, and Z10-Z12 on page 26)

| Latch (strobe) | Output | Transistor | Connector pin | Label as printed |
| --- | --- | --- | --- | --- |
| Z1 (DS1, A3J1-C) | Q1 | Q1 MPS-U45 | A3J3-A (overbar) | GAME OVER RELAY |
| | Q2 | Q2 MPS-U45 | A3J3-B (overbar) | TILT RELAY |
| | Q3 | Q3 MPS-U45 | A3J5-2 | COIN LOCKOUT COIL |
| | Q4 | Q4 MPS-U45 | A3J3-C (overbar) | L3 SHOOT AGAIN (PLAYBOARD) |
| | | (same line) | A3J2-1 | L2 SHOOT AGAIN (LIGHTBOX) |
| Z2 (DS2, A3J1-3) | Q1-Q4 | Q5-Q8 MPS-A13 | A3J2-2, -3, -5, -4 | L4, L5, L6, L7 |
| Z3 (DS3, A3J1-E) | Q1 | Q9 MPS-A13 | A3J2-10 | L8 |
| | Q2 | Q10 MPS-A13 | A3J2-9 | SOUND 16 |
| | Q3 | Q11 MPS-A13 | A3J2-7 | L11 |
| | Q4 | Q12 MPS-A13 | A3J2-8 | L10 |
| Z4 (DS4, A3J1-D) | Q1-Q4 | Q13-Q16 MPS-U45 | A3J3-25, -24, -22, -23 | L12, L13, L14, L15 |
| Z5 (DS5, A3J1-H) | Q1-Q4 | Q17-Q20 MPS-U45 | A3J3-13, -14, -16, -15 | L16, L17, L18, L19 |
| Z6 (DS6, A3J1-F) | Q1-Q4 | Q21-Q24 MPS-U45 | A3J3-21, -20, -18, -19 | L20, L21, L22, L23 |
| Z7 (DS7, A3J1-K) | Q1-Q4 | Q25-Q28 MPS-U45 | A3J3-9, -10, -12, -11 | L24, L25, L26, L27 |
| Z8 (DS8, A3J1-J) | Q1-Q4 | Q29-Q32 MPS-U45 | A3J3-Y, -X, -V, -W | L28, L29, L30, L31 |
| Z9 (DS9, A3J1-M) | Q1-Q4 | Q33-Q36 MPS-A13 | A3J3-5, -6, -K, -7 | L32, L33, L34, L35 |
| Z10 (DS10, A3J1-L) | Q1-Q4 | Q37-Q40 MPS-A13 | A3J4-1, -2, -4, -3 | L36, L37, L38, L39 |
| Z11 (DS11, A3J1-N) | Q1-Q4 | Q41-Q44 MPS-A13 | A3J3-4, -3, -T, -2 | L40, L41, L42, L43 |
| Z12 (DS12, A3J1-P) | Q1-Q4 | Q45-Q48 MPS-U45 | A3J3-D, -F, -P, -M | L44, L45, L46, L47 |
| | Q1-bar to Q4-bar (inverted outputs) | Q49-Q52 MPS-U45 | A3J3-E, -H, -R, -N | L48, L49, L50, L51 |

Lamp grounds ("LAMP GND."): A3J2-6, A3J3-17, A3J3-U, A3J3-Z, A3J4-5, A3J3-S and A3J3-C (plain C; the shoot-again
line is the overbarred C). A3J3 pins B, 1 and A carry +5V and ground beside Z12. Pin letters printed with an overbar
are distinct pins from the plain letters. The Z3 row is transcribed as printed: its Q3 line is labelled L11 and its Q4 line L10, the
reverse of the Q1-Q4 order every other latch follows.

## Solenoid and sound lines (printed page 26)

| A3J1 input | Transistor | Connector pin | Label as printed |
| --- | --- | --- | --- |
| B, A, Z, Y | Z13 SN7404N inverters | A3J5-6, -5, -1, -7 | SOUND 1, SOUND 2, SOUND 4, SOUND 8 |
| 21 (diode CR1) | Q53 2N6043 | A3J5-8 (ground A3J5-3) | SOL. 8 |
| 24 (CR2) | Q54 MPS-U45 | A3J6-3 | SOL. 3 |
| 23 (CR3) | Q55 MPS-U45 | A3J6-2 | SOL. 4 |
| 22 (CR4) | Q56 MPS-U45 | A3J6-1 (ground A3J6-4) | SOL. 7 |
| X | Q57 MPS-U45 driving Q58 2N3055 | A3J4-13 (ground A3J4-10) | SOL. 2 |
| T (CR5) | Q59 2N6043 | A3J4-8 (ground A3J4-9) | SOL. 9 |
| S (CR6) | Q60 2N6043 | A3J4-7 | SOL. 1 |
| R | Q61 MPS-U45 driving Q62 2N3055 | A3J4-6 (ground A3J4-14) | SOL. 5 |
| U | Q63 MPS-U45 driving Q64 2N3055 | A3J4-12 (ground A3J4-11, -15) | SOL. 6 |
