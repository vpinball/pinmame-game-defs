# Starship Troopers (Sega, 1997)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled; only `spatial_placement` is missing, because the retained table does not model
the trough, the under-troughs or the brain bug, ramp and pop flasher bulbs, the warrior bug and brain bug parts are
placed on the walls the script moves, the insert lamps are projected onto the table's insert lights, and no placement
has yet been checked against the factory location drawings**

## Identity and evidence precedence

This is Sega Pinball's Whitestar machine of December 1997, model 59, IPDB 4341, designed by Joe Balcer and Joe
Kaminkow; IPDB gives no production count. It covers the two `startrp` drivers of pinned PinMAME: `startrp` (CPU 2.01,
the root set) and its clone `startrp2` (CPU 2.00). `segames.c` builds both from `INITGAME(startrp, GEN_WS,
se_dmd128x32, 0)`: lower flippers only (`FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`), two extra lamp columns (lamps 1-80), no
custom solenoids, a 128x32 DMD and no auxiliary driver board. Both share the display ROM `sstdspa.200` and the sound
set, and `MACHINE_INIT(se)` treats every driver whose name starts `startrp` alike, so the two are `identical`. A
harness run exercised each.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks and mechanism
causality; the official manual (150 scanned pages without a text layer, the copy IPDB hosts) decides construction,
wiring, parts and placement on the drawings; pinned PinMAME decides routing. Two harness runs, one per driver, confirm
the routing and the switch-to-coil responses. Their scenario's notes say it closes each playfield switch once. Of the
placed matrix switches it toggles all but the trough positions 13-15 and the warrior bug's rear limit 33, held closed
from boot, its front limit 34, held open from boot, and the brain bug up switches 37 and 39, which it never writes; it
leaves the end-of-stroke inputs 81 and 83 to PinMAME. The retained table is the VPW Mod v2.0 recreation, which loads
`startrp2`; the pinned corpus script is byte-identical to its embedded script, so it corroborates the bindings but is
not independent.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). 1, 8, 11, 36, 44, 63 and 64 are NOT USED. 2 is
  the European 4th coin slot, 3 and 7 coin-door positions marked Future Use, 4-6 the right, centre (bill acceptor) and
  left coin slots, 54 Start, 55 slam tilt and 56 plumb bob. The dedicated inputs are -3 memory protect, -2/-1/0 the
  red/green/black service buttons (DS-6/7/8), 84 left button (DS-1), 83 left EOS (DS-2), 82 right button (DS-3), 81
  right EOS (DS-4) and 88, the mini flipper button (DS-5). 85-87 reach no input. The country selector is DIP bits 1-5.
- **Solenoids.** Public 1-32 are Q1-Q32 except the lower flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right)
  off public 15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left
  flipper coil at 48 and the right at 46; 45 and 47 are their power-phase states. The mini flipper Q14 stays at public
  14, driven by the ROM. Public 15 is PinMAME's fast-flip / game-on state (sega.vbs's `GameOnSolenoid = 15`); both
  drivers get the fast-flip byte at CPU RAM 0x00, and in both runs 15 rose when the served ball reached the shooter
  lane and fell at the drain. 16, 33-44 (no auxiliary board), 49 and 50 are unused. Q21 and Q22 are NOT USED. Q8 (the
  European token dispenser) and Q24 (the coin meter) are optional equipment.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column). Lamp 33 is NOT USED. Rows 7-10, columns 1-7,
  are the four 7-segment LED displays (49-55, 57-63, 65-71, 73-79); `se.c` types them as LED strobes.
- **G.I.** One relay, published as G.I. 0.

## Switch polarity and names

Whitestar's `switch_r` hands the CPU the complement of PinMAME's switch column and the driver's `invSw` is zero, so
public 1 is a closed contact. Every matrix switch here is a normally open contact. The trough opto 15 and the orbit
optos 47 and 48 read 1 with a ball in the beam. For the trough opto the board's theory text says so directly: the
blocked receiver acts as a closed switch. The orbit optos' 'Long-Hop' board text says the lit receiver 'makes the
switch', but the page prints no matrix rest state, so the record derives it as `docs/PLATFORMS.md` requires for
Whitestar, from the read path and a runtime proof. The known-working script holds 47 and 48 at 1 while the ball passes,
and in both runs the ROM answered a 100 ms 1 pulse on either one while the input was still 1, the right magnet rising
46-100 ms after the write. The contact therefore rests open. The EOS contacts 81 and
83 are N.C. on the flipper assemblies and open at the end of the stroke, but PinMAME does not take them from the host:
the driver's `FLIP_SOL(FLIP_L)` includes `FLIP_EOS`, so `core_updateSw` rewrites 81 and 83 on every update from the
flipper outputs 46 and 48, publishing 1 once a coil has been held for two updates. That is PinMAME's stroke model, the
reverse of the N.C. contact, and a host write to either address is overwritten.

