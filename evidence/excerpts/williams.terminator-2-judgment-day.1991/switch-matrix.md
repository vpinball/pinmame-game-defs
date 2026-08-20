# Terminator 2: Judgment Day - switch matrix

Source: `Terminator 2 Judgement Day Operations Manual.pdf` (ARC ARC retained source SHA-256 `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`), PDF page 46, printed page 1-26, "Switch Matrix". The crop retains the full printed grid and its row/column wiring headers. It was read manually from the scan; the original is image-only.

The manual orders addresses as **column x row**: the printed row-1 cells are 11, 21, 31 through 81. Column drive wires are 1 Green-Brown J207-1/U20-18, 2 Green-Red J207-2/U20-17, 3 Green-Orange J207-3/U20-16, 4 Green-Yellow J207-4/U20-15, 5 Green-Black J207-5/U20-14, 6 Green-Blue J207-6/U20-13, 7 Green-Violet J207-7/U20-12, and 8 Green-Gray J207-9/U20-11. The final connector digit is filled in on this scan; J207-9 is established by the keyed-pin skip and the same board's legible connector tables in sibling Williams manuals. Row return wires are 1 White-Brown J208-1/U18-11, 2 White-Red J208-2/U18-9, 3 White-Orange J208-3/U18-5, 4 White-Yellow J208-4/U18-7, 5 White-Green J208-5/U19-11, 6 White-Blue J208-7/U19-9, 7 White-Violet J208-8/U19-5, and 8 White-Gray J208-9/U19-7.

| Printed row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Right Flipper | 21 Slam Tilt | 31 Gun Loaded | 41 Left Jet | 51 Left Lock | 61 Left Ramp Entry | 71 Target 1 High | 81 Not Used |
| 2 | 12 Left Flipper | 22 Coin Door Closed | 32 Gun Mark | 42 Right Jet | 52 Not Used | 62 Left Ramp Made | 72 Target 2 | 82 Not Used |
| 3 | 13 Start Button | 23 Ticket Dispenser | 33 Gun Home | 43 Bottom Jet | 53 Low Escape Route | 63 Right Ramp Entry | 73 Target 3 | 83 Not Used |
| 4 | 14 Plumb Bob Tilt | 24 Test Position, Always Closed | 34 Grip Trigger | 44 Left Sling | 54 High Escape Route | 64 Right Ramp Made | 74 Target 4 | 84 Not Used |
| 5 | 15 Trough Left | 25 Left Outlane | 35 Not Used | 45 Right Sling | 55 Top Lock | 65 Low Chase Loop | 75 Target 5 Low | 85 Not Used |
| 6 | 16 Trough Center | 26 Left Return Lane | 36 Mid Left Stand-up Target | 46 Top Right Stand-up Target | 56 Top Lane Left | 66 High Chase Loop | 76 Ball Popper | 86 Not Used |
| 7 | 17 Trough Right | 27 Right Return Lane | 37 Mid Center Stand-up Target | 47 Mid Right Stand-up Target | 57 Top Lane Center | 67 Not Used | 77 Drop Target | 87 Not Used |
| 8 | 18 Outhole | 28 Right Outlane | 38 Mid Right Stand-up Target | 48 Bot Right Stand-up Target | 58 Top Lane Right | 68 Not Used | 78 Shooter | 88 Not Used |

The dedicated-grounded rows on the left are D1 Orange-Brown Left Coin Chute, D2 Orange-Red Center Coin Chute, D3 Orange-Black Right Coin Chute, D4 Orange-Yellow 4th Coin Chute, D5 Orange-Green Service Credits/Escape, D6 Orange-Blue Volume Down/Down, D7 Orange-Violet Volume Up/Up, and D8 Orange-Gray Begin Test/Enter. The complete printed row-4 cell at 24 is "Test Position, Always Closed"; this is the manual evidence for the generated constant switch rather than an inferred normally-closed playfield device.
