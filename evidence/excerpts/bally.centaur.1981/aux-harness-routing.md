# Transcription: Centaur harness routing sheet (W-1255-2), printed page 46 (PDF page 46)

Source: `manual-schematics.bally.centaur.1981` (the Installation and General Game
Operation Instructions with schematics PDF). This drawing shows the A9 (auxiliary
lamp driver) board's J2 and J3 connector wiring: each entry reads **main-matrix
lamp number → A9 connector pin → printed function** (where documented). The
main-matrix lamp number tells the technician which column+row encoding on the
lamp bus triggers that aux circuit's pair of bulbs via the AS-2518-43.

## A9J3 (upper bank):

| Lamp | A9J3 pin | Function |
|------|----------|----------|
| 72 | A9J3-18 | |
| NIU | A9J3-17 | |
| 56 | A9J3-16 | |
| 14 | A9J3-15 | |
| 21 | A9J3-12 | |
| 70 | A9J3-11 | |
| 53 | A9J3-9 | |
| 13 | A9J3-8 | |
| NIU | A9J3-6 | |
| NIU | A9J3-5 | |
| 20 | A9J3-3 | |

## A9J2 (lower bank):

| Lamp | A9J2 pin | Function |
|------|----------|----------|
| 27 | A9J2-12 | LEFT THUMPER BUMPER |
| 96 | A9J2-17 | #4 CHAMBER (2) (TOP) |
| 54 | A9J2-7 | TOP LEFT LANE |
| 82 | A9J2-19 | RIGHT THUMPER BUMPER |
| 95 | A9J2-20 | #3 CHAMBER (2) |
| 57 | A9J2-18 | |
| 43 | A9J2-1 | TOP MIDDLE LANE |
| NIU | A9J2-16 | |
| 52 | A9J2-15 | |
| 12 | A9J2-14 | |
| 40 | A9J2-2 | LEFT SLING SHOT |
| 62 | A9J2-3 | #2 CHAMBER (2) |
| 18 | A9J2-11 | |
| 80 | A9J2-10 | |
| 25 | A9J2-18 | TOP RIGHT LANE |
| 51 | A9J2-8 | |
| 10 | A9J2-7 | |
| 45 | A9J2-6 | RIGHT SLING SHOT |
| 60 | A9J2-5 | #1 CHAMBER (2) (FROM BOTTOM) |
| 15 | A9J2-4 | |
| 20 | A2J1-5 | (5.4 VAC) |

## Key observations

1. **A9J2-11 maps to main-matrix lamp 18 ("2K Bonus")** with the function cell
   blank -- the same deliberate blank as on the page-51 schematic. The lamp
   number identifies the column+row encoding whose strobe triggers this circuit:
   main-matrix lamp 18 (col 3, row 2). The game lights 2K Bonus, the aux board
   sees the encoding, and A9J2-11's pair of bulbs fire. The circuit is therefore
   a 2K Bonus companion illumination.
2. **A9J2-7 = 54 TOP LEFT LANE and A9J2-18 = 25 TOP RIGHT LANE** -- independently
   confirming the page-51 schematic's annotations for these two contested pins.
   The routing sheet is drawing W-1255-2, a different Bally drawing from the
   page-51 schematic (W-1207-11), produced for the harness fabricator rather
   than the board designer.
3. **Several pins have blank functions but printed lamp numbers** (52→A9J2-15,
   12→A9J2-14, 80→A9J2-10, 51→A9J2-8, 10→A9J2-7 second entry, 15→A9J2-4,
   57→A9J2-18 second entry). These document the second bulb of each series pair,
   routed to a different playfield location from the function-bearing bulb.
4. **A9J2-11 has only one entry** (18, no function) -- no second entry exists,
   so both bulbs in its pair are routed together, or the second wire's routing
   reference was omitted.
