# Time Machine coil, relay, flipper, and special-solenoid transcription

Source: PDF pages 30-31, printed pages 26-27. The Coil I.D. sheet was decided from the retained Archive.org PDF render; OCR was locator-only.

## CPU-controlled Coil I.D. sheet

| Public / printed side | Printed device | Printed type | CPU drive / transistor |
| --- | --- | --- | --- |
| 1 / SIDE L 01 | KLACKER | 29-900 | GRY-BRN / Q46 |
| 25 / SIDE R 01 | OUTHOLE | 23-840 | shared Q46 mux side |
| 2 / SIDE L 02 | CHIME-1 | 27-1400 | GRY-RED / Q45 |
| 26 / SIDE R 02 | TROUGH | 23-840 | shared Q45 mux side |
| 3 / SIDE L 03 | CHIME-2 | 27-1400 | GRY-ORN / Q44 |
| 27 / SIDE R 03 | SUPER VERTICAL UP KICKER | 23-800 | shared Q44 mux side |
| 4 / SIDE L 04 | CHIME 3 | 27-1400 | GRY-YEL / Q43 |
| 28 / SIDE R 04 | BALL LOCK | 24-900 | shared Q43 mux side |
| 5 / SIDE L 05 | FLASH NO.1 | NO.906 (4) | GRY-GRN / Q42 |
| 6 / SIDE L 06 | FLASH NO.2 | NO.906 (4) | GRY-BLU / Q41 |
| 7 / SIDE L 07 | FLASH NO.3 | NO.906 (4) | GRY-VIO / Q40 |
| 8 / SIDE L 08 | FLASH NO.4 | NO.906 (2), NO.89 (2) | GRY-BLK / Q39 |
| 9 | FLASH NO.5 | NO.906 (2), NO.89 (2) | BRN-BLK / Q30 |
| 10 | LEFT/RIGHT COIL RELAY K1 | K1 | BLK-RED / Q29 |
| 11 | GENERAL ILLUM. RELAY K1 | K1 | BRN-ORN / Q28 |
| 12 | FLASH NO.6 | NO.906 (2), NO.89 (2) | BRN-YEL / Q27 |
| 13 | FLASH NO.7 | NO.906 (2), NO.89 (2) | BRN-GRN / Q26 |
| 14 | FLASH NO.8 | NO.906 (2), NO.89 (2) | BRN-BLU / Q25 |
| 15 | FLASH NO.9 | NO.906 (2), NO.89 (2) | BRN-VIO / Q24 |
| 16 | LASER KICK | 23-800 | WHT-GRY / Q23 |

After SIDE R 04, the sheet shows no further right-side device rows. The Coil Tests prose on the same printed page nevertheless says coil 10 switches +34 volts for drives 1-8 between left and right sets and calls the result an effective total of 23 regular coils. Pinned Time Machine `s11.c` also types public 29-32 as four distinct muxed #89-bulb output states. This is material evidence that R05-R08 belong to the addressable right-bank design, but neither the prose nor a device row identifies fitted circuits, quantities, or feature names for them. Their per-address activity and fitment remain unknown rather than dead or invented.

## Coil Tests operating description

The printed prose describes sixteen regular microprocessor-pulsed drivers plus six switch-triggered drivers. Coil 10 works with drives 1-8 to select +34 V between coil/flash-lamp sets termed left and right; the PPB supplies isolation diodes and current-limiting resistors, and the manual says this "effectively provides 23 regular coils." Automatic Test pulses every regular solenoid or flash lamp sequentially while displaying its name and drive number. Select Coil chooses one drive and can pulse it repeatedly.

## Switch-triggered coil table

| Printed special address | Printed description | Control line (CPU to coil) | Power line (PS to coil) | Trigger line (coil switch to CPU) | Drive transistor (TIP 122) | Coil type |
| --- | --- | --- | --- | --- | --- | --- |
| SP1 | RIGHT POP BUMPER | BLU-ORN / CPU CN19-3 | RED / PS CN3-6 | ORN-BLK / CPU CN18-2 | Q8 | 23-800 |
| SP2 | CENTER POP BUMPER | BLU-RED / CPU CN19-4 | RED / PS CN3-6 | ORN-RED / CPU CN18-3 | Q9 | 23-800 |
| SP3 | LEFT SLINGSHOT | BLU-YEL / CPU CN19-6 | RED / PS CN3-6 | ORN-YEL / CPU CN18-4 | Q10 | 23-800 |
| SP4 | LEFT POP BUMPER | BLU-BRN / CPU CN19-7 | RED / PS CN3-6 | ORN-BRN / CPU CN18-5 | Q11 | 23-800 |
| SP5 | RIGHT SLINGSHOT | BLU-GRN / CPU CN19-8 | RED / PS CN3-6 | ORN-GRN / CPU CN18-8 | Q12 | 23-800 |
| SP6 | NOT USED | -- / CPU CN19-9 | -- / PS CN3-6 | -- / CPU CN18-9 | Q13 | -- |

The location drawing on the same printed page labels SP1 at the center pop and SP2 at the right pop. It agrees with SP4 at the left pop. Neither reading is silently corrected.

## Flippers

| Side | Printed coil | Supply / winding wires |
| --- | --- | --- |
| Left | 22-750/30-2600 | ORN-BLU / BLU-GRY / GRY-YEL |
| Right | 22-750/30-2600 | ORN-RED / BLU-VIO / BLK-WHT |
