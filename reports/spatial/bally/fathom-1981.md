# Fathom (Bally, 1981) spatial review

Status: partial. The physical machine record stays `partial` at `machines/partial/bally/fathom-1981.json`: twenty-two auxiliary lamp addresses have no semantic identity, four lamp addresses have no asserted coordinate, and one printed-versus-table identity disagreement is unresolved. Every switch, every solenoid and all sixty main-board lamp addresses are otherwise complete.

The matching source is the retained known-working `Fathom (Bally 1981).vpx` at SHA-256 `131f29d16bb2d311450c5409981ad0ee7c4664a065f40fd1a4617fd1a09b01a7`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `b28721214317659c5469ae1612f7316acb293ae4fdc405f6df2791859c2429ac`. Exact playfield bounds are `left=0 top=0 right=952 bottom=1974`, so every canonical coordinate is x/952 and y/1974 rounded to at most six fractional places. The trough kicker lands at y 0.863, the outhole drain at 0.956, the flippers at 0.844 and the plunger at 0.978, which is the sanity check that the y divisor is right.

## Evidence decisions

- This is a Bally MPU AS-2518-35 machine and reuses `controllers/pinmame/by35.json` unchanged. The fifth argument of its `INITGAME2` line is the auxiliary lamp-column count, **not** a switch-column count: `core_tGameData.hw` is `{flippers, swCol, lampCol, custSol, ...}` and the macro passes `0` for `swCol`. Fathom declares `lampCol = 8`, like Bally Centaur and Bally Kiss.
- Fathom is a six-column switch machine: the printed self-test table numbers forty-eight positions and the playfield wiring diagram draws six strobes. The sixth strobe `ST 5` comes from `A4J4-8`, which is the PIA1:B PB7 line published as continuous solenoid **20**, not 17. Three sources agree: the playfield sheet's own connector, `by35.c`'s default `(locals.b1 & 0x80) >> 2` column path, and `lisy35.c`'s Fathom case, which sets `lisy35_J4PIN8_is_strobe` and masks that bit out of the coil data. The retained harness run shows address 20 asserted continuously from the moment the game comes up. Bally Centaur spends public 17 on its sixth strobe and Bally Kiss spends 17 on a real coil; neither precedent transfers.
- The printed `Self Test #` column is a test order. The ROM's own solenoid test, captured in the retained harness run, pulses the coils in printed order 01 through 21 and resolved the whole mapping at once, including the fact that printed 01 (Knocker) is public 6 and printed 13 (Outhole Kicker) is public 7 - the same outhole address Centaur and Kiss use.
- Nineteen printed momentary functions sit on fourteen driver outputs because the Solenoid Expander (A15, AS-2518-66) relay-gates five of them between two coils each. Public lamp 47 is the relay's control input, not a bulb; the harness run proves it by showing that address energized only around the six in-line drop-target pulses.
- Public momentary 5 and public continuous 17 are genuinely spare: the A3 sheet routes 17 only to pins printed N/U, and the self-test cycle never pulses either address.
- The AS-2518-23 public-address to connector-pin mapping is a board property. Bally Centaur and Bally Kiss record identical mappings for all sixty addresses including the eight branch outputs, Fathom's own A5 sheet reproduces it for U1's first twelve outputs by straight-line trace, and the eight `N/U` pins that carry an arrow on Fathom's sheet are exactly those eight branch destinations. Fathom's own printed pin functions then name every address. Independent checks that fell out of this: the blue bonus ladder 1K to 7K lands on addresses 2, 18, 34, 50, 3, 19, 35 whose retained light objects climb one column at constant x with monotonically decreasing y, the green ladder does the same one column right, `50K Right Return Lane` (1) and `50K Left Return Lane` (49) land beside switches 21 and 24, the three `Scan Rollover Button` auxiliary lamps land on the three rollover buttons of switch 20, and `Solenoid Expander Relay Drive` (47) matches the harness observation.
- The AS-2518-52 auxiliary board is **not** the AS-2518-43 that Centaur and Kiss carry: four decoders and twenty-eight SCRs against two and twelve. Its own U1 fourth flip-flop is not driven, so only three latched address bits reach it and each decoder uses outputs 0-6 with output 7 printed `N/U`.
- General illumination is not a controller output on this machine: the playfield sheet takes it from an unswitched 5.9 VAC transformer secondary, so no `pinmame.output.gi` device is declared.
- Flipper coils have no driver-board output. All three coils hang on the 43 VDC bus behind relay K1, whose coil is public solenoid 19; PinMAME's synthetic 46 and 48 are what the retained script binds.

## Explicit projections

