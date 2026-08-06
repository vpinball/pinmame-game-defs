# Monster Bash (Williams, 1998)

Coverage: **partial - complete physical I/O inventory, WPC-95 bindings, mechanism causality, driver-variant boundary, normalized spatial placement, and recreation behavior validated; wiring conflicted pending resolution of the Dracula-position opto polarity conflict (switches 74-78) below**

## Identity and evidence precedence

This is the Williams WPC-95 physical product released 1998, IPDB 4441. It covers the `mb_*` clone tree: `mb_05` (0.5 prototype), `mb_10` (parent, production 1.0), `mb_106`, and `mb_106b`. Every one of these is a game-ROM revision for the same physical machine.

Evidence precedence for this definition: the retained known-working VPW Mod v1.0 script is runtime and mechanism-causality ground truth; the Williams operations manual controls physical construction, part numbers, wiring, polarity, quantities, and device presence; pinned PinMAME controls controller generation, public address topology, mechanism-table position ranges, and display metadata; the retained VPX geometry supplies normalized coordinates. The retained manual PDF is an image-only scan (`pdftotext` yields 158 bytes of form feeds only), so every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/monster-bash-1998/manual-transcription.md`; the retained OCR text is a search index only and never an authority.

## Controller platform and address topology

`GEN_WPC95` (`PINMAME_HARDWARE_GEN_WPC95 = 0x80`) with `wpc_dispDMD`. The controller profile is `pinmame.wpc-95`.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic 111-118. PinMAME's `mbGameData` inverted-switch mask `{0x00,0x00,0x00,0x3f,0x06,0x00,0x00,0x00,0x00,0x00,0x00,0x00}` inverts column 3 bits 0-5 (31-36) and column 4 bits 1-2 (42-43); the printed matrix page (2-51) shades those eight "OPTO, TYPICALLY CLOSED" *and also* shades column 7 (74-78, the Dracula position optos) the same way, which the mask leaves at `0x00` -- see the unresolved polarity conflict below.
- Solenoids: physical drivers 1-3, 5-6, 8-16 (2 sockets absent: 4 and 7 are printed but unfitted); flashers 17-26; Fliptronic upper-flipper circuits 33-36 (unfitted, no upper flippers); WPC-95 LPDC outputs 37/38 (Dracula motor forward/backward) with PinMAME's backward-compatibility mirrors at 41/42; Fliptronic lower-flipper circuits 45-48; PinMAME state channels 29-32; simulator-only 49 and reserved 50. `mbGameData` declares no `custSol` and no `lampCol`, so no address above 50 or above lamp column 8 is published.
- Lamps: 8x8 matrix 11-88, all addresses populated except 78 (Not Used).
- GI: five strings on public addresses 0-4.

Two WPC-95 numbering facts must not be lost. First, the printed solenoid table numbers the lower flipper circuits 29-32, while PinMAME publishes the same circuits at 45-48; the manual numbers are preserved as `manual.address` aliases. Second, LPDC outputs 37/38 and public addresses 41/42 are the *same* Dracula-motor drive lines, because `core_getSol` duplicates 37-40 into 41-44 for WPC-95, and PinMAME's own `mb_mech[2]` mechanism table reads the Dracula figure through 41/42 rather than 37/38. A recreation binds one physical H-bridge motor and accepts either address pair; it must never create two devices.

## Ball path, trough, and shooter

Monster Bash has no manual plunger. Four balls rest on trough optos 32-35, with Trough Ball 1 (32) at the eject end nearest the shooter lane and Trough Ball 4 (35) at the drain entrance. Solenoid 9 ejects the ball on 32; the retained script's ball-release handler (`RandomSoundBallRelease sw32`) pulses trough-eject opto 31 in the same event, so switch 31 is a documented projection onto the trough-Ball-1 kicker position rather than a separately placed object. The ejected ball rests on shooter-lane switch 18 and auto-plunger coil 1 launches it when the cabinet Launch Ball button (switch 11) is pressed.

Trough optos 31-36 and flipper-button optos 42/43 are printed as optos that rest closed. PinMAME's `mbGameData` inverted-switch mask covers exactly those eight, so the public state is already normalized: assert the public switch when a ball or flipper button is present and never invert again.

## Dracula: rotating figure, coffin, and target ring

A DC gearmotor drives the rotating Dracula figure through an H-bridge (A-16120 DC Motor Control Assembly) on public LPDC outputs 37 (forward) and 38 (backward); PinMAME duplicates the same two drive lines a second time at mirror addresses 41/42. PinMAME's own `mb_mech[2]` table (`MECH_TWODIRSOL`) reads the mechanism over a 90-step position counter (`DRACTIME = 90`): switch 78 asserts at steps 0-5, 77 at 18-23, 76 at 36-51, 75 at 64-69, and 74 at 85-89 -- i.e. printed Dracula Position 1 through Position 5 in ascending step order. The five position optos live on the A-21402 Defender Switch Board Assembly mounted inside the mechanism, not as five separate playfield objects, so all five switches are documented projections onto the rotating figure's own table-object center. The figure rotates roughly 90 degrees about the vertical axis (the retained script sets `Drac.rotz = 77 - 1.125*(MechPos-5)`), not a vertical travel; the five position optos share one normalized `x`/`y` because they sense the figure's angular position, not its height.

**Unresolved polarity conflict (`conflict.dracula-position-opto-not-normalized`):** the manual documents 74-78 as opto interrupters that rest closed (A-21402 Defender Switch Board Assembly, blank switch part number, "OPTO, TYPICALLY CLOSED" shading on 2-51), but PinMAME's inverted-switch mask leaves column 7 at `0x00` -- unlike columns 3 and 4 (31-36, 42/43) it does not normalize these five addresses -- and `mb_mech[2]` itself asserts each switch ON over its step range, the sense a normally-open sensor would report. This keeps `physical_wiring` conflicted and the record `partial`; resolving it needs a LibPinMAME harness trace of a legal `mb_10`/`mb_106b` ROM observing the idle public state of 74-78 and their transitions as the Dracula motor steps.

Dracula Target switch 25 is a different device: a 47-segment target-wall ring (retained-table collection `DracTargets`) that surrounds the figure. `DracTargets_Hit(idx)` fires the shared handler and only one segment is active at a time, selected by the figure's own rotation (`DracTargets(Int((12 + Drac.RotZ)/2+1.25)).IsDropped = 0`), so switch 25 is likewise a documented projection onto the figure rather than a fixed target position.

## Frankenstein: motorized table and hit target; Up/Down target bank

Motor 27 rotates the Frankenstein figure (`franky`) between a lowered rest position and a raised striking position. PinMAME's own `mb_mech[1]` table reads switches 83 (table down, steps 0-10) and 84 (table up, steps `FRANKTIME`-10..`FRANKTIME`-1, `FRANKTIME = 120`) from the WPC-95 mechanism API's position counter. The retained script instead drives 83/84 directly from the figure's own rotation angle (`franky.rotx`) and raises Frank Hit switch 87 whenever the angle sits in the striking band, toggling a hit-wall collision object (`fhitwall`) in step so a ball can only score the hit while the figure is in range. All three switches (83, 84, 87) are documented projections onto the Frankenstein figure or its hit-wall collision object, because there is no separately named playfield sensor for each.

Motor 28 raises and lowers the two-target bank (`frankytargets`) between an up (targets exposed) and down (targets retracted) position. PinMAME's own `mb_mech[0]` table reads switches 81 (bank up, steps 0-10) and 82 (bank down, steps `BANKTIME`-10..`BANKTIME`-1) from the same mechanism API. The retained script drives 81/82 directly from `frankytargets.z` threshold crossings. Left and right standup targets 85/86 sit on the bank and are reachable only while it is up; both have real, directly observed table positions (`HitTarget.sw85`, `HitTarget.sw86`).

## Other toys, kickers, and standard devices

Solenoid 2 (`SolBride`) raises and lowers a post (`BrideH`) near the top lanes; solenoid 3 (`SolMummy`) opens and closes the mummy coffin lid (`Mumcoffin`); neither toy has a dedicated printed switch, and both are driven purely as scored callbacks. Solenoid 8 (`SolLockPost`) raises a post (`LockP`) that locks a ball at the right ramp, sensed by right-ramp-lock switch 73. Two solenoid-operated one-way gates (solenoid 5 `LGate`, solenoid 6 `RGate`) admit a ball into a loop or lane while blocking return travel.

A ball resting on switch 28 (Left Eject) is kicked back by solenoid 15; a ball resting on opto 36 (Right Popper) is kicked back by solenoid 16. Two slingshots (coils 10/11, score switches 51/52) and three A-12030-3 jet bumpers (coils 12/13/14, skirt switches 53/54/55) are standard WPC devices; the retained script's `LeftSlingShot_Slingshot`/`RightSlingShot_Slingshot` and `Bumper1_Hit`/`Bumper2_Hit`/`Bumper3_Hit` handlers pulse the matching matrix addresses and fire the matching coils in the same event.

## Fliptronic column: flippers, center spinner, and eddy-current sensors

Two FL-11629 flippers on Fliptronic circuits 111-114 (lower right/left, EOS then button-opto). There are no upper flippers: positions 115 (EOS) and 116/118 (button-optos) are printed Not Used on the switch-locations parts list. 116 and 118 are nonetheless shaded as optos on the reused wiring-diagram template (the same Flipper Opto PCB Assembly A-17316 construction as the fitted 112/114), so their printed construction -- including `normally_closed = true` -- is preserved even though `availability` is `unused`; 115's template position is drawn as a plain leaf and carries no such printed opto construction.

Fliptronic F7 (public switch 117) is repurposed as the Center Spinner rather than an upper-left flipper position; the switch-locations parts list names it directly, and the retained script's `Spinner1_spin` handler (`vpmTimer.PulseSw 117`) confirms it independently. Flipper proximity sensors 47/48 are eddy-current sensors on two A-22149-1 Auto Adjust Eddy Sensor PCB assemblies (TDA0161 proximity IC with an auto-adjusting eddy controller and dual digital potentiometer), not mechanical switches; the retained script's own comment separates them from the opto pair 42/43 with `' Opto & proximity switches`.

