# The Machine: Bride of Pinbot — Switch Matrix (printed page 2-40)

Source: `the_machine_operations_manual.pdf` (Williams part 16-50002-101, March 1991), PDF page 108,
printed "2-40". Read from the page rendered at its native 300 dpi, with a 600 dpi render of the
connector label; the OCR text layer doubles every glyph and was used only to locate the page.

## Connector fan-out (top of page)

- Column drive connector, printed label `J20` (a detached `6` is printed to the left of pin 8;
  the label is transcribed exactly as printed), pins 8-1: `GRN-GRY` Column 8, `GRN-VIO` Column 7,
  `GRN-BLU` Column 6, `GRN-BLK` Column 5, `GRN-YEL` Column 4, `GRN-ORN` Column 3, `GRN-RED` Column 2,
  `GRN-BRN` Column 1.
- Row return connector `J208`, pins 1-8: `WHT-BRN` Row 1, `WHT-RED` Row 2, `WHT-ORN` Row 3,
  `WHT-YEL` Row 4, `WHT-GRN` Row 5, `WHT-BLU` Row 6, `WHT-VIO` Row 7, `WHT-GRY` Row 8.
- Every intersection 11-88 is drawn with the same diode-and-switch symbol. Legend at the table
  header: `White ──▷|──○ ○── Green`. No cell on this page is shaded and no opto legend is printed.

## THE MACHINE Switch Matrix

| Dedicated Grounded Switches | Row | Col 1 Green-Brown | Col 2 Green-Red | Col 3 Green-Orange | Col 4 Green-Yellow | Col 5 Green-Black | Col 6 Green-Blue | Col 7 Green-Violet | Col 8 Green-Gray |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Orange-Brown (1) Left Coin Chute, D1 | 1 White-Brown | Right Flipper `11` | Slam Tilt `21` | Skill Shot 50K `31` | Right Ramp Made `41` | Spinner `51` | Not Used `61` | Wireform Top `71` | (blank) `81` |
| Orange-Red (2) Center Coin Chute, D2 | 2 White-Red | Left Flipper `12` | Coin Door Closed `22` | Skill Shot 75K `32` | Not Used `42` | Shooter `52` | Not Used `62` | Wireform Bottom `72` | (blank) `82` |
| Orange-Black (3) Right Coin Chute, D3 | 3 White-Orange | Start Button `13` | Ticket Opto `23` | Skill Shot 100K `33` | Left Loop `43` | Upper Right Jet Bumper `53` | Head Left Eye `63` | Enter Mini Playfield `73` | (blank) `83` |
| Orange-Yellow (4) 4th Coin Chute, D4 | 4 White-Yellow | Plumb Bob Tilt `14` | Always Closed `24` | Skill Shot 200K `34` | Right Loop Top `44` | Upper Left Jet Bumper `54` | Head Right Eye `64` | Mini Exit Left `74` | (blank) `84` |
| Orange-Green (5) Normal Function: Service Credits / Test Function: Escape, D5 | 5 White-Green | Left Outlane `15` | Right Trough `25` | Skill Shot 25K `35` | Right Loop Bottom `45` | Lower Jet Bumper `55` | Head Mouth `65` | Mini Exit Right `75` | (blank) `85` |
| Orange-Blue (6) Normal Function: Volume Down / Test Function: Down, D6 | 6 White-Blue | Left FlipperL ane `16` | Center Trough `26` | Right Top Standup `36` | Under Playfield Kickback `46` | Jet Bumper Sling `56` | Not Used `66` | Left Ramp Enter `76` | (blank) `86` |
| Orange-Violet (7) Normal Function: Volume Up / Test Function: Up, D7 | 7 White-Violet | Right Flipper Lane `17` | Left Trough `27` | Right Bottom Standup `37` | Enter Head `47` | Left Slingshot `57` | Face Position `67` | Right Ramp Enter `77` | (blank) `87` |
| Orange-Gray (8) Normal Function: Begin Test / Test Function: Enter, D8 | 8 White-Gray | Right Outlane `18` | Left Standup `28` | Outhole `38` | Not Used `48` | Right Slingshot `58` | Not Used `68` | Not Used `78` | (blank) `88` |

Transcription notes:

- Cell 16 is printed with a line break inside the word, `Left FlipperL` / `ane`; it is kept
  literally above and read as "Left Flipper Lane", the wording the switch-locations page uses.
- Column 8 (81-88) carries an address number in every cell but no description at all. That is
  distinct from the explicit `Not Used` printed at 42, 48, 61, 62, 66, 68, and 78: the blank cells
  are recorded as blank, not completed as "Not Used".
- `Ticket Opto` (23) is the only switch name on this page that names optical construction; the
  switch-locations page prints `Not Used` in its part-number column for the same address.
- The dedicated grounded switch column prints `(1)`-`(8)` beside each wire colour and `D1`-`D8`
  at the bottom right of each cell.
