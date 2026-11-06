# Display glasses and complete display-board parts table

Source: Williams F-14 Tomcat factory manual, May 1987, 16-549-101, PDF page 39 / printed page 34, SHA-256 `a4ee36637957f770040db76015e784f000f90bab9cf7e8087bb86c37bd8dc10b`. Method: manual; transcribed and visually checked by primary GPT Sol against the retained native scan and enlarged renders of both table columns. Reviewed: true. The full board-parts region is transcribed below, left column followed by right column; punctuation, line wraps and spacing are normalized. `[blank]` records an empty printed cell.

## Alphanumeric Display Unit Board

Printed heading: including p/n D-11609 and associated parts.

| Part No. | Ckt Designator | Description |
| --- | --- | --- |
| 5760-12134-00 | [blank] | Bare P. C. Board |
| 5680-08968-00 | U8, U13, U14, U16 | IC, Anode/Digit Driver, UDN6118A or 6184 |
| 5310-09882-00 | U4 - U7 | IC, Quad NOR, 4001B |
| 5680-08969-00 | U11, U12, U15 | IC, Cathode Seg. Driver, UDN7180A |
| 5310-09153-00 | U1 - U3, U9, U10 | IC, Hex Buffer, 4050 |
| 5075-09135-00 | D1 | Zener diode, 1N4740A, 10V, 1 w |
| 5040-09343-00 | C4 | Capacitor, 10 µfd., 25v, ±5%, Axial |
| 5043-08996-00 | C3 | Capacitor, 0.1 µfd., 50v, ±20%, Axial |
| 5043-08980-00 | C1, C2, C5 - C7 | Capacitor, 0.01 µfd., 50v, Axial |
| 5019-10387-00 | SR1 - SR3 | SIP, 18 K, 9R, 10P, 5% |
| 5010-08773-00 | R1, R2, R8, [R20/R26 unclear], R23 | Resistor, 18 K, 1/4 w, 5% |
| 5010-10927-00 | R4, R6, R18, R19, R21, R22, R24, R25 | Resistor, 8.2 K, 1/2 w, 5% |
| 5010-10258-00 | R27, R28, R30 - R35 | Resistor, 1 M, 1/4 w, 5% |
| 5010-08981-00 | R3, R5, R7, R9, R10, R12 - R17 | Resistor, 10 K, 1/2 w, 5% |
| 5010-08772-00 | R11 | Resistor, 15 K, 1/4 w, 5% |
| 5670-10873-00 | DSPY1, DSPY2 | Display, 7-character, ALN |
| 5670-09439-00 | DSPY3, DSPY4 | Display, 7-character, 7-segment |
| 5791-10851-00 | J1 | Connector, 26 pin (Hdr), Rt. Angle |
| 5791-10869-06 | J2 | Connector, 6 pin (Hdr), Rt. Angle |
| 5791-10869-09 | J3 - J5 | Connector, 9 pin (Hdr), Rt. Angle |
| 03-8088-1 | Support | Support, Display |

The fourth designator in the first right-column resistor row is indistinct in the retained scan: R20 and R26 cannot be distinguished confidently. It is explicitly unresolved transcription detail, not an inferred resistor assignment or an additional machine-readiness claim. The two DSPY rows and both display-glass part numbers are clear.

## Glass-drawing context

The drawings above this table show the seven-position alphanumeric glass, p/n 5670-10873-00, and seven-position seven-segment glass, p/n 5670-09439-00, followed by their character-segment designations. Together with the complete board-parts table, they establish two alphanumeric and two numeric glasses. Public segment starts come from the pinned emulator layout and macro, not from a physical drawing coordinate or an added host offset.
