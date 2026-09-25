# Firepower (Williams, 1980) - recreation knowledge

Williams game number 497, February 1980, Williams System 6, four players, three-ball MULTI-BALL,
designed by Steve Ritchie with software and sound by Eugene Jarvis (IPDB 856). It is the first game
with LANE CHANGE and the first with electronic multiball. The physical release year is taken from
the machine's own instruction booklet (16P-497-103, January 1980), the March 1980 schematics and
IPDB; pinned PinMAME dates every Williams driver 1980.

## Reading the driver declaration

`src/wpc/s6games.c` declares every System 6 Firepower driver with
`INITGAMEFULL(frpwr_l6, s6_6digit_disp, 0, 45, 26, 25, 27, 28, 42, 12)`, which expands to
`core_tGameData {GEN_S6, s6_6digit_disp, {FLIP_SWNO(0,45)}, NULL, {{0}}, {0, {26, 25, 27, 28, 42, 12}}}`:

- `FLIP_SWNO(0,45)`: no left flipper matrix switch, and PinMAME's synthetic right-flipper button
  (public switch 82) is copied into matrix switch 45 every frame. On the machine, switch 45 is the
  LANE CHANGE switch the ROM reads to rotate the lit F-I-R-E lamps.
- `{{0}}`: the per-game inverted-switch mask is zero. Every public switch reads 1 closed and 0 open,
  which the ROM's own switch test confirms for all 58 wired positions.
- `{26, 25, 27, 28, 42, 12}`: the switches that fire special solenoids 17-22 (see below).

System 6 has no PinMAME profile of its own before this curation; `controllers/pinmame/system-6.json`
was written for it from `s6.c` and applies to every `GEN_S6` game.

## The controller contract a recreation drives

- Switches 1-64 are the sequential matrix, column-major: public = (column - 1) * 8 + row, which is
  exactly the number Figure 5 prints in each cell. Column 1 is the cabinet: tilts, credit button,
  three coin switches, slam tilt, high score reset. The service buttons are the direct inputs -7
  (Advance), -6 (Auto-Up/Manual-Down, 1 = Auto-Up), -5 (CPU diagnostic), -4 (sound diagnostic) and
  -3 (Master Command Enter).
- Flippers are not CPU-driven. Drive PinMAME's synthetic buttons 82 (right) and 84 (left). While
  the game is on (public solenoid 23), PinMAME fabricates flipper states 45/46 from 82 and 47/48
  from 84, and copies 82 into switch 45 (the retained flipper-button harness run shows it: 82 alone,
  with 45 never written, moves the lit lane-change lamp). The physical coils (8L25 right, 8L24 left,
  SFL-19-400/30-750-DC) are switched by the cabinet buttons through relay Z1 on the driver board,
  which the game-on line pulls in; each coil's end-of-stroke contact drops its power winding
  mechanically, so a recreation has no winding decision to make.
- Solenoids 1-8 and 14-22 are coils, 15 is two flash lamps, 9-13 are sound-command lines to the
  sound board, 2 and 3 are fitted drivers with no load (see below), 23 is the game-on enable.
  Addresses 24-44 are never published on System 6.
- Lamps 1-64: public = (column - 1) * 8 + row. Lamp 23 is not fitted. Columns 1-6 and column 7
  rows 1 and 8 (lamps 49 Right Special and 56 Credits (Playfield)) are playfield lamps; column 7
  rows 2-7 and all of column 8 are backbox inserts on the insert board.
- Displays: four six-digit player displays and a master display whose left pair (strobes 15-16) is
  the credit display and right pair (strobes 7-8) the ball-in-play and match display. PinMAME's
  display index 4 (memory positions 14-15) is credits and index 5 (positions 6-7) is ball in play;
  the ROM's solenoid test proves it by showing the test number on 4 and the solenoid number on 5.
  The Oliver seven-digit System 6 ROMs `frpwr_b6` and `frpwr_c6` publish the same six displays at
  other memory positions (see the driver `display_overrides`); their own harness runs show the
  credit on the entry at position 34 and the ball in play on the entry at position 14.
  PinMAME also publishes a 128x32 rendering frame of the segment layout, which is not a display on
  the machine.
- General illumination is an unswitched 6.3 VAC supply through fuse 6F1 (20 A) to the cabinet
  (coin-door lamps), the playfield and the insert board. There is no GI controller output.

## Special solenoids

