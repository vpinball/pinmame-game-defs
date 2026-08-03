# Metallica Pro (Stern, 2013)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical I/O, mechanisms, variant split, wiring, and recreation behavior validated**

## Identity and evidence precedence

This definition covers all 20 non-`h` Metallica drivers from `mtl_052` through `mtl_180c`. The `h`/`hc` family is the physically different Premium/LE playfield and has its own definition. JP's Metallica Pro 6.0.0 VPX script is the controller-semantics ground truth because it is a current, proven recreation bound to `mtl_180`; the official Stern manual governs physical inventory, wiring, assemblies, and service numbering; pinned PinMAME governs public API address groups, the SAM platform, DMD transport, and driver identity. The table author explicitly states that the Pro layout matches the original; its two added ramp spinners are ornamental, do not score, and must not be recreated as physical Pro switches.

## Edition differences that must be preserved

The Pro has ordinary matrix lamps and aggregate GI only. It has no Premium RGB/GI node board, no three-ball under-playfield coffin lock, no lowering coffin magnet or two-bit coffin processor, no captive-ball hammer, no motorized grave marker, and no motorized snake jaw/latch. Consequently public solenoids 51-58 and public lamp channels 81-136 are not part of this physical edition. The Pro retains four balls, a static grave-marker magnet behind three inline drop targets, an Electric Chair magnet and Sparky step-up driver, a passive captive ball, a static snake-head eject, and an electronically controlled loop up-post.

## Switches and initial state

All 64 matrix addresses, 24 dedicated addresses, and eight CPU-board DIP inputs are explicit, including unused locations. Four balls initially occupy trough switches 18-21. Output 1 ejects the rightmost ball and the proven script pulses shooter-path jam opto 22; switch 23 is the shooter lane. Switch 52 is the grave-marker ball opto, 53 is the Electric Chair opto, 51 is the right eject, and 54 is the snake eject. The inline drop targets use switches 60 bottom, 61 middle, and 62 top; they are active while raised and open when hit. Switches 33/34, 38/39, 55-59, and 63/64 are explicitly unused because their Premium-only moving marker, physical spinners, motorized jaw, and coffin hardware are absent.

## Coils, flashers, lamps, and GI

The Pro I/O Power Driver board exposes physical outputs 1-32. Outputs 1-18 cover trough, auto launch, both magnets, both ejects, loop post, optional shaker, pops, drop-bank reset, slings, flippers, one unused address, and the Sparky step-up driver. Outputs 19-32 are the service-manual flashers and 24 is the optional coin meter. PinMAME public solenoid 33 is the synthetic SAM game-on state, not ticket hardware. Optional ticket-dispenser advance, meter, and switched-ground service identities 33-35 are preserved separately under `physical.output.ticket`, because the stable LibPinMAME API does not transport them. There is no auxiliary-board public range 51-58. Standard lamps 1-80 exactly follow the Pro matrix on manual PDF page 122, with every blank address marked unused. The only PinMAME GI binding is aggregate `pinmame.output.gi/0`; the working script switches the whole ordinary-GI collection together and has no colored GI.

## Grave marker, chair, captive ball, and drop bank

The grave marker is static on Pro. Output 3 drives its centered magnet at working-table strength 70, switch 52 detects the ball, and switches 60-62 sit on the three inline drop targets leading into the capture area. Output 12 resets the bank. The Electric Chair uses magnet output 4 at working-table strength 45, opto 53, standup 35, and output 18 to shake/step up Sparky. The captive ball is passive: its impacts pulse switch 42 and there is no hammer output.

## Ejects, post, and standard devices

The right scoop holds a ball at switch 51 and output 6 ejects at VPX angle 220, strength 25, and force variation 2. The static snake mouth holds a ball at switch 54 and output 5 ejects at angle 195, strength 26, and angle/force variation 2; it deliberately has no jaw-open or latch sensor. Output 7 raises the loop post while energized and drops it when disabled, with no position sensor. Output 2 drives the auto launcher at VPX power 62 with 0.6 second full-plunge time and 0.3 random variation. The remaining playfield includes two lower flippers, three pop bumpers, two slingshots, two ramps, fuel standups, guitar-pick standups, and ordinary rollover/target switches. Do not add scoring loop spinners merely because JP's VPX includes two decorative non-scoring spinner objects.

## Optional cabinet hardware

Output 8 is the optional shaker and output 24 is the optional coin meter. The optional ticket dispenser uses physical service identities 33 for advance, 34 for its meter, and 35 for switched ground, plus dedicated switch D19 (public switch -5) for ticket-notch feedback. Retain those `physical.output.ticket` bindings even when a specific recreation omits the option; do not bind its advance line to PinMAME solenoid 33, which is game-on.

## Recreation checklist

- Create four trough balls on switches 18-21, keep switch 22 clear downstream, and bind shooter lane 23.
- Build the static grave-marker magnet and three normally-closed inline drop targets, the Electric Chair magnet/Sparky toy, passive captive ball, static snake eject, right scoop, auto launcher, and unsensed loop up-post with the documented causality.
- Implement public physical outputs 1-32, virtual game-on 33, matrix lamps 1-80, aggregate GI 0, the 128x32 DMD, all dedicated cabinet inputs, and optional shaker/coin/ticket hardware; the ticket service functions are physical identities without a stable LibPinMAME transport.
- Do not copy Premium-only outputs 51-58, RGB/GI lamp channels, coffin mechanisms, hammer, moving grave marker, motorized snake jaw, or loop-spinner scoring switches.
- Use the working VPX strengths, angles, timing, and state transitions as initial authoring values and the manual's service drawings for physical placement and wiring.

## Sources

- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; Pro service tables on PDF pages 119-129.
- `vpx.metallica-pro-jps-6.0.0`: extracted known-working `mtl_180` script, SHA-256 `d5ea2810308e05daee22c2a75b3d80a4b19fbd3f89e67144a38f9c20bdb33307`; callbacks and mechanisms on lines 35, 81-165, and 200-453.
- `vpx-table.metallica-pro-jps-6.0.0`: VPForums table, SHA-256 `837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118`; downloaded archive SHA-256 `5fafb136ed9f76ad32dcc035bd72c4dadd856562778f9fae53d7e1bcc9396ff0`.
- `runtime.metallica-pro.boot-start`: family-compatible `mtl_170` ROM run, raw SHA-256 `65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e`, ROM archive SHA-256 `2f11830ffb35f2a80258e47a5ea0abd17fc2350995bb1d1d1a165480be61f654`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM platform, display, and driver configuration.
