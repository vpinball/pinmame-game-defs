# Secret Service production-manual schematic observations

Source: Data East production manual from Archive.org item `Data_East__Secret_Service_Manual`, SHA-256 `f2d9c030951d1d8fef3db36447457689b69bac557935053293dd3c143ec4252a`. The pages below were visually checked against fresh 300 dpi Poppler renders because the PDF has no text layer.

- PDF page 30 / printed page 25 shows separate high-current `RIGHT FLIPPER SWITCH` and `LEFT FLIPPER SWITCH` cabinet circuits with BLU-VIO and BLU-GRY leads. The switches are not numbered as playfield switch-matrix addresses.
- PDF page 33 / printed page 28 shows the 8x8 playfield switch wiring, column-major SW9-SW64, separately from the cabinet flipper-button circuits.
- PDF page 34 / printed page 29 shows the 8x8 playfield lamp wiring LB1-LB64 and a separate G.I. lamp circuit.
- PDF page 32 / printed page 27 shows the +32 V L/R power-select relay on the MRB, the shared Q46-Q39 driver pairs, the post, kickback and Kickbig relay/coil circuits, five switch-triggered coils, and three flipper assemblies: Right Flipper, Left Flipper, and Upper Right Flipper.
- The production schematic labels the SP2-equivalent device `CLEAR POP BUMPER`, agreeing with both production coil tables.
- The production CPU/playfield schematics assign SP1/SP2/SP3/SP4/SP5/SP6 to Q11/Q9/Q8/Q10/Q12/Q13. The Coil Identification Table instead prints Q8/Q9/Q10/Q11/Q12/Q13; the structured wiring follows the schematics and preserves the three differing table cells as a conflict.
- The production schematic labels the right-flipper power lead at CN3 pin 6 `BLU-YEL`, while the production Coil Identification Table literally prints `BIU-YEL`. The structured record retains the printed table cell and records the same-manual disagreement explicitly.
