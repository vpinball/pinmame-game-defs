# The Lord of the Rings (Stern, 2003)

Coverage: **partial - manual-verified semantic I/O, mechanism inventory and behaviour, the complete public output inventory including board 520-5242-00 at lamps 81-99, and normalized placements; held below author-ready because switch 15's public opto polarity is unestablished, spatial evidence is not fully corroborated, five LED-board addresses have conflicting positions, fifteen printed devices remain unplaced, and the 2008 Limited Edition's physical compatibility is not yet sourced**

## Identity and evidence precedence

Whitestar machine. PinMAME roots the family at `lotr` with 46 drivers: English revisions, the 10.02 Limited Edition re-run, and Spanish, German, French and Italian releases. Every clone shares `init_lotr` and therefore the same emulator routing through `lotrGameData`. That does **not** prove identical physical hardware: `lotr_le` is a 2008 Limited Edition re-run whose physical compatibility remains unknown. ROM differences are read out of pinned `segames.c` per driver rather than summarized from names. There are four software shapes:

- **A German, French or Italian release runs its English sibling's CPU game ROM byte for byte** and differs only in the display ROM. `lotr`, `lotr_fr`, `lotr_gr` and `lotr_it` all take `lotrcpua.a00`; only `lotrdsp{a,f,g,i}.a00` differ. The same holds at every revision.
- **An English revision differs in CPU and display both** - `lotr9` is `lotrcpu.900` with `lotrdspa.900` against the root's `lotrcpua.a00` and `lotrdspa.a00`.
- **A Spanish release differs in all three.** It has its own CPU family `lotrcpul.*`, its own display `lotrdspl.*`, and the only other sound set in the tree: `LOTR_SND_SP`, five ROMs, against `LOTR_SND` for the other 38 drivers.
- **The Limited Edition differs in CPU alone** - `lotrcpua.a02`, sharing the root's display and sound.

Physical inventory authority is the **Stern English service manual**, IPDB machine 4858, an image-only 184-page scan with no text layer, so every printed table was read from pages rendered at 300 dpi. Runtime authority is the retained known-working script set; four recreations were retained and all run `cGameName = "lotr"`.

## The 520-5242-00 LED board: nineteen separately addressable emitters

`lotrGameData` declares two board identifiers. The second, `SE_BOARDID_520_5242_00`, is named in `src/wpc/se.h` in plain words: **"Lord of The Rings 19 LED Board"**. `se.c` drives it through `core_set_pwm_output_led_vfd(CORE_MODOUT_LAMP0 + 80, 3 * 8, CORE_MODOUT_LED, 4.f / 2.f)` and writes at `CORE_MODOUT_LAMP0 + 80`, `+ 88` and `+ 96` masked `0x07` - public lamp addresses **81 to 99**, nineteen LEDs. So `lampCol = 5` is not slack: it is 64 base lamps, the two auxiliary matrix columns at 65-80, and room for that board.

All four retained known-working scripts drive them. The controller profile exposes them after the 1-80 matrix through the same PinMAME lamp transport. All nineteen are enumerated as emitters 01-19 at public addresses 81-99; allocation slots 100-104 are not physical devices. Their normalized positions are compared through each script's explicit address-to-object binding rather than by assuming an `l<N>` object's suffix is its public address: that distinction matters because Hanibal reverses and permutes the object numbers. The Neo table's own info and script disclose its JPSalas lineage, so it is a supplemental measurement rather than independent corroboration. Fourteen addresses have an observed coordinate supported by a retained-table cluster; addresses 86, 87, 88, 89, 94 have none because no two script-bound measurements agree inside the threshold. No factory per-emitter semantic name or connector pin is invented, and the manual is not cited for evidence it does not contain.

## Addresses that are synthetic, mirrored or reserved

- Public 45 and 47 are the power-phase view of the same physical coils exposed at 46 and 48. Binding both halves creates two flippers where the machine has one.
- Public 15 is PinMAME's synthetic fast-flip and game-on state; 16 is its unused companion.
- Whitestar auxiliary board 520-5068-01 exposes three outputs, so 33, 34 and 35 carry the UK-only up/down posts and 36 is unused.
- General illumination is a **single aggregate channel 0**, although the cabinet has four separately fused 6.3v strings. A recreation must not infer four controllable channels from the fuse chart.

## Opto polarity: PinMAME normalizes nothing here

