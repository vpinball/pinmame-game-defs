# Williams Black Knight (game 500) - Solenoid Test and Figure 2 (Playfield Solenoid Locations and Solenoid Chart)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf`, PDF page 15 (Instruction Booklet 16P-500-103). Printed page number: `10` (printed at the lower left of the page). Orientation: upright; no rotation. Read from the 300 dpi render `render\man300-15.png` at 1.3x-2.6x zoom (`crops2\sl-*.png`). The operator's handbook (hb page 10) carries the same page; compared by contact sheet, same wording and callouts.

Normalization: none. The `*` before `11` is printed as `*11`.

## Solenoid Test (verbatim)

**Solenoid Test**

1. From Lamp Test depress ADVANCE with the switch set to AUTO-UP. Test 02 should be indicated in the Credits display. Display sequences from 01 thru 25. Corresponding solenoids 01 thru 24 are pulsed. Flipper relay is de-energized with subtest 25.
2. To continuously pulse a single solenoid set switch to MANUAL-DOWN. Operate ADVANCE pushbutton sequence through the solenoids one at a time. Set toggle switch to AUTO-UP to resume sequencing.

## Solenoid chart (beside Figure 2), verbatim

Heading: `Sol.` / `No.` | `Function`

| Sol. No. | Function |
|---|---|
| 01 | Ball Release |
| 02 | Lower Left 3-Bank Drop Target Reset |
| 03 | Lower Right 3-Bank Drop Target Reset |
| 04 | Upper Left 3-Bank Drop Target Reset |
| 05 | Upper Right 3-Bank Drop Target Reset |
| 06 | Ball Ramp Thrower |
| 07 | Multi-Ball Release |
| 08 | Lower Eject Hole |
| 09 | Right Magnet Relay |
| 10 | Left Magnet Relay |
| *11 | Special Relay |
| 12 | Not Used |
| 13 | Not Used |
| 14 | Not Used |
| 15 | Bell |
| 16 | Coin Lockout |
| 17 | Left Kicker |
| 18 | Right Kicker |
| 19 | Jet Bumper |
| 20 | Not Used |
| 21 | Not Used |
| 22 | Not Used |

(22 rows.) Footnote, verbatim (its `*` is printed at the left, hanging):

`* Special relay located on Power Supply Board (games with transformer in cabinet) or in backbox (games with transformer in backbox).`

Caption below the figure, italic, verbatim: `Figure 2. Playfield Solenoid Locations and Solenoid Chart`

## Figure 2: numbered callouts drawn on the playfield outline

The figure is a line drawing of the whole playfield (top at the top, shooter lane at the right edge, apron at the bottom). Thirteen two-digit callouts are drawn. Position estimates below are fractions of the drawn playfield frame (x from the left outer frame line to the right edge of the shooter-lane strip; y from the top arch to the apron bottom), so they are rough. Callouts 09 and 10 are drawn inside **dashed circles**. No callout is drawn for solenoids 11-16, 20-22 (11 is the special relay, located on the power supply board / in the backbox per the footnote).

| Callout | Rough position (x, y fractions) | Description of what it sits at |
|---|---|---|
| 19 | (0.50, 0.09) | Printed inside the large circle at the top centre: the jet bumper (a double-ring circle). |
| 04 | (0.34, 0.12) | Upper left, to the right of an angled, near-vertical bank of drop targets (three round target heads with a slotted reset bar) that stands just inside the left top arch; a long rounded-rectangle (flasher/lane box) sits to its left. Printed right of the bank. |
| 05 | (0.68, 0.12) | Upper right, printed below-left of an angled bank of round drop targets (four round heads along a diagonal slotted reset bar) that runs from upper left to lower right. |
| 07 | (0.18, 0.17) | Left side, below callout 04 and the upper left drop target bank, at the lower end of the left curved habitrail/lane that curves down the left side; printed in clear space left-below the bank. |
| 08 | (0.58, 0.41) | Centre-right, just to the right of the bottom end of the diagonal ramp / eject pocket (the diagonal tube that crosses the playfield from upper left to lower right ends near here); it is printed beside a dished rectangular pocket at the right end of the ramp. |
| 03 | (0.42, 0.43) | Centre, beneath the diagonal ramp, printed under an angled bank of round drop targets (four round heads along a diagonal slotted bar) that sits left of callout 08. |
| 02 | (0.16, 0.49) | Left side, printed to the right of a near-vertical bank of three drop targets (round heads on the left, slotted reset bar on the right) at the left of the lower playfield. |
| 10 | (0.26, 0.50) | In a **dashed circle**, in the open space to the right of callout 02, left-centre of the lower playfield. |
| 09 | (0.67, 0.50) | In a **dashed circle**, in the open space right of centre, just left of the curved right-side lane guide; mirror of callout 10. |
| 17 | (0.26, 0.70) | Lower left: printed at the right edge of the left slingshot (a triangular kicker with a slot outline in its upper portion). |
| 18 | (0.64, 0.70) | Lower right: printed at the left edge of the right slingshot, a mirror of 17. |
| 06 | (0.87, 0.82) | Lower right, next to the right-hand end of a long **dashed** elongated outline (a ramp/trough with an inner dashed outline) running diagonally in the apron area below the right flipper; printed at the top right end of that dashed shape, near the right wall. |
| 01 | (0.44, 0.95) | Bottom centre, below the apron curve, printed at the left end of the same long dashed elongated outline (near a small dashed circle at its left end). |

Other drawn items that carry no callout: a drawn row of eight round shapes along the very top edge (the top lane/target row above the arch); the two flippers and their guide lines at the bottom; two thin dashed lines marking the shooter lane at the right; dashed curved outlines near the upper left ramp (thin and bold dashed).

## Observations (internal comparison)

- The chart marks only solenoid `11` with `*`, whereas Table 4 (PDF page 16) also marks `09`, `10`, `17`, `18`, `19`, `20`, `21`, `22` with `*` (for different footnote meanings). Functions and numbers 01-22 are otherwise identical between this chart and Table 4.
- The test text says `Display sequences from 01 thru 25`, `solenoids 01 thru 24 are pulsed`, and `Flipper relay is de-energized with subtest 25`; the chart lists solenoids only to 22.
- Callout `07` (Multi-Ball Release) is drawn near the top left of the playfield, while `06` (Ball Ramp Thrower) and `01` (Ball Release) are drawn in the apron area at the lower right/bottom, all three on dashed or ramp-like outlines.
