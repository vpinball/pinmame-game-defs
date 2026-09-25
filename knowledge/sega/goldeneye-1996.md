# GoldenEye (Sega 1996)

Coverage: **partial**. Every address is enumerated and named. Polarity, mechanism and variant facts
are validated from the factory operations manual, pinned PinMAME, the retained known-working table
with two corroborating scripts, and hash-pinned harness runs; construction is too, except bulb types,
which the manual contradicts itself about. The record is partial for three reasons:

- **Spatial placement.** The retained manual scan kept the outlines of its playfield location
  drawings but not a single callout number. Every coordinate therefore comes from one community table
  and stays observed, and a few flasher sockets and lamps 40 and 58 have no socket object.
- **Solenoids 35 and 36.** In LibPinMAME's default output mode, public solenoids 35 and 36 carry
  magnet-board latch bits whose meaning no source states.
- **Bulb types (`conflict.bulb-types`).** The manual's lamp grid and its bulb pages disagree about
  which bulbs the playfield lamps and three flash lamps take (see below).

## Identity and drivers

- Sega Pinball, 1996 (IPDB 3792, OPDB `G43wE-MQV5K`). The hardware is a Whitestar CPU/Sound board
  (520-5136-42), an I/O Power Driver board (520-5137-00), a 128x32 dot-matrix display and a 2-Flipper
  Solid State Flipper Board (520-5080-00). GoldenEye is a five-ball game.
- The PinMAME driver `gldneye` is the only one for this machine. It is declared in `src/wpc/segames.c`
  with `INITGAME(gldneye,GEN_WS,se_dmd128x32,SE_BOARDID_520_5143_00)` and machine driver `de_mSES1`.
  The board ID enables PinMAME's model of the 520-5143-00 double-magnet processor.

## Evidence used

- **Operations manual:** Sega GoldenEye, 132 pages, a 2003 image-only scan supplied by the contributor.
  The switch grid and descriptions, lamp grid, coil and flash-lamp charts, flipper coil table, DIP
  country chart, fuse chart, playfield bulb and socket pages and the assembly parts lists are transcribed with native-resolution crops
  under `evidence/excerpts/sega.goldeneye.1996/`. The playfield location drawings lost their callout
  numbers in this scan, and most assembly drawings are blank; their parts tables survive.
- **Known-working table:** `Goldeneye (Sega 1996) VPW 1.2.1.vpx`, which supplies the runtime bindings
  and all geometry. The pinned `vpxtable_scripts` corpus adds the released VPW 1.2 script (same
  bindings) and an independent Dozer script, which corroborates the magnet-board switches and the tank
  trap door.
- **VPinMAME script library:** the `sega2.vbs` and `core.vbs` the table loads. `sega2.vbs` notes that
  GoldenEye and Apollo 13 put their flipper buttons on the switch matrix.
- **Pinned PinMAME:** `8371478a`, which supplies the Whitestar address routing, the magnet-board model
  and the output typing.
- **LibPinMAME harness runs of `gldneye`:** seven runs (`evidence/runtime/whitestar/`), covering
  satellite home, ball serve and launch, plus three ball-serve controls: one that changes no switch,
  one that raises only the VUK opto, and one that only empties the last trough position.

## Controller facts a recreation needs

- The switch matrix is sequential. Switch = (column - 1) x 8 + row, as printed. Matrix position 1 is
  the plumb bob tilt, 3 the start button, 4-6 the right, center/DBA and left coin slots, 7 the slam
  tilt and 9 the Fire Button in the cabinet gun.
- The coin-door buttons are the dedicated inputs:
  - -2 is Red (DS-6, Volume, or Left in test).
  - -1 is Green (DS-7, Service Credits, or Right in test).
  - 0 is Black (DS-8, Begin Test, or Enter in test).
  - -3 is the memory protect switch, which opens when the coin door opens.
- **Flipper buttons are matrix switches 63 (left) and 64 (right).** The cabinet buttons are wired to
  the SSFB, which fires the flipper coils itself and passes each button to the CPU. The flippers'
  end-of-stroke switches are wired to the SSFB too. The dedicated inputs DS-1 to DS-5, which PinMAME
  exposes at 84, 83, 82, 81 and 88, are printed NOT USED.
- **81 and 83 are written by PinMAME.** Because `gldneye` declares `FLIP_SOL(FLIP_L)`, which implies
  `FLIP_EOS`, `core_updateSw` rewrites 81 from 46 and 83 from 48 every frame. They read 1 while the
  ROM holds the flipper enables, which is throughout play. A host write lasts one frame at most, so a
  recreation must not drive them. 82, 84 and 88 are left to the host, and nothing uses them.