## Lamps, flashers, and general illumination

All lamp-matrix addresses are populated except 78 (Not Used). Four addresses drive two bulbs each -- 12 "Half Moon", 24 "Full Moon Fever", 31 "Quarter Moon", and 43 "Three-Quarter Moon" -- and the retained table binds both bulbs of each pair (`l12`/`l12c`, `l24`/`l24c`, `l31`/`l31c`, `l43`/`l43c`), so each has two placements. Several single-bulb addresses (11, 57, 61-66, 81-86) have a second co-located Light object stacked purely for brightness at an offset under one bulb diameter; the primary object is used and the duplicate is documented render doubling, matching the manual's single-bulb parts entries. Lamps 87 and 88 are the bulbs inside the illuminated Launch and Start buttons and are cabinet hardware.

The lamp-matrix page (2-52) carries four typographic slips against the authoritative parts list (2-44): "DRAC-ATTTACK" for Drac-Attack (14), "QUARTER MOOM (2)" for Quarter Moon (31), "THREE-QUARTERS MOON (2)" for Three-Quarter Moon (43), and "LEFT GARGOYLE" for Left Gargle (48). The last deserves the explicit note: the paired right-hand insert at 25 reads "RIGHT GARGLE" on both pages, and the Bride of Frankenstein insert trio is PRIMP / WARM UP / GARGLE (46/47/48 left, 27/26/25 right), so "GARGOYLE" is the slip and the parts-list label is canonical here.

