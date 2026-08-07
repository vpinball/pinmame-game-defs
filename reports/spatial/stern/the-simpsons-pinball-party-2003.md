# The Simpsons Pinball Party (Stern, 2003) spatial review

Status: partial. The physical machine record itself is `partial` at `machines/partial/stern/the-simpsons-pinball-party-2003.json` for the reasons below; most devices this audit covers do carry a validated placement or a documented projection, but a real, honest gap remains for lamps 73-80 and two unresolved source conflicts.

The matching source is the retained known-working, non-VPW `The Simpsons Pinball Party v0.8.2.vpx` at SHA-256 `c7d14c512ae81eb0e26cddf9f74690818ae2259350cd334fc98be5e7ece79034`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `5378f6baf3106ed013c6d1a787f4b6789bc1febe925903f05cb2eda9327b98ee`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2115`, and every canonical coordinate is x/952 and y/2115 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Stern operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology and public address arithmetic; the retained table supplies geometry.
- The retained manual's text layer double-doubles most characters and additionally shifts character codes by a constant on the diagnostics chapter's own embedded font subset; every printed table used here was read from a rendered page and transcribed into `external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/manual-transcription.md`, never from `pdftotext` output.
- Trough switches 10-14 and the stacking opto 15 have no dedicated playfield trigger object because the retained script reads all six through the shared cvpmBallStack helper class rather than individual Hit/Unhit events; all six are documented projections onto the trough's own release-kicker object (BallRelease).
- Solenoids 4 (Drops Reset Up) and 30 (Drop Bank Trips) act on all three drop-target bank positions at once and have no separate reset-bar mesh in the retained table; both are documented projections onto the bank's own middle target (Drop Target #2).
- Lamp 32 (Tournament Button) and matrix switch 53 (Tournament Button) are both optional, gated behind the Optional Tournament Kit per matching manual footnotes on both the switch- and lamp-locations pages; lamp 32 additionally has no `l32` object in the retained script's own lamp-fade sequence at all.
- Lamps 73-80 (Mini-DMD sign LEDs) take no spatial key at all rather than a fabricated or shared-local-origin coordinate: the retained table's LEDY/LEDG/LEDR collections are empty and the l73-l80 Primitive objects that do exist share one (x, y) distinguished only by a synthetic z stack.
- General illumination is a single aggregate PinMAME channel (`coreGlobals.nGI = 1`); its 42 placements come directly from the retained table's own `GI` collection (37 `GI_N` Light objects plus 5 `spotlightright*` objects), which the script's UpdateGI toggles together, matching the manual's own single-relay, multi-fuse wiring diagram.
- Solenoid 24 (Optional Coil) and solenoids 33-35 (AUX 1-3, UK-only up/down posts) take controlled `not_applicable`/`unused` records per their explicit manual footnotes; the retained table (a US/export-configuration recreation) models no object for any of them.

## Explicit projections

- pinmame.input.switch 10: Projected onto the five-ball trough's own release kicker (BallRelease, table object center): bsTrough.InitSw 0,14,13,12,11,10,0,0 reads all five trough positions through the shared cvpmBallStack helper's internal ball-queue logic, which exposes no separate playfield object per position.
- pinmame.input.switch 11: Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.
- pinmame.input.switch 12: Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.
- pinmame.input.switch 13: Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.
- pinmame.input.switch 14: Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10. Switch 14 is also the trough VUK opto nearest the kicker (Sw. 14 & 15 Part Note).
- pinmame.input.switch 15: Projected onto the five-ball trough's own release kicker (BallRelease, table object center): the 5-Ball Stacking Opto shares its Transmitter/Receiver OPTO PC Board note with switch 14 and has no dedicated playfield object in the retained extraction either.
- pinmame.output.solenoid 1: Projected onto the five-ball trough's own release kicker (BallRelease, table object center): SolRelease pulses bsTrough.ExitSol_On, the shared cvpmBallStack ejector for the whole trough, not a fixed visible coil body.
- pinmame.output.solenoid 4: Projected onto the drop-target bank's own middle target (SW18/Drop Target #2, table object center): dtDrop.SolDropUp resets all three bank positions together and the retained table exposes no separate reset-bar mesh.
- pinmame.output.solenoid 30: Projected onto the drop-target bank's own middle target (SW18/Drop Target #2, table object center): SolDropBankTrips (dtDrop.Hit 1/2/3) trips all three bank positions together; see solenoid 4.

## Counts

- Placements: 204
- Located input addresses: 51
- Located output bindings: 103
- Inputs with no spatial key at all: 0
- Outputs with no spatial key at all: 8
- Inputs with a controlled `cabinet_or_service` record: 20
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 2
- Outputs with a controlled `cabinet_or_service` record: 1
- Outputs with a controlled `unused` record: 18
- Outputs with a controlled `virtual` record: 1

## Promotion decision

This record stays `partial`. Two unresolved conflicts block promotion outright: pinned PinMAME applies zero switch-matrix inversion for every Whitestar game (`conflict.whitestar-invsw-never-populated`), which leaves the manual's two identified opto switches (14, 15) without a settled polarity; and the manual documents a real, populated cabinet button (DS-5, public switch 88) that this driver's own `hw.flippers` declaration makes structurally unreachable (`conflict.upper-flipper-button-not-read`). Independently, lamps 73-80 have no spatial placement because the retained table does not model them as distinct playfield objects, and the driver's declared four-column auxiliary lamp capacity (public 81-112) is not identified by any available primary source. `coverage.dimensions.physical_wiring = "conflicted"` and `coverage.missing = ["polarity", "output_enumeration", "spatial_placement", "unresolved_conflicts"]` record all of this explicitly rather than promoting on the strength of the otherwise-complete 1-64/1-50/1-80 address space.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/extracted-vpxtool.manifest.json`, SHA-256 `9f21a0b4af3387d3b7b3dbd7480909d141c2cfeb00c6c9b59f417723918338bc`, 1348 files, 167511025 bytes.
- Human transcription of every printed table and diagram read from the rendered manual pages, SHA-256 `18a1d499a3525bd72340f0e5a98af98c3fb8b867f0f3b1b655242f5cc7ef37e8`.
