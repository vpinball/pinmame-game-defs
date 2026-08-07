# Congo (Williams, 1995)

## Identity and evidence precedence

Congo is a Williams WPC-95 machine (manual 16-50050-101, November 1995,
FINAL). Pinned PinMAME's own `libpinmame.h` names the `GEN_WPC95` constant
"Integrated boards, Congo 3/96 - Cactus Canyon 2/99" — Congo is the game
PinMAME's own catalog anchors that hardware generation to. The retained
known-working table (original VP9 by JPSalas, VP10 conversion by nFozzy,
spotlight primitive by Dark, flasher images by LoadedWeapon) binds driver
`congo_21`, the production 2.1 ROM (DCS95 sound ROM S1.1).

This curation follows the project's standard evidence-authority order: the
retained script is runtime/causality ground truth, the Williams manual is
physical-construction/wiring/quantity ground truth, pinned PinMAME source is
controller-topology ground truth, and the retained table supplies geometry.
The retained manual has a usable but imperfect OCR text layer; every printed
table cited here was still read from 300-1200 dpi renders and transcribed by
hand into `evidence/excerpts/williams.congo.1995/`, not trusted from
`pdftotext`.

**This is a thin retained table** — 925 extracted files, far fewer than
richer WPC-95 recreations already curated in this project (Monster Bash: 2153
files). Several mechanism-internal ball sensors have no dedicated playfield
trigger object at all; those addresses are documented projections onto the
real kicker object that carries the mechanism's exit/entry point, not
invented coordinates.

## Controller platform and address topology

Reuses `controllers/pinmame/wpc-95.json` unchanged, confirmed directly from
`congoGameData`'s own `GEN_WPC95` field (not assumed from the task brief,
which suggested WPC-DCS or WPC-Security — both wrong; `congo.c` line 320
settles it). The switch matrix, Fliptronic column, LPDC duplication (37-40
mirrored at 41-44), and five-string GI layout all follow the standard WPC-95
rules already documented on that profile.

Congo declares no custom switch column, no auxiliary lamp column, and no
custom solenoid board (`congoGameData`'s trailing `hw` fields are all zero),
so this is a clean WPC-95 baseline with no address-remapping surprises beyond
the flipper circuits below. The switch matrix's eighth column (81-88) is
entirely unpopulated — Congo uses only seven of eight matrix columns.

**Flipper circuits.** Printed circuits 29/30 (Lwr Rt Power/Hold) and 31/32
(Lwr Lt Power/Hold) map to public addresses 45-48 (`CORE_FIRSTLFLIPSOL=45`).
Printed circuits 33-36 (the "Upr. Rt."/"Upr. Lt." driver-board slot,
`CORE_FIRSTUFLIPSOL=33`) already equal their own public addresses with no
translation. Congo fits exactly **one** upper flipper (left, at 35/36);
`congoGameData` declares `FLIP_SOL(FLIP_L | FLIP_UL)`, omitting `FLIP_UR`
entirely. Three independent sources agree there is no upper-right flipper:
the Switch Locations page marks F5/F6 (Upper Right Flipper E.O.S./Cabinet)
"Not Used"; the manual's own Solenoid/Flasher Table has no "Upper Right
Flipper" row at all in the printed Upr. Rt. slot (its two rows there are
instead labeled "Upper Left Post" and "Mystery Eject", ordinary non-flipper
coils); and the driver's own `FLIP_SOL` bitmask omits `FLIP_UR`. This is the
same "printed upper-flipper circuits repurposed for unrelated devices"
pattern already documented for other WPC-Fliptronic-generation machines in
this project, but simpler here: only two of the four printed Upr. Rt./Upr.
Lt. positions are repurposed (33/34), and the other two (35/36) are a
genuine, single upper flipper rather than a second flipper of any kind.

**Opto sweep: zero disagreement.** The Switch Matrix page shades exactly nine
addresses "OPTO, TYPICALLY CLOSED" (31-36, 41-43), and the Switch Locations
page independently identifies the same nine by their LED/photo-transistor
part numbers (A-18617-1/A-18618-1 for 31-35, A-16909 for 36 and 41-43) with
no separate switch part number. PinMAME's `congoGameData` inverted-switch
mask (`{0x00,0x00,0x00,0x3f,0x07,...}`, column 3 bits 0-5 = 31-36, column 4
bits 0-2 = 41-43) normalizes precisely the same nine addresses. This matches
the clean-sweep precedent already established by several other WPC-95/
Fliptronic-generation games in this project.

**A manual can disagree with itself four ways on one fact, and a script's
actual behavior can be the tiebreaker.** Congo prints its Solenoid/Flasher
Table three separate times (Section 2 at printed 2-42, an unnumbered
front-matter quick-reference copy, and a Section 3 copy beside the
schematics) plus once more as the Solenoid/Flashlamp Locations page. Two of
the four disagree with the other two on which of solenoids 15/16 is "Gorilla
Left" versus "Gorilla Right". The retained script's own `SolCallBack` sub
*names* (`"GorillaRight"` bound to solenoid 15) follow one pair of printed
tables, but the sub *bodies* physically rotate the opposite-side
`GoFlipperLeft`/`GoFlipperRight` primitive, agreeing with the other pair.
Taking the script's actual object manipulation — not its own sub-naming — as
runtime-semantics ground truth resolves the contradiction: solenoid 15 is
"Gorilla Left", solenoid 16 is "Gorilla Right". See
`evidence/excerpts/williams.congo.1995/solenoid-flasher-table.md` for the
full citation trail.

