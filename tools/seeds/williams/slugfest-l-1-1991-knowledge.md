# SlugFest (First Model), Williams 1991

Coverage: **partial**. Model 60001 is identified and its physical I/O and moving
inventory are documented, but physical emitter/sensor measurements, exact cam
behavior, generic emulator inputs/J111 physical loads and later dispenser configurations
remain bounded gaps. The raw insert/light references are candidates in the spatial
report; they are not promoted into physical bulb positions.

## Physical identity and firmware

The April 1991 manual 16-60001-101 and verified IPDB 3281 page establish Williams
SlugFest first model 60001, manufactured March 1991, two players, a WPC Dot Matrix
bat/baseball redemption game. Its original card dispenser is A-14471. The blue
Double inserts, white base squares, red instruction banner under the glass and
red cabinet trim distinguish this version in photographs. The retained user-supplied
VPX is DancingCan's 1.2, with Roccodimarco, Tab and Destruk ancestry and the embedded
VPW physics/sound credits. It selects `sf_l1`; no differently named table or edition
supplies its coordinates.

Pinned PinMAME `97aa922bf8e4b6970126192ec1ac1fb0305a4f62`, `bowlgames.c:477–502`,
groups production `sf_l1` and its `sf_d1` LED Ghost Fix on the same `sfGameData`,
`wpc_mDMDS`, WPC-DMD generation `0x4` and three sound ROMs. The LED fix changes
lamp timing, not the physical inventory. This project's shared pre-Fliptronic
controller profile is named `pinmame.wpc-alpha`; that profile name does not turn
this game's 128x32 DMD into an alphanumeric display. It has no physical flippers,
no copied matrix-flipper inputs, no declared custom mechanism handler and no
extra lamp columns. The DMD occupies the rear upright speaker/display assembly;
its callback index is 0.

The parts supplement 16-9190-B explicitly gives model 60021 a separate operations
manual 16-60021-101 and says its assemblies are identical except for the dispenser.
Original A-14471 and revised A-14471-1 share the gear motor and board but have
different magazine/pressure/lock parts and original A-14315/A-14316 versus revised
A-17231/A-17232 optical parts. Model 60021 also has documented artwork changes.
IPDB 6023's model 60121 lacks sufficient retained documentation for a validated
hardware/year/ROM compatibility claim. These are related physical versions, not
duplicate owners of `sf_l1`. This record's baseline remains 60001; full reproduction
of later dispensers and ticket conversion is not claimed.

Amendment 3 changes screen A-14563 to A-14811 from serial 730516; Amendment 4
changes hinged door A-14612 to A-14940 from serial 731027. These first-model
production changes are not new ROMs. Amendments 1/2 change pricing/redemption
defaults and presets: the later factory baseline is 25c per inning/$2 for nine
innings, one card per quarter or six tickets per quarter. The ROM's operator
configuration controls awards; do not implement one obsolete default in table
physics. The ticket dispenser is an alternative operator configuration, not a
second card motor on the same playfield.

## Controller contract and physical construction

The definition enumerates all dedicated inputs 1–8, all 64 matrix positions 11–88,
the generic flipper column 111–118, eight CPU option bits, solenoids 1–50, all 64
controlled-lamp positions 11–88 and GI callbacks 0–4. Every unfitted printed matrix
cell remains visible. The two blank lamp cells 87/88 are recorded as blank in the
excerpt, separately from explicitly printed Not Used switch and coil cells.

Controls 25/26/31–38 are on the separate control panel. Button 26 requests the bat,
37 starts one player and 38 two players. Four pitch buttons 32/33/34/35 request
fast/change-up/curve/screw; one-player mode lets the ROM choose a pitch. 31 is
Pinch Hit, 25 Steal Base/Run, 36 Throw Out Runner/Boo. Dedicated switches 1–4 are
coin chutes; 5–8 are credit/escape, volume-down/down, volume-up/up, test/enter.
Coin door 22 is held active while running the table, and constant 24 is held active.
Unjammed 28 is an operator acknowledgement button, normally released. The table's
held-active healthy-state substitution is a table defect, not a construction fact
or a canonical startup requirement.

