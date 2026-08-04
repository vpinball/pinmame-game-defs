# Mustang Pro (Stern, 2014)

Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, recreation behavior, and spatial placements validated**

## Identity and variants

This definition covers the physical Pro playfield used by non-`h` PinMAME drivers `mt_120`, `mt_130`, `mt_140`, `mt_145`, and colored-ROM variant `mt_145c`. IPDB 6098 identifies the Stern SAM Pro machine from April 2014; Premium, Limited Edition, and Boss use the physically different `h` family and a separate definition.

## Evidence precedence

The recovered working Mustang Pro PhysMod5 table by 85vett with gtxjoe's 1.0 functional mod is authoritative for controller-facing addresses, callback polarity, initial state, ball routing, mechanism causality, and the Board-5 lamp shuffle. The official Stern Pro manual is authoritative for the physical inventory, labels, wiring, part numbers, and printed diagnostic numbers. Pinned PinMAME source is authoritative for SAM topology and driver identity. An isolated exact-ROM run independently confirms the native display, GI address, and public lamp range. When these sources differ, preserve both physical and runtime facts and follow the proven table script for controller behavior.

## Physical differences from Premium/LE

The Pro lacks the Premium/LE turntable and its index/home switches, both single drop targets, auxiliary orbit gates, ramp diverter, lockbar action button, RGB arrow/action lighting, and 12-transistor auxiliary output board. Matrix positions 49-53 and 56-64 are therefore unused. The Pro instead has one orbit-post assembly at output 31 and right-scoop eject at output 32 through step-up drivers. N2O center/right are switches 4/5, spinner is 48, the standard lamp matrix uses Pro-specific labels, and its white/grid/sign Board-5 inventory ends at printed diagnostic 108.

## Switch topology

Matrix switches 1-64, dedicated D1-D8 at public 65-72, flipper switches D9-D16 at public 81-88, D17-D24 at public -7 through 0, and DIP D25-D32 are explicitly enumerated, including unused addresses. Normally-closed EOS inputs are 83 left and 81 right; flipper buttons are 84 left and 82 right. Momentary playfield contacts are marked `pulse`; lanes, trough, scoop, captive-ball, and other occupancy contacts remain sustained while occupied. The passive bowl/whirlpool holds switch 46 active from trigger entry until exit.

## Lamp addressing and GI

Standard matrix lamps 1-80 are direct. Board-5 printed diagnostics 81-97 are also direct, but printed 98 Toolbox is public `ChangedLamps` channel 103, printed 99 New Car is public 102, and printed 100-108 map to public 104-112. The JSON binds public controller channels and retains every printed value as `manual.address`; never wire the sign lamps by printed number alone. This exact shuffle is implemented by the recovered table and documented by the contemporaneous PinMAME integration discussion. The exact `mt_145` run emits public lamps through 112 and GI channel 0. The native display is a 128x32, depth-4 DMD.

## Trough and shooter lane

The physical trough has six ball sensors 17-22 plus jam opto 23. The recovered table creates six balls using `InitSw 0,23,22,21,20,19,18,0`, so its proven controller model occupies 18-23 and omits physical switch 17. Recreate all seven physical sensors, but use the script-compatible ordering unless a more exact physical simulation deliberately models the discrepancy. Output 1 ejects at 90 degrees with force 8 and pulses switch 22. Output 2 invokes an impulse auto-plunger using power 40, time 0.6, and random variation 0.3; physical shooter-lane occupancy is switch 47.

## Raising ramps

The mid and upper ramp assemblies each have distinct power/hold windings: outputs 3/4 and 5/6. The recovered recreation keys geometry from the hold windings. When output 4 is asserted it opens the mid gate and makes the bottom/mid ramp surface visible and collidable; de-assertion closes it and removes the surface. Output 6 does the equivalent for the upper ramp. Switches 39 and 40 are exit optos that pulse on ball traversal, not ramp-position sensors. Preserve both windings in the authored machine even though the proven script only uses the hold callbacks to select its simplified two-state route geometry.

## Orbit posts

The service manual prints one physical `31 UP POST` assembly. It initializes dropped; assertion raises it and de-assertion drops it. The working VPT implements that one assembly's blocking geometry with two tangent walls named `UpPost` and `UpPost2`, toggled atomically from output 31. Those are collision elements, not proof of two physical posts. Switches 44 right orbit and 45 left orbit report ball passage and do not sense post position.

## Scoop and captive ball

Switch 43 remains active while a ball is held in the right scoop. Output 32 ejects it at 185 degrees with nominal force 20, Z 0.4, and force variance 2. The working table visually sinks an entering ball by 4 units per 2 ms tick until below -30, then transfers it into the controller-facing one-ball stack; this is render/ownership handling rather than an extra PinMAME mechanism. The captive assembly has one nailed ball, back switch 8, front/rest switch 9, travel parameter 10, force transfer 1, and minimum impact force 7.

