# Starship Troopers — Backbox I/O Power Driver Board Detailed Wiring Diagram

Read from `Sega_1997_Starship_Troopers_Manual.pdf` (IPDB 4341), PDF page 102, printed Section 5, Chapter 1 page 88,
"Backbox I/O Power Driver Board Detailed Wiring Diagram", from 250-500 dpi renders of the scan. The page is one
drawing of the I/O Power Driver Board 520-5137-01's output connectors J6-J9 with each driver's label, wire colour and
load, the three bridge supplies and the optional printer connectors. Every connector row the page draws is listed;
`✻n` is the printed bulb or load count. Wire colours keep the page's slash form.

## J6 flash lamps (20V DC low power)

| J6 pin | Driver label as printed | Transistor | Wire | Load as printed | Bulb label as printed |
| --- | --- | --- | --- | --- | --- |
| 1 | Flash: Red ✻4 | Q25 | BLK/BRN | FLASH 1 | #555 Bulb ✻4 |
| 2 | Flash: Yellow ✻4 | Q26 | BLK/RED | FLASH 2 | #555 Bulb ✻4 |
| 3 | Flash: Green ✻4 | Q27 | BLK/ORG | FLASH 3 | #555 Bulb ✻4 |
| 4 | Flash: Blue ✻4 | Q28 | BLK/YEL | FLASH 4 | #555 Bulb ✻4 |
| 5 | Flash: Multiball ✻4 | Q29 | BLK/GRN | FLASH 5 | #89 + #906 Bulbs ✻1+✻3 |
| 6 | Flash: Lt. Ramp ✻4 | Q30 | BLK/BLU | FLASH 6 | #89 Bulb ✻4 |
| 7 | Flash: Rt. Ramp ✻4 | Q31 | BLK/VIO | FLASH 7 | #89 Bulb ✻4 |
| 8 | Flash: Pops ✻2 | Q32 | BLK/GRY | FLASH 8 | #89 Bulb ✻2 |
| 10 | (supply) | | ORG | 20V DC, common to every bulb group | |

Each group is drawn as that many bulb symbols in parallel between the driver line and the ORG 20V DC line. The
`#555` label on groups 1-4 disagrees with the Coils Detailed Chart Table (DR. 6, `#906 Bulb / 165-5004-00`) and with
the 4X Light & Clear Plastic Assembly's parts list (printed page 81, item 21B `#906 Wedge Base Bulb` 165-5004-00).

## J7 low-current coils (20V DC low power)

| J7 pin | Driver label as printed | Transistor | Wire | Load as printed |
| --- | --- | --- | --- | --- |
| 1 | | | BRN | 20V DC (Not Used) |
| 2 | Stepper Motor #1 | Q17 | VIO/BRN | COIL 17 |
| 3 | Stepper Motor #2 | Q18 | VIO/RED | COIL 18 |
| 4 | Stepper Motor #3 | Q19 | VIO/ORG | COIL 19 |
| 6 | Stepper Motor #4 | Q20 | VIO/YEL | COIL 20 |
| 7 | Not Used | Q21 | VIO/GRN | COIL 21, dashed box "COIL NOT USED" |
| 8 | Not Used | Q22 | VIO/BLU | COIL 22, dashed box "COIL NOT USED" |
| 9 | Flash: Brain Bug ✻2 | Q23 | VIO/BLK | COIL 23, two bulbs labelled "#89 Bulb ✻2" on the ORG 20V DC line |
| 10 | Option Coin Meter | Q24 | (VIO/GRY) | COIL 24, dashed box "COIL NOT USED (OPTIONAL)", labelled CABINET; supply RED +5V DC from J16-P7 I/O BOARD |

Stepper motor, drawn to the right of COIL 17-20: "STEPPER MOTOR SPI Nº 041-5062-00", "Haydon Nº 36864-12", with two
centre-tapped windings. Traced at 500 dpi:

| Phase line | Joins | Motor lead |
| --- | --- | --- |
| COIL 17 (Q17) | the fourth DOTS diode | RED, one end of the first winding |
| COIL 18 (Q18) | the second DOTS diode | GRN, one end of the second winding |
| COIL 19 (Q19) | the third DOTS diode | BLK, the other end of the first winding |
| COIL 20 (Q20) | the first DOTS diode | BLU, the other end of the second winding |
| supply bus | every diode's other side | both WHT centre taps; "GRY/RED +12V DC" from J16-P3 I/O BOARD |

Note beside the diodes, verbatim: "All four (4) 1N4004, Diodes, are located on Terminal Strips below the playfield."

## J8 high-current coils group 1 (50V DC)

