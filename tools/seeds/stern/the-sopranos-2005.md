# The Sopranos (Stern, 2005)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled; only `spatial_placement` is missing, because the retained table does not model
the trough switches, the safe limit or the five Episodes lamps, and several coil placements fall outside what the
factory drawings confirm**

## Identity and evidence precedence

This is Stern's Whitestar machine of February 2005, model I-0085, IPDB 5053, designed by George Gomez. It covers the
21 `sopr*` drivers of pinned PinMAME: CPU 5.00 (`sopranos` and its French, German, Italian and Spanish clones), 4.00,
3.00 (with `soprano3`, the alternative-sound set), 2.04 and the language-only 1.07 sets. `segames.c` builds all of them
from one `init_sopranos`, `INITGAME(sopranos, GEN_WS, se_dmd128x32, SE_BOARDID_520_5068_01)`: lower flippers only
(`FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`), two extra lamp columns (lamps 1-80), no custom solenoids, a 128x32 DMD and the
520-5068-01 auxiliary driver board for the UK posts. The ROMs differ in rules, language and sound, not hardware, so
every driver is `identical`. IPDB records that a few machines were first built on S.A.M. boards, tested overseas and
converted back to Whitestar before sale; no PinMAME driver represents a S.A.M. build.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks and
mechanism causality; the official service manual (born-digital, 214 pages, byte-identical to the copy IPDB hosts)
decides construction, wiring, parts and placement on the drawings; pinned PinMAME decides routing. Three harness runs
of `sopranos` 5.00 confirm the routing and settle the stacking opto's sense. The retained table is the
freneticamnesic/32assassin 1.0.2 beta rebuild; the pinned corpus's 2024 v1.22 script descends from it and repeats its
bindings, so it corroborates them but is not independent.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). Column 6 (41-48), 30, 52, 63 and 64 are NOT USED.
  The dedicated inputs are -3 memory protect, -2/-1/0 the red/green/black service buttons (DS-6/7/8), 84 left button
  (DS-1), 83 left EOS (DS-2), 82 right button (DS-3), 81 right EOS (DS-4) and 88, the NOT USED DS-5. 85-87 reach no
  input. The country selector is DIP bits 1-5.
- **Solenoids.** Public 1-32 are Q1-Q32 except the flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right) off
  public 15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left flipper coil
  at 48 and the right at 46; 45 and 47 are their power-phase states. Public 15 is PinMAME's fast-flip / game-on state
  (sega.vbs's `GameOnSolenoid = 15`): it rose on Start and fell at the drain. 33-35 are the UK board's AUX 1-3; 16, 36,
  37-44, 49 and 50 are unused.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column); 62-64 are NOT USED; 79 exists only with the
  tournament kit. **G.I.** is one relay at public 0.

## Switch polarity and names

Whitestar's `switch_r` and `dedswitch_r` both hand the CPU the complement of PinMAME's state and the driver leaves
`invSw` at zero, so public 1 is a closed contact everywhere. Every matrix switch, the two trough optos included, is
normally open:

- The Trough Up-Kicker Dual OPTO Boards page (PDF 132) states that the receiver acts as an open switch while light falls
  on it and as a closed switch when the beam is blocked.
- The table's `bsTrough` holds the VUK opto 14 at 1 while a ball waits at the up-kicker.
- For the stacking opto 15, which neither script writes, the ROM answers: with four balls held on 11-14, raising 15 to 1
  (or holding it there from power-up) makes the ROM fire the up-kicker six times and then the auto launch, while 0 draws
  nothing. Pass a kicked ball through 15 as a short 1 pulse.

The two end-of-stroke switches are the exception. The flipper wiring diagram prints them N.C.: closed at rest, opening
about 1/16" when the flipper is energized, and the CPU re-pulses the coil if the switch recloses during a hold. PinMAME
does not synthesize them here (no `FLIP_EOS`), so the ROM reads whatever the host writes; a recreation that leaves 81/83
at 0 only loses that re-pulse.

The memory-protect switch -3 is N.O. and closed by the shut coin door; public 1 blocks writes to protected RAM, so a
closed door is -3 at 1.

Library and table quirks, all recorded on the devices and none of them about the machine:

- `sega.vbs` and PinMAME's keyboard port put the slam-tilt key on 55, which this game prints as Tournament Start; the
  optional slam tilt kit is wired to 53.
- `sega.vbs` names the EOS addresses `swURFlip`/`swULFlip`.
- The table's `solTrough` pulses 22 (Center Lock 1) instead of 15.
- The pinned v1.22 script also writes 16 on the Start key; the retained 1.0.2 table's same lines are unreachable
  behind the VPinMAME key handler.
- The table models the right-ramp switch 25 as a spinner, which v1.22 corrects.

The manual's switch parts page prints the eject switches' matrix numbers as `17 & 18`; the grid and the same page's
wire-gate row show they are 17 and 28.

## Ball handling

- **Trough.** Four balls on 11 (left), 12, 13 and the VUK opto 14 at the up-kicker (Q1); the stacking opto 15 above it.
  Hold occupied positions at 1, initialize 11-14 at 1.
- **Shooter.** Manual plunger and the Q2 autoplunger arm; shooter-lane switch 16.
- **Ejects.** Two 30-degree ejects (500-6511-01): the left eject under the fish (17, Q21) and the center eject under the
  safe (28, Q3). A ball held in either drew repeated kicks in the gameplay run.
- **Three two-ball locks, each an up/down post that is down while its coil is energized:** Center Lock 1/2 (22/23) behind
  Q4 (500-5867-02, the "spinner lane ball lock"), Boat Lock 1/2 (31/32) on the right steel boat ramp behind Q22, and Bing
  1/2 (19/20) at the Bada Bing! behind Q23 (both 500-5867-09). In the gameplay run the left ramp (9) raised Q23 and the
  right ramp (25) dropped it, so the ROM can hold a post energized for a long stretch.
- **Control gates.** Q5/Q6 drive the left and right 2-way ball gates at the top (32-1800 mini coils, no position switch).

## Toys and targets

- **The safe.** A door above the playfield, struck on Safe Hit Left/Right (21/24), with a Safe coil (Q8, 22-1080) and a
  Safe Latch coil (Q30, 27-1500) on one dual bracket below and a Cherry limit switch 10. The ROM fired Q8 with Q30 at
  power-up and on every safe hit. In the table, energizing Q8 starts the door closing and releasing it starts it opening;
  while Q30's latch is set a Q8 change only selects the closing state without moving an idle door. The table writes 10
  at the end of each travel (1 open, 0 closed).
  Neither the manual nor a run settles the factory door's sequence or the limit switch's sense, so treat the table's
  model as a working recreation and 10 as the end-of-travel sensor.
- **The fish.** A molded head on the left side with a jaw lever worked by Q17 (27-1500) and a #44 LED flash lamp (Q25)
  behind its clear eyes. The ROM opens the jaw with speech; in the run it moved with a bumper hit and while a ball sat
  in the left eject below.
- **Bada Bing! pole dancers.** Q18 energizes a relay (500-6700-00) that runs a 24 V AC bi-directional motor (500-6887-00,
  about 46-55 RPM). The motor turns two dolls on shafts through a belt and pulleys. There is no position sensor: the
  dancers spin while Q18 is on.
- **1-bank drop target** (500-6893-01). Switch 26 closes while it is down; Q14 resets it and the 32-1250 trip coil Q7
  knocks it down. The ROM reset it at power-up and on Start, and tripped and reset it at the drain.
- **Bumpers, slingshots and flippers.** Left/right/bottom bumpers Q9/49, Q10/50, Q11/51, with red domes Q29 on the left
  and bottom bumpers. Slingshots Q12/59 and Q13/62, two contacts each. Flippers Q15/Q16 on one 50 V supply: a 40 ms kick,
  then 1 ms every 12 ms while held. Every one of these switch-to-coil pairs fired in the gameplay run.
- **Other switches.** Left/right orbit 18/33, left ramp 9, right ramp 25 and right ramp exit 29 (wire-gate switches);
  spinner 27; the standups 34/35 (narrow yellow) and the right 2-bank 36/37; top lanes 38-40; outlanes and return lanes
  57/58/60/61.
