# Junk Yard (Williams, 1996)

## Identity and evidence precedence

Junk Yard is a Williams WPC-95 machine (manual 16-50052-101, JANUARY 1997
FINAL). Pinned PinMAME's own `libpinmame.h` names the `GEN_WPC95` constant
"Integrated boards, Congo 3/96 - Cactus Canyon 2/99", i.e. Junk Yard is part
of the same integrated-board WPC-95 hardware generation as the other machines
in that era. The retained known-working table (VPX v1.3, author mfuegemann;
primitives/textures by Fuzzel and Dark, lighting by Hauntfreaks) binds driver
`jy_12`, the production 1.2 ROM (DCS sound).

This curation follows the project's standard evidence-authority order: the
retained script is runtime/causality ground truth, the Williams manual is
physical-construction/wiring/quantity ground truth, pinned PinMAME source is
controller-topology ground truth, and the retained table supplies geometry.
The retained manual (146 pages) carries a usable OCR text layer, but every
printed table cited here was read from 200 dpi renders and transcribed by a
vision-capable model worker into
`evidence/excerpts/williams.junkyard.1996/`, cross-checked across the repeated
copies (front matter, printed 2-38, and Section 3). **These transcriptions are
recorded with `reviewed: false` / `method: model`** — a vision-capable curator
has not yet visually re-checked them against the rendered pages. The
polarity, spatial, controller-topology, and mechanism-causality conclusions
rest on pinned PinMAME source, the retained VPX geometry/script, and the
cross-copy comparison rather than on the unchecked transcription alone; the
manual-derived device labels are therefore candidate until a curator
re-verifies the excerpt transcriptions.

**Junk Yard has no pop bumpers.** Unlike most WPC-95 machines, neither the
switch matrix nor the solenoid table lists a jet/popper bumper; the playfield
features standup targets, slingshots, a crane with a wrecking ball, a
refrigerator popper, a fork-lift scoop, a dog-house mechanism, and a spinner.

## Controller platform and address topology

Reuses `controllers/pinmame/wpc-95.json` unchanged, confirmed directly from
`jyGameData`'s own `GEN_WPC95` field in `src/wpc/sims/wpc/prelim/jy.c`. The
switch matrix, Fliptronic column, LPDC duplication (37-40 mirrored at 41-44),
and five-string GI layout all follow the standard WPC-95 rules already
documented on that profile.

