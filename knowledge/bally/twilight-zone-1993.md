# Twilight Zone (Bally, 1993)

Coverage: **partial - complete physical I/O inventory, WPC-Fliptronic bindings, mechanism causality, 32-driver variant boundary, and recreation behavior validated; semantic naming conflicted pending resolution of the clock-motor forward/reverse naming conflict below, and a small number of switches/one GI string have no validated spatial placement**

## Identity and evidence precedence

This is the Bally physical product released April 1993, IPDB 2358. It covers the `tz_*` clone tree rooted at `tz_92`: 32 driver rows spanning Bally production revisions (9.2 through L-5, H-7/H-8, I-7/I-8, D-1 through D-4, IFPA tournament revisions, the LA-9 PAPA tournament build, five prototype revisions P-3/P-3D/P-4/P-5/PA-1/PA-2) and seven FreeWPC community-firmware revisions. Every one of these is a firmware revision for the same physical machine; none is a virtual-only or unrelated driver.

Evidence precedence for this definition: the retained known-working VPX script ("Twilight Zone (Bally 1993) 2.4.5.vpx", by Skitso, based on Ninuzzu's original) is runtime and mechanism-causality ground truth; the Bally operations manual (16-50020-101) controls physical construction, part numbers, polarity, quantities, and device presence; pinned PinMAME controls controller generation, public address topology, and mechanism-table position ranges; the retained VPX geometry supplies normalized coordinates. The retained manual PDF is an image-only scan, so every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md`.

**Retained-scan limitation.** This particular scan is missing every even printed page from 2-48 through 2-54 inclusive: the Switch Matrix wiring page (2-50, which also carries the first half of the Switch Locations table, items 1-33: dedicated switches 1-8 and matrix 11-33), the Solenoid/Flasher Table wiring page (2-52), and the Lamp Matrix wiring page (2-54) are all absent. No wire color or connector/pin assignment is asserted for any device in this definition. Switches below address 34 are sourced from pinned PinMAME's `tz.c` `#define` list and its inverted-switch mask alone, without a printed manual cross-check.

## Controller platform and address topology

`GEN_WPCFLIPTRON` (`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`, pinned PinMAME's own comment: "Fliptronic flippers, Addams Family 2/92 - Twilight Zone 5/93") with `wpc_dispDMD`. The controller profile is the new `pinmame.wpc-fliptronic`, introduced by this definition for every later pre-WPC-95 Fliptronic-generation game to reuse.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, one optional custom switch column at 91-98 (`CORE_CUSTSWCOL`, here the eight clock-position optos), Fliptronic 111-118. Twilight Zone genuinely has **four** flippers (`FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U)`), confirmed by the manual's printed "Flipper Coils" list (FL-15411 orange lower left/right, FL-11753 yellow upper left, FL-11722 green upper right) -- unlike Monster Bash, the upper Fliptronic circuits here are real hardware, not repurposed.
- Solenoids: standard drivers 1-16 fitted (10-14 handled by native VPX slingshot/bumper physics, not scripted), 17-20 flashers, 21/23-27 magnets/motor/diverter (22 not fitted), 28 flasher, Fliptronic upper-flipper circuits 33-36, Fliptronic lower-flipper circuits 45-48, custom board outputs 51-58 (five flashers 51-55 plus the clock motor pair 56/57 and clock strobe 58), and a software-only fake gumball-release state at 59. PinMAME state channels 29-32; simulator-only 49 and reserved 50.
- Lamps: full 8x8 matrix 11-88, every position fitted (no gaps).
- GI: five strings on public addresses 0-4.

**This generation has no LPDC board.** Unlike WPC-95, addresses 37-44 are not a duplicated general-purpose output range here: pinned PinMAME's `core_getSol` dispatch only serves that branch for `GEN_WPC95`/`GEN_WPC95DCS`/`GEN_ALLS11`, and Twilight Zone's own `tz_getSol` hook does not claim any part of it either, so 37-44 are simply unused address space on this machine. The manual's printed auxiliary-board callout numbers 37-44 for the custom solenoid board are a *different* numbering scheme from the public PinMAME address space for the same physical outputs -- see below.

**Printed auxiliary-board item numbers are not public addresses.** The manual's Solenoid/Flasher Locations page numbers the custom board's outputs 37-44 (matching the board's own silkscreen), but PinMAME publishes the same eight physical outputs at 51-58. The retained script's own comments bridge the two schemes explicitly: `SolModCallback(51)` through `(55)` are annotated `'(37)` through `'(41)`, and the commented-out clock lines read `'(42) Clock Reverse'`, `'(43) Clock Forward'`, `'(44) Clock Switch Strobe'` against `SolCallback(56)`/`(57)`/`(58)`. The printed number is preserved as a `manual.address` alias on each device; the binding uses the true public address.

## Ball path, trough, and shooter

Twilight Zone has no manual plunger. A ball drains through the Outhole (18) into the trough, walking Far Left Trough (25) -> Left Trough (17) -> Center Trough (16) -> Right Trough (15) at the eject end. Solenoid 9 (Ball Release) ejects the ball on switch 15 into the shooter lane, where it rests on Auto-Fire Kicker opto 72; solenoid 3 fires it onto the playfield. Switch 26 (Trough Proximity) detects the Powerball by type rather than presence, set directly by `tz_handleBallState`'s ball-type check rather than a Hit event, so it has no bound VPX playfield object and no spatial placement here.

## Gumball machine

A ball diverted by solenoid 6 (Gumball Diverter) enters the gumball lane (switch 51, Gumball Popper Lane) and is caught by the Gumball Popper opto (switch 74), which solenoid 4 kicks into the gumball wheel. A real gumball then enters the delivery chute (switch 87, Gumball Enter opto) and travels to the exit (switch 56, Gumball Exit) where the player receives it. Solenoid 24 turns the internal gumball motor. Switch 55 (Gumball Geneva) senses the motor's geneva-gear position, but pinned PinMAME's `tz_handleMech` derives it synthetically from an internal position counter (`locals.gumPos`) rather than reading a physical Hit event, and no VPX trigger object binds it in the retained extraction -- it is documented here without a spatial placement rather than invented. `tz_getSol` also exposes a fake `CORE_CUSTSOLNO(9)` "gumball release" state (public 59) used only to simplify emulator-side sequencing; the retained script comments it out as "unreliable with SolModCallbacks", so it is declared `virtual`, not a real coil.

## Clock mechanism and the forward/reverse naming conflict

A bidirectional DC gearmotor (A-16120 D.C. Motor Control Assembly) drives a physical analog clock hand through solenoids 56/57 as a forward/reverse pair, strobed by solenoid 58 (A-16100, Clock Switch Strobe). Eight opto sensors report hand position: Minute board (A-16220) at 91-94, Hour board (A-16219) at 95-98; both boards are in PinMAME's fully-inverted custom switch column.

Pinned PinMAME does not expose the clock to the table script at all. `init_tz`'s `mech_add(0, &mechClock)` drives an internal `MECH_TWODIRSOL` simulation with its own switch/step-range table (`mechClock`), but the code that would translate motor position into switch state is wrapped in an `#if 0` block inside `tz_handleMech` in this pinned revision, so the mechanism's step table is defined but currently inert; the retained script instead reads the resulting position directly through `Controller.GetMech(0)`.

**Unresolved conflict (`conflict.clock-motor-direction-naming`).** Pinned PinMAME's `tz.c` names public solenoid 56 `sClockFwd` and public solenoid 57 `sClockRev` -- i.e. 56 = Forward, 57 = Reverse. Two independent sources disagree with PinMAME and agree with *each other*: the printed manual's Solenoid/Flasher Locations page reads item 42 (= public 56) "Clock Reverse" and item 43 (= public 57) "Clock Forward" -- the opposite direction -- and the retained script's own commented-out cross-reference lines read the same way (`'(42) Clock Reverse'` against `SolCallback(56)`, `'(43) Clock Forward'` against `SolCallback(57)`). Neither solenoid is exercised at runtime by the retained script (the `#if 0` block above means the clock motor never actually turns in this configuration), so there is no runtime observation available to break the tie between pinned PinMAME's internal variable name and the two independently-agreeing external sources. This keeps `semantic_naming` conflicted and the record `partial`. Resolving it needs a LibPinMAME harness trace driving solenoids 56/57 individually against a legal ROM while observing which direction a real or simulated clock hand moves, or the missing D.C. Motor Control Assembly schematic page.

## Magnets

Three eddy-current magnets: Left Magnet (solenoid 21, switch 83), Lower Right Magnet (solenoid 23, switch 81), and Upper Right Magnet (solenoid 22, switch 82). The third magnet is **not fitted** on this physical machine: both its solenoid and switch print "Not Used" with no part number at all in the manual, the strongest "not fitted" signature the manual uses anywhere. The retained script's own comment on the ROM's `SolUpperRightMagnet` callback reads `(*) only in prototype, supported by rom 9.4` -- the ROM can drive a third magnet, but no manual/schematic evidence of a production variant that actually carries it was found. `tz_inportData`'s "Third Magnet" toggle belongs to PinMAME's own internal text-mode ball-tracking simulator (`sim.c`), not a documented physical DIP option, and must not be read as evidence of a fitted variant.

## Mini-playfield

A raised second playfield reached through the Mini-Playfield Enter opto (switch 44). Two eddy-current magnets (solenoid 25 Left, solenoid 26 Right) manipulate the ball around the Camera/Mini-Playfield Top Hole (switch 42 -- the retained script's own comment calls it "camera / upper playfield", and the manual's plain label is preferred here as the physical construction authority), the Player Piano standup target (switch 43), and the Mini-Playfield Top/Exit optos (switches 75/76). Switches 45/46 (Mini-Playfield Left/Right) have named `sw45_Hit`/`sw45a_Hit`/`sw46_Hit`/`sw46a_Hit` subs in the retained script, but no gameitem, collection, or object binding for those exact names exists anywhere in the retained extraction (`gameitems.json`, `collections.json`), so their causal detail beyond the manual's plain label is unconfirmed and they carry no spatial placement.

## Three-position ball lock

Lower (switch 88, plain switch part), Center (switch 84, opto), and Upper (switch 85, opto) lock positions; solenoid 15 (Lock Release) kicks locked balls back into play.

## Slot machine, jet bumpers, and slingshots

A ball entering the slot machine crosses proximity switch 57 (underside of the playfield) and rests on kickout opto 58; solenoid 1 returns it to play. Three A-9415-2 jet bumpers (Lower/Left/Right, switches 31/32/33, solenoids 12/13/14) and two slingshots (Left/Right, switches 34/35, solenoids 11/10) are all handled by native VPX physics in the retained script rather than scripted `SolCallback` entries. The retained extraction's three `Bumper1`/`Bumper2`/`Bumper3` objects are generically named with no explicit per-object binding to a specific public switch address, so no spatial placement is asserted for switches 31-33 rather than guessing an assignment from relative position.

**A printed label correction.** `tz.c` unambiguously defines `#define swLSling 34` and `#define swRSling 35` (34 = Left, 35 = Right); the legacy migrated stub this definition replaces had these reversed. The manual's own Switch Locations page (item 34 = "Left Slingshot", item 35 = "Right Slingshot") and the retained table's `Wall.LeftSlingShot`/`Wall.RightSlingShot` geometry (x=0.296 and x=0.676 respectively, x=0 being the left edge) both independently confirm `tz.c` is correct.

## Flippers

Two lower Fliptronic flippers (FL-15411 orange, solenoids 45-48) and two genuine upper Fliptronic flippers (FL-11753 yellow upper-left solenoids 35/36, FL-11722 green upper-right solenoids 33/34), confirmed by the manual's printed Flipper Coils list. `Const UseSolenoids = 2` in the retained script means the ROM drives the coils directly (fast flips). `WPC_FLIPPERS` unconditionally complements the flipper switch column for this hardware generation exactly as `WPC_FLIPPERSW95` does for WPC-95, so the public state of 111-118 is already normalized.

## Driver variants

All 32 catalog rows trace `tz_92` and share `tzGameData`; none is virtual-only. `tz_94ch`/`tz_94h` are the pair the retained script's `cGameName` selects between (Romset 0/1); `tz_l2` is the revision both retained VPX script corpora (`vpxtable_scripts` and `vpx-standalone-scripts`) independently target. FreeWPC revisions `tz_f10` through `tz_f100` are community firmware for the same physical hardware. No edition/family split applies -- Twilight Zone shipped as a single physical configuration, not Pro/Premium/LE variants.

## Promotion decision

Identity, controller platform, address enumeration, mechanism inventory/behavior, variant coverage, and recreation knowledge are complete. Promotion to `author_ready` is refused for two reasons: `conflict.clock-motor-direction-naming` is a genuine, unresolved disagreement between pinned PinMAME's internal `#define` names and two independently-agreeing external sources, and switches 26, 31-33, 45, 46, 55, and GI address 2 have no validated playfield placement because no bound VPX object exists for them in the retained extraction (or, for GI address 2, the bound object's raw coordinate falls outside the playfield bounds). See `reports/spatial/bally/twilight-zone-1993.md` for the complete spatial audit.
