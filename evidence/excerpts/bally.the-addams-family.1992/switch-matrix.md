# The Addams Family — Switch Matrix (wiring)

Transcribed from `Bally_1992_The_Addams_Family_Operator_s_Handbook_January_1991_OCR_searchable_has_lamp_and_switch_matrices.pdf`,
printed pages 9-10, the Switch Matrix wiring. Visual re-transcription from the rendered page, not the
OCR text layer, which misreads digits and glyphs badly on this two-column board layout. Header:
`White ---|>--o o--- Green`. Unlike the WPC-95 switch matrix pages used on later machines in this
project, this page prints no shaded-opto legend; opto polarity for this machine is established from
the Switch Locations parts list instead (see `switch-locations.md`).

## Dedicated grounded switches

| Public | Wire | Connector | Normal function | Test function |
| --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute | -- |
| D2 | Orange-Red | J205-2 | Center Coin Chute | -- |
| D3 | Orange-Black | J205-3 | Right Coin Chute | -- |
| D4 | Orange-Yellow | J205-4 | 4th Coin Chute | -- |
| D5 | Orange-Green | J205-6 | Service Credits | Escape |
| D6 | Orange-Blue | J205-7 | Volume Down | Down |
| D7 | Orange-Violet | J205-8 | Volume Up | Up |
| D8 | Orange-Gray | J205-9 | Begin Test | Enter |

This page prints no per-switch return-IC column (unlike some later WPC-95 manuals), so no IC
designator is asserted for the dedicated column.

## Matrix drive columns / return rows

| Column | Wire | Connector | Drive IC | | Row | Wire | Connector | Return IC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 | | 1 | White-Brown | J208-1 | U18-11 |
| 2 | Green-Red | J206-2 | U20-17 | | 2 | White-Red | J208-2 | U18-9 |
| 3 | Green-Orange | J206-3 | U20-16 | | 3 | White-Orange | J208-3 | U18-5 |
| 4 | Green-Yellow | J206-4 | U20-15 | | 4 | White-Yellow | J208-4 | U18-7 |
| 5 | Green-Black | J206-5 | U20-14 | | 5 | White-Green | J208-5 | U19-11 |
| 6 | Green-Blue | J206-6 | U20-13 | | 6 | White-Blue | J208-7 | U19-9 |
| 7 | Green-Violet | J206-7 | U20-12 | | 7 | White-Violet | J208-8 | U19-5 |
| 8 | Green-Gray | J206-9 | U20-11 | | 8 | White-Gray | J208-9 | U19-7 |

## Matrix cells (public address = column x 10 + row)

| Row -> | Col1 | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Not Used | Slam Tilt | Upper Left Jet | Grave "G" | Shooter Lane | Left Ramp Enter | Swamp Lock Upper | Bookcase Open |
| 2 | Not Used | Coin Door Closed | Upper Right Jet | Grave "R" | Not Used | Train Wreck | Swamp Lock Center | Bookcase Closed |
| 3 | Start Button | Ticket Opto. | Center Left Jet | Chair Kickout | Bookcase Opto 1 | Thing Eject Lane | Swamp Lock Lower | Not Used |
| 4 | Plumb Bob Tilt | Always Closed | Center Right Jet [see note] | Cousin It | Bookcase Opto 2 | Right Ramp Enter | Lockup Kickout | Thing Down Opto |
| 5 | Left Trough | Right Flipper Lane | Lower Jet | Lower Swamp Million | Bookcase Opto 3 | Right Ramp Top | Left Outlane | Thing Up Opto |
| 6 | Center Trough | Right Outlane | Left Slingshot | Not Used | Bookcase Opto 4 | Left Ramp Top | Left Flipper Lane 2 | Grave "A" |
| 7 | Right Trough | Ball Shooter | Right Slingshot | Center Swamp Million | Bumper Lane Opto | Upper Right Loop | Thing Kickout | Thing Eject Hole |
| 8 | Outhole | Not Used | Upper Left Loop | Upper Swamp Million | Right Ramp Exit | Vault | Left Flipper Lane 1 | Not Used |

### Note on address 34

This rendered matrix page reads column 3 / row 4 as "Center Left Jet" — the same text as row 3 —
which would duplicate address 33's label. Both independent sources disagree with that reading: the
Operations Manual's printed Switch Locations parts list (2-39, see `switch-locations.md`) names item
34 "Center Right Jet", and the retained script's own comment on the object that pulses switch 34
reads `Bumper4_Hit ... vpmTimer.PulseSw 34 'Center Right Jet'`. Per the project's "prefer the parts
list, resolve typos via the symmetric partner" rule, address 34 is recorded as **Center Right Jet**,
matching the natural Upper-Left/Upper-Right/Center-Left/Center-Right/Lower naming progression of a
5-bumper cluster. The table above transcribes the page exactly as printed, including this
misprint, so the disagreement stays visible.

## Fliptronic flipper-grounded switches (public 111-118)

| Printed | Wire | Connector | Description |
| --- | --- | --- | --- |
| F1 (111) | Black-Green | J806-1 | Right Flipper End of Stroke |
| F2 (112) | Blue-Violet | J805-1 | Right Flipper Button |
| F3 (113) | Black-Blue | J806-3 | Left Flipper End of Stroke |
| F4 (114) | Blue-Gray | J805-2 | Left Flipper Button |
| F5 (115) | Black-Violet | J806-4 | Upper Right Flipper End of Stroke |
| F6 (116) | Black-Yellow | J805-3 | Upper Right Flipper Button |
| F7 (117) | Black-Gray | J806-5 | Upper Left Flipper End of Stroke |
| F8 (118) | Black-Blue | J805-5 | Upper Left Flipper Button |

Unlike Williams Monster Bash (WPC-95, where F7 is repurposed as a center spinner and F5/F6/F8 print
"NOT USED"), every one of TAF's eight Fliptronic positions is printed as a genuine flipper
EOS/button pair with real wire colors and connectors. Whether both upper positions are genuinely
fitted hardware, not merely printed template rows, is resolved in
`flipper-assembly-and-thing-flips.md`.
