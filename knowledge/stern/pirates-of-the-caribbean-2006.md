# Stern Pirates of the Caribbean (2006) - recreation knowledge

Canonical definition: `machines/partial/stern/pirates-of-the-caribbean-2006.json`
(`stern.pirates-of-the-caribbean.2006`). Spatial audit:
`reports/spatial/stern/pirates-of-the-caribbean-2006.json`. Manual transcriptions:
`evidence/excerpts/stern.pirates-of-the-caribbean.2006/`.

This record is deliberately `partial`. Read the "What is not settled" section before
authoring anything that depends on switch polarity, on the flasher bulb split between the
playfield and the back panel, or on general-illumination bulb positions.

## Identity, and the year trap

The physical machine is a **2006** Stern production game. Two independent sources agree:
the retained service manual's own printed page 3 carries `(c)2006  820-6384-00 Rev A`, and
pinned PinMAME's own catalog dates the earliest firmware in the `potc` clone tree
(`potc_108as` through `potc_115gf`) 2006, with the `300*`/`400*` revisions 2007 and the
`600*` revisions 2008.

PinMAME's clone-tree parent is `potc_600af`, the 2008 V6.0 English/French firmware, and the
generated stub this definition replaces therefore recorded the machine year as 2008. Under
this project's identity rule a later firmware revision does not create a new physical game,
so the physical record is 2006 and the parent driver's own 2008 year is carried only on that
driver's record.

`machine.ipdb_id` is omitted rather than guessed. IPDB was unreachable during this pass: it
returns HTTP 403 behind Cloudflare to a plain fetch and no headful browser session was
available. The year did not depend on it.

The physical family is the twenty-eight-driver `potc` clone tree: `potc_600af` plus
twenty-seven language and firmware clones (four each of V1.09, V1.10, V1.13, V1.15, V3.00,
V4.00 and V6.0, plus the single V1.08 and V1.11 Spanish revisions). Every one of them shares
the one static `potcGameData` struct that `sam.c`'s `INITGAME` macro produces, so no
controller address, switch polarity, lamp, solenoid or playfield fact differs between them.

## Platform: Stern S.A.M., with every profile rule re-derived from source

The task brief that seeded this curation described Pirates of the Caribbean as the project's
first Stern S.A.M. machine and `controllers/pinmame/sam.json` as unproven scaffolding. That
is wrong, and the correction is recorded here rather than reproduced: **thirty-one other
definitions already bind `pinmame.sam`, twenty of them `author_ready`** (Spider-Man 2007
and its Vault Edition, Iron Man 2010 and its Vault Edition, the four AC/DC builds, Avengers Pro, both Metallica
builds, both Mustang builds, both Star Trek builds, both Rolling Stones builds, both Walking
Dead builds and TRON Legacy LE), plus eleven partials. The profile is well exercised.

What is true is narrower and worth stating precisely: every address rule in that profile was
re-derived from pinned source for this curation rather than trusted -- `src/wpc/sam.c`,
`src/wpc/core.c`, `src/wpc/core.h`, `src/wpc/vpintf.c` and `src/libpinmame/libpinmame.h` --
and every rule matched, so the profile is reused unchanged. This is also the first S.A.M.
machine in the repository to carry a committed set of manual excerpts under
`evidence/excerpts/`.

Two of the profile's prose notes are imprecise and were left alone rather than edited from
inside one game's curation; both are recorded in the definition's controller-profile source
record and neither affects an address rule.

The rules that matter, all confirmed from pinned source rather than by analogy with any WPC
or Whitestar profile:

