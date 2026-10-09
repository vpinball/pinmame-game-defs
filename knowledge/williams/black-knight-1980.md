# Black Knight (Williams, 1980) - recreation knowledge

Williams game number 500, November 1980, Williams System 7, four players, two- or three-ball
Multi-Ball, designed by Steve Ritchie with art by Tony Ramunni and software by Larry DeMar (IPDB
310). It is the first game with Magna-Save, the first solid-state game with a multi-level playfield
(an upper playfield over the rear of the lower one, with four flippers), and it introduced the
Bonus Ball. The physical release year comes from the instruction booklet (16P-500-103, December
1980) and IPDB; pinned PinMAME dates every driver 1980.

## Reading the driver declaration

Black Knight's game data lives in PinMAME's simulator file `src/wpc/sims/s7/full/bk.c`, not in
`s7games.c`: `bkGameData = {GEN_S7, s7_dispS7, {0, ...}, &bkSimData, {{0}}, {0, {21, 22, 36, 0, 0, 0}}}`.

- `hw.flippers` is 0: no `FLIP_SWNO` matrix switch and no `FLIP_SOL`. The ROM cannot read the
  flipper buttons; PinMAME only fabricates flipper outputs from its synthetic buttons.
- `{{0}}`: the inverted-switch mask is zero. Every public switch reads 1 closed and 0 open, which the
  ROM's own switch test confirms for every position it reports.
- `{21, 22, 36}`: the switches that fire special solenoids 17, 18 and 19.
- The file's `#define` names and simulator state table (for example `sOuthole 1`, `sBallRel 6`,
  `sKnocker 11`, `swRTrough 17`) are a keyboard simulator's working names and several are wrong for
  the machine: solenoid 1 is the outhole kicker called Ball Release, 6 is the Ball Ramp Thrower and
  11 is the GI relay, not a knocker. This record takes its names from the manual and the ROM.
- `bkSimData` enables PinMAME's built-in simulator only while PinMAME's own keyboard handling is on;
  under LibPinMAME, as in every retained harness run, it does nothing.

No System 7 controller profile existed before this curation; `controllers/pinmame/system-7.json` was
written for it from `s7.c`, `s7.h` and `s7games.c` and applies to every `GEN_S7` game.

## The controller contract a recreation drives

- Switches 1-64 are the sequential matrix, column-major: public = (column - 1) * 8 + row, exactly
  the number the switch matrix prints in each cell. Column 1 is the cabinet: plumb bob and ball roll
  tilts, credit button, three coin switches, slam tilt and high score reset. Column 2 rows 1 and 2
  are the right and left Magna-Save buttons on the cabinet sides (9, 10). The service buttons are
  the direct inputs -7 (Advance), -6 (Auto-Up/Manual-Down, 1 = Auto-Up), -5 (CPU diagnostic), -4
  (sound diagnostic) and -3 (Master Command Enter).
- Flippers are not CPU-driven. Drive PinMAME's synthetic buttons 82 (right) and 84 (left). While the
  game is on (public solenoid 25) PinMAME fabricates flipper states 45/46 from 82 and 47/48 from 84.
  Each cabinet button has two contacts and works both flippers on its side, lower and upper (coils
  8L25 and 8L27 right, 8L24 and 8L26 left, SFL-19-400/30-750-DC), through relay Z1 on the driver
  board, which the game-on line pulls in.
- Solenoids: 1-8 coils (ball release, the four drop-bank resets, ball ramp thrower, Multi-Ball
  release, lower eject hole), 9 and 10 the Magna-Save magnet relays, 11 the GI relay, 15 the bell,
  16 the coin lockout, 17-19 the special solenoids (left and right kicker, jet bumper), 25 the
  game-on enable. 12-14 and 20-24 have no load; the ROM's solenoid test still pulses 1 to 24.
