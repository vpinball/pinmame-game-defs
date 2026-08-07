# Judge Dredd — Solenoid/Flasher Table

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF page 112, printed page 2-44, the
SOLENOID/FLASHER TABLE, including its General Illumination and Flipper Circuits sub-tables. Produced
by rendering the retained PDF at 300 dpi with `pdftoppm` and reading the table directly. The same
table is reprinted in Section 3 on PDF page 119 (printed 3-5).

Legend printed under the table: `J1XX = Power Driver Board; J9XX - Fliptronic II Board; 24-6549 = #44
Bulb; 24-8704 = #89 Bulb; 24-8768 = #555 Bulb; 24-8802 = #906 Bulb`.

The table has a **Cabinet** sub-column under both Voltage Connections and Drive Connections. It was
swept for every row: **no solenoid, flasher, GI string or flipper circuit on this machine uses either
Cabinet column.** Every drive is Playfield or Backbox.

## Solenoids and flashers

| Sol. | Function | Type | Voltage PF | Voltage BB | Xistor | Drive PF | Drive BB | Wire | Part / Flashlamp PF | Flashlamp BB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Globe Magnet | High Power | J130-1 | | Q82 | J107-3 | | Vio-Brn | A-12158-1 | |
| 02 | Left Popper | High Power | J130-2 | | Q80 | J107-3 | | Vio-Red | AE-26-1200 | |
| 03 | Right Popper | High Power | J130-4 | | Q78 | J107-3 | | Vio-Org | AE-23-800 | |
| 04 | Globe Arm | High Power | J130-5 | | Q76 | J118-2 | | Vio-Yel | 14-7989 | |
| 05 | Reset Drop Target | High Power | J130-6 | | Q64 | J107-3 | | Vio-Grn | AE-24-900 | |
| 06 | Globe Motor | High Power | J130-7 | | Q66 | J118-2 | | Vio-Blu | 14-7985 | |
| 07 | Knocker | High Power | J130-8 | | Q68 | J107-3 | | Vio-Blk | AE-23-800 | |
| 08 | Right Shooter | High Power | J130-9 | | Q70 | J107-3 | | Vio-Gry | AE-23-800 | |
| 09 | Left Shooter | Low Power | J127-1 | | Q58 | J107-2 | | Brn-Blk | AE-23-800 | |
| 10 | Trip Drop Target | Low Power | J127-3 | | Q56 | J107-2 | | Brn-Red | AE-27-1200 | |
| 11 | Diverter | Low Power | J127-4 | | Q54 | J107-2 | | Brn-Org | AE-25-1000 | |
| 12 | Not Used | Low Power | --- | | Q52 | --- | | Brn-Yel | --- | |
| 13 | Trough | Low Power | J127-6 | | Q50 | J107-2 | | Brn-Grn | AE-26-1500 | |
| 14 | Not Used | Low Power | --- | | Q48 | --- | | Brn-Blu | --- | |
| 15 | Left Slingshot | Low Power | J127-8 | | Q46 | J107-2 | | Brn-Vio | AE-27-1200 | |
| 16 | Right Slingshot | Low Power | J127-9 | | Q44 | J107-2 | | Brn-Gry | AE-27-1200 | |
| 17 | Judge Fire Flashers | Flasher | J126-1 | J125-1 | Q42 | J107-6 | J106-5 | Blk-Brn | 24-8802 (1) | 24-8802 (1) |
| 18 | Judge Fear Flashers | Flasher | J126-2 | J125-2 | Q40 | J107-6 | J106-5 | Blk-Red | 24-8802 (1) | 24-8802 (1) |
| 19 | Judge Death Flashers | Flasher | J126-3 | J125-3 | Q38 | J107-6 | J106-5 | Blk-Org | 24-8802 (1) | 24-8802 (1) |
| 20 | Judge Mortis Flashers | Flasher | J126-4 | J125-5 | Q36 | J107-6 | J106-5 | Blk-Yel | 24-8802 (1) | 24-8802 (1) |
| 21 | Pursuit Left Flashers | Flasher | J126-5 | J125-6 | Q28 | J107-6 | J106-5 | Blu-Grn | 24-8802 (2) | 24-8802 (1) |
| 22 | Pursuit Right Flashers | Flasher | J126-6 | J125-7 | Q30 | J107-6 | J106-5 | Blu-Blk | 24-8802 (2) | 24-8802 (1) |
| 23 | Blackout Flashers | Flasher | J126-7 | J125-8 | Q34 | J107-6 | J106-5 | Blu-Vio | 24-8802 (1) | 24-8802 (2) |
| 24 | Cursed Earth Flashers | Flasher | J126-8 | --- | Q32 | J107-6 | --- | Blu-Gry | 24-8802 (2) | --- |
| 25 | Lower Left Flashers | Gen. Purpose | J122-1 | J124-1 | Q26 | J107-6 | J106-5 | Blu-Brn | 24-8704 (2) | 24-8802 (2) |
| 26 | Globe Flashers | Gen. Purpose | J122-2 | J124-2 | Q24 | J107-6 | J106-5 | Blu-Red | 24-8802 (1) | 24-8802 (2) |
| 27 | Right Ramp Flashers | Gen. Purpose | J122-3 | J124-3 | Q22 | J107-6 | J106-5 | Blu-Org | 24-8704 (2) | 24-8802 (1) |
| 28 | Insert Flashers | Gen. Purpose | --- | J124-5 | Q20 | --- | J106-5 | Blu-Yel | --- | 24-8802 (3) |