Names follow the Switch Matrix Grid (DR. 4) and the printed page-21 table. The grid prints BRAIN BUG UP for both 37 and
39. The page-21 table calls 49 the TOP TURBO BUMPER, where the grid and the coil chart say LEFT: it is the top bumper
of the triangle, and the record keeps LEFT. The shared part cell beside 33-35 prints the roller micro switch 180-5119-00
three times, but the warrior bug target 35 is a stack switch (180-5133-00) on the bug carriage, per the assembly page.
Switch 16's part cell names only the switch assembly 500-5096-00, so its type is not recorded.

Two defects of the retained table do not reach the machine: its slingshot handlers pulse each other's switch (59 for
the right slingshot, 62 for the left), and `SolCallBack(8)` plays a knocker sound on the token-dispenser driver. The
manual and both harness runs pair 59 with the left slingshot Q12 and 62 with the right Q13, and the machine has no
knocker.

## Ball handling

- **Trough.** The 4-Ball Trough (OPTO) Assembly 500-6119-24 holds four balls on the roller micro switches 12 (left), 13
  and 14 and the up-kicker opto 15, which is ball position 1. Q1 kicks the ball on 15 into the shooter lane. Initialize
  12-15 at 1 with four balls loaded.
- **Shooter and auto launch.** A served ball rests on 16; the player plunges it, or Q2 fires the autoplunger. The
  shooter-lane shot runs into the right orbit.
- **VUK.** The VUK Assembly 500-5839-04 on the left side: a ball rests on 45 until Q3 kicks it up.
- **Super VUK and under-troughs.** Balls from the top exit hole (9) and the warrior bug's exit hole (10) roll through
  the Plastic Under-Trough 500-6244-00-59, which lists two micro switches 180-5057-00 (item 4, Qty. 2) and two
  1N4001 diodes. Balls from the pop exit hole (40) drop into the Mini-Under-Trough, the Metal Under-Trough (Small VUK)
  500-6243-00-59, which lists one switch (item 4, Qty. 1) with its diode on a terminal strip. Both lead to the Super
  VUK Assembly 500-6245-02-59; the ball rests on 46 and Q4 shoots it towards the right flippers. The manual names the
  pop exit path the Mini-Under-Trough and lists the 'Metal Mini-Trough' among the bottom-mounted assemblies; the
  assignment of 40 to the metal trough rests on those names and on the two troughs' switch counts.
- **Orbit magnets.** Two magnets Q5 (left) and Q6 (right) under the rear of the playfield, where the two orbits meet. A
  hard orbit shot with the left magnet on drops the ball into the top exit hole; with the right magnet on it goes into
  the top lanes; with a magnet off it completes the orbit. In both runs each orbit opto made the ROM fire the right
  magnet twice: a hold of 0.60-0.67 s that began while the input was still 1, and a 66-133 ms pulse about 2.1 s after
  the write. The detailed wiring diagram (printed page 88) feeds Q5, Q6 and the brain bug Q7 from the VIO/YEL 50V DC
  supply on J10-P3 (fused on the board by F20, 3A), each through its own 3A slow-blow fuse under the playfield by its
  assembly; Q7's coil side of its fuse is RED/WHT.

## Toys

- **Warrior bug.** Warrior Bug Assembly 500-6239-00-59: a bug carriage on a track at the upper left, driven forward
  and back by a unipolar HSI #36864-12 stepper (15 degrees and .004" per step, 12v DC, 4.6W) whose four phases are
  Q17-Q20. Roller switches 33 (rear) and 34 (front) sense the carriage at each end, and the target 35 rides it. Each
  hit pushes the bug back until the ball can reach the bug exit hole (switch 10). F5 (Q29) lights three #906 on the
  track and one #89 at its head, and lamp 34 (#555) sits at the head.

  The detailed wiring diagram (printed page 88) wires the motor's two centre-tapped windings: Q17 to RED and Q19 to BLK
  on one, Q18 to GRN and Q20 to BLU on the other, with both WHT taps on the +12V DC GRY/RED supply (J16-P3) and each
  phase's 1N4004 on a terminal strip below the playfield. Energizing 17, 18, 19, 20 in turn therefore alternates the
  windings one full step at a time. The direction comes from the known-working script. Its `cvpmMyMech` hands PinMAME's
  `mech.c` Sol1 = 17 in the four-step-solenoid mode (`vpmMechStepSol + vpmMechTwoDirSol`), where phases following in
  the order 20, 19, 18, 17 count the position up, toward the rear switch 33, and the order 17, 18, 19, 20 counts it
  down, toward the front switch 34. The script models the travel as 222 positions, with 34 at positions 0-1 and 33 at
  221-222; that length is the table's own, since the manual gives the .004" step but no travel length.

  The harness drove no mechanism, so 33 and 34 never changed. The ROM changed the phases at power-up, at the shooter
  lane, and from the bumper 49, the target 35, the bug hole 10 and the right orbit 48. The harness samples outputs
  about every 67 ms, too slowly to resolve the step order, so the runs do not show the direction themselves.
