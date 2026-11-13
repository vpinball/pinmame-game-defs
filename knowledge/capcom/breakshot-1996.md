# Breakshot (Capcom, 1996)

Breakshot is Capcom Coin-Op's billiards-themed pinball of May 1996 (IPDB 3784, model BRK3002, 1,000 built),
designed by Greg Kmiec. It is a single-level playfield with no ramps, three flippers, three star bumpers, two drop-target
banks, a captive ball with a Newton ball, and a centre feature: a post that rises in front of three pockets. This note
collects what a table author needs beyond the structured definition `machines/partial/capcom/breakshot-1996.json`,
which is partial only because seven fixed G.I. sockets have no checked position (see General illumination).

## Identity and drivers

The physical machine is the one IPDB 3784 and the Capcom operator's manual PM00147 (issue 05/02/96) describe. PinMAME runs
it with five drivers: `bsv103` (1.3, the root and the only one built with `INITGAMEFF`), `bsv102` (1.2), `bsb105` (Beta
1.5) and the two redemption builds `bsv100r` and `bsv102r`. All five use the same switch inversion mask and flipper
declaration, so they share one address map; only `bsv103` publishes solenoid 51, the ROM's game-on (Fast Flips) state.
The redemption builds were not run for this record.

PinMAME also declares `pp100`, Illinois Pinball's Pool Player of 2000, as a clone of `bsv103` with the same routing. Pool
Player was built from Breakshot machines, but its own sources describe a modified playfield and versions with an
automatic ball launcher, so it is a partial record of its own, `illinois-pinball.pool-player.2000`.

## Controller and addresses

Breakshot runs on modified Capcom hardware without a switch board: it drives a single lamp matrix and strobes its
switches with the second lamp matrix's hardware (PinMAME's `hw.lampCol` is 1). That shapes its switch map:

- Public 1-8 are the coin door and cabinet inputs: coins 1-4, the two flipper buttons (5 left, 6 right), Start (7) and the
  coin-door switch (8).
- Public 9-16 are dead under PinMAME: nothing writes or reads internal column 0 on this board. The manual's "*9 COIN
  DOOR-SLAM" is read by the ROM at public 29.
- Public 17-80 are the strobed matrix. The ROM reads the slam switch at 29, the tilt bob at 30 and the upper right
  flipper button at 21.
- 81-88 are PinMAME's flipper column. 82 and 84 are the host inputs for the right and left flipper buttons (core copies
  them into 6 and 5 every frame); the end-of-stroke bits 81, 83 and 85 are rewritten every frame, and nothing acts on 86-88.

Every switch read is inverted by the board, and PinMAME's `capInvSw` mask normalizes the six optos (36-38, 53, 54, 65), so
a public 1 is a closed contact or a blocked beam: write 1 when a ball is present. `normally_closed` is false for every
contact switch and true for the six optos, whose receivers conduct while the beam is clear.

Solenoids 1-32 are the driver board's outputs, 17-24 and 27 unfitted. At the pinned revision PinMAME mirrors each flipper
coil to a power and a hold address: S9 (left) to 47/48, S10 (right) to 45/46 and S11 (upper right) to 33/34. The
repository's Capcom controller profile still describes an older mirror table (9 to 45 only, 10 to 47), and its bsv
flasher range (28-32) is also older than the pinned source, which types only 28 as a bulb; this record follows the pinned
source.

Lamps 1-64 are one 8x8 matrix; 65 and 66 are the CPU and sound board LEDs. General illumination has no PinMAME output.
The ROM's Lamp Test and the manual's lamp matrix sheet agree on every lamp's column, row and wire colours but print
different connectors (the ROM J5/6 and J7/8, the sheet J9/10 and J4/5); the record's wiring follows the ROM. The sheet
calls lamp 11 "Jackpot (two)": two bulbs, both under the one Jackpot insert below LIT POCKET AWARDS. No source shows where
they sit under it, so the record places the second bulb on the first, the centre of the table's light l11.

## Flippers

Three flippers: left (S9), right (S10) and upper right (S11, beside the bonus saucer). The right cabinet button carries two
switches, 6 for the right flipper and 21 for the upper right one; the drawing prints them side by side. In the harness,
holding 21 fired S11. The VPinMAME system script maps a staged right flipper key to 81 instead, which the ROM never sees, so
a recreation that wants the upper flipper on its own key must drive 21. Each flipper has an end-of-stroke switch the ROM
reads (33 left, 34 right, 71 upper right); the retained table never writes them.

## Trough, outhole and shooter lane

