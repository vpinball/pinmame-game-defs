# FunHouse (Williams, 1990) spatial review

Status: partial. This is the first WPC-Alpha machine curated in this project. The physical machine record lives at `machines/partial/williams/funhouse-1990.json`.

The matching source is the retained known-working `Funhouse (Williams 1990)_1.3.vpx` at SHA-256 `69c37fa9a84e669a2934d6da0e5ee0277c4a0ef01e71eaa19e7271ba3396873e`. The retained extraction produced the embedded script at SHA-256 `322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- This manual carries a working `pdftotext` text layer, but its multi-column tables scramble under extraction, so every printed table used here was still read from 300/600 dpi rendered page images, not OCR text.
- FunHouse's switch matrix has exactly two opto positions (51, 55), both marked "(opto)" in the manual and both normalized by pinned PinMAME's inverted-switch mask -- a clean sweep with zero polarity disagreement.
- FunHouse is pre-Fliptronics WPC-Alpha hardware: `fhGameData` declares flipper switches only (`FLIP_SWNO(12,11)`) with no `FLIP_SOL()`, so no public solenoid address drives a flipper coil. Flipper power is wired through a dedicated flipper driver board (printed Flipper Circuits page) entirely outside the CPU-addressable solenoid matrix.
- Several switches and solenoids have no dedicated trigger/kicker object because the retained script sets their public state directly from another mechanism's own position (the trap door's rotation angle) or shares a saucer helper's underlying kicker object with a co-located switch. Those addresses are documented projections onto the real object that carries the underlying state, listed below.
- Two addresses (switch 63; G.I. strings 2 and 4's individual bulbs) and three lamps (54/55/56) have no asserted spatial placement at all rather than an invented or approximated coordinate.

## Explicit projections

- pinmame.input.switch 76: Projected onto the trap door primitive's own rotation state (PrTrap.RotX); the retained script sets this switch programmatically rather than reading a separate contact-switch object.
- pinmame.output.solenoid 5: Projected onto the trap door primitive; open/close solenoids share the mechanism's own position with switch 76.
- pinmame.output.solenoid 6: Projected onto the trap door primitive; see solenoid 5.
- pinmame.output.solenoid 3: Projected onto switch 46's position; the retained script's bsHideout saucer helper shares switch 46's own kicker object.
- pinmame.output.solenoid 16: Projected onto switch 65's position; the retained script's bsRudy saucer helper shares switch 65's own kicker object.
- pinmame.output.solenoid 8: Projected onto switch 28's position; the retained script's MBRelease handler acts directly on the WaSw28 lock-wall object with no separate release-mechanism object.
- pinmame.output.gi 1: Projected onto Rudy's own sign/shade assembly (RudySign1, RudySign2, RudyShade); the retained script's GI Case 1 drives that collection directly rather than a generic playfield wash.
- pinmame.output.solenoid 21: Projected onto switch 51 (Dummy Jaw); no dedicated jaw-motor VPX object was identified separately from Rudy's head figure.
- pinmame.output.solenoid 22: Projected onto switch 51 (Dummy Jaw); see solenoid 21.
- pinmame.output.solenoid 25: Projected onto switch 51 (Dummy Jaw); the only fixed point recorded for Rudy's Head Assembly.
- pinmame.output.solenoid 26: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.output.solenoid 27: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.output.solenoid 28: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.input.switch 73: Projected onto the retained table's Drain kicker object, shared with the outhole solenoid (1).

## Counts

- Placements: 141
- Located input addresses: 48
- Located output bindings: 88
- Unresolved input addresses: 1
- Unresolved output bindings: 5
- Inputs with a controlled `cabinet_or_service` record: 12
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 10
- Outputs with a controlled `cabinet_or_service` record: 4

## Promotion decision

This record stays `partial`. Two unresolved conflicts (`conflict.gangway-lamp-12-value`, `conflict.gi-region-naming`), six addresses with no spatial placement (switch 63; lamps 54/55/56; G.I. strings 2 and 4's individual playfield bulbs), and the absence of the mandatory independent high-tier cross-provider review together keep `coverage.status = "partial"` with `coverage.missing = ["spatial_placement", "unresolved_conflicts", "recreation_notes"]`. Every other dimension -- catalog identity, address enumeration, physical wiring, mechanism inventory and behavior, and variant coverage across the fifteen-driver `fh_l9` clone tree -- is validated.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json`, SHA-256 `85620e05458bd72bc57c2e203001a0f35db9806431e66e07ee08f05e90346ba9`, 2212 files, 219908807 bytes.
- Human transcription of every printed table read from the rendered manual pages: `external:pinmame-review-artifacts/funhouse/manual-transcription.md`.
