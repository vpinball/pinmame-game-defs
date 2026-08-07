# World Cup Soccer (Bally/Midway, 1994)

Coverage: **partial — complete physical I/O inventory, WPC-Security bindings, mechanism causality,
driver-variant boundary, and recreation behavior validated; wiring conflicted pending resolution of
the Fliptronic-cabinet-opto polarity conflict (switches 112/114) below, and one solenoid (34) has no
spatial evidence of any kind**

## Identity and evidence precedence

This is the Bally/Midway WPC-Security physical product released May 1994 (document 16-50031-101),
IPDB 2361. It covers the fourteen-driver `wcs_*` clone tree: `wcs_l2` (parent, production LX-2),
`wcs_l3c` (2016 community "Competition MOD" firmware), `wcs_la2`/`wcs_l1`/`wcs_la1` (earlier
language/region firmware), `wcs_d2` ("LED Ghost Fix"), `wcs_p2`/`wcs_p3` (prototypes),
`wcs_p5`/`wcs_p6` ("LED Ghost Fix" prototype-lineage firmware), and `wcs_f10`/`wcs_f50`/`wcs_f62`/
`wcs_f62b` (FreeWPC community reimplementations). Every one of these is a game-ROM revision for the
identical physical machine; `wcs.c`'s `CORE_GAMEDEF`/`CORE_CLONEDEF` share one static `wcsGameData`
struct across all fourteen.

Evidence precedence for this definition: the retained known-working VPW v1.5 script is runtime and
mechanism-causality ground truth; the Midway operations manual controls physical construction, part
numbers, wiring, polarity, quantities, and device presence; pinned PinMAME controls controller
generation, public address topology, mechanism-table position ranges, and display metadata; the
retained VPX geometry supplies normalized coordinates. The retained manual PDF carries a genuine but
unreliable OCR text layer on its multi-column parts lists, so every printed table used here was read
from rendered pages and transcribed into
`external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md` and its per-table
excerpts under `evidence/excerpts/midway.world-cup-soccer.1994/`.

## Controller platform and address topology

