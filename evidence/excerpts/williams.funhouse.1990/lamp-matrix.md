# FunHouse — Lamps Matrix (printed page 2-37)

Source: `Funhouse_OPS.pdf`, PDF page 98 (printed "2-37"), rendered at 300 dpi (and at 600 dpi for
the address-12 cell) and read directly from the image.

## Connector fan-out (top of page)

- `J137` column drive, pins 8-1: `YEL-GRY`=Column 8, `YEL-VIO`=Column 7, `YEL-BLU`=Column 6,
  `YEL-GRN`=Column 5, `YEL-BLK`=Column 4, `YEL-ORN`=Column 3, `YEL-RED`=Column 2, `YEL-BRN`=Column 1.
- `J133` row return, pins 1-9 (row 9 unused — only 8 rows exist): `RED-BRN`=Row 1, `RED-BLK`=Row 2,
  `RED-ORN`=Row 3, `RED-YEL`=Row 4, `RED-GRN`=Row 5, `RED-BLU`=Row 6, `RED-VIO`=Row 7, `RED-GRY`=Row 8.
- Legend: `Yellow (B+) ──((lamp))──▷|── Red` (bulb-and-diode symbol) at every populated cell. Every
  one of the 64 grid cells is populated (matches `lamp-locations.md`: no unused lamp positions).

## FUNHOUSE Lamp Matrix (full 8x8 grid, each cell's printed description)

Each printed row/column heading repeats the wire color already given above; only the cell text and
address are transcribed here (a small superscript self-test sequence number is also printed in
each cell but is not transcribed — it is a self-test playback order, not the public address, and
is not used by this definition).

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Red-Brown | Gangway 75,000 (Left) `11` | Clock 45 Minutes `21` | Clock 40 Minutes `31` | Clock 9 o'clock `41` | Lower Left Jet Bumper `51` | Left & Inside Rt Flipper Lanes (x 2) `61` | Magic Mirror Lights Extra Ball `71` | Million Plus `81` |
| 2 Red-Black | Gangway 100,000 `12` | Clock 8 o'clock `22` | Clock 35 Minutes `32` | Clock 7 o'clock `42` | Upper Left Jet Bumper `52` | S-T-E-P "S" `62` | Upper Right Jet Bumper `72` | Special Outlanes (x 2) `82` |
| 3 Red-Orange | Gangway 150,000 `13` | Clock 6 o'clock `23` | Clock 30 Minutes `33` | Clock 5 o'clock `43` | Superdog Lamp (x 2) `53` | Trap Door Bonus `63` | S-T-E-P "P" `73` | Trap Door Frenzy `83` |
| 4 Red-Yellow | Gangway 200,000 `14` | Clock 25 Minutes `24` | Clock 20 Minutes `34` | Clock 4 o'clock `44` | Steps Lights Frenzy `54` | Ramp Scores 250,000 `64` | Magic Mirror Lights Million `74` | Ramp "Steps" Lamp `84` |
| 5 Red-Green | Gangway 250,000 `15` | Clock 15 Minutes `25` | Clock 3 o'clock `35` | Clock 2 o'clock `45` | Steps Lights Extra Ball `55` | S-T-E-P "T" `65` | Magic Mirror Lights Jet Bumpers `75` | Magic Mirror Arrow `85` |
| 6 Red-Blue | Gangway Lights Extra Ball `16` | Clock 10 Minutes `26` | Clock 1 o'clock `36` | Clock 5 Minutes `46` | Steps 500,000 `56` | Upper Left Gangway Lane `66` | Magic Mirror Lights Superdog `76` | S-T-E-P "E" `86` |
| 7 Red-Violet | Shoot Again `17` | Clock 12 Minutes `27` | Clock 11 o'clock `37` | Clock 55 Minutes `47` | Ramp Overhead Lamp `57` | Extra Ball Lamp `67` | Magic Mirror Opens Gate `77` | Million `87` |
| 8 Red-Gray | Steps Open (Gate) `18` | Clock 0 Minutes `28` | Clock 50 Minutes `38` | Clock 10 o'clock `48` | Right Gangway Overhead Lamp `58` | Lock `68` | Magic Mirror Lights Quick Multi-ball `78` | Start Button (Cabinet) `88` |

## Cross-page disagreements found

- **Address 12**: this page reads "Gangway 100,000" (confirmed at 600 dpi: row 2, column 1,
  clearly "100, 000" not "10, 000"). The lamp-locations page (`lamp-locations.md`, printed 2-36)
  reads "Gangway 10,000" for the same address, also confirmed at 600 dpi. The two pages disagree
  by exactly one digit. Recorded as `conflict.gangway-lamp-12-value`, unresolved; the promoted
  definition's device label uses "Gangway 100,000" because it is the only value that fits the
  ladder implied by its neighbors (75,000 / ? / 150,000 / 200,000 / 250,000 / Extra Ball).
- **Address 51**: this page's cell reads "Lower Left Jet Bumper"; the lamp-locations page (and the
  solenoid/GI locations page, `solenoid-locations.md`) both read plain "Lower Jet Bumper" with no
  "Left" qualifier. FunHouse has exactly three jet bumpers (Left/Right/Lower per the solenoid
  table), not four, so "Left" here is read as an extra positional descriptor for the one lower
  bumper (which sits slightly left of table center) rather than a naming conflict; the shorter
  parts-list label is used as the primary device label per house convention (prefer the parts/
  locations list over the wiring/matrix page for labels).

## Explicit bulb-quantity markers

Only three addresses carry a printed "(x N)" quantity on this page: 61 "(x 2)", 82 "(x 2)", and
53 "(x 2)". Every other address has no printed quantity and is treated as a single bulb, matching
`lamp-locations.md`'s single-row-per-address listing.
