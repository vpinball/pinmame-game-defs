# Star Trek (Data East 1991) spatial evidence

Coverage stays **partial**. Placement status is observed throughout.

121 devices have coordinates. 6 have no spatial disposition.

The JSON report records each measurement, its object, drawing or texture locator, and the VPX extraction identity. Each drawing has its own affine fit from independently read pixel controls. The largest allowed leave-one-out residual is 0.04 normalized. Measurements near the edges or on the under-apron end extrapolate the controls. All drawing readings and projections are approximate.

Four slingshot switch placements project aperture centers from the 1992 × 4295 VPX playfield texture. The original-machine photo and bare-board reproduction photo identify the matching bores. The coordinates represent where the blades enter the playfield plane.

## Remaining placement work

- The three under-apron trough switch blades are obscured in the available photographs. Projected ball centers fall outside the photographic controls and disagree with independent controls near the trough.
- The factory schematic confirms four lamps on flash branch 1B, but the central pair shares a drawing region and the VPX supplies only one local proxy there. Keep those two middle positions open.
- The factory diagrams identify the GI feeds and the first three ramp-chase phase circuits. The retained table provides 26 shown bulb meshes in its GI collection, but their complete socket count and assignment to the two playfield feeds are unverified. Chase strips use render segments. The actual number and placement of emitters per phase remain unresolved.
- The reported locations use observed VPX object centers, factory drawing projections, and texture-aperture projections for the four slingshot blade entry points. Exact socket positions for the raised/rear lamps and hidden assemblies still need independent physical measurements.

Lamp 36 has a documented backbox lamp and a disputed additional playfield callout. Its playfield placement and total bulb count remain open.

## Flasher bulb accounting

The backbox counts are physical lamps on the same circuit. They are exempt from playfield coordinates. Rear-panel bulbs over the playfield count as playfield placements.

| Public output | Total bulbs | Backbox | Playfield located | Playfield pending |
| --- | --- | --- | --- | --- |
| 9 | 4 | 1 | 3 | 0 |
| 12 | 4 | 0 | 4 | 0 |
| 25 | 4 | 0 | 2 | 2 |
| 26 | 4 | 2 | 2 | 0 |
| 27 | 4 | 2 | 2 | 0 |
| 28 | 4 | 2 | 2 | 0 |
| 29 | 4 | 2 | 2 | 0 |
| 30 | 4 | 2 | 2 | 0 |
| 31 | 4 | 3 | 1 | 0 |
| 32 | 4 | 3 | 1 | 0 |

## Devices without coordinates or a spatial exemption

- `switch.left-trough`
- `switch.center-trough`
- `switch.right-trough`
- `lamp.ramp-chase-phase-1`
- `lamp.ramp-chase-phase-2`
- `lamp.ramp-chase-phase-3`
