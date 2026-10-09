# Williams Black Knight (game 500) - Switch Test and Figure 3 (Playfield Switch Locations and Switch Chart)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf`, Instruction Booklet 16P-500-103.

- Switch Test steps 1-2: PDF page 16 (lower part of the page, below Table 4).
- Switch Test steps 3-5, switch chart and Figure 3: PDF page 17, printed page number `12` (lower left of the page). (PDF page 16 shows no printed page number in the scan; by sequence it is printed page 11.)
- Orientation: both pages upright; no rotation. Read from the 300 dpi renders `render\man300-16.png` and `render\man300-17.png` at 1.3x-5x zoom (`crops2\st-*.png`); the figure's lockup-trough labels were cross-read from the 400 dpi handbook render `render\hb400-12.png` (`crops2\hb12-trough.png`) because they are blurred at 300 dpi.
- Normalization: none; text verbatim, including the typographic quotes around `rectangle`, the double dagger `‡`, the hyphen/en-dash in `20,000 - 99,000` (printed as a short dash with spaces), italic bold `Magna-Save`.

## Switch Test (verbatim)

**Switch Test**

1. From Solenoid Test depress ADVANCE with the switch set to AUTO-UP. Test 03 should be indicated in the Credits display and any stuck switches in the Master display. As stuck switch(es) is displayed a sound is produced. The display continuously cycles through the stuck switches and as they are opened, the number is removed from the sequence. When all switches are open, the Match display is blank and the sounds stop.
2. If all switches in a row are displayed, first verify that all are open and then check for a short to ground on the row wire.
3. Operate switches; a sound is produced and switch number is momentarily indicated in the ball in play display. If two switches in a row are indicated with one switch closed, check for a short between the column wires; for multiple indication check column wire for short to ground. If two switches in a column are indicated with one switch closed, check for short between row wires.
4. If proper indications are obtained in Test 03 but matrix problem is suspected in game play, disconnect lamp connectors 2P5 and 2P7. Recheck in game play. Perform CPU Self-Test if problem remains. If problem is cleared, check for short between lamp matrix and jet bumper mounting brackets.
5. Shorted diodes can cause "rectangle" switch matrix problems as follows: Lower left 3-bank right target down, (switch 27) lower right 3-bank center target down (switch 30) and as ball enters the lockup trough making switch 43, a shorted diode at switch 27 would cause switch 46, Playfield Tilt, to be indicated. Note that the "rectangle" is always completed with an incorrect switch diagonally opposite from the switch with the shorted diode.

## Switch chart (beside Figure 3), verbatim

Heading: `Switch` / `No.` | `Function (Score)`

| Switch No. | Function (Score) |
|---|---|
| 01 | Plumb Bob Tilt |
| 02 | Ball Roll Tilt |
| 03 | Credit Button |
| 04 | Right Coin Switch |
| 05 | Center Coin Switch |
| 06 | Left Coin Switch |
| 07 | Slam Tilt |
| 08 | High Score Reset |
| 09 | Right Magnet Button |
| 10 | Left Magnet Button |
| 11 | Left Outlane (5,000) |
| 12 | Right Outlane (5000) |
| 13 | Spinner (100/2,500*) |
| 14 | Right Ramp Rollunder (500/Mystery) |
| 15 | Right Inside Rollover (2,000/10,000**) |
| 16 | Left Inside Rollover (2,000/10,000**) |
| 17 | Right Ball Ramp |
| 18 | Center Ball Ramp |
| 19 | Left Ball Ramp |
| 20 | Outhole |
| 21 | Left Kicker (10) |
| 22 | Right Kicker (10) |
| 23 | Turnaround (5,000) |
| 24 | Lower Playfield Eject Hole (5,000) |
| 25 | Lower Left 3-Bank, Lower Target (1,000) |
| 26 | Lower Left 3-Bank, Center Target (1,000) |
| 27 | Lower Left 3-Bank, Upper Target (1,000) |
| 28 | Not Used |
| 29 | Lower Right 3-Bank, Right Target (1,000) |
| 30 | Lower Right 3-Bank, Center Target (1,000) |
| 31 | Lower Right 3-Bank, Left Target (1,000) |
| 32 | Not Used |
| 33 | Top Left 3-Bank, Lower Target (1,000) |
| 34 | Top Left 3-Bank, Center Target (1,000) |
| 35 | Top Left 3-Bank, Upper Target (1,000) |
| 36 | Jet Bumper (500) |
| 37 | Top Right 3-Bank, Lower Target (1,000) |
| 38 | Top Right 3-Bank, Center Target (1,000) |
| 39 | Top Right 3-Bank, Upper Target (1,000) |
| 40 | Not Used |
| 41 | Lockup Trough, Bottom (5,000‡) |
| 42 | Lockup Trough, Center (5,000‡) |
| 43 | Lockup Trough, Top (5,000‡) |
| 44 | Left Ramp Rollover (5,000) |
| 45 | Ballshooter Trough |
| 46 | Playfield Tilt |

