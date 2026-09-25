# Williams Firepower (game 497) — Figure 4, Playfield Switch Locations and Switch Chart

Source: `Williams_1980_Firepower_Instruction_Booklet.pdf` (IPDB 856, Instruction Booklet
16P-497-103, January 1980), PDF page 10, printed page 10. Transcribed by hand from a 200 dpi render
(`pdftoppm -r 200`, 1118x1800 px); the pixel positions below refer to that render.

Heading, verbatim: `Figure 4. Playfield Switch Locations and Switch Chart`.

## Switch chart, verbatim

`SWITCH` / `NO. FUNCTION (SCORE)`

| NO. | FUNCTION (SCORE) |
| --- | --- |
| 01 | Plumb Bob Tilt |
| 02 | Ball Roll Tilt |
| 03 | Credit Button |
| 04 | Right Coin Switch |
| 05 | Center Coin Switch |
| 06 | Left Coin Switch |
| 07 | Slam Tilt |
| 08 | High Score Reset |
| 09 | Outhole |
| 10 | Left Outside Rollover (1000) |
| 11 | Left Inside Rollover (1000/3000) |
| 12 | Left Kicker (10) |
| 13 | Left Eject Hole (1000/10,000) |
| 14 | Upper Middle Left Standup (50) |
| 15 | Spinner (100/1000) |
| 16 | Top Left Standup (50) |
| 17 | "1" Target (1000) |
| 18 | "2" Target (1000) |
| 19 | "3" Target (1000) |
| 20 | Not Used |
| 21 | "4" Target (1000) |
| 22 | "5" Target (1000) |
| 23 | "6" Target (1000) |
| 24 | Not Used |
| 25 | Bottom Left Jet Bumper (100/1000) |
| 26 | Top Left Jet Bumper (100/1000) |
| 27 | Top Right Jet Cumper (100/1000) |
| 28 | Bottom Right Jet Bumper (100/1000) |
| 29 | Top Center Target (1000) |
| 30 | Right Eject Hole (1000/10,000) |
| 31 | Upper Top Right Standup (50) |
| 32 | "F" Rollover (1000) |
| 33 | "I" Rollover (1000) |
| 34 | "R" Rollover (1000) |
| 35 | "E" Rollover (1000) |
| 36 | Upper Right Eject Hole (1000/10,000) |
| 37 | Lower Top Right Standup (50) |
| 38 | Middle Right Standup (50) |
| 39 | Top "POWER" Target (1000) |
| 40 | Middle "POWER" Target (1000) |
| 41 | Bottom "POWER" Target (1000) |
| 42 | Right Kicker (10) |
| 43 | Right Inside Rollover (1000/3000) |
| 44 | Right Outside Rollover (1000) |
| 45 | Right Flipper *LANE CHANGE* Switch (the two words in bold italic; the entry wraps onto a second line) |
| 46 | Ball Shooter |
| 47 | Playfield Tilt |
| 48 | Lower Right Standup (50) |
| 49 | Center Middle Left Standup (50) |
| 50 | Lower Middle Left Standup (50) |
| 51 | Left Ball Ramp |
| 52 | Not Used |
| 53 | Left Eject Rollover (1000) |
| 54 | Right Eject Rollover (1000) |
| 55 | Not Used |
| 56 | Not Used |
| 57 | Right Ball Ramp |
| 58 | Center Ball Ramp |

`Note: Second score is lit or flashing value.`

The chart stops at 58; switches 59-64 are not listed here and are printed `NOT USED` in Figure 5.
Entry 27 is literally printed `Top Right Jet Cumper`, a typing error for Bumper; Figure 5 prints
`TOP RIGHT JET BUMPER`.

## Drawing

The drawing is a schematic line plan of the playfield, not a scale drawing. Every number is placed
beside the device it identifies. Numbers inside a dashed circle mark devices that are not visible
from above: 09 (outhole, below the apron), 12 and 42 (the kicker switches behind the slingshot
rubbers), 45 (lane-change switch, below the playfield between the flippers, nearer the right
flipper), 47 (playfield tilt, below the lower left playfield), and the dashed oval holding `51 58
57` side by side below the apron to the left of the shooter lane (the ball ramp). Number 46 sits
at the foot of the shooter lane.

Identity reading, top to bottom (callout -> device the callout sits beside):