| J8 pin | Driver label as printed | Transistor | Wire | Coil as printed | Load | Coil-side supply |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Trough Up-Kicker | Q1 | BRN/BLK | 26-1200 | COIL 1 | YEL/VIO 50V DC bus |
| 3 | Auto Launch | Q2 | BRN/RED | 24-940 | COIL 2 | YEL/VIO 50V DC bus |
| 4 | VUK | Q3 | BRN/ORG | 26-1200 | COIL 3 | YEL/VIO 50V DC bus |
| 5 | Super VUK | Q4 | BRN/YEL | 26-1200 | COIL 4 | YEL/VIO 50V DC bus |
| 6 | Left Magnet | Q5 | BRN/GRN | 22-650 (Magnet) | COIL 5 | 3A Slo-Blo fuse to VIO/YEL 50V DC, J10-P3 I/O BOARD |
| 7 | Right Magnet | Q6 | BRN/BLU | 22-650 (Magnet) | COIL 6 | 3A Slo-Blo fuse to VIO/YEL 50V DC, J10-P3 I/O BOARD |
| 8 | Brain Bug | Q7 | BRN/VIO | 22-1080 | COIL 7 | RED/WHT to a 3A Slo-Blo fuse to VIO/YEL 50V DC, J10-P3 I/O BOARD |
| 9 | European Token Dispenser | Q8 | (BRN/GRY) | dashed box "COIL NOT USED (OPTIONAL)" | COIL 8 | YEL/VIO 50V DC bus |

The YEL/VIO 50V DC bus runs to "J10-P4 & P5 I/O BOARD". Note above the three fuses, verbatim: "Fuses are located
under playfield by assembly." Only the COIL 7 branch prints a wire colour between its coil and its fuse.

## J9 high-current coils group 2 (50V DC)

| J9 pin | Driver label as printed | Transistor | Wire | Coil as printed | Load | Coil-side supply |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Left Turbo Bumper | Q9 | BLU/BRN | 26-1200 | COIL 9 | YEL/VIO 50V DC bus |
| 2 | Bottom Turbo Bumper | Q10 | BLU/RED | 26-1200 | COIL 10 | YEL/VIO 50V DC bus |
| 4 | Right Turbo Bumper | Q11 | BLU/ORG | 26-1200 | COIL 11 | YEL/VIO 50V DC bus |
| 5 | Left Slingshot | Q12 | BLU/YEL | 26-1200 | COIL 12 | YEL/VIO 50V DC bus |
| 6 | Right Slingshot | Q13 | BLU/GRN | 26-1200 | COIL 13 | YEL/VIO 50V DC bus |
| 7 | Mini Flipper | Q14 | BLU/BLK | 22-1080 | COIL 14 | BLU/YEL to a 3A Slo-Blo fuse to RED/YEL 50V DC, J10-P1 & P2 I/O BOARD |
| 8 | Left Flipper | Q15 | ORG/GRY | 23-1100 | COIL 15 | GRY/YEL to a 3A Slo-Blo fuse to RED/YEL 50V DC, J10-P1 & P2 I/O BOARD |
| 9 | Right Flipper | Q16 | ORG/VIO | 23-1100 | COIL 16 | BLU/YEL to a 3A Slo-Blo fuse to RED/YEL 50V DC, J10-P1 & P2 I/O BOARD |

The same "Fuses are located under playfield by assembly." note stands under the three flipper fuses. Each coil is
drawn with a diode across it.

## Supplies

| Bridge as printed | Input | Fuse | Output |
| --- | --- | --- | --- |
| BRIDGE 2, 20V LOW CURRENT COILS (BRDG 2) | J17-P6 16V AC; J17-P7 16V AC through F7 | F7 5A Slo-Blo | 20V DC LOW POWER (J6 and J7) |
| BRIDGE 20, CONTROLLED LAMPS (BRDG 20) | J17-P8 13V AC; J17-P9 13V AC through F22 | F22 8A Slo-Blo | 18V DC to J13-P10 |
| BRIDGE 1, 50V HIGH CURRENT COILS (BRDG 1) | J11-P3 48V AC through F6; J11-P2 48V AC | F6 7A Slo-Blo | 50V DC through F21 (3A Slo-Blo) to 50V DC HIGH POWER (J8 and J9), and through F20 (3A Slo-Blo) to "Magnet J10 P3" |

## Printer connectors and notes

J3, pins 12 to 1: WHT/BLK; N/U; GRN/WHT Printer Control; BRN/WHT Printer Clock; KEY; N/U; N/U; N/U; N/U; N/U;
N/U; BRN Printer Busy. J2, pins 10 to 1, wire boxes top to bottom: ORG/WHT, ORG/GRY, ORG/VIO, ORG/BLU, ORG/GRN,
ORG/YEL, KEY, ORG/BLK, ORG/RED, ORG/BRN; the signal labels beside them read Printer Enable, Output 7, Output 6, Output
5, Output 4, Output 3, Output 2, Output 1, Output 0, nine labels for ten pins, printed too tightly on the scan to pair
each with its pin. The harness runs to boxes labelled CABINET and PRINTER INTERFACE and a dashed box NOT USED; a
vertical label beside it, partly illegible on the scan, reads "J2-P3-10 N/U & J3-P1-P11 N/U USED W/OPTIONAL PRINTER
HARNESS". This record uses none of the printer pins.

Notes on the page, verbatim:

- "Note: All Coils require diodes. Some diodes are located on Terminal Strips (under playfield) & not on the coil
  itself." Beside it, "D iode / O n / T erminal / S trip".
- "In this game, Q17, Q18, Q19 & Q20 have diodes on Terminal Strips. See the next chapter (Chp. 2) of this section
  (Sec. 5) for Playfield Diode Terminal Strip & Fuse Locations."
- "Note: For the General Illumination (G.I.) Circuit Detailed Wiring Diagram, see the next page."
