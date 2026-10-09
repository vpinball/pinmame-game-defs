# The Sopranos — General Illumination circuit and fuses

Transcribed from `Stern_2005_The_Sopranos_Service_Manual.pdf`, PDF page 126 (printed Section 5, Chapter 2, page 109,
"General Illumination Circuit Detailed Wiring Diagram"), read from a 198 dpi render (`gi-wiring.webp`), with the G.I.
rows of the Quick Reference Fuse Chart on PDF page 3.

## Relay

`Partial View I/O POWER DRIVER BD. 520-5137-01`: data latch U206 (74HCT273, `D0` pin 3 to `1Q` pin 2) drives transistor
Q200 (2N3904) through R254 (1K) as the `RELAY DRIVER`; diode D229 (1N4004) across the coil; the `G.I. RELAY` (contacts
8, 5, 6 / 7, 1, 3, 2, 4) switches the `G.I. 5.7v AC INPUT FROM XFRMR` (YEL, YEL, YEL, YEL-WHT, YEL-WHT, YEL-WHT on J14
pins 1-6) to `General Illumination (G.I.) Bulbs (5.7v AC)` through four `5A 250v SLO-BLO Fuses F27 F26 F25 F24` and J15.

## Circuits

| Circuit | Jumper | Code letter | Wires | Location as printed | Bulbs as printed |
| --- | --- | --- | --- | --- | --- |
| 1 | J15-P6 to J15-P1 (Fuse F24) | B | BRN-WHT to WHT-BRN | Location: Back Panel X12 | 12 ea. #44 Bulb (#1 #2 ... #12*) |
| 2 | J15-P7 to J15-P2 (Fuse F25) | Y | YELLOW to WHT-YEL | Location: Mid. / Lwr. Rt. P/F X13 | 11 + 1 ea. #44 + #555 (#1 #2 ... #13*); beside it: `4 ea. #44 Yellow Bulb where noted with ▼` |
| 3 | J15-P8 to J15-P3 (Fuse F26) | G | GREEN to WHT-GRN | Location: Upr. Rt. Playfield X8 + US Coin Door X2 (Euro X3) | 8 ea. #44 Bulb, and `2 ea. #555 Bulb` on the coin door (`Coin Door`, `Wiring Harness Connector`, `On Coin Door`, YEL-WHT / YEL) |
| 4 | J15-P9 to J15-P4 (Fuse F27) | V | VIOLET to WHT-VIO | Location: Middle / Lower Left Playfield X12 | 10 + 2 ea. #44 + #555 (#1 #2 ... #12*) |

Footnote: `* G.I. Bulb quantities may change during production.` A note beside circuit 1: `Note: Various Colors, see
Page 62 for Part Numbers.`

## Playfield-bottom drawing

The left of the page draws the bottom of the playfield `as if leaning up against the Backbox` (a mirror image; the
edge marked `This Edge is "Top of Playfield"` is the rear). Each G.I. socket carries a black circle with its circuit
letter. Read independently on the crop: 33 playfield circles, 12 `V`, 8 `G` and 13 `Y` (the printed circuit 2 total
is 11 + 1). Four `Y` circles on the right edge carry the `▼` mark. Two callout boxes name reflector-mounted G.I.:
`Above Playfield: G.I.s in Light Reflector on Right Wire Ramp.` and `Above Playfield: G.I.s in Light Reflectors X2 on
Spinner Bracket`. Below it a box `Below: Located at the top of the P/F, rear view of the Back Panel.` shows ten `B`
circles in a row and control lamps 65-72 (`For all Control Lamps, see Sec. 3, Chp. 2, Pages 22-23`), with two
`Flash Lamp Q26` sockets each marked `B` (`For all Flash Lamps, see Sec. 3, Chp. 2, Pages 18-21`); the inset is titled
`GIs on rear Back Panel (X12)`.

## Fuse chart rows (PDF page 3, "QUICK REFERENCE FUSE CHART", I/O Power Driver Board)

| Fuse | Rating | Circuit |
| --- | --- | --- |
| F24 | 5A 250v S.B. | 6.3v AC G.I. Lamps (BRN-WHT WHT-BRN) |
| F25 | 5A 250v S.B. | 6.3v AC G.I. Lamps (YEL WHT-YEL) |
| F26 | 5A 250v S.B. | 6.3v AC G.I. Lamps (GRN WHT-GRN) |
| F27 | 5A 250v S.B. | 6.3v AC G.I. Lamps (VIO WHT-VIO) |
| F6 | 7A 250v S.B. | 50v DC Primary High Power Coils/Flippers (on Power Box) |
| F7 | 5A 250v S.B. | 20v DC Low Power Coils |
| F20 | 4A 250v S.B. | 50v DC Magnets |
| F21 | 3A 250v S.B. | 50v DC Coils |
| F22 | 8A 250v S.B. | 18v DC Controlled Lamps |

The fuse chart prints the G.I. supply as 6.3v AC where the wiring diagram prints 5.7v AC; both are kept as printed.
The same page lists the playfield fuses `3A 250v S.B. 50v DC Right Flipper (BLU-YEL RED-YEL)` and `... Left Flipper
(GRY-YEL RED-YEL)` under the playfield near the assembly.
