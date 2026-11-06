# Xenon A9 auxiliary driver and light strip

PDF51 W-1207-3. MC14175B U1 latches AD0-AD2; four MC4028B decoders U2-U5 use PD0-PD3 at D. Output7 of every decoder is N/U; outputs8/9 are not populated. PinMAME reserves fifteen slots per data line; only output0..6 has a load candidate on this board. Public=65+16*d+a, d=0..3, a=0..6. Backbox quantity is read from numbered backside-of-insert drawings, not the emulator. Each named playfield circuit is a single schematic branch with no printed socket count; one branch does not prove one bulb. The separate owner-repair excerpt supplies observed playfield pair counts. Four door-frame quadrants have numbers1..8, each driver row reaches the two named sides. Ring-circle drawing prints each number1..7 twice. They are BACKBOX INSERT lights.

| Public (derived) | Decoder/output | SCR | J/pin | Source function | Quantity |
| --- | --- | --- | --- | --- | --- |
| 65 | U2/0 | Q1 | A9J2-7 | 1 LEFT & BOTTOM | 2 |
| 66 | U2/1 | Q2 | A9J2-4 | 5 TOP & LEFT | 2 |
| 67 | U2/2 | Q3 | A9J2-8 | 1 TOP & RIGHT | 2 |
| 68 | U2/3 | Q4 | A9J2-10 | 5 BOTTOM & RIGHT | 2 |
| 69 | U2/4 | Q5 | A9J2-9 | SIDE SAUCER | not specified (one branch) |
| 70 | U2/5 | Q6 | A9J2-6 | 3 RING CIRCLE | 2 |
| 71 | U2/6 | Q7 | A9J2-5 | N/U | no load |
| 81 | U3/0 | Q8 | A9J2-14 | 2 LEFT & BOTTOM | 2 |
| 82 | U3/1 | Q9 | A9J2-11 | 6 TOP & LEFT | 2 |
| 83 | U3/2 | Q10 | A9J2-15 | 2 TOP & RIGHT | 2 |
| 84 | U3/3 | Q11 | A9J2-18 | 6 BOTTOM & RIGHT | 2 |
| 85 | U3/4 | Q12 | A9J2-17 | END OF TUBE | not specified (one branch) |
| 86 | U3/5 | Q13 | A9J2-13 | 4 RING CIRCLE | 2 |
| 87 | U3/6 | Q14 | A9J2-12 | 7 RING CIRCLE | 2 |
| 97 | U4/0 | Q15 | A9J3-8 | 3 LEFT & BOTTOM | 2 |
| 98 | U4/1 | Q16 | A9J3-3 | 7 TOP & LEFT | 2 |
| 99 | U4/2 | Q17 | A9J3-9 | 3 TOP & RIGHT | 2 |
| 100 | U4/3 | Q18 | A9J3-11 | 7 BOTTOM & RIGHT | 2 |
| 101 | U4/4 | Q19 | A9J3-10 | BALL SHOOTER | not specified (one branch) |
| 102 | U4/5 | Q20 | A9J3-7 | 5 RING CIRCLE | 2 |
| 103 | U4/6 | Q21 | A9J3-4 | 2 RING CIRCLE | 2 |
| 113 | U5/0 | Q22 | A9J3-15 | 4 LEFT & BOTTOM | 2 |
| 114 | U5/1 | Q23 | A9J3-12 | 8 TOP & LEFT | 2 |
| 115 | U5/2 | Q24 | A9J3-16 | 4 TOP & RIGHT | 2 |
| 116 | U5/3 | Q25 | A9J3-18 | 8 BOTTOM & RIGHT | 2 |
| 117 | U5/4 | Q26 | A9J3-17 | N/U | no load |
| 118 | U5/5 | Q27 | A9J3-14 | 6 RING CIRCLE | 2 |
| 119 | U5/6 | Q28 | A9J3-13 | 1 RING CIRCLE | 2 |

Complete remaining A9J2 rows:1 N/U;2 N/U;3 KEY;16 N/U. A9J3:1 N/U;2 KEY;5 GND;6 GND;19 GND;20 GND. Decoder output7 on each U2-U5 is labelled N/U and has no resistor/SCR/load branch; upper selectors8-14 published by generic PinMAME have no independent fitted load. This is positive physical non-fitment evidence, not a runtime disposition. Separately, selftest-run.json, aux-run.json and play2-run.json show public72/88/104/120 active in every post-stabilization snapshot, with72 also toggling during startup. Pinned by35.c:134-148,151-166,273-280,387-390 shows how the selected bit is accumulated and refreshed but does not prove why the ROM drives output7. The parked-decoder explanation remains unproven; these four virtual addresses have unknown availability and observed runtime provenance. Selectors8-14 remain distinct generic padding.

Complete right-hand interboard lists, including wires:

| A9J2 pin | wire/function | A9J3 pin | wire/function |
| --- | --- | --- | --- |
| 1 | N/U | 1 | N/U |
| 2 | N/U | 2 | KEY |
| 3 | KEY | 3 | 20 |
| 4 | 15 | 4 | 78 |
| 5 | N/U | 5 | N/U |
| 6 | 81 | 6 | N/U |
| 7 | 10 | 7 | 82 |
| 8 | 51 | 8 | 13 |
| 9 | 54 | 9 | 53 |
| 10 | 56 | 10 | 25 |
| 11 | 18 | 11 | 58 |
| 12 | 85 | 12 | 21 |
| 13 | 81 | 13 | 60 |
| 14 | 12 | 14 | 83 |
| 15 | 52 | 15 | 14 |
| 16 | N/U | 16 | 54 |
| 17 | 43 | 17 | N/U |
| 18 | 57 | 18 | 72 |
| [no pin] | [no pin] | 19 | N/U |
| [no pin] | [no pin] | 20 | N/U |

The board connector labels GND for A9J3-5/6/19/20 while the harness list labels them N/U: preserve this wiring-detail difference; it does not add a bulb.

PDF53 W-1207-4b light strip, complete five-group wiring: group1 pin1 wire34 DS1/DS2; pin2 KEY; group2 pin3 wire98 DS3/DS4; group3 pin4 wire85 DS5/DS6; group4 pin6 wire91 DS7/DS8; group5 pin7 wire75 DS9/DS10; switched illumination bus pin5 wire20. Each pair is parallel. PDF40 printed36 AS-2518-60 parts: item1 A12 P-2948-434 PCB Light Strip; item2 DS1-DS10 E-125-71 Miniature Light; item3 J1 E-768-7 Connector KK100.