- **Polarity.**
  - GoldenEye has one opto, the trough VUK opto 15. The manual's theory of operation says it is an
    open switch while lit and closes when a ball blocks the beam, and Whitestar reads a closed
    contact as public 1. The harness is consistent with it. Raising only 15 as the lock-ball coil
    fires draws the up-kicker about 0.25 s later. Emptying only trough position 14 also draws it,
    but about 0.81 s later, and changing neither leaves the up-kicker to the ROM's retry cycle, about
    3.45 s after the first lock-ball pulse. In both single-switch runs the ROM then kicks four more
    times whatever 15 does, and then resumes its lock-ball retries only if 14 never opened.
  - The satellite home switch 20 is 1 at home, proven by the home-search runs.
  - The magnet boards report 23 (ball on the satellite magnet) and 24 (ball on the flipper magnet)
    as 1 in both independent scripts.
  - PinMAME applies no inversion; the `invSw` mask is zero. Consume every switch as delivered.
- **Solenoids** 1-14, 17, 18 and 20-24 are the printed drivers. 8 is the optional external replay
  knocker drive line (no coil in the game), and 24 is the optional coin meter, which the harness sees
  pulse with every coin. 3, 5, 6, 7, 19 and 23 are not used.
- **Flippers.** Physical Q15 (Left Flipper Enable) is published at 47 and Q16 (Right Flipper Enable)
  at 45; 48 and 46 are set alongside them. These are enables, not flips: a flipper fires while its
  button is held and its enable is on. In the harness run the ROM raised all four together and held
  them, about 14.8 s after the shooter-lane switch closed; the run does not show what it waited for.
  Public 15 and 16 are constant zero. `se_solenoid_w` masks both bits off in every write, and only
  15 could be reused, by a fast-flip address that se.c does not configure for `gldneye`.
- **Flash lamps** are 25-32 (FLAMP 1-8), each also lighting one or two backbox insert bulbs.
  The flash lamp chart prints #906 bulbs for the playfield sockets of 25-27 (see the bulb conflict).
- **Magnets.**
  - 33 is the satellite magnet and 34 the flipper magnet, published from the magnet board's aux
    latch.
  - 35 is latch bit 2 in LibPinMAME's default binary mode, with unknown meaning. In physical-output
    mode it carries the magnet processor's reset strobe instead.
  - 36 is latch bit 3 in binary mode, with unknown meaning. Nothing writes it in physical-output
    mode.
  - 37-44, 49 and 50 are unused platform slots.
- **Lamps** 1-80 run in ten rows of eight (lamp = (row - 1) x 8 + column), since `gldneye` declares
  two extra lamp columns. 9, 64, 70 and 71 are not used (the ROM still toggles 9, 64 and 70 in
  attract), 57 is the start button, and 72-80 are the nine GOLDENEYE letters on the backbox speaker
  panel. Lamp 40 is not placed: its only table object is a ramp-effect light with no bulb or insert
  object beside it.
- **Legacy aliases.** The superseded legacy record's numeric and zero-padded addresses (for example
  switch `7`, `07`, `007`) are kept as `vpe-legacy.*` aliases, including the G.I. relay's old lamp
  `0`, while legacy consumers still resolve them.
- **G.I.** is one aggregate channel (the G.I. relay). Behind it are four fused 6.3v AC strings: insert
  left, lower half playfield, insert right and coin door, and upper half playfield.
- **DIP bank SW300:** positions 1-4 select the country (all off is USA), and no setting uses 5-8.

## Mechanisms

### Trough, lock ball and up-kicker

Five balls rest on subminiature roller switches 10 (left) to 14 (right) in the 5-Ball Trough (OPTO)
Assembly. The Lock Ball Assembly (25-1240 coil, solenoid 17) releases one ball onto the up-kicker at
the right end, where the opto 15 sees it, and the 23-800 up-kicker (VUK, solenoid 1) kicks it into the
shooter lane.

Four harness runs show the sequence. After Start the ROM pulses 17. Raising only 15 draws 1 about
0.25 s later; emptying only trough position 14 draws it about 0.81 s later. If neither changes, the
ROM pulses 17 five times about 0.7 s apart, fires the auto launch (2) and the up-kicker (1), and
repeats that cycle about every 4.2 s for as long as the run lasts.

### Shooter lane and gun

There is no plunger. With a ball on the shooter-lane rollover (16), the player pulls the trigger of the
"007" gun on the cabinet (Fire Button, 9), and the ROM fires the 24-940 auto launch (2) about 0.08 s
later. It retries while 16 stays closed. Flasher 32 flashes while the ball waits, and the flipper
magnet comes on for about 6 s after the launch.

### Power scoop

