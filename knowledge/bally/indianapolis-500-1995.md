# Indianapolis 500 (Bally 1995)

Coverage: **partial**. Every address is enumerated and named, all construction, wiring, polarity,
mechanism and variant facts are validated from the factory manuals, pinned PinMAME and the retained
known-working table, and no conflict is open. The record stays partial only because the playfield
general-illumination sockets are known from one community table's light collections and are
therefore `observed`, not validated.

## Identity and drivers

- Midway Manufacturing Company under the Bally name, model 50026, released June 1995 (IPDB 2853,
  OPDB `Gr8l3-MDWr0`). The game ROM's own splash reads `INDIANAPOLIS 500 / 50026 REV. 1.1 R`.
- WPC-Security (WPC-S) hardware with a DCS sound board and a 128x32 DMD.
- PinMAME drivers: `i500_11r` (1.1R, parent), `i500_11b` (1.1 Belgian) and `i500_10r` (1.0R). All three
  are declared in `src/wpc/sims/wpc/prelim/i500.c` with the `wpc_mSecurityS` machine driver, share one
  `i500GameData` and the same six sound ROMs, and are the same physical machine.

## Evidence used

- **Operators Handbook** 16-10140, July 1995 (16 pages, Internet Archive
  `arcademanual_Indianapolis_500_OPS`): lamp, switch and solenoid tables with wiring and the location
  drawings. Transcribed with native-resolution crops under
  `evidence/excerpts/bally.indianapolis-500.1995/`.
- **Operations manual** (152 pages, IPDB `indy500manualfull.pdf`, image-only): the board and
  mechanism assembly pages that settle construction (A-19823, A-20047, A-19978, A-20038, A-20169,
  A-18159). The handbook's tables are repeated in it on printed 2-38 to 2-44.
- **Known-working table** `Indianapolis_500_VPX_1.1_RTM.vpx` (JPSalas VP9, Dozer VPX, Flupper ramps,
  2017) and its embedded script: runtime bindings and all geometry. Its two 4K MOD derivatives are
  the same geometry lineage.
- **VPW 1.36 script** (TastyWasps, 2023) from the pinned `vpxtable_scripts` corpus: same bindings,
  plus a separately driven upper right flipper.
- **Pinned PinMAME** `8371478a`: address routing, inverted-switch mask and the turbo model.

## Controller facts a recreation needs

- Switches use WPC column/row numbering `11-88`, coin door `1-8`, Fliptronic `111-118`.
- Opto switches, all already normalized in public state (1 = beam broken / ball present): trough
  41-45, lightup targets 56-58, upper popper 61, turbo popper 62, turbo ball sense 63 and turbo index
  66. PinMAME's mask `{..,0x1f,0xe0,0x27,..}` covers exactly these twelve. Do not invert them again.
- Switch 66 is an opto even though both printed switch matrices leave its cell unshaded: its part,
  A-20047, is the Turbo Opto PCB Assembly ("Opto Integrated 10mA").
- Fliptronic buttons 112/114/116 are cabinet optos; PinMAME's `WPC_FLIPPERS` read complements the
  whole column, so they too arrive normalized (1 = pressed). 111/113/115 are end-of-stroke leaf switches.
  117/118 (upper left) are not used.
- Switch 24 is the always-closed link; PinMAME closes it at reset. The retained table writes it open
  in `Table1_Init`, a defect in that table.
- Solenoids 1-28 are the printed drivers. 29-32 are WPC state channels (31 = Game-On, because no
  fast-flip address is configured; 32 always zero). 37-44 are dead on this generation. 49/50 are
  simulator/reserved.
- Flippers: lower right 45 (power) / 46 (power or hold), lower left 47/48, upper right 33 (power) /
  34 (power or hold). The printed flipper circuits 29-32 are the public 45-48.
- The Fliptronic upper-left circuits drive the pit-ramp diverter: 35 is its power winding, 36 its hold
  winding (raw bits, because the game declares no upper-left flipper).
- Solenoid 17 (Turbo Motor) and 18 (Race Track Motor) are printed in the Flasher category but drive
  motors; 17 is pulsed, and the turbo's speed follows the pulse spacing.
