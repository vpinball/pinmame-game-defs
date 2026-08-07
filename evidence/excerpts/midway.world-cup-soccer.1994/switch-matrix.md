# World Cup Soccer — Switch Matrix (wiring)

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF page 112, printed page 2-46, the `SWITCH MATRIX`
table (Bally/Midway 16-50031-101 Operations Manual, May 1994). The whole eight-by-eight block plus
the dedicated-switch and Flipper Grounded Switches columns is transcribed, not only the addresses
the definition names, so an unshaded or unused cell is as visible as a shaded one. The accompanying
crop (`switch-matrix.webp`) is the same region rendered grayscale so the shaded opto cells stay
legible.

Header: `White ----|--o/o---- Green`. Footer: `J2XX = CPU Board, J9XX = Fliptronic II Board`;
shaded cells `= Opto, Typically Closed`.

## Dedicated grounded switches

| Public (D#) | Wire | Connector | Return IC | Normal function | Test function |
| --- | --- | --- | --- | --- | --- |
| 1 (D1) | Orange-Brown | J205-1 | U17-5 | Left Coin Chute | — |
| 2 (D2) | Orange-Red | J205-2 | U17-7 | Center Coin Chute | — |
| 3 (D3) | Orange-Black | J205-3 | U17-11 | Right Coin Chute | — |
| 4 (D4) | Orange-Yellow | J205-4 | U17-9 | 4th Coin Chute | — |
| 5 (D5) | Orange-Green | J205-6 | U16-9 | Service Credits | Escape |
| 6 (D6) | Orange-Blue | J205-7 | U16-11 | Volume Down | Down |
| 7 (D7) | Orange-Violet | J205-8 | U16-7 | Volume Up | Up |
| 8 (D8) | Orange-Gray | J205-9 | U16-5 | Begin Test | Enter |

## Matrix drive columns

| Column | Wire | Connector | Drive IC |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

## Matrix return rows

| Row | Wire | Connector | Return IC |
| --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

## The 8x8 grid (public address = column*10 + row)

| Row \ Col | 1 | 2 | 3 (opto) | 4 (opto) | 5 (opto) | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Not Used (11) | Slam Tilt (21) | Trough 1 (Right) (31) | Goal Trough (41) | Skill Shot Front (51) | Rollover 1 (High) (61) | Left Ramp Diverted (71) | Left Jet Bumper (81) |
| 2 | Magna Goalie Button (12) | Coin Door Closed (22) | Trough 2 (32) | Goal Popper Opto (42) | Skill Shot Center (52) | Rollover 2 (62) | Left Ramp Entrance (72) | Upper Jet Bumper (82) |
| 3 | Start Button (13) | Buy Extra Ball (23) | Trough 3 (33) | Goalie Is Left (43) | Skill Shot Rear (53) | Rollover 3 (63) | Not Used (73) | Lower Jet Bumper (83) |
| 4 | Plumb Bob Tilt (14) | Always Closed (24) | Trough 4 (34) | Goalie Is Right (44) | Right Eject Hole (54) | Rollover 4 (Low) (64) | Left Ramp Exit (74) | Left Slingshot (84) |
| 5 | Left Flipper Lane (15) | Free Kick Target (25) | Trough 5 (Left) (35) | TV Ball Popper (45) | Upper Eject Hole (55) | Tackle Switch (65) | Right Ramp Entrance (75) | Right Slingshot (85) |
| 6 | Striker 3 (High) (16) | Kickback Upper (26) | Trough Stack (36) | Not Used (46) | Left Eject Hole (56) | Striker 1 (Left) (66) | Lock Mech. Low (76) | Kickback (86) |
| 7 | Right Return Lane (17) | Spinner (27) | Light Magna Goalie (37) | Travel Lane Rollover (47) | Not Used (57) | Striker 2 (Center) (67) | Lock Mech. High (77) | Upper Left Lane (87) |
| 8 | Right Outlane (18) | Light Kickback (28) | Ball Shooter (38) | Goalie Target (48) | Not Used (58) | Not Used (68) | Right Ramp Exit (78) | Upper Right Lane (88) |

Shaded (opto) cells, verified against the render: 31, 32, 33, 34, 35, 36 (all of column 3); 41, 42,
43, 44, 45 (column 4, rows 1-5 only — 46 is unshaded); 51, 52, 53 (column 5, rows 1-3 only — 54 is
unshaded). No cell in columns 1, 2, 6, 7, or 8 of the ordinary matrix is shaded.

## Flipper Grounded Switches (Fliptronic column, public 111-118)

| Public | Wire | Connector | Printed label | Shaded (opto)? |
| --- | --- | --- | --- | --- |
| 111 (F1) | Black-Green | J906-1 | Right Flipper End of Stroke | No |
| 112 (F2) | Blue-Violet | J905-1 | Right Flipper Opto | **Yes** |
| 113 (F3) | Black-Blue | J906-3 | Left Flipper End of Stroke | No |
| 114 (F4) | Blue-Gray | J905-2 | Left Flipper Opto | **Yes** |
| 115 (F5) | — | — | Not Used | No |
| 116 (F6) | — | — | Not Used | No |
| 117 (F7) | — | — | Not Used | No |
| 118 (F8) | — | — | Not Used | No |

Cross-checked against `evidence/excerpts/midway.world-cup-soccer.1994/boards-and-assemblies.md`:
part A-17316, the assembly wired at F2/F4, is documented there as the "Flipper Opto PCB Assembly"
(item 1: `03-9001 Interrupter Flip-Opto`; item 2: `A-16384 Flipper Opto Switch Assembly`, itself
built from an `Opto Inter Lg. 10mA` component) — genuine opto construction, confirming the shading
rather than contradicting the Switch Locations parts list's "...Cabinet" description (see
`switch-locations.md`).
