# Scared Stiff — General Illumination

Transcribed from `Scared_Stiff_OPS.pdf`, PDF page 111 (continuation of the Solenoid Locations page,
printed 2-46) and PDF page 123 (printed 3-10, General Illumination Circuit). Produced by rendering
the retained PDF at 300-600 dpi with `pdftoppm` and reading the table directly; this scan's text
layer is garbled multi-column OCR and was never trusted.

## GI table (printed 2-46 continuation)

| Addr | Function | Voltage conn. | Drive Xistor | Drive conn. | Part | Non-dimmable? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 (printed 01) | Upper Playfield | J105-1 | Q5 | J105-7 | 24-6549 (`#44`) | dimmable |
| 1 (printed 02) | Center Playfield | J105-2 | Q4 | J105-8 | 24-6549 (`#44`) | dimmable |
| 2 (printed 03) | Lower Playfield | J105-3 | Q3 | J105-9 | 24-6549 (`#44`) | dimmable |
| 3 (printed 04) | Illum String 4 (backbox) | J106-7 | Q2 | J106-10 | 24-6549 (`#555`) | always ON |
| 4 (printed 05) | Illum String 5 (backbox) | J106-6 | Q1 | J106-11 | 24-6549 (`#555`) | always ON |

Footnote on the printed page: `† These G.I. strings do not brighten and dim, they are always ON`,
applying to strings 4 and 5 only.

## General Illumination Circuit (printed 3-10)

Confirms 5 total GI strings, 3 built like Figure #1 (LS374 latch + MPSD52 driver + SC141 triac,
dimmable) and 2 like Figure #2 (diode-bridge only, binary). Cross-referenced against the
Solenoid/Flasher table's GI section above; both agree GI 0-2 are dimmable Playfield strings and GI
3-4 are non-dimmable backbox strings.

The retained script's `GIUpdates2` independently agrees: its own inline comments label `Case 3`/
`Case 4` "GI String 3 (Backbox)"/"GI String 4 (Backbox)" (its 1-based prose numbering for public
3/4). No conflict on GI classification, unlike Tales of the Arabian Nights or Theatre of Magic.
