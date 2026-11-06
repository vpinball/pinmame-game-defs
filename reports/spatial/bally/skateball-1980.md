# Skateball (Bally 1980) spatial blockers

Coverage: **partial**; missing `input_semantics`, `output_semantics`, `spatial_placement`.

The retained VPX table SHA-256 is `ddbcae8cdc87ccdd7305f02ad853bd039d4b6489b25bcd2b82c0c8e03e07fb02`; script `79336a53246582251087cd3a0892fe0e228737ea9e626813e2010bdcd65928c7`; extraction manifest `974f9fa675b77a99956f9d048cf5e426abbbef56bf13590cfc03043de98bbc0b` (806 files, 30137552 bytes). The machine definition is `b8d8d295890603aa33c212dfb44e86c08d97cec74834f2b45ae96b9ee23af029` and spatial seed `1b04ea1bd542f66445258504f34063a74ba4c4dd99322c1d19dc69ddaf29186e`.

VPX player view: x = raw_x / 952, y = raw_y / 1974, rounded to six decimals. Wall points use the arithmetic mean of all drag points; reset-coil projections use the arithmetic mean of raw target centers. Bank and coil projections are not physical coil centers.

The seed holds 38 raw object anchors, their individual file hashes and drag points where applicable, and every device derivation. There are 50 placements: 50 observed. There are 53 used devices without placements.

## Evidence and decisions

