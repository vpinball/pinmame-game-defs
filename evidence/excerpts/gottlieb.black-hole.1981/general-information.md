# Black Hole — Cover, PROM list, general information, coil chart, fuses and sound board test (printed cover, 1, 15-18)

Source: the idoc.pub copy of the Gottlieb *Black Hole Instruction Manual* (document jlk9z9rz1545), viewer pages 1-2 and
17-20 (cover, table of contents, printed pages 15-18); the Scribd copy has the same pages. Transcribed from the page
images.

## Cover and table of contents (viewer pages 1-2)

Cover: "BLACK HOLE INSTRUCTION MANUAL", "Gottlieb AMUSEMENT GAMES". Contents page: "FINAL EDITION APPLICABLE TO ALL GAMES
NOT HAVING THE LETTER "S" IN THEIR SERIAL NUMBER" / "BLACK HOLE (GAME #668) INSTRUCTION MANUAL". "BLACK HOLE PROMS":

| As printed | Part |
| --- | --- |
| GAME PROM (GAMES WITH SOUND SPEECH) | 668/2 |
| GAME PROM (GAMES WITH SOUND ONLY) | 668A/2 |
| SOUND SPEECH PROMS | 668/S1, 668/S2 |
| SOUND PROM | 668A/S |

The wiring section's own contents list (printed page 19) includes "INTERCONNECTION DIAGRAM (GAME NO. 668A)" on page 29.

## A. Printed circuit boards (page 15)

"A1 — Control Board; A2 — Power Supply; A3 — Driver Board; A4 — Score Displays (5); A5 — Status Display; A6 —
Sound/Speech Board; A7 — Sound/Speech Power Supply; A8 — Pop Bumper Driver Boards (6); A11 — Auxiliary Lamp Driver
Board — Lightbox". "Printed circuit board connectors will be labeled AX-JX. For example, A3-J4 is the connector J4 on
the driver board (A3)."

## B. Wire colours (page 15)

"0 Black, 1 Brown, 2 Red, 3 Orange, 4 Yellow, 5 Green, 6 Blue, 7 Purple, 8 Slate, 9 White. For example, 688 is a
BLUE-SLATE-SLATE striped wire."

## C. Fuses (pages 15-16)

Fuse panel: F1 Sound/Speech Power Supply 12VAC 1/2 Amp SLO-BLO; F2 Power Supply 10VAC 5 Amp SLO-BLO; F3 Displays 60VAC
1/4 Amp SLO-BLO; F4 Solenoids 25VAC 8 Amp SLO-BLO; F5 Controlled Lamps 8VAC 10 Amp; F6 Playboard Illumination 6.3VAC 10
Amp SLO-BLO; F7 Lightbox 6.3VAC 15 Amp SLO-BLO; F8 Sound/Speech Power Supply 24VDC 1 Amp SLO-BLO. "NOTE: F8 is not used
in foreign games."

Upper playfield fuses: F10 Right Pop Bumper 38VDC 2 1/2 Amp; F11 Bottom Left Pop Bumper 38VDC 2 1/2 Amp; F12 Upper
Center Pop Bumper 38VDC 2 1/2 Amp; F13 Lower Center Pop Bumper 38VDC 2 1/2 Amp; F14 Five Drop Target Bank 24VDC / Four
Drop Target Bank 24VDC 2 Amp; F15 Outhole, Hole Kicker 24VDC 1 Amp; F16 Trough Ball Gate 24VDC 1 Amp (all SLO-BLO).

Lower playfield fuses: F17 Kicker (to upper playfield) 24VDC 6 1/4 Amp; F18 Four Drop Target Bank 24VDC 2 Amp; F19 Ball
Return Gate 24VDC 1 Amp; F20 3-Position Drop Target Bank, 24VDC Bank, Hole Kicker 1 Amp; F21 Right Pop Bumper 24VDC 2
Amp; F22 Center Pop Bumper 24VDC 2 Amp (all SLO-BLO).

Handwritten below the table: "THIS GAME REQUIRES 3 BALLS".

## D. Coil chart (page 17)

Solenoid coils (part number, general usage, resistance in ohms, number of turns, wire gauge, wrapper colour):

| Part | Usage | Ohms | Turns | Gauge | Wrapper |
| --- | --- | --- | --- | --- | --- |
| A-1496 | KICKING RUBBERS, POP BUMPERS | 2.95 | 635 | #23 | Yellow |
| A-4893 | POP BUMPERS, BALL KICKER | 2.1 | 535 | #22 | Red |
| A-5194 | GONG | 4.5 | 780 | #24 | Blue |
| A-5195 | KNOCKER, HOLE KICKER | 12.3 | 1305 | #26 | White |
| A-16570 | HOLE KICKER, OUTHOLE | 15.5 | 1450 | #27 | Green |
| A-17875 | FLIPPERS | 2.8/40.0 | 560/1100 | #24/31 | Yellow |
| A-17891 | 5 BANK RESET | 3.35 | 850 | #22 | White |
| A-18102 | 3 BANK RESET, 7 BANK RESET USES 2 | 9.0 | 1430 | #24 | Red |
| A-18318 | 4 BANK RESET | 6.7 | 1130 | #24 | Orange |
| A-19300 | BALL KICKER | 7.8 | 1075 | #25 | Orange |
| A-20095 | SUPER FLIPPER | 1.55/35.5 | 450/900 | #22/31 | Red |

Relay coils: A-16890 Q, T, AND COIN LOCKOUT RELAYS 231.0 ohms, 4000 turns, #35, Orange; A-20558 GATE RELAY 156.0, 3400,
#34, White; A-18642 MEMORY/DROP TARGETS 58.0, 1590, #33, White. "*Coils may vary from game to game. Check game manual
for exact coil usage."

## E. Sound/speech board (A6) test (page 18)

"1. Game must be in game over mode to initiate test. 2. Pressing the test button on the sound board will initiate the
test. 3. The test must be completed to enable the sound board or game power must be turned on/off. 4. Words in bold
print with quotation marks are the voice responses the sound board issues at specific points in the test." The flow
chart runs a RAM test, an EPROM test, says "OFF" / "ON" as all DIP switches are set off and on, outputs a test tone and
then a "SOUND ENABLE TEST": "JUMPER, ONE AT A TIME, THE FOLLOWING SOUND ENABLE INPUTS (AT THE A6-J1 CONNECTOR) TO GROUND.
A6J1-8 Sound 1 — Response "1"; A6J1-9 Sound 2 — Response "2"; A6J1-11 Sound 4 — Response "4"; A6J1-12 Sound 8 —
Response "8"; A6J1-2 Sound 16 — Response "16"." "NOTE: SB1-2 AND SB1-8 ARE NOT INVOLVED IN DIP SWITCH TESTS."

## System 80 sound circuitry (printed page 29, Scribd viewer page 31)

Headed "SYSTEM 80 SOUND CIRCUITRY" (the page the wiring section's contents list as the 668A interconnection diagram):
"When the System 80 Sound/Speech Board is to be replaced by the Sound Board, the System 80's circuitry must be altered in
the following manner: 1. The Sound Speech Board is removed from its connector A6J1. 2. The Sound Board (A6) is then
installed in the same connector (A6J1) vacated by the sound/speech board in step one. 3. The Sound/Speech Power Supply
Board, A7, is removed from its connector, A12J3. 4. The female connector A12J3, and its male connector A12P3, are then
connected. In doing so 12VDC, 12VAC and a return for the 12VAC return will be available for use by the Sound Board. 5.
Once this procedure has been completed power can be safely applied to the game and the Sound Board." "WARNING: THESE
BOARDS ARE NOT INTERCHANGEABLE. INSTALLING ONE OF THESE BOARDS IN A GAME WHICH DOES NOT HAVE THE PROPER CIRCUITRY WILL
SEVERELY DAMAGE THAT BOARD."
