# High Speed — Switch-Matrix Table

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 34 (printed page 26, inside the
Test/Diagnostic Procedures section) and from the identical unpaginated quick-reference foldout bound
at PDF page 4. Read from 300 dpi `pdftoppm` renders; the Acrobat Paper-Capture OCR layer on this scan
is usable for cross-checking but was not trusted on its own. The accompanying crop is the same
region, rendered grayscale.

Public address = `(column - 1) * 8 + row` — System 11 sequential column-major numbering, not WPC's
column-times-ten notation. The printed matrix cells already carry that number in the lower-right
corner of each cell, so the printed number and the public address are the same figure here.

**There is no opto legend, no shaded cell, and no "typically closed" note anywhere on this page.**
Both copies of the table (PDF 4 and PDF 34) print all 64 cells with plain, unshaded borders and the
page carries no legend box of any kind — a genuine difference from the late-Williams WPC manuals this
project has mostly read, and consistent with a 1986 machine whose Switches parts list (see
`switch-locations.md`) contains no opto part number and no blank-switch-part row. The crop exists so
a reader can confirm that negative claim directly instead of trusting this transcription for it.

## Column and row wiring, verbatim

Column headers (drive): 1 = Q45 GRN-BRN 1J8-1; 2 = Q49 GRN-RED 1J8-2; 3 = Q44 GRN-ORN 1J8-3;
4 = Q48 GRN-YEL 1J8-4; 5 = Q43 GRN-BLK 1J8-5; 6 = Q47 GRN-BLU 1J8-7; 7 = Q42 GRN-VIO 1J8-8;
8 = Q46 GRN-GRY 1J8-9. (1J8-6 is skipped.)

Row headers (return): 1 = WHT-BRN 1J10-9; 2 = WHT-RED 1J10-8; 3 = WHT-ORN 1J10-7;
4 = WHT-YEL 1J10-6; 5 = WHT-GRN 1J10-5; 6 = WHT-BLU 1J10-3; 7 = WHT-VIO 1J10-2;
8 = WHT-GRY 1J10-1. (1J10-4 is skipped.)

## The full 8 x 8 matrix, verbatim cell text

| Row \ Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Plumb Bob Tilt (1) | Outhole (9) | Upper Left Stoplight Bank - Red Target (17) | Standup Target Arrow #1 (25) | Upper Left Jet Bumper (33) | Playfield Tilt (41) | Left Kicker (49) | Not Used (57) |
| 2 | Ball Roll Tilt (2) | Ball Trough #3 (Upper Left) (10) | Upper Left Stoplight Bank - Yel Target (18) | Standup Target Arrow #2 (26) | Lower Left Jet Bumper (34) | Left Ramp (42) | Right Kicker (50) | Not Used (58) |
| 3 | Credit Button (3) | Ball Trough #2 (Center) (11) | Upper Left Stoplight Bank - Grn Target (19) | Standup Target Arrow #3 (27) | Right Jet Bumper (35) | Right Ramp (43) | Left Star Rollover (51) | Not Used (59) |
| 4 | Right Coin Chute (4) | Ball Trough #1 (Lower Right) (12) | Left Flipper Return Lane (20) | Standup Target Arrow #4 (28) | Ball Shooter (36) | Left Spinner (44) | Right Star Rollover (52) | Not Used (60) |
| 5 | Center Coin Chute (5) | Lower Left Stoplight Bank - Red Target (13) | Right Flipper Return Lane (21) | Standup Target Arrow #5 (29) | Left Flipper Engine Revving (EOS) (37) | Center Spinner (45) | Not Used (53) | Not Used (61) |
| 6 | Left Coin Chute (6) | Lower Left Stoplight Bank - Yel Target (14) | Right Stoplight Bank - Red Target (22) | Standup Target Arrow #6 (30) | Right Flipper Engine Revving (EOS) (38) | Right Spinner (46) | Not Used (54) | Not Used (62) |
| 7 | Slam Tilt (7) | Lower Left Stoplight Bank - Grn Target (15) | Right Stoplight Bank - Yellow Target (23) | Left Outlane (31) | Upper Left Hideout (39) | Upper Right Hideout (47) | Not Used (55) | Not Used (63) |
| 8 | High-Score Reset (8) | Eject Hole (16) | Right Stoplight Bank - Green Target (24) | Right Outlane (32) | Lower Left Hideout (40) | Lower Right Hideout (48) | Not Used (56) | Not Used (64) |

Twelve positions (53-64) are printed "Not Used". Every other cell carries a device name; no cell is
blank.

## The "(EOS)" parenthetical on switches 37 and 38 — a disagreement inside this manual

This page prints 37/38 as "Left/Right Flipper Engine Revving **(EOS)**". The Switches parts list
(printed page 32) prints the same two addresses as "Left/Right Flipper **Lane Change** (Engine Revs)"
with part numbers `SW-1A-150-1` and `SW-1A-150`, and the C-9952-R Flipper Assemblies parts list
(printed page 35) identifies `SW-1A-150` as item **2b, "Lane Change Switch"** — a physically
different part from that same assembly's item **2a, "End of Stroke (EOS) Switch", `03-7811`**, which
carries no matrix address anywhere in this manual. The parts-list identification is therefore taken
as the label of record and this page's "(EOS)" parenthetical is recorded as a manual-internal error;
see `boards-and-assemblies.md` for the full flipper-assembly transcription.

## Switch-number range stated in the surrounding text (printed page 25)

> For HIGH SPEED, switch numbers can range from 01 through 52. Refer to the Switch-Matrix Table for
> switch numbers and wiring information. CPU Board connections at jacks 1J8 (columns) and 1J10 (rows)
> are also listed in the table.

## Amendment affecting this page's surrounding text

The Amendments sheet (Amendment Page 1, dated 040286) corrects the jumper example printed under
SWITCH TESTS paragraph 3 on printed page 27:

> To obtain the switch 09 indication, connect the test jumper between 1J10-9 and 1J8-2, not 1J10-1.
> (A jumper between 1J10-1 and 1J8-2 actually gives an indication of switch 16.)

Both figures in that correction agree with the matrix above: 1J8-2 is column 2, 1J10-9 is row 1
(switch 9, Outhole) and 1J10-1 is row 8 (switch 16, Eject Hole).