Flashers 18-26 (excluding 17) each drive at least one playfield bulb; only the playfield bulb(s) receive a coordinate, and back-panel/insert-panel bulbs stay uncoordinated backbox hardware. Address 17 (Wolfman Flashers) is the one flasher circuit with **zero** playfield bulbs -- both fitted lamps are on the back panel (2) and the insert panel (1) -- so it takes a `cabinet_or_service` spatial record with role `cabinet.insert-panel` rather than a location. The retained table's flasher render-doubling and centroid-helper objects (`f20a`, `f21c`, `f22c`) are excluded from placement, matching the project's established policy of never presenting a render helper as a physical socket.

General illumination splits three ways on the retained script's `UpdateGi` dispatch: GI address 0 drives collection `GIBot` (35 members); GI address 1 drives `GITopRight` (26) plus `GIBumpers` (13); GI address 2 drives `GITopLeft` (15). The manual prints no per-string bulb count, so physical quantity and every emitter coordinate come from these collections. One `GIBot` member, `light11`, sits at normalized x=1.087804 -- outside the retained table's 0..1 playfield bounds -- and is excluded here as a table modeling anomaly rather than a distinct physical bulb, leaving GI address 0 with 34 placements instead of 35. GI addresses 3 and 4 are backbox insert-panel strings with no playfield emitter; address 4 additionally feeds cabinet bulbs through J104, the only cabinet connection on the printed general-illumination wiring page.

