# NBA Fastbreak — Differences between the March and May 1997 editions

Compared: the May 1997 FINAL edition (`Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf`,
document 16-50053.1-101) against the earlier edition whose cover says March 1997
(`Bally_1997_NBA_Fastbreak_Operations_Manual_Final_no_schematics.pdf`). Every comparison was made on the rendered
300 dpi pages, cell by cell, not on the OCR text. Read from the rendered page (300 dpi scan), not from the OCR text.

Pages compared (March PDF page / printed folio against May PDF page / printed folio):

| Table | March | May |
| --- | --- | --- |
| Solenoid/Flashlamp Locations list | 118 / 2-40 | 63 / 2-40 |
| Switch Locations list | 120 / 2-42 | 64 / 2-42 |
| Lamp Locations list | 122 / 2-44 | 65 / 2-44 |
| Solenoid/Flasher Table | 124 / 2-46 | 68 / 2-50 |
| Lamp Matrix | 125 / 2-47 | 67 right / 2-49 (reprints: 71 / 3-4, 86 / 3-36) |
| Switch Matrix | 126 / 2-48 | 67 left / 2-48 (reprints: 70 / 3-2, 86 / 3-36) |

The March playfield drawings (PDF pages 119, 121, 123) were not rendered or compared; only the May drawings were read.
The May page 86 (printed `3-36`) reprints the Lamp Matrix and the Switch Matrix together on one page (left half blank
but for the folio); it was compared with `2-48`/`2-49` and agrees (including `SH(O)OT` in lamp 66, the lamp-matrix diode,
and the same shaded switch cells).

## Switch Matrix

No difference in any printed cell, wire, connector pin, IC pin, label or legend text. The shaded ("OPTO, TYPICALLY
CLOSED") cells are the same in both editions: 31-37, 51-55, F2, F4, F5, F6, F8. The scan quality differs (the March
shading is a uniform light-grey wash; the May shading is a faint stipple, clearer on the `3-2` and `3-36` reprints).
The printed folio is `2-48` in both. See `switch-matrix.md` for the measurements.

## Lamp Matrix

| Cell | March reading | May reading |
| --- | --- | --- |
| Lamp 66 (column 6, row 6) | `SH(Q)OT` | `SH(O)OT` (also `SH(O)OT` in the May reprints `3-4` and `3-36`) |
| Title-line drawing | a diode symbol between the lamp symbol and `Red` | `2-49`: no diode visible (a short dash); the May reprints `3-4` and `3-36` show the diode |
| Printed folio | `2-47` | `2-49` |

All other cells, all column headers (`J121-n`, `Qnn`), all row headers (`J125-n Qnnn`) and the `J1XX = Power Driver Board`
footnote agree.

## Solenoid/Flasher Table

No difference in any cell of any block (solenoids 01-28, General Illumination 01-05, Flipper Circuits 29-36, Motor &
Shot Clock Circuits 37-40, legend and footnotes, closing page references `3-26` and `3-25`). Both print `# 906 (1)`
(with a space) in row 20 and the same `NOT USED` rows 02, 21, 23. The printed folio is `2-46` in March and `2-50` in
May.

## Switch Locations

No difference in any item number, assembly part number, switch part number or description (including the typos
`TROUGH ELECT` for item 31 and the `5467-12693-66` switch part number for items 65-68), nor in the footnote. The OCR
text layers disagree on a few tokens (for example `A-17316`, `5647-12693-19`); the rendered pages agree.

## Lamp Locations

No difference in any item, assembly, bulb, socket or description (including `24-6768` for item 84 and the
`SOLD AS ASSEMBLY ONLY` rows 87-88), nor in the footnotes.

## Solenoid/Flashlamp Locations

No difference in any row (including item 06 assembly `A-17796`, item 04 `A-21530`, the unnumbered `Insert Panel
Flasher*` lines under 19 and 20, `Shoot 3` printed for item 36, and `14-8043` for item 38), nor in the legend or
footnotes. The OCR text layers disagree on `A-21530`/`A-17796`; the rendered pages agree with each other.