- **UK Post Save.** Board 520-5068-01 drives AUX 1/3, the left and right outlane ball deflectors (500-5788-02), and
  AUX 2, the center up/down post (500-6293-00). The UK cabinet buttons on 1 and 8 ask the ROM for them. Standard
  machines fit none of it, so all five devices are `optional`. Q24 is likewise optional: the coin meter, which the ROM
  pulsed four times per coin.

## Lamps, flashers and general illumination

- **Lamps.** All 80 lamp cells are wired as printed. 65-72 are the eight RIP portrait lamps behind the back panel (65-68
  top row, 69-72 bottom row) and sit outside normalized playfield space. 79 and 80 are the tournament and start button
  lamps.
- **Flashers.** Q19 super jackpot, Q20 safe, Q25 fish and Q27/Q28 the yellow sling domes. Q26 is the back flash: two #89
  on the back panel and one #906 yellow dome at the stage. Q29 is the two red bumper domes, Q31 one flasher on each side
  of the playfield, and Q32 two at the truck.
- **G.I.** One relay feeds four fused circuits:
  - Back panel, 12 #44 (F24).
  - Middle/lower right playfield, 13 by its location count and the drawing, though the bulb line prints 11 + 1 (F25).
  - Upper right playfield, 8, plus the 2 coin-door bulbs (F26).
  - Middle/lower left playfield, 12 (F27).

  The table's GI collection holds 33 lights, matching the 33 playfield sockets the G.I. drawing letters.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, normalized against its 952 x 2300 bounds, and are
checked against the three factory location drawings. The drawings validate most of them: all 62 table-placed lamps,
and most switches, coils and flashers. These stay unvalidated:

- **Projections onto mechanism objects.** The table does not model the trough switches 11-15 or the safe limit 10. The
  EOS contacts sit on the flippers, the auto launch is placed on the shooter-lane trigger, and the drop-target coils on
  the target. The safe coils, fish jaw, fish flasher and Bada Bing! relay are placed on the objects they move.
- **Drawing measurements (candidates).** The five Episodes lamps 73-77, which the table stacks at one point, and the UK
  AUX posts, which the US table lacks.
- **Placements the drawings do not confirm.** The flipper and slingshot coils, whose drawn boxes sit on coil bodies
  away from the bats and walls; the second Q31 flasher, which the table omits; and anything the spatial report lists.
- **G.I.** The 33 G.I. placements, whose bottom-view drawing has no reliable control fit.

Nothing here is a disagreement about the machine; the blockers are missing geometry, so the record carries no
conflicts.

## Author construction checklist

- **Ball path.** Build the 4-ball trough with stacking opto, the manual and auto shooter, two ejects, the three
  post-locks (each down while energized), the two control gates, the drop target with trip and reset, and the safe
  door with its two coils and limit switch.
- **Toys and scoring parts.** Build the talking fish (jaw coil and eye flash), the Bada Bing! motor and dancers, three
  bumpers, two slingshots, two flippers with N.C. EOS, the spinner, standups, the 2-bank, the lanes and the orbits.
- **Initial state.** Initialize 11-14 and -3 at 1. Pulse 15 per kicked ball.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases and 15 is game-on. Bind 33-35 only for a UK
  build, and Q24 only for a coin meter.
- **Displays and lights.** One 128x32 DMD in the cabinet. Recreate the 33 playfield G.I. bulbs, the 12 back-panel and 2
  coin-door bulbs, all lamps and flashers.

## Sources

- `manual.stern.the-sopranos.2005`: SHA-256 `4765c79a9fac44d14e4330477ffb4ab4d7af259499a3b5d1156adf83d75b0c88`, IPDB 5053's
  service manual; excerpts under `evidence/excerpts/stern.the-sopranos.2005/`.
- `vpx-table.sopranos-freneticamnesic-32assassin-1-0-2` and its embedded script (`56262b8b...`), with the retained
  1,441-file extraction and its manifest.
- `vpx-script.sopranos-v1-22`: the pinned corpus script (`ab44cf36...`).
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `runtime.the-sopranos.stacking-opto-and-gameplay`: three LibPinMAME runs, summarized in
  `evidence/runtime/whitestar/the-sopranos-stacking-opto-and-gameplay.json`.
- `drawing-callouts.the-sopranos.2026-10-09`: `tools/seeds/stern/the-sopranos-2005-callouts.json`.
