# Bally Eight Ball Deluxe (1981)

Eight Ball Deluxe is a Bally MPU AS-2518-35 (BY35) machine, the same physical controller family as
Centaur and Kiss, both already curated in this project. It reuses `controllers/pinmame/by35.json`
unchanged, confirmed directly from the pinned driver's own declaration in `src/wpc/by35games.c`
line 1122: `INITGAME2(eballdlx,GEN_BY35,dispBy7,FLIP_SW(FLIP_L),8,SNDBRD_BY61,0)`. `dispBy7` means
seven-digit player displays (not a DMD); `lampCol=8` means a full auxiliary lamp driver board is
present, giving PinMAME a public lamp address space of `(8+8)*8 = 128`, of which this physical
machine's retained known-working script drives 74 real addresses.

## Year: this definition uses 1981, not the retained table's "1980"

The retained known-working VPX table's own title reads "Eight Ball Deluxe (Bally 1980)". Pinned
`driver.c` dates every driver in the `eballdlx` family 1981 (`CORE_GAMEDEFNV(eballdlx,"Eight Ball
Deluxe (rev. 15)",1981,"Bally",...)`), and the repository's own pre-existing stub identity is
`bally.eight-ball-deluxe.1981`. This manual's own printed copyright, "COPYRIGHT MCMLXXXIV BY BALLY
MIDWAY MFG. CO." (1984), is a third value again — but it is the manual's *reprint* date under the
merged "Bally Midway" imprint, which did not exist until the 1983-84 Bally/Midway merger, not the
physical machine's release date. None of the three numbers agree, but only two of them are
candidates for the actual release year, and this definition uses 1981 to match the pinned driver
and the existing catalog identity; the table author's "1980" is treated as an informal or
mistaken date rather than a competing authority. Recorded as `conflict.retained-table-year-vs-
driver` for transparency even though it does not block promotion on its own.

## Switch and solenoid address derivation: two different rules on one platform

This game's manual carries no dedicated switch-matrix or lamp-matrix wiring table the way the
WPC-era manuals this project has curated do — it is the same compact "Installation and General
Game Operation Instructions" format Centaur's and Kiss's manuals use, with a printed Solenoid
Identification Table and Switch Assembly Self-Test Display Numbers table (both keyed by "Self
Test #", not the public controller address) plus a full playfield wiring schematic
(`W-1192-28C`). Centaur's and Kiss's curations already established that a printed Self-Test #
must never be assumed equal to the public address without independent verification. Running the
pinned LibPinMAME native library against the user's own legally held `eballdlx` ROM through
`tools/run_pinmame_harness.py` settled both tables definitively, and the two turned out to follow
**different rules**:

- **Switches**: holding each public address 1-40 in turn during the ROM's own "search each switch
  assembly for stuck contacts" self-test stage displayed that exact address on the player score
  displays. The public switch address equals the printed Self-Test # directly, with no
  translation. The playfield wiring schematic (`W-1192-28C`) independently confirms this: reading
  its five-column, eight-row switch matrix grid column-major (`address = (column-1)*8+row+1`)
  reproduces the printed Self-Test # for every switch on the sheet.
- **Solenoids**: the automatic 20-step solenoid self-test cycle (entered after six presses of the
  self-test button and then running unattended, repeating identically every ~20 seconds) shows
  that the printed Self-Test # is **not** the public address for solenoids. Self-test 01 (LEFT
  SLINGSHOT) fires public address 4; self-test 03 (KNOCKER) fires public address 6 — independently
  confirmed by the retained script's own `SolCallback(6) = "...Knocker..."` — and so on through the
  full derived table recorded in `review-artifacts/eight-ball-deluxe/manual-transcription.md`.

This is worth carrying forward: **a manual's two address tables on the same platform, even the
same page, can follow entirely different public-address rules.** Confirming one does not license
assuming the other follows the same pattern; each needs its own independent check.

## Three solenoids are genuinely dual-function, gated by one lamp

Public solenoid addresses 8, 9, and 10 each answer to **two** self-test identities:

| Address | Lamp 52 off | Lamp 52 on |
| --- | --- | --- |
| 8 | 7-Bank Drop Target Reset (self-test 15) | Saucer Kicker (self-test 17) |
| 9 | #1, 9 Drop Target Reset (self-test 08) | Outhole Kicker (self-test 18) |
| 10 | #2, 10 Drop Target Reset (self-test 09) | 4-Bank Drop Target Reset (self-test 16) |

