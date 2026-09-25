# Theatre of Magic — Power Driver Board connectors J119 and J120

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 149, printed page 3-27: the second page of the
Power Driver Board A-12697-3 connector list that begins on printed 3-26 (PDF page 148). Left
column, J119 and J120 blocks, complete. Verified against a native-resolution render of the page.

The list is specific to this game, not a generic board sheet: on the same page J126-1/-2 read "Sol 17
to playfield motor" / "Sol 18 to playfield motor" (Box Clockwise / Box Counter Clockwise), J126-3,
J126-6 and J126-7 read "Not Used" (solenoids 19, 22 and 23 are printed NOT USED in the solenoid
table), and J126-5 reads "Sol 21 to playfield coil" (Top Kickout).

| Pin | Printed text |
| --- | --- |
| J119-1 | White-Violet 6.8VAC G.I. to A-17051-1 J2-3 |
| J119-2 | Key |
| J119-3 | Violet Return G.I. to A-17051-1 J2-5 |
| J120-1 | Brown Return G.I. to playfield |
| J120-2 | Orange Return G.I. to playfield |
| J120-3 | Not Used |
| J120-4 | Key |
| J120-5 | Not Used |
| J120-6 | Not Used |
| J120-7 | White-Brown 6.8VAC to playfield |
| J120-8 | White-Orange 6.8VAC to playfield |
| J120-9 | Not Used |
| J120-10 | Not Used |
| J120-11 | Not Used |

A-17051-1 is the Coin Door Interface PCB Assembly (printed 3-32, PDF page 154; see
`coin-door-interface-gi.md`).

Reading: J120 carries G.I. strings 01 and 02 (Brown/White-Brown and Orange/White-Orange, the wire
colours the Solenoid/Flasher Table prints for strings 01 and 02) to the playfield. The Solenoid/Flasher
Table prints the same pins under its Backbox columns; see `general-illumination.md`. J119 carries a
White-Violet / Violet pair, string 05's colours (J121-11 / J121-6), to the coin door interface board.
