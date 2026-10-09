# Black Rose (Bally, 1992)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism and
recreation note is source-reconciled; `spatial_placement` is missing, because the three playfield
general-illumination strings' bulb positions rest on one community table, no retained drawing locates
them, and the two Top Popper flashers have no defensible placement, and `variant_differences` is missing,
because no retained source describes the prototype machines the `br_p17` and `br_p18` ROMs ran on**

## Identity and evidence precedence

This is the Midway (trade name Bally) WPC-Fliptronic physical product released July 1992, model 20013,
IPDB 313, 3,746 units: the pirate game with the ball cannon. It covers the eight `br_*` drivers: `br_l4`
(production L-4, PinMAME's parent), `br_l3` and `br_l1` (earlier production revisions), the community
LED Ghost Fix builds `br_d4`, `br_d3` and `br_d1`, and the prototypes `br_p17` and `br_p18`. All eight
share one `brGameData` and run on the same `wpc_mFliptronS` hardware. The production and LED Ghost Fix
revisions are `identical` to the physical machine; the prototypes' physical compatibility is `unknown`:
shared `brGameData` proves their routing, but no retained source describes the pre-production hardware. The catalog's 1993 year on `br_l4` and `br_l3` is the
firmware's; the machine shipped in July 1992 and the manual's cover reads August 1992.

Evidence precedence: the retained known-working VPW v1.4 script (`Const cGameName = "br_l4"`) is runtime
and mechanism-causality ground truth; the operations manual 16-20013-101 (an image-only 300 dpi scan)
controls physical construction, part numbers, wiring and device presence; pinned PinMAME controls the
controller generation and public address topology; the ROM's own service tests, run on a legal L-4 ROM,
settled the polarity and the names the ROM prints; the retained table supplies coordinates. Every table
used was read from rendered pages and is transcribed under `evidence/excerpts/bally.black-rose.1992/`.

The L-4 ROM's test menu differs from the manual's list, which was written for earlier firmware: it adds
T.12 FLIPPER COIL TEST and T.13 ORDERED LAMP, so the manual's "T.12 Cannon Test" is T.14 on L-4 (its own
screen still prints `T.12`).

## Controller platform and address topology

- Platform `pinmame.wpc-fliptronic`, hardware generation `0x8`, a 128x32 DMD.
- Switches: dedicated coin-door inputs 1-8 (5 Escape, 6 Down, 7 Up, 8 Enter in the menus), the 8x8
  matrix 11-88, and the Fliptronic positions 111-118. Matrix positions 11, 12, 23, 67, 68, 73-75 and
  77-88 are Not Used. 24 is the always-closed switch, which pinned `wpc.c` forces closed at start-up.
- `brGameData`'s inverted-switch mask is all zero and the machine has no optos in its matrix (23's
  "Ticket Opto" name is vestigial), so every fitted matrix switch is active at public 1 and rests open.
- Solenoids 1-28 are the power-driver outputs (12 and 16 Not Used); 29-31 are PinMAME's GILAMPS mirrors
  (`init_br` sets no fast-flip address), 32 is constant zero, 37-44 are unused (no LPDC on this
  generation), 49 is the simulator's shooter channel and 50 is reserved; `brGameData` declares no custom
  solenoids.
- Flippers: `FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR)`. Lower right 45/46 with EOS 111 and
  button 112, lower left 47/48 with 113/114, upper right 33/34 with 115/116. There is no upper left
  flipper: 35/36 and 117 have nothing fitted.
- Lamps 11-88 in WPC column/row order; GI 0-4 are the printed strings 01-05.

## Switch polarity and names: what the ROM's own tests settled

The T.1 SWITCH EDGES run drove every fitted playfield and cabinet switch except 13, 21, 22 and 24 to 1
and back. The ROM named each one at public 1 with its matrix row and column wire colours (for example
`OUTHOLE / WHT-GRN GRN-BRN` for 15) and cleared the name at 0. (Its frames for 37 and the T.8 frame for lamp 46
clip the leading R of RIGHT RETURN LANE at the display edge.) Inside T.1 the ROM still fires the sling
and jet coils from their switches (28 -> 6, 38 -> 5, 46 -> 13, 47 -> 14, 48 -> 15) and the flippers from
their buttons.

