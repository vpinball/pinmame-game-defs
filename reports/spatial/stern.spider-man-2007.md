# Spider-Man (Stern, 2007) spatial review

Status: validated and promoted to `machines/author-ready/stern/spider-man-2007.json`.

The matching source is `Spider-Man_3.0.vpx`, retained at `external:pinmame-vpx-sources/stern/spider-man-2007/source/Spider-Man_3.0.vpx` with SHA-256 `97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47`. Fresh `vpxtool git:v0.33.3` extraction produced the embedded Script stream at SHA-256 `ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128`; that paired embedded stream is the causality authority. The adjacent sidecar `external:pinmame-vpx-sources/stern/spider-man-2007/source/Spider-Man_3.0.vbs` remains secondary/corroborating only at SHA-256 `cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237`. `vpxtool` established exact playfield bounds `0..952` by `0..2115`; every canonical coordinate is rounded to at most six fractional places.

## Evidence decisions

- The embedded Script stream from the exact retained table is the runtime address and causality authority. The Stern service manual is the physical inventory, multiplicity, and physical-wiring authority. The exact matching table is the geometry authority.
- Manual page 6 identifies D15/public switch 86 as the upper-right flipper button and D16/public switch 85 as its normally-closed EOS. The embedded script asserts switch 86 from the right-flipper key and maps Q14 to `solURFlipper`/`RightFlipper2`; it does not assert switch 85, so the EOS identity and polarity remain manual-only physical truth.
- The sidecar differs materially: it declares `NoUpperRightFlipper` and `NoUpperLeftFlipper` and uses `Const UseSolenoids = 2`, while the embedded stream has neither declaration and uses `Const UseSolenoids = 1`. The sidecar also contains cvpmSaucer exit-variance settings and later audio/rolling-helper changes absent from the embedded stream; no canonical causal assertion uses it.
- Direct VPX centers cover visible sensors/effects/emitters. `LA*`, `LB*`, `Illumina*`, `Fotocellula*`, `l*r`, and other synchronized lightmap/render helpers are excluded from physical multiplicity.
- Q23, Q25, Q28, and Q31 retain physical quantities 2, 2, 2, and 3 from manual page 11. Q28 has two distinct manual-callout projections; Q29/Q30 are manual back-panel flashers projected to y=0. GI retains 42 placements and physical quantity 44 for the explicitly US/non-Euro scope; Euro hardware has three coin-door bulbs.
- Lamps 66-71 use `bulbPr3`-`bulbPr8`, whose table y coordinate is -12 for rear-panel rendering; they are explicitly projected to y=0. The manual page-9 lamp map identifies the same six back-panel lamps.
- Trough switches 18-22 are explicit assembly projections, not invented VPX sockets. The table's `cvpmTrough.InitSwitches Array(21, 20, 19, 18)` establishes the ball order; manual assembly 500-6318-24-ND establishes the four-ball switches and separate SW22 jam opto.
- Motor limit switches and the associated motor effects share exact table assembly anchors: `Primitive.Bank`, `Primitive.Sandman`, and `Primitive.Octopus`. Green Goblin Q19/Q28 use the exact `Primitive.Goblin` anchor; the broad table flasher overlay is not an extra physical socket.
- The 128×32 DMD is cabinet/backbox hardware, so its spatial record is controlled `not_applicable` with both PinMAME core and physical-manual provenance; no playfield display coordinate is asserted.

The visual review cache was restored under `external:pinmame-review-artifacts/stern/spider-man-2007/manual-pages/` with 23 rendered PNGs for manual pages 6, 8-11, 37, 68-69, 85, 91-100, and 118-121. Their filenames and SHA-256 hashes are recorded in the companion JSON report, so an empty cache is an audit failure rather than an assumed source. The complete behavior and startup reconstruction remains in the linked knowledge note.

Promotion is reproducible after the partial path is removed: tracked seed `tools/seeds/stern/spider-man-2007.json` is SHA-256 `f7a34de84cac7e19d852c54f2d83939f995902578cd6ae64b01ed1aff1c06f6c`, byte-identical to the promoted definition. The focused test exercises this real post-commit path and regenerates the same bytes twice.
