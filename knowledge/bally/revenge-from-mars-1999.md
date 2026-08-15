# Revenge from Mars (Bally, 1999)

Coverage: **partial - complete public address inventory, stock wiring, observed stock spatial placement, and observed aftermarket opto placement, with mechanism dynamics, non-opto polarity, and firmware-option fitment still incomplete**

## Identity and Pinball 2000 architecture

This is Bally model 50070, *Revenge from Mars*, the first Pinball 2000 title. A MediaGX PC renders a 640x240 game framebuffer onto a monitor in the head; the cabinet optics reflect that image onto a partly transparent playfield surface. PinMAME exports one 640x480 video display because each native row is doubled in the current layout. VPE should consume that exported video surface as the overlay texture, preserve its 2:1 logical pixel shape, and place the rendered plane through table-specific scene geometry rather than treating it as a DMD.

The power-driver board still exposes conventional playfield switches, coils, flashers, and lamps. PinMAME publishes those through the normal switch, solenoid, and lamp groups while the video frame is a separate display output. No general-illumination group is currently exported by the P2K driver, so this definition does not invent one.

## Public controller numbering

Playfield switches use public column/row addresses `11-88`. Printed direct inputs `D1-D8`, `D9-D16`, and `D17-D24` are exposed at `91-98`, `101-108`, and `111-118`. The factory manual's shaded trough, popper, jet-exit, lockup, and ramp-entry optos physically rest closed; PinMAME normalizes them before exposing switch state. The later optional expansion positions 53-56 are also optos.

Board drivers 1-32 retain public solenoid numbers 1-32. Board drivers 33-36 are exported through PinMAME's lower-flipper public addresses 45-48. Board drivers 37-48 become custom public outputs 51-62. Do not remap the printed driver numbers directly for 33-48; the JSON preserves both values as separate aliases.

The lamp board is not two contiguous 8x8 matrices. It is eight columns of sixteen bits, interleaving Bank A and Bank B per column. Convert printed notation with `public = (column - 1) * 16 + (Bank B ? 8 : 0) + (row - 1)`. The public range is zero-based `0-127` and the definition includes every cell, including all twelve printed unused positions.

## Stock spatial map

The factory location drawings on printed pages 2-38, 2-40, 2-42, and 2-44 locate every fitted stock playfield lamp, switch, solenoid effect, and flasher. Their player-view callout endpoints and directly labelled device centers are manually projected into the repository's normalized playfield plane (`x=0` left, `x=1` right, `y=0` rear, `y=1` apron). The retained excerpt records each crop's native pixel dimensions and approximate outer-table review bounds, but the drawings are orthographic service line art rather than surveyed CAD; all projected coordinates therefore remain `observed` and stop at three decimal places. Cabinet buttons, coin-door illumination, service hardware, unused outputs, and virtual outputs remain spatially not applicable.

The switch drawing has no devices at optional addresses 53-56 because the stock model 50070 is a four-ball machine. The myPinballs v2.0 installation guide documents the retrofit: Trough Ball 5 and 6 populate the two blank positions on the factory trough opto PCBs, while Right Lockup 2 and 3 populate mounting positions retained on the production lock weldment after those sensors were removed for cost. The trough points continue the factory Ball 1-4 spacing; the two lock points project consecutive ball positions within the existing Right Lockup 1 assembly. These four placements are `observed`, with explicit non-surveyed notes, rather than being presented as factory-manual coordinates.

## Stock devices and optional hardware

The February 1999 manual validates the stock four-ball trough, single drop target, right popper, auto plunger, right lockup, jet-exit post, lock diverter, up/down ramp, two Martian toys, gates, slings, jets, flashers, and flippers. It provides the connector, wire, transistor, and part data encoded in the definition. The manual establishes inventory and wiring but not enough dynamic detail to claim complete ball routing, actuator timing, startup positions, or launch vectors; those mechanism records remain observed.

Factory RFM leaves drivers 18 and 19 unpopulated. Community firmware 2.10 and later can drive an aftermarket knocker on 18 and shaker motor on 19. Driver 48 is a game-table ticket-dispenser option and is not normally fitted to a pinball cabinet. Firmware 2.22 and later can support a six-ball trough through an opto expansion; 2.60 uses optional switches 53-56 and requires the expansion for its six-ball mode. An author must select the intended firmware and physical option set explicitly.

The exact Prism boot-ROM revision paired with every later community update has not been independently authenticated. PinMAME boots its currently declared set combinations, but that is not proof that each pairing shipped together. Preserve the catalog variants and their notes; do not silently collapse all revisions into a single hardware claim.

## Display and rendering contract

PinMAME's P2K video source is 640x240. The exported CORE_VIDEO layout is 640x480 with rows doubled so legacy display sizing does not halve the output. The frame is already turned into readable row order by the driver; VPE must not mirror or vertically flip it again. A CRT-style filter may reconstruct scanline and shadow-mask character at the logical 640x240 resolution, but geometry, keystone, reflection plane, and cabinet occlusion belong to the authored Unity scene.

## Evidence precedence and known discrepancy

PinMAME's current `p2k_names.h` tables were walked completely against the games' own switch, coil, and lamp tests. Those measured runtime names and public addresses take precedence over visual inference. The manual remains physical truth for connectors, wires, driver transistors, parts, and stock-vs-unused fitment.

The operations manual's table and location drawing place 18B on the left slingshot and 28B on the right, while the machine lamp test reports the opposite semantic names. The definition therefore binds public 15/manual 18B to the runtime name Right Slingshot Spotlight at the manual's left-side coordinate and public 31/manual 28B to the runtime name Left Slingshot Spotlight at the manual's right-side coordinate. This deterministic split keeps machine-test semantics and factory physical positions without inventing a wiring swap, and the ignored conflict records why the names and sides appear crossed.

The supplied `Attack and Revenge from Mars (Midway-Williams) v600.vpx` is not RFM geometry. Its embedded script runs `afm_113b`, its callbacks are Attack from Mars addresses, and its extracted screenshot shows the AFM playfield. It is retained at SHA-256 `9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be` as a rejected candidate and contributes no RFM spatial or controller assertion.

## Remaining author-ready work

- Validate mechanism startup states, transition timing, ball routes, and launch vectors in an actual RFM recreation or repeatable runtime harness.
- Complete non-opto normally-open/closed and pulse semantics instead of inferring them from labels alone.
- Authenticate the optional six-ball/opto-expander, knocker, shaker, ticket, and Prism/firmware combinations per driver revision.

## Sources

- `manual.rfm.operations-1999`: February 1999 model 50070 operations manual, SHA-256 `6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df`; four stock location drawings, service tables, and assemblies.
- `manual.rfm.mypinballs-opto-expansion-v2`: myPinballs Opto Expansion Upgrade Install Instructions v2.0, SHA-256 `00a744e1cc6507c328b22f33fc4f3aa6f8ec4826dce0a8874493023ee8d48fbf`; retrofit wiring tables and installed trough/lock photographs.
- `pinmame.core.8371478a7640`: pinned P2K implementation and machine-test-verified device tables at revision `8371478a7640f1896dcdf565aed340dc5df989ba`.
- `vpx-table.attack-and-revenge-v600-rejected`: exact user-supplied hybrid VPX, rejected because it runs AFM ROM semantics and AFM geometry.
