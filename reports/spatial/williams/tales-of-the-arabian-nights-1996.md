# Tales of the Arabian Nights (Williams, 1996) spatial review

Status: partial. Every switch, solenoid, and lamp address that the retained table can support is located and validated, but the three dimmable playfield G.I. strings have no per-string socket evidence, so the physical machine record stays `partial` at `machines/partial/williams/tales-of-the-arabian-nights-1996.json`.

The matching source is the retained known-working `Tales of the Arabian Nights (Williams 1996).vpx` at SHA-256 `487375925e6f44998cd416b6d28983f08144d2bfe7a1432ac9ad16af7b23fec0`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `c4a742f2188c9e3dcba70a7717d5b8985bbd1d913cc05c17df3b2f9d341b876b`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2164`, and every canonical coordinate is x/952 and y/2164 (not 2162) rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries a genuine OCR text layer, but `pdftotext -layout` badly garbles the multi-column switch/solenoid/lamp tables. Every printed table used here was re-verified visually against the 300 dpi rendered pages and transcribed into `external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/manual-transcription.md`.
- Two switches (31, 42) and two mechanism-driven switches (56, 57) have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's continuous position (trough ball-release event, Genie figure rock angle, Spinning Lamp Unit disc rotation) rather than from a discrete Hit event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- G.I. classification: printed page 2-40 enters the G.I. rows' connectors under the wrong location columns (strings 1-3 `J106` under Backbox, strings 4-5 `J105` under Playfield) while the same rows print the #44 bulb under Playfield and the #555 bulb under Backbox. The manual's own Power Driver Board A-20028 connector list (printed 3-26) names `J106-1..3`/`J106-7..9` "G.I. to playfield" and `J105-5/6`/`J105-10/11` "G.I. to insert panel", so GI addresses 0-2 are the dimmable playfield strings and GI addresses 3-4 the always-on backbox insert-panel strings (address 4 also feeding the coin door through `J104`). GI 3-4 carry controlled `cabinet_or_service` records. The former conflict over GI address 2 is withdrawn: the retained script's playfield dimming on that address agrees with the machine.
- This retained table is smaller and older than the VPW mods used for several other curated WPC games (944 files, no VPW authorship). It renders all playfield G.I. from address 2 through lit/unlit texture swaps and 18 ambience lights (no bulb mesh, falloff radii of 100-200 units), not per-socket bulb objects, so the script's single binding proves no bulb's string (in the one recorded attract-mode harness run the ROM moved GI 0-2 together, which is why a single stand-in looks right there; gameplay lighting was not traced). GI addresses 0-2 are left spatially unresolved rather than assigned by proximity.
- Solenoids 16 and 17 (Left Eject Flasher, Inlane Flashers) print two playfield bulbs each, but the retained table models only one Light object per address; one placement is recorded and the quantity gap is disclosed in `physical.notes` rather than fabricating a second coordinate.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 31: Projected onto the trough Ball 1 kicker position (sw32): the retained script's ball-release handler (SolRelease) kicks the ball resting on switch 32 and pulses trough-eject opto 31 in the same event (vpmTimer.PulseSw 31), and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.
- Switch 42: Projected onto the Genie figure (Primitive GenieP, table object center): public switch 42 (Genie Target) is set from UpdateGenie's rocking-angle threshold (GenieAngle > 4.5) on the figure itself, not from a discrete trigger-hit event on either physical target blade.
- Switch 56: Projected onto the Spinning Lamp Unit disc center (Primitive LampPr/LampPr1/LampPr3, table object center at raw (510, 840)): SpinnerBallTimer_Timer pulses public switch 56 (Lamp Spin CCW) whenever the disc's simulated rotation crosses a position threshold while spinning counter-clockwise; there is no fixed sensor object.
- Switch 57: Projected onto the Spinning Lamp Unit disc center; see switch 56. SpinnerBallTimer_Timer pulses public switch 57 (Lamp Spin CW) at the same thresholds while the disc spins clockwise.

## Unresolved (no fabricated placement)

- pinmame.output.gi address 0: dimmable playfield G.I. string with no per-string socket list in any retained source; the retained table renders all playfield G.I. from address 2 without per-socket bulb objects
- pinmame.output.gi address 1: dimmable playfield G.I. string with no per-string socket list in any retained source; the retained table renders all playfield G.I. from address 2 without per-socket bulb objects
- pinmame.output.gi address 2: dimmable playfield G.I. string with no per-string socket list in any retained source; the retained table renders all playfield G.I. from address 2 without per-socket bulb objects

## Counts

- Placements: 146
- Located input addresses: 42
- Located output bindings: 98
- Unresolved output bindings: 3
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 20
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `virtual` record: 28

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for switches, solenoids, lamps, or the flipper pair, and the definition carries no conflicts. The three dimmable playfield G.I. strings (GI addresses 0-2) have no socket-level evidence, so `coverage.dimensions.spatial_placement = "unknown"` and the record stays `partial` with `coverage.missing = ["spatial_placement"]` until a per-string socket list (a G.I. wiring drawing, a playfield-harness survey, or a table that dispatches separate bulb collections per string) is retained.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/extracted-vpxtool.manifest.json`, SHA-256 `761846f3369203502a9083c19e46a0da046893a46df43abc734a53c61b19a04d`, 944 files, 128702095 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `fd33e241ed3715c93213ced0f051df1a72a1d042eb9dda0536273eb3b84ac176`.
- Attract-mode G.I. harness run `external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/harness/run3-scenario-attract.json`, SHA-256 `fea7675de0c9f542bbf3841a1bc4728bb1e13bcbcb98908dfc65ecf7186bf572`, from scenario `tools/harness-scenarios/wpc-95/totan-attract-gi-observe.json` (SHA-256 `a83c1e82f1cb7f329a27b07d7bdbd52e763e6fed5e98100507c191d4f939d4db`), with the run directory pinned by `external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/harness/run3-scenario.manifest.json` (SHA-256 `2e23f59ffaad461b238947971d76a3c10a9b331ada92b12d851c1e30ac2d80e9`); totan_14.zip SHA-256 `3ec0c9147f0a91cab94aa40ca931dfed3fa7e999f450daac0b2c43bbd092dab6`, pinmame64.dll SHA-256 `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c`. GI 3-4 held at level 8 throughout; in this attract-mode run GI 0-2 moved together between levels 0 and 3-8.