## Solenoid 7 and the knocker: recorded disagreement

Printed solenoid-table addresses 04 and 07 both show a populated power-driver transistor (Q67, Q69) with no voltage connection and no drive connection in any playfield, insert, or cabinet column, so neither has a fitted coil, flasher, flipper, or motor. Pinned PinMAME's `*** PRELIMINARY ***` `mb.c` defines `#define sKnocker 7`, consumed only by its preliminary ball simulator; the retained known-working VPW script sets `SolCallback(7) = "solKnocker"` and plays a knocker sound. These are reconcilable rather than contradictory: the WPC-95 operating system uses driver 7 as its standard knocker output and the ROM pulses it, but this physical machine ships with no knocker coil on that circuit. All three sources are cited on the address and no physical knocker device is claimed anywhere in this definition.

## Author construction checklist

- Build the four-ball trough with the drain at Trough Ball 4, the auto-plunger shooter lane, both slingshots, three jet bumpers, both ball gates, the mummy coffin, the bride post, the ramp lock post, the left eject and right popper kickers, the rotating Dracula figure with its target ring, the motorized Frankenstein figure with its hit wall, and the motorized Up/Down target bank.
- Preserve opto polarity for 31-36 and 42/43; do not invert what PinMAME already normalizes. Switches 74-78 are also printed normally-closed optos, but PinMAME does not normalize them and its own mechanism table implies the opposite sense -- treat their polarity as unresolved (`conflict.dracula-position-opto-not-normalized`) rather than assuming either convention.
- Treat LPDC outputs 37/38 and their PinMAME mirrors 41/42 as one physical two-direction H-bridge motor, not two or four devices.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the printed Not Used positions, Fliptronic 111-118 with 115/116/118 explicitly not installed and 117 repurposed as the Center Spinner, the eight CPU DIP bits, solenoids 1-50, lamps 11-88, GI 0-4, and the 128x32 DMD.
- Do not label public solenoid 7 a knocker; this machine has no fitted knocker coil despite the WPC-95 platform default.

## Sources

- `manual.williams.monster-bash.1998`: Williams Monster Bash operations manual, SHA-256 `8db31b4ac4a116a5a4ca83a456e291ad9bcecdec891ff08e4d3b4eb92df9e7aa`.
- `manual-support.williams.monster-bash.1998`: retained human transcription, SHA-256 `a5d8d4a1936fe379ed855227a1d73d3a26d95438f75e0c60f3b11e1080d84bfc`.
- `vpx-script.mb-vpw-1-0`: retained known-working VPW Mod v1.0 embedded script, SHA-256 `b043d07c74693ce5c713a9edc1529413f3c2ec4420b63488085cd45e4fe413e8`, binding `mb_106b`.
- `vpx-table.mb-vpw-1-0`: retained table, SHA-256 `bef48b75b072c3fc8b4803639cc65f54144db6ff7e9476f6ea6b1fc23bc68c8d`, bounds `left=0 top=0 right=952 bottom=2162`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/prelim/mb.c` and the WPC-95 core/solenoid/flipper handling at the pinned revision.
