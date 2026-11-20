Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 36-37: the PLAYFIELD flipper and coil wiring. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) - Playfield coil wiring (PDF page 36 right part + PDF page 37 left part)

Pages: PDF page 36 (right part) and PDF page 37 (left part), one continuous drawing, hand lettered, "PLAYFIELD".

Drive connectors are written A3Jn-m on the left margin of the drawing; the wire colour is printed in parentheses on the same line. Each coil has a diode drawn across it (cathode toward the supply side, i.e. the (-Y-) bus) unless stated.

## Supply buses
| Bus | Printed label | Notes |
| --- | --- | --- |
| Flipper supply | A2J1-6 (BLU-W) | top line, runs to the left flipper, right flipper and upper right flipper coils; also runs right and down through the fuse (see next row) |
| Solenoid supply | (-Y-) | a yellow bus (printed "(-Y-)" at several heads) feeding thumper, slingshots, drop-target coils, out-hole, 6-drop coils |
| Fuse | "1-AMP. S.B. PLAYFIELD FUSE" | vertical fuse symbol on the right edge; the A2J1-6 (BLU-W) bus continues through it into the (-Y-) bus |

Observation: the flipper bus A2J1-6 (BLU-W) and the (-Y-) coil bus are joined through the 1-amp slow-blow fuse; no other fuse is drawn.

## Flippers (top of PDF page 36)
| Coil | Drive connection | Wire colour | Drawing |
| --- | --- | --- | --- |
| LEFT FLIPPER | A3J1-9 | (-G-) | two windings in series, a diode across each, plus a switch drawn from the top node to the middle node (bracket + blade, with a flag-shaped contact); lower end of the windings goes to A3J1-9 |
| RIGHT FLIPPER | A3J1-8 | (-O-) | same construction (two windings, two diodes? see Uncertain), switch top-to-middle node |
| UPPER RIGHT FLIPPER | no direct drive line; its lower end connects through "E.O.S." to the node at the right flipper's lower end (the A3J1-8 line) | - | two windings, switch top-to-middle node |

E.O.S.: a contact symbol (two vertical bars, drawn like a capacitor) labelled "E.O.S." between the right flipper's lower node and the upper right flipper's lower node. It is the only drawing labelled E.O.S.; the "flag" switch symbols on the three flippers are unlabelled.

## Thumper
| Coil | Drive connection | Wire colour | Notes |
| --- | --- | --- | --- |
| THUMPER | A3J2-4 (as printed) | (PUR-W) | diode across, supply (-Y-) |

## Coils below (PDF page 36 right / PDF page 37 left), in drawing order
| Coil label (printed) | Drive connection | Wire colour | Notes |
| --- | --- | --- | --- |
| LEFT SLING SHOT | A3J2-4 | (BRN-) | diode, supply (-Y-) |
| RIGHT SLING SHOT | A3J5-11 | (O-W) | diode |
| TOP LFT. 3-BANK DROP TARG. | A3J2-10 | (G-R) | diode |
| OUT HOLE | A3J5-8 | (R-B) | diode |
| LOWER LFT. 3-BANK DR. TARG. | A3J1-5 | (BRN-Y) | diode |
| RIGHT 3-BANK DROP TARGET | A3-J5-12 | (O-B) | diode |
| 6-DROP TARGETS "M" | A3-J2-11 | (GREY) | diode |
| 6-DROP TARGETS "E" (first) | A3-J2-12 | (Y-W) | diode |
| 6-DROP TARGETS "T" | A3-J5-10 | (B-Y) | diode |
| 6-DROP TARGETS "E" (second) | A3-J5-9 | (O-R) | diode |
| 6-DROP TARGETS "O" | A3-J5-15 | (B-BLU) | diode |
| 6-DROP TARGETS "R" | A3-J5-14 | (Y-BLU) | diode |

(-Y-) is printed over the supply heads of: thumper, sling shots, lower/right bank row, and the 6-drop row ("(-Y-) 6-DROP TARGETS").

Not drawn on the playfield coil sheet: KNOCKER (cabinet sheet), COIN LOCKOUT (cabinet sheet), a separate METEOR DROP TARGET coil on J5-13 (O-W) (on the solenoid sheet).

## Uncertain readings
- the switch/contact symbols inside the flipper windings (bracket with filled flag) are unlabelled; read as the end-of-stroke (cut-off) contacts but not so labelled except the E.O.S. symbol between right and upper right flippers.
- the left flipper windings each have a diode; the right and upper right flipper windings are drawn WITHOUT diodes (windings only plus the switch). Best reading from the enlargements; the right flipper's lower node dots may hide a diode.
- wire routing from coil bottoms to the A3 lines is a nested set of rectangular loops; assignment of each wire to each coil was done from loop order (inner loop = upper line), consistent with the solenoid sheet pin names.
- the thumper's connector text reads "A3J2-4" (probable misprint).
