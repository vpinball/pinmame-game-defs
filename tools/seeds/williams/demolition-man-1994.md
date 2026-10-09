# Demolition Man (Williams, 1994)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism and
recreation note is source-reconciled; `variant_differences` is missing because the four prototype
drivers' hardware is undocumented, and `spatial_placement` because the back-panel G.I. string, three
lamps and three back-panel flashers have no defensible socket position in the retained table and no
drawing or bulb count can validate the G.I. bulbs**

## Identity and evidence precedence

This is the Williams WPC-DCS widebody ("SuperPin") released February 1994, model 50028, IPDB 662,
7,019 units, designed by Dennis Nordman. It covers the twenty `dm_*` drivers of pinned PinMAME, all
sharing one `dmGameData`:

- Production arcade ROMs: `dm_lx4` (LX-4, the parent), `dm_lx3`, `dm_la1` (the first, with an L-1 U2
  sound ROM), and their community LED Ghost Fix revisions `dm_dx4`, `dm_dx3` and `dm_da1`; the
  community competition patch `dm_lx4c` (2020). All `identical`.
- Williams home ROMs `dm_h5`, `dm_h5b`, `dm_h6`, `dm_h6b` (the B builds are "Coin Play"), the ghost-fix
  `dm_dh5` and `dm_dh5b`, and the competition patch `dm_h6c`. They use an eight-ROM DCS sound set; the
  manual's A-16917-50028 sound board prints sockets U8 and U9 as "Not Used" on the arcade build, so
  the home set fills sockets the board already has. `identical`.
- Prototypes `dm_pa2`, `dm_px5` and their ghost-fix builds `dm_pa3`, `dm_px6`, with the prototype P-4
  sound ROMs. `unknown`: they share the production `dmGameData`, which proves PinMAME's routing but
  not the prototype machines' hardware, and no retained source documents the prototype playfields,
  so `variant_differences` stays in `coverage.missing`.
- FreeWPC "Demolition Time" `dm_dt099` and `dm_dt101` (2014): community firmware for this machine, a
  1 MB image where the production U6 part is a 27c040 and the manual's jumper chart covers only
  1M/2M/4M ROMs. `compatible`; pinned dm.c notes that 1.01 does not use solenoids 28 and 30, so its
  output use is not the Williams ROMs'.

Evidence precedence: the retained known-working Knorr/Kiwi 1.3.1 table script (`cGameName = "dm_lx4"`)
is runtime ground truth; the operations manual 16-50028-101 (March 1994, IPDB, 308 ppi scans with
an OCR layer) controls construction, wiring and fitment; pinned PinMAME `97aa922b` controls the
generation and the public addresses; the ROM's own service tests, run on the legal `dm_lx4` ROM with
the pinned library, settled every polarity, every switch, coil, flasher and lamp name the ROM
prints, and the claw/elevator controls; the table supplies coordinates. Every table used is
transcribed under `evidence/excerpts/williams.demolition-man.1994/`.

## Controller platform and address topology

`GEN_WPCDCS` (hardware generation `0x10`), `wpc_dispDMD` (one 128x32 DMD), Fliptronic II flippers.
`FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L | FLIP_UL)`: lower flippers and an upper left flipper are
CPU-controlled; the upper right flipper circuit has no flipper on it.

- Switches: coin door 1-8, matrix 11-88 (column-first), Fliptronic 111-118, DIP 1-8.
- Solenoids: 1-28 on the power driver board; 29-32 PinMAME's WPC state remap (29, 30 and 31 carry
  remapped GPIO/game-on state, 29 and 31 seen active in every run; 32 is constant zero); 33 the upper-right flipper power line used as the **claw magnet**, 34 its unused hold
  line; 35/36 the upper left flipper; 45-48 the lower flippers; 37-44 and 49-50 unused; **51-58 the
  auxiliary 8-driver board's flashers**, which the manual prints as 37-44. `dm_getSol` publishes
  `WPC_EXTBOARD1` bits 0-7 as `CORE_CUSTSOLNO(1)`-(8), and the ROM's T.5 FLASHER TEST shows the
  printed numbers 37-44 while it pulses 51-58 in order.
