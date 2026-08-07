# Judge Dredd — Switch Matrix

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF page 110, printed page 2-42, the SWITCH
MATRIX table (the upper half of that page; the lower half is the start of SWITCH LOCATIONS, which is
transcribed separately in `switch-locations.md`). Produced by rendering the retained PDF at 300 dpi
and 600 dpi with `pdftoppm` and reading the table directly. The scan does carry a text layer, but its
multi-column output for this page is scrambled and was never trusted for any value here.

Legend printed under the matrix: `J2XX = CPU Board, J9XX = Fliptronic II Board` and a small box glyph
meaning `= Opto, Typically Closed`.

## Which cells carry the opto shading

The opto marker on this page is a fine halftone stipple filling the cell background. Reading it by eye
is unreliable on a dithered scan, so the whole 8x8 grid was swept mechanically as well: the page was
rendered at 600 dpi, dark connected components were labelled, components larger than 120 px were
treated as printed text and dilated out, and the remaining small blobs were counted per cell. The
result separates cleanly, with a noise floor of 0-2 blobs per cell:

```
small-blob count per cell (600 dpi, text masked)   col1 col2 col3 col4 col5 col6 col7 col8
row 1                                                 0    1    1    1    1   53   55    0
row 2                                                 2    0    0    1    1   51   29    0
row 3                                                 0    1    0    1    1   23   39    0
row 4                                                 1    0    1    0    0   29   50    0
row 5                                                 0    1    0    0    0    0   22    0
row 6                                                 0    1    0    0    1    6   23    0
row 7                                                 0    0    0    0    0   13   13    0
row 8                                                 0    0    0    0    0    1    0    0
```

The shaded set is therefore **61, 62, 63, 64, 66, 67, 71, 72, 73, 74, 75, 76, 77** — thirteen cells,
all in columns 6 and 7, rows 1-7, with 65 and 68 (column 6, rows 5 and 8) and 78 (column 7, row 8)
left unshaded. That set matches the Switch Locations parts list exactly: every shaded address there
carries either an `A-14231 (LED)` + `A-14232 (Trans.)` opto pair (62, 63, 64, 66, 67, 71, 72, 73, 74,
75, 76) or the `A-16598` Globe Position part (61, 77), and the three unshaded cells are the two
printed "Not Used" positions plus 68 Captive Ball 3, an `A-14227-15` standup.

Two things the shading does **not** cover are worth recording, because a reader would otherwise assume
the shading is the complete opto inventory of this machine:

- Column 8 (81-87, the six-ball trough plus Top Trough) is not shaded on this page at all, yet the
  Switch Locations parts list gives every one of those seven addresses an `A-16926 (Trans.)` +
  `A-16927 (LED)` pair. They are optos; the matrix page simply omits the marker for that column.
- Column 5 rows 4-8 (54-58, the JUDGE drop targets) is not shaded either, and the parts list gives
  them a single part number `A-16486` with no LED/transistor disclosure of any kind.

The accompanying crop is the same matrix region rendered grayscale so a reader can see the stipple
directly rather than trust this transcription's per-cell claim.

## Column and row wiring

Columns (drive): 1 Green-Brown J207-1/U20-18, 2 Green-Red J207-2/U20-17, 3 Green-Orange J207-3/U20-16,
4 Green-Yellow J207-4/U20-15, 5 Green-Black J207-5/U20-14, 6 Green-Blue J207-6/U20-13, 7 Green-Violet
J207-7/U20-12, 8 Green-Gray J207-9/U20-11.

Rows (return): 1 White-Brown J209-1/U18-11, 2 White-Red J209-2/U18-9, 3 White-Orange J209-3/U18-5,
4 White-Yellow J209-4/U18-7, 5 White-Green J209-5/U19-11, 6 White-Blue J209-7/U19-9, 7 White-Violet
J209-8/U19-5, 8 White-Gray J209-9/U19-7.