The controller profile declares `inversion_applied_by_emulator: true` as a platform capability, and for this driver pinned PinMAME exercises none of it. `lotrGameData` (`segames.c:1498`) is a positional aggregate that sets only `GEN_WS`, the display layout and the `hw` struct; the trailing `wpc` member - which is where `invSw` lives - is left at C zero-initialization, and `core.c:2455` memcpy's those zeros into the live `coreGlobals.invSw`. **The four printed optos are therefore published exactly as a recreation asserts them, and the ROM's own firmware accounts for the beam resting made.** An earlier pass of this definition said "PinMAME normalizes the public state", which arrived at the right instruction for a recreation by way of a mechanism that does not exist.

Three of the four are settled by observation rather than by argument. The retained known-working VPW 1.6 script asserts switches 14, 41, 47 when a ball is present, through direct assert/release pairs whose sense is unambiguous - and it is known-working on the ball trough, which is exactly where a reversed opto fails first. Switch 15 is the exception: no retained recreation binds it at all (the VPW table does its stacking bookkeeping without a `Controller.Switch(15)` call, and neither alt table binds 14 or 15), so the public sense the ROM expects there is genuinely unestablished and is carried as `conflict.whitestar-invsw-never-populated` rather than guessed from its sibling.

`normally_closed: true` on these four records describes the physical contact, not the public state. Do not read it as a polarity instruction.

## Custom mechanisms

- **Four-ball trough and up-kicker.** Four balls rest in the under-playfield trough on printed switches 11, 12 and 13 with the fourth position read by opto 14, the 4-Ball Trough VUK Opto at the eject end. Solenoid 1, the Trough Up-Kicker, lifts the ball at the eject end into the shooter lane, where switch 16 reads it. Printed switch 15, the 4-Ball Stacking Opto, watches the stack feeding the trough. The manual numbers the positions from the left, so printed Trough #1 is the position furthest from the shooter lane; the retained VPW script numbers its trough objects in the opposite order, which is a labelling difference and not a wiring disagreement. All three retained scripts initialise switches 11-14 closed at start of game because balls rest on them.
- **Balrog motorized toy.** The Balrog toy is driven by motor 041-5088-01 on printed solenoid 22, gated by the DC relay 520-5066-00 on printed solenoid 20. Printed switches 31 Balrog Open and 32 Balrog Closed read the two end positions and are mutually exclusive; the retained VPW script asserts one and clears the other as the motor runs. Printed switch 28 Balrog Hit is a separate above-playfield switch on the toy that registers a ball strike and is driven in the retained script from a wobble value rather than from the motor position, so a recreation must not derive it from the open or closed state.
- **Sword ball lock.** Three above-playfield switches read balls held in the sword lock: printed 17 Sword Lock High, 18 Sword Lock Mid and 19 Sword Lock Low, all switch part 180-5119-02. Printed solenoid 21, the Sword Lock Release, frees the stack. The high position is the one furthest from the release coil.
- **One Ring magnet and back panel.** The One Ring on the back panel is held and released by the magnet on printed solenoid 6, which is the only output with its own fuse, printed F20 4A 250v slow-blow and marked THIS GAME ONLY in the quick reference fuse chart. Printed opto 47 Ring Made, on the back panel, reads a ball completing the ring. Printed solenoid 26 flashes the ring and 27 the back panel behind it.
- **Loop diverter gate.** Printed solenoid 8, the Loop Diverter, steers a ball out of the loop toward the left Orthanc tower. The manual carries a dedicated Diverter Gate Adjustment Procedure: with power off and the playfield raised, the crank-bar set screw is loosened, the paddle is held against the right flat rail to open the gate to the left tower, the plunger is pushed home, and the screw is retightened so the paddle rests as close to the left flat rail as possible without touching it. Printed switch 42 Inner Loop and the orbit switches 20, 21, 37 and 38 read balls through the loop.
- **Vertical up-kickers and top saucer.** Three vertical up-kickers and one saucer return balls to play. Printed solenoid 3 with switch 9 is the left VUK, printed solenoid 4 with opto 41 is the top VUK, printed solenoid 5 with switch 30 is the right VUK, and printed solenoid 19 with switch 46 is the top saucer. The retained VPW and JPSalas scripts label solenoid 4 Upper-Left VUK and solenoid 19 Upper-Right Kicker; the manual's Top VUK and Top Saucer are the printed names and control.
- **Mini playfield.** A separate mini playfield carries four switches printed Mini PF U.L., U.R., L.L. and L.R. at addresses 33 to 36, all switch part 180-5057-00. The printed switch-location drawing shows the mini playfield moved off the main playfield for clarity, so its printed drawing position is not its installed position; the coordinates here come from the retained recreations.
- **UK-only up/down posts.** UK cabinets add three up and down posts driven from a UK 3X Transformer Driver Board and exposed on Whitestar auxiliary outputs 33, 34 and 35. The printed coil and flash lamp location drawing places Aux 1 at the left inlane area, Aux 2 between the flippers and Aux 3 at the right. These are absent from non-UK cabinets, as are the two cabinet-side buttons at printed switches 1 and 8.

