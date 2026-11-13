# Breakshot — Cabinet, Backbox, & Playfield Lamps (location drawing)

Transcribed from `Capcom_1996_Breakshot_Manual.pdf` (Capcom PM00147, issue 05/02/96), PDF page 74, printed
page 70 (drawing P62400), the location drawing that faces the lamp table on PDF page 75 (`lamp-table.md`).
The page is a 150 dpi scan; the committed crop `lamp-locations.webp` is the whole drawing at its native
resolution (518x1313), with the backbox box above the playfield outline. The numbers were read on gridded
4x tiles of that crop and checked on 8x zooms; positions below are crop pixels.

## How the drawing marks a lamp

Every callout is a small black disc with a white label, printed on the lamp's insert or socket without a
leader line. Controlled lamps carry their table reference (`1`-`64`); general illumination sockets carry
their string number and a letter (`65A` ... `68Q`, skipping I and O, as the table does); the backbox
fluorescent carries `69`.

Every controlled reference from the table is printed exactly once, except two:

- `2` is not printed. The table prints row 2 as `12B NOT USED` with `-----` in every other cell.
- `27` is not printed. The table names it `43B RIGHT TOPLANE`. The drawing shows three top-lane inserts
  side by side below the row of ball inserts: the left one carries disc `45` (`65B LEFT TOPLANE`), the
  centre one disc `32` (`48B CENTER TOPLANE`), and the right one, at about (241, 484), is drawn as an
  insert outline with no disc. It is the only unlabelled lamp insert on the drawing.

## Callouts by area

The playfield outline runs from (24, 430) to (405, 1289).

- Backbox (above the playfield): `69` at the left of the backbox box.
- Top of the playfield: one row of ball inserts at y 468, left to right `9`, `14`, `10`, `15`, `13`,
  `16`; below it the top lanes, `45` and `32` at y 492 and the unlabelled right-lane insert.
- Upper left: `33` near the left orbit; `5`, `4`, `3` in a diagonal line below and left of the left
  bumper; `12` further left at the side; `8` below `3`, right of the captive ball lane.
- Upper centre: `25` and `26` either side of the centre pocket assembly's top, `11` inside the assembly
  below them.
- Upper right: `49` left of the right drop bank; `48`, `47`, `46` in a diagonal line along the bank's
  front; `7` at the right side, above the upper right flipper.
- Centre: `42`, `43`, `44` across the three centre pockets at y 754.
- Below the pockets, two fans of ball inserts: left `30`, `29`, `18`, `31`, `17`, `19`; middle `20`,
  `24`, `22` with `41` below them; right `38`, `37`, `39`; and `36`, `35`, `34` in a diagonal line at the
  right.
- The bonus rack, a triangle pointing down: `60`-`64` across its top row (y 938), then `56`, `57`, `58`,
  `59`, then `53`, `54`, `55`, then `51`, `52`, with `50` at its point (y 1015). `40` sits to its right,
  `21` below `40`, and `23` to the rack's left.
- Lower playfield: `28` at the left outlane (the kicker), `6` above the gap between the flippers.
- Cabinet: `1` at the bottom left corner of the outline, where the start button sits on the cabinet front.
- General illumination: `65A` and `65B` at the outline's front edge beside `1`, on no drawn part;
  `65C`-`65K` around the slingshots and inlanes and `65L`-`65P` up the lower left side; `66A`-`66J` up
  the left side with `66K`-`66N` either side of the centre pockets, `67A`-`67M` across the top, and
  `68A`-`68Q` down the right side.

## Legibility

The scan is coarse, so several digits are blurred. These readings were settled by the shape of the
legible stroke and by the one-label-per-reference set: `8` (6/8/9), `18` (8 vs 0/6), `23` (3 vs 8/9),
`28` (8 vs 3), `29` (9 vs 7), `33` (vs 35), `38` (8 vs 6/0), `40` (0 vs 8), `41`, `50` (0 vs 9/8), `56`
(6 vs 8/5), `58` (8 vs 6) and `61`; among the G.I. letters `65M`, `65P` (P vs R) and `68Q` (Q vs O/D).
Each reading falls within 0.02 normalized of the retained table's lamp object of that number.
