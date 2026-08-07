# Bram Stoker's Dracula (Williams, 1993)

Coverage: **partial** — every dimension is validated except one lamp with no resolvable
spatial evidence (lamp 53, Magnet) and one unresolved wiring-provenance conflict
(`conflict.upper-flipper-circuit-side-naming`). See
`reports/spatial/williams/bram-stoker-s-dracula-1993.md` for the full audit.

## Overview

Bram Stoker's Dracula is a Williams WPC-Fliptronic machine (`GEN_WPCFLIPTRON`,
`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`), designed around the 1992 Francis Ford Coppola
film. The physical family is the five-driver `drac_*` clone tree: `drac_l1` (production
parent, and the driver the retained known-working script binds directly via
`Const cGameName = "drac_l1"`), `drac_d1` (D-1 LED Ghost Fix), `drac_l2c` (2016 community
Competition MOD), and two prototype revisions `drac_p11`/`drac_p12`. All five share one
static `dracGameData` struct, so all five are physically identical.

This is the fourth WPC-Fliptronic game curated in this project (after Bally Twilight
Zone, Bally The Addams Family, and — via the WPC-DCS variant — Williams Indiana Jones and
Williams Star Trek: The Next Generation), reusing `controllers/pinmame/wpc-fliptronic.json`
unchanged. Its switch-matrix opto sweep found **zero disagreement** with pinned PinMAME
across all three affected columns (5, 7, and 8) — the cleanest sweep result of any
Fliptronic-generation game curated so far, matching the clean-sweep precedent already set
by Bally Kiss, Bally The Addams Family, and Williams Star Trek: The Next Generation.

## Physical devices

Switch, lamp/GI, and controlled-device records are in the adjacent machine definition
(`machines/partial/williams/bram-stoker-s-dracula-1993.json`). The full manual
transcription is retained at `external:pinmame-review-artifacts/dracula/manual-
transcription.md`, and per-table excerpts are committed at
`evidence/excerpts/williams.bram-stoker-s-dracula.1993/`.

### Switch matrix opto identity

Unlike most other curated WPC manuals, this one marks opto construction by writing
"Opto ___" directly into the printed switch-matrix cell rather than shading. Column 5's
seven "Opto ___" cells (51-57) and column 7's three "Opto ___" cells (71-73) match
pinned PinMAME's inverted-switch mask exactly (`0x7f` and `0x07` respectively). Column
8's single opto (switch 82, "Ball On Magnet") cannot be determined from the matrix page
at all — none of 81/82/83 is labelled "Opto" there — and is only resolvable from the
Switch Locations parts list, where 82 alone carries genuine A-14315(LED)+A-14316(Trans)
construction while 81 and 83 use the ordinary leaf part 5647-12693-14. This again matches
PinMAME's mask (`0x02`, row 2 only) exactly. Zero disagreement anywhere in the matrix.

### No physical upper flippers

Three independent sources converge on "no upper flippers fitted": the Switch Locations
parts list has no row at all for Fliptronic positions F5-F8 (unlike F1-F4, which each
carry a real part number); the Solenoid/Flasher Table lists only two flipper-coil rows
("Lower Left Flipper", "Lower Right Flipper" — no "Upper" row at all); and the retained
known-working script never references public switches 115-118 anywhere. The generic
Fliptronic II circuit-diagram pages (3-17 through 3-21) still print all eight F1-F8
positions descriptively and pinned PinMAME's own `dracGameData` sets
`FLIP_SW(FLIP_L | FLIP_U)` (reading both lower and upper button state) despite
`FLIP_SOL(FLIP_L)` (declaring only lower-flipper coils) — the same "board reads upper
positions with no upper coil ever installed" pattern already established for Monster
Bash's `mbGameData`. This is a known WPC-Fliptronic driver characteristic, not evidence of
real upper-flipper hardware.

### Repurposed upper-flipper circuits

Because there are no upper-flipper coils, solenoids 33-36 (the printed upper-flipper
power/hold driver-transistor pairs) are repurposed for four unrelated devices: 33
Up/Down Post Diverter, 34 Right Gate, 35 Castle Release Post, 36 Left Gate Actuator — the
same pattern already established for Indiana Jones's printed circuits 33-36 (right-ramp
diverter and Top Lockup post) and Monster Bash's repurposed Fliptronic switch position.
Pinned PinMAME's own `src/wpc/core.h` macros (`sURFlipPow`/`sURFlip` = 33/34,
`sULFlipPow`/`sULFlip` = 35/36) call 33/34 the upper-**right** circuit and 35/36 the
upper-**left** circuit, while this manual's own Solenoid/Flasher Table prints the
opposite ("Up Lt. F." at 33/34, "Up Rt. F." at 35/36) — a genuine, unresolved
left/right-naming disagreement recorded as `conflict.upper-flipper-circuit-side-naming`,
in the same family as Attack From Mars's afm.c loop-gate naming defect. It does not
affect any device's function or address, both of which are taken from the manual's
function column directly.