- Lamps: public = (column - 1) * 8 + row. Column 1 rows 1-6 and 8 are the backbox lamps on the
  master display (Shoot Again, Ball In Play, Tilt, Game Over, Match, High Score, Bonus Ball Time);
  everything else from 9 to 64 is on the playfield except 43-46 (not used). Lamp 7 is printed
  Credits (Playfield) but no bulb is fitted: the playfield harness leaves lamp column 1 N.C. and the
  master display has no row 7. The ROM lights it whenever credits are posted.
- Displays: PinMAME's s7_dispS7 publishes eight entries. Index 2 is player 1 (memory start 1),
  index 3 player 2 (9), index 0 player 3 (21) and index 1 player 4 (29), all seven digits; indexes 4
  and 5 are the tens and units of the ball-in-play / match display (starts 0 and 8) and indexes 6
  and 7 those of the credit display (starts 20 and 28), the four digits of the master display. The
  four-player harness run shows each player's score on those indexes. PinMAME also publishes a
  128x32 rendering frame, which is not a display on the machine.
- General illumination is a 6.3 VAC supply routed through the K1 Special Relay on the power supply
  board (early games: a stand-alone GI relay on the backbox floor). Solenoid 11 energizes K1 and
  turns the GI off. The ROM keeps it off (GI on) in attract mode and play, energizes it when the
  ball is tilted, and flickers it on tilt warnings and during the Multi-Ball light show.
- DIP switches: 1 and 2 are DS1 on the sound board. The CPU board's two banks (9-24) are never read
  by the Black Knight ROM: its only read of the DIP port is a discarded flag-clearing read. All
  settings are software adjustments (Functions 13-41, reached with Advance and the credit button);
  Functions 42-49 are the factory audit totals.

## Special solenoids

The left kicker (17), right kicker (18) and jet bumper (19) are each fired directly by their own
special switch (8SW65, 8SW66, 8SW67) through the driver board while the game-on enable is set; the
CPU only sees the separate scoring contacts 21, 22 and 36. PinMAME publishes the special solenoid
whenever that matrix switch closes, which the switch-test and gameplay harness runs show. The ROM
can also fire special solenoid slots itself: its solenoid test pulses 17 to 24 as steps 17 to 24.
Slots 6 and 7 (public 23 and 24) have no driver on the Black Knight driver board.

## Mechanisms a table author has to build

- **Outhole and ball ramp.** No trough: the three balls rest on a ball ramp below the apron, with
  rest switches 19 (left), 18 (centre) and 17 (right, the exit end by the shooter lane). A drained
  ball falls into the outhole (20); Ball Release (1) kicks it onto the ramp. Ball Ramp Thrower (6)
  throws the ball at 17 into the shooter lane onto the Ballshooter Trough switch (45). A game starts
  only with all three balls on the ramp, the lockup or the shooter switch (at most one in the
  shooter lane).
- **Four drop-target 3-banks**: lower left (25-27, reset 2), lower right (29-31, reset 3), top left
  (33-35, reset 4) and top right (37-39, reset 5), the top two on the upper playfield. A drop target
  stays down, so the ROM sees its switch closed until the reset; it resets a bank the moment all
  three are down, at every ball start and at the start of Multi-Ball, and when the bank's timed lamp
  (17-20) runs out first (booklet). Completing a bank lights one of its three arrows and a
  Magna-Save, right (lamp 9) first, then left (lamp 10).
- **Magna-Save.** A magnet under each side of the lower playfield, below the lower drop banks,
  switched by relay 9 (right) or 10 (left). With its lamp lit, the Magna-Save button on that side of
  the cabinet (switch 9 right, 10 left) makes the ROM energize the magnet for a few seconds to catch
  a ball heading for the outlane; the inside rollovers then score 10,000. The playfield solenoid
  sheet prints the relay coils' legends with the sides swapped (8L9 LEFT MAGNET RELAY on solenoid 9),
  but its own contact labels, Table 4, the retained script and the ROM put 9 on the right magnet.
