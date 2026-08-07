# The Addams Family — Solenoid Table

Transcribed from `Bally_1992_The_Addams_Family_Operator_s_Handbook_January_1991_OCR_searchable_has_lamp_and_switch_matrices.pdf`,
printed page 5, the Solenoid Table, together with the Flipper Coils list printed on the same page.
Both PDFs retained for this machine carry an OCR text layer, but the OCR misreads digits and glyphs
badly on this two-column board layout (e.g. "Uuthole" for "Outhole", "M,." for "AE", "J!rn" for
"Brn"), so this is a visual re-transcription from the rendered page, not the OCR text. The General
Illumination Circuits block printed on the same page is transcribed separately as
`general-illumination.md`.

| Sol. | Function | Type | Wire | Connection | Driver | Part number |
| ---: | --- | --- | --- | --- | --- | --- |
| 01 | Chair Kickout | High Power | Vio-Brn | J130-1 | Q82 | AE-26-1200 |
| 02 | Thing Knocker | High Power | Vio-Red | J132-2 | Q80 | AE-23-800 |
| 03 | Ramp Diverter | High Power | Vio-Orn | J130-4 | Q78 | AE-26-1500 |
| 04 | Ball Release | High Power | Vio-Yel | J130-5 | Q76 | AE-26-1200 |
| 05 | Outhole | High Power | Vio-Grn | J130-6 | Q64 | AE-27-1200 |
| 06 | Thing Magnet | High Power | Vio-Blu | J130-7 | Q66 | A-12158-1 |
| 07 | Thing Kickout | High Power | Vio-Blk | J130-8 | Q68 | AE-23-800 |
| 08 | Lockup Kickout | High Power | Vio-Gry | J130-9 | Q70 | AE-26-1200 |
| 09 | Upper Left Jet | Low Power | Brn-Blk | J127-1 | Q58 | AE-26-1200 |
| 10 | Upper Right Jet | Low Power | Brn-Red | J127-3 | Q56 | AE-26-1200 |
| 11 | Center Left Jet | Low Power | Brn-Org | J127-4 | Q54 | AE-26-1200 |
| 12 | Center Right Jet | Low Power | Brn-Yel | J127-5 | Q52 | AE-26-1200 |
| 13 | Lower Jet | Low Power | Brn-Grn | J127-6 | Q50 | AE-26-1200 |
| 14 | Left Slingshot | Low Power | Brn-Blu | J127-7 | Q48 | AE-27-1200 |
| 15 | Right Slingshot | Low Power | Brn-Vio | J127-8 | Q46 | AE-27-1200 |
| 16 | Left Magnet | Low Power | Brn-Gry | J127-9 | Q44 | 20-9247 12V |
| 17 | Telephone/Upper Right Ramp | Flasher | Blk-Brn | J126-1 / J125-1 | Q42 | #906 |
| 18 | Train/Upper Left Ramp | Flasher | Blk-Red | J126-2 / J125-2 | Q40 | #906 |
| 19 | Lower Ramp/Jet Bumpers (2) | Flasher | Blk-Org | J126-3 / J125-3 | Q38 | #906 |
| 20 | Left Lightning Bolt/Mini Flipper | Flasher | Blk-Yel | J126-4 / J125-5 | Q36 | #906 |
| 21 | Right Lightning Bolt/Swamp | Flasher | Blu-Grn | J126-5 / J125-6 | Q28 | #906 |
| 22 | The Power/Backbox Cloud (3) | Flasher | Blu-Blk | J126-6 / J125-7 | Q30 | #906 |
| 23 | Upper Magnet | Low Power | Blu-Vio | J126-7 / J125-8 | Q34 | 20-9247 12V |
| 24 | Right Magnet | Low Power | Blu-Gry | J126-8 / J125-9 | Q32 | 20-9247 12V |
| 25 | Thing Motor | Flasher | Blu-Brn | J122-1 | Q26 | 14-7966 12V |
| 26 | Thing Eject Hole | Flasher | Blu-Red | J122-2 | Q24 | AE-30-2000 |
| 27 | Bookcase Motor | Flasher | Blu-Org | J122-3 | Q22 | 14-7969 12V |
| 28 | Swamp Release | Flasher | Blu-Yel | J122-4 | Q20 | AE-30-2000 |

## Flipper coils (same page)

Printed below the GI block without a solenoid number (public addresses per `wpc-fliptronic.json`,
not the printed circuit order):

| Printed label | Wire | Connection | Part number |
| --- | --- | --- | --- |
| Upper Left Flipper | Gry-Yel | J109-5 | FL-11753 |
| Upper Right Flipper | Blu-Yel | J109-7 | FL-11630 |
| Lower Left Flipper | Gry-Yel | J109-5 | FL-15411 |
| Lower Right Flipper | Blu-Yel | J109-7 | FL-15411 |

Distinct coil part numbers for each of the four positions (FL-11753 upper-left, FL-11630
upper-right, FL-15411 for both lower flippers) with real wire colors and connectors is one of the
three independent lines of evidence that both upper mini-flippers are genuine fitted hardware, not a
template row; see `flipper-assembly-and-thing-flips.md` for the other two.