`GEN_WPCSECURITY` (`PINMAME_HARDWARE_GEN_WPCSECURITY = 0x20`) with `wpc_dispDMD`. The controller
profile is `pinmame.wpc-security`, confirmed directly from `wcs.c`'s own `wcsGameData` declaration
rather than assumed from the task brief. Page 3 of the manual independently confirms the platform in
its own text: "This game uses a new Security CPU Board that is not downward compatible...".

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic
  111-118. `wcsGameData`'s inverted-switch mask `{0x00,0x00,0x00,0x3f,0x1f,0x07,0x00,0x00,0x00,
  0x00,0x00,0x00}` inverts column 3 in full (31-36), column 4 rows 1-5 (41-45), and column 5 rows
  1-3 (51-53) — fourteen addresses, exactly matching the printed matrix's own opto shading with
  **zero disagreement** in the ordinary 8x8 matrix. The mask's twelfth element (index 11, the
  Fliptronic column) is `0x00`, so it does *not* cover the printed opto shading on Fliptronic
  positions F2/F4 (public 112/114) — see the unresolved polarity conflict below.
- Solenoids: physical drivers 1-3, 5-6, 8-16 (all fitted, including 4 "Lock Release" and the
  backbox-mounted 7 "Knocker" — this machine genuinely has a knocker coil, unlike some other WPC-era
  games curated in this project); flashers/motors 17-28; Fliptronic upper-flipper circuits 33-35
  repurposed for Magna Goalie/Loop Gate/Lock Magnet, 36 unfitted; WPC-Security has **no** integrated
  LPDC board (unlike WPC-95/WPC-95DCS), so 37-44 are simply unused address space, not a duplicated
  range; Fliptronic lower-flipper circuits 45-48; PinMAME state channels 29-32 (31 never populated
  by this driver — see below); simulator-only 49 and reserved 50; a synthetic custom-solenoid mirror
  at 51 despite `wcsGameData` declaring `custSol = 0` — see below.
- Lamps: 8x8 matrix 11-88, every address populated (no "Not Used" lamp positions, unlike the switch
  matrix).
- GI: five strings on public addresses 0-4, three playfield (0, 1, 4) and two backbox insert-panel
  (2, 3).

Two WPC-Security numbering facts must not be lost. First, this generation's public solenoid
addresses for the lower flippers (45-48) match the manual's own printed circuit numbers exactly —
there is no LPDC remap to alias, unlike WPC-95. Second, `wcs.c` computes a genuinely dispatched
custom-solenoid address (public 51, `CORE_CUSTSOLNO(1)`) even though `wcsGameData` declares
`custSol = 0`: `core_getSol`'s `solNo > 50` branch calls `hw.getSol` unconditionally, regardless of
the declared count, and `wcs_getSol`'s own body returns `core_getSol(sDivHold) ||
core_getSol(sRampDiv)` — a live OR-combination readout of solenoids 16 and 8 with no physical
control line of its own. A recreation should bind one physical diverter mechanism to solenoids 8 and
16 and treat 51 as a derived diagnostic value, never a fourth device.

## Ball path, trough, and shooter

World Cup Soccer has an **automatic** plunger (`wcsSimData` declares `TRUE /* automatic plunger */`
and there is no cabinet Launch Ball switch in the matrix, unlike several other games curated in this
project). Five balls rest on trough optos 31-35 (31 nearest the eject coil, 35 nearest the drain
entrance), all printed opto and normalized by PinMAME's inverted-switch mask. Solenoid 6 ejects the
ball on 31 toward the shooter lane; the retained script's `SolTrough` handler fires that kick and
pulses Trough Stack (36) in the same event. Pinned PinMAME's own internal ball-routing simulator
(`wcs_stateDef`, cited here only for switch/solenoid name cross-reference, never as physical
mechanism authority) places the `"Trough stack"` state immediately after the trough-eject state and
before the shooter-lane skill states, confirming switch 36 senses the ball's staging position toward
the shooter lane rather than a sixth ball resting in the trough — it has no dedicated VPX object of
any kind and is a documented projection onto the trough-eject `Kicker.sw31` position. The ejected
ball rests on shooter-lane switch 38 (Ball Shooter); the retained script's `cvpmImpulseP` helper
auto-fires an impulse coil with no distinct public WPC-Security solenoid address of its own. Three
printed optos then trip in sequence down the skill-shot lane — Front (51), Center (52), Rear (53) —
built from the identical LED/phototransistor construction (`A-16908`/`A-16909`) as the Goal/Goalie
hole optos on the "10-Switch Opto Assembly" board.

## The goalie: motorized figure, position optos, and target ring

A DC gearmotor (`A-17741` Goalie Unit Assembly) drives the goalie figure one-directionally,
reversing at each end of travel (`wcs_goalieMech`: `MECH_LINEAR|MECH_REVERSE|MECH_ONESOL`,
`WCS_GOALIETIME = 50`, `WCS_GOALIESLACK = 10`). `wcs_handleMech` sets public switches 43 (Goalie Is
Left) and 44 (Goalie Is Right) directly from the motor's position counter (`mech_getPos(0)`), but
**only while solenoid 21 is actively driving the motor** (`if ((mech & 0x01) && core_getSol
(sGoalieMot))`). Solenoid 21 is printed under the manual's "Flasher" type column with a "* +12VDC"
footnote rather than a normal flashlamp part number; this is a printed-table category quirk, not a
device conflict — `wcs.c`'s own `#define sGoalieMot 21` and the retained script's `SolGoalie`
handler (which plays `fx_goaliedrive`, a motor sound, not a flash effect) both independently confirm
the real function. The same pattern applies to solenoids 23/24 (the spinning-ball turntable motor,
below).