The WPC matrix is read directly. `sfGameData` masks 54/55 and 61–63, so the active
high public states for those optical events represent normally-closed matrix
contacts. Prize 23 is optical but unmasked; its positive prize event reaches a
normally-open matrix contact. The pitcher assembly proves optical construction
for 54 even though the switch-location table puts motor part 14-7959 in its part
cell. Do not apply controller-wide inversion again. Physical optical-beam rest,
mechanical parking and the public `initial_active` setting are separate concerns.

Switches 41–47 are seven consecutive left-to-right target contacts. The switch
locations list transposes center/3R on 44/45, but its drawing, the matrix and the
actual `41 + targetIndex` script handlers agree that 44 is center and 45 is the
first target to its right. This is a settled source misprint, not an unresolved
conflict. Target 1R/2R wording in the lamp table is retained literally in its
excerpt; no physical order is reversed to accommodate a label.

Coil 1 powers the bat; 2 is the one under-playfield pitch magnet; 7 is the cabinet
knocker. 21 is the center-ramp motor. 22/23/24 are three electrical drive branches
of **one** 14-7959 pitch motor: the game's own A-14381 regulator drawing shows
their separate resistor paths joining one motor. Do not instantiate or count
three motors. 27 is the original card-dispenser motor. 28 is its low-card lamp,
despite being transported through a solenoid callback. 17–19 are #806 flashers in
the rear upright Bleachers Assembly; 20/25/26 are #912 ramp flashers on the
playfield. Bleacher controlled lamps 11/21/31 are independent #555 circuits,
not copies of the flasher callbacks. The retained AllLamps collection omits all
three; that is a table omission, not evidence of absent hardware.

Outputs 29/30 are used virtual mirrors of WPC_GILAMPS bits 5/6: pinned code
defines their register-state meaning even though attached J111 loads and this
game's physical use remain unproven. Output 31 is the physical RLY1 on the
fitted rear-cabinet A-12697-1 Power Driver Board. The game's manual names relay
part 5580-08994-01; its schematic shows T7 through R208/Q99 driving the coil.
The BOM says 4PDT while the drawn symbol says DPDT; neither reading establishes
additional contacts or fitted flippers. Pinned code exports the controlling
WPC_GILAMPS bit 7 at 31, observed during native service navigation. There is no
game-on output 19. Output 32 is an unused constant-zero virtual state channel.
Core code can fabricate virtual 45–48 from generic buttons 112/114 with 31 enabled,
even though this machine has no flippers. These must not be interpreted as bat
power/hold windings. The generic column is preserved without inventing physical
flippers or claiming the ROM never reads a bit merely because a probe names no
switch. Outputs 32–44 and 49/50 have no fitted device through this game's declared
pre-Fliptronic/no-simulator paths.

## Mechanics and ball conservation

Six physical balls and approximately 7° playfield slope are factory requirements.
The rear/back-row trough 51 and front strike trough 52 feed adjustable passive
return ramps and the lowest trough leading to one pitcher. The cabinet trough
must be higher than the playfield trough when clamped down. A recreation must
conserve six balls through visible pitching, rear capture, strike return and
grandstand routes; creating a new ball per pitch hides jams and corrupts occupancy.
The game's switch-location table fits part 5647-12133-08 at both trough contacts.
The factory Red Parts Catalog 16-9190-B, printed 6-12, identifies this exact
component as a microswitch. The shared component table establishes its type;
the game's own manual establishes where it is fitted. See
[the complete component table excerpt](../../evidence/excerpts/williams.slugfest-l-1.1991/component-microswitches.md).

The A-14356 pitcher encloses a motor-driven pitch plate between curved guides
and two spring-steel covers. It rotates clockwise viewed from the left, with a
timing cam through the opto bracket. Its front-pointing arm is the unblocked home
state 54. Fast/medium/slow outputs choose motor speed; the magnet affects slow
pitches much more than fast ones. Too much guide pressure prevents a slow ball
from feeding, and incorrect upper cover/deflector adjustment launches a fast
ball into the air. T.13 reports PITCHING, BLOCKED/UNBLOCKED and ERROR. The
retained script's trajectory forces, ball radius, deadlines and opto windows are
implementation tuning, not factory dimensions or measured motor timing.

A-14464's bat coil/plunger pulls its drive arm and roller linkage against an
extension spring, swinging the bat around its shaft. The spring restores rest
against an adjustable stop/bumper. The assembly's A-14789 coil-assembly name
and the driver table's A-14499 identify separate documented source roles.
Button 26 is a command, not an EOS. The current table deliberately moves the bat
from `BatPress/BatRelease` and only observes coil 1; that fallback is not proof
that the physical coil is optional or that its duty follows the fallback timing.

