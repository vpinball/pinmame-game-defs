# High Speed — Lamps parts list

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 41 (printed page 33, Section 2), read
from a 300 dpi `pdftoppm` render. Unlike the Switches and Solenoids/Flashers pages, this page has no
Part No. column at all: it is a two-column `Lamp | Location/Description` list, with a small playfield
thumbnail drawing in the middle-right of the page that carries no legible lamp callout numbers at this
scan quality.

This page is the label authority for lamp semantics and is the only source that states which lamps are
on the backglass rather than the playfield.

## Parts list, verbatim, all 64 addresses

| Lamp | Location/Description |
| --- | --- |
| 1 | Game Over (Backglass) |
| 2 | Match (Backglass) |
| 3 | Shoot Again (Backglass) / Drive Again (Playfield) |
| 4 | Left Outlane Special |
| 5 | Right Outlane Special |
| 6 | Ball In Play (Backglass) |
| 7 | Left Spinner 1000 Arrow |
| 8 | Right Spinner 1000 Arow |
| 9 | 20,000 Light Kickback (Left & Right Flipper Lanes) |
| 10 | Center Spinner 1000 Arrow |
| 11 | Extra Ball (Eject Hole) |
| 12 | Escape (Eject Hole) |
| 13 | Red Light (Lwr Left Target Bank) |
| 14 | Yellow Light (Lwr Left Target Bank) |
| 15 | Green Light (Lwr Left Target Bank) |
| 16 | Kickback Arrow (Left Outlane) |
| 17 | Red Light (Upr Left Target Bank) |
| 18 | Yellow Light (Upr Left Target Bank) |
| 19 | Green Light (Upr Left Target Bank) |
| 20 | Left Freeway Arrow |
| 21 | Right Freeway Arrow |
| 22 | Red Light (Right Target Bank) |
| 23 | Yellow Light (Right Target Bank) |
| 24 | Green Light (Right Target Bank) |
| 25 | Standup Target Arrow - 1 |
| 26 | Standup Target Arrow - 2 |
| 27 | Standup Target Arrow - 3 |
| 28 | Standup Target Arrow - 4 |
| 29 | Standup Target Arrow - 5 |
| 30 | Standup Target Arrow - 6 |
| 31 | Freeway Scores 25,000 |
| 32 | Freeway Scores 50,000 |
| 33 | Freeway Scores 75,000 |
| 34 | Freeway Scores 100,000 |
| 35 | Freeway Lights Extra Ball |
| 36 | Ramp Earns Bonus X |
| 37 | Ramp Earns Ramp Bonus |
| 38 | Ramp Earns Getaway |
| 39 | Ramp Earns Hideout |
| 40 | Ramp Earns Hideout Jackpot |
| 41 | Stoplights Light Escape (Center) |
| 42 | Red Light (Ramp Stoplight) |
| 43 | Yellow Light (Ramp Stoplight) |
| 44 | Green Light (Ramp Stoplight) |
| 45 | Bonus 1000 |
| 46 | Bonus 2000 |
| 47 | Bonus 3000 |
| 48 | Bonus 4000 |
| 49 | Bonus 5000 |
| 50 | Bonus 6000 |
| 51 | Bonus 7000 |
| 52 | Bonus 8000 |
| 53 | Bonus 9000 |
| 54 | Bonus 10,000 |
| 55 | Bonus 20,000 |
| 56 | Bonus 30,000 |
| 57 | Bonus 40,000 |
| 58 | Bonus 50,000 |
| 59 | Bonus 60,000 |
| 60 | Bonus 5X |
| 61 | Bonus 4X |
| 62 | Hold Bonus |
| 63 | Bonus 3X |
| 64 | Bonus 2X |

"Arow" at lamp 8 is the page's own typo; its symmetric partner at lamp 7 reads "Arrow", as does lamp
10, so the intended word is Arrow.

## What this page settles

- **Lamps 1, 2 and 6 are backglass-only** and have no playfield position at all.
- **Lamp 3 is a two-bulb circuit split across the backglass and the playfield**: one bulb behind the
  backglass "Shoot Again" panel, one under a playfield "Drive Again" insert. This is what the
  Lamp-Matrix Table's `[2]` marker on address 3 means.
- **Lamp 9 is a two-bulb circuit with both bulbs on the playfield**, one in each flipper return lane,
  which is what its own `[2]` marker means.
- **Lamp 40's `[2]` marker has no location breakdown on either page**: the matrix reads "Ramp Earns
  Hideout Jackpot" and this list reads the same, so the manual states two bulbs but never says where
  the second one is. There is no third page for lamps.
- **Lamp 41 is a stoplight-related insert but not one of the Ramp Stoplight trio** (42-44); the trio is
  the three bulbs of the playfield Traffic Light Assembly, `B-10921`, item 9 of the Playfield Parts
  list.