This is not a harness artifact or a coincidence of the auto-cycle: the retained known-working
script's own `SolSaucer`, `SolBallRelease`, and `SolReset` subs (`script.vbs` lines 77-108) each
branch explicitly on `Controller.Lamp(52)` and call a different physical action in each branch —
independently reproducing the exact same three dual-function addresses the harness found, from a
completely different kind of evidence (script logic vs. runtime tracing). Both self-test identities
are recorded as `manual.self-test` aliases on the one output device; the device is not split into
two records, because it is one physical coil.

The practical reading: Lamp 52 appears to be a "feature active" flag — most plausibly tied to the
saucer/Add-a-Ball state described in Section IV's SAUCER FEATURE — that repurposes three coils
which are otherwise individual per-target drop-bank reset actuators into ball-handling actuators
(trough release, saucer kick, and a second bank-wide reset) while that feature is active. This
curation did not attempt to fully reconstruct the exact rule that sets Lamp 52, since that is
gameplay-rule reconstruction beyond the address-and-wiring scope of this pass; it is recorded here
as a lead rather than asserted as settled.

## Flippers are not CPU-controlled

`eballdlx` declares `FLIP_SW(FLIP_L)` — a switch mask — and no `FLIP_SOL` bit at all. In
`src/wpc/core.c`, `core_updateSw`'s `if ((flip & FLIP_SOL(FLIP_L)) == 0)` branch is true for this
game, so PinMAME **fakes** the flipper solenoids rather than reading real driver-board output for
them: the flipper coils fire directly off the physical flipper buttons through a relay circuit
(publicly enumerated as solenoid 19, "K1 Relay (Flipper Enable)"), not through any CPU-timed
solenoid address. This matches the by35 platform note already established by Centaur and Kiss:
`FLIP_SWL`/`FLIP_SWR` are both zero for this `flip` value, so no dedicated flipper-button switch
position is copied into the game's own switch matrix either, and the generic flipper column at
internal index 11 (public 81-88) is never read by this ROM.

## Three drop-target banks, one saucer, one outhole

The retained script's own mechanism wiring (`script.vbs` lines 225-235) is unambiguous and gives
three separate `cvpmdroptarget` banks:

- **7-target bank** ("Deluxe" bank, switches 17-23, self-test-table-named "1,9" through "7,15"):
  Feature G. Completing it once scores 2000 per target and flashes the single "8 Ball" standup
  (switch 33 in the switch table's numbering is actually the Single Drop Target — the "8 Ball"
  flash is driven by lamp 33, a separate lamp address, not a matrix switch); completing the same
  seven targets a second pass scores 3000 each as "deluxe". Reset is solenoid 8's Lamp(52)=0
  identity (whole-bank raise); solenoids 9 (Lamp 52 off), 10 (Lamp 52 off), and 11-15
  unconditionally each re-fire one target's individual drop/reset animation.
- **4-target bank** ("In-Line" targets, switches 1-4): Feature C. 1st-4th target down scores
  5000/10,000/15,000/20,000 and lights 2X/3X/4X/5X. Reset is solenoid 10's Lamp(52)=1 identity.
  The related "In-Line Back Target" (switch 5, "Bank Shot", scoring 50,000) is a separate fixed
  standup, not part of this drop bank.
- **Single target** (switch 33): Feature E. Scores 500, or scores and advances the lit right-lane
  value; stays down until the ball returns through lane A or B. Reset is solenoid 7
  unconditionally.

The **saucer** (switch 34, Feature B) is a ball-capture mechanism (`bsTP`, a `cvpmBallStack`
object) kicked out by solenoid 8's Lamp(52)=1 identity. The **outhole** (switch 8, the ball-drain
sensor beneath the playfield) is a second `cvpmBallStack` object (`bsTrough`) released by solenoid
9's Lamp(52)=1 identity.

## Direct switch-to-coil relationships (no CPU timing)

The Solenoid Identification Table carries its own note directly beneath the printed table: "NOTE:
SLINGSHOT & THUMPER BUMPER COILS WILL BE ENERGIZED WHEN SWITCH IS MADE." This is the manual's own
statement that solenoids 1-5 (the two slingshots and three thumper bumpers) are wired directly to
their switch, not fired under ROM timing control the way every other solenoid on this machine is;
the retained script has no `SolCallback` entry for any of addresses 1-5, consistent with a
direct hardware relationship rather than a scripted one. This definition records five `direct`
relationship entries for these pairs (switch 38 -> solenoid 3, 39 -> 2, 40 -> 1 for the bumpers;
36 -> 5, 37 -> 4 for the slingshots).

