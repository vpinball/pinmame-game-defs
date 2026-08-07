# Bram Stoker's Dracula — Lamp Matrix and Lamp Locations

Transcribed from `Dracula_Bram_Stoker_OPS.pdf`, PDF page 114 (printed 3-2, Lamp Matrix
wiring table) and PDF page 107 (printed 2-44, Lamp Locations parts list and playfield
diagram). Rendered at 300 dpi grayscale with `pdftoppm`.

## Lamp Matrix (page 114, printed 3-2)

Column wiring: 1 Yellow-Brown J137-1/Q98, 2 Yellow-Red J137-2/Q97, 3 Yellow-Orange
J137-3/Q96, 4 Yellow-Black J137-4/Q95, 5 Yellow-Green J137-5/Q94, 6 Yellow-Blue
J137-6/Q93, 7 Yellow-Violet J137-7/Q92, 8 Yellow-Gray J137-9/Q91. Row wiring: 1 Red-Brown
J133-1/Q90, 2 Red-Black J133-2/Q89, 3 Red-Orange J133-4/Q88, 4 Red-Yellow J133-5/Q87, 5
Red-Green J133-6/Q86, 6 Red-Blue J133-7/Q85, 7 Red-Violet J133-8/Q84, 8 Red-Gray
J133-9/Q83.

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Not Used | 21 Coffin Lock 1 | 31 R. Lane: Video "V" | 41 Right Return | 51 Coffin Lamp 1 | 61 Left Skill 100K | 71 Dracula "C" | 81 Rats Mode |
| 2 | 12 Not Used | 22 Coffin Lock 2 | 32 R. Lane: Video "I" | 42 Right Drain | 52 Coffin Lamp 2 | 62 M. Skill 1 Million | 72 Dracula "L" | 82 Dracula "A" |
| 3 | 13 Not Used | 23 Dracula "A" | 33 R. Lane: Video "D" | 43 Coffin Multiball | 53 Magnet | 63 R. Skill 100K | 73 Left 3-bank Top | 83 T.L. Hole: Mystery |
| 4 | 14 Not Used | 24 R. Ramp: 0.5 Million | 34 R. Lane: Video "E" | 44 Playfield 2X | 54 Shoot Again | 64 Top 3-lane Left | 74 Left 3-bank Middle | 84 T.L. Hole: Carriage |
| 5 | 15 Not Used | 25 R. Ramp: 1 Million | 35 R. Lane: Video "O" | 45 Castle Multiball | 55 Love Never Dies | 65 Top 3-lane Middle | 75 Left 3-bank Bottom | 85 T.L. Hole: Ex-ball |
| 6 | 16 R. Ramp: Lock | 26 R. Ramp: 2.5 Million | 36 Dracula "R" | 46 Playfield 3X | 56 Coffin Lamp 3 | 66 Top 3-lane Right | 76 Middle 3-bank Left | 86 T.L. Hole: Jackpot |
| 7 | 17 Dracula Face | 27 R. Ramp: Double | 37 Left Drain | 47 Mist Multiball | 57 L. Ramp Lock | 67 Dracula "U" | 77 Middle 3-bank Middle | 87 Launch Ball |
| 8 | 18 R. Ramp: 2 Million | 28 R. Ramp: 1.5 Million | 38 Left Return | 48 Dracula "D" | 58 L. Ramp Diverted | 68 Jet Insert | 78 Middle 3-bank Right | 88 Game Start |

(Column/row layout confirmed directly against the Lamp Locations parts list below; every
label independently agrees between the two pages except that this wiring page spells the
"Dracula" chase inserts as the full word plus a quoted letter, e.g. `Dracula "C"`, while
the parts list below uses a parenthesised letter within the word, e.g. `Dra(c)ula` — the
same seven inserts either way.)

**Internal manual disagreement:** this page prints address 63 as "R. Skill **100K**",
while the Lamp Locations parts list (page 107, printed 2-44) prints the same address as
"R Skill **500K**". Both are transcribed verbatim; neither page is preferred over the
other since this is a backbox scoring-legend value (not a wiring, polarity, or placement
fact) and the device already carries a controlled `cabinet_or_service` spatial record
regardless of which value is correct.

## Lamp Locations (page 107, printed 2-44)

The diagram draws a separate "A-16399 Back Panel Assy." box **above** the main playfield
outline containing exactly four lamps: 58, 61, 62, 63. These do not appear anywhere on
the main playfield diagram below that box.

