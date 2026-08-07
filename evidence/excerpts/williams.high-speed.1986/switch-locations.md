# High Speed — Switches parts list and switch-locations diagram

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 40 (printed page 32, Section 2 "Game
Parts Information"), read from a 300 dpi `pdftoppm` render. The page carries the parts list on the
left and a numbered playfield locations drawing on the right; both are transcribed here.

This is the authoritative label page for switch semantics. Where it and the Switch-Matrix Table
(printed page 26) disagree, this page wins, per the project's own "prefer the parts list" rule.

## Opto sweep — the whole list, every row

Every row below carries a part number in the Part No. column. **No row is blank, no row carries an
opto/LED/phototransistor part number, no row carries a second construction line, and the page has no
opto legend, footnote, or shading of any kind.** The only footnotes on the page are the `*` Coinco
attribution on items 4-7 and the bracketed `[Kicker Actuating Sw: A-4834-H; B-8734 w/RC]` annotation
spanning items 49-51. Combined with the unshaded Switch-Matrix Table, this manual documents **no
opto and no normally-closed matrix switch anywhere on this machine**.

## Parts list, verbatim

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | A-8476 | Plumb Bob Tilt |
| 2 | B-6572 | Ball Roll Tilt |
| 3 | SW-1A-126 | Credit Button |
| 4 | 904845* | Right Coin Chute (* - Coinco p/n) |
| 5 | 904845* | Center Coin Chute |
| 6 | 904845* | Left Coin Chute |
| 7 | 904704* | Slam Tilt |
| 8 | 5641-09369-00 | High Score Reset |
| 9 | 17-1067 | Outhole |
| 10 | 5647-09957-00 | Left Trough |
| 11 | 5647-09957-00 | Center Trough |
| 12 | 5647-09933-00 | Right Trough |
| 13 | A-11022 | Red Target (Lwr Left Stoplight Bank) |
| 14 | A-11054 | Yellow Target (Lwr Left Stoplight Bank) |
| 15 | A-11055 | Green Target (Lwr Left Stoplight Bank) |
| 16 | 17-1012 | Eject Hole |
| 17 | A-11022 | Red Target (Upr Left Stoplight Bank) |
| 18 | A-11054 | Yellow Target (Upr Left Stoplight Bank) |
| 19 | A-11055 | Green Target (Upr Left Stoplight Bank) |
| 20 | SW-1A-124 | Left Flipper Return Lane |
| 21 | SW-1A-124 | Right Flipper Return Lane |
| 22 | A-11022 | Red Target (Right Stoplight Bank) |
| 23 | A-11054 | Yellow Target (Right Stoplight Bank) |
| 24 | A-11055 | Green Target (Right Stoplight Bank) |
| 25 | A-8253 | Standup Target Arrow - 1 |
| 26 | A-8253 | Standup Target Arrow - 2 |
| 27 | A-8253 | Standup Target Arrow - 3 |
| 28 | A-8253 | Standup Target Arrow - 4 |
| 29 | A-8253 | Standup Target Arrow - 5 |
| 30 | A-8253 | Standup Target Arrow - 6 |
| 31 | SW-1A-124 | Left Outlane |
| 32 | SW-1A-124 | Right Outlane |
| 33 | A-7459-7 | Upper Left Jet Bumper |
| 34 | A-7459-7 | Lower Left Jet Bumper |
| 35 | A-7459-7 | Right Jet Bumper |
| 36 | SW-1A-138 | Ball Shooter |
| 37 | SW-1A-150-1 | Left Flipper Lane Change (Engine Revs) |
| 38 | SW-1A-150 | Right Flipper Lane Change (Engine Revs) |
| 39 | A-11047 | Upper Left Hideout |
| 40 | 17-1085 | Lower Left Hideout |
| 41 | SW-1A-117 | Playfield Tilt |
| 42 | SW-1A-160 | Left Ramp |
| 43 | SW-1A-160 | Right Ramp |
| 44 | SW-1A-118 | Left Spinner |
| 45 | SW-1A-118 | Center Spinner |
| 46 | SW-1A-118 | Right Spinner |
| 47 | A-11047 | Upper Right Hideout |
| 48 | 17-1085 | Lower Right Hideout |
| 49 | SW-1A-122 | Left Kicker (scoring) [Kicker Actuating Sw: A-4834-H; B-8734 w/RC] |
| 50 | SW-1A-122 | Right Kicker (scoring) [Kicker Actuating Sw: A-4834-H; B-8734 w/RC] |
| 51 | SW-1A-157 | Left Star Rollover [Kicker Actuating Sw: A-4834-H; B-8734 w/RC] |
| 52 | SW-1A-157 | Right Star Rollover |
| 53-64 | Not Used | Not Used |

The bracketed `[Kicker Actuating Sw: A-4834-H; B-8734 w/RC]` annotation is printed once, spanning the
three lines 49/50/51, and reads as belonging to the two Kicker rows (49, 50) rather than to the Left
Star Rollover row whose line it happens to end beside: it names the *actuating* switch of a kicker
assembly, and 51/52 are plain star rollovers with no kicker. `SW-1A-122` is the scoring switch of the
kicker assembly; `A-4834-H` / `B-8734 w/RC` is the separate switch that fires the coil directly.

## Numbered locations drawing on the same page

Read from the same render. The drawing is a plan view of the playfield with each switch number in a
circled callout and a leader line to the device. Observations that constrain identity, recorded
because they are geometric facts a table transcription cannot carry:

- The three jet-bumper circles are drawn as: **33 upper-left and highest**, **34 directly below 33**,
  **35 to the right of both and between them in height**. This ordering is the decisive evidence for
  which physical bumper each address belongs to.
- **37** and **38** are drawn at the two lower flippers — 37 at the left flipper, 38 at the right —
  confirming these switches are on the flipper base assemblies under the playfield rather than
  anywhere in the backbox or on the cabinet front.
- **39 is drawn above 40** in the long left ball chute, and **47 is drawn above 48** in the mirror
  right chute. Each hideout is therefore a two-switch lane with the "Upper" switch nearer the rear.
- **41** (Playfield Tilt) is drawn with a **dashed** callout circle placed outside the playfield
  outline at the lower left, the drawing's convention for a hidden/under-playfield item.
- **9** is at the left end of the outhole/trough tube along the bottom, with **10, 11, 12**
  progressing along the tube toward the right, so 12 is the trough position nearest the shooter-lane
  feed.
- **17/18/19** form a top-to-bottom vertical trio at the upper left; **13/14/15** a second
  top-to-bottom trio lower on the left; **22/23/24** a left-to-right diagonal trio in the middle.
- **42** is left of **43** at the very top of the playfield; **51** is at the top-left corner and
  **52** at the top-right; **44** is on the far left, **45** right of centre, **46** on the right;
  **20** is left of **21**, and **49** is left of **50**.
- A third flipper bat is drawn on the **right** side of the playfield roughly level with the 47/48
  callouts, above the right hideout lane. The manual's Solenoids/Flashers list names an "Upper
  Flipper" coil but never states its side; this drawing is where the upper-right position comes from.
