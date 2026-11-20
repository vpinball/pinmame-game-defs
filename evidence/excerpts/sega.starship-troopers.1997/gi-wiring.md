# Starship Troopers — General Illumination circuit wiring

Read from `Sega_1997_Starship_Troopers_Manual.pdf` (IPDB 4341), PDF page 103, printed Section 5, Chapter 2, page 89,
"Playfield Wiring / General Illumination Circuit Detailed Wiring Diagram", from a 300 dpi render checked against a
Windows OCR pass. The crop `gi-wiring.webp` renders the page.

Board side, I/O POWER DRIVER BOARD 520-5137-01:

- U206 74HCT273 Data Latch, D0 (pin 3) to 1Q (pin 2), through R254 1K Ω to Q200 2N3904 Transistor ("RELAY DRIVER"),
  which grounds the G.I. RELAY coil; the coil (relay pins 7 and 8) is fed from 20v DC with D229 1N4004 Diode across it.
- "G.I. 6.3v AC INPUT FROM XFRMR": J14 pins 1-3 YEL, pins 4-6 YEL/WHT, from the transformer's 6.3v AC secondary.
- "5A 250v SLO-BLO Fuses" F27, F26, F25, F24 between the relay and J15 pins 4, 3, 2 and 1.
- J15 pin labels: 9 VIOLET, 8 GREEN, 7 YELLOW, 6 BRN/WHT, 5 blank, 4 WHT/VIO, 3 WHT/GRN, 2 WHT/YEL, 1 WHT/BRN.
- "General Illumination (G.I.) Bulbs (6.3v AC)".

"G.I. Bulbs (6.3v AC) General Location (Strings Noted by Fuse & Wire Colors):"

| Circuit | Fuse | Pins | Wires | Location as printed | Bulbs as printed |
| --- | --- | --- | --- | --- | --- |
| 1 | F24 | J15-P6 to J15-P1 | BRN/WHT to WHT/BRN | Under Upper Left Playfield: | 10 Ea. #44 Bulb ✻ |
| 2 | F25 | J15-P7 to J15-P2 | YEL to WHT/YEL | Under Lower Left Playfield: | 7 Ea. #44 Bulb ✻ |
| 2 | F25 | | | Above Lt. Mid. P/F & Lt. Return Ln.: | 2 Ea. #555 Bulb ✻ |
| 3 | F26 | J15-P8 to J15-P3 | GRN to WHT/GRN | Under Upper Right Playfield: | 7 Ea. #44 Bulb ✻ |
| 3 | F26 | | | In Coin Door: | 2 Ea. #555 Bulb ✻ |
| 4 | F27 | J15-P9 to J15-P4 | VIO to WHT/VIO | Under Lower Right Playfield: | 6 Ea. #44 Bulb ✻ |
| 4 | F27 | | | Above Rt. Ramp & Rt. Return Ln.: | 2 Ea. #555 Bulb ✻ |

The circuit, fuse, pin and wire cells are printed once per circuit; the rows that repeat a circuit carry only the
second location line, which the page prints under the first.

String drawing to the right of the legend: "WHT/BRN (Fuse F24)" Circuit 1, bulbs numbered #1, #2 … #10;
"WHT/YEL (Fuse F25)" Circuit 2, #1, #2 … #9; "WHT/GRN (Fuse F26)" Circuit 3, #1 on the playfield side of a "Coin Door
Wiring Harness Connector", then "on Coin Door" #8 and #9 on YEL/WHT and YEL; "WHT/VIO (Fuse F27)" Circuit 4, #1, #2 …
#8. The return wires BRN/WHT, YEL, GRN and VIO run back to J15.

Note on the page: "✻ G.I. Bulb quantities may change during production."
