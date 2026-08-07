# White Water — Switch Matrix (wiring table)

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF page 114, printed
page 3-4 ("Switches" / "Switch Matrix"). Transcribed from a 200 dpi render.
Unlike some later WPC manuals in this project, this page carries **no opto
shading legend** — every cell uses the same plain typeface regardless of
switch construction, so opto identity for this machine comes from the
Switch Locations parts list (`switch-locations.md`), not from this page's
typography.

Column headers (drive wire / connector / driver IC): 1 Green-Brown J207-1
U20-18, 2 Green-Red J207-2 U20-17, 3 Green-Orange J207-3 U20-16, 4
Green-Yellow J207-4 U20-15, 5 Green-Black J207-5 U20-14, 6 Green-Blue
J207-6 U20-13, 7 Green-Violet J207-7 U20-12, 8 Green-Gray J207-9 U20-11.

Row headers (return wire / connector / receiver IC): 1 White-Brown J209-1
U18-11, 2 White-Red J209-2 U18-9, 3 White-Orange J209-3 U18-5, 4
White-Yellow J209-4 U18-7, 5 White-Green J209-5 U19-11, 6 White-Blue
J209-7 U19-9, 7 White-Violet J209-8 U19-5, 8 White-Gray J209-9 U19-7.

Cell labels, address = column*10 + row (manual's own convention, confirmed
on page 33: "Example - Switch 23 is 2nd column, 3rd row"):

| addr | label | addr | label | addr | label | addr | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 21 | Slam Tilt | 31 | River "R2" | 41 | Light Lock Left |
| 12 | Not Used | 22 | Coin Door Closed | 32 | River "E" | 42 | Light Lock Right |
| 13 | Start Button | 23 | Ticket Opto. | 33 | River "V" | 43 | Left Loop |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | River "I" | 44 | Right Loop |
| 15 | Outhole | 25 | Left Outlane | 35 | River "R1" | 45 | Secret Passage |
| 16 | Left Jet Bumper | 26 | Left Flipper Lane | 36 | 3-bank Top | 46 | Left Ramp Enter |
| 17 | Right Jet Bumper | 27 | Right Outlane... (see note) | 37 | 3-bank Center | 47 | Rapids Enter |
| 18 | Center Jet Bumper | 28 | Right Outlane | 38 | 3-bank Lower | 48 | Canyon Entrance |

| addr | label | addr | label | addr | label | addr | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | Left Sling | 61 | Whirlpool Popper | 71 | Rapids Ramp Main | 81 | Not Used |
| 52 | Right Sling | 62 | Whirlpool Exit | 72 | Not Used | 82 | Not Used |
| 53 | Ball Shooter | 63 | Lockup Right | 73 | Hot Foot Upper | 83 | Not Used |
| 54 | Lower Jet Arena | 64 | Lockup Center | 74 | Hot Foot Lower | 84 | Not Used |
| 55 | Right Jet Arena | 65 | Lockup Left | 75 | Disaster Drop Main | 85 | Not Used |
| 56 | Extra Ball | 66 | Left Ramp Main | 76 | Right Trough | 86 | Bigfoot Opto 1 |
| 57 | Canyon Main | 67 | Not Used | 77 | Center Trough | 87 | Bigfoot Opto 2 |
| 58 | Bigfoot Cave | 68 | Disaster Drop Enter | 78 | Left Trough | 88 | Not Used |

(Row 3/column 2 prints "Right Flipper Lane" at 27 and row-4/column-2 prints
"Always Closed" at 24; the table above is column-major and matches the
Switch Locations parts list exactly — see that file for the authoritative
per-cell reading used by the curator.)

## Dedicated grounded switches (coin door)

| D# | Wire | Connector | Normal function | Test-mode function |
| --- | --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 | Left Coin Chute | — |
| D2 | Orange-Red | J205-2 | Center Coin Chute | — |
| D3 | Orange-Black | J205-3 | Right Coin Chute | — |
| D4 | Orange-Yellow | J205-4 | Fourth Coin Chute | — |
| D5 | Orange-Green | J205-6 | Service Credits | Escape |
| D6 | Orange-Blue | J205-7 | Volume Down | Down |
| D7 | Orange-Violet | J205-8 | Volume Up | Up |
| D8 | Orange-Gray | J205-9 | Begin Test | Enter |

## Fliptronic (F1-F8)

| F# | Wire | Connector | Label |
| --- | --- | --- | --- |
| F1 | Black-Green | J905-1 | Lower Right E.O.S. Switch |
| F2 | Blue-Violet | J905-2 | Lower Right Flipper Button |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S. Switch |
| F4 | Blue-Gray | J905-2 (2nd conn.) | Lower Left Flipper Button |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S. Switch |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Button |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. Switch |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Button |

F7/F8 print with the same generic template as the fitted F1-F6 positions
(this is the shared WPC Fliptronic CPU-board silkscreen), but the Switch
Locations parts list has no row at all for F7/F8 — no assembly, no switch
part — so the upper-left flipper position is enumerated as unfitted
template wiring, not a physical switch.
