# Scared Stiff — Switch Matrix

Transcribed from `Scared_Stiff_OPS.pdf`, PDF page 109, printed page 2-44, the SWITCH MATRIX table.
Produced by rendering the retained PDF at 300-600 dpi with `pdftoppm` and reading the table directly;
this scan's text layer is garbled multi-column OCR and was never trusted. The accompanying crop is
the same region, rendered grayscale.

Legend printed on the matrix page: `J2XX = CPU Board; [box] = Opto, Typically Closed`. The rendered
matrix page shades **zero** cells with that opto box — every one of the 64 matrix positions and all
eight Fliptronic positions are printed with plain (unshaded) borders. This is a genuine difference
from Monster Bash's manual, which does shade its trough/flipper/Dracula-position optos on this same
kind of page. Opto identity for Scared Stiff instead comes from the Switch Locations parts list; see
`switch-locations-opto-sweep.md`. The crop lets a reader confirm directly that no cell is shaded,
rather than trusting this transcription's negative claim on its own.

## Switch matrix (column = tens digit, row = units digit)

Column wiring: 1 Green-Brown J206-1/U20-18, 2 Green-Red J206-2/U20-17, 3 Green-Orange J206-3/U20-16,
4 Green-Yellow J206-4/U20-15, 5 Green-Black J206-5/U20-14, 6 Green-Blue J206-6/U20-13, 7
Green-Violet J206-7/U20-12, 8 Green-Gray J206-9/U20-11. Row wiring: 1 White-Brown J208-1/U18-11, 2
White-Red J208-2/U18-9, 3 White-Orange J208-3/U18-5, 4 White-Yellow J208-4/U18-7, 5 White-Green
J208-5/U19-11, 6 White-Blue J208-7/U19-9, 7 White-Violet J208-8/U19-5, 8 White-Gray J208-9/U19-7.

| Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 21 | Slam Tilt | 31 | Trough Eject | 41 | Coffin Left | 51 | Left Slingshot | 61 | Three Bank Upper | 71 | Left Skull Lane | 81 | Not Used |
| 12 | Wheel Index | 22 | Coin Door Closed | 32 | Trough Ball 1 | 42 | Coffin Center | 52 | Right Slingshot | 62 | Three Bank Middle | 72 | Center Skull Lane | 82 | Not Used |
| 13 | Start Button | 23 | Buy In Button | 33 | Trough Ball 2 | 43 | Coffin Right | 53 | Upper Jet | 63 | Three Bank Lower | 73 | Right Skull Lane | 83 | Not Used |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Trough Ball 3 | 44 | Left Ramp Enter | 54 | Center Jet | 64 | Left Leaper | 74 | Secret Passage | 84 | Not Used |
| 15 | Not Used | 25 | Extra Ball Lane | 35 | Trough Ball 4 | 45 | Right Ramp Enter | 55 | Lower Jet | 65 | Center Leaper | 75 | Not Used | 85 | Not Used |
| 16 | Kickback | 26 | Left Flipper Lane | 36 | Right Popper | 46 | Left Ramp Made | 56 | Upper Slingshot | 66 | Right Leaper | 76 | Not Used | 86 | Not Used |
| 17 | Right Flipper Lane | 27 | Right Outlane | 37 | Left Kickout | 47 | Right Ramp Made | 57 | Crate Sensor | 67 | Left Ramp 10 Point | 77 | Not Used | 87 | Not Used |
| 18 | Shooter Lane | 28 | Single Standup | 38 | Crate Entrance | 48 | Coffin Entrance | 58 | Left Loop | 68 | Right Loop | 78 | Not Used | 88 | Not Used |

## Dedicated grounded switches (coin door, printed D1-D8)

| Addr | Wire | Connector | Label |
| --- | --- | --- | --- |
| 1 (D1) | Orange-Brown | J205-1/U17-5 | Left Coin Chute |
| 2 (D2) | Orange-Red | J205-2/U17-7 | Center Coin Chute |
| 3 (D3) | Orange-Black | J205-3/U17-11 | Right Coin Chute |
| 4 (D4) | Orange-Yellow | J205-4/U17-9 | 4th Coin Chute |
| 5 (D5) | Orange-Green | J205-6/U16-9 | Service Credits / Escape |
| 6 (D6) | Orange-Blue | J205-7/U16-11 | Volume Down / Down |
| 7 (D7) | Orange-Violet | J205-8/U16-7 | Volume Up / Up |
| 8 (D8) | Orange-Gray | J205-9/U16-5 | Begin Test / Enter |

## Fliptronic grounded switches (printed F1-F8, public 111-118)

| Printed | Public | Wire/Connector | Switch part | Description |
| --- | --- | --- | --- | --- |
| F1 | 111 | Black-Green / J208-13 | SW-1A-194 | Lower Right Flipper EOS |
| F2 | 112 | Blue-Violet / J212-12 | A-17316 | *Lower Right Flipper Cabinet (button) |
| F3 | 113 | Black-Blue / J208-12 | SW-1A-194 | Lower Left Flipper EOS |
| F4 | 114 | Blue-Gray / J212-11 | A-17316 | *Lower Left Flipper Cabinet (button) |
| F5 | 115 | Black-Violet / J208-11 | --- | Not Used |
| F6 | 116 | Black-Yellow / J212-10 | --- | Not Used |
| F7 | 117 | Black-Gray / J208-10 | --- | Not Used |
| F8 | 118 | Black-Blue / J212-9 | --- | Not Used |

`*` = "Not Shown" on the playfield map (cabinet-mounted). F5-F8 print `---` for both assembly and
switch part number in the Switch Locations list — a genuine blank, not merely absent from a diagram.
Scared Stiff has no upper flippers. This corrects the legacy-migrated stub, which incorrectly modeled
116/118 as "Upper Right/Left Flipper" used switches.
