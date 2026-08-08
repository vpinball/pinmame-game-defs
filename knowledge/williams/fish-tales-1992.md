# Fish Tales (Williams, 1992)

Coverage: **partial - complete physical I/O inventory, WPC-Fliptronic bindings, mechanism causality,
driver-variant boundary, and normalized spatial placement validated; wiring conflicted pending
resolution of the two switch-polarity conflicts below; recreation knowledge is source-reconciled and complete**

## Identity and evidence precedence

This is the Williams WPC-Fliptronic physical product released August 1992, IPDB 861. It covers the
nine-driver `ft_*` clone tree: `ft_l5` (parent, production L-5), `ft_l5p` (L-5 text-size patch),
`ft_d5`/`ft_d6` (community LED Ghost Fix revisions), `ft_l3`/`ft_l4` (earlier firmware), and
`ft_p2`/`ft_p4`/`ft_p5` (prototypes). Every one of these shares the identical `ftGameData` struct and
is a firmware revision of the same physical machine. The retained known-working VPW 1.1 script binds
`ft_l5` directly (`Const cGameName = "ft_l5"`), the production parent, so no driver substitution note
is needed.

Evidence precedence for this definition: the retained known-working VPW 1.1 script is runtime and
mechanism-causality ground truth; the Williams operations manual controls physical construction, part
numbers, wiring, polarity, quantities, and device presence; pinned PinMAME controls controller
generation and public address topology; the retained VPX geometry supplies normalized coordinates.
This manual is OCR'd (Adobe Acrobat Paper Capture), but its multi-column tables are not reliable from
OCR text alone, so every printed table used here was read from a rendered page and transcribed into
`external:pinmame-review-artifacts/fish-tales/manual-transcription.md`.

`ft.c`'s own header comment is worth carrying forward as context for the whole file: its author writes
"I don't have access to this game, I guessed most of it from a Playfield picture and the rulesheet!"
and "I'm guessing on the reel optos". The ball-state simulator this disclaimer most directly concerns
(`ft_stateDef`/`ft_handleBallState`) is not consulted by this definition at all -- a VPX-driven
recreation uses the retained table's own ball physics, not PinMAME's built-in simulator -- but the
disclaimer is directly relevant to one specific `ftGameData` field: the upper-right flipper
declaration discussed below.

## Controller platform and address topology

`GEN_WPCFLIPTRON` (`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`) with `wpc_dispDMD`. The controller
profile is `pinmame.wpc-fliptronic`.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic 111-118.
  `ftGameData` declares no custom switch column (`hw.swCol = 0`). Of the 64 matrix positions, 43 are
  fitted and 21 are Not Used (11, 12, 23, 67, 68, 71-78, 81-88); the Switch Locations parts list and
  the Switch Matrix legend agree exactly on the unused set.
- Solenoids: physical drivers 1-3, 6, 8-16, 28 (coils/motor); flashers 17-23, 25-27; two Fliptronic
  lower-flipper circuits 45-48; four Fliptronic upper-flipper circuits 33-36 (unfitted, see below);
  PinMAME state channels 29-32; unused WPC-Fliptronic address space 37-44 (this generation has no
  LPDC board); simulator-only 49 and reserved 50; and three PinMAME-internal-only reel-simulation
  addresses 51-53 (see below). `ftGameData` declares `hw.custSol = 3`, publishing exactly those three
  addresses (`CORE_FIRSTCUSTSOL = 51`, so `CORE_CUSTSOLNO(1..3)` resolves to public 51/52/53).
- Lamps: 8x8 matrix 11-88, every address populated -- unlike several other WPC games curated in this
  project, this manual's Lamp Locations page marks **no** address "Not Used". `ftGameData` declares no
  auxiliary lamp column (`hw.lampCol = 0`).
- GI: five strings on public addresses 0-4, exactly matching this manual's own five printed GI rows.

## Solenoids 51-53: a PinMAME-only reel-position artifact, not real hardware

