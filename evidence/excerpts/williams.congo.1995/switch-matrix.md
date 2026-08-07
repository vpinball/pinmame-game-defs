# Congo -- Switch Matrix (manual printed page 2-40, PDF page 109)

Transcribed verbatim from a 300/600 dpi render of `Congo_OPS.pdf` page 109. Header: "SWITCH MATRIX" with a legend arrow "White --> -o/ o-- Green" and, at the bottom, "J2XX = CPU BOARD" and a shaded-box legend "= OPTO, TYPICALLY CLOSED". Cells shaded in the original page are marked **[OPTO]** below; every other cell is a plain leaf/microswitch/button per the Switch Locations page. Address = column*10 + row (column is the drive line, row is the return line).

Column drive wiring: 1 Green-Brown J206-1 U20-18; 2 Green-Red J206-2 U20-17; 3 Green-Orange J206-3 U20-16; 4 Green-Yellow J206-4 U20-15; 5 Green-Black J206-5 U20-14; 6 Green-Blue J206-6 U20-13; 7 Green-Violet J206-7 U20-12; 8 Green-Gray J206-9 U20-11.

Row return wiring: 1 White-Brown J208-1 U18-11; 2 White-Red J208-2 U18-9; 3 White-Orange J208-3 U18-5; 4 White-Yellow J208-4 U18-7; 5 White-Green J208-5 U19-11; 6 White-Blue J208-7 U19-9; 7 White-Violet J208-8 U19-5; 8 White-Gray J208-9 U19-7.

Dedicated grounded switches (left-hand column, D1-D8, no matrix address): D1 Orange-Brown J205-1 U17-5 "Left Coin Chute"; D2 Orange-Red J205-2 U17-7 "Center Coin Chute"; D3 Orange-Black J205-3 U17-11 "Right Coin Chute"; D4 Orange-Yellow J205-4 U17-9 "4th Coin Chute"; D5 Orange-Green J205-6 U16-9 "Normal Function: Srv Crdts / Test Function: Escape"; D6 Orange-Blue J205-7 U16-11 "Normal Function: Volume Dn / Test Function: Down"; D7 Orange-Violet J205-8 U16-7 "Normal Function: Volume Up / Test Function: Up"; D8 Orange-Gray J205-9 U16-5 "Normal Function: Begin Test / Test Function: Enter".

Flipper Grounded Switches (right-hand column, F1-F8, no matrix address): F1 Black-Green J208-13 "Lower Right Flipper E.O.S."; F2 Blue-Violet J212-12 "Lower Right Flipper Opto" **[OPTO]**; F3 Black-Blue J208-12 "Lower Left Flipper E.O.S."; F4 Blue-Gray J212-11 "Lower Left Flipper Opto" **[OPTO]**; F5 Black-Violet J208-11 "Upper Right Flipper E.O.S." (position not fitted -- see switch-locations.md); F6 Black-Yellow J212-10 "Upper Right Flipper Opto" **[OPTO]** (position not fitted); F7 Black-Gray J208-10 "Upper Left Flipper E.O.S."; F8 Black-Blue J212-9 "Upper Left Flipper Opto" **[OPTO]**.

Matrix cells, one row per printed column (each column's own eight rows top to bottom):

- Column 1 (11-18): 11 Inner Left Loop; 12 Upper Loop; 13 Start Button; 14 Plumb Bob Tilt; 15 Jet Exit; 16 Left Outlane; 17 Right Return Lane; 18 Shooter Lane.
- Column 2 (21-28): 21 Slam Tilt; 22 Coin Door Closed; 23 Not Used; 24 Always Closed; 25 Right Eject Rubber; 26 Left Return Lane; 27 Right Outlane; 28 "You" Standup Target.
- Column 3 (31-38): 31 Trough Eject **[OPTO]**; 32 Trough Ball 1 **[OPTO]**; 33 Trough Ball 2 **[OPTO]**; 34 Trough Ball 3 **[OPTO]**; 35 Trough Ball 4 **[OPTO]**; 36 Volcano Stack **[OPTO]**; 37 "Mystery" Eject; 38 Right Eject.
- Column 4 (41-48): 41 Lock Ball 1 **[OPTO]**; 42 Lock Ball 2 **[OPTO]**; 43 Lock Ball 3 **[OPTO]**; 44 "Mine Shaft"; 45 Left Loop; 46 Left Bank Top; 47 Left Bank Center; 48 Left Bank Bottom.
- Column 5 (51-58): 51 "Travi"; 52 "Com"; 53 2-Way Popper; 54 "We Are" Standup Target; 55 "Watching" Standup Target; 56 "Perimeter Defense"; 57 Left Ramp Enter; 58 Left Ramp Exit.
- Column 6 (61-68): 61 Left Slingshot; 62 Right Slingshot; 63 Left Jet Bumper; 64 Right Jet Bumper; 65 Bottom Jet Bumper; 66 Not Used; 67 Right Ramp Enter; 68 Right Ramp Exit.
- Column 7 (71-78): 71 (A)my; 72 A(m)y; 73 Am(y); 74 (C)ongo; 75 C(o)ngo; 76 Co(n)go; 77 Con(g)o; 78 Cong(o).
- Column 8 (81-88): 81 Not Used; 82 Not Used; 83 Not Used; 84 Not Used; 85 Not Used; 86 Not Used; 87 Not Used; 88 Not Used.

Shaded ("OPTO, TYPICALLY CLOSED") cells total exactly nine addresses: 31, 32, 33, 34, 35, 36 (column 3, rows 1-6) and 41, 42, 43 (column 4, rows 1-3). No other matrix position, and none of F1/F3/F5/F7 (the EOS positions), is shaded.