System 6 has six special solenoid drivers, 17-22, for the four jet bumpers and two kickers
(slingshots). On the machine each is fired directly by its own special switch, 8SW65-8SW70, through
the driver board, as long as the game-on enable is set; the CPU sees only the separate scoring
contact in the matrix (switches 26, 25, 27, 28, 42 and 12). PinMAME has no public address for the
special switches and instead publishes the special solenoid whenever the matrix switch named in
`sxx.ssSw` closes. The retained gameplay harness run shows each pair: 26 -> 17 top left bumper,
25 -> 18 bottom left, 27 -> 19 top right, 28 -> 20 bottom right, 42 -> 21 right kicker,
12 -> 22 left kicker. Unlike System 11 and Data East, System 6 applies no permutation between the
special-solenoid slot and the public address.

The booklet prints solenoid 20 as `Bottom Left Jet Bumper` twice (Table 3 and Figure 3's chart),
repeating row 18. Everything else says Bottom Right: the schematic's coil 8L20 BOTTOM RIGHT JET
BUMPER and special switch 8SW68, Figure 3's callout 20 inside the lower right bumper, PinMAME's
switch map and the harness. A previous owner has pencilled `Rt` beside the row on the IPDB scan.

## Mechanisms a table author has to build

- **Outhole and ball ramp.** No trough: the three balls rest on a ball ramp below the apron, with
  rest switches 51 (left), 58 (centre) and 57 (right, the exit end). A drained ball falls into the
  outhole (9) below the apron centre; Ball Release (solenoid 1) kicks it onto the ramp. Ball Ramp
  Thrower (solenoid 8) throws the ball at position 57 into the shooter lane, onto the Ball Shooter
  switch (46). At game start with a full ramp the ROM throws the first ball; a new game cannot
  start until all balls are back on the ramp.
- **Three eject holes**: left (13, solenoid 4), right (30, solenoid 5) and upper right in the top
  corner (36, solenoid 6). A flashing hole locks the ball and a new ball is released from the ramp,
  a flashing hole or an unlit hole, in that order; locking all three balls starts MULTI-BALL.
  Otherwise the ROM kicks the ball straight back out; the harness shows repeated kicks while a hole
  switch stays closed. Star rollovers 53 and 54 sit in the lanes feeding the left and right holes.
- **Left ball saver kicker**: a kickback at the foot of the left outlane, solenoid 7. When lamp 2
  (Ball Saver Kicker On) is lit and the ball rolls over the left outside rollover (10), the ROM
  fires solenoid 7 and turns lamp 2 off. Which feat lights it is an operator adjustment: the POWER
  targets, targets 1-3 or 4-6 on one ball, or spotting 1-6. At factory settings the retained kicker
  harness run lights it from targets 1-3 and not from the POWER targets.
- **Four jet bumpers and two kickers** on special solenoids, as above.
- **Two three-target banks above the flippers**, "1" "2" "3" (17, 18, 19) left and "4" "5" "6"
  (21, 22, 23) right, with target arrows 26-31. They are standups on production machines. The first
  ten machines had two 3-banks of drop targets here (IPDB, Steve Ritchie), and the production
  hardware still carries their traces: the schematic calls the switches "Drop Target" and the
  arrows "Drop Target Arrow", Table 3 prints solenoids 2 and 3 Not Used with drivers Q17 and Q19
  fitted and their harness wires ending N/C, and switches 20, 24, 52 and 55 are printed NOT USED.
  The ROM still drives 2 and 3 as bank resets - at every ball start, and 2 when targets 1-3 are made
  (harness). A recreation of the production machine leaves them unconnected.
- **Three POWER standups** on the right (39, 40, 41, top to bottom) with blue lamps 9-11, and the
  **top centre target** (29) between the I and R lanes.
- **Four top rollover lanes F-I-R-E** (32-35) with lamps 5-8. LANE CHANGE: each closure of the right
  flipper's switch 45 rotates the lit F-I-R-E lamps one lane (harness: 45 moves lamp 5 off, lamp 6
  on). Spotting F-I-R-E advances the bonus multiplier and lights the FIRE insert.
- **Eight 50-point standups** on rubber-post runs: 16 top left; 14, 49 and 50 down the left rail,
  with 49 level with the left eject hole; 31 and 37 below the upper right eject hole; 38 middle
  right; 48 lower right.
- **Spinner** on the left orbit (15) with lamp 32.
- **FIRE and POWER inserts** above the kickers, each with two lamp bulbs (lamps 3 and 4) and one of
  the two Type 89 flash lamps on solenoid 15, which the ROM flashes every few seconds in attract
  mode.

## Tilts

