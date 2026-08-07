# Fish Tales — Lamp Matrix (wiring)

Transcribed from `Fish_Tales_OPS.pdf`, PDF page 96, printed page 3-2, the `Lamp Matrix` table
(identical duplicate present, unnumbered, at PDF page 148 — see `manual-transcription.md`). Read
from the rendered page, not the OCR text layer.

## Matrix drive columns

| Column | Wire | Connector | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J137 | Q98 |
| 2 | Yellow-Red | J137 | Q97 |
| 3 | Yellow-Orange | J137 | Q96 |
| 4 | Yellow-Black | J137 | Q95 |
| 5 | Yellow-Green | J137 | Q94 |
| 6 | Yellow-Blue | J137 | Q93 |
| 7 | Yellow-Violet | J137 | Q92 |
| 8 | Yellow-Gray | J137 | Q91 |

All eight columns are driven from Power Driver Board connector J137.

## Matrix return rows

| Row | Wire | Connector | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J133 | Q90 |
| 2 | Red-Black | J133 | Q89 |
| 3 | Red-Orange | J133 | Q88 |
| 4 | Red-Yellow | J133 | Q87 |
| 5 | Red-Green | J133 | Q86 |
| 6 | Red-Blue | J133 | Q85 |
| 7 | Red-Violet | J133 | Q84 |
| 8 | Red-Gray | J133 | Q83 |

All eight rows are returned through Power Driver Board connector J133.

## Address legend

Printed beside the matrix; agrees address-for-address and label-for-label with the Lamp Locations
parts list (`lamp-locations.md`) — no disagreement between the two pages.

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Hold Bonus | 31 | Stringer Tail 1 | 51 | Bonus 1X | 71 | Casters Club |
| 12 | Video Mode | 32 | Stringer Tail 2 | 52 | Bonus 2 X | 72 | Doubles Jackpot |
| 13 | Rock the Boat | 33 | Stringer Tail 3 | 53 | Auto Cast | 73 | Lock 3 |
| 14 | Light Extra Ball | 34 | Stringer Tail 4 | 54 | Bonus 4X | 74 | Lock 2 |
| 15 | Instant Multi-ball | 35 | Right Boat Entry | 55 | Right Fish Head | 75 | Lock 1 |
| 16 | Lie (L) | 36 | Rt. Boat Feed Frenzy | 56 | Right Fish Body | 76 | Rt. Side Feed Frenzy |
| 17 | Lie (I) | 37 | Left Boat Entry | 57 | Right Fish Tail | 77 | Long Cast |
| 18 | Lie (E) | 38 | Lt. Boat Feed Frenzy | 58 | Light Long Cast | 78 | Extra Ball |
| 21 | Stringer Body 1 | 41 | Tropical | 61 | School Fish 1 | 81 | Stretch 5X Actual |
| 22 | Stringer Body 2 | 42 | Freshwater | 62 | School Fish 2 | 82 | Stretch 3X Actual |
| 23 | Stringer Body 3 | 43 | Cast Again | 63 | School Fish 3 | 83 | Stretch 2X Actual |
| 24 | Stringer Body 4 | 44 | Deep Sea | 64 | School Fish 4 | 84 | Stretch Actual Size |
| 25 | Lt. Side Feed Frenzy | 45 | Left Fish Head | 65 | School Fish 5 | 85 | Stretch Total Lie |
| 26 | Monster Bonus | 46 | Left Fish Body | 66 | School Fish 6 | 86 | Video Mode |
| 27 | Fish Finder | 47 | Left Fish Body [sic, repeats 46's label] | 67 | Super Jackpot | 87 | Cast |
| 28 | Jackpot | 48 | Specials | 68 | Light Fish Finder | 88 | Start Button |

Note on address 47: this legend prints "Left Fish Body" for both 46 and 47, which does not match
the Lamp Locations parts list (`lamp-locations.md`), which prints 46 "Left Fish Body" and 47 "Left
Fish Tail" — a clear pairing with the matching 56/57 "Right Fish Body"/"Right Fish Tail" entries on
both pages, and with 45/55 "Left/Right Fish Head". The parts list is taken as authoritative for the
label per this project's standing convention (prefer the parts list over the matrix legend for
wording), and this discrepancy is recorded here rather than silently corrected on the matrix side.
Every other address in this legend agrees with the parts list.

Compare also address 16/17/18 wording: this legend reads "Lie (L)"/"Lie (I)"/"Lie (E)" in that
order (16, 17, 18), while the parts list reads "Letter (L) IE"/"Letter L(I)E"/"Letter Ll(E)" for the
same three addresses in the same order — both agree on which physical lane is which address; only
the exact parenthesis wording differs (see `switch-matrix.md` for the identical pattern on the
switch side, addresses 44/45/46).