- **Lockup trough and Multi-Ball** on the upper playfield: three switches 41 (bottom), 42, 43 (top).
  Each locked ball is held and a new one thrown with 6. Three locked balls, or the lit lower
  playfield eject hole (24, solenoid 8), start Multi-Ball: the ROM pulses the Multi-Ball Release (7)
  with the balls still in the lock. The booklet marks as adjustable its rule that the lock arrows (21, 40,
  42) do not flash until the turnaround (23) is made; at the factory settings the gameplay harness
  run flashes them from game start, before 23 is made. Scoring is doubled with two balls in play and tripled with three.
- **Lower playfield eject hole** (24), kicked by 8.
- **One jet bumper** on the upper playfield and **two kickers** (slingshots), on special solenoids.
- **Spinner** in the left orbit (13), lit by the right inside rollover; **right ramp rollunder**
  (14, upper playfield) with the Mystery value lit by the left inside rollover; **left ramp
  rollover** (44, upper playfield) and the **turnaround** (23) for the extra balls; outlanes 11 and
  12, inlanes 15 and 16.
- **Rebound standups**: early playfields carried a vertical switch behind three of the drop banks
  (28, 32, 40). The manual prints them NOT USED and draws none; IPDB and Steve Ritchie record that
  they were removed in production. The ROM still scans them. They are optional devices here.
- **Bonus Ball**: with two or more players the highest scorer gets a timed bonus ball (lamp 8 in the
  backbox), with both magnets lit.

## Tilts

Ball roll tilt (2) tilts on its first closure; plumb bob (1) and playfield tilt (46) on the third
(adjustable). Each warning closure flickers the GI through relay 11. Slam tilt (7) returns the game
to game over.

## Driver variants

`bk_l4` (production L-4), `bk_l3` (L-3, different IC14 and IC26), `bk_l2` (the Rev 2 game ROMs IPDB
hosts) and `bk_f4` (L-4 with French speech). All run the same hardware with the same init data and
display layout; the L-3 and French-speech solenoid tests behave exactly like L-4. The `bk_l2` ROM is
not in the authorized ROM library, so it has no harness run.

## Running the ROM in LibPinMAME

A first power-up from empty CMOS stops on the game-identification screen. Power up once more with
the saved NVRAM and the game comes up in attract mode; every retained run initializes its state
directory with one empty-NVRAM boot first. The diagnostics are entered with Manual-Down (-6 = 0) and
Advance (-7); Auto-Up then steps Test 00 (sound), 01 (lamps), 02 (solenoids) and 03 (switches), each
shown in the credit display, and Manual-Down holds one solenoid step. Drive everything with direct
switch writes so the driver's simulator stays off. In gameplay, hold drop-target switches closed
until the reset fires, as real drop targets stay down; a momentary pulse never completes a bank.

## Retained table caveats

The retained known-working table (Bord, 3.0, November 2021) is faithful in layout and bindings. Its
defects:

1. `SolCallback(23) = "vpmNudge.SolGameOn"`: on System 7 the game-on state is 25 (the table's own
   S7.VBS says so), so the nudge handler never sees game-on. Gate on 25.
2. The apron light `l7` has TimerInterval 36 and lights with the jet bumper; lamp 7 has no bulb on
   the machine.
3. The ball ramp and the lock are modelled as ball stacks without per-switch objects, and the
   outhole as the trough's entry kicker; place those switches from Figure 3.

## Evidence

- The English manual with paginated schematics (IPDB) for every table, chart, location drawing and
  wiring sheet; the 400 dpi copy of the instruction booklet for the drawing registration; the
  colour schematic scan as a cross-check; the A-8762 retrofit kit sheet.
- IPDB 310 for identity, production history, the GI relay and the rebound switches, and its
  photographs for the magnet positions.
- Pinned PinMAME `97aa922b` for the System 7 contract and the Black Knight game data.
- The retained table and its byte-identical pinned corpus script for geometry and runtime bindings,
  and the S7.VBS library it loads.
- LibPinMAME harness runs: solenoid test (L-4, L-3, French L-4), switch test, gameplay causality,
  Multi-Ball, and the four-player display roles; and a static reading of the ROM's DIP-port access.
