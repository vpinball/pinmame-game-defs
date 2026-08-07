# The Getaway: High Speed II — SWITCH MATRIX wiring table

Transcribed from `Getaway_HSII_OPS.pdf`, PDF page 109, printed page 3-4, "SWITCH MATRIX". Rendered
at 300 dpi with `pdftoppm` and read directly; the retained OCR text layer was not trusted. This
manual's matrix page carries no opto shading convention (unlike Monster Bash); opto identity comes
instead from the Switch Locations parts list's paired LED/phototransistor part numbers (see
`switch-locations.md`) and the Accelerator/Opto Ramp Switch board assembly pages (see
`accelerator-and-opto-ramp-boards.md`).

## Column and row drive wiring

Column connector J206 (drive, green wires): 1=Green-Brown, 2=Green-Red, 3=Green-Orange,
4=Green-Yellow, 5=Green-Black, 6=Green-Blue, 7=Green-Violet, 8=Green-Gray.

Row connector J209 (return, white wires): 1=White-Brown (J209-1, U18-11), 2=White-Red (J209-2,
U18-9), 3=White-Orange (J209-3, U18-5), 4=White-Yellow (J209-4, U18-7), 5=White-Green (J209-5,
U19-11), 6=White-Blue (J209-7, U19-9), 7=White-Violet (J209-8, U19-5), 8=White-Gray (J209-9, U19-7).

## Matrix grid (column × row → printed device name, address)

| Row \ Col | 1 (Green-Brown) | 2 (Green-Red) | 3 (Green-Orange) | 4 (Green-Yellow) | 5 (Green-Black) | 6 (Green-Blue) | 7 (Green-Violet) | 8 (Green-Gray) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 White-Brown | Not Used (11) | Slam Tilt (21) | Left Sling (31) | Top Yellow (41) | Top Green (51) | Top Jet (61) | Top Loop (71) | Opto 1 (81) |
| 2 White-Red | Not Used (12) | Coin Door Closed (22) | Right Sling (32) | Middle Yellow (42) | Middle Green (52) | Left Jet (62) | Middle Loop (72) | Opto 2 (82) |
| 3 White-Orange | Start Button (13) | Ticket Opto. (23) | Gear Shifter Low (33) | Bottom Yellow (43) | Bottom Green (53) | Bottom Jet (63) | Bottom Loop (73) | Opto 3 (83) |
| 4 White-Yellow | Plumb Bob Tilt (14) | Always Closed (24) | Gear Shifter High (34) | Right Bank Bottom (44) | Ramp Down (54) | Not Used (64) | Top Lock (74) | Opto Made Loop (84) |
| 5 White-Green | Left Freeway Bottom (15) | Left Outlane (25) | Not Used (35) | Right Bank Middle (45) | Outhole (55) | Made Up/Down Ramp (65) | Middle Lock (75) | Enter Left Ramp (85) |
| 6 White-Blue | Left Freeway Top (16) | Left Return Lane (26) | Top Red (36) | Right Bank Top (46) | Left Trough (56) | Not Used (66) | Bottom Lock (76) | Left Bank Bottom (86) |
| 7 White-Violet | Right Freeway Bottom (17) | Right Return Lane (27) | Middle Red (37) | Not Used (47) | Center Trough (57) | Made Left Ramp (67) | Eject Hole (77) | Left Bank Middle (87) |
| 8 White-Gray | Right Freeway Top (18) | Right Outlane (28) | Bottom Red (38) | Not Used (48) | Right Trough (58) | Not Used (68) | Shooter (78) | Left Bank Top (88) |

## Dedicated Grounded Switches (D1-D8)

| Wire | Connector | Function |
| --- | --- | --- |
| D1 Orange-Brown | J205-1 | Left Coin Chute |
| D2 Orange-Red | J205-2 | Center Coin Chute |
| D3 Orange-Black | J205-3 | Right Coin Chute |
| D4 Orange-Yellow | J205-4 | 4th Coin Chute |
| D5 Orange-Green | J205-6 | Normal: Service Credits / Test: Escape |
| D6 Orange-Blue | J205-7 | Normal: Volume Down / Test: Down |
| D7 Orange-Violet | J205-8 | Normal: Volume Up / Test: Up |
| D8 Orange-Gray | J205-9 | Normal: Begin Test / Test: Enter |

## Flipper Grounded Switches (F1-F8)

| Wire | Connector | Function |
| --- | --- | --- |
| F1 Black-Green | J906-1 | Right Flipper End of Stroke |
| F2 Blue-Violet | J905-1 | Right Flipper Button |
| F3 Black-Blue | J906-3 | Left Flipper End of Stroke |
| F4 Blue-Gray | J905-2 | Left Flipper Button |
| F5 Black-Violet | J906-4 | Upper Right Flipper End of Stroke |
| F6 Black-Yellow | J905-3 | Upper Right Flipper Button |
| F7 Black-Gray | J906-5 | Upper Left Flipper End of Stroke |
| F8 Black-Blue | J905-5 | Upper Left Flipper Button |

This F1-F8 block is the generic Fliptronic II CPU-board wiring template shared across every WPC
Fliptronic-generation title (the same eight silkscreen positions appear regardless of which flippers a
specific machine actually fits); the Switch Locations parts list (`switch-locations.md`) is the
game-specific fitment evidence, and it lists no switch assembly for F7/F8 at all. `gwGameData`
(`FLIP_SW(FLIP_L | FLIP_UR)`) independently agrees: only the lower pair and the upper-right position
carry a flipper bit.