## Drops, pops, slings, flippers, spinner, and bowl

GEARS switches 34-38 latch individually while down; output 7 raises the complete five-bank. Pop switches 30-33 pair with outputs 9-12 using the physical labels in the service manual. Slingshot switches 26/27 pair with outputs 13/14. Lower flippers use outputs 15/16, buttons 84/82, and normally-closed EOS inputs 83/81. Every spinner rotation pulses switch 48. The passive whirlpool/bowl has no dedicated output and keeps switch 46 active while a ball crosses its trigger.

## Recreation checklist

- Construct every listed physical input and output, including explicit unused controller positions, seven trough/jam sensors, the single orbit-post assembly, the two dual-winding ramps, standard lamp matrix, Board-5 grid/sign lighting, GI, and native DMD.
- Initialize the orbit post dropped, the captive ball at front/rest switch 9, five-bank targets raised, six trough balls with the script-compatible 18-23 ordering, and ramp collision routes according to their hold-output state. If reproducing the proven VPT route geometry, animate both tangent collision elements from the one post output.
- Bind extended lamps to JSON public addresses and use the printed diagnostics only as physical aliases.
- Keep route-exit switches 39/40 distinct from ramp position; neither ramp has a dedicated position switch on the Pro.
- Treat the recovered table's force, direction, Z, timing, and captive-ball constants as proven authoring starting points; refine geometry against measurements without changing controller causality.

## Spatial coordinate model

Every physical playfield input, actuator, lamp, and GI socket has a normalized player-view placement: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. Exact object centers come from the known-working VPT only after script/manual reconciliation. Trough contacts, captive-ball switch 9, implicit EOS contacts, sign lamps, back-panel flashers, and GI sockets use explicitly disclosed assembly or drawing projections with practical uncertainty; cabinet, service, virtual, unpopulated, unused, and DIP devices are explicitly outside playfield space.

The Pro manual's lighting drawing proves 32 physical GI emitters behind one public transport channel: 15 wedge-base playfield lamps, eight bayonet-base playfield lamps, two separately called-out spot assemblies, and seven red rear bayonet lamps. Calibrated drawing projections preserve the four physical GI-0 through GI-3 regions; VPT light pools, broad fields, and reflections are excluded.

The switch-location drawing plots callouts 49 and 50 even though the electrical matrix table leaves 49-53 blank and the working Pro script binds neither 49 nor 50. The definition follows the proven controller behavior and electrical table, keeps both channels explicitly unused, and records the drawing conflict instead of inventing two live switches. The drawing is still valuable as evidence that the page was shared or revised inconsistently.

The standard lamp audit corrects a prior one-address shift: both 43 and 44 are blank, 45 is Shot Arrow #5, 49 is the bottom right 3-bank lamp, and 80 is the physical right-pop lamp. Addresses 20/26 and 34/42 are paired color channels at shared fourth-gear and sixth-gear insert centers.

## Sources

- `manual.mustang-pro`: official Stern `Mustang-Manual.pdf`, SHA-256 `63d0b8d44dadb22e8e878586805f805b71aa65038a77e00f5b973ece3b118235`; scanned I/O tables on PDF pages 12, 15, 18, and 20, physical location drawings on PDF pages 13, 16, 19, and 21, and GI map on PDF page 40.
- `vpx-table.mustang-pro-85vett-gtxjoe-1.0`: working `Mustang Pro_85vett_mod_gtxjoe_1.0.vpt`, 32,862,208 bytes, SHA-256 `3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c`, retained externally under `pinmame-vpx-sources/stern/mustang-pro-2014`; source archive SHA-256 `d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615`. Because one embedded image stream is one byte short, the vpxtool analysis derivative sets the GameData `SIMG` and `SSND` counts to zero; the OLE rewrite also zeroes 58 residual bytes after the GameData `ENDB` marker. All 5,311 GameItem streams and the embedded script remain byte-identical. The derivative SHA-256 is `b859cc86dd69978411eeaabb135e270c950e01498b2f986b034c6b49f5b9e7ed` and it is not distributed as the source table.
- `vpx.mustang-pro-85vett-gtxjoe-1.0`: exact embedded script SHA-256 `4ddf63df5b96e20da501ae336948e877473d21a4eeaf118a58bb7fcba9105a00`, extracted mechanically from the retained VPT.
- `runtime.mustang-pro.boot-start`: exact `mt_145.zip` isolated run; raw evidence SHA-256 `c5002a38d3a392aec6e0160e1cd7988917e38e6118e375ef8e7f03e8d9b7bfe2`, ROM archive SHA-256 `4240f7e311dfc571d8d1149e703d5f251d45b4dbccd3dfe157f781e750de7409`; ROM bytes remain external.
- `pinmame.core.4ec52ff0ac13`: pinned SAM platform and driver configuration.
- IPDB machine 6098: Mustang (Pro), Stern, April 2014; browser-verified because IPDB's Cloudflare gate prevents stable automated retrieval.
