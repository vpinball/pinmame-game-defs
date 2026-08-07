# Creature from the Black Lagoon — Lamp Matrix wiring table

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 108, printed page 3-4, "LAMPS" /
"LAMP MATRIX CIRCUIT". Read directly from a 300 dpi `pdftoppm` render.

Column headers (drive, Power Driver Board J137/J138): 1 Yellow-Brown/J137-1/Q98, 2 Yellow-Red/J137-2/Q97,
3 Yellow-Orange/J137-3/Q96, 4 Yellow-Black/J137-4/Q95, 5 Yellow-Green/J137-5/Q94, 6 Yellow-Blue/J138-6/Q93,
7 Yellow-Violet/J138-7/Q92, 8 Yellow-Gray/J138-9/Q91.

Row headers (return, J133): 1 Red-Brown/J133-1/Q90, 2 Red-Black/J133-2/Q89, 3 Red-Orange/J133-4/Q88,
4 Red-Yellow/J133-5/Q87, 5 Red-Green/J133-6/Q86, 6 Red-Blue/J133-7/Q85, 7 Red-Violet/J133-8/Q84,
8 Red-Gray/J133-9/Q83.

The 64-cell body of this table reproduces the same lamp-address-to-description mapping as
`lamp-locations.md` (verified by spot-checking every row against the Lamp Locations parts list; no
disagreement found), so it is not retyped cell-by-cell here — this excerpt exists to record the column
and row wiring identity, not a second copy of the label table. `J1XX = Power Driver Board`.

The circuit description explains the standard WPC lamp-matrix drive: the processor toggles a 74LS74
per column through a ULN-2803/TIP107 driver (bringing the column high) while a TIP102 row driver grounds
the selected row, turning the lamp on; over-current is sensed by an LM339 comparator that forces the
row driver off. No opto or special-construction language appears anywhere on this page; every lamp
address is an ordinary incandescent bulb per its Bulb No. column in `lamp-locations.md` (#906-family
lamp-locations bulb types translate to #555/#44 printed types elsewhere but no distinct construction
class).
