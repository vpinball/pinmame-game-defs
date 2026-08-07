# Judge Dredd — Switch Locations

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF pages 110 and 111, printed pages 2-42 (lower
half) and 2-43, the SWITCH LOCATIONS parts list and its playfield location diagram. Produced by
rendering the retained PDF at 300 dpi and 600 dpi with `pdftoppm` and reading the pages directly.

The whole list is transcribed, including every row printed `---` / Not Used, because a blank part
number is exactly the evidence that proves nothing is fitted at that address.

Footnotes printed at the bottom of 2-43: `* Not Shown`, `† Located Under Playfield`.

## Parts list

| Item | Switch Part # | Where Used |
| --- | --- | --- |
| F1 | SW-1A-194 | \*Lower Right Flipper EOS |
| F2 | A-16384-1 | \*Lower Right Flipper Cabinet |
| F3 | SW-1A-194 | \*Lower Left Flipper EOS |
| F4 | A-15894 | \*Lower Left Flipper Cabinet |
| F5 | SW-1A-194 | \*Upper Right Flipper EOS |
| F6 | A-16384-1 | \*Upper Right Flipper Cabinet |
| F7 | SW-1A-194 | \*Upper Left Flipper EOS |
| F8 | A-15894 | \*Upper Left Flipper Cabinet |
| 11 | 20-9846-1 | Left Fire Button |
| 12 | 20-9846-1 | Right Fire Button |
| 13 | 20-9663-1 | Credit (Start) |
| 14 | A-15361 | \*Plumb Bob Tilt |
| 15 | 5647-12693-19 | Left Shoot Lane |
| 16 | 5647-12693-19 | Left Outlane |
| 17 | 5647-12693-19 | Left Return Lane |
| 18 | A-14227-15 | 3-bank Targets |
| 21 | SW-1A-117 | \*Slam Tilt |
| 22 | 5643-09288-00 | \*Front Door Closed |
| 23 | --- | \*Ticket Dispenser |
| 24 | 5643-09288-00 | \*Closed |
| 25 | A-16910-15 | Top Right Post |
| 26 | 5647-12693-19 | Captive Ball 1 |
| 27 | A-14227-15 | Mystery |
| 28 | --- | Not Used |
| 31 | 20-9663-9 | Buy-In (Extra Ball) |
| 32 | --- | Not Used |
| 33 | 5647-12693-19 | Left Rollover |
| 34 | 5647-12693-19 | Inside Right Return |
| 35 | 5647-12693-19 | Top Center Rollover |
| 36 | A-16910-15 | Left Score Target |
| 37 | 5647-12693-13 | †Subway Enter 1 |
| 38 | 5647-12693-13 | †Subway Enter 2 |
| 41 | 5647-12693-19 | Right Ball Shooter |
| 42 | 5647-12693-19 | Right Outlane |
| 43 | 5647-12693-19 | Outside Right Return |
| 44 | 20-9663-13 | Super Game |
| 45 | --- | Not Used |
| 46 | --- | Not Used |
| 47 | --- | Not Used |
| 48 | --- | Not Used |
| 51 | SW-1A-114 / SW-1A-120 | Left Sling (Kicker) / (Score) |
| 52 | SW-1A-114 / SW-1A-120 | Right Sling (Kicker) / (Score) |
| 53 | 5647-12693-19 | Captive Ball 2 |
| 54 | A-16486 | Drop Target "J" |
| 55 | A-16486 | Drop Target "U" |
| 56 | A-16486 | Drop Target "D" |
| 57 | A-16486 | Drop Target "G" |
| 58 | A-16486 | Drop Target "E" |
| 61 | A-16598 | \*Globe Position #1 |
| 62 | A-14231 (LED) / A-14232 (Trans.) | Left Ramp Enter |
| 63 | A-14231 (LED) / A-14232 (Trans.) | Left Ramp To Lock |
| 64 | A-14231 (LED) / A-14232 (Trans.) | Left Ramp Exit |
| 65 | --- | Not Used |
| 66 | A-14231 (LED) / A-14232 (Trans.) | Center Ramp Exit |
| 67 | A-14231 (LED) / A-14232 (Trans.) | Left Ramp Enter |
| 68 | A-14227-15 | Captive Ball 3 |
| 71 | A-14231 (LED) / A-14232 (Trans.) | †Magnet Over Ring |
| 72 | A-14231 (LED) / A-14232 (Trans.) | Top Right Opto |
| 73 | A-14231 (LED) / A-14232 (Trans.) | Left Popper |
| 74 | A-14231 (LED) / A-14232 (Trans.) | Right Popper |
| 75 | A-14231 (LED) / A-14232 (Trans.) | Top Ramp Exit |
| 76 | A-14231 (LED) / A-14232 (Trans.) | Right Ramp Exit |
| 77 | A-16598 | \*Globe Position #2 |
| 78 | --- | Not Used |
| 81 | A-16926 (Trans.) / A-16927 (LED) | Trough 1 |
| 82 | A-16926 (Trans.) / A-16927 (LED) | Trough 2 |
| 83 | A-16926 (Trans.) / A-16927 (LED) | Trough 3 |
| 84 | A-16926 (Trans.) / A-16927 (LED) | Trough 4 |
| 85 | A-16926 (Trans.) / A-16927 (LED) | Trough 5 |
| 86 | A-16926 (Trans.) / A-16927 (LED) | Trough 6 |
| 87 | A-16926 (Trans.) / A-16927 (LED) | Top Trough |
| 88 | --- | Not Used |

