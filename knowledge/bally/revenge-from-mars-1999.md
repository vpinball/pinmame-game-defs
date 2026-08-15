# Revenge from Mars (Bally, 1999)

Coverage: **partial - complete public address inventory, switch polarity, stock wiring, documented firmware milestones, observed stock/aftermarket spatial placement, and a retained trough/auto-plunger trace, with mechanism dynamics and exact per-driver option/flash pairings still incomplete**

## Identity and Pinball 2000 architecture

This is Bally model 50070, *Revenge from Mars*, the first Pinball 2000 title. A MediaGX PC renders a 640x240 game framebuffer onto a monitor in the head; the cabinet optics reflect that image onto a partly transparent playfield surface. PinMAME exports one 640x480 video display because each native row is doubled in the current layout. VPE should consume that exported video surface as the overlay texture, preserve its 2:1 logical pixel shape, and place the rendered plane through table-specific scene geometry rather than treating it as a DMD.

The power-driver board still exposes conventional playfield switches, coils, flashers, and lamps. PinMAME publishes those through the normal switch, solenoid, and lamp groups while the video frame is a separate display output. No general-illumination group is currently exported by the P2K driver, so this definition does not invent one.

## Public controller numbering

Playfield switches use public column/row addresses `11-88`. Printed direct inputs `D1-D8`, `D9-D16`, and `D17-D24` are exposed at `91-98`, `101-108`, and `111-118`. The factory manual's shaded trough, popper, jet-exit, lockup, and ramp-entry optos physically rest closed; the later optional expansion positions 53-56 use the same opto convention. PinMAME publishes every per-game P2K opto at its raw active-low level (`0` active/beam blocked, `1` inactive), not at a normalized active-high level. Every other fitted contact is recorded normally open: the manual requires an open gap for playfield blade contacts and explicitly calls both EOS switches normally open, while PinMAME's P2K input map uses inactive `0` / active `1` for the remaining grounded controls. The controller's `inversion_applied_by_emulator` flag still means consumers use the mixed public levels as delivered and do not apply one controller-wide inversion.

Board drivers 1-32 retain public solenoid numbers 1-32. Board drivers 33-36 are exported through PinMAME's lower-flipper public addresses 45-48. Board drivers 37-48 become custom public outputs 51-62. Do not remap the printed driver numbers directly for 33-48; the JSON preserves both values as separate aliases.

The lamp board is not two contiguous 8x8 matrices. It is eight columns of sixteen bits, interleaving Bank A and Bank B per column. Convert printed notation with `public = (column - 1) * 16 + (Bank B ? 8 : 0) + (row - 1)`. The public range is zero-based `0-127` and the definition includes every cell, including all twelve printed unused positions.

## Stock spatial map

The factory location drawings on printed pages 2-38, 2-40, 2-42, and 2-44 locate every fitted stock playfield lamp, switch, solenoid effect, and flasher. Their player-view callout endpoints and directly labelled device centers are manually projected into the repository's normalized playfield plane (`x=0` left, `x=1` right, `y=0` rear, `y=1` apron). The retained excerpt records each crop's native pixel dimensions and approximate outer-table review bounds, but the drawings are orthographic service line art rather than surveyed CAD; all projected coordinates therefore remain `observed` and stop at three decimal places. Cabinet buttons, coin-door illumination, service hardware, unused outputs, and virtual outputs remain spatially not applicable.

The switch drawing has no devices at optional addresses 53-56 because the stock model 50070 is a four-ball machine. The myPinballs v2.0 installation guide documents the retrofit: Trough Ball 5 and 6 populate the two blank positions on the factory trough opto PCBs, while Right Lockup 2 and 3 populate mounting positions retained on the production lock weldment after those sensors were removed for cost. The trough points continue the factory Ball 1-4 spacing; the two lock points project consecutive ball positions within the existing Right Lockup 1 assembly. These four placements are `observed`, with explicit non-surveyed notes, rather than being presented as factory-manual coordinates.

## Stock devices and optional hardware

The February 1999 manual validates the stock four-ball trough, single drop target, right popper, auto plunger, right lockup, jet-exit post, lock diverter, up/down ramp, two Martian toys, gates, slings, jets, flashers, and flippers. It provides the connector, wire, transistor, and part data encoded in the definition. The retained release-DLL scenario supplies the four active-low trough positions and shooter-lane switch 18 as host stimuli; it legitimately observes driver 9 after Start, driver 15 after Launch, and the RGB24 video callback, but its switch readbacks are not ROM evidence. A separately built `PINMAME_P2K_DEBUG=ON` DLL repeats the path with PinMAME's deterministic ball model owning the switches: full trough, one position opened after eject, switch 18 active, switch 18 cleared after driver 15, and all four trough positions active again after the modeled drain. The debug delays are test scaffolding, not physical timing measurements.

