# Monster Bash — Lamp Matrix (wiring)

Transcribed from `Williams_1998_Monster_Bash_English_Manual.pdf`, PDF page 120, printed page 2-52,
the lamp matrix wiring table. Read from the rendered page; the retained scan is image-only. Header
`Yellow (B+) —(coil)— Red`. Footer `J1XX = Power Driver Board`.

## Matrix drive columns

| Column | Wire | Connector | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J121-1 | Q96 |
| 2 | Yellow-Red | J121-2 | Q100 |
| 3 | Yellow-Orange | J121-3 | Q95 |
| 4 | Yellow-Black | J121-4 | Q99 |
| 5 | Yellow-Green | J121-5 | Q94 |
| 6 | Yellow-Blue | J121-6 | Q98 |
| 7 | Yellow-Violet | J121-7 | Q93 |
| 8 | Yellow-Gray | J121-9 | Q97 |

## Matrix return rows

| Row | Wire | Connector | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J125-1 | Q104 |
| 2 | Red-Black | J125-2 | Q108 |
| 3 | Red-Orange | J125-4 | Q103 |
| 4 | Red-Yellow | J125-5 | Q107 |
| 5 | Red-Green | J125-6 | Q102 |
| 6 | Red-Blue | J125-7 | Q106 |
| 7 | Red-Violet | J125-8 | Q101 |
| 8 | Red-Gray | J125-9 | Q105 |

## Printed lamp-function cells against the parts list

The lamp-matrix cell text agrees with the printed 2-44 parts list (`lamp-locations.md`) on every
address. Four cells carry obvious typographic slips against the parts list, and the parts list is
taken as authoritative for the label in each case:

| Public | Matrix page | Parts list (authoritative) |
| --- | --- | --- |
| 14 | DRAC-ATTTACK | DRAC-ATTACK |
| 31 | QUARTER MOOM (2) | QUARTER MOON (2) |
| 43 | THREE-QUARTERS MOON (2) | THREE-QUARTER MOON (2) |
| 48 | LEFT GARGOYLE | LEFT GARGLE |

Address 48 deserves the explicit note: the matrix reads "LEFT GARGOYLE" but the parts list reads
"LEFT GARGLE", and the paired right-hand insert at 25 reads "RIGHT GARGLE" on both pages. The Bride
of Frankenstein insert trio is PRIMP / WARM UP / GARGLE (46/47/48 left, 27/26/25 right), so "GARGOYLE"
is the slip. The matrix page also abbreviates FRANKENSTEIN to FRANK at 13 and 71-76.
