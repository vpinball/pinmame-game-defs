# 24 (Stern, 2009)

Coverage: **partial - public I/O inventory and controller causality are documented, but authoring-critical physical construction remains unresolved**

## Identity and evidence precedence

This definition covers Stern's February 2009 physical machine and every PinMAME driver `twenty4_130`, `twenty4_140`, `twenty4_144`, and `twenty4_150`. PinMAME dates final V1.5 to 2010, but that is a firmware release date, not a second hardware product. The known-working `24 (Stern 2009) v.2.3.1.vbs` is the semantic ground truth for controller callbacks and physical causality. ROM service diagnostics validate labels and wire colors. Stern's partial Pink/Blue book validates physical assemblies but is not a complete service I/O manual; the later official Iron Man Vault manual is used only for standard connector pins on the same SAM boards. IPDB and Stern validate the physical toy behaviors.

## Balls, trough, and shooter

The machine has four balls resting on trough switches 18-21. Q1 feeds through jam switch 22 to shooter switch 23, where the player can plunge manually or Q2 can auto-launch. The proven VPX script pulses switch 15 during its release bookkeeping, but the ROM Switch Test proves 15 is the physical Tournament Start cabinet button. Never construct a fifth trough/release sensor at 15. Preserve individual occupancy and sustained trough/shooter state. Except for the two proven cabinet buttons, the partial manual does not establish factory contact construction; choose suitable physical sensors while preserving every validated semantic binding and pulse/sustained behavior.

## Motorized suitcase and visible lock

The suitcase is a stepper-driven moving assembly and a three-ball visible lock, not a single solenoid animation. The proven VPX script registers Q21 alone as its logical animation callback, but the same line's hardware comment explicitly lists physical suitcase motor positions Q21/Q23/Q25/Q30. These four drives energize the 24 V stepper assembly 511-5072-00 through cable 036-5634-11-A7; their A/B/C/D electrical order and individual supply-wire colors are not established, so retain the Q identities and determine phase wiring for the chosen motor driver. Q28 separately raises/releases the lock post. Home switch 48 is active only at the closed/home endpoint, clears during travel, and returns near home. The ordinary ROM coil diagnostic skips all four drive positions and the auxiliary menu exposes a dedicated Suitcase Motor Test. The proven script animates roughly from 358 to 320 and back, but tune physical travel to the modeled geometry. Its corrected visible-lock order maps physical bottom switch 43 to ROM 45, middle 44 to 44, and top 45 to ROM 43. IPDB confirms balls can remain locked while the suitcase is open or closed. Recreate moving collision geometry, three physical ball seats, the release post, and actual containment.

## Safe House, Sniper House, and drop targets

The Safe House contains a saucer on switch 3 with eject Q3. Q12 flips the entire front down to expose the miniature army-men interior and its flashers; return it upright when disabled and move its collision surface with it. Q13 resets the two House drop targets on 11/13. The Sniper House uses Q14 to open and reveal target 62, Q29 to operate the neighboring up-post, and a figure that waggles while firing. Single drop targets 60/61 reset independently with Q4/Q5. Stern describes several single Sniper targets as obscuring or freeing shots, so every drop and facade position must alter ball collision and shot availability rather than merely render an animation.

## Gates, posts, routes, and standard devices

Q6/Q7 operate the left/right control gates and Q22 operates the unsensed left-ramp up-post. Left-loop spinner 10 pulses; left/right orbit contacts are 46/54; right-ramp entrance is 58; top lanes are 55-57; lower outlane/return pairs are 24/25 and 29/28. Flippers use Q15/Q16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pop pairs are Q9/SW30, Q10/SW31, and Q11/SW32; slings are Q17/SW26 and Q18/SW27. Fixed standups are House 1/2, Cell Phone 4, CHLOE 5-9, MOLE 33/34, and the right bank 39-41. Q8 is an optional shaker added in ROM v1.44; Q24 is an optional common-board 5 V device channel with no stock playfield device identified.

