# The Sopranos — coil and flash lamp location drawing

Read from `Stern_2005_The_Sopranos_Service_Manual.pdf`, PDF page 9 (printed `DR. 7`, "COIL & FLASH LAMP LOCATIONS"),
left half. The drawing is an embedded 1-bit scan (1311 x 3306 px at 346 ppi); the crop `coil-flash-locations.webp`
renders it at that native resolution. It is drawn upright: rear at the top, flippers at the bottom, with a small
`Backpanel (front view)` box above the playfield.

Each coil or flash lamp is marked by its driver number in a box: white for above the playfield, black for below, grey
for not on the playfield. A small tag beside some flash-lamp boxes gives the colour of the mini-Mars dome
(`Color = Color of Mini-Mars of Flash Lamp Bulb`).

- Back panel box: two grey `26` boxes.
- Playfield: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18` (twice:
  a large black block at the upper left and a second box by the left ramp), `19`, `20`, `21`, `22`, `23`, `25`, `26`
  (one, with a `Yellow` tag), `27` (`Yellow`), `28` (`Yellow`), `29` (twice, each tagged `Red`), `30`, `31` (twice, one
  on each side of the playfield), `32` (twice, at the rear, either side of a small `K` mark), `AUX 1`, `AUX 2`, `AUX 3`.
  No `24` is drawn.

Notes printed beside the drawing:

- `Some Coil or Flash Lamp Diodes may be located under the playfield, in the Cabinet or Backbox on Terminal Strips or Diode Boards and not on the assemblies. DOTS: Diode On Terminal Strip See Section 5, Chapter 2, Playfield Wiring.`
- `Coil Q24 is Optional. If either a Coin Meter, Token Dispenser or Knocker (all optional equipment) is required, call Technical Support for more information, 1-800-542-5377 or 1-708-345-7700.`

The right half of the page carries generic `Typical Switch Wiring & Schematic`, `Dedicate Switch Schematic`, `Typical
Lamp Schematic & Wiring` and `Typical Coil Schematic & Wiring` drawings (the last uses #1 Trough Up-Kicker, 26-1200,
Q1, BRN-BLK, J8 and J10-P4/5 YEL-VIO as its example).

The coordinates of every callout, as read independently on this crop, and the curator's corrections and drawing
measurements are in `tools/seeds/stern/the-sopranos-2005-callouts.json` (page `pdf-9`).