`ftGameData` declares `hw.custSol = 3` and names the three custom solenoids `sFakeReel1`/`sFakeReel2`/
`sFakeReel3` -- the driver's own comment says: "Define fake solenoids used to move the ball from the
reel to the ball catapult! We use 1 solenoid for each ball." `ft_getSol` returns each one's boolean
state purely from PinMAME's own internal software `reelPos` counter (0-149, six named zones), gated on
the reel motor being stopped. The driver's own inline comments label these addresses `(33)`, `(34)`,
and `(35)`, which are stale under the pinned revision: `CORE_FIRSTCUSTSOL = 51`, so
`CORE_CUSTSOLNO(1..3)` resolves to public **51, 52, 53**, verified directly in code rather than by
hand. The retained known-working VPX script never references any of the three addresses anywhere --
it implements its own complete, independent reel-position physics (see below) with no dependency on
this channel. All three are recorded `kind: "virtual"`, `availability: "unused"`; there is no real
driver-board transistor or coil behind any of them.

## The fishing reel: motorized multiball lock (headline mechanism)

A 50V gear motor (part 14-7967, solenoid 28) drives a belt/pulley system that rotates a physical
fishing-reel drum (A-14945 Fish Reel Unit Assembly, printed 2-26/2-27). A ball enters the reel via
reel-entry switch 35 after being kicked up the Habit Trail from the Caster's Club VUK (solenoid 3,
switch 47). Two discrete opto pairs (A-14315 LED / A-14316 photo-transistor, one top bracket and one
bottom bracket) report the reel's rotational position back to the CPU as switches 37 (Reel 1) and 38
(Reel 2).

Two independent, non-identical models exist for how the reel's rotation maps to those two switches.
Pinned PinMAME's own `ft_handleMech` uses a 0-149 position counter with `ERROR_RANGE = 10`: switch 38
(Reel 2 opto) is closed only at the Ball-1-Up position (0-10), while switch 37 (Reel 1 opto) is closed
across all six ball lock/release windows (Ball1Up=0, Ball2Up=50, Ball3Up=100, Ball1Down=75,
Ball2Down=125, Ball3Down=25, each +/-10). The retained known-working VPX script implements its own
richer, independent 0-360 degree `ReelPosition` angle counter with six named zones (10-30 Lock1, 70-90
Ball3Out, 130-150 Lock3, 190-210 Ball1Out, 250-270 Lock2, 310-330 Ball2Out), derives switches 37/38
directly from that counter through its own 23-branch `Select Case`, and drives the visible Reel
primitive's own rotation from the same value (`Reel.Rotx = ReelPosition + 46`). Three ball-catch
Kicker objects (`ReelEnter1`/`2`/`3`) model up to three balls riding the reel simultaneously before
`BallOut()` drops one at a time into the catapult -- this is the machine's multiball lock. Because
neither switch has a dedicated playfield sensor object (both are pure derivations of the internal
angle counter), both are documented projections onto the visible Reel drum Primitive.

**Unresolved polarity conflict (`conflict.reel-opto-switches-not-normalized`):** the manual documents
37/38 as opto construction (discrete A-14315/A-14316 parts, corroborated independently by the Fish
Reel Unit Assembly page's identical part numbers for the reel's own top/bottom opto brackets), but
pinned PinMAME's inverted-switch mask leaves column 3 (which carries 37/38) at `0x00` -- unlike column
4 (47/48, see below), it does not normalize these two confirmed-opto addresses. This manual's own
Switch Matrix wiring page carries no shading or opto legend at all (a format difference from several
other WPC manuals in this project), so it cannot independently corroborate either reading.

## Ball popper and drop target: normalized, but not documented as opto

