# Creature from the Black Lagoon — Switch Matrix wiring table

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 106, printed page 3-2,
"SWITCHES" / "SWITCH MATRIX CIRCUIT". Read directly from a 300 dpi `pdftoppm` render. Unlike Monster
Bash's or Scared Stiff's equivalent page, this table carries **no shaded-cell opto legend** — every
cell is plain text — so opto identity for this machine comes from `switch-locations.md`'s LED/Trans
part-number pairs, not from any shading cue on this page.

## Dedicated Grounded Switches (direct-grounded, not part of the 8x8 matrix)

| Addr | Wire | Connector | Board pin | Where used |
| --- | --- | --- | --- | --- |
| 1 | Orange-Brown | J205-1 | U18-11 (row: White-Brown J208-1) | Left Coin Chute |
| 2 | Orange-Red | J205-2 | U18-9 (White-Red J208-2) | Center Coin Chute |
| 3 | Orange-Black | J205-3 | U18-5 (White-Orange J208-3) | Right Coin Chute |
| 4 | Orange-Yellow | J205-4 | U18-7 (White-Yellow J208-4) | 4th Coin Chute |
| 5 | Orange-Green | J205-6 | U19-11 (White-Green J208-5) | Service Credits (normal) / Escape (test) |
| 6 | Orange-Blue | J205-7 | U19-9 (White-Blue J208-7) | Volume Down (normal) / Down (test) |
| 7 | Orange-Violet | J205-8 | U19-5 (White-Violet J208-8) | Volume Up (normal) / Up (test) |
| 8 | Orange-Gray | J205-9 | U19-7 (White-Gray J208-9) | Begin Test (normal) / Enter (test) |

## 8x8 switch matrix (column = drive wire/connector, row = return wire/connector; address = column*10+row)

Column headers: 1 Green-Brown/J206-1/U20-18, 2 Green-Red/J206-2/U20-17, 3 Green-Orange/J206-3/U20-16,
4 Green-Yellow/J206-4/U20-15, 5 Green-Black/J206-5/U20-14, 6 Green-Blue/J206-6/U20-13,
7 Green-Violet/J206-7/U20-12, 8 Green-Gray/J206-9/U20-11.

Row headers: 1 White-Brown/J208-1/U18-11, 2 White-Red/J208-2/U18-9, 3 White-Orange/J208-3/U18-5,
4 White-Yellow/J208-4/U18-7, 5 White-Green/J208-5/U19-11, 6 White-Blue/J208-7/U19-9,
7 White-Violet/J208-8/U19-5, 8 White-Gray/J208-9/U19-7.

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Not Used | 21 Slam Tilt | 31 Not Used | 41 Cola | 51 Left Out Lane | 61 Right Ramp Exit | 71 Not Used | 81 Not Used |
| 2 | 12 Not Used | 22 Coin Door | 32 Not Used | 42 Hot Dog | 52 Left Return Lane | 62 Left Ramp Exit | 72 Not Used | 82 Not Used |
| 3 | 13 Credit/Start Button | 23 Not Used | 33 Bottom Jet | 43 Popcorn | 53 Start Combo | 63 Center Lane Exit | 73 Not Used | 83 Not Used |
| 4 | 14 Plumb Bob Tilt | 24 Not Used | 34 Right Popper | 44 Ice Cream | 54 Right Out Lane | 64 Upper Ramp | 74 Not Used | 84 Not Used |
| 5 | 15 Top Left Rollover | 25 P of P-A-I-D | 35 Right Ramp Enter | 45 Left Jet | 55 Outhole | 65 Bowl | 75 Not Used | 85 Not Used |
| 6 | 16 Left Subway | 26 A of P-A-I-D | 36 Left Ramp Enter | 46 Right Jet | 56 Right Trough | 66 Shooter | 76 Not Used | 86 Not Used |
| 7 | 17 Center Subway | 27 I of P-A-I-D | 37 Lower Right Popper | 47 Left Slingshot | 57 Center Trough | 67 Not Used | 77 Not Used | 87 Not Used |
| 8 | 18 Center Shot | 28 D of P-A-I-D | 38 Ramp Up/Down | 48 Right Slingshot | 58 Left Trough | 68 Not Used | 78 Not Used | 88 Not Used |

This cross-checks the Switch Locations parts list (`switch-locations.md`) cell for cell with zero
disagreement: every "Not Used" cell here matches a "Not Used"/"---" row there, and every labeled cell
matches that page's "Where Used" text exactly (including the 53 = "Start Combo" naming discussed
below).

## Flipper Grounded Switches (F1-F8, direct-grounded circuit, public addresses 111-118)

| F# | Public addr | Wire | Connector | Printed function |
| --- | --- | --- | --- | --- |
| F1 | 111 | Black-Green | J906-1 | Right Flipper End of Stroke |
| F2 | 112 | Blue-Violet | J905-1 | Right Flipper Opto |
| F3 | 113 | Black-Blue | J906-3 | Left Flipper End of Stroke |
| F4 | 114 | Blue-Gray | J905-2 | Left Flipper Opto |
| F5 | 115 | Black-Violet | J906-4 | Upper Right Flipper End of Stroke |
| F6 | 116 | Black-Yellow | J905-3 | Upper Right Flipper Opto |
| F7 | 117 | Black-Gray | J906-5 | Upper Left Flipper End of Stroke |
| F8 | 118 | Black-Blue | J905-5 | Upper Left Flipper Opto |

`J2XX = CPU Board, J9XX = Fliptronic II Board` (printed caption under the table).

**This is the source of `conflict.upper-flipper-switches-unconfirmed-fitment`.** This page prints all
eight F1-F8 positions with real, distinct wire colors and Fliptronic-II-board connector pins, labeled
"Upper Right/Left Flipper End of Stroke/Opto" for F5-F8 with no "Not Used" marking anywhere on this
page. But `switch-locations.md` (the playfield-diagram parts list, a different page of the same
manual) lists only F1-F4 and does not mention F5-F8 at all, not even as a "Not Used" row, and the
Solenoid/Flasher Locations page (`solenoid-flasher-locations.md`) prints only two flipper coils
(Lower Left FL-15411, Lower Right FL-11629) with no upper-flipper coil circuit at any address —
consistent with pinned `cftbl.c`'s `FLIP_SOL(FLIP_L)` (lower coils only) but not conclusive about
whether the EOS/opto *switches* for the absent upper flippers were also left unpopulated. Two
same-manual pages disagree on whether F5-F8 are fitted hardware; this excerpt is the wiring-page half
of that disagreement.

## Opto-relevant switch-matrix circuit description (bottom of page)

The page's schematic block for the switch matrix describes the standard WPC comparator interface
(LS374SC column driver through a ULN-2803, LM339 row comparator) with no per-cell shading legend
anywhere on the page — unlike Monster Bash's and Scared Stiff's switch-matrix pages, which shade
opto cells "OPTO, TYPICALLY CLOSED". This is why this manual's opto identity has to come from the
Switch Locations parts list's LED/Trans construction pairs instead of a shading sweep of this page.
