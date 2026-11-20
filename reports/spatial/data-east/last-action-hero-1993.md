# Last Action Hero (Data East, 1993) spatial review

Status: observed. Every playfield switch but the crane limits, every coil the retained table models with a script-bound object and the three magnets are placed from that table; cabinet, backbox, topper, virtual and unused addresses carry a controlled `not_applicable` record. The matrix lamps, the flash lamps, flash drive 9, the G.I., the crane lock, the knocker and the crane limit switches have no coordinate. No placement was checked against the manual's location drawings, so every placement stays `observed` and the record stays at `machines/partial/data-east/last-action-hero-1993.json`.

The geometry source is the retained known-working `Last Action Hero (Data East 1993) VPW v1.1.vpx` (SHA-256 `0a1e3fcfc652086003106fb22290ec54166dd5121f8d405f4a3cd2389d59b173`); its embedded script (SHA-256 `1038027da4bdabe7a447d96df6eb79bb3830b2af18a17330d709feb4eaa139e5`) is the runtime binding authority. Exact playfield bounds are 952 x 2162; every table coordinate is x/952 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority; the 1993 manual and its schematic book are the physical inventory, construction and wiring authority; the 1.12 ROM's own service tests settle names and switch-to-coil pairs; pinned PinMAME owns controller topology; the retained table supplies geometry for script-bound objects only.
- The table is a Visual Light Mapper build. `Lampz.MassAssign` binds each matrix lamp to a bulb-mode light-map source Light that draws no bulb, and the table models no insert bulb; a light that sits on no bulb makes no socket, so no matrix lamp is placed, and a raised socket (a flasher dome, a crane cab lamp, a back-panel lamp) is never placed on such a source either, so no flash lamp is placed.
- Primitives are placed at the centre of their world-space mesh bounds from the retained `vpxtool export obj --units vpu` export (SHA-256 `3213fbabb085338dd19d06179a899baedd82be4c35228f7a6cf46cd938ffa6b7`); the crane is placed at the rotation axis its three meshes share, which the builder checks against the script's ball-on-the-boom formula.
- Triggers and walls are placed at the centroid of their drag points, never at the editor pivot a Trigger stores.
- The Left/Right relay 10, the shaker motor 16, the topper flash groups 1R and 7R, the credit-button lamp 64 and the cabinet switches are cabinet, backbox or topper devices.

## Blockers

- Every placement comes from one community table (the VPW Film Crew's v1.1) and none was checked against the manual's location drawings, so all of them stay observed. Promotion needs a callout check of the drawings or a second, independent table lineage.
- No matrix lamp has a coordinate. The table drives lamps 1-63 through bulb-mode light-map source Lights that draw no bulb and models no insert bulb, and a light that sits on no bulb makes no socket; the lamps need a reproducible measurement on the manual's Lamp Locations drawing (printed page 31). Lamps 31, 40 and 43 have no bound Light at all: each lights two inserts, the script fades two light-map sets for each with live Lampz.Callback lines and leaves only its Lampz.MassAssign line commented out, and choosing between the table's Lights would rest on their names alone. Which address the right captive-ball insert is wired to is a recorded conflict.
- Flash lamps 2R-6R and 8R (26-30, 32) have no coordinate: the table drives them through light-map sources at playfield height and models no bulb or dome, and a raised flash-lamp socket is never placed on a light-map source. Their sockets are drawn on the manual's Flash Lamp / Coil Tests location drawing.
- Flash drive 9 has no coordinate: two of its lamps ride the crane boom and two light the backbox insert.
- The G.I. relay 11 has no coordinate: the table's G.I. Lights are light-map sources that draw no bulb, and no retained page counts or locates the G.I. bulbs.
- The crane lock 4 rides the sweeping boom and has no fixed location; the knocker 8 is located by no retained page.
- CN3 pins 5-1 (solenoid addresses 40-44) have no coordinate: no retained page shows anything connected to them.
- The crane motor 14 is a projection onto the crane's rotation axis, and the drop-target reset coil 13 a projection onto the middle drop target.
- The crane limit switches 60 and 61 have no coordinate: the table binds no object to them, and the manual's Switch Locations drawing (printed page 29) prints them at the two ends of the boom's sweep, 60 at the left ramp entrance and 61 at the top of the right orbit beside 47, not at the crane's axis.
- The three magnets 37-39 are placed on the table's magnet triggers; the manual says only that they are in the centre of the playfield.

## Explicit projections

- pinmame.output.solenoid 13: The drop-target reset coil is projected onto the middle drop target sw19; the retained table models no coil.
- pinmame.output.solenoid 14: The crane motor is projected onto the crane's rotation axis, which the Crane Assembly drawing puts the motor under; it is not a measured motor centre.

## Counts

- Placements: 65
- Validated input addresses: 0
- Observed-only input addresses: 46
- Validated output bindings: 0
- Observed-only output bindings: 19
- Output bindings with no coordinate: 78
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `unused` record: 11
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 11

## Promotion decision

Refused. `coverage.missing` lists `spatial_placement` because every coordinate rests on one community table without a drawing check and the matrix lamps, the flash lamps, the G.I., the crane lock and the knocker are not placed; the other open requirements keep the record partial as well.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/data-east/last-action-hero-1993/vpw-1.1/extracted-vpxtool.manifest.json`, SHA-256 `0a3fcdbabc4d9b1076e9be0a1117c996b06b7a42421a6cd024fd2b27149faca8`, 2652 files, 1996442982 bytes.
- World-space export `external:pinmame-vpx-sources/data-east/last-action-hero-1993/vpw-1.1/world-obj/Last Action Hero (Data East 1993) VPW v1.1.obj`, SHA-256 `3213fbabb085338dd19d06179a899baedd82be4c35228f7a6cf46cd938ffa6b7`.
- Manual SHA-256 `546f0272d7d2a4334224843fc1498077c45896cb8c492daa569ac07d3161c61d`; schematic book SHA-256 `7925654b30802ba7246efdddcebb90cba62cffd39ad36945124d005fec30d702`.
