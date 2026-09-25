# Cactus Canyon (Bally, 1998)

Coverage: **author_ready - complete physical I/O inventory, WPC-95 bindings, wiring and public polarity, mechanism causality, driver-variant boundary, normalized spatial placement, and recreation behavior validated; no switch-polarity conflict remains**

## Identity and evidence precedence

Bally physical product released 1998, IPDB 4445, OPDB `G4835-Mb5eO`. It covers the five-driver `cc_*` clone tree: `cc_13` (production 1.3, the parent; the retained known-working VPW table's `cGameName = "cc_13"` binds this ROM), `cc_10` (1.0), `cc_104` (Bally / The Pinball Factory 1.04 Test 0.2), `cc_12` (1.2), and `cc_13k` (Bally 1.3 "Real Knocker" patch). All five are recorded `physical_compatibility: "identical"`; none changes the switch matrix, lamp matrix, solenoid/flasher table, or playfield hardware.

Evidence precedence for this definition: the retained embedded VPW script is the runtime address and causality authority; the Bally operations manual (part 16-50066-101, January 1999 Final, scanned by flipperspill.com) is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME (`src/wpc/sims/wpc/prelim/cc.c`, revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`) owns controller topology; the retained VPX table supplies geometry. The retained manual PDF carries a fresh OCR text layer, so every printed table used here was extracted with `pdftotext -layout` and then confirmed against the rendered page image; the retained human transcription is the source of record whenever OCR and the rendered page disagree. A second retained Cactus Canyon manual documents the unrelated Chicago Gaming Company remake (models 14000-SE/SE+/LE) and names hardware ("Hall Effect PCB", "H Bridge PCB", "Window LED PCB") that does not exist on this WPC-95 machine; nothing in this note or the resulting definition cites that document.

The retained VPX table (`Cactus Canyon (Bally 1998) VPW 1.0.2.vpx`) has exact playfield bounds `left=0 top=0 right=952 bottom=2162`; every normalized coordinate in this note and the definition is `x/952` and `y/2162`.

## Controller platform and address topology

`GEN_WPC95` (`PINMAME_HARDWARE_GEN_WPC95 = 0x80`) with `wpc_dispDMD`. The controller profile is `pinmame.wpc-95`.

- Switches: dedicated coin-door/service positions 1-8, matrix 11-88 as drive column then return row, Fliptronic 111-118. `ccGameData`'s inverted-switch mask is `{0x00,0x00,0x00,0x7f,0x03,0x00,0x00,0xc1,0x00,0x00,0x00,0x00}`: column 3 (`0x7f`, rows 1-7) normalizes 31-37, column 4 (`0x03`, rows 1-2) normalizes 41-42, and column 7 (`0xc1`, rows 1/7/8) normalizes 71, 77, 78. The Fliptronic/flip-switch-column byte (index 11, `CORE_FLIPPERSWCOL`) is `0x00`, the same value every other reviewed WPC-95 game leaves it at, because WPC-95 reads that column through `WPC_FLIPPERSW95` with its own fixed hardware inversion independent of the driver's `invSw` array; the flipper-opto positions 112/114 are therefore already normalized by hardware, not by this mask.
- Solenoids: physical drivers 1-6, 8-22 (driver 7, the knocker circuit, is printed with a populated power-driver transistor Q69 but no coil connection anywhere, so it is unfitted on the standard machine); solenoid 23 is likewise a populated-transistor, unfitted flasher position. Fliptronic upper-flipper circuits 33-36: this machine has no upper flippers, and only two of the four positions are repurposed (33 power / 36 hold for the Bart toy motor and hat), leaving 34 and 35 genuinely unused. WPC-95 LPDC outputs 37/38 (train motor forward/reverse) are duplicated by PinMAME's backward-compatibility mirror at 41/42 -- the same physical H-bridge drive lines to the A-22271 Train Motor Circuits assembly, not a second motor. PinMAME state channels 29-32 (two WPC J111 general-purpose mirrors, the synthetic game-on/fast-flip state at 31, and a constant-zero reserved position at 32); Fliptronic lower-flipper circuits 45-48; simulator-only position 49; reserved position 50; and custom solenoids 51-64, all unused because `ccGameData` declares no `custSol`.
- Lamps: 8x8 matrix 11-88, all addresses populated except 85, 86, and 87 (Not Used).
- GI: five strings on public addresses 0-4. `ccGameData` declares no `lampCol`, so no auxiliary lamp column exists.

Two numbering facts must not be lost. First, the printed solenoid table numbers the lower-flipper circuits 29 (power)/30 (hold) and 31 (power)/32 (hold); PinMAME publishes the same circuits at public 45/46 (Lower Right Flipper) and 47/48 (Lower Left Flipper). Second, printed 37/38 (train motor) are WPC-95 LPDC outputs at public 37/38 directly, and PinMAME additionally mirrors them at public 41/42; a recreation binds one physical two-direction motor and accepts either address pair, never creating a second device.

## Ball path, trough, and shooter

Four balls rest on trough optos 32 (Trough Ball 1, nearest the eject coil) through 35 (Trough Ball 4, drain entrance). Solenoid 9 (`ReleaseBall` callback) ejects the resting ball; the retained script's trough handling manages the shift, and `sw31_Hit` pulses trough-eject opto 31 as the ejected ball leaves. The ejected ball rests on shooter-lane switch 18, and auto-plunger coil 1 (`AutoPlunger` callback) launches it -- there is no manual plunger.

## Train: motorized figure on tracks

Solenoids 37 (reverse) and 38 (forward) drive the train along its track through an H-bridge (A-22271 Train Motor Circuits assembly, gates U3A/U3B reverse and U3C/U3D forward). On the physical-ROM (PROC=0) path the retained script registers a VPinMAME `cvpmMech` for it (script.vbs lines 191-203): `Sol1 = 38`, `Sol2 = 37`, `vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear`, `Length 570`, `Steps 613`, `.AddSw 72, 0, 0` and `.AddPulseSw 71, 14, 3`. PinMAME therefore asserts Train Home (72) only at mech step 0 and pulses Train Encoder (71) for 3 of every 14 steps while the train moves; `TrainF`/`TrainB` only animate the `Train`/`Train1` primitives toward `TrainMech.Position`. The `sw71` Timer object is used only by the PROC=1 community P-ROC path. Both switches are documented projections onto the Train mechanism's own retained table objects, because there is no separate playfield sensor object for either address.

## Mine: motorized entrance sign, and mine popper

Solenoid 17 raises and lowers the Mine sign (retained Primitive `MineSign`); `MineTimer_Timer` also drops or raises the Mine Entrance wall (switch 15's `IsDropped` flag) as the sign passes a threshold. Mine Home (77) and Mine Encoder (78) are the printed position/step optos on the A-22443 Mine Dual Opto PCB. On the physical-ROM path the retained script registers a VPinMAME `cvpmMech` (script.vbs lines 176-187): `Sol1 = 17`, `vpmMechOneSol + vpmMechReverse + vpmMechLinear`, `Length 100`, `Steps 49`, `.AddSw 77, 0, 1` and `.AddPulseSw 78, 8, 2`, so PinMAME asserts Mine Home at mech steps 0-1 and Mine Encoder for 2 of every 8 steps. Both are documented projections onto the Mine mechanism's own retained table object (Primitive `MineSign`).

Separately, a ball resting in the mine hole on opto 41 (Mine Popper, A-22467) is kicked back to the playfield by solenoid 6 (`SolMinePopper` callback); the retained script's `MineHole_Hit`/`MinePopper_Hit` handlers animate the kickout.

## Saloon: popper, gate, and Bart toy

A ball resting in the saloon hole on opto 42 (Saloon Popper, A-22435) is kicked back to the playfield by solenoid 8 (`SolSaloonPopper` callback); in the retained script `BartPopper_Hit` asserts opto 42 (`BartHole_Hit` only plays a sound) and the `SolSaloonPopper` callback performs the kickout. The retained table names the physical kicker object `bartpopper` and adds a co-located script-only `secretentrance` kicker at the identical coordinate (489.5982, 193.86546), which is a duplicate of the same physical device rather than a second one.

The Saloon Gate is a mechanical switch (part 5647-12693-11) on a gate near the saloon, address 73; the retained table has no dedicated solenoid driving this gate, only the sensing switch.

Solenoid 33 (`MoveBart` callback) oscillates the Bart figure left/right along the X axis for as long as it is held on (`Bart1_Timer`); solenoid 36 (`MoveHat` callback) lifts the hat and returns it (`Bart2_Timer`/`BHit_Timer` sine-style Y animation). Saloon Bart Toy switch 75 senses a ball hitting the figure (`sw75_Hit` pulses it). Both solenoids repurpose printed Fliptronic upper-flipper circuit positions (33/34 would be upper-right flipper power/hold, 35/36 upper-left) because the machine has no upper flippers; only one half of each pair is actually used (33 power, 36 hold), leaving 34/35 genuinely unused.

## Drop targets, gunfight posts, and loop gates

Four independent drop targets sit in ascending playfield-x order (61 Left, 62 Left Center, 63 Right Center, 64 Right, all A-22296), each with its own reset coil (solenoids 2-5, callbacks `Drop1`-`Drop4`) and mechanical switch (part 5647-12693-21).

Solenoids 14/15 (`GunPostLeft`/`GunPostRight` callbacks, A-22465) raise and lower two posts (retained table objects `LPin`/`RPin`) that block the Left Out/Right Out lanes; there is no printed switch dedicated to either post.

Solenoids 21/22 (`LGate`/`RGate` callbacks, A-22482) operate the left and right loop gates; the printed solenoid table lists both on "Flasher"-type driver circuits, which names the driver bank, not the device, and the device is a coil.

## Slingshots and jet bumpers

Each slingshot assembly (A-17801) carries a kick switch (A-17800/SW-1A-114) and a separate scored switch (A-17794/SW-1A-120, with a diode attached), matching switch matrix rows 51 (Left) and 52 (Right).

Left (B-12030-2/A-16443, switch 53) and Right (B-12030-2/A-16443, switch 54) jet bumpers are native round VPX `Bumper` objects; Bottom (A-23146, switch 55) is modeled in the retained table as a slingshot-style `Wall` object (`sw55`, with its own `sw55_Slingshot`/`sw55_Timer` handlers) rather than a round bumper ring -- a table-authoring choice, not a missing device, and it is grouped with the two true slingshots in `vpmNudge.TiltObj`. By normalized x, Left (0.1603) sits left of Right (0.3377); Bottom's y (0.2065) is greater than both (0.1642, 0.1246), i.e. closer to the player, matching its name.

## Lower flippers

Two flippers (A-14876-R right, A-15849-L left, coil FL-11630) on Fliptronic circuits. Each flipper has a separate power and hold winding: the ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. There are no upper flippers; the upper-flipper Fliptronic circuits (33-36, and switches 115-118) are either unfitted or repurposed for the Bart toy.

## Opto polarity

The opto sweep checked both manual cues -- matrix shading ("OPTO, TYPICALLY CLOSED") and a populated Opto Assembly Part Number with a blank Switch Part Number, cross-referenced against the board-assembly pages (A-18617-1/A-18618-1 Trough IR LED/Photo Transistor PCB; A-22407 Train Single Opto; A-17316 Flipper Opto PCB; A-20246 10-Opto PCB; A-22443 Mine Dual Opto PCB) -- column by column against `ccGameData`'s inverted-switch mask, and found **full agreement**: every physically normally-closed opto switch (31-37, 41-42, 71, 77, 78, plus the Fliptronic 112/114 button optos handled by WPC-95's own hardware inversion) is normalized by the emulator. No `conflict.*-opto-not-normalized` entry is present for this machine. Rows that show a blank Switch Part Number but are **not** opto (28, 44, 86, 87 standup-target assemblies A-20499-12, and 46 the Beer Mug switch assembly A-20783-7) confirm that a blank Switch Part Number alone is not a reliable opto signal; the board-assembly pages are the tie-breaker. The upper-flipper opto template positions (F6/F8, printed shaded but unfitted because there are no upper flippers) are correctly excluded from the normalized set.

## Flashers and general illumination

Flashers 18-20 and 24-28 are printed with fitted playfield bulbs; 21 and 22 on the same driver bank are the loop-gate coils. Addresses 24, 26, 27, and 28 (Beacon, Saloon, Back Right, and Back Left Flashers) are each printed twice on the Solenoid/Flasher Locations page -- once "Playfield" and once "Insert Panel" -- so each fits two `#906` bulbs; only the playfield bulb receives a playfield coordinate, and the insert-panel bulb is backbox hardware behind the translite with no playfield coordinate. Flasher 26's playfield bulb is the Saloon flasher on a bracket at the right ramp (printed 2-37), which the table models as the decorative spotlight `SpotP`; its script-bound lights only render the glow on the saloon. Flasher 18's placement is the smallest-radius bulb light beside the mine hole, a rule-based choice because 2-37 does not draw it. Address 23 is a populated power-driver transistor (Q25) with no voltage or drive connection in any column, so no flasher is fitted there. Solenoid 17 drives the Mine Motor rather than a flasher.

General illumination splits three ways on the retained script's `UpdateGI` dispatch (`GiCallback2 = GetRef("UpdateGI")`): GI address 0 drives the `LeftGI` collection (10 physical bulb positions, printed Illumination String 1, #44 bulbs), GI address 1 drives `RightGI` (12 physical positions, printed Illumination String 2, #44 bulbs), and GI address 2 drives `TopGI` plus `TopGI2` (16 physical positions, printed Illumination String 3, #44 bulbs; `TopGI2`'s three members are switched on only when the table's VRRoom option is 0 and duplicate three `TopGI` bulbs rather than adding positions). Each collection lists roughly twice as many raw members as physical bulbs; clustering members within 25px (about one bulb diameter) collapses them to the counts above, and each placement is the smallest-falloff-radius member's own center, never a cluster centroid. There is no `Case 3`/`Case 4` in `UpdateGI`, so GI addresses 3 (Illumination String 4, #555, backbox insert-panel) and 4 (All Illumination, #555, backbox insert-panel plus cabinet via J104) have no playfield representation in the retained table, matching the manual (String 4 is insert-panel-only; String 5/"ALL ILLUMINATION" is insert-panel-plus-cabinet) and take a controlled `cabinet_or_service` spatial record. The printed footnote "these general illumination strings do not brighten and dim, they are always on" is a single unscoped sentence below the whole General Illumination block on this manual (unlike some other WPC-95 manuals' per-row asterisk), so it applies to all five strings.

The 128x32 dot-matrix display is backbox hardware and takes a controlled `not_applicable` spatial record with both PinMAME core and manual provenance.

## Variants

- `cc_13` (parent): Bally production 1.3 game ROM shipped with the physical machine; the driver the retained known-working VPW table binds to (`cGameName = "cc_13"`).
- `cc_10`: Bally game ROM 1.0 for the same physical machine; switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware unchanged.
- `cc_104`: Bally / The Pinball Factory 1.04 Test 0.2 game ROM, a later test firmware revision of the same physical machine.
- `cc_12`: Bally game ROM 1.2, a later firmware revision with no controller-address or playfield change.
- `cc_13k`: Bally 1.3 "Real Knocker" patch ROM, a community patch of the same 1.3 firmware that changes the knocker driver behavior for operators who field-install a real knocker coil on public solenoid 7 (fitted with a drive transistor but no coil on the standard machine); it does not add or remove any playfield device.

All five drivers are recorded `physical_compatibility: "identical"`.

## Author construction checklist

- Build the four-ball trough (drain at Trough Ball 4), the auto-plunger shooter lane, both slingshots, the left/right round jet bumpers plus the bottom slingshot-style jet bumper, the four-target drop bank, both gunfight posts, both loop gates, the mine popper, the saloon popper (with its co-located duplicate kicker treated as one device), the saloon gate, the motorized mine entrance sign, the motorized train on tracks, and the Bart figure/hat toy.
- Preserve opto polarity for 31-37, 41-42, 71, 77, 78, and the Fliptronic 112/114 button optos; PinMAME already normalizes all of them, so do not invert again.
- Treat LPDC outputs 37/38 and their PinMAME mirrors 41/42 as one physical two-direction train motor, not two devices.
- Do not label public solenoid 7 a knocker on the standard `cc_13`/`cc_10`/`cc_104`/`cc_12` machine; it has a populated driver transistor but no fitted coil. Only `cc_13k` exists for operators who field-install one.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the printed Not Used positions, Fliptronic 111-118 with 115-118 not installed, the eight CPU DIP bits, solenoids 1-64 (34/35 and 51-64 genuinely unused), lamps 11-88 with 85-87 not installed, GI 0-4, and the 128x32 DMD.
- Give only the playfield-side bulb of solenoids 24, 26, 27, and 28 a playfield coordinate; their insert-panel bulbs are backbox hardware.
- GI addresses 3 and 4 have no playfield representation; they are backbox insert-panel (and, for address 4, cabinet) circuits.

## Sources

- `pinmame.catalog.4ec52ff0ac13`: pinned PinMAME catalog driver records for the `cc_*` clone tree, revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/prelim/cc.c` `ccGameData` and related WPC-95 core/solenoid/flipper handling, revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`.
- `controller-profile.pinmame-wpc-95`: WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules (`internal:controllers/pinmame/wpc-95.json`).
- `manual.bally.cactus-canyon.1998`: Bally Cactus Canyon operations manual (part 16-50066-101, January 1999 Final, scanned by flipperspill.com), SHA-256 `dfd55dad3d85899c6e6b8a392f7965dff41ffade91587ba1b145762b7d6e1015`.
- `manual-support.bally.cactus-canyon.1998`: retained human transcription of every table used by this definition, SHA-256 `68119b41c5bc5cada849c64ea0fc105262394eaaa71f0f5704f4c43b1efe2904`.
- `vpx-table.cc-vpw-1-0-2`: retained known-working VPW 1.0.2 recreation (`Cactus Canyon (Bally 1998) VPW 1.0.2.vpx`), SHA-256 `2e93faec289ce517a30f7285187d9eedca4652417ea2744e381c04a2e94e371b`, bounds `left=0 top=0 right=952 bottom=2162`.
- `vpx-script.cc-vpw-1-0-2`: retained embedded VPW script (`script.vbs`, 3,711 lines), SHA-256 `7b07f1492c5db71dd7acc33c8c5875cfbbe7a799092722b2372784149cd06313`.
- `vpx-extraction.cc-vpw-1-0-2`: canonical `vpxtool` extraction manifest, SHA-256 `a0f7c251d961e72d588951496cbafd73ff9836475c5bc006cc44e63906aaa8bb`, 1268 files, 139765398 bytes.
