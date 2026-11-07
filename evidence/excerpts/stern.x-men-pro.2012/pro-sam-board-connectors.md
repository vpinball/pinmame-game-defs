# Pro SAM board: complete output connector regions

Stern Service Bulletin 178, page 2, identifies X-MEN as CPU 520-5246-02 / I/O Power Driver 520-5249-00, and X-MEN (L/E) as CPU 520-5303-04 / I/O Power Driver 520-5317-00. The Batman row also identifies 520-5249-00. Original bulletin: https://sternpinball.com/wp-content/uploads/2018/10/sb178.pdf, SHA-256 9eb0e9f6eaa277a1c4f005d575b3015720f31df0fe083760bfe1b44c152cecf9, 217489 bytes, two pages. The printed date is December 13, 2011; the apparent chronology is not silently corrected.

The exact 520-5249-00 schematic is retained in Stern's Batman TDK manual, SHA-256 c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219, 10579058 bytes, 207 pages. PDF pages 136/137 (printed 116/117), sheet 2 LEFT/RIGHT, show the internal output routes. PDF 142 (printed 122) gives the component layout. These are the same board's internal connections, not Batman harness, load or fitment evidence. The original Pro cabinet board photograph `gallery-images/sale-23-19.jpg` independently shows the ordinary SAM topology corresponding to this layout; the bulletin establishes the actual edition/part association.

All pins in the four output connector regions are transcribed below. Q numbers name driver transistors, not independent evidence of a fitted load.

| Connector | Pin | Internal route |
| --- | ---: | --- |
| J8 | 1 | Q1 |
| J8 | 2 | KEY |
| J8 | 3 | Q2 |
| J8 | 4 | Q3 |
| J8 | 5 | Q4 |
| J8 | 6 | Q5 |
| J8 | 7 | Q6 |
| J8 | 8 | Q7 |
| J8 | 9 | Q8 |
| J9 | 1 | Q9 |
| J9 | 2 | Q10 |
| J9 | 3 | KEY |
| J9 | 4 | Q11 |
| J9 | 5 | Q12 |
| J9 | 6 | Q13 |
| J9 | 7 | Q14 |
| J9 | 8 | Q15 |
| J9 | 9 | Q16 |
| J7 | 1 | +20V |
| J7 | 2 | Q17 |
| J7 | 3 | Q18 |
| J7 | 4 | Q19 |
| J7 | 5 | KEY |
| J7 | 6 | Q20 |
| J7 | 7 | Q21 |
| J7 | 8 | Q22 |
| J7 | 9 | Q23 |
| J7 | 10 | Q24 |
| J6 | 1 | Q25 |
| J6 | 2 | Q26 |
| J6 | 3 | Q27 |
| J6 | 4 | Q28 |
| J6 | 5 | Q29 |
| J6 | 6 | Q30 |
| J6 | 7 | Q31 |
| J6 | 8 | Q32 |
| J6 | 9 | KEY |
| J6 | 10 | +20V |

The own Pro game chart literally copies `J8-P1`, `J8-P2`, `J8-P4`, `J8-P5`, `J8-P6`, `J8-P7`, `J8-P8`, and `J8-P9` into rows 9-16; that source reading remains unchanged in `pro-coils.md`. Structured control connections instead follow the exact board's J9 routes above. The LE chart's `J8-P11`, `J8-P12`, `J8-P14`, `J8-P15`, `J8-P16`, `J8-P17`, `J8-P18`, and `J8-P19` belong to the different 520-5317-00 board and cannot independently correct the Pro. The correction changes neither stable device IDs nor public numerical bindings. Game-specific power/control wire colors, loads and functions continue to follow the own Pro chart, with literal diagnostic differences disclosed separately.