## Lamps, flashers, display, and emulator capacity

Lamp-matrix addresses 1-80 are populated except explicit unused address 9. The ROM service test reports addresses 72-75 only as CTU and 76-78 only as MOLE; numeric suffixes in JSON preserve unique bindings without inventing an unverified face order. The 2009 machine uses incandescent matrix lamps and aggregate GI 0. Q19/Q20/Q26/Q27/Q31/Q32 are feature flashers. Bind the native 128x32 four-bit DMD and synthetic SAM game-on 33. Because PinMAME declares `SAM_NO_AUX`, public 51-66 remain explicit unused emulator capacity, not physical outputs, and legacy game-on aliases 34-36 are not devices.

## Author construction checklist

- Build the typed four-ball trough, manual/auto shooter, motorized suitcase with four addressed stepper drives/home sensor/three ball seats/release post, Safe House facade and saucer, House two-bank, Sniper facade/figure/target/post, both single drops, control gates, ramp post, flippers, pops, slings, routes, spinner, and fixed targets.
- Initialize trough switches 18-21 and suitcase home switch 48. Preserve ball occupancy, normally-closed EOS state, endpoints, moving collision geometry, drop latching/reset, gate direction, lock ordering, and physical release causality.
- Bind every matrix/dedicated/DIP input, Q1-Q32, synthetic game-on 33, explicit unused auxiliary 51-66, lamp 1-80, GI 0, and the DMD. Do not create playfield hardware from aliases or emulator capacity.
- Use the proven VPX script as the runtime tie-breaker, ROM diagnostics for exact semantics and wire labels, Stern's partial manual for 24 construction, and the later SAM schematic only for standardized board connector pins.

## Coverage blockers

This definition is intentionally partial. The following are recreation blockers, not coordinate-tolerance notes:

- Suitcase phase causality is incomplete. The pinned v2.3.1 script establishes that Q21, Q23, Q25, and Q30 are four physical drive positions for the 24 V stepper and that Q21 is the logical animation callback. Its proven behavior does not identify the physical A/B/C/D phase order or individual supply/control wire colors. The official Stern page-43 assembly list identifies the motor and microswitch hardware but no phase map; the ordinary ROM coil test skips these decoder holes, and the suitcase menu run proves only that a separate test exists. A physical recreation therefore cannot yet be wired from this record without a continuity/diagnostic capture or authoritative schematic, nor can an equivalent driver abstraction be claimed to preserve factory causality.
- Contact construction and normal-state coverage is incomplete. The manual identifies suitcase microswitch parts 180-5119-02 and 180-5119-00, but does not map those contacts or establish the factory construction, normal state, and seat for every used playfield switch. The JSON deliberately retains `switch_type: unknown` and the validated matrix semantics instead of telling an author to substitute a sensor while calling the result complete.
- Trough geometry is only an ordered shared-assembly projection. The exact VPX exposes Drain and BallRelease, not SW18-SW22 contact objects; the five recorded points preserve the order and controller causality with about +/-0.03 normalized practical uncertainty, but do not establish the physical seat or contact/optic construction of each trough position.
- Lamp addresses 72-78 are semantically grouped by the ROM diagnostic as CTU (72-75) and MOLE (76-78), but their individual face order is not established. Q27 also retains the exact script's tentative `under jet?` comment rather than an unsupported named physical target. Their controller bindings and direct/derived coordinates are preserved, but the unresolved physical naming must not be read as author-ready recreation semantics.

## Sources

