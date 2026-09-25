# Twilight Zone — Switch Matrix and switch list items F1-33 (printed 2-50)

Transcribed from `Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf` (the complete IPDB copy of
operations manual 16-50020-101), PDF page 118, printed page 2-50. Read from the 300 dpi render; the PDF's OCR layer
was used only to find the page. The Internet Archive scan lacks this page. Two regions are transcribed whole: the
"SWITCH MATRIX" table at the top of the page and the "SWITCH LOCATIONS" item list at the lower left. The drawing
beside the list is excerpted separately (`mini-playfield-switch-drawing.md`). Cell text is literal; line breaks
inside a cell are joined with a space.

## Switch Matrix

Column headings (number, wire colour, CPU connector, driver pin):

| Column | Wire | Connector | Driver |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-Yellow | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |
| 9 | Gray-White | *J5-1 | (blank) |

A diode symbol is printed above columns 6-7 between the labels "White" and "Green".

Row headings (number, wire colour, CPU connector, receiver pin):

| Row | Wire | Connector | Receiver |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | J208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

Cells (switch number, printed name):

| Row | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 | Col 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Right Inlane | 21 Slam Tilt | 31 Left Jet Bumper | 41 Dead End | 51 Gumball Popper Lane | 61 Lower Skill | 71 Not Used | 81 Lower Right Magnet | 91 Clock 15 Minutes |
| 2 | 12 Right Outlane | 22 Coin Door Closed | 32 Right Jet Bumper | 42 The Camera | 52 Hitch-Hiker | 62 Center Skill | 72 Auto-Fire Kicker | 82 Not Used | 92 Clock 0 Minutes |
| 3 | 13 Start Button | 23 Buy-In Button | 33 Lower Jet Bumper | 43 Player Piano | 53 Left Ramp Enter | 63 Upper Skill | 73 Right Ramp | 83 Left Magnet | 93 Clock 45 Minutes |
| 4 | 14 Plumb Bob Tilt | 24 Always Closed | 34 Left Slingshot | 44 Mini Playfield Enter | 54 Left Ramp | 64 Upper Right 5 Million | 74 Gumball Popper | 84 Center Lock | 94 Clock 30 Minutes |
| 5 | 15 Right Trough | 25 Far Left Trough | 35 Right Slingshot | 45 Mini Playfield Left (2) | 55 Gumball Geneva | 65 Power Payoff (2) | 75 Mini Playfield Top | 85 Upper Lock | 95 Clock Hour 1 |
| 6 | 16 Center Trough | 26 Trough Proximity | 36 Left Outlane | 46 Mini Playfield Right (2) | 56 Gumball Exit | 66 Middle Right 5 Million 1 | 76 Mini Playfield Exit | 86 Not Used | 96 Clock Hour 2 |
| 7 | 17 Left Trough | 27 Ball Shooter | 37 Left Inlane 1 | 47 Clock Millions | 57 Slot Proximity | 67 Middle Right 5 Million 2 | 77 Middle Left 5 Million | 87 Gumball Enter | 97 Clock Hour 3 |
| 8 | 18 Outhole | 28 Rocket Kicker | 38 Left Inlane 2 | 48 Lower Left 5 Million | 58 Slot Kickout | 68 Lower Right 5 Million | 78 Upper Left 5 Million | 88 Lock Lower | 98 Clock Hour 4 |

No cell is shaded and the table carries no opto legend.

Dedicated grounded switches (left-hand block):

| Switch | Wire | Connector | Printed function |
| --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute |
| D2 | Orange-Red | J205-2 | Center Coin Chute |
| D3 | Orange-Black | J205-3 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 | Normal function: Service Credits; Test function: Escape |
| D6 | Orange-Blue | J205-7 | Normal function: Volume Down; Test function: Down |
| D7 | Orange-Violet | J205-8 | Normal function: Volume Up; Test function: Up |
| D8 | Orange-Gray | J205-9 | Normal function: Begin Test; Test function: Enter |

Flipper grounded switches (right-hand block):

| Switch | Wire | Connector | Printed function |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Right Flipper End of Stroke |
| F2 | Blue-Violet | J905-1 | Right Flipper Opto |
| F3 | Black-Blue | J906-3 | Left Flipper End of Stroke |
| F4 | Blue-Gray | J905-2 | Left Flipper Opto |
| F5 | Black-Violet | J906-4 | Upper Right Flipper End of Stroke |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Opto |
| F7 | Black-Gray | J906-5 | Upper Left Flipper End of Stroke |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto |

Footnotes under the table: "J2XX = CPU Board, J9XX = Fliptronic II Board" and "* Located on 8 Driver P.C.B.,
A-16100, in backbox."

## Switch list, items F1-F8 and 11-33

Under "SWITCH LOCATIONS", columns "Item", "Switch Part #", "Where Used". The list continues on page 2-51.

| Item | Switch Part # | Where Used |
| --- | --- | --- |
| F1 | 5490-12451-00 | *Lower Right Flipper EOS |
| F2 | A-15894 | *Lower Right Flipper Cabinet |
| F3 | 5490-12451-00 | *Lower Left Flipper EOS |
| F4 | A-15894 | *Lower Left Flipper Cabinet |
| F5 | 5490-12451-00 | *Upper Right Flipper EOS |
| F6 | A-15894 | *Upper Right Flipper Cabinet |
| F7 | 5490-12451-00 | *Upper Left Flipper EOS |
| F8 | A-15894 | *Upper Left Flipper Cabinet |
| 11 | 5647-12693-19 | Right Inlane |
| 12 | 5647-12693-19 | Right Outlane |
| 13 | 20-9663-1 | Start Button |
| 14 | A-15361 | *PlumbBob Tilt |
| 15 | 5647-12693-08 | Right Trough |
| 16 | 5647-09957-00 | Center Trough |
| 17 | 5647-09957-00 | Left Trough |
| 18 | 5647-12133-12 | Outhole |
| 21 | 27-1066 | *Slam Tilt |
| 22 | 5643-09288-00 | *Coin Door Closed |
| 23 | 20-9663-9 | Buy-In Button |
| 24 | ---- | Always Closed |
| 25 | 5647-09957-00 | Far Left Trough |
| 26 | A-16528 | †Trough Proximity |
| 27 | 5647-12693-04 | Ball Shooter |
| 28 | 5647-12693-55 | Rocket Kicker |
| 31 | SW-11A-37 | Left Jet Bumper |
| 32 | SW-11A-37 | Right Jet Bumper |
| 33 | SW-11A-37 | Lower Jet Bumper |

Item 24's part column prints four dashes, not a part number. This page carries no legend for the `*` and `†`
markers.
