# Big Bang Bar — Opto Boards

Transcribed from `Capcom_1996_Big_Bang_Bar_Manual.pdf`, printed page 76 (PDF page 80), "OPTO
BOARDS". Rendered at 300 dpi, read visually. A grayscale crop of the three board diagrams is
retained at `manuals/rendered/capcom.big-bang-bar.1996/opto-boards.png` (evidence of a
drawing — component-placement schematics — not a printed table). PDF page number = printed
page number + 4.

Three physical opto-board assemblies are documented:

- **A0020000** — single-board slotted opto switch ("Creature" silkscreen). One connector
  header (.100 STR 5-PIN, `CN00104-05`), one resistor (MOF 1W 5% 510 OHM, `RS00119-01`), one
  opto switch (SLOTTED, .375, PIN-IN, `SW00148`). Connector `J1` pins `GND`, `C`, `+`,
  `PGND`.
- **A0015604-4R** — 4-transistor photo-receiver ("Rx") board. One connector header (.100 R/A
  7-PIN, `CN00137-07`), four transistors (21T313 NPN PHOTO, `TR00104`, silkscreened Q1-Q4).
- **A0015702-4R** — 4-LED transmitter ("Tx") board. One connector header (.100 R/A 4-PIN,
  `CN00137-04`), four IREDs (21E187 100MA T-1 3/4, `DI00103`, silkscreened LED1-LED4), four
  resistors (MOF 1W 5% 330 OHM, `RS00112-04`).

## Full parts/quantity table

| No. | Description | Component Part Number | A0020000 qty | A0015604-4R qty | A0015702-4R qty |
| --- | --- | --- | --- | --- | --- |
| 1 | CONNECTOR HEADER .100 R/A 4-PIN | CN00137-04 | — | — | 1 |
| 1 | CONNECTOR HEADER .100 R/A 7-PIN | CN00137-07 | — | 1 | — |
| 1 | CONNECTOR HEADER .100 STR 5-PIN | CN00104-05 | 1 | — | — |
| 2 | IRED 21E187 100MA T-1 3/4 | DI00103 | — | — | 4 |
| 3 | RESISTOR MOF 1W 5% 330 OHM | RS00112-04 | — | — | 4 |
| 3 | RESISTOR MOF 1W 5% 510 OHM | RS00119-01 | 1 | — | — |
| 4 | TRANSISTOR 21T313 NPN PHOTO | TR00104 | — | 4 | — |
| 5 | SWITCH, OPTO, SLOTTED, .375, PIN-IN | SW00148 | 1 | — | — |

The receiver/transmitter pair (A0015604-4R / A0015702-4R) is exactly the part-number pair
the switch-locations table (printed page 83) cites for switches 36-39 (trough), confirming
those four are through-beam (separate transmitter/receiver board) optos rather than the
single-board slotted-opto type (A0020000). No switch-locations row cites A0020000 by part
number in the legible portion of that scan.