| Addr | Bulb | Description | Location |
| --- | --- | --- | --- |
| 11-15 | — | Not Used | — |
| 16 | #44 | R. Ramp: Lock | playfield |
| 17 | #44 | Dracula Face | playfield |
| 18 | #555 | R. Ramp: 2 Mil. | playfield |
| 21 | #44 | Coffin Lock 1 | playfield |
| 22 | #44 | Coffin Lock 2 | playfield |
| 23 | #555 | Dracul(a) | playfield |
| 24 | #555 | R. Ramp: .5 Million | playfield |
| 25 | #555 | R. Ramp: 1 Million | playfield |
| 26 | #555 | R. Ramp: 2.5 Million | playfield |
| 27 | #555 | R. Ramp: Double | playfield |
| 28 | #555 | R. Ramp: 1.5 Million | playfield |
| 31 | #555 | R. Lane: (V)ideo | playfield |
| 32 | #555 | R. Lane: V(i)deo | playfield |
| 33 | #555 | R. Lane: Vi(d)eo | playfield |
| 34 | #555 | R. Lane: Vid(e)o | playfield |
| 35 | #555 | R. Lane: Vide(o) | playfield |
| 36 | #555 | D(r)acula | playfield |
| 37 | #555 | Left Drain | playfield |
| 38 | #555 | Left Return | playfield |
| 41 | #555 | Right Return | playfield |
| 42 | #555 | Right Drain | playfield |
| 43 | #555 | Coffin Multiball | playfield |
| 44 | #555 | Playfield 2X | playfield |
| 45 | #555 | Castle Multiball | playfield |
| 46 | #555 | Playfield 3X | playfield |
| 47 | #555 | Mist Multiball | playfield |
| 48 | #555 | (D)racula | playfield |
| 51 | #555 | Coffin Lamp 1 | playfield |
| 52 | #555 | Coffin Lamp 2 | playfield |
| 53 | #44 | Magnet | playfield (no VPX object — see below) |
| 54 | #44 | Shoot Again | playfield |
| 55 | #44 | Love Never Dies | playfield |
| 56 | #555 | Coffin Lamp 3 | playfield |
| 57 | #555 | L. Ramp Lock | playfield |
| **58** | **#555** | **L. Ramp Diverted** | **Back Panel Assy. (backbox)** |
| **61** | **#555** | **L. Skill 100K** | **Back Panel Assy. (backbox)** |
| **62** | **#555** | **M. Skill 1 Mil.** | **Back Panel Assy. (backbox)** |
| **63** | **#555** | **R. Skill 500K** | **Back Panel Assy. (backbox)** |
| 64 | #555 | T. 3-lane: Left | playfield |
| 65 | #555 | T. 3-lane: Middle | playfield |
| 66 | #555 | T. 3-lane: Right | playfield |
| 67 | #555 | Drac(u)la | playfield |
| 68 | #44 | Jet Insert | playfield |
| 71 | #555 | Dra(c)ula | playfield |
| 72 | #555 | Dracu(l)a | playfield |
| 73 | #555 | Left 3-bank Top | playfield |
| 74 | #555 | Left 3-bank Middle | playfield |
| 75 | #555 | Left 3-bank Bottom | playfield |
| 76 | #555 | M. 3-bank Left | playfield |
| 77 | #555 | M. 3-bank Middle | playfield |
| 78 | #555 | M. 3-bank Right | playfield |
| 81 | #44 | Rats Mode | playfield |
| 82 | #555 | Dr(a)cula | playfield |
| 83 | #555 | T.L. Hole: Mystery | playfield |
| 84 | #555 | T.L. Hole: Carriage | playfield |
| 85 | #555 | T.L. Hole: Ex. Ball | playfield |
| 86 | #555 | T.L. Hole: Jackpot | playfield |
| 87 | (none printed) | Launch Ball | cabinet button |
| 88 | (none printed) | Game Start | cabinet button |

## Resolved facts

- **Lamps 58, 61, 62, 63** are drawn only inside the "Back Panel Assy." box, never on the
  main playfield diagram. The retained VPX table corroborates this independently: its
  `Light.l58`/`Light.L61`/`Light.L62`/`Light.L63` objects all normalize to y &lt; 0.011,
  i.e. sitting right at the playfield's rear edge rather than at a genuine mid-playfield
  position — consistent with a table author placing translite/backbox lamps near the top
  edge of the play surface for lack of anywhere better to put them. All four take a
  controlled `cabinet_or_service` spatial record.
- **Lamp 53 (Magnet, #44)** has no matching `Light` object anywhere in the retained
  extraction and is never referenced in `script.vbs`. It is a genuine bulb per this page
  but has no resolvable spatial evidence; its `spatial` key is omitted rather than a
  coordinate being invented.
- The seven Dracula name-chase lamps (23, 36, 48, 67, 71, 72, 82) spell D-R-A-C-U-L-A in
  address order 48→36→23→71→67→72→82. The five R. Lane "Video" lamps
  (31-35) spell VIDEO in already-ascending address order.
