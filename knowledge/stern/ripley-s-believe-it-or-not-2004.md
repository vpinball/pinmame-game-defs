# Ripley's Believe It or Not! (Stern, 2004)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete public I/O inventory, factory wiring and parts, native displays, custom mechanisms, firmware/language variants, and recreation behavior validated**

## Identity and evidence precedence

This definition covers the single 2004 physical product and all 25 PinMAME 3.00, 3.01, 3.02, 3.10, and 3.20 English/French/German/Italian/Spanish drivers. The optional UK three-post board is configuration-dependent hardware, not another product. The known-working VPW v1.3 script is controller-facing semantic and causal ground truth; the official Stern manual governs physical construction, wiring, parts, coils, bulbs, and boards; pinned PinMAME governs public routing, clone identity, and native display layouts. Runtime traces validate the exact ROM, public callbacks, GI, and display availability without treating inactivity as proof of absence.

## Four-ball path, shooter, scoop, and lock

Four balls initialize on trough switches 11-14. Q1 ejects the ball at 14 through stacking opto 15, and the proven table advances the remaining balls at 100 ms intervals. Shooter switch 16 supports manual plunge and Q2 auto-launch. Side-scoop entry 28 leads to held VUK switch 29 and Q12 eject. The Vari-VUK is a separate ball device on 52/Q3. Q5's proven `LockDiverter` feeds the visible lock, whose top/middle/bottom seats are 44/45/46; Q13 ejects from that lock path. Preserve sustained occupancy, actual containment, hidden paths, and release causality rather than pulsing all ball-position switches.

## Seven-detent vari-target

The 515-7322-00 vari-target has seven mechanical stops and three optos on board 520-5234-00. The proven script uses a 267-unit lever, 50-unit target width, 0.3 spring factor, 600-unit/s return, and sensor thresholds at path-length 1/6 for 42, 1/2 for 43, and 3/4 for 41. During travel it clears all three and asserts only the deepest crossed threshold; at boot it deliberately initializes 42 and 43 closed with 41 open. Q21 resets toward the 15-degree home angle. Recreate physical detents, spring/ball energy transfer, threshold order, and the overlapping boot state. The adjacent VUK 52/Q3 must remain a distinct ball device.

## Idol Eye and Shrunken Head magnets

The lower Idol Eye path closes opto 24. Q19 drives the Idol magnet to hold and throw the ball, while Q22 separately powers the opto emitter as a switched-ground LED; do not render Q22 as a decorative lamp. The Shrunken Head closes opto 23 and uses Q20 to hold then throw the ball. The proven virtual implementation samples at 150 ms, centers on tick 3, kills velocity/spin on tick 4, and releases/cools after tick 12 with bounded upward correction. Those timings are a reliable virtual baseline, while the manual's physical assemblies govern placement and field interaction.

## Flippers and Whitestar public-output traps

Q14 is the ordinary upper-right flipper output at public solenoid 14, with DS-5/public switch 88 as its button. The working table directly drives its virtual flipper from that key; its generic `sURFlipper` callback is not a Whitestar remap and must not replace Q14. Physical Q15 left and Q16 right are removed from public 15/16 and moved into PinMAME's lower-flipper pairs: Q16 uses power-phase address 45 and canonical `sLRFlipper` callback 46, while Q15 uses power-phase 47 and canonical `sLLFlipper` callback 48. PinMAME synthesizes each canonical callback's hold bit whenever the power bit is active. Bind the single physical right/left devices to 46/48, never instantiate 45/47 as extra coils, and retain normally-closed EOS inputs 81/83. Public 15 is synthetic fast-flip/game-on, while public 16 is unused.

## Diverters, post, pops, slings, routes, and optional hardware

