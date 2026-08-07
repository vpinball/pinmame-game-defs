# Congo (Williams, 1995) spatial review

Status: validated. Every spatial dimension audited here is complete except for one switch, but the physical machine record itself remains `partial` at `machines/partial/williams/congo-1995.json` because that one address has no reliable coordinate; see the promotion decision below.

The matching source is the retained known-working `Congo (Williams 1995) 1.1.vpx` at SHA-256 `45a6448efb586475a6886962c5bace44789be1d7cd3dde2c507169fdf085432c`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `19c19ea64bb120af66ef3ca309a2ec98c08b35ecf08e198bb26b3cd1611cd936`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a usable but imperfect OCR text layer (Paper Capture scan); every printed table used here was still read from 300/600/1200 dpi renders and transcribed by hand into `evidence/excerpts/williams.congo.1995/`.
- Several switches have no dedicated playfield trigger object because the retained script's cvpmTrough helpers (bsTrough, bsVolcano) model multi-position ball sensing purely as an internal switch array. Those addresses are explicit documented projections onto the real kicker object that carries the mechanism's exit/entry point.
- GiTop member `GI10_Deactivated` is excluded as a table modeling anomaly (its own name marks it disabled); GI address 1's physical quantity is 13, not the collection's raw 14 members.
- Flasher `F8L3` (part of solenoid 27, Volcano Flasher) sits at normalized x=1.022303, outside the retained table's 0..1 playfield bounds, and is excluded as the modeled stand-in for the printed table's backbox bulb; the other three Volcano Flasher bulbs (2 playfield #89, 1 playfield #906) are placed normally.
- GI strings 0-2 use the retained table's GiGorilla/GiTop/GIBottom emitter collections, matching the retained script's `UpdateGi`/`UpdateGiOn` dispatch exactly. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- Solenoids 41-44 are PinMAME's unused WPC-95 LPDC mirrors; Congo populates no LPDC output at all (37-40 are also unused), unlike WPC-95 games with a DC-motor mechanism.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.
- Switch 25 (Right Eject Rubber) is the sole unresolved spatial gap; its `spatial` key is omitted entirely rather than a coordinate or an undefined status being invented, matching the precedent set by other partial records in this project for a genuinely unlocatable address.

## Explicit projections

- Switch 31: Projected onto the trough's own release kicker (Kicker BallRelease, table object center): the retained cvpmTrough helper (bsTrough) models switches 32-35 purely as an internal switch array with no separate playfield trigger object, and the trough-eject opto is pulsed in the same SolRelease handler that fires the BallRelease kicker.
- Switch 32: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31. The retained cvpmTrough helper has no separate visible object per ball position.
- Switch 33: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 34: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 35: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 41: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center): the retained cvpmTrough helper (bsVolcano) models switches 41-43 purely as an internal switch array with no separate playfield trigger object, and the volcano ejects a locked ball through the same sw36a kicker (.Initexit sw36a).
- Switch 42: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.
- Switch 43: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.

## Counts

- Placements: 187
- Located input addresses: 51
- Located output bindings: 100
- Unresolved input addresses: [25]
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 14

## Promotion decision

No authoring-critical semantic, wiring, or mechanism question remains unresolved, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Switch 25 (Right Eject Rubber) is a genuinely used, printed switch with no reliable coordinate anywhere in the retained thin table -- its only candidate VPX object shares an identical, evidently-unmoved local-space coordinate with an unrelated object -- so it is left without a `spatial` key rather than being invented. The definition therefore carries `coverage.missing = ["spatial_placement"]` and stays `partial` until a richer retained table, a manual playfield diagram calibration, or another source resolves this one address.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/congo-1995/extracted-vpxtool.manifest.json`, SHA-256 `c9b02744cbb2e1b0659c7032b0ef42d4e7cadf5c36ed33ac171a037b8be82b62`, 925 files, 47770557 bytes.
- Human-readable manual transcriptions under `evidence/excerpts/williams.congo.1995/` (six tables plus the DIP switch chart), each hashed and cited from the definition's manual source record.
