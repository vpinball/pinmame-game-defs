# Big Bang Bar — Schematic sheet 7/12: "DIAGRAM, PLFD DEVICES, FLASHERS, WIRING"

Transcribed from `Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf`, sheet 7 of 12
(12-page document, letter-landscape, each sheet titled "CAPCOM COIN-OP, INC.", part no.
"PB-5 WIRING", drawn by B. ZIEGLER, dated 6/7/96). Rendered at 200 dpi for triage, then
re-rendered at 400 dpi and cropped for exact transcription. This is the single most
authoritative solenoid source found: a dedicated wiring sheet with its own printed "DEVICE #
& DESCRIPTION" legend table (four columns, S1-S8/S9-S16/S17-S24/S25-S32) directly above the
matching schematic symbols.

## Full S1-S32 device table (exactly as printed)

| # | Description | | # | Description | | # | Description | | # | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OUTHOLE | | S9 | L. FLIPPER | | S17 | 3-BANK RESET | | S25 | (FLASHER) ALIENS |
| S2 | TROUGH | | S10 | R. FLIPPER | | S18 | STAR BUMPER LEFT | | S26 | (FLASHER) LOWER LOCK |
| S3 | KNOCKER | | S11 | UR. FLIPPER | | S19 | STAR BUMPER MIDDLE | | S27 | ORBIT GATE LEFT |
| S4 | L. SLINGSHOT | | S12 | EJECT HOLE | | S20 | STAR BUMPER RIGHT | | S28 | ORBIT GATE RIGHT |
| S5 | R. SLINGSHOT | | S13 | ISLAND DIVERTER | | S21 | (FLASHER) BACKBOX L. | | S29 | 1-BANK RESET |
| S6 | KICKBACK | | S14 | RAMP DIVERTER 1 | | S22 | TUBE DANCER & B.B. R. | | S30 | (MOTOR) TUBE DANCER |
| S7 | 4-BANK RESET | | S15 | RAMP DIVERTER 2 | | S23 | (FLASHER) DANCE FLOOR | | S31 | (MOTOR) ALIENS FORWARD |
| S8 | LOWER LOCK POST | | S16 | ALIEN LOCK POST | | S24 | (FLASHER) EJECT HOLE | | S32 | (MOTOR) ALIENS REVERSE |

This matches the manual's printed page-82 `Ref.` table exactly, address for address,
resolving that table's unnumbered "BACKBOX RIGHT (FLASHER)" row: S22 drives two devices in
parallel from one connector pin.

## Schematic symbol types (read from the wiring diagram itself, not only the text legend)

- S1-S20 and S27-S29 are drawn with the coil-plus-flyback-diode symbol used throughout this
  sheet set for genuine solenoid coils.
- S21, S23, S24, S25, S26 are drawn with the circular radiating-line "light bulb" symbol used
  throughout for lamps/flashers, consistent with their printed "(FLASHER)" labels.
- **S22 drives two device symbols in parallel from one connector pin** (wire VIO/BLU on
  J20/J21 pin 6), matching "TUBE DANCER & B.B. R.". In this scan, **both** S22 symbols are
  drawn as the circular bulb symbol, not the coil symbol used for S1-S20/S27-S29 — this
  appears to conflict with the Tube Lady Assembly mechanism parts drawing (printed page 108,
  PDF 112), which shows a genuine coil (item 1A) as part of that same mechanism. Not
  resolved by this sheet alone; recorded as an open construction question.
- S30 is drawn with a circle-and-"M" motor symbol, distinct from both the coil and bulb
  symbols, confirming a rotating motor. S31/S32 (Aliens Forward/Reverse) are drawn with the
  ordinary coil symbol, feeding an unlabeled 4-pin connector routed "TO POWER BOARD J14" —
  consistent with one small motor-driver/reversing sub-circuit for one physical reversible
  gearmotor (corroborated by the Alien Mech Assembly parts page, printed page 104/PDF 108,
  which draws exactly one DC gearmotor item driving two gear-and-shaft pairs, and by the
  Game Diagnostics section's dedicated "C2-02: ALIEN MOTOR" calibration test, printed page
  41/PDF 45-46, which describes a single motor calibrated at two power levels), not two
  independent motors.

## Connector pin-to-address mapping

- Block S1-S8 -> 8-pin connector, wires BRN/BLK..BRN/GRY, arrow "TO DRIVER BOARD J14".
- Block S9-S16 -> 9-pin connector (pin 6 is a KEY/no-wire position), wires GRN/BRN..GRN/GRY,
  arrow "TO DRIVER BOARD J18" (matches schematic sheet 2's own J17/J18 = SOL9-16 naming).
- Block S17-S24 -> 9-pin connector (pin 7 is KEY), wires VIO/BRN..VIO/GRY, arrow printed
  **"TO DRIVER BOARD J18"** — almost certainly a labeling error in the original schematic
  (sheet 2's own connector naming has J20/J21 = SOL17-24, not J18); read and reported exactly
  as printed rather than silently corrected.
- Block S25-S32 -> 9-pin connector (pin 4 is KEY), wires GRY/BRN..GRY/BLK, arrow "TO DRIVER
  BOARD" (destination connector number cut off in this crop, consistent with sheet 2's J25).

## Cross-reference: schematic sheet 2/12, "DIAGRAM, DRIVER BOARD WIRING"

Sheet 2 documents the driver-board connector/wire-color layout (not individual device names)
for the same SOL1-32 range, confirmed pin-for-pin identical to sheet 7's addresses:

- J13/J14 (SOL1-8): BRN/BLK, BRN/RED, BRN/ORG, BRN/YEL, BRN/GRN, BRN/BLU, BRN/VIO, BRN/GRY.
- J17/J18 (SOL9-16): GRN/BRN, GRN/RED, GRN/ORG, GRN/YEL, GRN/BLK, GRN/BLU, GRN/VIO, GRN/GRY.
- J20/J21 (SOL17-24): VIO/BRN, VIO/RED, VIO/ORG, VIO/YEL, VIO/GRN, VIO/BLU, VIO/BLK, VIO/GRY.
- J24/J25 (SOL25-32): GRY/BRN, GRY/RED, GRY/ORG, GRY/YEL, GRY/GRN, GRY/BLU, GRY/VIO, GRY/BLK.

Sheet 2 also draws harness-bundle arrows ("TO PLAYFIELD SOLENOIDS" / "TO PLAYFIELD FLIPPERS"
/ "TO PLAYFIELD FLASHERS" / "TO PLAYFIELD MOTORS") spanning groups of pins for cable-routing
purposes; these bundle boundaries (e.g. a "flasher" arrow spanning SOL23-27, which includes
S27 Orbit Gate Left — confirmed a genuine coil by sheet 7's own symbol) describe physical
harness bundling, not device-type classification, and must not be read as contradicting
either pinned PinMAME's `CORE_MODOUT_BULB_89_20V_DC_WPC` output-type declaration for
addresses 21-26 or sheet 7's own per-device symbol shapes, which agree with each other on
the 21-26 flasher-bulb range.
