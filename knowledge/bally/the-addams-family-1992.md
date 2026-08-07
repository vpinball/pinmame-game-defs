# The Addams Family (Bally, 1992)

Coverage: **partial - complete physical I/O inventory, WPC-Fliptronic bindings, mechanism causality, address enumeration, and spatial placement validated; kept partial solely because this knowledge note has not yet had the independent high-tier review this project requires before recreation_knowledge counts as validated. No conflict, unresolved address, or missing spatial placement remains.**

## Identity and evidence precedence

This is the Bally/Midway physical product released January 1992, IPDB #20, WPC part-number family 16-20017 (Operations Manual 16-20017-101, Operator's Handbook 16-20017-103, WPC Schematic Manual 16-20017-102A). It covers the `taf_*` clone tree rooted at `taf_l5`: 20 driver rows spanning Bally production revisions L-1 through L-7 with their D-*/LED-Ghost-Fix pairings, prototype revisions P-2/P-3, the newest known H-4/I-4 revision, the German-distributor-only L-6/D-6, a home/competition L-5C patch, and a 2026 community ball-saver patch (`taf_d7bs`) of the L-7 prototype. Every one of these is a firmware revision for the same physical machine.

**The 1994 Williams "Addams Family Special Collectors Edition / Gold" (`tafg_*`, IPDB #21) is a separate physical machine and is out of scope for this definition.** Three independent facts establish this: the WPC part-number family changes entirely (WPC 50038 vs this machine's WPC 20017); pinned PinMAME's own `taf.c` carries a 2000-era maintainer comment reading `/* 161000 TAFG is not a clone of TAF anymore */` immediately above a block that adds a dedicated Buy-In button and separate sound ROMs for `tafg`; and the retained manual set is physically distinct (Gold's manual is retained separately at `manuals/by-machine/williams.the-addams-family-gold.1994/`, and this definition's three PDFs were visually confirmed to never print "Gold" or "Special Collectors Edition" anywhere). `machines/stubs/tafg_lx3.json` is left untouched; it needs its own curation pass with Gold's own manual set as evidence, not a silent merge into this record.

Evidence precedence for this definition: the retained known-working VPX table ("The Addams Family (Bally1992) v2.3.2 (g5k)" by g5k, Sliderpoint and 3rdaxis, `cGameName = "TAF_L7"`) is runtime and mechanism-causality ground truth; the Operations Manual (16-20017-101) and Operator's Handbook (16-20017-103) control physical construction, part numbers, polarity, quantities, and device presence; pinned PinMAME (`taf.c`) controls controller generation, public address topology, and mechanism-counter causality; the retained VPX geometry supplies normalized coordinates. All three manual PDFs carry an OCR text layer, but the OCR misreads digits and glyphs on the two-column tables, so every printed table used here was visually re-transcribed from rendered pages into `external:pinmame-review-artifacts/the-addams-family-1992/manual-transcription.md` rather than trusted from OCR text.

## Controller platform and address topology

`GEN_WPCFLIPTRON` (`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`, pinned PinMAME's own comment names this exact machine: "Fliptronic flippers, Addams Family 2/92 - Twilight Zone 5/93") with `wpc_dispDMD`. This definition reuses `controllers/pinmame/wpc-fliptronic.json` unchanged -- the same profile Twilight Zone introduced.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic 111-118. `tafGameData` declares no custom switch column (`swCol = 0`).
- Solenoids: standard drivers 1-28 (all fitted; unlike Monster Bash's unfitted 4/7, every one of TAF's 28 printed solenoid-table rows has a real device), Fliptronic upper-flipper circuits 33-36, Fliptronic lower-flipper circuits 45-48. `tafGameData` declares no custom solenoids (`custSol = 0`), so nothing above 51 is claimed. Addresses 37-44 are simply unused address space on this generation (no LPDC board; see `wpc-fliptronic.json`'s own note), not a duplicated WPC-95-style mirror pair.
- Lamps: full 8x8 matrix 11-88 except two genuinely unused positions (41, 76). No auxiliary lamp column (`lampCol = 0`).
- GI: five strings on public addresses 0-4; address 3 is printed "Not Used" and has no playfield object.

## Opto polarity -- a clean cross-check, no conflict

Sweeping the Operations Manual's Switch Locations parts list (printed 2-39) for the Non-negotiable #1 opto signature (blank Switch Number, populated paired opto-assembly part number, "Opto" in the description) finds exactly seven addresses: the four Bookcase optos (53-56, assembly A-15017/A-15018), the Bumper Lane opto (57, assembly A-14231/A-14232), and the two Thing position optos (84/85, assembly A-15285). `tafGameData`'s inverted-switch mask --
`{0x00,0x00,0x00,0x00,0x00,0x7c,0x00,0x00,0x18,0x00,0x00,0x00}` -- covers exactly the same seven positions, column for column (column 5 bits 2-6 = 53-57) and row for row (column 8 bits 3-4 = 84-85). **Full agreement.** Unlike Monster Bash's Dracula-position optos or Centaur's lamp 113, there is no unresolved polarity conflict anywhere in this definition.

One address deserves a note despite not being a real opto: item 23 ("Ticket Opto.") has the word "Opto" in its printed description, but both its Switch Number *and* Switch Assy columns read blank/"Not Used" -- the manual's signature for "enumerated, never fitted", the same pattern this project uses for Monster Bash's knocker (solenoid 7) and Twilight Zone's third magnet.

## Both upper Fliptronic flippers are real, fitted hardware

Non-negotiable #3 asks whether the Fliptronic block hides a repurposed position (Monster Bash puts a spinner on F7). Here the opposite question needed settling: **are both upper flipper positions genuinely fitted, or is one a template row** (Monster Bash's F5/F6/F8 print "NOT USED")? Three independent sources say both are real:

1. `tafGameData.hw.flippers` sets both `FLIP_SW(FLIP_U)` and `FLIP_SOL(FLIP_U)` -- unlike Monster Bash, where `FLIP_SOL(FLIP_L)` only is set despite `FLIP_SW(FLIP_L|FLIP_U)`.
2. The Operations Manual prints a full illustrated, itemized parts breakdown for both `A-15205-R` "Flipper Assembly - Upper Right" (EOS switch `SW-1A-193`, coil `FL-11630` "Flipper Coil - Red", crank link, bumper plug, 20 line items) and `A-15205-L-1` "Flipper Assembly - Upper Left" -- not blank template pages.
3. The retained VPX script wires `SolCallback(sURFlipper) = "SolURFlipper"` and `SolCallback(sULFlipper) = "SolULFlipper"`, each rotating an independently animated table object (`Flipper1` upper-right, `Flipper2` upper-left, rendered with "Thing" hand art).

The two positions serve different gameplay roles. The **upper-left flipper is "Thing's Mini-Flipper"**, marketed in the manual's own "'Thing Flips' Automatic Calibration" section as "an exclusive Williams/Bally pinball innovation": an AI-calibrated *automatic* flip enabled by the far-left flipper return lane, not a normal player-controlled flipper -- "the ball will be diverted to the upper left mini-flipper and the game ('Thing') will attempt to shoot the ball into the swamp... between 50-60% of the time." `taf_stateDef`'s `stTFlip` case is the *only* place in the driver's own ball-routing logic that reads any upper-flipper solenoid (`core_getSol(sULFlip)`), confirming the asymmetry. The manual names this feature's own calibration inputs explicitly: the Bumper Lane Opto (57, printed "above the upper left mini-flipper"), the three Swamp Million targets (45/47/48), and the Swamp Lock Upper switch (71).

The **upper-right flipper** is never named in the rules text and never referenced in `taf.c`'s ball-routing sim; it is documented here as ordinary Fliptronic hardware with its own EOS/button pair and coil (`FL-11630`), CPU/software-timed like the left one (`FLIP_BUT(FLIP_L)` gives only the *lower* positions the direct hardware button-to-coil bypass on this generation). This project has not independently confirmed from static sources alone whether the ROM ties its firing unconditionally to the right flip button or gates it further -- that nuance is not required to recreate the physical device correctly, since a table author just wires the coil the way the known-working retained script does.

## Ball path, trough, and shooter

A ball drains through the Outhole (18) into a three-position trough -- Left Trough (15) nearest the drain, Center Trough (16), Right Trough (17) at the release position -- and solenoid 4 (Ball Release) kicks the ball at Right Trough into the shooter lane, where it rests on switch 27 (Ball Shooter) until the player pulls the manual plunger. TAF has no auto-plunger.

## Bookcase (Vault) and Thing hand -- motor-position mechanisms, not discrete sensors

Two mechanisms are driven purely by internal motor-position counters inside `taf_handleMech`, with **no discrete playfield sensor** behind either pair of switches:

- **Bookcase** (A-14970 assembly, solenoid 27): `locals.bookPos` is a 0-199 tick counter, incremented while solenoid 27 is asserted and wrapping at `TAF_BOOKTICKS = 200`. `swBookOpen` (81) asserts for `bookPos < 15`; `swBookClose` (82) asserts for `100 <= bookPos < 115`. The retained script never calls `Controller.Switch(81)` or `(82)`; it only reads `Controller.GetMech` to animate the visible `vault_base`/`vault_plastic`/`vault_post`/`vault_screws`/`vault_upright` rotation and swap the base's shadow image.
- **Thing hand** (A-14711 Hand Drive Assembly, solenoid 25): `locals.thingPos` is a 0-399 tick counter, wrapping at `TAF_THINGTICKS = 400`. `swThingDn` (84) asserts for `thingPos < 15`; `swThingUp` (85) for `200 <= thingPos < 215`. The retained script reads `Controller.GetMech` to drive `Thing.RotY`, `handMAGNET.RotY`, and a non-linear `thingBox.Rotx` lookup table (a 26-branch piecewise table in `ThingMotor`) so the visible box lid tracks the hand's rise smoothly.

Both pairs of switches are recorded here with a documented spatial projection onto their own mechanism's retained primitive (`vault_base` for 81/82, `Thing` for 84/85) rather than an invented sensor position, following the same allowance Monster Bash's Dracula-position optos used for `Primitive Drac`.

**The Thing hand is a separate mechanism from the four Bookcase optos** (53-56, "Bookcase Opto 1-4"): those four are fixed playfield sensors near the loop habitrail that calibrate ball detection around the bookcase area, not part of the rotation-position counter above.

## Thing saucer -- capture, magnet grab, and kickout

A ball entering the Thing saucer closes switch 87 (Thing Eject Hole). Solenoid 6 (Thing Magnet) then energizes a magnet under the saucer so the Thing hand mechanism appears to grab the captured ball (`ThingMagnet(Enabled)` sets `ThingBall = True` and drives the hand-grab sound/animation); solenoid 26 (also literally named "Thing Eject Hole" on the printed solenoid table) kicks the ball back out. All three devices -- the capture switch, the magnet, and the eject kicker -- share one physical assembly (`A-15368` Eject Assembly) and one retained script object, `ThingSaucer`. The separate Thing Kickout hole (switch 77, solenoid 7, assembly `A-15200`) is a distinct device elsewhere on the playfield.

## Swamp lock

Balls lock in sequence down the Vault habitrail: Swamp Lock Upper (71), Center (72, which additionally drops `Wall70` to hold the ball), Lower (73, which drops `Wall69`). Solenoid 28 (Swamp Release) releases locked balls into the Lockup Kickout hole (switch 74), and solenoid 8 (Lockup Kickout) kicks the released ball back to the playfield.

## Jet bumpers -- resolving a label discrepancy at address 34

Five B-12030-2 jet bumpers on switches/solenoids 31-35. The Operator's Handbook's rendered Switch Matrix wiring page (printed p.9-10) happens to render the column-3/row-4 cell identically to row 3 ("Center Left Jet"), which would duplicate switch 33's label. Two independent sources disagree with that page and agree with each other: the Operations Manual's Switch Locations parts list (2-39) names item 34 "Center Right Jet", and the retained script's own comment on `Bumper4_Hit` (the handler that pulses switch 34 and fires solenoid 12) reads the same. Per this project's "prefer the parts list, resolve typos via the symmetric partner" rule, address 34 is Center Right Jet, matching the natural Upper-Left / Upper-Right / Center-Left / Center-Right / Lower naming of the five-bumper cluster.

## Cousin It -- four targets, one address

Public switch 44 ("Cousin It") is shared by four standup targets on one figure -- `SW44a1`, `SW44a2`, `SW44b1`, `SW44b2` in the retained script, each independently pulsing switch 44 -- matching the printed parts list's two item rows ("44a ... Cousin It (2)" / "44b ... (2)", four targets total). All four cluster tightly in the retained geometry (x in [0.4075, 0.4292], y in [0.3903, 0.4645]), consistent with one small creature figure rather than four separated targets.

## Grave word features

Two independent five-letter word features exist on separate address ranges. The jet-bumper cluster's lamp column 3 spells **G-R-E-E-D** (lamps 31-35, one letter per jet). A different set of **standup targets and lamps spell GRAVE**: switches 41 ("Grave G"), 42 ("Grave R"), and 86 ("Grave A") are dedicated standup targets, while lamps 43 ("Grave G"), 44 ("Grave R"), 14 ("Grave A"), 17 ("Grave V"), and 48 ("Grave E") light the letters -- four different lamp-matrix columns, not a contiguous run, so "V" and "E" are lit by other shots (the Vault and Electric Chair features respectively) rather than by dedicated standup targets of their own.

## Magnets

Three under-playfield magnets implemented through the retained script's shared `cvpmMagnet` helper class rather than a scripted `SolCallback`: Left Magnet (solenoid 16, `LeftMagnet.InitMagnet LMagnet`), Upper Magnet (solenoid 23, `UpperMagnet.InitMagnet UMagnet`), and Right Magnet (solenoid 24, `RightMagnet.InitMagnet RMagnet`). None has a dedicated printed sensor switch; they hold and redirect the ball generically rather than gating a specific shot the way the Thing magnet does.

## Lower flippers

Two FL-15411 flippers on Fliptronic circuits 45/46 (right) and 47/48 (left). `FLIP_BUT(FLIP_L)` gives these two positions the direct hardware button-to-coil bypass circuit (minimum latency), dropping to the hold winding once the end-of-stroke leaf switch closes. The retained table runs `Const UseSolenoids = 2` (fast flips).

## General illumination

`UpdateGI`'s `Case 0` ("Left String") drives collection `GILeftString` (7 bulbs: GI11, GI41, GI38, LLightning1, GI14, GI28, GI15) and `Case 4` ("Right String") drives `GIRightString` (4 bulbs: GI42, GI34, GI33, SwampLight). There is no `Case 1`, `Case 2`, or `Case 3` block, matching the manual's own printed table exactly: GI02 "Insert House String" and GI03 "Insert People String" are backbox strings with no playfield object, and GI04 is printed "Not Used" outright.

## A modeling quirk worth flagging for future curators

The seven "THING" name-chase header lamps (public 81-87, spelling the word across the top of the backbox insert/header area rather than the playfield proper) sit at a small negative normalized y in the retained table (-0.0288 to -0.0292), just beyond the table's own defined top=0 edge. This matches the manual's own Lamp Locations diagram, which draws these seven lamps in a row *above* the cabinet outline rectangle -- i.e. a real design detail (a header strip mounted above the play surface), not a table-authoring bug. This definition clamps their recorded `y` to the schema-valid boundary 0.000000 and discloses the raw offsets in `vpx-geometry.txt`; a future curator encountering the same pattern on another WPC game should look for the same explanation before assuming a bug.

Similarly, every lamp address on this table has a co-located "b"-suffixed Light object (`L11`/`L11b`, `L12`/`L12b`, ... `L87b`) at an offset under one bulb diameter -- a systematic brightness-doubling technique used uniformly across the whole table, not evidence of physical two-bulb inserts (the manual marks no lamp position with a `(2)` bulb-quantity note). One address, 45 ("The Mamushku"), has two candidate primary objects instead of the usual primary+"b" pair (`L45old` and `L45bold`, neither referenced anywhere in `script.vbs`, relying on VPinMAME's default lamp-matrix name binding); `L45bold` is treated as the current art revision here.
