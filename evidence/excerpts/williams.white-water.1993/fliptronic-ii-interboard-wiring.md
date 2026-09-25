# White Water — A-15472 Fliptronic II Board Interboard Wiring

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF page 146, printed
page 3-36 ("A-15472 Fliptronic II Board Interboard Wiring"). Rendered at the
scanned page's own native resolution. This page carries a board-outline
drawing of the A-15472 Fliptronic II board naming connectors J901 through
J907, plus the complete per-pin function table for J901, J902, J904, and
J905–J907 (J903 is an unlabeled 34-pin ribbon cable to J202/J601/J506).

This is the only page in the retained manual that labels each flipper-circuit
connector pin individually; the Flipper Circuits table on page 3-8
(`solenoid-flasher-wiring.md`) prints one combined "pin,pin" cell per physical
flipper position covering both windings together, with no indication of which
pin is which winding. This page resolves that: **the hold winding is on the
lower-numbered pin of each pair, the power winding on the higher**, for every
one of the three flipper positions.

## J901 (Power Driver Board 50VAC feed)

| Pin | Function |
| --- | --- |
| 1 | White-Blue (50VAC) from Power Driver Board J104-2 |
| 2 | White-Blue (50VAC) loop from J901-1 |
| 3 | White-Blue (50VAC) from Power Driver Board J104-1 |
| 4 | N/C |
| 5 | White-Blue (50VAC) loop from J901-3 |

## J902 (flipper coil windings, 13-pin)

| Pin | Function |
| --- | --- |
| 1 | N/C |
| 2 | N/C |
| 3 | N/C |
| 4 | Orange-Violet (holding) upper right flipper coil |
| 5 | N/C |
| 6 | Black-Yellow (power) upper right flipper coil |
| 7 | Orange-Blue (holding) lower left flipper coil |
| 8 | N/C |
| 9 | Blue-Gray (power) lower left flipper coil |
| 10 | N/C |
| 11 | Orange-Green (holding) lower right flipper coil |
| 12 | N/C |
| 13 | Blue-Violet (power) lower right flipper coil |

## J903, 34-pin Ribbon Cable

(data) To/from J202; J601; J506 — no per-pin function table printed.

## J904 (logic supply from Power Driver Board)

| Pin | Function |
| --- | --- |
| 1 | Gray (+5V) from Power Driver Board J114-3,4 |
| 2 | Gray-Green (+12V) from Power Driver Board J114-1,2 |
| 3 | N/C |
| 4 | Black (Grd) from Power Driver Board J114-5,7 |
| 5 | Black (Grd) from Power Driver Board J114-5,7 |

## J905 (opto switch board feeds)

| Pin | Function |
| --- | --- |
| 1 | Blue-Violet to right opto switch board J1-1 |
| 2 | Blue-Gray to left opto switch board J1-1 |
| 3 | Black-Yellow to right opto switch board J1-2 |
| 4 | N/C |
| 5 | Black-Blue to left opto switch board J1-2 |
| 6 | Orange (Grd) to left opto switch board J1-3 |

## J906 (EOS switches)

| Pin | Function |
| --- | --- |
| 1 | Black-Green to lower right EOS switch |
| 2 | N/C |
| 3 | Black-Blue to lower left EOS switch |
| 4 | Black-Violet to upper right EOS switch |
| 5 | N/C |
| 6 | Orange (Grd) to EOS switches |

## J907 (flipper coil +50V supply, 9-pin)

| Pin | Function |
| --- | --- |
| 1 | N/C |
| 2 | N/C |
| 3 | N/C |
| 4 | Blue-Yellow (+50V) to upper right flipper coil |
| 5 | Blue-Yellow (+50V) loop from J907-4 |
| 6 | Gray-Yellow (+50V) to lower left flipper coil |
| 7 | Gray-Yellow (+50V) loop from J907-6 |
| 8 | Blue-Yellow (+50V) to lower right flipper coil |
| 9 | Blue-Yellow (+50V) loop from J907-8 |

## Resulting per-winding connector map

| Position | Hold pin (wire) | Power pin (wire) | Shared supply (J907, wire) |
| --- | --- | --- | --- |
| Upper Right Flipper | J902-4 (Org-Vio) | J902-6 (Blk-Yel) | J907-4,5 (Blu-Yel) |
| Lower Left Flipper | J902-7 (Org-Blu) | J902-9 (Blu-Gry) | J907-6,7 (Gry-Yel) |
| Lower Right Flipper | J902-11 (Org-Grn) | J902-13 (Blu-Vio) | J907-8,9 (Blu-Yel) |

These wire colors match the Pwr wire/Hold wire columns already transcribed
from page 3-8 (`solenoid-flasher-wiring.md`) exactly; only the assumed
pin-to-winding order printed there was wrong. J907 is the shared +50V supply
feed for each coil's frame, common to both windings, matching the single
combined connector printed in the page 3-8 Flipper Circuits table's
Playfield (PF) column.