- Lamps: the 8x8 matrix 11-88; 74 and 75 are Not Used; 86-88 are the cabinet Buy-in, Launch Ball and
  Start button lamps.
- G.I.: public 0-4 are the manual's strings 01-05: Back Panel, Upper Right, Upper Left, Lower Right,
  Lower Left (the T.6 test's names, in that order).

## Switch polarity and names

PinMAME's `dmGameData` inverted-switch mask `{0x00, 0x00, 0x30, 0x3f, 0x00, 0x00, 0x40, 0x2f, ...}`
inverts public 25, 26, 31-36, 67, 71-74 and 76 - the same fourteen cells the Switch Matrix page
shades "Opto Switch" (both sides enumerated). In the ROM's T.1 SWITCH EDGES every matrix switch
11-88 (22 excepted, it stayed released) was named at public 1 and cleared at 0, with one exception:
24 Always Closed is named when it falls to 0, so a recreation holds 24 at 1. T.1 also names 28, 37,
68 and 75 "NOT USED". The T.14 CLAW TEST, which draws an X "when the switch is activated (blocked)",
marks Claw R. (25), Claw L. (26), Elev. Index (67) and Elev. Hold (74) while each is 1. So a recreation
drives every opto at public 1 while its beam is blocked and never inverts it again; the optos'
matrix contacts are closed at rest (`normally_closed: true`), every other switch is normally open.

Fliptronic: `WPC_FLIPPERS` returns the complement of the flipper column, so 111-118 are already
normalized. In T.1, 112 fired the lower right flipper (45/46) and 114 the lower and upper left
flippers (47/48 with 35/36); **116 and 118 did the same** (116 is the unused F6 position, 118 the
upper-left cabinet opto). PinMAME rewrites the end-of-stroke bits 111, 113 and 117 from the coil
states; it does not synthesize 115 (no `FLIP_SOL(FLIP_UR)`), which reads back a host write and which
the ROM ignores. The cabinet has two red flipper
buttons and two A-17316 opto boards with two optos each, and the gun handles' mechanical triggers
also operate the flippers; no page says which actuator interrupts which opto. The table's wpc.vbs
writes only 112 and 114, which the ROM treats as complete flipper inputs.

The handles: switch 11 is the cabinet Launch Ball button wired with the right handle's thumb
button; 12 is the left handle's thumb button; 23 is the cabinet Buy-in (Extra Ball) button.

The Switch Matrix page prints 75 "Elevator Ramp" and the switch drawing has a balloon 75, but the
Switch Locations list and the Section 3 reprint print Not Used and the ROM names 75 NOT USED. The
table's elevator-ramp trigger writing 75 is harmless.

## The Cryoclaw and elevator (headline mechanism)

The Cryoclaw/Elevator is two gear-reduced motors and an electromagnet:

- **Elevator** (A-17597): one-direction 14-7993 gear motor on solenoid 18, pulsed by the CPU to slow
  it. The Elevator Index opto (67) detects DOWN; the motor coasts so the actuator normally stops just
  past it. The Elevator Hold opto (74) sees a ball on the elevator (pinned dm.c: it also reads blocked
  while the elevator rises empty, and the game expects Hold to clear shortly before Index sets when
  lowering an empty elevator).
- **Claw arm** (A-16989): reversible 12 V gear motor 14-7992 through the A-16120 D.C. Motor Control
  board: solenoid 19 is "Claw Motor Left" (away from the elevator), 20 "Claw Motor Right" (toward
  it). The CPU pulses the lines to vary speed and, per dm.c's P-ROC notes, drives both together while
  pulsing; a full swing takes about 1.15 s. In the T.14 run CLAW RIGHT drove 19 and 20 together.
- **Position optos** on the A-16986 Cryoclaw Opto PCB: 25 Claw Right, 26 Claw Left. Manual state
  table: Right blocked/Left open = arm at right over the elevator; Right open/Left blocked = arm at
  left; both open = in range; both blocked = out of range, and the CPU refuses to run the motor (a
  disconnected board reads the same).
- **Magnet**: SZ-33-3000 on the arm, driven by the Fliptronic upper-right flipper power line
  (public 33, "CLAW MAGNET" in T.4). The claw test's MAGNET ON is "on solidly for a short period and
  then pulsed for a longer period".

A cycle: the right-ramp diverter (solenoid 5 power, 15 hold, one A-17241 assembly) opens and sends a
right-ramp ball to the elevator; the arm moves right over the elevator, the magnet comes on, the
elevator lifts the ball to it, the arm swings left under player control (flipper buttons or gun
triggers) and the player drops the ball (launch or handle buttons) onto one of five goal lanes:
Capture Simon (81, which feeds the bottom popper), Super Jets (82), Prison Break (83), Freeze (84),
ACMAG (85), lit by lamps 61-65. In multiball and ball search it runs automatically. On a detected
fault the CPU keeps the diverter closed; the errors are Claw Disabled, Arm Out of Range, Elevator
Broken, Magnet Broken, Claw Motor Error and Ramp Diverter Is Stuck Open/Closed. At power-up the game
cycles elevator, claw and magnet to drop any captured ball at ACMAG (dm.c). T.14's functions run only
while Enter is held: AUTO RUN, CLAW LEFT, CLAW RIGHT, RUN ELEVATOR, PARK ELEVATOR ("runs the elevator
motor until the elevator index"), MAGNET ON.

PinMAME's `dm_handleMech` models all of this only when `--handle-mechanics` enables it; the retained
table keeps `HandleMechanics = 0` and models the arm (147-step cvpmMech on 19/20, 25 at 0-2, 26 at
140-147) and the elevator (70-step cvpmMech on 18, 67 at 0-2, 74 at 65-70) itself. Their step counts
are the table author's, not measurements.

## Other mechanisms

- **Trough**: five balls on the 7 Ball Trough opto boards, 31 (right, exit) to 35 (left, entry) and
  Trough Jam 36. A drain rolls straight in (no outhole kicker); Ball Release (1) feeds the shooter
  lane. The assembly pages say five balls; one error passage says the game "normally uses six".
- **Auto plunger** (3) launches from the shooter lane (27) on the Launch Ball or handle buttons; no
  manual plunger. A launch feeds the upper left flipper via the right loop.
- **Top popper** (4, opto 73) and **bottom popper** (2, opto 76, the Underground/Computer chute);
  **eject** saucer (14, switch 66) beside the Retina Scan.
- **Car chase**: two Matchbox cars in the opto car tunnel; the ball pushes them into the optos 71 and
  72, then the Car Chase Standup (87).
- **Retina Scan**: a custom captive ball (eyeball) strikes the Eyeball Standup (77); lamp 78 and the
  Eyeball Flasher (53) light it.
- **Flippers**: lower right (45/46), lower left (47/48) and upper left (35/36) with FL-11629 and
  FL-11630 coils; the upper left flips with the lower left. The Upper Left Flipper Gate switch is 86.
- **Slingshots** left (41 -> 9), right (42 -> 10) and top (44 -> 12), **jet bumpers** left (43 -> 11)
  and right (45 -> 13): the ROM fires each coil from its switch (T.1 run). Upper and Lower Rebound
  (54, 88) are rubber switches.

## Lamps, flashers and general illumination

- Lamps 11 (Ball Save), 82 (Center Ramp Outer) and 83 (Center Ramp Inner) have two bulbs each (the
  ROM prints "C. RAMP OUTER (2)" and "INNER (2)"). The table's fader drives the inner pair from lamp 82
  and never reads 83 - a table defect.
- Flashers 17 and 21-28 each light one playfield bulb and one #906 backbox insert flasher; 23 is a
  #906 on the playfield, the rest #89. Flashers 51-58 are playfield-only; 55 (Elevator 2) has two
  bulbs. The Claw (17) and Elevator (55, 56) flashers sit on the back panel above the playfield's
  top edge on the location drawing.
- G.I.: all five strings feed the playfield (J121) and the backbox (J120); string 05 also the coin
  door. Printed bulbs #44 (playfield) and #555 (backbox).

## Spatial status and why the record stays partial

Coordinates are x/1093 and y/2162 of the retained widebody table (rear y=0, apron y=1), taken from
the objects the script binds (`tools/demolition_man_spatial_seed.py`). The factory location drawings
(PDF 99, 101 and 103) were read callout by callout by independent readers and fitted to the table's
jet bumpers, flipper pivots and (on the lamp page, whose bumpers are hidden) the Cryoclaw pivot hub;
a table placement whose own callout lands within 0.07 normalized under both fits is `validated`, which
is 111 of the 127 placements checked (`tools/seeds/williams/demolition-man-1994-callouts.json`). The
16 stay `observed`: switches 46, 53, 72 and 77, lamps 61 and 62, the ball release (1), the bottom popper
(2) and flashers 38, 40 and 44 (their callouts land beyond the limit); switches 54, 62 and 76 and lamp 13
(the drawings print no balloon for them); and the diverter hold (15), whose balloon has no leader and sits
beyond the outline. Projections onto a mechanism (trough optos, claw optos
and motors, elevator index, the diverter's power winding), the flipper windings and the G.I. are not
checked. Missing entirely: the Back Panel G.I. string (the table's UpdateGI has no case for string 0),
lamps 71-73 and flashers 17, 55 and 56 (the table renders them only as Flasher sprites, which are not
sockets). The playfield G.I. groupings are the table author's and no drawing locates a G.I. bulb.

## Author construction checklist

1. Leave PinMAME's inversion of the fourteen optos alone; drive each at 1 when blocked.
2. Hold 24 (Always Closed) and 22 (Coin Door Closed) at 1.
3. Wire the cabinet: 11 (Launch Ball button and right handle thumb), 12 (left handle thumb), 23
   (Buy-in), 13 (Start); flipper inputs 112 and 114 are enough, 118 is a second left input.
4. Build the claw arm on 19/20 with 25/26 at its ends, the elevator on 18 with 67 at the bottom and
   74 for a ball on it, and the magnet on 33; a one-direction elevator and a two-direction arm.
5. Drive the auxiliary flashers from 51-58, not from 37-44.
6. Treat 111, 113 and 117 as PinMAME-synthesized end-of-stroke bits; 115 is unused.

## Sources

The operations manual and parts list (IPDB 662), the IPDB page, pinned PinMAME `97aa922b`, the retained
Knorr/Kiwi 1.3.1 table and script with the wpc.vbs library it loads, and eight hash-pinned LibPinMAME
harness runs of `dm_lx4` (T.1, two T.14, T.4, T.5, T.6, T.8, T.12). The curator is
`tools/curate_demolition_man.py`; `tools/demolition_man_runtime_evidence.py` builds the runtime
evidence and `tools/demolition_man_spatial_seed.py` the placement seed.

## Procedural note

`coverage.missing` is `["variant_differences", "spatial_placement"]` and the record remains `partial`. Wiring-detail
disagreements inside the manual (the lamp matrix's J133 row prefix against the connector list's J134,
the F2/F6 wire colours swapped between the switch matrix and the flipper pages, the coin-door J2 pin
numbering, the J133-7 "not used" row-6 pin) are kept literally in the excerpts and stated on the
affected devices; none changes a device, its address or its fitment, so the record opens no conflict.
