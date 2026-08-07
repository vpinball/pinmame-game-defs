# Bram Stoker's Dracula — Switch Matrix

Transcribed from `Dracula_Bram_Stoker_OPS.pdf`, PDF page 116, printed page 3-4, the SWITCH
MATRIX table. Produced by rendering the retained PDF at 300 dpi grayscale with `pdftoppm`
and reading the table directly. This page marks opto-construction switches by writing
"Opto" directly into the printed cell label rather than by shading; no crop is needed
because the evidence is the printed text itself, which is fully captured below.

Column wiring: 1 Green-Brown J207-1/U20-18, 2 Green-Red J207-2/U20-17, 3 Green-Orange
J207-3/U20-16, 4 Green-Yellow J207-4/U20-15, 5 Green-Black J207-5/U20-14, 6 Green-Blue
J207-6/U20-13, 7 Green-Violet J207-7/U20-12, 8 Green-Gray J207-9/U20-11. Row wiring: 1
White-Brown J209-1/U18-11, 2 White-Red J209-2/U18-9, 3 White-Orange J209-3/U18-5, 4
White-Yellow J209-4/U18-7, 5 White-Green J209-5/U19-11, 6 White-Blue J209-7/U19-9, 7
White-Violet J209-8/U19-5, 8 White-Gray J209-9/U19-7.

## Switch matrix (column = tens digit, row = units digit)

| Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 21 | Slam Tilt | 31 | Under Shooter Ramp | 41 | Trough 1 Ball | 51 | Opto T.R. Lane | 61 | Left Jet | 71 | Opto Castle Popper | 81 | Magnet Left |
| 12 | Not Used | 22 | Coin Door Closed | 32 | Not Used | 42 | Trough 2 Balls | 52 | Opto Magnet L. Pocket | 62 | Right Jet | 72 | Opto Coffin Popper | 82 | Ball On Magnet |
| 13 | Start Button | 23 | Ticket Opto. | 33 | Not Used | 43 | Trough 3 Balls | 53 | Opto Castle 1 | 63 | Bottom Jet | 73 | Opto L. Ramp Entry | 83 | Magnet Right |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Launch Ball | 44 | Trough 4 Balls | 54 | Opto Castle 2 | 64 | Left Sling | 74 | Not Used | 84 | L. Ramp Score |
| 15 | L. Drop Target | 25 | Top 3-lane Left | 35 | Left Drain | 45 | Not Used | 55 | Opto Wire Ramp Popper | 65 | Right Sling | 75 | Not Used | 85 | L. Ramp Diverted |
| 16 | L. Drop Score | 26 | Top 3-Lane Middle | 36 | Left Return | 46 | Not Used | 56 | Opto Crypt Popper | 66 | Left 3-bank Top | 76 | Not Used | 86 | Middle 3-bank Left |
| 17 | Shooter Lane | 27 | Top 3-lane Right | 37 | Right Return | 47 | Not Used | 57 | Opto Castle 3 | 67 | Left 3-bank Middle | 77 | R. Ramp Up | 87 | Middle 3-bank Middle |
| 18 | Not Used | 28 | R. Ramp Score | 38 | Right Drain | 48 | Outhole | 58 | Mystery Hole | 68 | Left 3-Bank Bottom | 78 | Not Used | 88 | Middle 3-bank Right |

Opto set (labelled "Opto ___" on this page): `{51, 52, 53, 54, 55, 56, 57, 71, 72, 73}`.
This is columns 5 (all 7 rows) and 7 (rows 1-3 only). Pinned PinMAME's `dracGameData`
inverted-switch mask `{0x00,0x00,0x00,0x00,0x00,0x7f,0x00,0x07,0x02,0x00,0x00,0x00}`
normalizes column 5 = `0x7f` (rows 1-7, i.e. 51-57 exactly) and column 7 = `0x07` (rows
1-3, i.e. 71-73 exactly) — a clean match with zero disagreement for both columns.

Column 8 (`0x02`, row 2 only = switch 82) is **not** resolvable from this page alone: none
of 81/82/83 is written "Opto" here. The Switch Locations parts list settles it (see
`switch-locations.md`): only 82 carries genuine A-14315/A-14316 opto parts; 81 and 83 use
the plain leaf-switch part 5647-12693-14. This also matches PinMAME's column-8 mask
exactly.

## Dedicated grounded switches (coin door, printed D1-D8)

| Addr | Wire | Connector | Label |
| --- | --- | --- | --- |
| 1 (D1) | Orange-Brown | J205-1 | Left Coin Chute |
| 2 (D2) | Orange-Red | J205-2 | Center Coin Chute |
| 3 (D3) | Orange-Black | J205-3 | Right Coin Chute |
| 4 (D4) | Orange-Yellow | J205-4 | 4th Coin Chute |
| 5 (D5) | Orange-Green | J205-6 | Service Credits / Escape |
| 6 (D6) | Orange-Blue | J205-7 | Volume Down / Down |
| 7 (D7) | Orange-Violet | J205-8 | Volume Up / Up |
| 8 (D8) | Orange-Gray | J205-9 | Begin Test / Enter |

## Fliptronic grounded switches (printed F1-F8, public 111-118)

| Printed | Public | Wire/Connector | Description (this page) |
| --- | --- | --- | --- |
| F1 | 111 | Black-Green / J906-1 | Lower Right E.O.S. Switch |
| F2 | 112 | Blue-Violet / J905-1 | Lower Right Flipper Button |
| F3 | 113 | Black-Blue / J906-3 | Lower Left E.O.S. Switch |
| F4 | 114 | Blue-Gray / J905-2 | Lower Left Flipper Button |
| F5 | 115 | Black-Violet / J906-4 | Upper Right E.O.S. Switch |
| F6 | 116 | Black-Yellow / J905-3 | Upper Right Flipper Button |
| F7 | 117 | Black-Gray / J906-5 | Upper Left E.O.S. Switch |
| F8 | 118 | Black-Blue / J905-5 | Upper Left Flipper Button |

This page prints all eight Fliptronic II positions descriptively, matching the board's
generic wiring template. It is **not** by itself proof of physical fitment — see
`switch-locations.md`, where F5-F8 have no printed row at all (unlike Scared Stiff, where
F5-F8 print an explicit blank `---`/`Not Used` row). Combined with the Solenoid/Flasher
Table (`solenoid-flasher-wiring.md`) showing only two flipper-coil rows and the retained
known-working script never once referencing public switches 115-118, this machine has no
physical upper flippers.
