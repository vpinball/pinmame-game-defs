# Solenoid Identification Table

Source: `Eight_Ball_Deluxe_OPS.pdf`, PDF page 22 (printed page 17), "SOLENOID IDENTIFICATION TABLE".
Transcribed from a 300 dpi render (`manuals/rendered/bally.eight-ball-deluxe.1981/page-22.png`);
`pdftotext` interleaves this page's two side-by-side sub-tables and cannot be trusted for it.

The "Self Test #" column is the order the ROM's own solenoid self-test displays while firing each
coil, not the public controller address; see `review-artifacts/eight-ball-deluxe/manual-transcription.md`
for the harness-derived Self-Test-#-to-public-address table.

| Self Test # | Solenoid identification |
| --- | --- |
| 01 | LEFT SLINGSHOT |
| 02 | RIGHT SLINGSHOT |
| 03 | KNOCKER |
| 04 | LEFT THUMPER BUMPER |
| 05 | RIGHT THUMPER BUMPER |
| 06 | BOTTOM THUMPER BUMPER |
| 07 | SINGLE DROP TARGET RESET |
| 08 | #1, 9 DROP TARGET (TOP) |
| 09 | #2, 10 DROP TARGET |
| 10 | #3, 11 DROP TARGET |
| 11 | #4, 12 DROP TARGET |
| 12 | #5, 13 DROP TARGET |
| 13 | #6, 14 DROP TARGET |
| 14 | #7, 15 DROP TARGET (BOTTOM) |
| 15 | 7 DROP TARGET RESET |
| 16 | 4 DROP TARGET RESET |
| 17 | SAUCER |
| 18 | OUTHOLE KICKER |
| 19 | COIN LOCKOUT DOOR |
| 20 | K1 RELAY (FLIPPER ENABLE) |

"NOTE: SLINGSHOT & THUMPER BUMPER COILS WILL BE ENERGIZED WHEN SWITCH IS MADE." (printed directly
beneath the table on the same page).