- **Sequential public switch numbering, not column-times-ten.** SAM imports its machine
  driver from `PinMAME`, which sets `MDRV_SWITCH_CONV(core_swSeq2m, core_m2swSeq)` with
  `core_swSeq2m(no) = no + 7`. Public switch `N` is therefore internal switch-array column
  `(N + 7) / 8`, bit `(N + 7) % 8`. That places the 8x8 playfield matrix at public 1-64,
  `swMatrix[9]` (dedicated D-1 to D-8) at 65-72, the never-written `swMatrix[10]` at 73-80
  (which is why the profile's address rules skip that range), and the flipper column
  (`CORE_FLIPPERSWCOL = 11`) at 81-88. `swMatrix[0]`, the upper dedicated byte D-17 to D-24,
  lands at public **-7 through 0**.
- **The manual prints the switch matrix as four drive rows by sixteen return columns**,
  numbered sequentially `SW. #1` to `SW. #64` across each drive row in turn. That matches
  PinMAME exactly, because `sam.c` reads two internal columns per strobe
  (`MAKE16BIT(swMatrix[2 + stb*2], swMatrix[1 + stb*2])`, four strobes). Printed drive row 1
  is public 1-16, row 2 is 17-32, row 3 is 33-48, row 4 is 49-64.
- **The start button lives inside the playfield matrix range.** `SAM_COMPORTS` puts the
  Start Button and Tournament Start on internal column 2 bits 7 and 6, which are public 16
  and 15, and this manual independently prints `SW. #15 TOURNAMENT START` and `SW. #16 START
  BUTTON` with the black `CABINET` tag. Do not assume any address in 1-64 is a playfield
  switch.
- **The lamp matrix is row-major, the opposite axis order from Whitestar's switch matrix.**
  Public lamp `N` is printed row `(N - 1) / 8 + 1`, column `(N - 1) % 8 + 1`: ten ground rows
  (`Q33`-`Q42`) by eight drive columns (`IC-U17`-`IC-U10`), with rows 9 and 10 driven from
  the Aux Lamp strobe's two data bits and carrying public 65-80. This was re-derived from
  this manual's own printed grid, and `sam.c` confirms it independently by naming lamps 24,
  32, 40, 48, 56, 64 and 72 as the H, E, A, R, T and two Heart Chest LEDs of board
  `520-5258-00` - which is column 8 of rows 3 to 9.
- **The four flipper coils are ordinary numbered solenoids, with no 45-48 remap.** Whitestar
  moves physical Q15/Q16 off public 15/16 onto legacy flipper addresses; SAM does not.
  `sam.c` writes only `coreGlobals.solenoids` and the physical-output array and never touches
  `coreGlobals.solenoids2`, and `coreGlobals.hasModulatedFlippers` is never set for SAM, so
  public 45-48 are dead. This machine's two flipper coils are public 15 and 16, and the
  retained script confirms it directly with `SolCallBack(15) = SolLFlipper` and
  `SolCallBack(16) = SolRFlipper`. One address carries both the power pulse and the hold: the
  board drives 40 ms of power then a 1 ms pulse every 12 ms, which is why `sam.c` gives
  solenoids 13-16 a 14 ms `switchDownLatency`.
- **The I/O board's solenoid latches are not in address order.** `SOL_B` (0x02400021) is
  public 1-8, `SOL_A` (0x02400020) is 9-16, `SOL_C` (0x02400022) is 17-24, and `FLSH_LMP`
  (0x02400023) is 25-32. Irrelevant to a consumer, but worth knowing before reading a trace.
- **Public solenoids 33-66 always exist and this machine drives none of them.** `INITGAME`
  hardcodes `hw.custSol = 16` for every SAM game, so `coreGlobals.nSolenoids` is always 66
  and LibPinMAME's `ChangedSolenoids` contract always covers 51-66. Address 33 is PinMAME's
  synthetic game-on / fast-flips state, read from one byte of game RAM at
  `samlocals.fastflipaddr` (`0x0105a7fe` for any driver whose short name starts `potc_600`)
  and explicitly declared `CORE_MODOUT_NONE`. 34-36 return the same bit through `core_getSol`
  but are zero in both aggregate paths a consumer reads. 37-44 mirror internal indices 41-48,
  which `sam.c` never writes. 49-50 are PinMAME's own ball simulator. 51-66 belong to an
  auxiliary driver board: `potcGameData` declares `SAM_NO_AUX`, so none of `sam.c`'s six
  auxiliary-board write paths is enabled and nothing ever writes them. The manual's Coils
  Detailed Chart Table stops at `#32`, matching.
- **One general-illumination channel, not five.** `coreGlobals.nGI = 1` and `sam.c` drives
  `coreGlobals.gi[0]` from bit 0 of the latch at 0x0240002B with its own comment
  `Bit 0 drives GI relay`. Every physical illumination string behind that relay switches
  together. The retained script matches: its `UpdateGI` ignores the string number entirely.
- **The EOS switches are synthesized from the buttons.** `sam.c`'s dedicated-switch read
  copies each flipper button bit into the adjacent EOS bit
  (`data |= (data & (bit8|bit10|bit12|bit14)) << 1`) with the comment "SAM is not using
  standard VPM flipper coils, so the EOS simulation does not take place, and the ROM reports
  technician errors". Public 81 and 83 are real switches on the flipper assemblies
  (`180-5149-00`), but a recreation does not need to drive them independently.
- **The printed D-numbers run backwards against the public addresses inside each flipper
  nibble.** `sam.c` reverses each nibble of the flipper column, so public 81/82/83/84 are the
  manual's D-12/D-11/D-10/D-9 and public 85/86/87/88 are its D-16/D-15/D-14/D-13. All four
  of the latter are printed `NOT USED` and are additionally structurally unreachable: this
  game's `hw.flippers` is `FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`, so `core.c`'s
  `locals.flipMask` evaluates to `0x0f` and `core_updateSw` never writes the upper four bits.

## Machine layout in one paragraph

Two flippers, three pop bumpers in a triangular cluster in the rear right, two slingshots,
three top lanes, left and right orbits, a left ramp, a treasure chest on the right that
captures and locks a ball, a motorised spinning "Plunder" disc at the rear left ringed by six
stand-up targets, a six-target "Pirate" bank across the middle of the playfield, an eject
hole beside the pop bumpers, a Jack scoop, a skill hole at the top, and the headline toy: a
model ship at the rear left that rotates about its beam to dive bow-down as the player sinks
it, with its masts folding forward. The compass ring of twelve inserts around a two-bulb
"Four Winds" centre, the five HEART letters and two Heart Chest dots on LED board
`520-5258-00`, and the JACK and KEY letter sets are the main insert groups.

## Mechanisms

Full topology, marks, ranges and causality are in the definition's `mechanisms` array. What
is worth reading here is the reasoning behind the two that are easy to get wrong.

### The sinking ship

Driven by a 24 V motor on public solenoid 21 whose **direction comes from a separate relay
PCB** on public solenoid 27 (`Relay PCB / 511-5024-03`), not from reversing the motor
output. The retained script makes the split explicit: `SolShipMotor` only enables the
position timer, and `SolMotorDir` sets the sign the timer steps by. A recreation must read
27 to know which way 21 will travel.

Two limit switches report the ends of travel, both `180-5189-00` below the playfield: public
63 (Ship Home) at the upright rest position and public 62 (Ship Fully Sunk) at the far end.
**Between the two ends neither switch is made**, so the hardware reports three
distinguishable states, not a continuous position. The retained script steps an internal
0-3 counter through two intermediate sink attitudes, which is table modelling rather than
reported hardware state, and neither intermediate attitude has a switch behind it.

Public 61 (Ship Made) is a separate opto pair in the ship's own shot path. It is not a
position sensor and must not be treated as one.

Two more coils act on the sails rather than the hull - public 5 (Raise Sails, 26-1200) and
public 28 (Lower Sails Latch, 29-1400) - and the retained script only accepts either while
the hull is at home (both subs test `If ShipPos = 0`). Public 29 (Ship Pin, printed
`UP POST`) is a retractable post in front of the ship and public 32 (Flash: Ship) is its
flasher.

Startup and reset: the retained script sets `Controller.Switch(63) = 1` in `Table1_Init`, so
the ship rests at home with the home switch made and the sails latched down. That is recorded
as `initial_active` on the switch record. The motor does not actuate either limit switch;
the hull reaching the end of travel closes it.

### The Plunder disc

Public solenoid 6 is a 12 V motor (`511-5024-04`) that spins the disc continuously while
asserted. **The disc has no position sensor of any kind.** No printed switch reports its
angle, and the retained script drives it as a `cvpmTurnTable` whose visible rotation is a
free-running timer stepping `RotatingPlatform.RotZ` by 7 degrees, so a recreation gets speed
but not phase. What the ROM actually knows is only whether a ball is on the disc, from the
two opto pairs at its entrance and exit: public 11 (Plunder Enter) and public 4 (Plunder
Exit). The retained script keeps its own `BallinSpin` counter off exactly those two.

The six stand-up targets around the disc are public 42-47 (`180-5133-02`, above playfield),
and public solenoid 23 (Plunder Pin, 22-900) is a retractable post at the disc.

### The trough carries two different switch constructions

The four-ball trough's position switches are printed as two families on one page: `TROUGH #4
(L)`, `#3` and `#2` at public 18, 19 and 20 are mechanical switches (`180-5119-02`), while
`TROUGH #1 (R)` at public 21 is an opto pair annotated `(VUK OPTO)` with transmitter and
receiver parts `515-0173-00` and `515-0174-00`. A fifth address, public 22, is a second opto
pair annotated `(STACK OPTO)` and named `TROUGH JAM` in italics; it sits in the exit path
rather than at a ball rest position. Construction must be checked per switch even inside one
assembly - the same lesson Williams Bram Stoker's Dracula's Mist Magnet already established.

Solenoid 1 lifts one ball out to the shooter lane. It does **not** actuate the jam opto: the
retained script's `vpmTimer.PulseSw 22` from inside `SolTrough` is the ball crossing that
opto as it leaves.

## What the retained table is and is not good for

The retained recreation is a thin, non-VPW community build: 1,229 extracted files and a
**32,543-byte** script, against the 240-290 kB VPW-authored scripts several other games in
this run used. It is judged on what it actually models. Where it models an address with a
plausibly placed object, that object supplies the coordinate; where it does not, no
coordinate was invented. Its `AllLamps` collection does cover 78 of the 80 lamp addresses
(everything except the two cabinet button lamps), which is better coverage than the thin
tables used for Creature, The Getaway and The Simpsons Pinball Party managed.

Three specific things about it are worth knowing before trusting it:

1. **It has a real script defect on Plunder 1.** `Sub sw43_Hit` is defined twice - once
   pulsing switch 42, once pulsing switch 43 - and `sw42_Hit` is not defined at all, so only
   one of the two definitions can survive and public switch 42 goes unreported at runtime.
   The table does contain a correctly positioned `sw42` HitTarget object, which is what this
   record's placement uses. This is a defect in the recreation, not evidence about the
   physical machine.
2. **Its pop-bumper switch bindings are rotated against the manual.** See the conflict
   below. The placements in this record follow the manual and the table's own geometry, not
   the script's object ordering.
3. **It duplicates several emitters as co-located render doubles**, and its flasher light
   counts exceed the manual's printed bulb quantities. The excluded objects are enumerated in
   the spatial audit's `excluded_object_classes`.

## Back panel: ten lamps and ten G.I. bulbs that are not on the playfield

Printed page 91 (`Back Panel Assembly, Individual Parts Only`) is the page the lamp-matrix
footnote points at, and it is decisive. The back panel carries:

- `ITEM 2`: ten 2-lug sockets with `#44` clear heavy-filament bulbs, each labelled `G.I.` on
  the drawing. The Lamp Locations page says the same thing independently: "THE TOP TEN CLEAR
  BULBS ARE G.I.s; NOT CONTROL LAMPS."
- `ITEM 3`: seven 3-lug sockets with `#44` red bulbs, labelled `LP. 33` to `LP. 39` - the
  matrix's `BACKPANEL #1 (L)` to `#7 (R)`.
- `ITEM 4`: three 3-lug sockets with `#44` green bulbs, labelled `LAMP 78`, `LAMP 79`,
  `LAMP 80` - the matrix's `LEFT`, `MIDDLE` and `RIGHT TOP LANE`.
- `ITEM 5`: two 2-lug stand-up sockets with `#89` clear bulbs, both labelled `Q22 FLASH`.

So **ten matrix lamp addresses are backbox devices**, and three of them (78-80) are named
after playfield lanes whose switches (public 12, 13, 14) really are on the playfield. The
retained table does model a Light object for each of the ten at the extreme rear edge of the
playfield, normalized y between 0.020 and 0.022; those coordinates are recorded in the
retained geometry dump and deliberately not promoted to playfield placements. This is the
same pattern Williams Fish Tales's backbox 3-lamp board already established.

## Flashers

This game fits five, and three sources agree exactly on which: the manual's own Test Flash
Lamps note ("This Game: Q20, Q22, Q30, Q31 & Q32"), the Coils Detailed Chart Table's `#89
Bulb` rows, and pinned `sam.c`'s own `potc` block, which declares
`CORE_MODOUT_BULB_89_20V_DC_WPC` at solenoid indices 20, 22 and a run of three from 30. Zero
disagreement.

Quantities are printed on two of them: `#22 FLASH: REAR CENTER (X2)` and `#30 FLASH: BACK
RIGHT [X3]`. Where those bulbs physically sit is the one thing this manual contradicts itself
about; see the conflict below.

## What is not settled

Four unresolved conflicts, all recorded as first-class `conflicts` entries.

1. **`conflict.sam-invsw-never-populated`** - the platform-wide polarity gap. Pinned Stern
   S.A.M. source populates no inverted-switch mask at all: `INITGAME`'s positional
   initializer leaves `wpc.invSw` at its C zero default and searching the whole of `sam.c`
   for `invSw` returns no assignment anywhere. Against that, this manual positively
   identifies seven opto switches - 3, 4, 11, 21, 22, 60 and 61 - and never states
   normally-open or normally-closed for any individual switch. Physical construction is known
   for seven addresses while their emulator-side normalization is not. Check this on every
   future S.A.M. curation rather than assuming it; it is the same shape as the Whitestar gap
   already recorded for Stern The Simpsons Pinball Party. Resolution needs a LibPinMAME
   harness trace observing the idle public state of those seven addresses.
2. **`conflict.flasher-back-panel-bulb-count`** - the Coil & Flash Lamp Locations page draws
   one `22` and one `30` callout in its back-panel inset, which makes both printed quantities
   add up, while printed page 91 lists exactly two `#89` sockets on the back panel and labels
   **both** of them `Q22 FLASH` with no `Q30` socket anywhere. This record follows page 91's
   explicit parts list for address 22 and gives it a `cabinet_or_service` record with
   quantity 2; address 30 carries no spatial key at all, because no placement set can match
   its printed quantity of three without choosing a side.
3. **`conflict.pop-bumper-position-naming`** - the manual names the three bumpers LEFT, RIGHT
   and BOTTOM on both its switch page and its coil page, and its locations plan draws the
   three coil callouts at the cluster's left, right and player-nearest positions in that
   order. The retained script binds them in naive numeric order instead, which makes its LEFT
   bumper the player-nearest one. Only one bijection between three names and three positions
   is geometrically coherent; the manual's two pages plus the table's own geometry agree on it
   against the script's identifier ordering alone, so this record uses the manual's reading
   for all six placements (switches 30/31/32 and coils 9/10/11) and records the disagreement
   rather than resolving it silently, because the runtime script is normally this project's
   authority for address semantics and it is the source being overruled.
4. **`conflict.coin-door-adjust-button-order`** - `sam.c` disagrees with itself about which
   red coin-door adjustment button is public -2 and which is -1: its descriptive comment
   block says D21 is Plus and D22 is Minus, while its own keyboard input-port table puts
   Minus on the bit that becomes -2. This manual agrees with the input-port table, so two
   sources against one resolve it that way. Recorded for provenance completeness even though
   both addresses are coin-door service buttons.

Two output addresses carry no spatial record at all:

- **Public solenoid 30**, for the reason in conflict 2.
- **G.I. address 0**. This manual prints no general-illumination bulb table anywhere. The
  only G.I. inventory it states is the ten back-panel `#44` sockets on printed page 91 and
  the three right-ramp LED modules the Lamp Locations page calls out ("THE 3 LEDS MODULES ON
  THE RIGHT RAMP ARE G.I.s; NOT CONTROL LAMPS"). The playfield G.I. bulb inventory is spread
  across the Section 4 assembly pages and was not exhaustively enumerated in this pass, so
  neither a bulb quantity nor a placement set is asserted. The retained table's own `GI`
  collection has 85 members, but many are co-located render doubles and ten are back-panel
  proxies, so it cannot substitute for the missing table.

Finally, this curation pass ran single-session and did **not** obtain the mandatory
independent high-tier cross-provider review described in `docs/INSTRUCTIONS.md`.
`recreation_notes` therefore stays in `coverage.missing` until that review runs against the
exact proposed tree, matching the precedent Bally Cirqus Voltaire and Williams Fish Tales set
for the same procedural gap.

## Two things worth carrying to the next Stern S.A.M. game

1. **Re-derive the lamp axis order from the game's own printed grid.** Stern's switch matrix
   and lamp matrix do not share an axis convention across platform generations: Whitestar's
   switch matrix is column-major and its lamp matrix row-major, and S.A.M.'s lamp matrix is
   row-major over ten rows by eight columns while its printed switch matrix is four drive rows
   by sixteen returns. Confirming the lamp mapping against `sam.c`'s own per-game
   `strncasecmp(gn, ...)` block - which names specific addresses on specific boards - is the
   cheapest independent check available, and on this game it agreed on all seven addresses it
   covers.
2. **`hw.custSol = 16` is a macro constant, not a per-game decision.** Every Stern S.A.M.
   game enumerates public solenoids 51-66 whether or not an auxiliary driver board is fitted.
   What differs between games is `gameSpecific1`: it selects which, if any, of `sam.c`'s six
   auxiliary write paths is enabled. Read that field before deciding whether 51-66 mean
   anything on a given machine.