Plumb bob (1), ball roll (2) and playfield (47, below the lower left playfield) tilt the ball in
play: first closure for the ball-roll and playfield tilts, third (adjustable) for the plumb bob.
Slam tilt (7) returns the game to game over.

## DIP switches and Master Command

PinMAME's DIP addresses are `bank * 8 + bit + 1` (see the controller profile). 1 and 2 are the
sound board's two-position switch DS1. 17-19 are the Master Command switches the booklet documents
(switch 8 zero audit totals, 7 restore factory settings, 6 auto-cycle), read by the ROM only while
Master Command Enter (-3) is held; PinMAME labels them D1-D3. The rest of the Master Command bank
and the second CPU-board bank (9-16, printed NOT USED in Figure 2) carry no function.

## Driver variants

- Williams: `frpwr_l6` (production L-6), `frpwr_l2` (L-2: earlier PROM 1, differing only in price
  presets and maximum credits per IPDB), the free-play-fix flipper ROM versions `frpwr_l6ff` and
  `frpwr_l2ff`, and Ted Estes's T-6 `frpwr_t6`/`frpwr_t6ff`. All identical hardware.
- Oliver System 6 custom ROMs `frpwr_a6` and `frpwr_d6` (6-digit, 2008): the same board with a 4 KB
  EPROM set.
- Oliver seven-digit conversions `frpwr_b6` and `frpwr_c6` on the same System 6 board: PinMAME's
  fp_7digit_disp moves the six displays to memory positions 0, 7, 20, 27 (seven digits wide), 34
  (credits) and 14 (ball in play), which each driver's own harness run confirms.
- The Oliver System 7 conversions `frpwr_a7`, `frpwr_b7`, `frpwr_c7`, `frpwr_d7` and `frpwr_e7`
  replace the CPU board with a Williams System 7 board, a different controller generation. They are
  not part of this record: like the Kiss and Eight Ball Deluxe prototypes, a different CPU board
  makes a separate physical record, `williams-oliver.firepower.1980`, which stays partial until a
  System 7 controller profile exists.

## Running the ROM in LibPinMAME

A first power-up from empty CMOS stops on the game-identification screen (`0497` then `1497 6` in
the player 1 display, 04 and 00 on the master display) and shows no lamps. Power up once more with
the saved NVRAM and the game comes up in attract mode with the 550,000 high score. The retained
harness runs therefore initialize each state directory with exactly one empty-NVRAM boot before the
evidentiary run.

## Retained table caveats

The retained known-working table (3rdaxis, Slydog43 & G5K, V1.0, 2018) is faithful in layout and
in almost every binding. It loads `frpwr_b7`, the Oliver System 7 conversion ROM, but every binding
this record takes from it (switches, lamps, solenoids 1-22) lies in the address space the two boards
share, and the production-ROM harness runs and the booklet confirm each one. Its defects:

1. Every 50-point standup handler pulses switch 48, so switches 14, 16, 31, 37, 38, 49 and 50 are
   never driven. The script has eight handlers but the table has only seven walls: standup 49 has
   none (the Vs A.I. revision adds it as StandupTarget8). Bind each standup to its own address.
2. Solenoid 7 only plays a sound; the table kicks the ball from its own copy of lamp 2. Drive the
   kickback from solenoid 7.
3. Lamp 56, the credit window lamp on the apron, is not modelled; the Vs A.I. revision adds it.
4. The ComboTrigger objects between the 1-6 targets pulse two target switches at once, a table aid.
5. It sets `UseSolenoids=25`, the game-on address of the System 7 ROM it loads. With any System 6
   driver of this record the game-on enable is solenoid 23, so a recreation must gate its flippers
   on 23. Loaded unchanged with a System 6 ROM, the table loses only its fast-flip key path, since
   solenoid 25 never asserts; core.vbs still forwards the ROM's flipper outputs 46 and 48, so the
   flippers move with ROM latency.

## Evidence

- Instruction Booklet 16P-497-103 (IPDB), cross-checked against a second printing (Internet
  Archive), for the switch, lamp and solenoid tables and location drawings.
- March 1980 schematics (IPDB) for wiring, the insert board, the master display, power and the
  sound board.
- Service Bulletin SS 20 for the flash lamp ground; Ted Estes's drop-target note and IPDB for the
  prototype history.
- Pinned PinMAME `8371478a` for the System 6 contract and the Oliver System 6 conversion drivers.
- The retained known-working table and its Vs A.I. revision for geometry and runtime bindings.
- LibPinMAME harness runs: solenoid test, switch test, gameplay causality, ball saver kicker, the
  flipper-button path, and the seven-digit `frpwr_b6` and `frpwr_c6` displays.