## How coordinates were resolved

Four recreations were retained. Three factory-layout tables are treated as three measurements: a lamp, switch or flasher placement is `validated` only when **all three agree** within 0.025 normalized units. The fourth Neo LED recreation is a disclosed JPSalas derivative and contributes only a supplemental measurement for addresses 81-99. Every one of those addresses is resolved through each table script's own binding; fourteen positions remain `observed` and five remain unpublished conflicts. Overall, 63 device spatial records are observed against 97 validated, with 162 physical placements in total because one output can drive multiple emitters.

That threshold is deliberately conservative because **independence between the three is unestablished and the two available signals disagree**. Measured, the JPSalas and Hanibal tables agree with each other to within 0.0155 on every lamp both model while either differs from VPW by up to 0.187. Documented, VPW credits an "EBIsLit - Baseline playfield scan" and JPSalas records its playfield as "based on Ebislit's playfield", while Hanibal declares only "4k Mod" in its title and names no baseline. The measured clustering pairs JPSalas with Hanibal; the documented ancestry pairs VPW with JPSalas. No lineage model is asserted.

The VPW table identifies itself as **"Lord Of The Rings - Valinor Edition"** with original artwork, so where its insert layout departs from the printed diagrams that is an artwork difference rather than an error. Its Fellowship inserts form a closed ring of runes rather than the printed arc of named characters, which accounts for 14 of the 35 rejected measurements - lamps 6, 9-17, 96-99, where VPW alone is the outlier. Across all 35 rows the rejected measurement is VPW's 30 times, Hanibal's 9 times, JPSalas's 7 times and Neo's 2 times. Neo participates only for addresses 81-99 and its disclosed JPSalas lineage means its agreement is supplemental, not an independent vote.

Public flasher 25 is not a single-point device. All three retained factory-layout scripts bind all three physical bulbs, and the resolver groups their co-located rendering objects into left, right and bottom emitter measurements before consensus. Every emitter is independently `validated` by all three tables; none is a projection or a rejected alternate measurement.

**13 placements across 13 device records are projections**, not measurements: each takes the coordinate of a co-located device the printed DR.7 diagram places beside it. Be precise about why. The resolver searches the three tables for `l<N>`, `sw<N>` and configured flasher objects only, so no coil search was ever run and this is not a finding that the tables model no coils - it is that the resolver has no coil group and the projection therefore stands on the printed diagram alone. Every one is `observed` and listed with its anchor in the spatial report. **3 coordinates are computed** rather than held by any table - per-axis medians of tables that disagreed - and each is marked `coordinate_origin: computed` with the tables it was derived from.

## Notable printed details

- Optos, which rest closed, are switches 14, 15, 41, 47.
- Printed NOT USED: matrix switches 26, 27, 63, 64; dedicated switch DS-5; solenoids 12, 28.
- The ring magnet on coil 6 is the only output with its own fuse, printed F20 and marked THIS GAME ONLY.
- The lamp matrix axes are transposed between the manual and PinMAME: PinMAME's lamp column strobe corresponds to the printed **row** and its lamp row to the printed **column**. Do not map them by name.

## Preserved source anomalies

- Lamps 15 and 33 are printed LEGOLES, not LEGOLAS. The spelling is consistent across both cells at 300 dpi, so it is the manual's own error rather than a scan artifact. Transcribed as printed; do not silently normalize.
- The known-working VPW script names coil 4 SolULVUK and coil 19 SolURKicker, where the manual prints TOP VUK and TOP SAUCER. Same addresses and same devices; the disagreement is label-only and the manual controls physical naming.

## Recreation guidance

Bind the flippers once, at 46 and 48. Enumerate the dedicated switches at their negative and 81-84 addresses rather than folding them into the matrix. Treat GI as one channel. Model the trough with the printed numbering, remembering that printed Trough #1 is furthest from the shooter lane. Drive Balrog Hit from a collision, not from the toy's position. The 8x10 matrix occupies 1-80 and the nineteen-emitter board occupies 81-99 on the same lamp transport; do not invent anything at 100-104, which is allocation space rather than physical hardware.