- The manual (SHA-256 `0758b23c3d33b28c06be006ba768151075b0f31ae9cddad6739e6c5ab7513a1a`) PDF 21 lists the switch and coil self-test labels. PDF 13's top-parts drawing and an owner photograph show an upper-left drop bank with the rollover lanes to its right. Figure V on PDF 22 differs in upper-bank and lane geometry; it was not fitted or used to validate placements. All coordinates remain observed.
- The switch positions use script-bound triggers, targets, bumpers, spinner and kicker centers, except for the observed outer-lane override. The manual's self-test table names switch 13 lane #3 and 15 lane #1 without assigning sides; Figure V separately draws rollover circles 15, 14, 13 left-to-right and corroborates relative number order. Its differing upper-playfield geometry is not fitted or used to validate absolute placements/as-built artwork. Photo-026 clearly shows #1 left and #3 right on a physical replacement reproduction, agreeing with the redrawn table artwork; it does not independently authenticate original 1980 artwork. The old-board photo-022 has unreadable lane numerals. Crosswise anchors 13 at Trigger.sw15/right and 15 at Trigger.sw13/left remain observed and cite photo-026 for orientation, the manual for identity/relative order, and table objects for coordinates.
- The table's lane switch/lamp pairing is internally consistent: switch 13 with lamp 24 (Light.l24, x 481.5) at left, switch 15 with lamp 56 (Light.l56, x 685.6491) at right. Both halves differ from the observed replacement-board/artwork orientation; this is not described as a factory-proven lane defect. Lamps 24/56 remain unplaced and no render-light center is adopted as a socket position.
- Switch 17 uses seven script-bound wall drag-point centroids as projections onto three drop-target and four rebound scoring assemblies; the slingshot switch locations likewise use wall centroids. Reset coils use the means of their bank targets; saucer, bumper, slingshot and flipper coils project onto their modeled mechanisms or pivots. None is a measured coil center.
- The schematic (SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`) PDF 10 names the left, bottom and right thumper lamps. Lamps 25, 41 and 57 use the corresponding bumper centers as projections of hidden bulbs, not observed socket centers. The retained table script swaps left and right bindings for 25 and 57; physical labels determine placement.
- The table's Drain is a destroy/helper below the physical outhole, and BallRelease is a serve helper. Neither establishes the physical outhole center; switch 8 and coil 7 remain unplaced.
- Of 119 extracted Light objects, 27 show a bulb mesh; all are gi-prefixed. No controlled lamp light shows a bulb mesh. The playfield underside photograph contains sockets but does not supply a registered per-socket map with circuit identities. No other controlled lamp positions are inferred from insert or render-helper centers.
- The related VPW 1.0 recreation (table SHA-256 `7afc7026cfeb51b7346c8080dfc91a5d49e9ecb7ddd97a330b8139f0347b48fc`, script `d2f021710d7260d26f825176574ae2b3d7968d00973a865eefd75c734dabb0ff`, manifest `5a9c466b3c89d14f3a0ca4bde4fcdefbb76ade1cfb05d03484ed1c5fde2018d3`; 2507 files and 699407300 bytes) has 85 Light objects, none with a visible bulb mesh. It is based on a mod of the earlier table, so it is not independent geometry validation. Its combined `BM_Parts` mesh was exported to world-space OBJ `7501ac70d1e31d88f385d94ede21d05bdf11a04a2141bfc9ee5a0542a643e57b` and welded at 0.1 VPU into 965 pieces (inventory `22e1f79f39723a254c1a5d9d6b2954c0ae85ece1a5a21789c7ae9f1e1d278025`). The three largest pieces align with top-lane inserts and have flat profiles; the investigation does not establish a reliable physical socket identity and wiring map. The later lamp 25 and 57 lighting arrays agree with the factory bumper sides.
- The table's always-on GI lights are not PinMAME-controlled GI outputs. The 5.9 VAC factory GI circuit is physical illumination; the table lights do not establish its complete socket count or wiring membership.

- Continuous outputs 17/20 are physically unfitted according to the game's own wiring, but their published startup burst is unexplained. All 17-20 rising/falling edges are retained in continuous-startup-observations.md. Inversion and timing alone do not prove the PIA/ROM cause; availability remains unknown and output_semantics stays missing. Their spatial N/A records refer only to physical non-fitment.

## Unplaced used devices

- `device.outhole-kicker` — Outhole kicker
- `lamp.1-2-3-special` — 1-2-3 special
- `lamp.10k-bonus` — 10K bonus
- `lamp.1k-bonus` — 1K bonus
- `lamp.20k-bonus` — 20K bonus
- `lamp.20k-saucer` — 20K saucer
- `lamp.2k-bonus` — 2K bonus
- `lamp.2x-bonus` — 2X bonus
- `lamp.30k-saucer` — 30K saucer
- `lamp.3k-bonus` — 3K bonus
- `lamp.3x-bonus` — 3X bonus
- `lamp.40k-bonus` — 40K bonus
- `lamp.4k-bonus` — 4K bonus
- `lamp.4x-bonus` — 4X bonus
- `lamp.50k-saucer` — 50K saucer
- `lamp.5k-bonus` — 5K bonus
- `lamp.5x-bonus` — 5X bonus
- `lamp.60k-bonus` — 60K bonus
- `lamp.6k-bonus` — 6K bonus
- `lamp.7k-bonus` — 7K bonus
- `lamp.8k-bonus` — 8K bonus
- `lamp.9k-bonus` — 9K bonus
- `lamp.a-drop-target` — A drop target
- `lamp.a-lane` — A lane
- `lamp.b-lane` — B lane
- `lamp.bonus-special` — Bonus special
- `lamp.credit-indicator` — Credit indicator
- `lamp.e-drop-target` — E drop target
- `lamp.k-drop-target` — K drop target
- `lamp.left-outlane-special` — Left outlane special
- `lamp.lower-rollover-button` — Lower rollover button
- `lamp.middle-drop-targets-100k` — Middle drop targets 100K
- `lamp.middle-drop-targets-10k-center` — Middle drop targets 10K center
- `lamp.middle-drop-targets-10k-left` — Middle drop targets 10K left
- `lamp.middle-drop-targets-10k-right` — Middle drop targets 10K right
- `lamp.middle-drop-targets-20k-left-arrow` — Middle drop targets 20K left arrow
- `lamp.middle-drop-targets-20k-right-arrow` — Middle drop targets 20K right arrow
- `lamp.number-1-lane` — Number 1 lane
- `lamp.number-2-lane` — Number 2 lane
- `lamp.number-3-lane` — Number 3 lane
- `lamp.right-outlane-special` — Right outlane special
- `lamp.s-drop-target` — S drop target
- `lamp.same-player-shoots-again` — Same player shoots again
- `lamp.saucer-collect-bonus` — Saucer collect bonus
- `lamp.saucer-extra-ball` — Saucer extra ball
- `lamp.spinner-1k` — Spinner 1K
- `lamp.spot-multiplier` — Spot multiplier
- `lamp.t-drop-target` — T drop target
- `lamp.top-center-drop-target-arrow` — Top center drop target arrow
- `lamp.top-left-drop-target-arrow` — Top left drop target arrow
- `lamp.top-right-drop-target-arrow` — Top right drop target arrow
- `lamp.upper-rollover-button` — Upper rollover button
- `switch.outhole` — Outhole

## Projection and evidence inventory

- `assembly-projection`: `solenoid:11`, `solenoid:12`, `solenoid:13`, `solenoid:14`, `solenoid:15`, `solenoid:2`.
- `bank-centroid-projection`: `solenoid:10`, `solenoid:8`, `solenoid:9`.
- `direct`: `switch:14`, `switch:18`, `switch:19`, `switch:2`, `switch:20`, `switch:21`, `switch:22`, `switch:23`, `switch:24`, `switch:26`, `switch:27`, `switch:28`, `switch:3`, `switch:30`, `switch:31`, `switch:33`, `switch:34`, `switch:35`, `switch:38`, `switch:39`, `switch:4`, `switch:40`, `switch:5`.
- `flipper-pivot-projection`: `solenoid:46`, `solenoid:48`.
- `hidden-bulb-projection`: `lamp:25`, `lamp:41`, `lamp:57`.
- `physical-lane-override`: `switch:13`, `switch:15`.
- `wall-centroid`: `switch:36`, `switch:37`.
- `wall-contact-projection`: `switch:17`.

Retained evidence: `manuals/by-machine/bally.skateball.1980/` for the originals, rendered pages and OCR; `vpx-sources/bally/skateball-1980/` for the original table, extraction and candidates; `review-artifacts/skateball-1980/photos/` for old-board photos 022/036, replacement-board photo 026 and their download manifest. Photo excerpts are `evidence/excerpts/bally.skateball.1980/playfield-photo-observations.md` and `replacement-playfield-lanes.md`; exact unexplained callback edges are in `continuous-startup-observations.md`.