- **Brain bug.** Brain Bug Assembly 500-6256-00-59: the brain bug figure on a slide plate under the centre of the
  playfield, raised by the 22-1080 coil Q7 through a window flap, with three Cherry limit switches: 37 and 39 report it
  up, 38 a hit on it. Q23 lights two #89 beside its picture. No harness run raised it outside the ball search, so 37 and
  39 were never exercised; 38, closed once in each run while Q7 was off and the bug down, drew no coil, flasher or G.I.
  change. The retained table holds 37 and 39 at 1 while Q7 is on.

## Flippers

The lower flippers (500-5944-14 left, 500-5944-04 right, 23-1100 coils) get a 40 ms pulse on a button closure and then
1 ms every 12 ms while held, from one 50v supply; each N.C. EOS opens at full stroke. The ROM reads the buttons 82 and
84 and drives Q15 and Q16 itself (PinMAME publishes them at 47/48 and 45/46); PinMAME fakes no flipper output from a
button and synthesizes the EOS inputs, as above. The mini flipper (500-5944-02,
22-1080, fluorescent orange bat) sits right of centre above the trough. Its own N.O. cabinet button 88 (DS-5) is read
by the CPU, which fires Q14 itself. No EOS input is wired for it: the three-flipper circuit draws only the two lower
EOS switches, although the mini assembly's item range on the parts page takes in the EOS switch 180-5149-00. In both
runs holding 88 pulsed 14. The retained table fires its
mini flipper from its own key handler while 15 is set, with `SolCallback(14)` commented out.

Holding the right flipper button in the harness also drew a ball search (2, 7, 14, 9, 6, 10, 3, 11, 5, 12, 13 and 4,
a quarter second apart, continuing after release). It is the ROM looking for the ball last seen leaving the super VUK,
not a flipper response.

## Lamps, flashers and general illumination

- **Inserts.** Most inserts are #555 bulbs; 31, 32, 44, 45, 56 and 64 are #44. Lamp 40 lights both return lanes.
- **7-segment displays.** The 4X 7-Segment Display Board 520-5166-00 carries four 1" red MTN4126-CHR displays over the
  flippers: WARRIOR (lamps 49-55) top left, HOPPER (57-63) top right, PLASMABUG (65-71) bottom left and TANKER (73-79)
  bottom right, segment A-G in lamp column order. The board's solder-side note says CN1 pins 12-15 feed DISP1-DISP4
  "respectively", but its schematic and the lamp numbers put pin 15 (row 7) on DISP1; the record follows the schematic.
- **Tanker Bug sign.** Lamps 35, 36 and 39 light the Tanker Bug Sign over the super VUK: the Screened Plastic -20 Assy
  of the Tanker Bug Assembly 500-6254-00-59 (printed pages 59 and 61) carries three #555 bulbs in offset sockets under
  red, blue and fluorescent orange covers. The plastic stands upright, with 39 below 35 and 36, as DR. 5 draws it and the
  retained table models it.
- **Lamp 33.** The grid shades it NOT USED, DR. 5 draws no 33 and the table binds no light. The ROM's lamp shows still
  write the bit with the rest of row 5 (100 changes in each run), which PinMAME publishes whether or not a bulb is
  fitted.
- **Flashers.** F1-F4 (Q25-Q28) are one #906 under each red, yellow, green and blue dome of four groups of four (top
  left, top right, left side, right side). Each group is a 4X Light & Clear Plastic Assembly 515-6778-01-59, with four
  #906 bulbs under one Mini-Mars cover of each colour: three sit on the plastic ramp and one over the wire ramp by the
  Hopper Bug. The detailed wiring diagram labels the four groups '#555 Bulb ✻4', but the coil chart and the
  assembly's parts list both give the #906 165-5004-00. F5 (Q29) is the warrior bug's three #906 (165-5004-00) and one
  #89 (165-5000-89), so it has no single bulb part. F6 and F7 (Q30, Q31)
  are three #89 along the left ramp or the right side plus one at the lower left or right of the centre inserts. F8
  (Q32) is two #89 at the pops. Q23 is the brain bug's two #89.