- G.I. strings: public 0 Upper Left Playfield, 1 Upper Right Playfield, 2 Lower Playfield (these three
  light the playfield; 0 and 2 also feed backbox bulbs), 3 Backbox-Coindoor and 4 Backbox Title
  (backbox only).
- Lamps 71-84 are red LEDs inside the three lightup targets, not bulbs. 67, 68 and 85 are unused;
  86-88 light the Launch, Buy-In and Start buttons.

## Mechanisms

### Trough and launch

Four balls sit on optos 42 (right, at the eject) to 45 (left); 41 (Top Trough) is a fifth opto on the
same trough. Solenoid 13 serves a ball into the shooter lane (25). Solenoid 1, a kicker at the foot of
the lane, launches it, automatically or when the player presses the Launch button (11). There is no
manual plunger.

### Turbo

The signature toy at the upper left. A ball entering the turbo popper (opto 62) is raised by solenoid 5
up the turbo feed ramp into the turbo, a horizontal impeller in a housing turned by a 12 VDC
gearmotor on solenoid 17. The impeller holds up to four balls in its quadrants; turning slowly it
stores them, spun up it throws them out onto the turbo exhaust ramp. Turbo Ball Sense (63) is an
LED/phototransistor pair through the housing wall and Turbo Index (66) is an opto board under the
impeller. PinMAME models the speed from the spacing of solenoid-17 pulses (stopped after roughly a
second without a pulse, fast when pulses come back to back) and closes 66 for three of every sixteen
steps of a 64-step revolution. The retained table's own turbo model advances four quadrants and
opens 66 once per quadrant, holding it closed for the rest; recreations need an index edge per
quadrant, and the exact duty cycle is not established by any source retained here.

### Race track

An upright arched track at the rear right of the playfield. Solenoid 18 runs its gear motor, which
carries a small car and driver around the arch. No switch reports its position; two reflector sockets
sit at the top corners of the arch.

### Pit ramp diverter

On the left side beside the three-bank targets. A plunger coil (35 power, 36 hold) turns a blade with
a large car and driver on it to divert the ball; a master spring returns it. No switch senses its
position.

### Poppers and kickers

- Upper popper at the rear (opto 61, solenoid 2) lifts the ball onto the rear wire ramp.
- Upper eject saucer at the top centre (switch 64, solenoid 3).
- Lower kicker at right centre (switch 65, solenoid 4, a hammer-style kicker arm).

### Targets, bumpers and slingshots

- Three lightup targets (56 left, 57 center, 58 right), each an illuminated target whose board
  carries the target opto and four red LEDs (lamps 71-74, 75-78, 81-84). "Upper" and "lower" LEDs
  differ in height on the upright board, not in playfield position.
- Three-bank orange targets 28/31/32 on the left, stationary targets 34, 46, 47, 48 and 55.
- Jets: Left 72 / solenoid 8, Right 73 / 9, Center 74 / 10 (the center jet is the lower one), each
  with a flasher in its wafer (23, 24, 25).
- Slingshots 26/11 and 27/12; switch 54 (Ten Point) is a rubber scoring switch at the right.

### Flippers

Three blue FL-11629 flippers: lower left, lower right and an upper right flipper at mid-right below
the right ramp, each with its own cabinet opto and end-of-stroke switch. The 2017 table moves the
upper flipper with the lower right callback; the 2023 VPW script drives it from its own address 34.

## Manual discrepancies worth knowing

- The lamp-locations list swaps the names of lamps 18 and 27 against the lamp matrix. The matrix is
  right: 18 (Turbo Wrench) sits by the turbo and 27 (Left Ramp Wrench) by the left ramp wrench target.
- Switch 63's LED/phototransistor is printed A-14231/A-14232 in the handbook and turbo assembly but
  A-16908/A-16909 on the 10-opto board page; both are optos.
- The flasher wiring drawing prints different wire colours for solenoids 14-16 than the solenoid table.
- Solenoid 12's assembly is printed `A-9362-R-3` in one list and `B-9362-R-3` in another.

## What would complete the record

A socket-level survey of the playfield general illumination on a real machine (or a factory drawing
assigning each G.I. socket to strings 1-3) would let the G.I. placements be validated and the record
promoted.
