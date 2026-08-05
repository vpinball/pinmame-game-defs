# Medieval Madness (Williams, 1997)

Coverage: **author-ready - complete physical I/O inventory, WPC-95 bindings, wiring, mechanism causality, driver-variant boundary, normalized spatial placement, and recreation behavior validated**

## Identity and evidence precedence

This is the Williams WPC-95 physical product released July 1997, IPDB 4032, manual 16-50059-101, project number 559, game number 50059. It covers the whole `mm_*` clone tree: `mm_05`, `mm_10`, `mm_109`, `mm_109b`, `mm_109c`, `mm_10pfx`, and `mm_10u`. Every one of those is a game-ROM revision for the same physical machine; the Zen Studios "Pinball FX" and Global VR "Ultrapin" images only change display text and do not create a separate physical game, so their catalog years 2018 and 2006 never override the 1997 build.

Evidence precedence for this definition: the retained known-working VPW v1.0 script is runtime and mechanism-causality ground truth; the Williams operations manual controls physical construction, part numbers, wiring, polarity, quantities, and device presence; pinned PinMAME controls controller generation, public address topology, and display metadata; the retained VPX geometry supplies normalized coordinates. All four retained manual PDFs are image-only scans, so every printed table used here was read from rendered pages. The OCR text retained beside them is a search index and never an authority.

## Controller platform and address topology

`GEN_WPC95` (`PINMAME_HARDWARE_GEN_WPC95 = 0x80`) with `wpc_dispDMD`, DCS sound, and a security CPU. The controller profile is `pinmame.wpc-95`.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic 111-118. The manual states the notation itself in T.13: "The number on the left indicates the column. The number on the right indicates the row. Example - Lamp 23 means 2nd column, 3rd row." PinMAME's `mmGameData` inverted-switch mask corroborates it, inverting column 3 rows 1-7 and column 4 row 1, which is exactly the printed opto set.
- Solenoids: physical drivers 1-28; PinMAME state channels 29-32; Fliptronic upper-flipper circuits 33-36; WPC-95 LPDC output 37 with PinMAME's backward-compatibility mirror at 41; Fliptronic lower-flipper circuits 45-48; simulator-only 49 and reserved 50.
- Lamps: 8x8 matrix 11-88, all 64 addresses populated. The pinned harness observed every one of them active.
- GI: five strings on public addresses 0-4.

Two WPC-95 numbering facts must not be lost. First, the printed solenoid table numbers the lower flipper circuits 29-32, while PinMAME publishes the same circuits at 45-48; the manual numbers are preserved as `manual.address` aliases. Second, LPDC output 37 and public address 41 are the *same* drawbridge motor, because `core_getSol` duplicates 37-40 into 41-44 for WPC-95. A recreation binds one motor and accepts either address; it must never create two.

## Coin-door service buttons

The printed switch matrix aligns dedicated switches D1-D8 with matrix rows 1-8: 1-4 are the left, center, right, and fourth coin chutes, 5 is Service Credits/Escape, 6 is Volume Down/Down, 7 is Volume Up/Up, and 8 is Begin Test/Enter. PinMAME's MAME-only keyboard port (`WPC_COMPORTS`) labels those four service bits in the opposite order, which is a UI key binding rather than public address semantics. The pinned harness settled the whole group against the running ROM. Holding public switch 8 with the coin door open produced the ROM's own prompt `TO RESET SCORES- HOLD ENTER`; pulsing public switch 7 raised the ROM's `VOLUME` display from 12 to 15; pulsing public switch 6 lowered it back to 12. Switch 5 is the remaining position. A consumer that maps an "Enter" action must map it to switch 8, not switch 5.

## Ball path, trough, and shooter

Medieval Madness has no manual plunger. Four balls rest on trough optos 32-35, with Trough Ball 1 (32) at the eject end nearest the shooter lane and Trough Ball 4 (35) at the drain entrance. Solenoid 2 ejects the ball on 32 and the same event asserts trough-eject opto 31. The ball lands on shooter-lane switch 18 and auto-plunger coil 1 launches it when the cabinet Launch Ball button (switch 11) is pressed. In loops mode a launched ball travels the full loop and is delivered cleanly to the left flipper.