## General illumination is uncontrolled — no `pinmame.output.gi` group exists for this platform

The playfield wiring schematic (`W-1192-28C`) wires General Illumination as a bare two-wire AC
circuit — `40-A2J1-6` and `50-A2J1-3 RET.` feeding "GEN. ILLUM. (23)" — with no lamp-driver or
solenoid-driver connector anywhere in the path. This matches the retained script's own behavior:
`For each xx in GI: xx.State = 1` runs once at table load and is never called again. The BY35
controller profile has no `pinmame.output.gi` group at all (unlike the System 11 and WPC platforms
already curated in this project, where GI is at minimum a pair of ordinary solenoid addresses or a
dedicated dimmable channel) — this schematic is the physical reason: there is no CPU path to
general illumination on this machine at all. Following the project rule that a device without any
controller binding is not a controller-addressable device, this definition does not enumerate the
retained table's 26 `Light.GI_*` playfield-illumination bulb objects as `outputs`; they are real
physical bulbs, but they are not devices this or any recreation binds to a controller address.

## Auxiliary lamp board (addresses 97-116): enumerated, not fully traced to the schematic

Unlike Centaur's and Kiss's curations, which traced their AS-2518-43 auxiliary lamp board all the
way from PinMAME's public address through the decoder/SCR chain to the exact A5Jx/A9Jx connector
pin, this pass used the retained known-working script's own explicit `NFadeLm <address>,
l<address>` bindings (`script.vbs` lines 476-679) as the address-enumeration and spatial-placement
source for the auxiliary board (addresses 97-116, plus the multi-image backbox lamp groups at 101,
117, 118, and 119), and did not additionally derive each address's own SCR-to-connector-pin
identity from the wiring schematic's A5J1/A5J3-to-A9J2/A9J3 tables (visible on the same
`W-1192-28C` sheet, "1 RACK" through "50X DELUXE"/"SPECIAL DELUXE"). The addresses and positions
are runtime-validated; the exact physical board-pin path for each one is not. This is why
`coverage.missing` names `output_semantics` and the record stays `partial`.

## DIP option switches: partially resolved

The AS-2518-35 MPU module carries four eight-position DIP banks (S1-S32; `BY35HW_DIP4` is
unconditionally set for `GEN_BY35` in `src/wpc/by35.c`'s `MACHINE_INIT(by35)`). Section V.B and the
Feature Operation section (Section IV) between them document the function of 27 of the 32
switches: coin-chute credit ratios (1-5, 9-13, 17-20), maximum credits (25-26), high score feature
(27), match feature/credit display (28), balls per game (31-32), and seven feature-specific
switches named inline in Section IV (8, 14, 16, 21, 22, 23, 24). Switches 6, 7, 15, 29, and 30 are
not named anywhere in the pages read for this pass; they are recorded with a `candidate`
provenance and an honest "function not resolved in this pass" label rather than a guess. This is
why `coverage.missing` names `input_semantics` and the record stays `partial`.

## Physical switch construction

The manual's own "ASSEMBLY ADJUSTMENTS: GENERAL" section (page 18) states plainly: "All switch
assemblies consist of leaf springs, contacts, separators, plastic tubing and screws" — a
machine-wide statement, not a per-switch specification. No switch on this 1981 machine is
opto-constructed (optos are a later Williams/Bally convention); every matrix switch in this
definition is recorded `leaf` except the physical credit pushbutton (`button`) and the plumb-bob
tilt mechanism (`tilt`).

## Physical family

The physical family is the six-driver `eballdlx` clone tree: `eballdlx` (production revision 15,
the reference for this definition), `eballd14` (revision 14, earlier firmware), and four later
Bally/Oliver and community free-play/rules/bugfix conversions (`eballdla`, `eballdlb`, `eballdlc`,
`eballdld`) that keep the identical switch matrix, solenoid table, lamp boards, and playfield.
Every driver is physically identical. `eballchp` (Eight Ball Champ, 1985) and `eightbll` (Eight
Ball, 1977) are unrelated physical machines with their own separate stubs and must not be merged
into this family.