The proven table binds Q4 to `TempleDiv` on the manual's left-ramp path and Q5 to `LockDiverter` on the right-ramp path. Energizing either callback rotates its collision primitive to the end position; release returns it to the start position. Recreate Q4's Temple branch and Q5's feed into lock seats 44-46, while treating ramp switches 31/53 as ball-passage sensors rather than diverter-position feedback. Q23 controls the unsensed top post. Six pop pairs are Q6/SW25, Q7/SW26, Q8/SW27, Q9/SW49, Q10/SW50, and Q11/SW51. Slings are Q17/SW59 and Q18/SW62, with two physical contacts per switch address. The upper mini-playfield has left/center/right contacts 38-40. Build every named orbit, ramp, spinner, lane, jackpot loop, head/tombstone target, and shared Tombstones 2+3 switch 32.

Q24 remains an optional, unassigned 5 V output: the exact script retains a `SolKnocker` routine but deliberately comments out the Q24 callback, and runtime activity proves only that public 24 can transition. A stock recreation must not invent either a physical or audible knocker. The UK 520-5068-01 board adds left/center/right posts at public 33-35; optional matrix switches 1/8 are sustained left/right UK cabinet buttons. They are rules-facing inputs, not post-position sensors, and no direct electrical/mechanical button-to-post linkage is established. Install all five items only for the UK/special configuration; a standard configuration legitimately omits them.

## Lamps, GI, and four native display surfaces

All matrix lamps 1-80 are installed with the exact #555/#44 parts and matrix wiring in JSON. The matrix is eight drive columns by ten return rows, enumerated across each row. Q25-Q32 are the eight flasher channels: Q25 drives two #89 lower-pop/lower-left flashers, while Q30 drives one #89 under the upper playfield and one #906 on the right ramp. GI public 0 is one relay controlling four separately fused physical strings: F24 back panel, F25 upper/mid-right playfield, F26 upper-left/back panel/coin door, and F27 upper-right/mid-left/lower playfield. The script's `GIUpdate2` suffix selects the second, modulated callback interface; it is not a second GI address. Recreate the four physical circuits but route their common controllable state through GI 0.

The machine has a main native 128x32 DMD and three independent physical 5x7 mini-DMD blocks on board 520-5236-00. The `dispBION` layout array exposes them in controller-index order 0 main, 1 left, 2 center, and 3 right, which is encoded explicitly in JSON. `CORE_NODISP` only suppresses the three small layouts from the legacy composite renderer; it does not make them virtual or absent. PinMAME also writes a backward-compatible 15x7 segment representation, and the proven script consumes that legacy view, but a new recreation should bind the three native 5x7 surfaces and avoid building a single physical 15x7 display. The boot harness received layout callbacks for indices 0-3 but pixel-frame callbacks only for the main DMD, so runtime activity of the small displays is not claimed beyond source/manual validation.

## Author construction checklist

- Build four trough seats/stacking opto, manual and auto shooter, side scoop/VUK, three-seat visible lock, seven-detent vari-target and its separate VUK, both ball-throw magnets, both ramp diverters, top post, three flippers, six pops, two slings, elevated mini-playfield, all routes/targets/spinners, optional UK posts, complete lamps/flashers/GI, and all four native DMD surfaces.
- Initialize coin-door memory protect -3, trough 11-14, and vari optos 42/43 active. Preserve ball occupancy, normally-closed lower EOS contacts, vari detents and threshold order, magnet capture/release timing, moving collision, diverter/post direction, visible lock containment, and real release paths.
- Bind all matrix/dedicated/DIP inputs, every physical Q1-Q32 through its declared public address, fast-flip 15, optional AUX33-35, explicit unused compatibility positions, lamps 1-80, GI 0, and four displays. Never instantiate mirror/compatibility callbacks as extra playfield hardware.

## Sources

- `manual.stern-ripleys.2004`: official 191-page manual SHA-256 `94a94aef7437fa5f78cadddd66801e96224cfe6a5b8ff643c4c6b09d979fad9e`, organized under the external manual cache with searchable text, table extraction, and rendered visual review.
- `vpx.ripleys-vpwmod-1.3`: exact known-working script SHA-256 `3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7`.
- `rom.stern-ripleys.3.20`: exact external archive SHA-256 `092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3`; ROM bytes remain external.
- `runtime.ripleys.boot`, `runtime.ripleys.boot-start`, and `runtime.ripleys.gameplay`: separately hashed LibPinMAME traces with their evidence limits stated in JSON.
