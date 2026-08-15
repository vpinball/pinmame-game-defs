# Revenge From Mars operations manual service-table transcription

Source: *Revenge From Mars Operations Manual*, February 1999, model 50070. Transcribed from PDF pages 86-88 (printed pages 2-46 through 2-48) and visually checked against the rendered pages. The repeated Section 3 copies on PDF pages 90-95 corroborate the same wiring.

## Lamp matrix wiring, printed page 2-46

The manual presents eight columns, each with eight Bank A rows and eight Bank B rows. The PinMAME public bit index is `(column - 1) * 16 + (Bank B ? 8 : 0) + (row - 1)`.

| Column | Bank A wire | Bank A connector | Bank A transistor | Bank B wire | Bank B connector | Bank B transistor |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | YEL-BRN | J108-9 | Q5 | YEL-BRN | J107-10 | Q6 |
| 2 | YEL-RED | J108-10 | Q9 | YEL-RED | J107-11 | Q10 |
| 3 | YEL-ORG | J108-11 | Q13 | YEL-ORG | J107-12 | Q14 |
| 4 | YEL-BLK | J108-12 | Q17 | YEL-BLK | J107-13 | Q18 |
| 5 | YEL-GRN | J108-13 | Q21 | YEL-GRN | J107-14 | Q22 |
| 6 | YEL-BLU | J108-14 | Q25 | YEL-BLU | J107-15 | Q26 |
| 7 | YEL-VIO | J108-15 | Q29 | YEL-VIO | J107-16 | Q30 |
| 8 | YEL-GRY | J108-16 | Q33 | YEL-GRY | J107-17 | Q34 |

| Row | Bank A wire | Bank A connector | Bank A return | Bank B wire | Bank B connector | Bank B return |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | BRN-BLK | J108-1 | Q3 | RED-BRN | J107-1 | Q4 |
| 2 | BRN-RED | J108-2 | Q7 | RED-BLK | J107-2 | Q8 |
| 3 | BRN-ORG | J108-3 | Q11 | RED-ORG | J107-3 | Q12 |
| 4 | BRN-YEL | J108-4 | Q15 | RED-YEL | J107-4 | Q16 |
| 5 | BRN-GRN | J108-5 | Q19 | RED-GRN | J107-5 | Q20 |
| 6 | BRN-BLU | J108-6 | Q23 | RED-BLU | J107-6 | Q24 |
| 7 | BRN-VIO | J108-7 | Q27 | RED-VIO | J107-7 | Q28 |
| 8 | BRN-GRY | J108-8 | Q31 | RED-GRY | J107-8 | Q32 |

The manual marks these twelve cells NOT USED: `11A`, `12A`, `14A`, `22A`, `31A`, `32A`, `33A`, `34A`, `58A`, `38B`, `48B`, and `72B`.

The printed page places Left Slingshot Spotlight at `18B` and Right Slingshot Spotlight at `28B`. PinMAME's complete machine-test walk finds the opposite runtime names; the canonical definition follows the measured machine-test mapping and retains this disagreement explicitly.

## Switch wiring, printed page 2-47

| Matrix column | Wire | Connector | Driver |
| --- | --- | --- | --- |
| 1 | GRN-BRN | J116-1 | U45-18 |
| 2 | GRN-RED | J116-2 | U45-17 |
| 3 | GRN-ORG | J116-3 | U45-16 |
| 4 | GRN-WHT | J116-4 | U45-15 |
| 5 | GRN-BLK | J116-5 | U45-14 |
| 6 | GRN-BLU | J116-6 | U45-13 |
| 7 | GRN-VIO | J116-7 | U45-12 |
| 8 | GRN-GRY | J116-8 | U45-11 |

| Matrix row | Wire | Connector | Receiver |
| --- | --- | --- | --- |
| 1 | WHT-BRN | J116-12 | U51-7 |
| 2 | WHT-RED | J116-13 | U51-5 |
| 3 | WHT-ORG | J116-14 | U51-9 |
| 4 | WHT-YEL | J116-15 | U51-11 |
| 5 | WHT-GRN | J116-16 | U57-7 |
| 6 | WHT-BLU | J116-17 | U57-5 |
| 7 | WHT-VIO | J116-18 | U57-9 |
| 8 | WHT-GRY | J116-19 | U57-11 |

The shaded entries are labelled `OPTO, TYPICALLY CLOSED`. The stock manual shades trough jam and balls 1-4, right popper, jet exit, right lockup 1, and left ramp entrance; current PinMAME additionally names later optional expansion inputs 53-56 as optos.

| Printed direct inputs | Public addresses | Signal connector | Ground |
| --- | --- | --- | --- |
| D1-D8 coin slots and four unused positions | 91-98 | J114-1,2,3,4,5,6,8,9; ORN-* wires | J114-14 black |
| D9-D12 diagnostic Escape, Down, Up, Enter | 101-104 | J114-10,11,12,13; GRY-* wires | J114-14 black |
| D13-D16 lower flipper EOS and two unused positions | 105-108 | J115-9,10,20,21; BLK-* wires | J115-22 black |
| D17-D24 cabinet tilt, door, flipper, and action inputs | 111-118 | J113-1,2,3,4,6,7,8,9; BLK-* wires | J113-10 black |