That run settles the one real disagreement inside the manual: the Switch Locations list prints 47
"Bottom Jet" and 48 "Right Jet", while the Switch Matrix prints 47 Right Jet and 48 Bottom Jet. The ROM
names 47 RIGHT JET and 48 BOTTOM JET and fires the Right and Bottom Jet Bumper coils from them, and the
list's own drawing and the retained script agree, so the list's two description cells are transposed.

Pressing 116 fired the upper right flipper (33/34): the right cabinet button breaks both beams of the
right Flipper Opto Switch Board, so one button works both right flippers. The left board also wires its
second opto to F8 (public 118), but there is no upper left flipper; a T.1 run showed the switch grid
marking 118 (and 117) closed while the ROM named nothing and drove nothing.

The Fliptronic buttons are optos per the Flipper Opto Switch Board page and the Fliptronic II connector
list, although the Switch Locations list's rows 11 and 12 print leaf-switch parts (SW-1A-192/191) for the
right and left flipper buttons. Either way the public button state is already normalized (WPC_FLIPPERS
reads the column complemented), so a recreation drives 112/114/116 at 1 while pressed.

## The ball cannon (headline mechanism)

The A-14635 Cannon Assembly sits in the lower centre of the playfield between the slingshots, with a
catapult (A-14640) under it.

- **Loading.** When Davy Jones' Locker is open, a ramp shot drops into the locker and a subway under the
  playfield (switch 61 at its top, 66 at its bottom) carries the ball into the catapult, where it closes
  the cannon kicker switch 35. The rules load the cannon from the side (upper right) flipper and from the
  shooter at the start of a ball.
- **Aiming.** With a ball loaded the 20 V cannon motor (solenoid 3, 14-7965) sweeps the cannon from side
  to side and the Fire button on the lockdown bar (switch 34) flashes (Fire Button flasher, solenoid 27).
  The manual prints no cannon position sensor and the matrix has no free cannon switch: the motor sweeps
  the cannon and the player times the shot (the rules say to press Fire when the cannon is aimed at the
  desired target); how the ROM tracks the aim, if at all, is not documented. Pinned `br.c`'s simulator writes a sweep-direction bit to the unused matrix
  position 77 and marks it "FAKE!, Not used in the Pin"; do not treat 77 as a real input.
- **Firing.** Pressing Fire makes the ROM pulse the catapult coil (solenoid 8, A-15016), which shoots the
  ball out of the cannon at whatever it points at. The cannon should reach from the far left shot (the
  lockup) to the far right shot (the jets); the targets are the flashing jewels and treasure chests, which
  award features and SINK SHIP letters. Completing SINK SHIP lights the Broadside shot to sink the ship.
- **Feedback.** In T.14 CANNON TEST the ROM shows `SW.35 CANNON = CLOSED` at public 1 and `OPEN` at 0 and
  fires 8 on the closure; `MOTOR = ON` drives 3. The two Cannon Flashers (solenoid 26) light the cannon.
- **Recreation.** The retained script models the sweep as a disc rotating between -45 and +45 degrees
  while 3 is on and launches a new ball from its CannonKicker along the disc angle when 8 fires with 35
  set. The sweep range, rate and launch speed are the table author's choices, not measurements; the
  physical cannon has a level adjustment (manual maintenance pages).

## The up/down ramp (Davy Jones' Locker)

The A-14918 Ramp Lifting Mechanism moves the up/down ramp (A-14831 Lift Ramp Assembly). The Ramp Up coil
(solenoid 10, AE-26-1200) raises it and the Ramp Down solenoid (11, SM1-29-1000-DC) lowers it again.
Switch 54 is the only feedback and is closed when the ramp is down: the manual's error messages say to
check that "switch 54, ramp down, is definitely closed when the ramp is down, and positively open when
the ramp is up", and the ROM reports a ramp that fails three tries in a row. Raised, the ramp opens the
locker so the next ramp shot loads the cannon; lowered, the shot rides the ramp. The rules open the locker
on the skill shot (the flashing lower 3-bank from the plunger), on completing the lower, middle and upper
3-banks, on consecutive ramp shots from the side flipper, and on the 3-bank rebound. A recreation should
drive 54 from the ramp's real travel, closed only once the ramp is fully down.

