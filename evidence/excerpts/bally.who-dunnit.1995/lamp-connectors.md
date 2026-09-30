# WHO dunnit — Power Driver Board lamp connector list

Source: Bally *WHO dunnit* manual, PDF page 159, printed 3-27, continuation of the Power Driver Board connector list. Independently read from the native-resolution scan on 2026-09-30. This is a transcription of the connector-list claim; it does **not** replace the different matrix headers on PDF 124 (2-42).

The page explicitly prints **J133 Not Used** and **J137 Not Used**.

| Column | Printed playfield connector | Printed wire |
| ---: | --- | --- |
| 1 | J138-1 | Yellow-Brown |
| 2 | J138-2 | Yellow-Red |
| 3 | J138-3 | Yellow-Orange |
| 4 | J138-4 | Yellow-Black |
| 5 | J138-5 | Yellow-Green |
| 6 | J138-6 | Yellow-Blue |
| 7 | J138-7 | Yellow-Violet |
| 8 | J138-9 | Yellow-Gray |

J138-8 is printed **Key**. Each column above says “to playfield lamps”.

| Row | Printed playfield connector | Printed wire | Printed cabinet connector |
| ---: | --- | --- | --- |
| 1 | J135-1 | Red-Brown | — |
| 2 | J135-2 | Red-Black | — |
| 3 | J135-4 | Red-Orange | — |
| 4 | J135-5 | Red-Yellow | — |
| 5 | J135-6 | Red-Green | — |
| 6 | J135-7 | Red-Blue | J134-7 |
| 7 | J135-8 | Red-Violet | J134-8 |
| 8 | J135-9 | Red-Gray | J134-9 |

J135-3 and J134-3 are printed **Key**. J134-1/-2/-4/-5/-6 are **Not Used**. J135 rows say “to playfield lamps”; J134 rows 6–8 say “to cabinet lamp”. A dash in the excerpt's cabinet column means this page gives no corresponding row assignment, not proof of an absent lamp.

The separate insert column feed is printed **J136-3 Yellow-Gray Col 8 to insert lamps**; J136-1 is **Key**, and J136-2 **Not Used**.

## Unresolved difference from the matrix

PDF 124 (2-42) instead prints columns 1–6 on **J137-1..6**, columns 7/8 on **J138-7/9**, and all eight row headers on **J133-1,2,4..9**. Thus all 64 matrix cells carry the row-header discrepancy; columns 1–6 also carry a column-header discrepancy. Cabinet lamps 87/88 have the additional J134/J136 routing claim. Only the column-7 J138-7 and column-8 J138-9 assignments agree narrowly; J138-8 is a key in this list. Agreement on those pins does not corroborate the remaining headers. Preserve both readings as `conflict.lamp-matrix-connectors` until a documented original production harness/board inspection or applicable factory correction settles the physical routing.
