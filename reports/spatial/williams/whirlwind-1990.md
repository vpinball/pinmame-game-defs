# Whirlwind (Williams, 1990) spatial review

Status: author_ready. Complete physical inventories, bulb placements and documented projections are reconciled with the factory construction and retained runtime source.

Coordinates use x/964 and y/2162: left=0, right=1; rear=0, front=1. A renderer glow does not supply a socket coordinate.

## Evidence decisions

- Factory construction identifies 13 C-bank playfield flashlamps. The complete D13356 catalog elevation and actual LMP1-LMP10 pattern prove five rear-playfield flashlamps plus five GI positions; the independent handbook specifies 2/1/2 on 37/39/40, correcting the operations table's three-left-bulb erratum. The original script drives playfield glow helpers and additional backglass/VR proxies; the former mounting conflict was a source-reading error.
- GI 11 has 15 controlled bulbs: 10 playfield plus 5 rear-panel. GI 16 has 29: 11 playfield plus 18 controlled backbox. Seventeen constant backbox and two coin-door bulbs are excluded. Each playfield emitter has a pinned physical inventory and reviewed coordinate; rear sockets project onto their own panel plane.
- All 13 C-bank flashlamps are placed: 5 actual dome bases, 6 measured factory symbols and 2 physically photographed under-insert glass bodies. The latter use bounded two-camera projections at approximately (.527,.331)/(.616,.352), with 0.015 normalized uncertainty; no exact filament/Z claim.
- All 57 playfield matrix bulbs reconcile factory construction with actual socket/PCB correspondence. Six own jet meshes agree exactly; two own cellar glass meshes replace colored cover centers. Insert/glow helpers never add quantities or displace physical bulbs.
- ROM Switch Levels proves targets 26-29 active at public 1 and inactive at 0, with control 15 before and after. The uninverted S11 read path and zero mask establish normally-open matrix contacts. See the portable drop-target-levels excerpt.
- Both right flippers have their own coils and EOS switches, sharing one cabinet button. The two physical right coils do not have independent CPU outputs.
- Jet 21 follows the location list's Lower Top Jet Bumper, resolving the duplicated Top Lower wording in the wiring table.

## Promotion decision

- No authoring-critical spatial or semantic blocker remains. Approximate photo measurements, rear-panel projections and renderer limitations are explicitly disclosed.

## Explicit mechanism projections

- Switch 10: Projected onto the Drain kicker (Kicker.Drain, table object center): switch 10 (Outhole) has no dedicated VPX trigger object -- the retained script's cvpmBallStack helper (bsTrough.InitSw 10,11,12,13) manages it abstractly, and Drain is the physical object nearest the outhole funnel (Drain_Hit feeds the trough via bsTrough.addball).
- Switch 11: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center): switches 11-13 (Ball Trough #1-#3) have no individual VPX trigger objects -- the retained script's cvpmBallStack helper manages all three abstractly against the single BallRelease exit kicker (bsTrough.InitKick BallRelease,75,4), the trough mechanism's own retained object.
- Switch 12: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.
- Switch 13: Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.
- Switch 42: Projected onto the Right Ramp's own retained geometry (the RightRampUp/RightRampDown shared entry endpoint, table object center): switch 42 (Right Ramp Down) has a real printed switch part (5647-12001-00) but no dedicated VPX trigger object -- the retained script instead sets Controller.Switch(42) directly from the same SolRightRampEntryLifter/SolRightRampEntryDown handlers that swap the ramp's up/down geometry, because the physical switch is mechanically slaved to the same ramp position those solenoids control.

## Counts

- Placements: 166
- Located input addresses: 46
- Located output bindings: 89
- Outputs with no spatial record: 0
- Outputs with incomplete spatial records: 0

## Retained evidence

- Original table SHA-256: `105477078e68547c24167fc9ba99baeff24ec48ce16c46ec2530184a67f92e23`; script: `e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2`.
- Manual SHA-256: `365421ffdc059180ef5457fec2aa7567981954c383ab26d6b1e92223b790c649`; source record carries acquisition URLs and per-page excerpts.
- Extraction: 1881 files, 129468345 bytes, canonical sorted manifest SHA-256 `4b3b7045c243787f381a42be2479aa53325783618820689468b6b0bce8dc7b49`.
- Research, supplemental tables, raw runtime traces and geometry checks: `external:pinmame-review-artifacts/whirlwind-20261106/` and `external:pinmame-vpx-sources/williams/whirlwind-1990/supplemental-20261106/`.