- switch 1: Projected onto the retained Drain kicker object, the point at which a ball leaves the playfield into the outhole. The outhole switch itself sits inside the outhole under the apron and has no playfield-surface object; the retained script models the whole outhole and trough as one cvpmBallStack (bsTrough.Initsw 0,1,2,3) with no per-switch object.
- switch 2: Projected onto the retained BallRelease kicker object, the trough's own eject point. Trough position switches sit inside the ball trough behind the outhole, not on the playfield surface, and the retained script models them only as cvpmBallStack positions.
- switch 3: Projected onto the retained BallRelease kicker object; see switch 2. The printed name covers two ball positions on one matrix contact, which is why one address serves the 2nd-left and 1st-right trough stations.
- switch 18: Projected onto the retained Spinner object sw18: the spinner switch is part of the spinner assembly rather than a separate playfield sensor.
- switch 36: Projected onto the retained RightSlingShot wall, whose _Slingshot handler pulses this address.
- switch 37: Projected onto the retained LeftSlingShot wall, whose _Slingshot handler pulses this address.
- switch 38: Projected onto the retained Bumper2 object, whose _Hit handler pulses this address.
- switch 39: Projected onto the retained Bumper3 object, whose _Hit handler pulses this address.
- switch 40: Projected onto the retained Bumper1 object, whose _Hit handler pulses this address.
- solenoid 1: Projected onto the 1st Blue Inline Drop Target (retained object sw44), the target this address raises when the Solenoid Expander relay is de-energized, since the reset coil sits under the bank rather than on the playfield surface.
- solenoid 2: Projected onto the top target of the left six-bank (retained object sw32); the bank reset coil sits under the bank.
- solenoid 3: Projected onto the #3 Middle Drop Target (retained object sw33); the bank reset coil sits under the bank.
- solenoid 4: Projected onto the 1st Green Inline Drop Target (retained object sw48); the bank reset coil sits under the bank.
- solenoid 7: Projected onto the retained Drain kicker object, the outhole mouth. The outhole kicker sits inside the outhole under the apron.
- solenoid 8: Projected onto the retained Bumper1 object; the coil is inside the bumper body.
- solenoid 9: Projected onto the retained Bumper3 object; the coil is inside the bumper body.
- solenoid 10: Projected onto the retained Bumper2 object; the coil is inside the bumper body.
- solenoid 11: Projected onto the retained LeftSlingShot wall; the coil is behind the slingshot rubber.
- solenoid 12: Projected onto the retained RightSlingShot wall; the coil is behind the slingshot rubber.
- solenoid 13: Projected onto the retained sw4 kicker (Top Saucer). With the Solenoid Expander relay energized the same driver output drops the 1st Blue Inline Drop Target instead.
- solenoid 14: Projected onto the retained sw5 kicker (Right Saucer). With the Solenoid Expander relay energized the same driver output drops the 2nd Blue Inline Drop Target instead.
- solenoid 15: Projected onto the 3rd Blue Inline Drop Target (retained object sw42), the target this coil drops.
- lamp 12: Projected onto the retained Bumper2 object, the right thumper bumper the manual names for this circuit. The retained table binds its own address-12 light objects to the bottom bumper instead; see conflict.thumper-bumper-lamp-address-swap.
- lamp 28: Projected onto the retained Bumper3 object, the bottom thumper bumper the manual names for this circuit. The retained table binds its own address-28 light objects to the right bumper instead; see conflict.thumper-bumper-lamp-address-swap.
- lamp 44: Projected onto the retained Bumper1 object, the left thumper bumper. The retained table agrees on this one address.

## Excluded object classes

- Light L12, which normalizes to exactly the same coordinate as Light L1 and is a co-located leftover rather than a second bulb.
- Light L13, a stray object at (0.906, 0.653) for an address the printed wiring puts in the back box and which the retained script's own lamp routine leaves commented out.
- Trigger sw1, an unused object at (0.701, 0.005) with no handler anywhere in the retained script; the outhole switch is modelled by the ball stack instead.
- HitTarget sw42a, sw43a and sw44a, the rear meshes of the three blue in-line targets, which the retained script passes as second elements of the same drop-target array rather than as separate targets.
- Trigger sw20c1, a fourth rollover object with no handler; the printed name gives three rollover buttons and the script drives three.
- Light Light66g, Light81a and Light82g, which normalize to a negative x and are table modelling anomalies rather than bulbs.

## Counts

- Placements: 115
- Located input addresses: 38
- Located output bindings: 71
- Unresolved inputs (no spatial key): []
- Unresolved outputs (no spatial key): 25
- Inputs with a controlled `cabinet_or_service` record: 10
- Inputs with a controlled `dip_switch` record: 32
- Inputs with a controlled `unused` record: 3
- Outputs with a controlled `cabinet_or_service` record: 9
- Outputs with a controlled `internal_nonvisual` record: 2
- Outputs with a controlled `unused` record: 6

## Promotion decision

Promotion to `author_ready` is refused. `coverage.missing` is `["output_semantics", "spatial_placement", "unresolved_conflicts"]`, and each entry names a concrete gap:

- `output_semantics`: twenty-two AS-2518-52 auxiliary lamp addresses have no function on any retained source. Resolving them needs a Fathom insert-panel drawing that reaches the A9 J2/J3 pins, or a photograph of the A9 harness on real hardware.
- `spatial_placement`: lamp 43 and auxiliary lamps 66, 82 and 98 have no asserted coordinate, and the twenty-two unnamed auxiliary addresses have none either.
- `unresolved_conflicts`: `conflict.thumper-bumper-lamp-address-swap`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/fathom-1981/extracted-vpxtool.manifest.json`, SHA-256 `c6aceb38d454b8236155caa431268ba32ef59212eb3193de983577f307baaac4`, 1259 files, 87975187 bytes.
- Harness run `external:pinmame-review-artifacts/fathom-1981/harness-solenoid-self-test.json`, SHA-256 `0c5e23417255f4830587db93f767883ae28ac52b27456975758265b4dee84556`, and the boot run at SHA-256 `7eda9b26f6b87df76994055fef1ab93751726c38c3f9e515f2bdc7a98c793284`.
- Normalized geometry dump `external:pinmame-review-artifacts/fathom-1981/vpx-geometry.txt`, SHA-256 `c02d409b92e5ce34e3dc143bc6abd2351a90ac2bf1b0e62146037593cd91bd7d`.
- Rendered manual and schematic pages under `external:pinmame-manuals/rendered/bally.fathom.1981/`.
- Transcribed excerpts under `evidence/excerpts/bally.fathom.1981/`.