**A driver-board circuit-class label is not a device-kind classification.**
The printed Solenoid/Flasher Table's "Solenoid Type" column names the power-
driver-board wiring section (High Power / Low Power / Flasher / Gen.
Purpose), not the device's function. Solenoids 22-24 (Map Eject, Left Gate,
Right Gate) are wired through the same "Flasher" bank as the five genuine
light flashers (17-21) but are ordinary kicker/gate coils; the "Gen.
Purpose" bank (25-28) conversely drives four genuine flasher bulbs. Do not
infer `output.kind` from this column.

## Ball path, trough, and shooter

A four-ball trough (switches 32-35, drain-to-eject order) feeds the shooter
lane (switch 18) through the auto plunger (solenoid 1) — Congo has no manual
plunger. The retained script's `cvpmTrough` helper (`bsTrough`) reads
32-35 as a plain switch array with no dedicated playfield object per ball
position; the trough-eject opto (switch 31) is pulsed by the same
`SolRelease` handler (solenoid 9) that fires the physical release kicker
(`BallRelease`). Switches 31-35 are therefore documented projections onto
`BallRelease`'s own coordinate, not five distinct playfield sensor positions.

A ball draining down the left outlane (switch 16) is returned to play by the
Kickback coil (solenoid 2); the manual's own instruction card states the
feature is re-lit by completing the Left Bank three-target bank (switches
46/47/48, "Left Bank Top/Center/Bottom").

## The two-way popper and the Amy ramp

A single saucer at switch 53 (the retained script's `bsAmyVuk`, a
`cvpmSaucer`) can eject a captured ball in either of two directions: solenoid
3 fires the primary (up) kick, solenoid 4 the alternate (down) kick. The
manual's adjustment A.2 20 ("Amy Feed Disabled") is described as a
workaround "for use when the Amy ramp or Two-way popper are broken", which
independently confirms the popper feeds the same physical complex as the Amy
ramp (the ramp whose shots light lamps 16-18, spelling AMY). This machine
has **no magnet of any kind** — an earlier task brief that seeded this
curation pass described a magnet, but neither the manual, the driver source,
nor the retained script mentions one anywhere; that framing was wrong and is
corrected here.

## The Volcano: three-ball lock and popper