A drained ball rolls into the outhole under the apron (35). S1 kicks it into a three-ball trough under the apron that rises
towards the shooter lane, sensed by optos 38, 37 and 36, position 1 (36) at the shooter end. S2 serves the ball from
position 1 into the shooter lane (43), and the player plunges it by hand. At start-up the trough holds all three balls, so
36-38 read 1. Pressing Start with a credit fires S2 together with both drop-bank resets (S7 and S13); in the harness the
ROM pulsed S2 five times while 36 stayed closed and released it once the ball left position 1.

## Drop-target banks

Both banks have three drops and a standup behind them. The right bank on the upper right is 49 (left), 50 (centre) and 51
(right) with the standup 52, reset by S7; the left bank is 73 (lowest), 74 and 75 (highest) with the standup 76, reset by
S13. In the harness, dropping 49, 50 and 51 took the score from 0 to 9,000, and dropping 73 and 74 each played the ROM's
drop-target animation. The ROM resets both banks with the trough eject when Start begins a game. With a bank's three drops
held down for four seconds it fired neither reset, and the run served no further ball, so when it resets a completed bank
during play was not observed.

Two sources number the right bank one lower: the manual's switch drawing (discs 48-51) and the retained table (drops 48-50,
standup 51). The manual's own table, the ROM's Switch Test and the harness agree on 49-52: 48 alone changes nothing.

## Centre feature

At the centre, two Lite Super Cue targets (77, 78) flank a post (S12 up, S14 down; switch 66 closed while it is up) at the
foot of the centre pocket assembly, and an opto (65) sits at the assembly's foot. Behind the post are three pockets side by
side, each with a switch (68, 69, 70) and an eject coil (S25, S26, S32), lit by inserts 42-44 and by the matrix lamps 25 and
26 (Center Pocket G.I.). The Center Pocket Flash, S28 (part LP00103), lights two bulbs above the pockets, one on
each shoulder of the assembly; PinMAME models it as a #89 bulb. IPDB describes the feature as a
large metal plug that rises after each captured ball and that the player hits, with three scoops behind it that hold balls
for multiball. The retained table raises three walls for the post and sets 66 once it is up.

## Other playfield features

- Star bumpers: 57 and S31 on the upper left, 58 and S30 at the lower centre, 59 and S29 on the upper right.
- Captive ball lane, upper left: the Newton ball passes a hit to the captive ball, which rolls over the captive rollover
  (79) to the captive standup (55). Lamps 3-5 and 8 line it.
- Top lanes 60, 61 and 62 under inserts 45, 32 and 27; the orbit optos 53 and 54 at the left and right orbit entrances;
  the bankshot lane 63 on the upper right (lamp 49).
- Top gates S16 (left) and S15 (right) on the 20 V line: each gate stands open while its coil is energized.
- Left outlane kickback S6, lit by lamp 28 KICKER; bonus saucer 67 with S8 below the upper right flipper.
- The bonus rack: lamps 50-64 in a triangle pointing down above the flippers, 60-64 across its top.

## Redemption and the optional dispensers

The manual documents a redemption setup the standard machine does not ship with
(`evidence/excerpts/capcom.breakshot.1996/redemption-and-dispensers.md`). Its Redemption menu (F, PDF 55), which it says
is not in every software version, pays tickets, tokens, credits or extra balls at up to five score levels within a time
limit, through an optional ticket dispenser (adjustment B1-16: Deltronics model 1275 or Coin Controls CTD10) or token
dispenser (B1-17: a Bally Wulff or Coin Controls dispenser, or a Coin Controls Compact Hopper). The ticket dispenser has a
motor, a notch switch and a meter (test C1-09); a token dispenser is fired by a solenoid and usually has no feedback
switch (test C1-10). Both hang off the RS232/Coin Meter PCB on the CPU's J3, which carries a ticket meter, a coin meter
and a motor drive line; in the German configuration a Token Driver PCB switches 50 V to the token dispenser (PB-6
wiring, PDF 145). `bsv100r` and `bsv102r` are the redemption builds.

None of this reaches a PinMAME address. Pinned `capcom.c` leaves the J3 lines unmapped, so no dispenser motor, solenoid
or meter is published. The ROM numbers the ticket dispenser's notch switch 16 (WHT-GRY), in the cabinet column PinMAME
never reads on Breakshot, and its Switch Test shows that name while public 32, 40, 64 or 72 is held, positions the
standard machine leaves empty. The structured definition records the standard machine; a recreation of a redemption
Breakshot has to model the dispenser outside the emulator.

## General illumination

