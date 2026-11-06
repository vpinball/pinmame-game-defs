# Haunted House: displays and lightbox wiring

Original manual SHA-256 `168a1bc2e2198b03154835d45471eb5b3910f1619930c5c3fd48f9b86ad8c21f`. Primary curator visually checked PDF 29–30/printed 25–26, PDF 35–36/printed 31–32, PDF 45–46/printed 41–42 and PDF 60/printed 56. Diagram prose below is a literal circuit-label transcription, with normalized line wrapping. Complete printed lightbox-parts table follows.

The lightbox schematic shows four A4 SCORE DISPLAY boards, A5 STATUS DISPLAY (four digits), and a separate 5A4 BONUS DISPLAY inside the explicitly dashed LOCATED ON MAIN PLAYFIELD region. Segment digits for the bonus are D1–D6. The lightbox-parts drawing shows four six-digit windows and one four-digit status window; the main-playboard drawing PDF 53 places the six-digit bonus at the front of the cellar viewing window.

The driver-board latch Z1 Q4 drives A3 transistor Q4. Its common collector fans out directly to A3J3-C-bar L3 SHOOT AGAIN (PLAYBOARD) and A3J2-1 L2 SHOOT AGAIN (LIGHTBOX). Both bulbs share public lamp 3. L2 here is a printed lamp label, not the emulator's lamp 2 latch bit. A3 Q5 belongs to Z2 Q1/public 4. The complete Z1/Z2 output region on PDF 29/printed 25 reads:

| Public latch | IC output | A3 transistor | Connector | Printed load/label |
| --- | --- | --- | --- | --- |
| 0 | Z1 Q1 | Q1 MPS-U45 | A3J3-A-bar | GAME OVER RELAY |
| 1 | Z1 Q2 | Q2 MPS-U45 | A3J3-B-bar | TILT RELAY |
| 2 | Z1 Q3 | Q3 MPS-U45 | A3J5-2 | COIN LOCKOUT COIL |
| 3 | Z1 Q4 | Q4 MPS-U45 | A3J3-C-bar and A3J2-1 | L3 SHOOT AGAIN (PLAYBOARD), L2 SHOOT AGAIN (LIGHTBOX) |
| 4 | Z2 Q1 | Q5 MPS-A13 | A3J2-2 | L4 |
| 5 | Z2 Q2 | Q6 MPS-A13 | A3J2-3 | L5 |
| 6 | Z2 Q3 | Q7 MPS-A13 | A3J2-5 | L6 |
| 7 | Z2 Q4 | Q8 MPS-A13 | A3J2-4 | L7 |

The PDF 29/printed 25 Z1 Q3 driver region identifies the coin-lockout coil and its A3 Q3 MPS-U45 driver and A3J5-2 connector; that region omits the winding, wire and supply. PDF 46/printed 42 identifies A3J5 pin 2 as COIN LOCKOUT wire 877 and shows it passing through A12J7/P7 pin 8 to the front-door COIN LOCKOUT coil. Its other end goes through pin 7 on wire 222. PDF 45/printed 41 labels the rectifier output on wire 222 +24V DC; the adjacent +38V DC rectifier is separate. The winding part number remains unknown in the retained evidence.

- [Master driver connector fanout](coin-lockout-driver.webp): PDF 46/printed 42, A3J5 and the wire 877 driver branch.
- [Front-door coil branch](coin-lockout-door.webp): PDF 46/printed 42, A12J7/P7 pins 7 and 8, wires 222 and 877, and the coil.
- [Rectifier supply](coin-lockout-supply.webp): PDF 45/printed 41, +24V DC wire 222 and the adjacent +38V DC supply.

Z3 Q2 / Q10 / A3J2-9 is SOUND16. Z3 Q3 / Q11 / A3J2-7 is printed L11 on the board and HIGH GAME TO DATE on the lightbox sheet. Z3 Q4 / Q12 / A3J2-8 is printed L10 on the board and GAME OVER on the lightbox sheet. PinMAME numbers by latch order: public 10 is Q3/high game to date and public 11 is Q4/game over. Keep the swapped printed L labels as manual aliases rather than swapping public bindings.

Other lightbox branches: NAME AND SCENE LAMPS on 6.3VAC 077 / return 000; TILT LIGHT A10J4/P4-2 wire 022 from T relay; MATCH LIGHT pin 1 wire 011 and BALL IN PLAY LIGHT pin 3 wire 033 from Q relay. The note says name/scene bulbs are #44 or #455 flashing. A12P4-13 is +6V DC 322; pin 14 SOUND16 is 555. Ground wire color 54, 18GA. These relay-contact legends are physical loads; no additional independent CPU lamp addresses are printed for them.

## LIGHTBOX PARTS, PDF 60/printed 56

| ITEM | DESCRIPTION | PART NO. |
| --- | --- | --- |
| 1 | Cable Assy. | Specify Game |
| 2 | Light Box Assy. | Specify Game |
| 3 | Power Supply Assy. | MA-114 |
| 4 | Control Board Assy. | RS-30 |
| 5 | Game Prom | 669/1 |
| 6 | Sound/Speech Power Supply | MA-188 |
| 7 | Master Driver Board Assy. | RS-21 |
| 8 | Sound/Speech Board Assy. | MA-216 |
| 9 | Sound Prom | 669/S2 |
| 10 | Sound Prom | 669/S1 |
| 11 | Grill Assy. (2 ea.) | D-20405 |
| 12 | 6 Digit Display | MA-116 |
| 13 | 4 Digit Display | MA-115 |
| 14 | Insert | Specify Game |
| 15 | Back Glass | Specify Game |

Note: Auxiliary Lamp Driver Board not shown—Part No. MA-234. Lamps used are #455 (3EA) and #44 (55EA). These counts refer to the lightbox, not the playfield GI.