(46 rows; switch numbers 47-64 are not listed in the chart.)

Footnotes under the chart, verbatim (line breaks as printed; the first line starts at the left edge, the `*Spinner` line is indented, the other lines hang at the left):

```
Note: Second value is lit or flashing value
  *Spinner lit for interval after making
right inside rollover
Mystery is 20,000 - 99,000 and lit for interval
after making left inside rollover
**Inside rollovers light when made after using
Magna-Save feature            (Magna-Save in bold italic)
  ‡Only one lockup trough switch scores for
each locked-up ball
```

Caption below the figure, italic, verbatim: `Figure 3. Playfield Switch Locations and Switch Chart`

## Figure 3: numbered callouts drawn on the playfield outline

Line drawing of the whole playfield (same outline as Figure 2 in `solenoid-locations.md`): top arch with a row of eight round shapes at the top edge, left top-left habitrail/lane curving down the left side, a long diagonal ramp from upper left to lower right, slingshot kickers at lower left and lower right, flippers, an apron (the lower box) with a dashed elongated outline at its lower right, and the shooter lane strip at the right. Callouts are plain numerals unless noted. Position estimates are fractions of the drawn frame (x from the left outer frame line to the right edge of the shooter-lane strip; y from the top edge of the drawing to the bottom of the apron box), rough.

No callout is drawn for switches 01-10, 28, 32, 40 or 47-64 (28, 32 and 40 are `Not Used`; 01-10 are cabinet/coin-door/button switches). Callouts drawn: 11-27, 29-31, 33-39, 41-46 (33 callouts).

**Callouts drawn dashed or in dashed circles:** `23`, `46` (each inside a dashed circle). `19`, `18`, `17` sit along a long dashed elongated outline in the apron area at the lower right; `19` is partly enclosed by the dashed outline's end and in the scan appears inside a small dashed arc. Callout `20` is printed at the left end of the same dashed outline (outside it).

| Callout | Rough position (x, y fractions) | Description |
|---|---|---|
| 44 | (0.12, 0.06) | Upper left, at the top of the left curved lane, to the left of a tall oval (rollover) slot beside the left-top arch. |
| 43 | (0.22, 0.08) | Small numeral inside the upper end of the tall rectangular lockup trough drawn at the upper left (just right of the left habitrail, left of the upper-left drop bank). Top label of three. |
| 42 | (0.21, 0.11) | Small numeral in the middle of the same trough. |
| 41 | (0.19, 0.13) | Small numeral at the bottom (lower end) of the same trough. (The three small numerals read 43 (top), 42, 41 (bottom) on the 400 dpi handbook render; at 300 dpi the top one is blurred.) |
| 35 | (0.35, 0.10) | Upper left, printed to the right of the top (upper) slot of the upper-left angled 3-bank of drop targets (round heads on the left, slotted bar on the right). |
| 34 | (0.33, 0.13) | Same bank, right of the middle slot. |
| 33 | (0.31, 0.16) | Same bank, right of the bottom slot. |
| 36 | (0.49, 0.09) | Inside the large double-ring circle at the top centre (jet bumper). |
| 39 | (0.64, 0.10) | Upper right, rotated numeral at the upper-left end of the angled upper-right 3-bank of drop targets (diagonal bank running upper left to lower right), printed left of the slotted bar. |
| 38 | (0.68, 0.12) | Same bank, middle slot (rotated numeral). |
| 37 | (0.72, 0.15) | Same bank, lower end (rotated numeral). |
| 23 | (0.37, 0.22) | In a **dashed circle**, centre-left, in the open area just inside the dotted loop/arc above the diagonal ramp. |
| 13 | (0.19, 0.37) | Left of centre, printed just below the left end of a small horizontal bar/lever (a spinner drawn as a short bar on the left habitrail exit). |
| 31 | (0.36, 0.41) | Centre, left of the lower-right 3-bank of drop targets (angled bank under the diagonal ramp), at the bank's left end. |
| 30 | (0.42, 0.43) | Same bank, below its middle. |
| 29 | (0.49, 0.45) | Same bank, below its right end. |
| 24 | (0.57, 0.41) | Right of the lower-right 3-bank, beside the dished pocket at the lower end of the diagonal ramp (lower playfield eject hole). |
| 14 | (0.71, 0.41) | Right of centre, printed under a short horizontal bar (ramp rollunder) at the right end, below the right lane guide. |
| 27 | (0.17, 0.46) | Left, printed right of the top slot of the lower-left near-vertical 3-bank of drop targets. |
| 26 | (0.16, 0.48) | Same bank, right of the middle slot. |
| 25 | (0.14, 0.52) | Same bank, right of the bottom slot; a small stray dot follows the numeral in the scan. |
| 16 | (0.12, 0.67) | Lower left, printed above the left slingshot at the top of the left inside lane (left inside rollover), left of a small slotted rollover. |
| 15 | (0.77, 0.67) | Lower right, mirror of 16 (right inside rollover). |
| 11 | (0.04, 0.69) | Far left, printed left of a slotted left outlane rollover. |
| 12 | (0.83, 0.70) | Far right, printed above a slotted right outlane rollover. |
| 21 | (0.25, 0.70) | Lower left, printed at the right edge of the left slingshot (triangular kicker; small slot outline inside). |
| 22 | (0.62, 0.70) | Lower right, printed at the left edge of the right slingshot. |
| 46 | (0.11, 0.87) | In a **dashed circle**, in the left part of the apron box at the lower left. |
| 45 | (0.92, 0.85) | Lower right, printed in the shooter-lane strip at the right of the apron, right of the right end of the dashed elongated outline. |
| 19 | (0.71, 0.90) | Apron, lower right, at the left end of the dashed elongated outline (partially in a dashed arc); rotated numeral. |
| 18 | (0.76, 0.88) | Apron, same dashed outline, right of 19 (rotated numeral). |
| 17 | (0.81, 0.87) | Apron, same dashed outline, right of 18 (rotated numeral). |
| 20 | (0.43, 0.95) | Bottom centre, below the apron curve, printed at the left end of the dashed elongated outline (near a small dashed circle at its left end). |

