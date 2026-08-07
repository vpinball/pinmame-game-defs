# Switch Assembly Self-Test Display Numbers

Source: `Eight_Ball_Deluxe_OPS.pdf`, PDF page 22 (printed page 17), "SWITCH ASSEMBLY SELF-TEST
DISPLAY NUMBERS". Transcribed from a 300 dpi render
(`manuals/rendered/bally.eight-ball-deluxe.1981/page-22.png`); `pdftotext` interleaves this page's
two side-by-side sub-tables and cannot be trusted for it.

A LibPinMAME harness run holding each public switch address 1-40 in turn during the ROM's own
stuck-switch search (self-test stage 5) showed the held address's number directly on the player
score displays, confirming the public switch address equals this table's "Self Test #" column with
no translation required (see `review-artifacts/eight-ball-deluxe/manual-transcription.md`,
"Harness derivation").

| Switch # | Description | Switch # | Description |
| --- | --- | --- | --- |
| 01 | 2X INLINE DROP TARGET | 21 | 5, 13 DROP TARGET |
| 02 | 3X INLINE DROP TARGET | 22 | 6, 14 DROP TARGET |
| 03 | 4X INLINE DROP TARGET | 23 | 7, 15 DROP TARGET |
| 04 | 5X INLINE DROP TARGET | 24 | 30 POINT REBOUND (2) |
| 05 | INLINE BACK TARGET | 25 | "D" TARGET |
| 06 | CREDIT BUTTON | 26 | "E" FIRST TARGET |
| 07 | TILT (3) | 27 | "L" TARGET |
| 08 | OUTHOLE | 28 | "U" TARGET |
| 09 | COIN III (RIGHT) | 29 | "X" TARGET |
| 10 | COIN I (LEFT) | 30 | "E" 2ND TARGET |
| 11 | COIN II (MIDDLE) | 31 | RIGHT OUTLANE |
| 12 | "A" ROLLOVER | 32 | LEFT OUTLANE |
| 13 | "B" ROLLOVER | 33 | SINGLE DROP TARGET |
| 14 | "C" ROLLOVER | 34 | SAUCER |
| 15 | "D" ROLLOVER | 35 | ROLLOVER BUTTON |
| 16 | SLAM (2) | 36 | RIGHT SLINGSHOT |
| 17 | 1, 9 DROP TARGET | 37 | LEFT SLINGSHOT |
| 18 | 2, 10 DROP TARGET | 38 | LEFT THUMPER BUMPER |
| 19 | 3, 11 DROP TARGET | 39 | RIGHT THUMPER BUMPER |
| 20 | 4, 12 DROP TARGET | 40 | BOTTOM THUMPER BUMPER |

Quantities in parentheses (e.g. "SLAM (2)", "TILT (3)", "30 POINT REBOUND (2)") are the manual's own
notation for multiple physical switches wired to the one matrix address.