- **G.I.** One relay switches 6.3v AC to four fused circuits: 10, 7 + 2, 7 + 2 and 6 + 2 bulbs, 36 in all, of which two
  (on circuit 3) light the coin door. The page warns that quantities may change during production.

## Spatial status and why the record stays partial

Every used playfield device except the brain bug, ramp and pop flashers has a placement from the retained table's object
coordinates, and every cabinet, service, virtual and unused address has a controlled `not_applicable` record. The record
stays partial because:

- the table does not model the trough switches 12-15 or the under-trough switches 9, 10 and 40 as switches, so they
  are projected onto the release kicker and the hole objects that pulse them;
- the warrior bug's stepper motor, end switches and target, the brain bug coil and its up switches, and lamp 34 are
  projections onto the walls the script moves, the motor onto the rear wall where the Warrior Bug Assembly drawing
  mounts it;
- the lamps DR. 5 draws below the playfield light inserts, and the table models no bulb or socket under the
  playfield: each is projected onto the bulb light the script drives at its insert, which gives the insert's position
  but not the socket's;
- the 7-segment LED segments are placed at the lit centres of the table's segment textures, which agree with the
  manual's A-G key but were not measured on a real display;
- no flasher Light draws a bulb of its own, so a flasher is placed only where the table models a part under its Light:
  the sixteen F1-F4 Lights each sit on a Mini-Mars dome and its socket, and two of F5's four bulbs are modelled on the
  warrior bug assembly. The brain bug flasher (Q23), F6, F7 and F8 have only render lights and glow sprites, so their
  twelve bulbs and F5's other two have no placement until the flash lamp location drawing (DR. 7) is measured or a
  table models them;
- the table models 28 G.I. sockets against the 34 playfield bulbs; the G.I. page gives each bulb's circuit and a
  broad region, not a socket position, so the six missing sockets need a factory socket drawing or playfield photographs;
- no placement has been checked against the factory location drawings (DR. 5 and DR. 7) by a callout fit.

## Author construction checklist

- **Ball path.** Four-ball opto trough with an up-kicker, shooter lane with auto launch, left and right orbits with
  magnets at their meeting point, two ramps (the left with a wire exit), three top lanes, three turbo bumpers, two
  slingshots, the VUK on the left, the super VUK fed by the under-troughs from the top, bug and pop exit holes.
- **Targets.** Two four-target banks down the left and right sides, the left ramp, pop and VUK pairs and the right ramp
  stand-up, the warrior bug target and the brain bug.
- **Toys.** The stepper-driven warrior bug with its end switches, and the pop-up brain bug with its three switches.
- **Initial state.** Initialize 12-15 and -3 at 1. Leave 81 and 83 alone: PinMAME rewrites them from the flipper
  outputs. Start the warrior
  bug at one end with its end switch closed.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases and 15 is game-on. Bind Q14 directly. Bind Q8 only
  with a token dispenser and Q24 only with a coin meter.
- **Displays and lights.** One 128x32 DMD in the backbox, behind the Showcase Bezel of the Backbox (Front Side) Assembly,
  and the four 7-segment LED displays on the playfield. Recreate
  the 34 playfield G.I. bulbs and the 2 coin-door bulbs, all lamps and flashers.

## Sources

- `manual.sega.starship-troopers.1997`: SHA-256 `0b773570c3ddaa38f6d63f7a590d4a8986f34facf70064cf3446cfc44ae22d09`,
  IPDB 4341's English manual; excerpts under `evidence/excerpts/sega.starship-troopers.1997/`.
- `identity.sega.starship-troopers.1997`: the IPDB machine page, read through the Wayback Machine.
- `vpx-table.starship-troopers-vpw-2-0` and its embedded script (`e97088ef...`), with the retained extraction and its
  manifest.
- `vpx-script.e97088ef82faf822`: the pinned corpus copy of the same script.
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `runtime.starship-troopers.startrp` and `runtime.starship-troopers.startrp2`: two LibPinMAME runs, summarized in
  `evidence/runtime/whitestar/starship-troopers-startrp-gameplay.json` and
  `evidence/runtime/whitestar/starship-troopers-startrp2-gameplay.json`.
- `legacy.game.sst`: the superseded migration record, kept only for its alias values.