A-14290's single lift motor and cam cycle the center ramp up and down. The
motor is counter-clockwise viewed from the left; opto 55 is normally unblocked
when stopped. Clear feedback alone does not identify which height the cam has
reached: phase/history is required. T.12 reports MOVING, BLOCKED/UNBLOCKED and
ERROR. The table initializes down and models phase-dependent occlusion; its
assumed angular windows, endpoint timing and startup suppression do not measure
the factory cam. Preserve a failed transition as a jam/error, rather than clearing
the error merely because a command was sent.

Seven A-14452 target panels in A-14150 rotate independently and actuate their own
A-14697 switch wires. They are not a drop-target bank and have no reset coil.
The ROM owns which lit result scores. A rear wireform/deflector routes a returning
ball. A-14446's three shaped grandstand return ramps have independent left,
middle and right opto paths 61/62/63 using A-14315 emitters/A-14316 detectors.
They sense passage into gravity returns, not the height of the center ramp.

Original A-14471's A-14469 gear motor, A-14527 cable/pulley, piston, guide rod
and extension spring form the card-feed linkage beneath the pressure-loaded
magazine. Optical prize 23 confirms passage and low 27 reports stock. Operator
Unjammed 28 acknowledges a corrected jam/empty condition and resumes remaining
awards; it does not continuously sense healthy feed. Low lamp 28 is off normally,
on for low stock and blinks when jammed/empty. A.6.06 chooses stop or ignore
dispenser errors. The factory capacity is about 1,030 cards,
with around 30 left when considered empty; about 1,000 can be dispensed per fill.
Card thickness and one-card chute gap matter: the next card can retain the
dispensed one, and excessive humidity or unsuitable cards can stop feed. The
table's 15-card stock and 120/180/60/140 ms cycle are simulation choices. In a
recreation, acknowledge a card only when it actually advances; a motor command
alone must not award one. A fault can leave prize 23 quiet; recovery requires an
operator press of 28 after the physical fault is cleared.

The knocker is a cabinet striker with no ball route or sensor. Three control
speed branches, a magnet, a knocker and a card-low lamp must not be conflated
with interchangeable coils merely because they share the solenoid transport.

## Spatial evidence and remaining work

The retained extraction is exact:3,636 files/741,886,310 bytes, manifest
`3e31614714de9b6d84f5817b5188c73ae1536f4165015f98329f12eda0c91730`.
It is reproducible with the repository manifest helper, including every sorted
relative POSIX filename, size and SHA-256. The table bounds are 0,0 to 1100,2000;
coordinates use x left 0/right 1, y rear 0/front 1, rounded to six places.

Seven card-face trigger centers are explicit observed projections for the hidden
target contacts. They are not surveyed switch-wire centers. The 53 script-bound
insert Lights are invisible non-bulb insert overlays; their raw centers are useful
report-only references, not canonical emitter coordinates. Three script-bound
ramp-flasher Lights also remain report-only candidates until reconciled with
actual #912 sockets. No registration anchor, baked primitive origin, lightmap
receiver or Flasher sprite supplies an asserted physical placement. The report
keeps all candidate object names and raw coordinates so a future physical survey
can resolve them without re-extracting the table.

Bleachers/backbox displays and lamps and the separate control-panel lights are
classified cabinet/rear-panel from the factory assemblies, including control
Light objects beyond y=2000; they are never clamped onto the playfield. Five GI
strings are physically named and wired. Backbox and four pitch-control #555s
use cabinet classification. Actual playfield socket counts/positions on GI0/3/4
are unknown. The script explicitly calls several cohorts regional/provisional;
their helpers cannot establish electrical branch membership or bulb quantities.

Promotion requires a reconciled physical bulb/sensor/actuator survey, measured
pitch/ramp cam geometry and response behavior (including startup and jams),
bounded meaningful use of the generic inputs and any fitted J111 loads, and full documented
later-dispenser/ticket option behavior if those versions are to be claimed.
Retained sources, excerpts, exact hashes and runtime scenarios are portable in
the definition; full manuals, community VPX, ROM bytes and raw traces stay in
the external evidence roots. No unresolved physical disagreement is disguised
as a source-name conflict, and independent review does not confer maintainer approval.
