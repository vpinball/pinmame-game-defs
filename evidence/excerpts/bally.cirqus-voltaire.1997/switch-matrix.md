# Cirqus Voltaire — Switch Matrix

Transcribed from `Bally_1997_Cirqus_Voltaire_Manual.pdf`, PDF page 155, printed page 2-49, the SWITCH
MATRIX table. Read directly from a 600 dpi `pdftoppm` render (the retained scan's `pdftotext -layout`
text layer interleaves the eight rows' wrapped labels out of order and was not trusted for the grid
itself, only used to locate the page). The accompanying crop is the same region, rendered grayscale.

Legend printed on the matrix page: `J2XX = CPU BOARD; [shaded box] = OPTO, TYPICALLY CLOSED`. Column 3
(Green-Orange, addresses 31-38) is shaded for **all eight** rows — every position from Trough Eject
through Top Targets. That is a wider opto set than pinned PinMAME's `cvGameData` inverted-switch mask
normalizes (mask index 3 = `0x3f`, bits 0-5 only, i.e. rows 1-6 / addresses 31-36); rows 7-8 (37, 38 —
"WOW" Targets and Top Targets) are shaded on this page but bit 6/7 of that mask index are clear. See
`conflict.wow-top-targets-opto-not-normalized` in the machine definition.

## Switch matrix (column = tens digit, row = units digit)

Column wiring: 1 Green-Brown J206-1/U20-18, 2 Green-Red J206-2/U20-17, 3 Green-Orange J206-3/U20-16,
4 Green-White J206-4/U20-15, 5 Green-Black J206-5/U20-14, 6 Green-Blue J206-6/U20-13, 7 Green-Violet
J206-7/U20-12, 8 Green-Gray J206-9/U20-11. Row wiring: 1 White-Brown J208-1/U18-11, 2 White-Red
J208-2/U18-9, 3 White-Orange J208-3/U18-5, 4 White-Yellow J208-4/U18-7, 5 White-Green J208-5/U19-11,
6 White-Blue J208-7/U19-9, 7 White-Violet J208-8/U19-5, 8 White-Gray J208-9/U19-7.

| Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Backbox Luck | 21 | Slam Tilt | 31 | Trough Eject `[opto]` | 41 | Left Lane | 51 | Left Slingshot | 61 | Light Standup Target | 71 | Left Saucer | 81 | Not Used |
| 12 | Wire Ramp Enter | 22 | Coin Door Closed | 32 | Trough Ball 1 `[opto]` | 42 | Ringmaster Up | 52 | Right Slingshot | 62 | Lock Standup Target | 72 | Right Saucer | 82 | Not Used |
| 13 | Start Button | 23 | Right Loop Upper | 33 | Trough Ball 2 `[opto]` | 43 | Ringmaster Middle | 53 | Upper Jet Bumper | 63 | Ramp Enter | 73 | Not Used | 83 | Not Used |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Trough Ball 3 `[opto]` | 44 | Ringmaster Down | 54 | Middle Jet Bumper | 64 | Ramp Magnet | 74 | Big Ball Rebound | 84 | Not Used |
| 15 | Left Loop Upper | 25 | Inner Loop Left | 35 | Trough Ball 4 `[opto]` | 45 | Left Ramp Made | 55 | Lower Jet Bumper | 65 | Ramp Made | 75 | "Volt" Right | 85 | Not Used |
| 16 | Top Eddy | 26 | Left Inlane | 36 | Popper Opto `[opto]` | 46 | Trough Upper | 56 | Skill Shot | 66 | Ramp Lock Low | 76 | "Volt" Left | 86 | Not Used |
| 17 | Right Inlane | 27 | Left Outlane | 37 | "WOW" Targets `[opto]` | 47 | Trough Middle | 57 | Right Outlane | 67 | Ramp Lock Middle | 77 | Not Used | 87 | Not Used |
| 18 | Shooter Lane | 28 | Inner Loop Right | 38 | Top Targets `[opto]` | 48 | Left Loop Enter | 58 | Ring "N", "G" | 68 | Ramp Lock High | 78 | Not Used | 88 | Not Used |

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

## Flipper grounded switches (printed F1-F8, public 111-118)

| Printed | Public | Wire/Connector | Shaded (opto)? | Description |
| --- | --- | --- | --- | --- |
| F1 | 111 | Black-Green / J208-13 | no | Lower Right Flipper E.O.S. |
| F2 | 112 | Blue-Violet / J212-12 | yes | Lower Right Flipper Opto |
| F3 | 113 | Black-Blue / J208-12 | no | Lower Left Flipper E.O.S. |
| F4 | 114 | Blue-Gray / J212-11 | yes | Lower Left Flipper Opto |
| F5 | 115 | Black-Violet / J208-11 | no | Right Spinner |
| F6 | 116 | Black-Yellow / J212-10 | yes | Upper Right Flipper Opto |
| F7 | 117 | Black-Gray / J208-10 | no | Left Spinner |
| F8 | 118 | Black-Blue / J212-9 | yes | Upper Left Flipper Opto |

F5 and F7 are printed "RIGHT SPINNER" and "LEFT SPINNER" respectively on this page — the physical
sides agree with the retained table's own geometry (`sw115spinner` at normalized x=0.823, right side;
`sw117spinner` at normalized x=0.090, left side). A prior legacy-migrated record had these reversed
("Left Spinner" at 115, "Right Spinner" at 117); this transcription and the VPX geometry both correct
that. F6 and F8 are printed as wired opto positions on this page (real wire color and `J212`
connector pin, matching the F2/F4 button-opto pattern) even though the Switch Locations list (see
`switch-locations.md`) marks both assembly and switch part "NOT USED" for F6/F8 with no upper
flippers ever installed. Per the precedent already established for Monster Bash's F6/F8, this page
documents the WPC-95 CPU board's generic Fliptronic circuit template, present on the board hardware
regardless of whether this specific machine populates it; the Switch Locations list's blank assembly
column is the physical-fitment authority. `switch.generic-116`/`switch.generic-118` are recorded
`unused` with the printed opto construction preserved in `physical.notes`.