## Matrix (column = tens digit, row = units digit)

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Left Fire Button | 21 | Slam Tilt | 31 | Buy-In (Extra Ball) | 41 | Right Ball Shooter |
| 12 | Right Fire Button | 22 | Front Door Closed | 32 | Not Used | 42 | Right Outlane |
| 13 | Credit (Start) | 23 | Ticket Dispenser | 33 | Left Rollover | 43 | Outside Right Return |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Inside Right Return | 44 | Super Game |
| 15 | Left Shoot Lane | 25 | Top Right Post | 35 | Top Center Rollover | 45 | Not Used |
| 16 | Left Outlane | 26 | Captive Ball 1 | 36 | Left Score Post | 46 | Not Used |
| 17 | Left Return Lane | 27 | Mystery | 37 | Subway Enter 1 | 47 | Not Used |
| 18 | 3-Bank Targets | 28 | Not Used | 38 | Subway Enter 2 | 48 | Not Used |

| Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | Left Sling (2) | 61 | Globe Position #1 | 71 | Magnet Over Ring | 81 | Trough 1 |
| 52 | Right Sling (2) | 62 | Crane Exit | 72 | Top Right Opto | 82 | Trough 2 |
| 53 | Captive Ball 2 | 63 | Left Ramp To Lock | 73 | Left Popper | 83 | Trough 3 |
| 54 | Drop Target "J" | 64 | Left Ramp Exit | 74 | Right Popper | 84 | Trough 4 |
| 55 | Drop Target "U" | 65 | Not Used | 75 | Top Ramp Exit | 85 | Trough 5 |
| 56 | Drop Target "D" | 66 | Center Ramp Exit | 76 | Right Ramp Exit | 86 | Trough 6 |
| 57 | Drop Target "G" | 67 | Left Ramp Enter | 77 | Globe Position #2 | 87 | Top Trough |
| 58 | Drop Target "E" | 68 | Captive Ball 3 | 78 | Not Used | 88 | Not Used |

`(2)` on 51 and 52 is printed inside the cell and records that each slingshot carries two switches
(the kicker switch and a separate score switch), both wired to the one matrix address — see the parts
list, which gives `SW-1A-114` (Kicker) and `SW-1A-120` (Score) for each.

## Dedicated grounded switches (left block of the same page)

| Addr | Printed | Wire | Connector | Label |
| --- | --- | --- | --- | --- |
| 1 | D1 | Orange-Brown | J205-1 | Left Coin Chute |
| 2 | D2 | Orange-Red | J205-2 | Center Coin Chute |
| 3 | D3 | Orange-Black | J205-3 | Right Coin Chute |
| 4 | D4 | Orange-Yellow | J205-4 | 4th Coin Chute |
| 5 | D5 | Orange-Green | J205-6 | Normal Function: Service Credits / Test Function: Escape |
| 6 | D6 | Orange-Blue | J205-7 | Normal Function: Volume Down / Test Function: Down |
| 7 | D7 | Orange-Violet | J205-8 | Normal Function: Volume Up / Test Function: Up |
| 8 | D8 | Orange-Gray | J205-9 | Normal Function: Begin Test / Test Function: Enter |

## Flipper grounded switches (right block of the same page)

| Printed | Wire | Connector | Label |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Right Flipper End of Stroke |
| F2 | Blue-Violet | J905-1 | Right Flipper Opto |
| F3 | Black-Blue | J906-3 | Left Flipper End of Stroke |
| F4 | Blue-Gray | J905-2 | Left Flipper Opto |
| F5 | Black-Violet | J906-4 | Upper Right Flipper End of Stroke |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Opto |
| F7 | Black-Gray | J906-5 | Upper Left Flipper End of Stroke |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto |

F8's wire colour is printed `Black-Blue`, the same as F3; the print is preserved verbatim rather than
silently corrected. None of the eight Fliptronic positions is shaded with the opto marker, even though
F2/F4/F6/F8 are printed "Opto" by name.