The lamp table lists 54 #44 G.I. bulbs (LP00104) on four strings, 65A-65P (ORG/WHT, 14 bulbs), 66A-66N (BLU/WHT, 13),
67A-67M (GRN/WHT, 12) and 68A-68Q (BLK/WHT, 15), lettered without I and O, and the backbox fluorescent 69. The ROM does
not switch them and PinMAME has no output for them, so the structured definition has no device to carry them.

The lamp drawing marks every socket with its string and letter, so the strings' membership is the machine's own. The
retained table models 47 of the sockets as always-on lights of its `GI` collection, the bake sources of its G.I.
lightmaps (gi014 repeats gi011 exactly). Each socket's disc was paired one-to-one, nearest first, with a table light
and checked like the lamp placements: under the page's control fit and its callout fit on 62 lamp discs,
all 47 pairs land within the 0.07 callout limit, most within 0.01, and those sockets take the light's centre. 66L and
66N are the loosest, about 0.057 from gi044 and gi045: the drawing prints their discs below 66K and 66M, while the
table puts the two lights above. Seven sockets have no table light and keep their disc's position through the control
fit, observed only: 67A, 67B and 67F across the top, 68B at the top right, 68K on the right, and 65A and 65B, printed
just inside the outline's front edge beside disc 1 where the drawing shows no part. A disc is printed on or beside its
socket and is about 0.05 of the playfield width across, so a drawing-only position is good to a few hundredths. The
spatial report carries the same inventory with every offset (`uncontrolled_lighting` in
`reports/spatial/capcom/breakshot-1996.json`).

Those seven sockets are why the record is `partial`, with `spatial_placement` its only missing requirement: a position
read off a drawing alone is not a checked one, and the two at the front edge may not even light the playfield. A
recreation that models them, or a drawing that locates them, checked against a photograph of a Breakshot playfield
showing them (with the apron removed for 65A and 65B), would settle it.

| Socket | String wire | x | y | Position from |
| --- | --- | ---: | ---: | --- |
| 65A | ORG/WHT | 0.218 | 0.987 | drawing only (observed) |
| 65B | ORG/WHT | 0.278 | 0.987 | drawing only (observed) |
| 65C | ORG/WHT | 0.719 | 0.731 | table light gi04, disc within 0.007 |
| 65D | ORG/WHT | 0.681 | 0.776 | table light gi03, disc within 0.005 |
| 65E | ORG/WHT | 0.750 | 0.812 | table light gi02, disc within 0.003 |
| 65F | ORG/WHT | 0.685 | 0.832 | table light gi01, disc within 0.005 |
| 65G | ORG/WHT | 0.223 | 0.832 | table light gi05, disc within 0.004 |
| 65H | ORG/WHT | 0.157 | 0.812 | table light gi06, disc within 0.004 |
| 65J | ORG/WHT | 0.225 | 0.777 | table light gi07, disc within 0.004 |
| 65K | ORG/WHT | 0.188 | 0.732 | table light gi08, disc within 0.004 |
| 65L | ORG/WHT | 0.045 | 0.641 | table light gi001, disc within 0.003 |
| 65M | ORG/WHT | 0.046 | 0.606 | table light gi002, disc within 0.004 |
| 65N | ORG/WHT | 0.045 | 0.578 | table light gi003, disc within 0.001 |
| 65P | ORG/WHT | 0.042 | 0.549 | table light gi004, disc within 0.005 |
| 66A | BLU/WHT | 0.046 | 0.458 | table light gi005, disc within 0.003 |
| 66B | BLU/WHT | 0.073 | 0.427 | table light gi006, disc within 0.003 |
| 66C | BLU/WHT | 0.063 | 0.389 | table light gi007, disc within 0.002 |
| 66D | BLU/WHT | 0.076 | 0.354 | table light gi008, disc within 0.003 |
| 66E | BLU/WHT | 0.040 | 0.272 | table light gi009, disc within 0.005 |
| 66F | BLU/WHT | 0.041 | 0.135 | table light gi010, disc within 0.003 |
| 66G | BLU/WHT | 0.051 | 0.103 | table light gi011, disc within 0.004 |
| 66H | BLU/WHT | 0.085 | 0.080 | table light gi012, disc within 0.007 |
| 66J | BLU/WHT | 0.152 | 0.033 | table light gi048, disc within 0.007 |
| 66K | BLU/WHT | 0.338 | 0.374 | table light gi043, disc within 0.004 |
| 66L | BLU/WHT | 0.307 | 0.346 | table light gi044, disc within 0.057 |
| 66M | BLU/WHT | 0.569 | 0.373 | table light gi046, disc within 0.004 |
| 66N | BLU/WHT | 0.599 | 0.346 | table light gi045, disc within 0.057 |
| 67A | GRN/WHT | 0.211 | 0.032 | drawing only (observed) |
| 67B | GRN/WHT | 0.285 | 0.023 | drawing only (observed) |
| 67C | GRN/WHT | 0.361 | 0.016 | table light gi022, disc within 0.008 |
| 67D | GRN/WHT | 0.471 | 0.017 | table light gi023, disc within 0.006 |
| 67E | GRN/WHT | 0.558 | 0.018 | table light gi024, disc within 0.005 |
| 67F | GRN/WHT | 0.630 | 0.022 | drawing only (observed) |
| 67G | GRN/WHT | 0.211 | 0.136 | table light gi013, disc within 0.005 |
| 67H | GRN/WHT | 0.254 | 0.132 | table light gi015, disc within 0.010 |
| 67J | GRN/WHT | 0.253 | 0.206 | table light gi047, disc within 0.003 |
| 67K | GRN/WHT | 0.291 | 0.100 | table light gi12, disc within 0.003 |
| 67L | GRN/WHT | 0.399 | 0.100 | table light gi11, disc within 0.004 |
| 67M | GRN/WHT | 0.507 | 0.100 | table light gi10, disc within 0.005 |
| 68A | BLK/WHT | 0.801 | 0.027 | table light gi025, disc within 0.010 |
| 68B | BLK/WHT | 0.755 | 0.039 | drawing only (observed) |
| 68C | BLK/WHT | 0.882 | 0.052 | table light gi026, disc within 0.004 |
| 68D | BLK/WHT | 0.657 | 0.081 | table light gi021, disc within 0.003 |
| 68E | BLK/WHT | 0.614 | 0.100 | table light gi09, disc within 0.006 |
| 68F | BLK/WHT | 0.634 | 0.141 | table light gi020, disc within 0.002 |
| 68G | BLK/WHT | 0.779 | 0.148 | table light gi13, disc within 0.008 |
| 68H | BLK/WHT | 0.939 | 0.367 | table light gi028, disc within 0.014 |
| 68J | BLK/WHT | 0.931 | 0.394 | table light gi029, disc within 0.030 |
| 68K | BLK/WHT | 0.889 | 0.443 | drawing only (observed) |
| 68L | BLK/WHT | 0.792 | 0.460 | table light gi031, disc within 0.009 |
| 68M | BLK/WHT | 0.881 | 0.456 | table light gi030, disc within 0.013 |
| 68N | BLK/WHT | 0.850 | 0.577 | table light gi032, disc within 0.009 |
| 68P | BLK/WHT | 0.831 | 0.602 | table light gi033, disc within 0.006 |
| 68Q | BLK/WHT | 0.868 | 0.620 | table light gi034, disc within 0.008 |