**Unresolved polarity conflict (`conflict.ball-popper-drop-target-normalized-non-opto`):** pinned
PinMAME's `ftGameData` inverted-switch mask covers column 4 = `0xc0` (bits 6 and 7 -- verified in code:
`(0xc0 >> 6) & 1` and `(0xc0 >> 7) & 1` are the only set bits in the entire twelve-column mask),
normalizing public switches 47 (Ball Popper) and 48 (Drop Target). The manual documents both as
ordinary microswitches with no opto or proximity marking: 47 is `SW-1A-167-1`/`A-11658-1` and 48 is
`5647-12693-31`/`A-15211`, the latter cross-checking exactly against the 1-Bank Drop Target Assembly's
own microswitch item (printed 2-29). A physically normally-closed *mechanical* switch can legitimately
need the same software inversion an opto does, so this is not necessarily a defect -- but the manual
gives no independent confirmation either way, and it is the opposite disagreement direction from the
reel-opto conflict above (there, confirmed optos are *not* normalized; here, non-opto-marked switches
*are*). Both conflicts point at the same resolution path: a LibPinMAME gameplay-harness trace against
a legal `ft_l5` ROM, observing the idle public state of 37/38/47/48 against known ball position.

The drop target itself is a small raise/lower ramp: the A-15211 assembly is driven by two separate
coils, solenoid 12 (Up) and solenoid 13 (Down). The retained script models a single `DropTarget` class
instance (`DT48`) whose `DTAnimate` state machine drives a visible Primitive through hit-bend, drop,
hold-down, raise-hold, and reset phases; the public switch state is a side effect of that animation
reaching its fully-dropped or fully-reset threshold, not a direct collision-to-switch binding.

## No upper flippers, despite a driver declaration that says otherwise

Fish Tales has exactly two flippers, both lower (Fliptronic 111-114), and the upper positions (33-36,
115-118) are recorded not fitted -- a resolved finding, not a first-class conflict, but significant
enough to document at length because it directly contradicts pinned PinMAME's own driver metadata.
`ftGameData` declares `FLIP_SW(FLIP_L|FLIP_UR) | FLIP_SOL(FLIP_L|FLIP_UR)`, naming an upper-**right**
flipper as real driver-modeled hardware (button, EOS switch, and coil). Four independent,
game-specific manual sources unanimously disagree:

1. The Switch Locations parts list (printed 2-43) prints **no F5, F6, F7, or F8 row at all** -- not
   even a "NOT USED" placeholder of the kind several other WPC-Fliptronic manuals in this project use
   for genuinely unfitted upper positions.
2. The Fliptronic II Flipper Assembly parts list (printed 2-16) names exactly two assemblies,
   `A-15205-R-2` and `A-15205-L-2`, both lower positions, with no separate upper-flipper part anywhere
   in Section 2.
3. The full Playfield Parts list (printed 2-40/2-41) has exactly two flipper-assembly line items.
4. The Solenoid Table (printed 3-8) prints exactly two flipper-circuit rows ("Lower Right Flipper",
   "Lower Left Flipper"), again with no placeholder row for an upper pair.

The retained known-working VPX script independently confirms the same conclusion: it calls both
`NoUpperLeftFlipper` and `NoUpperRightFlipper` unconditionally at load (before any other
initialization), defines no `SolCallback`/`SolModCallBack` entry for solenoids 33-36, and references no
switch address in 111-118 anywhere in 251,489 bytes of code. Only the *generic* Fliptronic II
circuit-theory pages (printed 3-15 through 3-19) print wiring for all four possible flipper positions
-- and the manual's own diagrams there describe board-level capability present on every Fliptronic II
board regardless of which positions a given game's harness populates, not evidence of actual fitment
on this machine.