A ball entering the Volcano crosses the entrance opto (switch 36, "Volcano
Stack") and is fed into the retained script's second `cvpmTrough` helper
(`bsVolcano`), which reads three lock optos (41-43) as a plain switch array
with no dedicated playfield object. Solenoid 6 (Volcano Popper) ejects a
locked ball back to the playfield through the same kicker object (`sw36a`)
that models the entrance. Switches 41-43 are documented projections onto
`sw36a`'s own coordinate.

## The underground Gray Gorilla mini-playfield

This is Congo's headline mechanism, and the physical machine has no magnet —
the ball is captured and flung purely by two small mechanical flipper-arm
primitives. Completing the G-R-A-Y lamp sequence (lamps 62-65) opens a
hidden lower-level compartment; the manual's own instruction cards read
"COMPLETE G-R-A-Y SEQUENCE TO ACTIVATE LOWER LEVEL GRAY GORILLA FEATURE" and
"USE FLIPPER BUTTONS TO SWING GORILLA LEFT AND RIGHT AND HIT PINBALL INTO
C-O-N-G-O TARGETS. COMPLETE CONGO TO DEFEAT GRAY GORILLA AND AWARD BONUS."
The manual's own Gorilla Mechanism Test (T.16) confirms the physical
construction: "the operator [can] enable the underground mini-playfield and
test its operation... the left and right flipper buttons will operate the
gorilla mechanism and [display] the state of the gorilla stand-up switches"
— the five CONGO standup targets (switches 74-78).

Solenoids 15 (Gorilla Left) and 16 (Gorilla Right) each swing one of two
small captive flipper-arm primitives (`GoFlipperLeft`, `GoFlipperRight`)
inside the compartment; a separate timer gently rocks the gorilla figure
itself (`Gorilla.objRotZ`) between three fixed angles independent of which
arm just fired. A dedicated persistent "lower playfield" ball prop (created
by `CreateLPFball`/`kickerLPF` at power-on) represents the ball visually
while it is in the hidden compartment — a common VPX technique for a
genuinely hidden play area. The five CONGO standup targets (switches 74-78)
have real, dedicated `HitTarget`/`Wall` objects in the retained extraction
(unlike the trough/Volcano optos above), so their playfield placements are
directly validated rather than projected.

## Other kickers, gates, and posts

- **Mystery saucer** (switch 37, solenoid 34 "Mystery Eject"): a captured
  ball is held and kicked back through the same saucer object
  (`bsMystery`).
- **Map saucer** (switch 38 "Right Eject", solenoid 22 "Map Eject"): a
  captured ball is held and kicked back through the same saucer object
  (`bsMap`).
- **Ramp diverter** (solenoid 5): rotates a diverter flap (`Diverter`)
  between two ramp paths and toggles a companion guide (`DiverterSwoop`) in
  the same motion; no dedicated switch.
- **Left/right gates** (solenoids 23/24, `gate2`/`gate4`): simple one-way
  gates with no dedicated switch.
- **Top Loop Post** (solenoid 8): raises/lowers a post blocking the Upper
  Loop shot (switch 12); initialized raised (blocking) at power-on.
- **Upper Left Post** (solenoid 33): sits in the printed Fliptronic
  "Upr. Rt." driver-board slot but is an ordinary post, not flipper
  hardware — see the flipper-circuit note above.
- **Slingshots** (switches 61/62, solenoids 10/11) and **jet bumpers**
  (switches 63-65, solenoids 12-14): standard construction, no surprises.

## Lamps, flashers, and general illumination

The lamp matrix spells five words/names across its eight columns: CONGO
(11-15), AMY (16-18), ZINJ (split across 21/22 and 56/57 — the lost city
from the 1995 Congo film, spread across two non-adjacent matrix addresses
because they sit at different physical playfield insert locations), GRAY
(62-65, the sequence that unlocks the Gray Gorilla feature), and HIPPO
(81-85). Lamps 71/72 ("Travi"/"Com") together spell TRAVICOM, the name of
Karen Ross's company in the 1995 Congo film — the resolution evidence for
the "Corn" vs "COM" manual disagreement on lamp 72 (see below).

General illumination is the standard WPC-95 five-string layout: three
playfield strings (0 Playfield Gorilla, 1 Playfield Top, 2 Playfield Bottom)
and two backbox strings (3, 4; string 4 also feeds one cabinet bulb through
J104). GI address 1's retained emitter collection (`GiTop`) contains one
member, `GI10_Deactivated`, excluded as a table modeling anomaly (its own
name marks it disabled) rather than a fitted bulb, leaving 13 of 14
placements. Flasher solenoid 27 (Volcano Flasher) models four bulbs per the
manual (two playfield `#89`, one playfield `#906`, one backbox `#906`); the
backbox bulb's VPX stand-in (`F8L3`) sits at normalized x=1.022303, outside
the playfield's 0..1 bounds, and is excluded rather than placed. Flasher
solenoid 20 (Skill Shot Flasher) documents two bulbs per the manual (one
playfield, one backbox) but only one VPX Light object exists; the backbox
bulb has no playfield coordinate, matching the pattern already established
for other WPC-95 games in this project.

**Manual self-disagreement: lamp 72 "Corn" vs "COM".** The Lamp Locations
page (2-39) prints "Corn"; the Lamp Matrix page (2-38) prints "COM", and the
co-located switch at address 52 prints "Com" on both of its own pages
(Switch Matrix and Switch Locations). Three of four printed mentions agree,
and — decisively — lamps 71/72 spell "TRAVICOM" together with lamp 71
("Travi"), the name of the film company. "COM" is used; "Corn" is the
typographic slip.

**Manual self-disagreement: GI address 2 bulb code.** The Solenoid/Flashlamp
Locations page prints "24-8549" for "Playfield Bottom", matching none of
that page's own four legend codes. The Solenoid/Flasher Table page states
the bulb type directly as "#44" for the same string. "#44" (`24-6549`) is
used; "24-8549" is treated as a printing error.

## Author construction checklist

- WPC-95 hardware, one CPU/power-driver board pair, standard five-string GI,
  seven-column (not eight) switch matrix, no auxiliary lamp/switch/solenoid
  boards.
- Exactly one upper flipper (left); the "Upr. Rt." Fliptronic slot drives an
  ordinary post (33) and a saucer eject (34) instead.
- Headline feature: a hidden lower-level compartment with a gently rocking
  gorilla figure and two small flipper arms that fling the ball at five
  CONGO standup targets, entered after completing G-R-A-Y. No magnet.
- Volcano: entrance opto plus a three-ball lock, ejecting through one shared
  kicker.
- Two-way popper (Amy VUK) feeding the Amy ramp / Gray Gorilla complex, with
  independent up/down eject directions.

## Sources

- `pinmame.catalog.4ec52ff0ac13`: pinned catalog driver records for the
  `congo_*` clone tree.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/prelim/congo.c` and shared
  WPC-95 core source (`core.h`, `core.c`, `wpc.c`, `libpinmame.h`).
- `controller-profile.pinmame-wpc-95`: the shared WPC-95 controller profile.
- `manual.williams.congo.1995`: the retained Williams Congo operations
  manual (16-50050-101), transcribed into
  `evidence/excerpts/williams.congo.1995/`.
- `vpx-table.congo-jpsalas-nfozzy` / `vpx-script.congo-jpsalas-nfozzy`: the
  retained known-working recreation and its embedded script.