## Other mechanisms

- **Pirates' Cove lockup.** A ball enters past 71 and stops at Lockup 1 (63) or, with one held, at
  Lockup 2 (64); the Left Ball Lockup coil (9) kicks them out. Locking while LOCK 1 flashes starts 2-ball
  multiball and locking both during 2-ball multiball starts 3-ball multiball.
- **Broadside popper.** A ball in the Broadside hole at the top centre rests on 55 and the D-11335-1
  popper (solenoid 1) kicks it up onto the center habitrail, which returns it towards the flippers. Two
  Top Popper flashers (25) sit on the back panel behind it.
- **Trough.** The outhole (15) kicker (2) feeds a three-ball trough (18 left, 17 center, 16 right at the
  release end); the ball release (4) feeds the manual shooter lane (25). The game is three-ball.
- **Slingshots, jets.** Slings 28/6 (left) and 38/5 (right); jets 46/13 (left), 47/14 (right) and 48/15
  (bottom), entered past 58 and left past 57.
- **Stand-up targets.** Three 3-banks (bottom 31-33, middle 41-43, top 51-53) and the right single
  stand-up 65 (the Doubloon target).

## Lamps, flashers and general illumination

The T.8 SINGLE LAMPS run lights each lamp 11-88 alone in matrix order and names it, in the Lamp Matrix's
wording (17 COMBO SHOT RIGHT, 67 COMBO SHOT LEFT, 81 SKILL (OPEN), 82 SKILL (LOCKER) where the Lamp
Locations list prints Sequence Shot 2, Sequence Shot 1, Skill Shot 1 and Skill Shot 2). Lamps 11 and 86
have two bulbs each. 78 and 87 (Insert Left/Right) are backbox insert lamps and 88 is the Credit button.

Flashers 17-24, 27 and 28 each also feed a backbox insert bulb. 27, the Fire Button flasher, lights the
button on the lockdown bar. 25 (Top Popper) and 26 (Cannon) have two playfield bulbs each.

GI: the T.6 run names GI 0 JETS & BACK RAMP, 1 TOP PLAYFIELD, 2 BOT. PLAYFIELD, 3 LEFT/TOP INSERT and
4 RIGHT INSERT. The Power Driver Board connector list prints the first three strings' J120 lines as going
"to insert board", but the table, the bulb types and the ROM make them playfield strings, so that is how
they are recorded; 3 and 4 are backbox strings, and 4's colour also feeds the coin door.

## Spatial status and why the record stays partial

Placements come from the retained VPW v1.4 table's script-bound objects, and the factory location
drawings validate most of them. The three trough switches, the Ramp Down switch and the two ramp-lift
coils have no table object and are measured on the drawings. The playfield GI bulb positions are the
table author's grouping, and the Top Popper flashers have no defensible coordinate, so
`spatial_placement` stays missing. `variant_differences` stays missing too: the two prototype
drivers' physical compatibility is unknown until a source describes the pre-production machines.

## Author construction checklist

- Drive matrix switches at public 1 when closed; never invert them.
- Drive 112, 114 and 116 for the buttons; the right button also drives 116 for the upper right flipper.
- Model the cannon: subway 61 -> 66 -> catapult (35), motor 3 sweeps, catapult 8 fires on Fire (34).
- Model the up/down ramp with 54 closed only when fully down.
- Model the two-ball lock 71/63/64 with coil 9 and the Broadside popper 55 with coil 1.
- Treat 77 as unused, and 117/118 as having no flipper behind them.

## Sources

The manual's excerpts, the IPDB page, the retained table and script, and the runtime evidence under
`evidence/runtime/wpc-fliptronic/black-rose-br_l4-*.json` are the sources; the definition's `sources`
list carries their hashes and locators.
