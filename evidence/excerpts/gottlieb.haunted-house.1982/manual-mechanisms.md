# Haunted House: mechanism construction

Original manual SHA-256 `168a1bc2e2198b03154835d45471eb5b3910f1619930c5c3fd48f9b86ad8c21f`. Primary curator visually checked PDF 42–43/printed 38–39, PDF 61/printed 57 and PDF 62/printed 58. The source diagrams' roles and the complete assembly parts tables are retained below. Descriptions of drawn topology are curator observations, not extra printed cells.

## Cellar K relay and reset, PDF 42/printed 38

The retained crop `cellar-relay-reset.webp` shows A3J3-25 / wire 100 / L12 energizing K RELAY through A9P1/J1-1. A3J3-24 / wire 111 / L13 drives Q3 and the separate 5 BANK reset winding, through A9P1/J1-2. Q3 is 2N5875 OR 2N5879; R3 is 4.7K 5% 1/4W. Solenoid 6 is the separate HOLE through A3J4-12 / 233 / A9P1/J1-3. Power pins 5, 4, 15 are 255, 244, 855 respectively, labeled +24V, switched +24V fused, switched +24V.

## Cellar up-kicker contact, PDF 43/printed 39

The crop `cellar-k-contact.webp` shows the normally open K contact between wire 366 (+38V DC input on A9P1/J1-6) and wire 9 feeding UP KICKER COIL. A 3.3UF 100V N.P. capacitor C5 is across that contact. Thus L12 controls a relay that supplies a separate high-current winding. The flippers and kicking rubbers in the same block are locally switched circuits; none is another CPU solenoid output.

## Trap-door assembly, PDF 61/printed 57

The crop `trap-door-assembly.webp` shows the hinged plate, mounting plate, lever arm, coil/plunger linkage and two springs. The companion schematic PDF 42/printed 38 shows the coil's local TRAP DOOR SW. contact, separately from matrix SW36 TRAP DOOR TROUGH. That local contact has no published matrix address. PDF 14/printed 10 says the door is adjusted flush to 1/64 inch above the playfield; bracket B's leading edge is 1/8–1/4 inch left of bracket C's 45-degree bend. The installation adjustment is not a simulation travel or timing measurement.

| ITEM | DESCRIPTION | PART NO. |
| --- | --- | --- |
| 1 | Trap Door, Bracket and Stop Assy. | A-21437 |
| 2 | Hinge Pin | A-21438 |
| 3 | Tru-Arc Retaining Ring #5133-12 | FA-680 |
| 4 | Trap Door Mounting Plate | A-2384 |
| 5 | Support Bracket | A-2389 |
| 6 | Screw #6-32 x 3/16 inch Lg. | FA-87 |
| 7 | Spring | A-8727 |
| 8 | Tru-Arc Retaining Ring #5133-25 | FA-683 |
| 9 | Tru-Arc Retaining Ring #5133-18 | FA-682 |
| 10 | Link and Plunger Assy. | A-18686 |
| 11 | Spring | A-590 |
| 12 | Coil Mounting Bracket | A-15409 |
| 13 | Coil | A-17875 |
| 14 | Core | A-5065 |
| 15 | Coil Stop and Mounting | A-21441 |
| 16 | Screw | FA-67 |
| 16 (merged cell repeated) | Washer | FA-617 |
| 17 | Lever Arm | A-21435 |

## Rollover target, PDF 62/printed 58

The drawing shows a pivoted target face/arm on a fulcrum and shaft, with a return spring and no coil. The target can yield under the ball, then return by spring force. The drawing names no matrix input for the target face itself; SW26 is the separately documented roll-down target trough.

| ITEM | DESCRIPTION | PART NO. |
| --- | --- | --- |
| 1 | Target Face | See Playboard Parts Information |
| 2 | Target Arm | A-21429 |
| 3 | Fulcrum | A-15819 |
| 4 | Tru-Arc Retaining Ring #5133-18 | FA-682 |
| 5 | Spring | A-21430 |
| 6 | Shaft | A-21431 |
| 7 | Nut #*-32 | FA-652 |
| 8 | Screw | FA-300 |

The scan's nut-size character is retained as `*`; it is not read confidently enough to normalize.

## Vertical upkicker, PDF 62/printed 58

| ITEM | DESCRIPTION | PART NO. |
| --- | --- | --- |
| 1 | Wire Form and Bracket | A-21414 |
| 2 | Screw - RHMS #6-32 x 3/16 inch Lg. (3 ea.) | FA-30 |
| 3 | Screw - RHMS #5-40 x 5/8 inch Lg. | FA-2 |
| 4 | Switch | B-21415 |
| 5 | Slotted Hex - WAHMS #8-32 x 5/16 inch Lg. | FA-67 |
| 6 | Standard Washer #8 | FA-617 |
| 7 | Coil Mounting Bracket | C-21416 |
| 8 | Rubber Grommet | A-5240 |
| 9 | Plunger | A-21412 |
| 10 | Spring | A-1942 |
| 11 | Coil Mounting Bracket | A-1509 |
| 12 | Diode - 1N4004 | XO-254 |
| 13 | Coil | A-5194 |
| 14 | Sleeve | A-21411 |

This assembly's A-5194 winding does not replace the separate cellar A-21741 winding named on the game's COILS USED table. The generic exploded assembly must not silently override that game-specific row.
