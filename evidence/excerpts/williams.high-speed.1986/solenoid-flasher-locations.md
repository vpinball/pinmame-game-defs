# High Speed — Solenoids/Flashers parts list and locations diagram

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 42 (printed page 34, Section 2), read
from a 300 dpi `pdftoppm` render. The page carries the parts list plus a Rubber Parts list on the
left and a numbered playfield locations drawing on the right; all three are transcribed here.

Where this page and the Solenoid Table (printed page 25) differ in wording, both are recorded: this
page is the label authority, the Solenoid Table is the wiring authority.

## Parts list, verbatim

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | AE-23-800-01 | Outhole |
| 2 | AE-23-800-03 | Ball Release |
| 3 | AE-23-800-03 | Eject Hole |
| 4 | 5580-10883-00 | Police Light Relay (Backbox) |
| 5 | #63 Flashlamps | Left Blue Playfield Flashers |
| 6 | #63 Flashlamps | Right Blue Playfield Flashers |
| 7 | AE-24-900-02 | Left Hideout Relay |
| 8 | AE-24-900-02 | Right Hideout Relay |
| 9 | #63 Flashlamps | Left Red Flashers |
| 10 | #63 Flashlamps | Insert Board Flashers |
| 11 | Pwr Sup Bd Relay | General Illumination |
| 12 | #63 Flashlamps | Right Red Flashers |
| 13 | AL-23-800-01 | Ramp Gates |
| 14 | AE-24-900-01 | Left Outlane Kickback (w/relay) |
| 15 | AE-23-800-02 | Knocker |
| 16 | 904218-696 | Coin-Lockout Relay (Coinco p/n) |
| 17 | AE-23-800-03 | Left Kicker |
| 18 | AE-23-800-03 | Right Kicker |
| 19 | AE-23-800-03 | Right Jet Bumper |
| 20 | AE-23-800-03 | Lower Left Jet Bumper |
| 21 | AE-23-800-03 | Upper Left Jett Bumper |
| 22 | #63 Flashlamps | Top Playfield Flashers |
| — | FL 23/600-30/2600-50VDC | Upper Flipper |
| — | FL 23/600-30/2600-50VDC | Right Flipper |
| — | FL 23/600-30/2600-50VDC | Left Flipper |

"Jett" at item 21 is this page's own typo; items 19 and 20 read "Jet", as do all three jet-bumper rows
of the Switches parts list.

Wording differences against the Solenoid Table: this page adds "(Backbox)" to item 4, adds "Playfield"
to items 5 and 6, adds "(w/relay)" to item 14, and gives item 11 a descriptive part ("Pwr Sup Bd
Relay") where the Solenoid Table gives the number 5580-09555-00. Item 16 carries a different Coinco
part number here (904218-696) from the Solenoid Table (404603-22); no source in this manual reconciles
the two, and the device is a coin-door lockout relay with no bearing on any playfield fact.

## Rubber Parts list, verbatim

| Item | Part No. | Description |
| --- | --- | --- |
| A | 23-6300 | 5/16" Ring |
| B | 23-6302 | 1" Ring |
| C | 23-6303 | 1-1/4" Ring |
| D | 23-6306 | 2-3/8" Ring |
| E | 23-6310 | 5" Ring |
| F | 23-6519-4 | Red Ring |
| G | 23-6535 | Bumper |
| H | 23-6552 | Sleeving |

## Numbered locations drawing on the same page

Read from the same render. Solenoid item numbers appear in solid callout circles and rubber items in
lettered circles; several solenoid items carry a **dashed** callout circle, the drawing's convention
for a hidden or under-playfield part. Observations that constrain identity:

- **21, 20 and 19** are the three jet-bumper circles, laid out exactly as the switch-locations drawing
  lays out 33/34/35: **21 upper-left and highest**, **20 directly below it**, **19 to the right of
  both**. Solenoid 21 pairs with switch 33 (Upper Left), 20 with switch 34 (Lower Left) and 19 with
  switch 35 (Right), which is also the pairing PinMAME's own `ssSw` array declares.
- **9** has **two** leader lines, to two small round flasher positions on the **left** side of the
  playfield, one above the other. **12** likewise has two leader lines to two positions on the
  **right** side. Both are consistent with the plural "Flashers" in their names: each of these two
  circuits drives two flasher bulbs.
- **5** and **6** each have a **single** leader line to a single elongated rounded lens shape, 5 to the
  left of the "freeway" insert fan and 6 to its right, at the same height. Both are drawn dashed.
- **22** points to a slot along the very top edge of the playfield, above the ramp area.
- **13** points into the ramp-gate area at the top centre.
- **17** and **18** are the two lower kickers (slingshots), 17 left and 18 right, matching switches 49
  and 50.
- **14** is a dashed callout at the far left just above the lower-left ball guide (the left outlane
  kickback), **2** a dashed callout at the lower right of the trough tube, and **1** a dashed callout at
  the lower centre of it — the same trough geometry the switch-locations drawing numbers 9-12.
- **4, 10, 11, 15 and 16** have no callout on the playfield drawing at all, consistent with the
  Solenoid Table putting 4 and 15 in the Backbox, 10 on the backbox Insert Board (connector 9), 11 on
  the Power Supply Board (connector 3) and 16 in the cabinet (connector 7).