The scoop at the upper left has a micro switch (50) on the Power Scoop Assembly and a separate Kick Big
Assembly (23-800, solenoid 4) that kicks the ball out.

### Tank

The Tank Trap Door Plunger Assembly (27-1500, solenoid 22) opens a trap door (diverter) wire in the
wire ramp on the left. A ball on that ramp then drops into the tank at the upper left, where 56 reports
it and the tank kicker (23-800, solenoid 14) kicks it out.

### Satellite

- **Drive.** The dish carries a 22-600 magnet (33). It is swung back and forth by a 24v AC 6 RPM motor
  through a crank arm and cam link, and the motor is switched by the satellite motor relay (21, a 24V
  DC 10A DPDT relay).
- **Home switch.** A motor-cam microswitch reports home (20). The ROM runs the motor at power-up until
  20 closes and releases the relay about 0.1 s after it does. If 20 never closes, it gives up after
  about 14 s.
- **Launch ramp.** The Satellite Launch Ramp Assembly (solenoid 20) lifts a ramp with a skill-shot flap
  in the centre of the playfield so the ball can run up onto the dish.
- **Ball hold.** The magnet board holds the ball there while 33 is on and reports it on 23. The
  Satellite flasher (28) lights the dish.

### Up-down ramp

The Up-Down Metal Ramp Plunger Assembly (27-1500, solenoid 18) moves the metal ramp at the upper right.
The retained script lowers it while 18 is on. No switch reports its position.

### Flipper magnet

A 22-600 magnet sits under the playfield between the flippers (34), and the magnet board reports a
ball on it (24). It catches balls heading down the centre.

### Targets, bumpers and slingshots

These are stand-up targets only, with no drop targets or reset coils:

- the left bank 25-28 (printed "left 5-bank" but with four switches)
- the right 5-bank 44-48
- the 2-bank 33/34
- the left and right stand-ups 30/31
- the eject stand-up 39

There are also three turbo bumpers (9-11 / 41-43, with lamps 19, 27 and 41 in their caps) and two
slingshots (12/13 / 61/62).

## Manual and table discrepancies worth knowing

- **Bulb types (open conflict).** The lamp grid prints #44 in every cell and the flash lamp chart
  prints #906 for the playfield sockets of 25-27. The playfield bulb pages instead list 54 #555 wedge
  bulbs, the three turbo pop bumper sockets marked "Use #555 Bulbs only", and no #906 bulb or socket
  (quantity 0, "not used in this game"); they also list 94 #44 bayonet bulbs, so #44 bulbs are on the
  playfield too. The boards page says the eight light boards L1-L8 carry #555 bulbs, but not which
  lamps sit on them. The ramp assembly pages list #555 bulbs in the "Tank Multiball" and two-bulb
  "Lock Ball" signs, the Helicopter Assembly and the Spot Light Assembly, the last two in a socket the
  wedge-base page lists at quantity 0. So the turbo bumper lamps 19, 27 and 41, the ramp sign and
  helicopter lamps (by their names most likely 49, 60, 61 and 69), and an unknown set of other
  playfield lamps take #555 bulbs. Pinned PinMAME models every lamp as #44 and all eight flash lamps
  as #89, which for 25-27 matches the bulb pages rather than the flash lamp chart. The start button
  and the speaker-panel letters, whose own parts list prints #44, are not in dispute.

- **Coil part number.** The coil chart prints the power scoop coil as 090-5000-01. The Kick Big
  Assembly prints 090-5001-01.
- **Left 5-bank.** It is printed as a 5-bank but has four switches (25-28) and four lamps (45-48).
- **Slam tilt.** `sega2.vbs` sets `swSlamTilt = 8`, a position the manual prints Not Used. The retained
  table writes the slam tilt at 7 itself, and the manual puts it at 7.
- **Switch 49.** The table binds a rollover trigger (SW49) to 49, which the manual prints Not Used.
- **Solenoid 45.** The table binds `SolCallback(45)` to a no-op.
- **Flasher 26.** The table drives flasher 26 on a light at the GOLDENEYE insert, not at the flipper
  magnet the manual names, and it drives flasher 30 on two lights, neither at the helicopter.

## What would complete the record

- A scan of the manual with legible location-drawing callouts, a second independent table geometry,
  or a survey of a real machine, to validate positions and place the missing flasher sockets and
  lamps 40 and 58.
- Photographs of an unrestored playfield's underside showing which inserts sit on light boards L1-L8
  and which bulbs the FLAMP 1-3 sockets carry, to settle the bulb conflict.
- A playfield G.I. socket list.
- The meaning of the magnet board's aux latch bits 2 and 3, which LibPinMAME's default mode publishes
  at 35 and 36. A ROM trace of what `gldneye` writes to the magnet board would settle it.