Together those traces observe the trough and auto-plunger's controller-facing state sequence without promoting host input readback to ROM evidence. They do not independently validate the physical mechanism model, coil force, launch vectors, or the remaining moving assemblies. The trough, auto plunger, right popper, drop target, jet-exit post, lock diverter, up/down ramp, and right-lock eject therefore remain observed until a faithful recreation or instrumented physical machine supplies their startup positions, transitions, and ball routes.

Factory RFM leaves drivers 18 and 19 unpopulated. Community firmware 2.10 and later can drive an aftermarket knocker on 18 and shaker motor on 19. Driver 48 is a game-table ticket-dispenser option and is not normally fitted to a pinball cabinet. The official myPinballs update log says 2.22 begins recognizing six balls when the optional trough hardware is fitted and 2.50 can use those extra balls during Capture Multiball. Version 2.60 and later requires the complete four-opto expansion to operate correctly: 53-54 are trough balls 5-6 and 55-56 are right-lock positions 2-3 for a physical three-ball lock. Consequently `rfm_260` is marked physically different rather than stock-compatible.

The exact Prism boot-ROM revision paired with every later community update has not been independently authenticated. PinMAME records and boots its declared Prism, update-flash, and sound-flash combinations, but that proves emulator compatibility rather than which combination shipped with each community release. The official update log also does not authenticate the ticket option per driver. Preserve the catalog variants and their sourced hardware milestones without swapping flash components or collapsing the 2.60 expansion contract into the stock configuration.

## Display and rendering contract

PinMAME's P2K video source is 640x240. The exported CORE_VIDEO layout is 640x480 with rows doubled so legacy display sizing does not halve the output. The frame is already turned into readable row order by the driver; VPE must not mirror or vertically flip it again. A CRT-style filter may reconstruct scanline and shadow-mask character at the logical 640x240 resolution, but geometry, keystone, reflection plane, and cabinet occlusion belong to the authored Unity scene.

## Evidence precedence and known discrepancy

PinMAME's current `p2k_names.h` tables were walked completely against the games' own switch, coil, and lamp tests. Those measured runtime names and public addresses take precedence over visual inference. The manual remains physical truth for connectors, wires, driver transistors, parts, and stock-vs-unused fitment.

The operations manual's table and location drawing place 18B on the left slingshot and 28B on the right, while the machine lamp test reports the opposite semantic names. The definition therefore binds public 15/manual 18B to the runtime name Right Slingshot Spotlight at the manual's left-side coordinate and public 31/manual 28B to the runtime name Left Slingshot Spotlight at the manual's right-side coordinate. This deterministic split keeps machine-test semantics and factory physical positions without inventing a wiring swap, and the ignored conflict records why the names and sides appear crossed.

The supplied `Attack and Revenge from Mars (Midway-Williams) v600.vpx` is not RFM geometry. Its embedded script runs `afm_113b`, its callbacks are Attack from Mars addresses, and its extracted screenshot shows the AFM playfield. It is retained at SHA-256 `9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be` as a rejected candidate and contributes no RFM spatial or controller assertion.

## Remaining author-ready work

- Retain faithful traces for the right popper, drop target, jet-exit post, lock diverter, up/down ramp, and right-lock eject, including startup position, transition behavior, and physical ball route. The ROM-only harness can identify requested outputs but cannot measure physical force or vectors.
- Authenticate the ticket option and exact Prism/update-flash/sound-flash combination for each later community driver; PinMAME's runnable set composition is not release provenance.

## Sources

- `manual.rfm.operations-1999`: February 1999 model 50070 operations manual, SHA-256 `6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df`; four stock location drawings, service tables, and assemblies.
- `manual.rfm.mypinballs-opto-expansion-v2`: myPinballs Opto Expansion Upgrade Install Instructions v2.0, SHA-256 `00a744e1cc6507c328b22f33fc4f3aa6f8ec4826dce0a8874493023ee8d48fbf`; retrofit wiring tables and installed trough/lock photographs.
- `service-bulletin.rfm.mypinballs-code-updates`: official myPinballs code-update log acquired 2026-08-15; quoted knocker, shaker, six-ball trough, and physical-lock firmware milestones.
- `pinmame.core.8371478a7640`: pinned P2K implementation and machine-test-verified device tables at revision `8371478a7640f1896dcdf565aed340dc5df989ba`.
- `runtime.rfm.stock-ball-serve`: pinned release-DLL stock serve/launch scenario and 640x480 video trace.
- `runtime.rfm.debug-ball-cycle`: isolated P2K debug-model trace covering eject, shooter lane, launch, drain, and trough return.
- `vpx-table.attack-and-revenge-v600-rejected`: exact user-supplied hybrid VPX, rejected because it runs AFM ROM semantics and AFM geometry.