## Custom mechanisms

### Mist Magnet ball-levitation carriage

The headline mechanism. A single electromagnet (solenoid 27, "Magnet") is mounted on a
motor-driven carriage (solenoid 28, "Magnet's Motor") that travels diagonally beneath
the playfield between a right-side entry near the Right Gate and a left-side exit near
the Left Gate. The retained script tracks the carriage's position purely in software: a
0-500 counter (`MagnetPos`) increments or decrements by 0.4 per tick while solenoid 28 is
energized, reversing direction at each endpoint (`MagnetDir`), and the carriage's visible
(x, y) is recomputed every tick as a straight-line interpolation between two fixed
endpoints (raw table coordinates (850, 885) and (126, 1220)). The carriage therefore has
no single resting coordinate; it is a documented projection onto the fixed detection-zone
`Trigger.Magnet` object (raw (390, 1000)) rather than either transient endpoint.

Three switches report the mechanism's state, and only one of them is a true opto:

- **Switch 82 (Ball On Magnet, opto)**: the retained script's `MistTimer_Timer` tests
  every ball in the trigger's collision region against a fixed diagonal line equation
  representing the physical light beam, independent of carriage position. This is the
  only genuinely opto-constructed magnet-area switch (A-14315/A-14316), and it is the
  only one PinMAME's inverted-switch mask normalizes.
- **Switch 81 (Magnet Left, plain leaf, part 5647-12693-14)**: asserts when
  `MagnetPos > 490`, i.e. the carriage is near its left/exit end (raw x ≈ 126), which
  feeds the Left Gate.
- **Switch 83 (Magnet Right, plain leaf, same part)**: asserts when `MagnetPos < 10`,
  i.e. the carriage is near its right/entry end (raw x ≈ 850), which feeds the Right
  Gate.

The driver's own `stMagnet` ball-state case requires the magnet to be both energized
(`core_getSol(sMagnet)`) and at the matching endpoint switch/position before releasing
the ball toward the corresponding gate — an explicit causal link between the magnet coil,
the motor position, and the two endpoint limit switches, not merely proximity.

Thirteen "mist lights" (`ml1`-`ml13`) are script-only position-indicator lamps driven
directly from `MagnetPos \ 33` in `MotorTimer_Timer`. They have no PinMAME public
address and are not modeled as controller-facing lamp devices; they are pure VPX visual
convenience, the same caveat this project's evidence-authority rules ask for when a
retained table adds effects the ROM never drives.

### Castle Lock lane and release post

A three-position lock lane behind the Left Ramp diverter queues balls on three genuine
opto switches: 57 (Castle Lock 3, entry, nearest the diverter), 54 (Castle Lock 2), and
53 (Castle Lock 1, exit, nearest the release post). Solenoid 35 (Castle Release Post,
printed "Dis. Castle Release Pst", wired through the otherwise-unused upper-flipper power
driver transistor) retracts the post (`clpost.isdropped = 0`) to release the ball queued
at position 53 toward the shooter lane; the retained script's `clpost_Timer` sub restores
the post 280 ms later. The driver's own ball-state chain (`L. Ramp Div.` → `Castle Lock 3`
→ `Castle Lock 2` → `Castle Lock 1`, exit output `sCastleRelease`) confirms balls queue in
that order and release one at a time from the position nearest the post.

### Left and Right Mist Magnet entry gates

One-way gates admit a ball onto the Mist Magnet carriage from either side. Solenoid 34
(Right Gate, wired through the other otherwise-unused upper-flipper power driver
transistor) opens a gate near the top-right loop (`RGate.open = 1`, plus dropping
`RGateWall`) so a ball can fall onto the carriage from the right; solenoid 36 (Left Gate
Actuator) opens a gate near the Magnet Left Pocket opto (switch 52) admitting a ball from
the left (`LGate.open = 1`, plus dropping `Wall_LO`). The driver's own ball-state chain
independently confirms both paths lead to `stMagnet`.

### Moving Right Ramp / Coffin Ramp section

A section of the Right Ramp raises and lowers to route the ball either up the ramp toward
the Coffin Popper or over a hump back into general play. Solenoid 14 (Right Ramp Up)
raises it, disables the ramp's own collision (letting the ball pass up and over), and sets
the retained script's `Controller.Switch(77) = True`; solenoid 4 (Right Ramp Down) does
the reverse. The Switch Locations parts list prints a real part number for switch 77
(5647-12693-36), but the retained script sets its public state directly from the solenoid
commands rather than reading a discrete position sensor — an implementation
simplification worth noting, not a source disagreement (all three sources agree the
switch and the solenoid-driven mechanism both genuinely exist).

### Shooter Ramp entry diverter

A small flap near the auto-plunger lane (solenoid 8, Shooter Ramp Entry) diverts the
auto-launched ball either up a habitrail loop toward the right side of the playfield
(solenoid energized, `sramp2.Collidable = 0`, `FLRamp.rotatetoend`) or lets it fall
through toward the Left Loop (solenoid off), per the driver's own `stBallLane` ball-state
case. No discrete switch reports this flap's position; the driver infers the routing
purely from the current solenoid state.