The retained VPW script does **not** read PinMAME's mechanism position at all: its own `UpdateGoalie`
routine runs an entirely independent sinusoidal position simulator (`GoalieTheta` incrementing every
frame) and asserts switches 43/44 directly from that simulation's own angle. Both switches are
therefore documented projections onto the goalie figure's own table object (`Primitive
BM_goalkeeper`) rather than fixed playfield sensors; the retained script's own `InitGoalie` sets
`BP_goalkeeper.x=376/.y=280`, matching this primitive's stored position (374.4, 281.5) almost
exactly, which is what confirms the projection target rather than an arbitrary nearby object.

The goalie's own 35-segment target-wall ring (`GoalieWalls`, retained-table objects `HitTarget.
GT006` through `GT040`) surrounds the figure; `GWalls_Hit` fires the shared handler and pulses
Goalie Target (48, part `A-17779`) whenever a ball strikes whichever single segment is currently
collidable, the same "rotating figure with a segmented hit ring" pattern already documented
elsewhere in this project for a different WPC machine's rotating antagonist figure. Switch 48 is
likewise a documented projection, here onto the nearest fixed reference in the same script region
(`Trigger.swPlunger`, which shares switch 38's exact coordinates) rather than an invented
target-wall centroid.

## The spinning soccer ball and the two magnets

A separate DC gearmotor turntable (`A-17569` Motor Assembly with an `A-16120` DC Motor Control
Assembly H-bridge driver board) spins a small soccer-ball toy under a plastic dome. `wcs_ballMech`
(`MECH_LINEAR|MECH_CIRCLE|MECH_TWODIRSOL`) models it as continuous two-direction rotation with no
discrete position switch; the retained script's `cvpmTurnTable` helper drives the visual spin
directly from solenoids 23 (clockwise) and 24 (counter-clockwise), both — like solenoid 21 above —
printed under the "Flasher" category with a "* +12VDC" footnote despite being motor drive lines.

Two independent playfield magnets complete the electromechanical inventory. Solenoid 33 (Magna
Goalie, `20-9247`) energizes a magnet (`cvpmMagnet` on the retained table's `MagnaGoalie` trigger,
strength 16, `GrabCenter = False`) that deflects rather than captures the ball, helping the player
save a shot that would otherwise drain. Solenoid 35 (Lock Magnet, also `20-9247`) energizes a second
magnet (`LockMagnet` trigger, strength 40, `GrabCenter = True` — genuinely halts the ball at the
magnet's center) that holds a locked ball for the multiball feature. Neither magnet has a dedicated
playfield switch; both are tracked purely in game software.

## Fliptronic circuits repurposed for Magna Goalie, Loop Gate, and Lock Magnet

World Cup Soccer has no upper flippers (`wcsGameData.hw.flippers = FLIP_SW(FLIP_L | FLIP_U) |
FLIP_SOL(FLIP_L)` — switches for all four flipper positions are read, but only the lower-flipper
solenoids are driven). The manual's own two tables on the same printed page (2-48) directly confirm
this by driver-transistor identity: solenoid 33 (Magna Goalie) shares `Q2`/`J902-6`/`Yel-Vio` with
the generic Flipper Circuits table's "Up Rt. Power" row; solenoid 34 (Loop Gate) shares `Q7`/
`J902-4`/`Org-Vio` with "Up Rt. Hold"; solenoid 35 (Lock Magnet) shares `Q1`/`J902-3`/`Yel-Gry` with
"Up Lt. Power". The fourth upper-flipper position, Up Lt. Hold (`Q5`), has no solenoid-table row at
all and is genuinely unfitted (public solenoid 36).

Solenoid 34 is the one address in this definition with **no** spatial evidence of any kind. The
manual's own two tables even disagree on its name — "Loop Gate" on the primary Solenoid/Flasher
Table (matching `wcs.c`'s `#define sLoopGate 34`) versus "Lock Gate" on the Solenoid/Flasher
Locations parts list, for the identical coil part (`A-14406`) and assembly (`A-17796`, "Ball Gate
Actuator Assy." on the Lower Playfield Parts list). Unlike the ramp diverter and ramp lock post
below, an exhaustive search of the retained table's `gameitems/` directory and `script.vbs` found no
Gate, Flipper, Wall, Trigger, or Light object and no script reference of any kind for this address.
Its playfield location is not asserted.

## Ramp diverter, ramp lock post, and the Fliptronic column's opto polarity conflict

Solenoid 8 (Ramp Diverter) swings a diverter flap (`A-18138`) and solenoid 16 (Diverter Hold) holds
it in the diverted position; the retained script toggles two collision walls together. Left Ramp
Diverted (71) is the printed switch for this mechanism. Solenoid 4 (Lock Release, fully fitted —
verified at 600 dpi after an initial mis-transcription, see the manual-transcription review
artifact) retracts a post (`A-18155`) that otherwise holds a ball on the left ramp, sensed by Lock
Mech. Low (76) and Lock Mech. High (77) — a *mechanical* ramp lock distinct from the magnetic Lock
Magnet feature above.

**Unresolved polarity conflict (`conflict.flipper-cabinet-opto-not-normalized`):** the switch-matrix
page shades Fliptronic positions F2/F4 (public 112/114, the lower-right/lower-left flipper cabinet
buttons) exactly like the ordinary opto columns and prints them "Right/Left Flipper Opto". The
`A-17316` board/assembly page independently confirms genuine opto-interrupter construction (item 1
`03-9001 Interrupter Flip-Opto`; item 2 `A-16384 Flipper Opto Switch Assembly`, built from an "Opto
Inter Lg. 10mA" component) — so the switch-locations parts list's plainer "Lower Right/Left Flipper
Cabinet" description is not a contradiction, just a less specific label for the identical hardware.
But `wcsGameData`'s inverted-switch mask has twelve elements (columns 0-11, one per switch-matrix
column including the Fliptronic column at index 11); its twelfth element is `0x00`, so unlike the
fourteen ordinary-matrix opto addresses, PinMAME does not normalize 112/114 despite the confirmed
physical construction. This keeps `physical_wiring` conflicted and the record `partial`; resolving
it needs a LibPinMAME harness trace of a legal `wcs_l2` ROM observing the idle and active public
state of 112/114 as both lower flipper buttons are pressed and released.

## Other toys and standard devices

A ball resting on opto 42 (Goal Popper Opto) is kicked by solenoid 1 to award a goal; Goal Trough
(41) senses a ball en route. A ball resting on opto 45 (TV Ball Popper) is kicked by solenoid 2.
Three ordinary VUK-style kickers cover the Upper/Left/Right Eject Holes (solenoids 5/15/14, switches
55/56/54) — `wcs.c`'s own `#define` names (`swLHole`/`swRHole`) additionally tie 56/54 to the
printed "Left/Right Free Kick Hole" feature, and the internal simulator calls 55 the "Assist Hole".
Three `A-9415-2` jet bumpers (solenoids 9/10/11) are sensed by switches 81/82/83; the retained
script's `Bumper1_Hit`/`Bumper2_Hit`/`Bumper3_Hit` handlers reveal that table object `Bumper2` is the
printed "Left" jet bumper and `Bumper1` is the printed "Upper" one — an object-index crossing
confirmed directly from the script rather than assumed from either label. Two slingshots (solenoids
12/13, score switches 84/85) each carry a direct-fire kick switch (`SW-1A-114`) and a separate
debounced score switch (`SW-1A-120`) wired to one public address. A ball in the left outlane trips
Kickback (86); when lit, solenoid 3 fires the kickback plunger, and Kickback Upper (26) senses the
return path while also doubling, per PinMAME's own internal naming, as the Header Lane sensor for
the same physical lane.

## Fliptronic column: lower flippers

Two `FL-11629` (Blue) flippers on Fliptronic circuits 111-114 (lower right/left, EOS then
button-opto). The ROM energizes the power winding on the cabinet button opto (112 right, 114 left),
then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes.
World Cup Soccer runs `Const UseSolenoids = 2` (fast flips). Fliptronic positions 115-118 are
printed Not Used on both the switch matrix and the switch-locations parts list; there are no upper
flippers.

## Lamps and general illumination

All 64 lamp-matrix addresses are populated; unlike the switch matrix, no lamp position is printed
Not Used. Four addresses drive two bulbs each — 46 "Ultra Spinner", 47 "Ultra Jets", 71 "Light
Jackpot", 78 "Ultra Ramps" — and unlike the brightness-doubled lamp pairs documented for some other
WPC-era games in this project, the manual prints a **distinct assembly number for each bulb** of
every pair, and the retained table's second `Light` object for each address sits at a materially
different playfield coordinate (not a co-located stack). Both bulbs of each pair are therefore
recorded as genuinely separate placements. Lamps 87 and 88 are the bulbs inside the illuminated
buy-in and start buttons; the retained table places both `Light` objects at normalized y > 1,
outside the playfield surface, independently confirming cabinet mounting.

General illumination splits three ways on the retained script's `GIUpdate2` dispatch, which
implements only `Case 0` (drives collection `GILeft`), `Case 1` (`GIRight`), and `Case 4` (`GITop`)
— with **no** `Case 2` or `Case 3` at all. This matches the manual's own wiring table exactly: GI
strings 0, 1, and 4 (printed 01, 02, 05) are the only three with a Playfield voltage/drive
connection printed; strings 2 and 3 ("Insert Background"/"Insert Title") are Backbox-only. Unlike
several other WPC-era games curated in this project, there is **zero** disagreement here between the
manual's physical wiring and the script's runtime implementation. Three `GITop` members (GI034,
GI035, GI036) sit at normalized y = -0.021148, just outside the playfield's 0..1 bounds near the top
rail; their y is clamped to the schema-valid boundary 0.000000 with the raw offset disclosed in the
spatial report, the same handling this project has already established for a small negative-offset
lamp row on a different WPC machine.

## Author construction checklist

- Build the five-ball trough with the drain at Trough Ball 5, the automatic-impulse shooter lane,
  the three-opto skill shot, both slingshots, three jet bumpers, the motorized goalie with its
  35-segment target ring, the spinning-ball turntable, the two independent magnets (Magna Goalie
  deflect-only, Lock Magnet capture), the mechanical ramp lock post, the ramp diverter, the Goal and
  TV poppers, the three eject holes, and the kickback.
- Preserve opto polarity for 31-36, 41-45, and 51-53; do not invert what PinMAME already normalizes.
  Switches 112/114 are also printed opto interrupters, but PinMAME does not normalize them — treat
  their polarity as unresolved (`conflict.flipper-cabinet-opto-not-normalized`) rather than assuming
  either convention.
- Do not place solenoid 34 (Loop Gate/Lock Gate) anywhere on the playfield; no evidence supports a
  coordinate.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the printed Not Used
  positions, Fliptronic 111-118 with 115-118 not installed, the eight CPU DIP bits, solenoids 1-51
  (36 unfitted; 37-44 unpublished on this generation; 51 a diagnostic mirror only), lamps 11-88, GI
  0-4, and the 128x32 DMD.
- Solenoids 21, 23, and 24 are motor drive lines despite being printed under the manual's "Flasher"
  type column; do not model them as flash lamps.

## Sources

- `manual.midway.world-cup-soccer.1994`: Midway World Cup Soccer operations manual, SHA-256
  `29fd3c44c9ddcf5f965270011c71d34a701c13095cbeb286e26e62201931e48e`.
- `manual-support.midway.world-cup-soccer.1994`: retained human transcription index, SHA-256
  `7055d31403f69bedd4dffa94aad45952c18e75065941e204338eb9a818690f75`.
- `vpx-script.wcs-vpw-1-5`: retained known-working VPW v1.5 embedded script, SHA-256
  `c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5`, binding `wcs_l2`.
- `vpx-table.wcs-vpw-1-5`: retained table, SHA-256
  `ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d`, bounds
  `left=0 top=0 right=952.941 bottom=2152.941`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/wcs.c` and the WPC-Security core/solenoid/
  flipper handling at the pinned revision.
