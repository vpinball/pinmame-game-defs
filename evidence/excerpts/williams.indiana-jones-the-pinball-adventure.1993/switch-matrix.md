# Indiana Jones — Switch Matrix

Transcribed from `Indiana_Jones_OPS.pdf`, PDF page 110, printed page 2-46, the Switch Matrix table.
`pdftotext -layout` on this scan produces text but the table cells are frequently scrambled/
duplicated by the underlying Paper Capture OCR layer (columns overlap, rows repeat), so this was
read from the rendered page, not trusted from the extracted text stream. This manual prints no
shaded-opto legend on the matrix page (unlike the WPC-95 manuals in this project); opto polarity for
this machine is established from the Switch Locations parts list instead (see `switch-locations.md`).

Header: column driver wires `Green-*` from `J207-n`/`U20-nn`; row return wires `White-*` from
`J209-n`/`U18-nn`/`U19-nn`; dedicated column `Orange-*` from `J205-n`/`U17-nn`/`U16-nn`; Fliptronic
column `Violet-White`/`Q11`/`J5-4`. `*Note: Used as switches other than flipper switches in this
game` (footnote on the Fliptronic block, F5-F8).

## Dedicated grounded switches (public 1-8)

| Public | Wire | Connector | Return | Function |
| --- | --- | --- | --- | --- |
| 1 (D1) | Orange-Brown | J205-1 | U17-5 | Left Coin Chute |
| 2 (D2) | Orange-Red | J205-2 | U17-7 | Center Coin Chute |
| 3 (D3) | Orange-Black | J205-3 | U17-11 | Right Coin Chute |
| 4 (D4) | Orange-Yellow | J205-4 | U17-9 | 4th Coin Chute |
| 5 (D5) | Orange-Green | J205-6 | U16-9 | Service Credits / Escape |
| 6 (D6) | Orange-Blue | J205-7 | U16-11 | Volume Down / Down |
| 7 (D7) | Orange-Violet | J205-8 | U16-7 | Volume Up / Up |
| 8 (D8) | Orange-Gray | J205-9 | U16-5 | Begin Test / Enter |

## Matrix switches

| Addr | Description | Addr | Description | Addr | Description | Addr | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Single Drop Top | 21 | Slam Tilt | 31 | Left Eject | 41 | Left Ramp Enter |
| 12 | Buy-in Button | 22 | Coin Door Closed | 32 | Exit Idol | 42 | Right Ramp Enter |
| 13 | Start Button | 23 | Ticket Opto | 33 | Left Slingshot | 43 | Top Idol Enter |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Gun Trigger | 44 | Right Popper |
| 15 | Left Outlane | 25 | (I)ndy Lane | 35 | Left Jet | 45 | Center Enter |
| 16 | Left Return Lane | 26 | I(n)dy Lane | 36 | Right Jet | 46 | Top Post |
| 17 | Right Return Lane | 27 | In(d)y Lane | 37 | Bottom Jet | 47 | Subway Lockup |
| 18 | Right Outlane Top | 28 | Ind(y) Lane | 38 | Center Standup | 48 | Right Slingshot |
| 51 | Advent(u)re Tgt. | 61 | (A)dventure Tgt. | 71 | Captive Ball Frt. | 81 | Trough 6 |
| 52 | Adventu(r)e Tgt. | 62 | A(d)venture Tgt. | 72 | Mini Top Hole | 82 | Trough 5 |
| 53 | Adventur(e) Tgt. | 63 | Ad(v)enture Tgt. | 73 | Mini Bottom Hole | 83 | Trough 4 |
| 54 | Left Loop Top | 64 | Captive Ball Back | 74 | Right Ramp Made | 84 | Trough 3 |
| 55 | Left Loop Bottom | 65 | Mini Top Left | 75 | Mini Top Right | 85 | Trough 2 |
| 56 | Right Loop Top | 66 | Mini Middle Top Left | 76 | Mini Middle Top Right | 86 | Trough 1 |
| 57 | Right Loop Bottom | 67 | Mini Middle Bottom Left | 77 | Mini Middle Bottom Right | 87 | Top Trough |
| 58 | Right Outlane Bottom | 68 | Mini Bottom Left | 78 | Mini Bottom Right | 88 | Shooter |

Column 9 (`Violet-White`, `Q11`, `J5-4`): 91 Wheel Position 1, 92 Wheel Position 2, 93 Wheel
Position 3, 94 Mini Playfield Left Limit, 95 Mini Playfield Right Limit. These printed "91-95"
numbers are the physical 9th-switch-column silkscreen used by the 3-sw Opto and Motor Opto Switch
PCB schematics, not the PinMAME public address — see `switch-locations.md`'s "Custom switch column"
section.

## Fliptronic column (F1-F8, public 111-118)

F1 Lower Right Flipper EOS, F2 Lower Right Flipper Cabinet (opto), F3 Lower Left Flipper EOS, F4
Lower Left Flipper Cabinet (opto), F5 Center Drop Bank Left, F6 Center Drop Bank Middle, F7 Center
Drop Bank Right, F8 Left Ramp Made — F5-F8 carry the footnote asterisk (repurposed, not flippers);
this game has no upper flippers (`FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L)` in `ijGameData`, no `FLIP_U`).
