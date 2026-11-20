# Factory solenoid driver and load routing, #1104-E

W-1183-5c (schematics PDF page 4), U2 decoder and continuous drivers.
The selector and PB bit are source labels. The public number is
derived from the driver. Slash-separated connectors identify branches
shown electrically common on this sheet. J2 coordinates are A3 on
this sheet. Parts and printed test order are in FO 579 page 17/20.
Where a branch is N/U or reserved, the following annotates fitment
from W-1187-1c (page 7), A3 connector list, and W-1192-1c (page 8).

| Selector | U2 pin | Driver | A3 connector | Printed load (on active branch) | Public |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | Q2 | J1-3 | SAUCER | 1 |
| 1 | 2 | Q1 | J2-9 / J1-2 | CHIME 10 | 2 |
| 2 | 3 | Q5 | J2-10 | CHIME 100 | 3 |
| 3 | 4 | Q6 | J2-11 | CHIME 1000 | 4 |
| 4 | 5 | Q7 | J2-12 | EXTRA CHIME | 5 |
| 5 | 6 | Q3 | J3-4 / J2-5 | KNOCKER | 6 |
| 6 | 7 | Q4 | J1-5 | OUTHOLE | 7 |
| 7 | 9 | Q8 | J5-10 | LT BOTTOM BUMPER | 8 |
| 8 | 10 | Q13 | J5-12 | LT TOP BUMPER | 9 |
| 9 | 11 | Q14 | J5-11 | RT TOP BUMPER | 10 |
| 10 | 12 | Q9 | J5-9 | RT BOTTOM BUMPER | 11 |
| 11 | 13 | Q10 | J5-15 | LT SLING SHOT | 12 |
| 12 | 14 | Q12 | J5-13 | LT DROP TARGET RESET | 13 |
| 13 | 15 | Q11 | J5-14 | RT SLING SHOT | 14 |
| 14 | 16 | Q16 | J5-8 | RT DROP TARGET RESET | 15 |
| 15 | 17 | [blank] | [blank] | OPEN | — |

| PIA bit | A3 J3 logic input | Driver | Load branch | Public |
| --- | --- | --- | --- | --- |
| PB4 | 11 CONT. 2 | Q17 | J5-7 N/U | 17 |
| PB5 | 9 CONT. 4 | Q19 | J2-8 COIN L/O | 18 |
| PB6 | 8 CONT. 1 | Q15 | K1 FLIPPER ENABLE RLY. | 19 |
| PB7 | 10 CONT. 3 | Q18 | J2-15 / J5-3 N/U | 20 |

A3J1-2 and A3J2-5 are marked NOTE 1, reserved, on W-1187-1c.
A3J5-3 also says NOTE 1 there. Its matching playfield sheet does
not populate the wire. For the outputs above, the game wiring
labels are:

| Load destination | Wire code | A3 jack |
| --- | --- | --- |
| SAUCER | 53-1 | J1-3 |
| CHIME 10 | 58 | J2-9 |
| CHIME 100 | 57 | J2-10 |
| CHIME 1000 | 56 | J2-11 |
| EXTRA CHIME | 54 | J2-12 |
| KNOCKER | 83 | J3-4 |
| OUT HOLE | 63-1 | J1-5 |
| LT. BOTTOM BUMPER | 74 | J5-10 |
| LT. TOP BUMPER | 75 | J5-12 |
| RT. TOP BUMPER | 78 | J5-11 |
| RT. BOTTOM BUMPER | 71 | J5-9 |
| LT. SLING SHOT | 85 | J5-15 |
| LT. DROP TARGET RESET | 80 | J5-13 |
| RT. SLING SHOT | 83 | J5-14 |
| RT. DROP TARGET RESET | 18 | J5-8 |
| COIN LOCKOUT | 36 | J2-8 |
| K1 supply, TO A2J3-9 | 30 | J3-5 |

Wire codes come from W-1186-4c, W-1187-1c and W-1192-1c. For the
saucer and outhole the playfield sheet adds the branch suffix
`-1` to codes `53` and `63` from the backbox wiring diagram.
The backbox J2 diagram calls the last chime EXTRA CHIME, the A7
drawing calls it CHIME X, and FO 579 names it CHIME 10,000.

W-1183-5c draws two K1 contacts, one between each cabinet button
(J2-1 right, J2-2 left) and the corresponding playfield flipper coil
(J1-9 right, J1-8 left). W-1192-1c draws a local EOS switch across
one of each coil's windings. W-1192-1c also draws two parallel
coil symbols on each drop-reset line. FO 579 lists two reset coils
without specifying whether the count is per game or per assembly.
The symbols and parts-list count are kept separately.