| Callout | Device drawn beside it |
| --- | --- |
| 32, 33, 34, 35 | the four top rollover lanes, left to right, with 29 (the top centre target) drawn between 33 and 34 |
| 36 | the upper right eject hole in the top right corner |
| 16 | the top left rubber, below lane 32 |
| 26, 27 | the two upper jet bumpers, 26 left and 27 right |
| 25, 28 | the two lower jet bumpers, 25 left and 28 right |
| 15 | the spinner on the left orbit |
| 31, 37 | the right rubber pair below the upper right eject hole, 31 above 37 |
| 30 | the right eject hole |
| 54 | the star rollover in the right eject lane |
| 14, 49, 50 | the left rail rubber band, top to bottom; 49 is level with the left eject hole |
| 13 | the left eject hole in the left rail |
| 53 | the star rollover in the left eject lane |
| 17, 18, 19 | the left target bank, left to right |
| 21, 22, 23 | the right target bank, left to right |
| 38 | the right rubber below the right orbit exit |
| 39, 40, 41 | the three-target POWER bank on the right side, top to bottom |
| 48 | the right rubber below the POWER bank |
| 11, 10 | the left inlane and left outlane rollovers |
| 43, 44 | the right inlane and right outlane rollovers |
| 12, 42 | the left and right kicker switches (dashed) |
| 45 | lane-change switch (dashed) |
| 47 | playfield tilt (dashed) |
| 09 | outhole (dashed) |
| 51, 58, 57 | the ball ramp below the apron (dashed oval), left to right |
| 46 | ball shooter |

## Registration against the retained table

Pixel centres of ten device symbols in the 200 dpi render were read against a 10 px grid and
paired with the centres of the matching objects in the retained `Firepower (Williams 1980).vpx`
(bounds 952 x 1974):

| Control point | Drawing px | Table units |
| --- | --- | --- |
| jet bumper 26 | (270, 389) | Bumper1 (325.0, 379.6) |
| jet bumper 27 | (406, 426) | Bumper2 (548.6, 424.3) |
| jet bumper 25 | (288, 527) | Bumper4 (342.5, 579.7) |
| jet bumper 28 | (421, 571) | Bumper3 (541.2, 624.1) |
| left eject hole 13 | (98, 670) | KLeftEjectHole (60.2, 757.6) |
| right eject hole 30 | (540, 370) | KRightEjectHole (741.3, 301.1) |
| upper right eject hole 36 | (522, 160) | KUpperEjectHole (670.6, 64.0) |
| star rollover 53 | (121, 816) | LeftEjectRollover (98.1, 992.5) |
| star rollover 54 | (560, 510) | RightEjectRollover (782.5, 511.6) |
| ball shooter 46 | (628, 1377) | BallShooter (900.6, 1746.4) |

A least-squares affine fit gives
`X = 1.54361 x + 0.03582 y - 114.683` and `Y = -0.06049 x + 1.40318 y - 154.686` (table units
from drawing pixels), with an RMS residual of 21.1 table units and a worst residual of 36.7, about
0.02 and 0.04 of the playfield width. That is the precision of a schematic line plan, so every
coordinate derived from it is rounded to two decimals of the normalized playfield.

Hidden devices with no table object, placed from the centre of their dashed callout (or, for 49,
the midpoint of its rubber segment):

| Switch | Drawing px | Table units | Normalized (x/952, y/1974) |
| --- | --- | --- | --- |
| 09 outhole | (329, 1425) | (444.2, 1824.9) | (0.47, 0.92) |
| 47 playfield tilt | (142, 1331) | (152.2, 1704.4) | (0.16, 0.86) |
| 45 lane change | (395, 1248) | (539.7, 1572.6) | (0.57, 0.80) |
| 51 left ball ramp | (523, 1378) | (742.0, 1747.3) | (0.78, 0.89) |
| 58 centre ball ramp | (545, 1378) | (775.9, 1745.9) | (0.82, 0.88) |
| 57 right ball ramp | (567, 1378) | (809.9, 1744.6) | (0.85, 0.88) |
| 49 centre middle left standup | (145, 640) | (132.0, 734.5), corrected by the mean residual of its two rail neighbours to (109.6, 729.1) | (0.12, 0.37) |

The two rail neighbours used for the 49 correction are 14 at drawing (122, 556), which the fit
places at (93.5, 618.1) against the table's StandupTarget4 at (73.8, 615.7), and 50 at drawing
(158, 718), placed at (154.9, 843.2) against StandupTarget6 at (129.8, 834.8).