## Observations (internal comparison with the Switch Matrix on PDF pages 18/69)

- Switch 21: the matrix cell reads `LOWER KICKER 3-BANK, LEFT TARGET` (column 3, row 5), whereas this chart reads `Left Kicker (10)`. Switch 22: matrix `RIGHT KICKER`, chart `Right Kicker (10)`. The matrix text of cell 21 therefore disagrees with the chart wording (the matrix wording is the odd one: it names a 3-bank target, no such bank exists on the left side at this address in the chart).
- Switch 13: matrix `LEFT SPINNER`, chart `Spinner (100/2,500*)` (no side given in the chart). The lamp matrix names `RIGHT SPINNER`.
- Switches 28, 32, 40: matrix `NOT USED STANDUP`, chart `Not Used`. Switches 47-64: matrix `NOT USED`; not in the chart.
- Switch 12 score is printed `(5000)` without the thousands comma; every other score has a comma (`(5,000)`).
- Switch 14 `Right Ramp Rollunder (500/Mystery)`; matrix `RIGHT RAMP ROLLUNDER`.
- Switch 44: chart `Left Ramp Rollover (5,000)`, matrix `LEFT RAMP ROLLOVER`; lamp matrix names a `LEFT RAMP ROLLUNDER EXTRA BALL WHEN LIT` lamp (spelling `ROLLUNDER` vs `ROLLOVER`).
- Switch 41-43: chart `Lockup Trough, Bottom / Center / Top`; the figure places the numerals 43 (top), 42, 41 (bottom) in that order, consistent with the names.
- Step 5 mentions switch 27 (lower left 3-bank right target, as worded in the step: `Lower left 3-bank right target down, (switch 27)`) whereas the chart and matrix name switch 27 `Lower Left 3-Bank, Upper Target`; and `lower right 3-bank center target down (switch 30)` agrees with the chart `Lower Right 3-Bank, Center Target`. The step's `right target` wording for switch 27 therefore differs from the chart's `Upper Target`.
- Step 3 says the switch number is indicated `in the ball in play display`; step 1 says stuck switches are shown in the `Master display`.

## Registration of Figure 3 onto the retained table frame (curator measurement)

Figure 3 is drawn at the same scale on PDF page 12 of the operator's handbook
(`Williams_1980_Black_Knight_Operators_Handbook.pdf`, a 400 dpi 1-bit scan rendered at its native
400 dpi, 2328 x 3534 px), which is sharper than the 300 dpi copy in the manual, so the measurement
was made there. Pixel coordinates below are on that full-page render; the table coordinates are the
retained table's object centres in table units (bounds 0..952 x 0..1974).

Control points (drawing feature -> table object):

