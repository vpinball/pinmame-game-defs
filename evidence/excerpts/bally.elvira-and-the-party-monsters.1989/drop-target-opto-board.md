# Bally Elvira and the Party Monsters (1989) — 3-Bank Drop Target Opto Board C-12559

Source: Bally Midway *Elvira and the Party Monsters* Operations and Parts Information Manual
16-2011-101, IPDB machine 782 file `Elvira_and_the_Partymonsters_OCR_searchable.pdf`, PDF page 95,
printed page 3-3 (assembly and schematic), and PDF page 79, printed page 2-27 (parts list). Read from
the native 300 dpi render. The crop is the schematic on printed page 3-3.

Parts list, printed page 2-27:

| Part Number | Ckt Designation | Description |
| --- | --- | --- |
| 5768-12368-00 | *(blank)* | 3-Bank Opto Board |
| 5490-10159-00 | Opto 1- Opto3 | Opto Interruptor, MDL, S/G |
| 5010-08930-00 | R1, R3, R5 | Resistor, C.F., 470 Ω, 1/2w, 5% |
| 5010-09162-00 | R8 | Resistor, C.F., 100KΩ, 1/4w, 5% |
| 5010-09324-00 | R2, R4, R6 | Resistor, C.F., 27KΩ, 1/4w, 5% |
| 5010-08774-00 | R7 | Resistor, C.F., 22KΩ, 1/4w, 5% |
| 5043-08980-00 | B | Capacitor, .01mfd., +80 -20% |
| 5370-12272-00 | U1 | I.C., Quad. Comp., LM339 |
| 5791-10871-04 | J2 | Connector, 4-pin Hdr, Sq Pin .156 |
| 5791-10871-07 | J1 | Connector, 7-pin Hdr, Sq Pin .156 |

The scan's ohm sign is a W-shaped glyph; it is transcribed as Ω. The board drawing above the list
shades R9, R10 and R11 with the legend "Not Installed". The text layer of this page shifts the
designator column by one row; the table here is read from the rendered page, not from that layer.

Schematic, printed page 3-3:

- Three opto interrupters, `Opto 1`, `Opto 2`, `Opto 3`, each an LED fed from `+12 V` through a
  470 Ω 1/2 W resistor (`R1`, `R3`, `R5`) and a phototransistor pulled up to `+12 V` through 27 KΩ
  (`R2`, `R4`, `R6`).
- Three sections of an `LM339` quad comparator. Each phototransistor collector feeds a comparator
  `+` input; the `-` inputs share a reference from `R8` 100 KΩ to `+12 V` and `R7` 22 KΩ to ground.
- Each comparator output drives a matrix row through a `1N4004` diode: `row 1 D1` on `J1` pin 4,
  `row 2 D2` on `J1` pin 5, `row 3 D3` on `J1` pin 7.
- The phototransistor emitters return to `J1` pin 1, labelled `column`. `J1` pin 6 is the key.
- `J1` pins 2 and 3 are drawn as terminals with no label and no connection.
- The fourth comparator section is tied off with capacitor `B`.
- `J2`: pin 3 `Circuitry Ground`, pin 1 `+12 V Power Input`, pin 2 `Key`, pin 4 `N.C.`
- `R9`, `R10`, `R11` (18 KΩ to ground) are shaded, and the legend reads "shaded box = Not Installed".

The board therefore presents each opto to the switch matrix as an ordinary diode-isolated row closure
on the drop-target column. The switch location list prints items 41, 42 and 43 (Left, Center and Right
Drop Target "J", "A", "M") as `p/o C-12559`.