## Solenoid and flasher table, printed page 2-48

| Driver | Function | Fuse / power | Drive transistor | Drive connector / wire | Device |
| --- | --- | --- | --- | --- | --- |
| 1 | Left Martian | F101 / J102-1 RED-BRN | Q59 | J110-13 VIO-BRN | AE1-26-1500 |
| 2 | Right Martian | F101 / J102-1 RED-BRN | Q60 | J110-14 VIO-RED | AE1-26-1500 |
| 3 | Jet Exit Post | F101 / J102-1 RED-BRN | Q61 | J110-15 VIO-ORG | AE1-26-1500 |
| 4 | Right Gate | F101 / J102-1 RED-BRN | Q62 | J110-16 VIO-YEL | A-14406 |
| 5 | Left Gate | F102 / J102-2 RED-BLK | Q63 | J110-17 VIO-GRN | A-14406 |
| 6 | Drop Target Down | F102 / J102-2 RED-BLK | Q64 | J110-18 VIO-BLU | SM1-26-600 |
| 7 | Drop Target Up | F102 / J102-2 RED-BLK | Q65 | J110-19 VIO-BLK | AE1-26-1200 |
| 8 | Right Popper | F102 / J102-2 RED-BLK | Q66 | J110-20 VIO-GRY | AE1-25-1000 |
| 9 | Trough Eject | F103 / J102-3 RED-ORG | Q51 | J112-11 BRN-BLK | AE1-26-1500 |
| 10 | Left Slingshot | F103 / J102-3 RED-ORG | Q52 | J112-12 BRN-RED | AE1-26-1200 |
| 11 | Right Slingshot | F103 / J102-3 RED-ORG | Q53 | J112-13 BRN-ORG | AE1-26-1200 |
| 12 | Left Jet Bumper | F103 / J102-3 RED-ORG | Q54 | J112-14 BRN-YEL | AE1-26-1200 |
| 13 | Right Jet Bumper | F100 / J102-7 RED-YEL | Q55 | J112-15 BRN-GRN | AE1-26-1200 |
| 14 | Bottom Jet Bumper | F100 / J102-7 RED-YEL | Q56 | J112-16 BRN-BLU | AE1-26-1200 |
| 15 | Auto Plunger | F100 / J102-7 RED-YEL | Q57 | J112-17 BRN-VIO | AE1-23-800 |
| 16 | Right Lockup | F100 / J102-7 RED-YEL | Q58 | J112-18 BRN-GRY | AE1-23-800 |
| 17 | Center Arrow Flasher | F109 / J102-8 RED-WHT | Q43 | J110-1 BLU-BRN | #906 |
| 18 | Not used in stock machine | F109 | Q44 | J110-2 BLU-RED | none |
| 19 | Not used in stock machine | F109 | Q45 | J110-3 BLU-ORG | none |
| 20 | Not used | F109 | Q46 | J110-4 BLU-YEL | none |
| 21 | Not used | F109 | Q47 | J110-5 BLU-GRN | none |
| 22 | Right Popper Flasher | F109 / J102-8 RED-WHT | Q48 | J110-6 BLU-BLK | #906 |
| 23 | Left Arch Flasher | F109 / J102-8 RED-WHT | Q49 | J110-7 BLU-VIO | #89 |
| 24 | Not used | F109 | Q50 | J110-8 BLU-GRY | none |
| 25 | Right Arch Flasher | F109 / J102-8 RED-WHT | Q67 | J112-9 BLK-BRN | #89 |
| 26 | Left Martian Flasher | F109 / J102-8 RED-WHT | Q68 | J112-10 BLK-RED | #89 |
| 27 | Right Martian Flasher | F109 / J102-8 RED-WHT | Q69 | J112-19 BLK-ORG | #89 |
| 28 | Attack Mars Flasher | F109 / J102-8 RED-WHT | Q70 | J112-20 BLK-YEL | #906 |

| Driver pair | Function | Fuse / power | Transistors | Drive connector / wires | Device |
| --- | --- | --- | --- | --- | --- |
| 33-34 | Lower-right flipper power / hold | F104 / J103-1 RED-GRN | Q35 / Q36 | J112-1 YEL-GRN / J112-2 ORG-GRN | FL1-11629 |
| 35-36 | Lower-left flipper power / hold | F105 / J103-2 RED-BLU | Q37 / Q38 | J112-3 YEL-BLU / J112-4 ORG-BLU | FL1-11629 |
| 37-38 | Lock diverter power / hold | F106 / J103-3 RED-VIO | Q39 / Q40 | J112-5 YEL-VIO / J112-6 ORG-VIO | FL1-22241 |
| 39-40 | Up/down ramp power / hold | F107 / J103-4 RED-GRY | Q41 / Q42 | J112-7 YEL-GRY / J112-8 ORG-GRY | FL1-11753 |