Given four unanimous, game-specific physical sources plus the known-working script against one
self-disclaimed driver field (`ft.c`'s own header: "I don't have access to this game, I guessed most
of it"), this definition records solenoids 33-36 and switches 115-118 as not fitted. This is treated
as a resolved finding rather than an unresolved `conflicts` entry, matching this project's precedent
for asymmetric-evidence naming/fitment corrections (for example Attack From Mars's loop-gate naming
defect and Indiana Jones's slingshot transposition), and is documented here in full rather than
silently decided.

## Cast handle, shooter lane, and the platform "shooter" common switch

Fish Tales has no manual plunger. The cabinet-front position a spring plunger rod normally occupies is
instead fitted with a "Fishing Reel handle" pushbutton assembly (A-15130, installed per assembly step
9), wired to switch 31 ("Cast"). The ball itself is auto-launched by solenoid 1 (Ball Shooter) once it
rests on shooter-lane switch 56, under ROM control (`Const UseSolenoids = 2`, fast flips). The Cast
button is used for Video Mode control during play. Notably, `ftGameData`'s own `wpc.comSw.shooter`
field is set to `swCast` (address 31) rather than to the shooter-lane switch (56) -- PinMAME's
platform-level "shooter" common-switch role, normally a ball-in-lane sensor on other WPC games, is
assigned here to this cabinet-front pushbutton instead.

## Other mechanisms

Solenoid 6 (`SolGate`, part A-14406) is a one-way gate with no dedicated printed switch; the retained
script toggles its `.Open`/`.Collidable` state. Solenoid 8 (script name `TopperFish`) actuates a
bell-armature toy on the large backglass "Fish & Plastic Insert" panel (A-15304 Coil Unit Assembly,
A-6306-2 Bell Armature Assembly) -- a backbox device with no printed switch and no playfield
coordinate. Three SW-11A-37 jet bumpers (solenoids 14/15/16, switches 51/52/53) and two slingshots
(solenoids 4/5, score switches 57/58 with a diode per the manual's footnote) are standard WPC devices.

The A-15109 Boat Unit Assembly carries two rollover-switch pairs for the port/starboard boat-exit
lanes (32/33) and boat-entry lanes (42/43), the captive-ball standup target (A-14691-5, switch 41),
and two lamp boards (A-15338 five-lamp PCB for 11-15, A-11271 four-bulb array for 35-38). No page read
describes a motor, tilt actuator, or moving axis for the boat prop itself -- unlike the reel, which is
explicitly motor-driven, the assembly page shows only switches, lamps, and flashers. On the evidence
gathered here the boat is a stationary playfield structure the ball rolls through/over, not a
mechanically animated rocking mechanism; "Rock the Boat" (lamp 13, flasher 21) is a scoring-mode name
on the rules pages, not evidence of physical motion. This should be re-checked if stronger contrary
evidence surfaces later.

The cabinet knocker (solenoid 7) and the backbox fish toy (solenoid 8) are both cabinet/backbox
devices with `not_applicable`/`cabinet_or_service` spatial records rather than playfield coordinates.

## Lamps: a backbox insert-panel board hiding behind matrix addresses 16-18

Lamps 16, 17, and 18 ("Letter (L)IE", "Letter L(I)E", "Letter Ll(E)") share assembly `A-15339`, the
manual's own "3-Lamp Board Assembly" mounted on the Back Panel Assembly (printed 2-30) -- a **backbox**
insert-panel board, not a playfield insert. This is confirmed independently of the same-numbered,
same-theme playfield rollover switches at 44/45/46 (also "Letter ...IE" labeled, assembly
`A-12688`/`A-12688-1`), which sit on the boat-unit assembly instead: the player collects the L-I-E
letters by rolling over the boat switches, and the backbox lamp board lights up to show progress -- a
classic WPC "insert panel" progress display, physically separate from the switches that score it. The
retained script models two co-located Light objects per address (base plus an "f"-suffix pair sitting
near the playfield's own rear edge) purely for visual effect; neither is treated as a playfield
coordinate, matching the manual's authoritative backbox classification. GI strings 0, 1, and 3
("Backbox G.I." per the manual) likewise have no playfield representation in the retained script,
consistent with all three being backbox circuits rather than an unmodeled gap; GI strings 2 and 4
("Playfield G.I.") drive the script's real `TopGI`/`BottomGI` collections (21 and 11 bulbs
respectively).

Lamp 48 ("Specials") is recorded with two placements: the retained table models two genuinely
distinct, mirrored Light objects (`l48` at the left outlane cluster alongside single-address lamp 58,
`l48a` at the right outlane cluster alongside single-address lamp 68) that both parse to public
address 48 under `vpmMapLights`' trailing-digit convention. The manual's Lamp Locations page prints no
explicit "(2)" quantity marker for this address; the two-placement quantity is inferred from the
retained table's own geometry rather than an explicit manual count, and is disclosed as such.

Two labeling disagreements between the Lamp Matrix legend (printed 3-2) and the authoritative Lamp
Locations parts list (printed 2-42) are preserved rather than silently corrected: the matrix legend
reads "Lie (L)"/"Lie (I)"/"Lie (E)" for 16/17/18 where the parts list reads "Letter (L) IE"/"Letter
L(I)E"/"Letter Ll(E)" (both agree on which physical device is which address; only the exact wording
differs), and the matrix legend repeats "Left Fish Body" for both 46 and 47 where the parts list
correctly distinguishes 46 "Left Fish Body" from 47 "Left Fish Tail" (matching the symmetric 56/57
"Right Fish Body"/"Right Fish Tail" pair on both pages). The parts list is authoritative for the label
in both cases, per this project's standing convention.

## Author construction checklist

- Build the three-position ball trough with the outhole, the auto-plunger shooter lane fed by the
  cabinet-front Cast reel-handle button (not a spring plunger), the motorized fishing reel with its
  three-ball lock and catapult release, the Caster's Club VUK, the Fish Finder saucer, the left gate,
  the raise/lower drop-target ramp, three jet bumpers, both slingshots, the boat unit's rollover lanes
  and captive-ball target, the cabinet knocker, and the backbox fish toy.
- There are no upper flippers. Do not bind solenoids 33-36 or switches 115-118 to any coil, button, or
  EOS switch despite pinned PinMAME's `ftGameData` declaring an upper-right flipper; see the dedicated
  section above for the full four-source citation trail.
- Treat switches 37/38 (Reel 1/Reel 2) and 47/48 (Ball Popper, Drop Target) as unresolved polarity
  questions (`conflict.reel-opto-switches-not-normalized`,
  `conflict.ball-popper-drop-target-normalized-non-opto`) rather than assuming either inversion
  convention.
- Lamps 16-18 are backbox insert-panel devices, not playfield inserts, despite sharing their
  "Letter ...IE" theme with the boat-mounted playfield switches 44-46.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the 21 printed Not Used
  positions, Fliptronic 111-118 (111-114 fitted, 115-118 not), the eight CPU DIP bits, solenoids 1-53
  (with 51-53 recorded virtual/unused, no real coil), lamps 11-88 (all fitted), GI 0-4, and the 128x32
  DMD.

## Sources

- `manual.williams.fish-tales.1992`: Williams Fish Tales operations manual (16-50005-101, August
  1992), SHA-256 `3bcd72631e2276eddf3b77a95ad693a1c16aaa30dea529acaf69cb3a259561c6`.
- `manual-support.williams.fish-tales.1992`: retained human transcription, SHA-256
  `4d45217f9b63775a5d1f969365a6333a8fd2e55417c84bbad15d81407664df3a`.
- `vpx-script.ft-vpw-1-1`: retained known-working VPW 1.1 embedded script, SHA-256
  `b6289a7087f11bd1902d8b059fe663723a6319c6490d1a2fa124d3dd7089e1f5`, binding `ft_l5`.
- `vpx-table.ft-vpw-1-1`: retained table, SHA-256
  `1f82c0237831b50c514e53c8938636f59ee584fc4346c143a3216b9f5d8a1029`, bounds
  `left=0 top=0 right=952.9412 bottom=2164.7058`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/ft.c` and the WPC-Fliptronic core/solenoid/
  flipper handling at the pinned revision.

## Procedural note

The recreation knowledge is source-reconciled and complete. The definition remains partial only for the two unresolved switch-polarity conflicts described above.