## Opto sweep across the whole list

Sweeping every row for the two-part `(LED)` + `(Trans.)` construction disclosure gives:

- `A-14231 (LED)` + `A-14232 (Trans.)`: 62, 63, 64, 66, 67, 71, 72, 73, 74, 75, 76 — eleven addresses.
- `A-16926 (Trans.)` + `A-16927 (LED)`: 81, 82, 83, 84, 85, 86, 87 — seven addresses.
- `A-16598` with no LED/transistor breakout, but shaded as an opto on the matrix page: 61, 77.
- Everything else carries a single mechanical switch part number (`SW-1A-*`, `5647-*`, `5643-*`,
  `A-14227-15`, `A-16910-15`, `A-15361`, `20-96*` cabinet buttons, `A-16486` drop targets) or `---`.

`A-16486` on the five JUDGE drop targets is the one construction that this list does not resolve
either way: it is a single assembly number with no LED/transistor pair and no opto shading, so the
list is silent on whether the target's own switch is optical or mechanical.

## Two disagreements inside this page

1. **Item 62 is printed `Left Ramp Enter`, the identical label already printed on item 67.** The
   Switch Matrix page on 2-42 prints 62 as `Crane Exit`, and the location diagram on this same page
   2-43 draws the 62 callout at the extreme left edge of the playfield beside the crane assembly, not
   on the ramp. The duplicated row is a copy-paste slip in the parts list.

2. **Three addresses printed "Not Used" in this list still have callouts drawn in this page's own
   playfield diagram: 28, 32 and 65.** 28 points to a small part at the top of the crane / Magnet Over
   Ring assembly beside 71; 32 points at the plastic orbit ramp on the lower-left run past the globe;
   65 points at a part on the right-hand ramp. Conversely, item **67 — a fitted opto with a full
   `A-14231`/`A-14232` part pair — has no callout anywhere in the diagram at all.** The other printed
   "Not Used" addresses (45, 46, 47, 48, 78, 88) have no callout, so this is not a general habit of
   the drawing: the diagram appears to have been drawn from a design revision in which 28, 32 and 65
   were fitted and 67 was not, and the parts list was updated for production while the drawing was
   not.

## Playfield location diagram — callouts present

Transcribed by sweeping the drawing on 2-43 for every numbered callout, so an absence below is a
recorded absence rather than an unchecked one:

11, 12, 13, 15, 16, 17, 18 (drawn three times, one per target of the 3-bank), 25, 26, 27, 28, 31, 32,
33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 68,
71, 72, 73, 74, 75, 76, 77, 81, 82, 83, 84, 85, 86, 87.

Absent: 14, 21, 22, 23, 24 (all cabinet/coin-door, and 14/21/22/23/24 are marked `*Not Shown` in the
list), 45, 46, 47, 48, 78, 88 (Not Used), F1-F8 (marked `*Not Shown`), and **67**.

61 and 77 are both drawn inside the Deadworld disc outline at its centre, even though the parts list
marks them `*Not Shown`; they are position sensors on the rotating globe assembly rather than points
on the playfield surface.