| Control | Drawing px | Table units |
| --- | --- | --- |
| Jet bumper 36, centre of the drawn cap | (627, 1110) | Bumper1 (470.206, 182.437) |
| Spinner 13, centre of the drawn bar | (303, 1657) | Spinner (155.928, 705.523) |
| Top left bank, target 34 slot | (418, 1168) | sw34 (275.269, 248.914) |
| Top right bank, target 38 slot | (847, 1140) | sw38 (672.649, 203.535) |
| Lower right bank, target 30 slot | (585, 1780) | sw30 (424.179, 812.315) |
| Left ramp rollover 44 slot | (263, 1090) | sw44 (123.164, 158.847) |
| Left outlane 11 slot | (184, 2410) | sw11 (47.624, 1440.586) |
| Right outlane 12 slot | (975, 2410) | sw12 (810.419, 1441.538) |
| Left inside rollover 16 slot | (251, 2340) | sw16 (115.048, 1375.535) |
| Right inside rollover 15 slot | (905, 2340) | sw15 (745.609, 1375.382) |
| Left flipper pivot (round end) | (400, 2625) | LeftFlipper centre (267.619, 1636.758) |
| Left flipper tip | (506, 2688) | LeftFlipper tip at rest, 116 units along 118 degrees (370.0, 1691.3) |
| Right flipper pivot | (747, 2623) | RightFlipper centre (589.855, 1636.491) |
| Right flipper tip | (645, 2686) | RightFlipper tip at rest, 116 units along -118 degrees (487.4, 1691.0) |
| Apron bottom-right corner | (1022, 2977) | apronwall vertex (873.0, 1974.0) |
| Top right bank, target 39 slot | (809, 1088) | sw39 (635.282, 156.744) |
| Outer playfield frame, top-left corner | (137, 922) | table origin (0, 0) |
| Outer playfield frame, bottom-left corner, constructed: the drawing does not draw this corner, because its outline jogs inward at the apron notch near y 2760 and its drawn bottom-left vertex is at about (181, 2978). The point is the intersection of the left frame line (straight from the top corner down to the notch, x = 142.822 - 0.006634 y, within 1.4 px), extended down past the notch, with the bottom edge (y = 2977.462 + 0.002513 x from x 200 to 1000, within 0.6 px), extended left | (123, 2978) | table bottom-left corner (0, 1974) |

A least-squares affine fit maps drawing pixel (u, v) to table units:
x = 0.957718 u + 0.008570 v - 143.358, y = -0.001043 u + 0.962168 v - 886.320.
The RMS residual is 9.4 table units (about 0.010 of the width); the largest leave-one-out error is
17.3 units (the apron corner). The convex hull of the controls has the corners (123, 2978),
(137, 922), (809, 1088), (847, 1140), (975, 2410) and (1022, 2977), and every point read below lies
inside it, the nearest (17) 44 px inside its edge, so none of them is extrapolated. The curator
recomputes this fit from the controls and readings and derives the normalized values from it.

Points read on the drawing and their registered positions, rounded half-up to two decimals because
the fit is good to about 0.01:

| Callout | Drawing px (what was read) | Table units | Normalized |
| --- | --- | --- | --- |
| 41 Lockup Trough, Bottom | (328, 1190), the label inside the lock bracket | (181.0, 258.3) | (0.19, 0.13) |
| 42 Lockup Trough, Center | (342, 1138), the label inside the lock bracket | (193.9, 208.3) | (0.20, 0.11) |
| 43 Lockup Trough, Top | (355, 1083), the label inside the lock bracket | (205.9, 155.3) | (0.22, 0.08) |
| 17 Right Ball Ramp | (955, 2708), label inside the dashed ball-ramp outline | (794.5, 1718.2) | (0.83, 0.87) |
| 18 Center Ball Ramp | (897, 2737), same outline | (739.2, 1746.2) | (0.78, 0.88) |
| 19 Left Ball Ramp | (851, 2765), same outline | (695.4, 1773.2) | (0.73, 0.90) |
| 20 Outhole | (615, 2890), the small dashed circle at the lower left end of the ball-ramp outline, beside the label 20 | (470.4, 1893.7) | (0.49, 0.96) |
| 46 Playfield Tilt | (250, 2717), centre of the dashed callout circle | (119.4, 1727.6) | (0.13, 0.88) |
| 23 Turnaround (check only) | (503, 1378), centre of the dashed callout circle | (350.2, 439.0) | (0.37, 0.22) |

Checks against objects the table does model: the registered 41 lies 0.007 from the table's LockOut
kicker (0.1971, 0.1328), which kicks the locked balls back out, and 42 and 43 straddle its LockMech
kicker (0.2127, 0.1041), so the drawing and the table agree on the lock mechanism. The retained
table's playfield image (`images/playfieldgioff.png`, 2048 x 4096, stretched over the table bounds;
the `sw11` rollover slot lies exactly under its object centre) shows the bare wood under the apron
with the outhole cut-out, whose small round tab at the lower left end centres on image pixel (1000,
3940), table (464.8, 1898.8): 7.6 units from the registered outhole 20, so the drawing and the table
agree on the outhole too. The table's turnaround trigger sw23 (0.3855, 0.2635) lies 0.04 below the
dashed 23 circle, which marks the switch under the ramp only roughly; the table object is used for
23.
