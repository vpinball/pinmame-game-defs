# Fish Tales — Switch Matrix (wiring)

Transcribed from `Fish_Tales_OPS.pdf`, PDF page 98, printed page 3-4, the `Switch Matrix` table.
Read from the rendered page, not the OCR text layer. The accompanying crop (`switch-matrix.webp`) is
the same region.

**This page carries no shading and no opto/proximity legend of any kind.** Every one of the 64
switch positions uses one identical unshaded switch symbol. This is a genuine format difference from
some other WPC manuals in this project (for example Williams Monster Bash's switch matrix page,
which shades six columns "OPTO, TYPICALLY CLOSED"): Fish Tales' Switch Matrix page simply does not
use shading to mark construction at all. The crop was still produced, per instructions, to document
this absence as a visual fact rather than assert it from prose alone — a reader can look at the crop
and see for themselves that no cell differs from any other.

## Matrix drive columns

| Column | Wire | Connector | Drive IC |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-Yellow | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

## Matrix return rows

| Row | Wire | Connector | Return IC |
| --- | --- | --- | --- |
| 1 | White-Brown | J209 | 18-11 (printed without a "U" prefix, unlike rows 2-8) |
| 2 | White-Red | J209 | U18-9 |
| 3 | White-Orange | J209 | U18-5 |
| 4 | White-Yellow | J209 | U18-7 |
| 5 | White-Green | J209 | U19-11 |
| 6 | White-Blue | J209 | U19-9 |
| 7 | White-Violet | J209 | U19-5 |
| 8 | White-Gray | J209 | U19-7 |

All eight matrix return rows are wired through CPU Board connector J209 (unlike Monster Bash's
1998 manual, where rows split across two connectors J208/J209 — the WPC/WPC-95 platform difference
between Fliptronic-generation and WPC-95-generation CPU boards, not a transcription error).

## Address legend

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 31 | Cast | 51 | Left Jet | 71 | Not Used |
| 12 | Not Used | 32 | Left Boat Exit | 52 | Center Jet | 72 | Not Used |
| 13 | Start Button | 33 | Right Boat Exit | 53 | Right Jet | 73 | Not Used |
| 14 | Plumb Bob Tilt | 34 | Spinner | 54 | Rt. Stand-up Tgt 1 | 74 | Not Used |
| 15 | Outhole | 35 | Reel Entry | 55 | Rt. Stand-up Tgt 2 | 75 | Not Used |
| 16 | Trough 1 | 36 | Catapult | 56 | Ball Shooter | 76 | Not Used |
| 17 | Trough 2 | 37 | Reel 1 | 57 | Left Sling | 77 | Not Used |
| 18 | Trough 3 | 38 | Reel 2 | 58 | Right Sling | 78 | Not Used |
| 21 | Slam Tilt | 41 | Captive Ball | 61 | Extra Ball | 81 | Not Used |
| 22 | Coin Door Closed | 42 | Right Boat Entry | 62 | Top Right Loop | 82 | Not Used |
| 23 | Ticket Opto | 43 | Left Boat Entry | 63 | Top Eject Hole | 83 | Not Used |
| 24 | Always Closed | 44 | Lie (E) | 64 | Top Left Loop | 84 | Not Used |
| 25 | Left Outlane | 45 | Lie (I) | 65 | Right Return | 85 | Not Used |
| 26 | Left Return Lane | 46 | Lie (L) | 66 | Right Outlane | 86 | Not Used |
| 27 | Lt. Stand-up Tgt 1 | 47 | Ball Popper | 67 | Not Used | 87 | Not Used |
| 28 | Lt. Stand-up Tgt 2 | 48 | Drop Target | 68 | Not Used | 88 | Not Used |

This legend agrees address-for-address with the Switch Locations parts list
(`switch-locations.md`) on which positions are fitted; the only wording difference between the two
pages is that this legend spells the three "Lie" lamps' letters plainly (44=Lie(E), 45=Lie(I),
46=Lie(L)) while the parts list nests the letter inside a fixed "L I E" frame at each address
(44=Letter(L)IE, 45=Letter L(I)E, 46=Letter Ll(E)). Both pages agree on which physical lane each
address is.

## Dedicated switches (printed 3-6, PDF page 100)

The eight dedicated grounded switches are documented on a separate printed page (3-6) from the
64-position matrix (3-4), unlike some other WPC manuals that print both on one sheet. Standard WPC
coin-door dedicated-switch harness, CPU Board J205 through Coin Door Interface Board J1/J3:

| Addr | Wire | CPU J205 | CDI J1 | CDI J3 | Label |
| --- | --- | --- | --- | --- | --- |
| D1 | Orange-Brown | 1 | 14 | 4 | Left Coin Chute |
| D2 | Orange-Red | 2 | 13 | 5 | Center Coin Chute |
| D3 | Orange-Black | 3 | 12 | 6 | Right Coin Chute |
| D4 | Orange-Yellow | 4 | 17 | *(blank)* | Forth [sic] Coin Chute |
| D5 | Orange-Green | 6 | 11 | 7 | Service Credits (Normal) / Escape (Test) |
| D6 | Orange-Blue | 7 | 10 | 8 | Volume Down (Normal) / Down (Test) |
| D7 | Orange-Violet | 8 | 9 | 9 | Volume Up (Normal) / Up (Test) |
| D8 | Orange-Gray | 9 | 8 | 11 | Begin Test (Normal) / Enter (Test) |
| — | Black | 11 | 15 | 3 | Ground |

D4's Coin Door Interface J3 pin is blank on the printed diagram, unlike D1-D3; transcribed as
printed.