Trough optos 31-35, left-popper opto 36, castle-gate opto 37, and moat-enter opto 41 are printed as optos that rest closed. PinMAME's `mmGameData` inverted-switch mask covers exactly those eight (column 3 rows 1-7 plus column 4 row 1), so the public state is already normalized: assert the public switch when a ball is present and never invert again.

## Castle: drawbridge, gate, lock, and explosion

The castle is four cooperating devices and the diagnostics prove their order.

- **Drawbridge (solenoid 37).** A continuously rotating low-power motor, not a two-position solenoid. Switch 56 closes at the raised limit and 57 at the lowered limit. T.18 runs the motor continuously and pauses briefly on each up/down switch *edge*; a missing edge produces "Drawbridge Up Switch Bad" or "Drawbridge Down Switch Bad". PinMAME's own `mm_handleMech` models the same behaviour with a 500-step position counter that closes 56 near steps 490-10 and 57 near steps 240-260, and it starts a session with the drawbridge up.
- **Castle gate / portcullis (solenoids 5 power and 6 hold).** T.19 first lowers the drawbridge and refuses to run at all without the drawbridge-down switch. With the gate closed the ball path is moat-enter 41, castle-gate 37, then moat-enter 41 again as the ball rebounds. With the gate held open the path is 41, 37, then castle-lock 44 into the lock area. The ROM drops the hold coil after two idle minutes so it cannot overheat.
- **Castle lock and left popper (solenoid 3).** Balls that pass the gate are held behind switch 44 and collect on left-popper opto 36; solenoid 3 returns them to the playfield.
- **Exploding castle (solenoid 4).** Pressing Enter inside T.19 shakes the castle three times and then explodes it for roughly four seconds. The superstructure has to be reset by hand afterwards.

## Trolls

Two trolls rise through the playfield on Fliptronic upper-flipper circuits: left troll on public solenoids 33 power and 34 hold, right troll on 35 and 36. The flipper circuit diagram on manual page 3-11 says so in a footnote: "The UPPER RIGHT FLIPPER circuit is used for the LEFT TROLL. The UPPER LEFT FLIPPER circuit is used for the RIGHT TROLL." This is the clearest place where physical kind and emulator transport differ: these are troll actuators, not flippers, and `mmGameData` declares `FLIP_SOL(FLIP_L)` so PinMAME never drives them as flippers. Position switch 74 (left) or 75 (right) closes while the troll is raised, and PinMAME's `mm_handleMech` ties each up-switch directly to its hold output. A ball striking a raised troll closes under-playfield switch 45 or 46. Troll targets 15 and 25 are the standups behind each troll, reachable while it is down. The ROM lowers a raised troll after two idle minutes so the troll coils cannot overheat; a recreation must reproduce that timeout rather than leave a troll up indefinitely.

## Tower, diverter, and lock post

T.17 documents two tower states. With the tower diverter (solenoids 15 power and 16 hold) up, a right-ramp shot runs right-ramp-enter 63 then right-ramp-exit 64 and returns to the right flipper. With the diverter held down, the shot runs 63, raises tower lock post 26, climbs into the tower, and closes tower-exit switch 58. The ROM returns to the ramp state after two idle minutes so the diverter coil cannot overheat. The lock post works inverted in PinMAME's simulation: a held ball is released when the post output drops, so drive the post's physical state from the output rather than from a scripted timer.

## Loops and control gates

Two solenoid gates decide whether a loop shot completes or feeds the jets. T.16 gives the causality exactly: travelling left to right the *right* gate (solenoid 27) opens on the second left-loop switch, Left Loop High (66); travelling right to left the *left* gate (solenoid 28) opens on the second right-loop switch, Right Loop High (68). When the opposite gate stays closed the ball is routed through Left Top Lane 47 or Right Top Lane 48 into the jet bumpers instead. The ROM's error strings distinguish the two failure modes: "Gate Stuck Closed" surfaces in loops mode and "Gate Stuck Open" in jets mode.

## Standard devices