## Defects in the retained table

The VPW v1.1 table plays correctly on bsv103 but reports several switches as other addresses than the machine. Each is a
defect of the table, recorded on the device it affects:

- Its slingshots are crossed (the left reports 42, the right 41).
- Its star bumpers are rotated (upper left reports 58, lower centre 59, upper right 57).
- Its right bank is numbered one lower (48-50 and the standup 51), so the ROM never sees its first drop.
- The comments beside its three flipper callbacks name the wrong flippers; the bindings themselves are right.

## Spatial placements

Every playfield placement is the centre of the retained table's object that the script binds to the address, or the
mechanism the switch or coil belongs to. The factory location drawings check 120 table placements and validate 120: each drawing was fitted on its bumper caps, flipper pivots and playfield-outline corners and on its other discs, and a placement validates when its own disc lands within 0.07 normalized under both fits (`tools/seeds/capcom/breakshot-1996-callouts.json`). The trough and its two coils lie under the apron, where the
drawings print only numbers in open space, so they are documented projections onto the script's trough objects. Lamp 11's
second bulb is a documented projection onto its first, under the same Jackpot insert.

## Sources

- Capcom operator's manual PM00147, 05/02/96, from IPDB: switch, solenoid and lamp tables and location drawings, the
  redemption menu, dispenser adjustments and tests, and the PB-6 interface wiring (excerpts under
  `evidence/excerpts/capcom.breakshot.1996/`).
- The ROM's own Switch, Solenoid and Lamp Tests and a short game, run on LibPinMAME from the pinned source
  (`evidence/runtime/capcom/breakshot-service-diagnostics.json`).
- PinMAME `src/wpc/capgames.c`, `capcom.c`, `capcom.h`, `core.h` and `core.c` at the pinned revision.
- VPW's Breakshot v1.1 table and its script, with the VPinMAME `Capcom.vbs` and `core.vbs` it loads.
