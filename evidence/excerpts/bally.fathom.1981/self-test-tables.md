# Bally Fathom (game #1233) — Solenoid Identification Table and Switch Assembly Self-Test Display Numbers

Source: `Bally_1981_Fathom_English_Manual.pdf`, PDF page 23, printed page 17.
Transcribed by hand from a 200 dpi render of that page. Both tables are transcribed in full,
including the three blank Switch Self Test rows, because a blank row is the evidence that a matrix
position is unfitted and is only visible if it is written down.

Heading, verbatim: `GAME #1233 FATHOM` / `SOLENOID IDENTIFICATION TABLE`.

## SOLENOID IDENTIFICATION TABLE

The column heading is `Self Test #`, not an address. See `self-test-procedure.md` for what the
number means: the ROM flashes it on the player score displays as it pulses each coil.

| Self Test # | SOLENOID IDENTIFICATION |
| --- | --- |
| 01 | KNOCKER |
| 02 | TOP SAUCER |
| 03 | RIGHT SAUCER |
| 04 | LEFT THUMPER BUMPER |
| 05 | BOTTOM THUMPER BUMPER |
| 06 | RIGHT THUMPER BUMPER |
| 07 | LEFT SLINGSHOT |
| 08 | RIGHT SLINGSHOT |
| 09 | 3 TOP DROP TARGET RESET |
| 10 | 6 DROP TARGET RESET |
| 11 | 3 MIDDLE DROP TARGET RESET |
| 12 | RIGHT INLINE DROP TARGET RESET |
| 13 | OUTHOLE KICKER |
| 14 | 1ST GREEN INLINE DROP TARGET |
| 15 | 2ND GREEN INLINE DROP TARGET |
| 16 | 3RD GREEN INLINE DROP TARGET |
| 17 | 1ST BLUE INLINE DROP TARGET |
| 18 | 2ND BLUE INLINE DROP TARGET |
| 19 | 3RD BLUE INLINE DROP TARGET |
| 20 | COIN LOCKOUT DOOR |
| 21 | K1 RELAY (FLIPPER ENABLE) |

Twenty-one printed entries. The physical driver board publishes only fifteen momentary and four
continuous outputs, so the printed list is not a one-to-one address list; the Solenoid Expander
(A15, AS-2518-66) shares five driver outputs between two coils each. See `solenoid-driver-a3.md`.

## SWITCH ASSEMBLY SELF-TEST DISPLAY NUMBERS

Heading, verbatim: `SWITCH ASSEMBLY SELF-TEST DISPLAY NUMBERS`, columns `Switch Self Test #` and
`DESCRIPTION`.

| Switch Self Test # | DESCRIPTION |
| --- | --- |
| 01 | OUTHOLE |
| 02 | #1 LEFT OF OUTHOLE |
| 03 | #2 LEFT AND #1 RIGHT OF OUTHOLE |
| 04 | TOP SAUCER |
| 05 | RIGHT SAUCER |
| 06 | CREDIT BUTTON |
| 07 | RIGHT FLIPPER BUTTON |
| 08 | *(printed blank — no description, no entry)* |
| 09 | COIN III (RIGHT) |
| 10 | COIN I (LEFT) |
| 11 | COIN II (MIDDLE) |
| 12 | "C" LANE |
| 13 | "B" LANE |
| 14 | "A" LANE |
| 15 | TILT (3) |
| 16 | SLAM (2) |
| 17 | RIGHT CENTER TARGET |
| 18 | SPINNER |
| 19 | 10 POINT AND 6 DROP TARGET REBOUND |
| 20 | 3 LEFT ROLLOVER BUTTONS |
| 21 | RIGHT RETURN LANE |
| 22 | RIGHT OUTLANE |
| 23 | LEFT OUTLANE |
| 24 | LEFT RETURN LANE |
| 25 | TOP SAUCER ROLLOVER BUTTON |
| 26 | RIGHT SAUCER ROLLOVER BUTTON |
| 27 | LEFT SIDE DROP TARGET F (BOTTOM) |
| 28 | LEFT SIDE DROP TARGET E |
| 29 | LEFT SIDE DROP TARGET D |
| 30 | LEFT SIDE DROP TARGET C |
| 31 | LEFT SIDE DROP TARGET B |
| 32 | LEFT SIDE DROP TARGET A (TOP) |
| 33 | #3 MIDDLE DROP TARGET |
| 34 | #2 MIDDLE DROP TARGET |
| 35 | #1 MIDDLE DROP TARGET |
| 36 | RIGHT SLINGSHOT |
| 37 | LEFT SLINGSHOT |
| 38 | RIGHT THUMPER BUMPER |
| 39 | BOTTOM THUMPER BUMPER |
| 40 | LEFT THUMPER BUMPER |
| 41 | *(printed blank — no description, no entry)* |
| 42 | 3RD BLUE INLINE DROP TARGET |
| 43 | 2ND BLUE INLINE DROP TARGET |
| 44 | 1ST BLUE INLINE DROP TARGET |
| 45 | *(printed blank — no description, no entry)* |
| 46 | 3RD GREEN INLINE DROP TARGET |
| 47 | 2ND GREEN INLINE DROP TARGET |
| 48 | 1ST GREEN INLINE DROP TARGET |

Forty-eight numbered positions, which is six columns of eight on the AS-2518-35 switch matrix.
Positions 08, 41 and 45 are printed blank. Note `TILT (3)` and `SLAM (2)`: the parenthesised
number is the count of series contacts on that one matrix position, not a second address.

The page footer is the printed page number `17`.