- `manual.stern-24-parts.2009`: official partial parts book SHA-256 `c547202e54b3ffbe53ba955db9eed8d52a6fef4b4807416de2f31ccf18aaf71f`, organized under the external manual cache with searchable text and rendered pages.
- `vpx.stern-24-2.3.1`: pinned known-working script SHA-256 `7bf550806bd87c17417a974ed75b1700885da883e0dce5ce31d7dc7ba6cc094f`.
- `rom.stern-24.twenty4-150`: exact external archive SHA-256 `f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4`; the ROM readme supplies revision-specific mechanism fixes.
- `runtime.stern-24-switch-diagnostic-1-17`, `runtime.stern-24-switch-diagnostic-22-64`, `runtime.stern-24-coil-diagnostic`, `runtime.stern-24-lamp-diagnostic`, and `runtime.stern-24-suitcase-motor-menu`: separately hashed held-switch, coil, lamp, and menu traces with their evidence limits stated in JSON.

## Normalized spatial retrofit

Coordinates use the global playfield space: x=0 is left, x=1 is right, y=0 is rear/backglass, and y=1 is front/apron. The exact working VPX was found in the required search order at `L:\Visual Pinball\Tables\24 (Stern 2009).vpx`, copied to the established external VPX cache, and extracted with vpxtool `git:v0.33.3`. Its embedded `twenty4_150` script is retained as an object/callback artifact, while the pinned known-working v2.3.1 script remains the semantic and causality tie-breaker where the older embedded script differs.

Direct centers are used for the exact VPX playfield objects: targets, bumpers, gates, lanes, routes, flippers, slingshots, toy anchors, visible lock, lamps, and flasher helpers. The suitcase, Safe House, Sniper House, Q21/Q23/Q25/Q30 stepper drives, and switch 48 deliberately use shared-assembly anchors. EOS contacts are disclosed projections to exact flipper centers. Trough switches 18-22 are an ordered projection between the exact VPX Drain and BallRelease anchors because the working VPX has no trough-contact objects; the stated uncertainty is practical authoring tolerance, not coordinate precision. No coordinate is inferred from a perspective drawing.

The 40 exact VPX GI objects are not 40 physical sockets: each broad odd `GI_n` and its localized even helper are synchronized render layers for one physical GI position, and four lane-guide objects provide the remaining anchors. The definition therefore carries 22 physical GI anchors. Flasher quantities follow the semantic comments and physical inventory (`Q19` x3, `Q20` x2, `Q26` x3, `Q27` x1, `Q31` x2, `Q32` x3), while synchronized VPX helper objects are not multiplied into hardware.

The older embedded script's visible-lock ordering is superseded by the reviewed v2.3.1 mapping: physical bottom/middle/top contacts 43/44/45 bind to ROM switches 45/44/43. The official Stern parts book, IPDB, and manufacturer evidence remain authoritative for physical multiplicity and custom mechanisms; the SAM reference manual remains limited to shared board topology and connector pinouts. The unresolved suitcase stepper phase order, exact factory contact construction, and precise hidden trough contact seats remain concrete author tasks documented in the base knowledge and mechanism records.

## Spatial evidence

- `vpx-table.stern-24-2009-local`: exact VPX SHA-256 `7e8bf294f3b3dd4bfe53e2727957d000568bc9d079caeed60038ceeb8d1b89f5`, 61,915,136 bytes, retained under the external VPX source cache; extracted object packet and candidate map are retained under the external review-artifact cache.
- `vpx.stern-24-embedded-2.0.1`: extracted script SHA-256 `be3a0e0e96df6d232fa1fa99110e63781abdca5484a1b97de75de0fd1760135a`; it is an older embedded artifact and does not override the pinned semantic v2.3.1 script.
- The geometry source search stopped after the exact table was found in `L:\Visual Pinball\Tables`; the archive folder and public VPU/VPF fallback were not needed.

## Status decision

This is a schema-v2 **partial**, not author-ready. The direct VPX coordinates, disclosed shared-assembly anchors, ordered trough projection, physical quantities, and controller-to-mechanism records are retained as evidence. The conflicts above remain open because an author still lacks the suitcase phase wiring, complete factory contact construction/normal states, precise hidden trough seats, and a few physical names needed for a full recreation.