Rows 12 and 14 are printed `Not Used` with blank voltage connections, blank drive connections and a
blank part number, but they still list a populated drive transistor (Q52 and Q48). The blank
connection columns, not the presence of a transistor, are what prove nothing is fitted.

Row 28 is the mirror-image case: it has a populated Backbox voltage connection, a populated Backbox
drive connection and three `#906` backbox flashlamps, but blank Playfield columns throughout. It is a
real, driven output with no playfield emitter at all.

## General Illumination

| Printed | Function | Type | Voltage PF | Voltage BB | Xistor | Drive PF | Drive BB | Wire | Bulb PF | Bulb BB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | String 1 | G.I. | J-120-1 | J-121-1 | Q18 | J-120-7 | J-121-6 | Wht-Brn | 24-6549 (`#44`) | 24-8768 (`#555`) |
| 02 | String 2 | G.I. | J-120-2 | J-121-2 | Q10 | J-120-8 | J-121-8 | Wht-Org | 24-8768 (`#555`) | 24-8768 (`#555`) |
| 03 | String 3 | G.I. | J-120-3 | J-121-3 | Q14 | J-120-9 | J-121-7 | Wht-Yel | 24-6549 (`#44`) | 24-8768 (`#555`) |
| 04 | String 4 | G.I. | J-120-5 | J-121-5 | Q16 | J-120-10 | J-121-10 | Wht-Grn | 24-8768 (`#555`) | 24-8768 (`#555`) |
| 05 | String 5 | G.I. | J-121-6 | --- | Q12 | J-120-11 | --- | Wht-Vio | 24-8768 (`#555`) | --- |

String 5's Playfield voltage connection is printed `J-121-6`, a J121 (backbox) pin sitting in the
Playfield column, and the same pin is already printed as String 1's Backbox drive connection. The
print is preserved verbatim rather than corrected; String 5's drive connection `J-120-11` is a J120
(playfield) pin, and its Backbox columns are blank, so the row otherwise reads as playfield-only.

There is no footnote on this page marking any GI string non-dimmable, unlike several other WPC
manuals.

## Flipper Circuits

| Flipper | Winding | Voltage conn. | Power Xistor | Hold Xistor | Drive conn. | Power wire | Hold wire | Coil | Coil colour |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lower Left | Lwr. Lt. Power | J907-7 (Gry-Yel) | Q3 | | J902-9 | Blu-Gry | | FL-11629 | BLUE |
| Lower Left | Lwr. Lt. Hold | J907-7 (Gry-Yel) | | Q9 | J902-7 | | Org-Blu | FL-11629 | BLUE |
| Lower Right | Lwr. Rt. Power | J907-9 (Blu-Yel) | Q4 | | J902-13 | Blu-Vio | | FL-11629 | BLUE |
| Lower Right | Lwr. Rt. Hold | J907-9 (Blu-Yel) | | Q11 | J902-11 | | Org-Grn | FL-11629 | BLUE |
| Upper Left | Up Lt. Power | J907-1 (Gry-Yel) | Q1 | | J902-3 | Blk-Blu | | FL-11629 | BLUE |
| Upper Left | Up Lt. Hold | J907-1 (Gry-Yel) | | Q5 | J902-1 | | Org-Gry | FL-11629 | BLUE |
| Upper Right | Up Rt. Power | J907-4 (Blu-Yel) | Q2 | | J902-6 | Blk-Yel | | FL-11630 | RED |
| Upper Right | Up Rt. Hold | J907-4 (Blu-Yel) | | Q7 | J902-4 | | Org-Vio | FL-11630 | RED |

Four flippers are fitted, each with a separate power and hold winding. This table assigns them no
numbers at all — there is no printed 29-36 flipper numbering on this page — so there is nothing here
to mistake for a public solenoid address. The upper right flipper is the one circuit that uses a
different coil, `FL-11630` (Red) rather than `FL-11629` (Blue).
