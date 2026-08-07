# Judge Dredd — Lamp Matrix

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF page 108, printed page 2-40, the LAMP MATRIX
table. Produced by rendering the retained PDF at 300 dpi with `pdftoppm` and reading the table
directly. Legend printed under the table: `J1XX = Power Driver Board`. Header note: `Yellow (B+) —
(lamp) —>|— Red`.

## Column and row wiring

Columns (drive): 1 Yellow-Brown J137-1/Q98, 2 Yellow-Red J137-2/Q97, 3 Yellow-Orange J137-3/Q96,
4 Yellow-Black J137-4/Q95, 5 Yellow-Green J137-5/Q94, 6 Yellow-Blue J137-6/Q93, 7 Yellow-Violet
J138-7/Q92, 8 Yellow-Gray J138-9/Q91.

Rows (return): 1 Red-Brown J133-1/Q90, 2 Red-Black J133-2/Q89, 3 Red-Orange J133-4/Q88, 4 Red-Yellow
J133-5/Q87, 5 Red-Green J133-6/Q86, 6 Red-Blue J133-7/Q85, 7 Red-Violet J133-8/Q84, 8 Red-Gray
J133-9/Q83.

Columns 1-6 leave the Power Driver Board on J137 and columns 7-8 on J138; the row returns are all on
J133, and J133-3 is skipped (row 3 is J133-4).

## Matrix (column = tens digit, row = units digit)

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Perp 1 (White) | 21 | Perp 4 (White) | 31 | Perp 3 (White) | 41 | Crime Level 4 (White) |
| 12 | Perp 1 (Red) | 22 | Perp 4 (Red) | 32 | Perp 3 (Red) | 42 | Crime Level 3 (Red) |
| 13 | Perp 1 (Yellow) | 23 | Perp 4 (Yellow) | 33 | Perp 3 (Yellow) | 43 | Crime Level 2 (Yellow) |
| 14 | Perp 1 (Green) | 24 | Perp 4 (Green) | 34 | Perp 3 (Green) | 44 | Crime Level 1 (Green) |
| 15 | Perp 2 (White) | 25 | Perp 5 (White) | 35 | Lock 1 | 45 | Meltdown |
| 16 | Perp 2 (Red) | 26 | Perp 5 (Red) | 36 | Lock 2 | 46 | Impersonator |
| 17 | Perp 2 (Yellow) | 27 | Perp 5 (Yellow) | 37 | Lock 3 | 47 | Battle Tank |
| 18 | Perp 2 (Green) | 28 | Perp 5 (Green) | 38 | Buy-In | 48 | Stop Meltdown |

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | Stakeout | 61 | Right Extra Ball | 71 | Drop Target "J" | 81 | Award Stakeout |
| 52 | Safecracker | 62 | Right Start Feature | 72 | Drop Target "U" | 82 | Blackout Jackpot |
| 53 | Pursuit | 63 | Tank Center | 73 | Drop Target "D" | 83 | Drain Shield |
| 54 | Ultimate Challenge | 64 | Award Sniper | 74 | Drop Target "G" | 84 | Judge Again |
| 55 | Manhunt | 65 | Air Raid | 75 | Drop Target "E" | 85 | Advance Crime Level |
| 56 | Blackout | 66 | Left Center Feature | 76 | Award Safecracker | 86 | Tank Right |
| 57 | Sniper | 67 | Tank Left | 77 | Multi-ball Jackpot | 87 | Super Game |
| 58 | Pick A Prize | 68 | Mystery | 78 | Award Bad Impersonator | 88 | Start Button |

All 64 matrix positions carry a label; this machine has no "Not Used" lamp position. Three of the 64
are cabinet button lamps rather than playfield inserts — 38 Buy-In, 87 Super Game, 88 Start Button —
which the Lamp Locations parts list confirms by giving them `20-9663-*` button assemblies and a `---`
bulb number.

Label differences worth noting against the Lamp Locations parts list on 2-41, which is the
authoritative label source: this page prints 61 as `Right Extra Ball` where the parts list prints
`Extra Ball (2)`, and prints no bulb quantity anywhere.
