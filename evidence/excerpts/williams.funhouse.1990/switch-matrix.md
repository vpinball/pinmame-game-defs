# FunHouse — Switches Matrix (printed page 2-39)

Source: `Funhouse_OPS.pdf`, PDF page 100 (printed "2-39"), rendered at 300 dpi and read directly
from the image (this manual's text layer scrambles multi-column tables under `pdftotext`).

## Connector fan-out (top of page, see `switch-matrix.webp`)

- `J206` column drive, pins 8-1: `GRN-GRY`=Column 8, `GRN-VIO`=Column 7, `GRN-BLU`=Column 6,
  `GRN-BLK`=Column 5, `GRN-YEL`=Column 4, `GRN-ORN`=Column 3, `GRN-RED`=Column 2, `GRN-BRN`=Column 1.
- `J208` row return, pins 1-8: `WHT-BRN`=Row 1, `WHT-RED`=Row 2, `WHT-ORN`=Row 3, `WHT-YEL`=Row 4,
  `WHT-GRN`=Row 5, `WHT-BLU`=Row 6, `WHT-VIO`=Row 7, `WHT-GRY`=Row 8.
- Each matrix intersection is drawn as a diode-and-switch symbol; the grid below is the same data
  in tabular form. No cell anywhere on this page is shaded — this manual identifies opto
  construction only by the printed word "(opto)"/"(Opto)" next to a switch's description on this
  page and on the switch-locations page (`switch-locations.md`), never by matrix-cell shading.

## FUNHOUSE Switch Matrix (full 8x8 grid plus dedicated column)

Legend: `White ──▷|──○ Green` (a diode-and-switch symbol) is drawn at every populated
intersection. Cells with no description are undrawn (no switch fitted).

| Dedicated Grounded Switches | Row | Col 1 Green-Brown | Col 2 Green-Red | Col 3 Green-Orange | Col 4 Green-Yellow | Col 5 Green-Black | Col 6 Green-Blue | Col 7 Green-Violet | Col 8 Green-Gray |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Orange-Brown (1) Left Coin Chute, D1 | White-Brown, 1 | Right Flipper `11` | Slam Tilt `21` | S-T-E-P "P" (Lower Right) `31` | Left Slingshot (Kicker) `41` | Dummy Jaw (Opto) `51` | Rt Inside Flipper Return Lane `61` | Rt Outside Flipper Return Lane `71` | — `81` |
| Orange-Red (2) Center Coin Chute, D2 | White-Red, 2 | Left Flipper `12` | Front Door `22` | Top Superdog Standup Target `32` | Left Flipper Return Lane `42` | Right Outlane `52` | Right Ballshooter `62` | Left Trough `72` | — `82` |
| Orange-Black (3) Right Coin Chute, D3 | White-Orange, 3 | Start Button `13` | Not Used `23` | Upper Left Gangway Rollunder `33` | Left Outlane `43` | Right Slingshot (Kicker) `53` | Right Trough `63` | Outhole `73` | — `83` |
| Orange-Yellow (4) 4th Coin Chute, D4 | White-Yellow, 4 | Plumb Bob Tilt `14` | Test Position, Always Closed `24` | Bottom Superdog Standup Target `34` | Wind Tunnel Hole `44` | S-T-E-P "T" (Upper Left) `54` | S-T-E-P "E" (Upper Center) `64` | Center Trough `74` | — `84` |
| Orange-Green (5) Normal: Service Credits / Test: Escape, D5 | White-Green, 5 | Steps Lights Frenzy `15` | Lock Mech Right `25` | Steps Track Lower `35` | Trap Door `45` | Steps Superdog (opto) `55` | Dummy Eject Hole `65` | Upper Right Loop Switch `75` | — `85` |
| Orange-Blue (6) Normal: Volume Down / Test: Down, D6 | White-Blue, 6 | Upper Ramp Switch `16` | Steps Lights Extra Ball `26` | Steps 500,000 `36` | Rudys Hideout Kickbig `46` | Ramp Entrance `56` | Upper Right Gangway Lane `66` | Trap Door Closed `76` | — `86` |
| Orange-Violet (7) Normal: Volume Up / Test: Up, D7 | White-Violet, 7 | S-T-E-P "S" (Lower Left) `17` | Lock Mech Center `27` | Center Superdog Standup Target `37` | Left Ballshooter `47` | Jet Bumper Lane `57` | Lower Right Drop Hole `67` | Upper Right Jet Bumper `77` | — `87` |
| Orange-Gray (8) Normal: Begin Test / Test: Enter, D8 | White-Gray, 8 | Upper Left Jet Bumper `18` | Lock Mech Left `28` | Steps Track Upper `38` | Ramp Exit Track `48` | Tunnel Kickout `58` | Lower Jet Bumper `68` | — `78` | — `88` |

Each dedicated grounded switch also prints a small parenthetical "Normal Function" / "Test
Function" pair for D5-D8, transcribed above; D1-D4 are plain coin chutes with no dual function.

Column 8 (address range 81-88) has no printed description in any cell — it is entirely unpopulated
on this physical machine, matching the switch-locations page's "78-88 Not Used" note.

Confirms every fh.c `#define` address against its printed matrix position; no disagreement found.