Junk Yard declares no custom switch column, no auxiliary lamp column, and no
custom solenoid board (`jyGameData`'s trailing `hw` fields are all zero), so
this is a clean WPC-95 baseline with no address-remapping surprises beyond
the flipper circuits below. The switch matrix's eighth column (81-88) is
entirely unpopulated; switches 23, 25, 55, and 75 are also printed Not Used.

**Flipper circuits.** Printed circuits 29/30 (Lwr Rt Power/Hold) and 31/32
(Lwr Lt Power/Hold) map to public addresses 45-48 (`CORE_FIRSTLFLIPSOL=45`).
Printed circuits 33-36 (the "Upr. Rt."/"Upr. Lt." driver-board slot,
`CORE_FIRSTUFLIPSOL=33`) already equal their own public addresses. Junk Yard
fits **no upper flippers**: `jyGameData` declares `FLIP_SOL(FLIP_L)` only, so
no upper flipper solenoid is CPU-driven and no upper `FLIP_EOS` bit is set.
The Switch Locations page marks F6/F7/F8 (Upper Right/Optos and Upper Left
E.O.S./Opto) Not Used.

The flipper-column switch treatment deserves precision because it depends on
PinMAME's `flipMask` construction (`core.c:2510-2517`), which is driven by
`jyGameData`'s `FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L)`. That mask always
carries the lower-right/left button bits and the lower EOS bits (from
`FLIP_SOL(FLIP_L)`), and additionally the upper-right/left **button** bits
(from `FLIP_SW(FLIP_U)`); it carries no upper EOS bit. The two addresses that
PinMAME genuinely **forces every VBLANK** regardless of keyboard mode are the
lower end-of-stroke contacts 111 and 113: `core_updateSw` recomputes them from
`core_getSol` (the flipper hold-coil state) plus `CORE_FLIPSTROKETIME`
(`core.c:1756-1775`) and writes them back, so **a recreation must not drive
111 or 113**. The button addresses 112/114/116/118 are read from and written
back to the matrix unchanged when keyboard handling is off
(`core.c:1731`, the LibPinMAME default `g_fHandleKeyboard=0`), so the emulator
publishes no meaningful runtime state at them; 116/118 are additionally
unfitted (no physical upper-flipper button exists) and are recorded `unused`,
while 117 (upper-left EOS) is dead because no upper `FLIP_EOS` bit is set.
F5, however, is **not** a flipper contact at all: the manual prints it
"SPINNER" (part 5647-12693-24), and the retained script's `Switch115_Spin`
handler pulses it as the playfield spinner. This is the same "Fliptronic F5
repurposed for a non-flipper device" pattern Monster Bash established with its
Center Spinner.

## Opto polarity sweep

The manual's Switch Locations parts list (2-35) identifies eleven
opto-constructed switches by printing an LED/photo-transistor pair on two
lines rather than a single mechanical part: 31-35 (A-18617-1/A-18618-1, the
trough) and 36-37, 41-44 (A-16908/A-16909, lock-up/sewer/scoop/crane optos).
The switch matrix (2-34) shades column 3 rows 1-7 as "OPTO, TYPICALLY CLOSED".

Pinned PinMAME's `jyGameData` inverted-switch mask
(`{0x00,0x00,0x00,0x7f,0x07,0x00,...}`) normalizes column 3 rows 1-7
(31-37) and column 4 rows 1-3 (41-43). That matches the manual on ten of the
eleven opto addresses. The single disagreement is **switch 44 (Past Crane)**:
opto-constructed per the manual but **not** normalized by PinMAME (column 4
row 4 is outside the mask's `0x07`). This is the same family of conflict as
Monster Bash's Dracula-position optos and Indiana Jones's captive-ball opto,
and is recorded as `conflict.junkyard.past-crane-opto-not-normalized`.

## Mechanisms

- **Four-ball trough and release** (A-19963-1): the retained script's
  `cvpmBallStack` helper `bsTrough` reads switches 32-35 as a plain switch
  array and ejects the ball through solenoid 9, pulsing opto 31 in the same
  `SolTrough` event.
- **Shooter lane and auto plunger** (A-21022): the `Autoplunger` handler pulls
  back and fires `Auto_Plunger` only when switch 18 is active.
- **Crane with wrecking ball** (A-21523): solenoid 3 (Power Crane) drives the
  arm, solenoid 15 (Hold Crane) holds it; switches 15 (Top Left Crane), 44
  (Past Crane), and 28 (Crane Down) report the head's positional limits.
- **Refrigerator popper** (A-21216): `bsFridgePopper` uses switch 37 as the
  entry and switches 36/43 as the internal ball-stack array; solenoid 2 ejects.
- **Bus ramp diverter** (A-21409-1): solenoid 6 rotates a diverter flap
  (`Sol6.IsDropped`) with no dedicated switch.
- **Spike the dog** (A-21383): solenoid 16 drives the dog-house spike arm;
  `SpikeBark`/`SpikeTimer` animate it while switch 74 reports a ball in the
  dog-house entry.
- **Fork-lift scoop** (A-21220): solenoid 5 (Scoop Down) and solenoid 21
  (Scoop Up) lower/raise the fork arms; switches 73 (Scoop Made) and 72 (state)
  report the scoop.
- **Car targets** (SW-1A-210): five **standup** targets at the top of the
  playfield (46-48, 53-54); there is no resettable drop mechanism.
- **Three-bank target clusters** (A-21349-1 / A-21351): four clusters of three
  **standup** targets (56-58, 61-63, 64-66, 76-78); no bank is solenoid-reset.
- **Slingshots** (B-9362-R-3): left (10/51) and right (11/52).
- **Spinner**: Fliptronic F5 (public 115).

## Service and setup

The front-matter DIP Switch Chart documents five country combinations
(America, European, French, German, Spain) across SW1-SW8. The machine uses
four balls. The crane mechanism and the wrecking ball are the headline
features, with the cars, refrigerator, dog-house, and fork-lift scoop forming
the themed toy complex.

## Unresolved

The past-crane opto polarity conflict (switch 44) is the one open polarity
question; a LibPinMAME gameplay-harness trace of the public idle state of
switch 44 on a legal `jy_11`/`jy_12` ROM is the concrete resolution path.
Several crane/trough/sewer mechanism-internal sensors are documented
projections onto the mechanism's real kicker rather than surveyed
coordinates.

## Sources

- Williams Junk Yard Operations Manual (16-50052-101, January 1997 FINAL),
  146 pages, SHA-256 `08819a08990c61070c4a3a99a4d5f00d9d082b6d00477ffaf9b0a58fddce3fe1`.
- Retained known-working table `Junk Yard (Williams 1996).vpx` v1.3 by
  mfuegemann, SHA-256 `8ff2c1c8ae3457a4b88ff2207bc506d07435b049343301ded4dbf8e855bef07f`.
- Pinned PinMAME `8371478a7640f1896dcdf565aed340dc5df989ba`,
  `src/wpc/sims/wpc/prelim/jy.c`.