### Up/Down Post Diverter

A spring-loaded post near the top of the playfield (solenoid 33, printed "Up/Dn Post
Diverter", wired through the otherwise-unused upper-flipper power driver transistor)
toggles the ball between two orbit/ramp paths (`wDivert.isdropped`, `FDivert.rotate`).
Left Ramp Entry (opto switch 73) senses a ball entering the diverted path.

### Single Left Drop Target

A single drop target — **not a bank** — sits near the top-left rollover lanes. Hitting it
drops the target (switch 15, L. Drop Target) and reveals a rollover behind it (switch 16,
L. Drop Score) that scores the ball's passage; solenoid 25 (L. Drop Target Reset) raises
it again after a delay via the retained script's `SolDTUp` callback. This corrects an
earlier candidate description of a "3-bank drop target" at this address: the retained
script instantiates exactly one `DropTarget` class object (`DT15`, `Set DT15 = (new
DropTarget)(sw15, sw15a, BM_sw15, 15, 0, false)`) for switch 15. The genuine 3-bank
standup-target arrays on this machine are the unrelated Left 3-bank (switches 66/67/68)
and Middle 3-bank (switches 86/87/88) banks, both plain standup targets with no drop
mechanism at all.

## Lamp chases

Seven lamps spell the machine's own name letter by letter: 48(D), 36(R), 23(A), 71(C),
67(U), 72(L), 82(A), in address order 48→36→23→71→67→72→82. Five more
(31-35) spell VIDEO in already-ascending address order, illuminating the "R. Lane" video
mode qualifier lamps in sequence.

## Backbox and cabinet devices

Four lamps (58 L. Ramp Diverted, 61 L. Skill 100K, 62 M. Skill 1 Million, 63 R. Skill)
are drawn only inside the manual's separate "A-16399 Back Panel Assy." box, above the
main playfield diagram — the retained table corroborates this independently (all four
normalize to y < 0.011, sitting right at the playfield's rear edge rather than a genuine
mid-playfield position). Lamp 63 additionally carries an internal manual disagreement:
the Lamp Matrix wiring page prints "R. Skill 100K" while the Lamp Locations parts list
prints "R Skill 500K" for the same address — a cosmetic scoring-legend discrepancy with
no bearing on wiring, polarity, or placement, transcribed verbatim from both pages.

GI strings 3 and 4 are backbox-only circuits (string 4 additionally reaches a cabinet
bulb through J119) with no playfield voltage or drive connection printed anywhere,
matching the retained script's `GIUpdate2`, which drives a single non-playfield bulb
(`gibg4`/`gibg5`) for each rather than a playfield light collection. GI strings 0-2 (Lower/
Upper/Center Playfield) drive the retained table's `GIBOT`/`GITOP`/`GIMID` collections
exactly, with zero script-vs-manual disagreement — unlike Williams Tales of the Arabian
Nights or Bally Theatre of Magic, both of which found a genuine GI script-vs-manual
conflict.

## Unresolved questions

- Lamp 53 (Magnet, #44) is a genuine bulb per the Lamp Locations parts list, but has no
  matching `Light` object in the retained extraction and no reference anywhere in
  `script.vbs`. Resolving its position needs either a different retained table that does
  model it, or a playfield photograph/insert map.
- `conflict.upper-flipper-circuit-side-naming`: pinned PinMAME's own macro naming and
  this manual's printed circuit-side label disagree about which upper-flipper driver-
  transistor pair (33/34 vs 35/36) is nominally "right" versus "left." Resolving it would
  need either a WPC-Fliptronic schematic sheet that traces the physical driver-board
  silkscreen, or acceptance that the naming is cosmetic and immaterial once the real
  device functions are known (which this definition already treats it as, while still
  recording the disagreement).

## Sources

- `manual.williams.bram-stoker-s-dracula.1993`: `Dracula_Bram_Stoker_OPS.pdf`, the
  Williams operations manual, SHA-256
  `de6840bb83a98333ef96a2781e3170103e5856380e9c46aad237974fc028498a`.
- `manual-support.williams.bram-stoker-s-dracula.1993`: retained human transcription,
  `external:pinmame-review-artifacts/dracula/manual-transcription.md`.
- `vpx-table.drac-vpw-1-0` / `vpx-script.drac-vpw-1-0`: the retained known-working VPW
  1.0 table and its embedded script, SHA-256
  `e291eb0ab61eb8940aba6f54d16efd512d4565cbb6af29fcae5530035de7575e` and
  `32f4f0ed85702cc015563eb262ea6c5b7cb7c90f6d30fa6b73c36f3c37c42c5f`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/drac.c` at the pinned PinMAME
  revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`.
- `ipdb.williams.bram-stoker-s-dracula.1993`: IPDB machine number 3072.