Three A-12030-3 jet bumpers (coils 12/13/14, skirt switches 53/54/55) sit above the right ramp entrance. Two slingshots (coils 10/11) each carry an A-17800 kick switch and a *separate* A-17794 score switch with a diode attached; only the score switch reaches the matrix, at 51 and 52. The right three-bank (switches 71/72/73, assembly A-21576-4) is a plain standup bank with no reset coil - it is not a drop-target bank. Catapult target 12 guards the catapult saucer; a ball entering the saucer closes switch 38 and coil 8 flings it up the left ramp path. Merlin's Magic hole under the jets is right-eject switch 28 with coil 9.

## Lamps, flashers, and general illumination

All 64 lamp-matrix addresses are populated. Two addresses drive two bulbs: 15 "Save the Damsel!" and 78 "Super Jets". They are different cases. Lamp 15 is one large circular insert lit by two bulbs - the lamp-locations map draws it as a single circle between the triangular 14 and the small rectangular 16 - so it has one placement and a physical quantity of two. Lamp 78 is two separate arrow inserts, one in each orbit lane; the map numbers only the right-hand arrow but draws the matching left-hand arrow uncalled-out, and the retained table binds an emitter to each, so both are placed. Lamps 87 and 88 are the bulbs inside the illuminated Launch and Start buttons and are cabinet hardware. The lamp-locations parts list calls lamp 72 "Ball Save" while the lamp matrix prints the insert legend "Magic Shield"; they are the same insert and the printed insert legend is canonical here.

Flashers 17-25 all drive two bulbs. Addresses 17-20 have a playfield flasher *and* a separate insert-panel flasher behind the backbox translite - they are the only flasher circuits with two voltage and two drive connections, on J133-6/J134-5 and J111/J112 - so only their playfield bulb gets a coordinate. Addresses 21-25 have two bulbs each, and for 22 and 25 the manual's Note 2 places one on the playfield and one on back-panel assembly A-20158; the retained table has exactly that pair at the rear playfield edge.

GI strings 01-03 are the bottom, middle, and top playfield circuits and the retained script drives them from `UpdateGI` as the GIB, GIM, and GIT emitter arrays. Strings 04 and 05 are the top and bottom *insert panel* circuits behind the translite; the printed table marks both "always on, they do not brighten and dim", string 05 also feeds a cabinet connector, and the retained script deliberately leaves both cases empty. The manual prints no per-string bulb count, so the physical quantities recorded here come from the retained table's emitter arrays.

## Startup and service state a recreation must establish

- Trough optos 32-35 asserted with four balls, drawbridge-up switch 56 asserted, coin-door-closed switch 22 asserted.
- Switch 24 is a permanently closed link (part 5643-15190-00) that proves the matrix is connected; hold it active. The retained VPW script initializes it to 0, which is a table simplification with no observed effect.
- The A-18249-3 coin-door interlock removes +50 V and +20 V solenoid power when the door opens; with the door open the ROM shows "COIN DOOR IS OPEN / COILS AND FLASHERS ARE DISABLED".
- PinMAME reports state channel 29 active throughout attract mode. Channel 31 is the ROM's fast-flip flag, not a physical game-on relay: the harness saw it active during ball play *and* in an attract frame shortly after the coin-door Enter button was released, so do not treat it as a ball-in-play indicator. Neither channel is a physical Medieval Madness device.
- The pinned harness reproduced a first-boot factory reset ("FACTORY SETTINGS RESTORED" then "BOOKKEEPING TOTALS CLEARED") from empty NVRAM.

## Production split and two documented manual disagreements

Williams changed five subassemblies on **July 21, 1997**, and the parts section prints both configurations. Games produced before that date use A-21712-2 (up/down post), A-21733 (popper), A-21719 (troll), A-21723 (drawbridge/gate) and A-21976 (drawbridge switch/bracket); later games use A-21712-5, A-22027, A-22034, A-22033 and A-22036. The coil and switch part numbers inside them are identical - the A-21719 and A-22034 troll assemblies both carry an FL-11753 coil and a 5647-12693-11 miniature switch - so only the enclosing assembly differs and a recreation does not change behaviour, but the assembly numbers are recorded for both builds.

Two places in the manual disagree with themselves, and both are recorded rather than averaged:

- **Fliptronic positions F5-F8.** The game-specific switch-locations parts list on page 2-48 marks all four Not Used, which matches a machine with no upper flippers. The flipper circuit diagram on page 3-11 nonetheless draws F6 and F8 as upper-flipper cabinet optos and labels F5 and F7 "Basket Made Opto" and "Basket Hold" - devices Medieval Madness does not have. Page 3-11 is a reused Williams template, so the game-specific parts list governs and public switches 115-118 stay unused.
- **Lamp 72.** The lamp matrix prints the insert legend "Magic Shield"; the lamp-locations parts list calls the same socket "Ball Save". Same insert, two names; the printed insert legend is canonical here.

## Supply voltages and the general-illumination circuit

Manual page 3-11 shows the flipper and troll circuits fed from +50 V on J119 (RED-GREEN, RED-BLUE, RED-VIOLET and RED-GRAY), and the drawbridge motor from GRAY-YELLOW +12 V on J139-2. Manual page 3-10 shows all five general-illumination strings running from the 6.3 V transformer secondary, with the three playfield strings on a triac-switched circuit that can be dimmed and the two insert-panel strings on a bridge-rectified circuit that cannot. That page bounds every string at up to 18 bulbs but publishes no exact per-string count, and no parts page itemizes the insert-panel sockets, so the physical bulb count for GI 04 and GI 05 is deliberately not asserted here and has to be read from the machine. The three playfield strings take their counts and coordinates from the retained table's emitter arrays.

## Author construction checklist

- Build the four-ball trough with the drain at Trough Ball 4, the auto-plunger shooter lane, both slingshots, three jet bumpers, the right three-bank, the catapult saucer and its guard target, Merlin's Magic eject, both loops with their two control gates, both ramps, the tower with its diverter and lock post, both trolls with their targets, and the complete castle (drawbridge motor, portcullis power/hold, castle lock, left popper, exploding castle).
- Preserve opto polarity for 31-37 and 41 and for the two flipper-button optos; do not invert what PinMAME already normalizes.
- Treat solenoids 37 and 41 as one drawbridge motor, and 33-36 as troll actuators rather than flippers.
- Reproduce the three anti-overheat timeouts: tower-lock mode reverts after two minutes, castle mode reverts after two minutes, and a raised troll lowers after two minutes.
- Pick the pre- or post-July-21-1997 assembly set to match the machine being recreated; behaviour is identical, only the assembly part numbers change.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the printed Not Used positions, Fliptronic 111-118 with 115-118 explicitly not installed, the eight CPU DIP bits, solenoids 1-50, lamps 11-88, GI 0-4, and the 128x32 DMD.

## Sources

- `manual.williams.medieval-madness.1997`: operations manual 16-50059-101 front matter and Section 1, SHA-256 `57d3b23e0d73e31318fb7054a1dc966db0924cf8f908a5844719ba9f50f0e672`.
- `manual-parts.williams.medieval-madness.1997`: Section 2 Parts Information, SHA-256 `9baac8156b1115171c0c5fc1cced2a4bfa2280067c72a49b58678d89c70b6f1d`.
- `manual-schematics.williams.medieval-madness.1997`: Section 3 Wiring Diagrams and Schematics, SHA-256 `1a426136cbc9df6297e8ea41d4f7b166d2b91aa2b188909b74d15be7b1c3d77d`.
- `vpx-script.mm-vpw-1-0`: retained known-working VPW v1.0 embedded script, SHA-256 `cdc5590888d810a44b772ec327789362cd27dd7a6c58870bc148b2d87a0f90f8`, binding `mm_109b`.
- `vpx-table.mm-vpw-1-0`: retained table, SHA-256 `9a05a555d03aca3d48d73b3e6566220b27fde46aa5d2517a08faacdbc58bcab9`, bounds `left=0 top=0 right=952.941 bottom=2164.706`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/mm.c` and the WPC-95 core/solenoid/flipper handling at the pinned revision.
- `runtime.medieval-madness.boot-start-and-service`: pinned LibPinMAME harness runs recorded in `evidence/runtime/wpc-95/medieval-madness-boot-start-and-service.json`.
