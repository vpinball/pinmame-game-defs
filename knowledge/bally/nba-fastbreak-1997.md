# NBA Fastbreak (Bally, 1997)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism and
recreation note is source-reconciled; only `spatial_placement` is missing, because no retained source
locates the general-illumination bulbs (strings 4 and 5 not at all, strings 1-3 only through one
community table's grouping)**

## Identity and evidence precedence

This is the Midway Manufacturing Company (trade name Bally) WPC-95 physical machine released March 1997,
model 50053, IPDB 4023, 4,414 units, four balls. It covers the eight `nbaf_*` drivers: `nbaf_31` (game
ROM 3.1 with sound S2 3.0, the parent), `nbaf_11` (1.1, the first production release), `nbaf_11a` (1.1 with
German speech), `nbaf_11s` (1.1 with the prototype sound ROM S0.4), `nbaf_115` (1.15), and `nbaf_21`,
`nbaf_22`, `nbaf_23` (2.1-2.3). All share one `nbafGameData` on `wpc_m95S`, so every driver is `identical`
to the physical machine. From 2.1 the firmware can link two machines for head-to-head play through the
NBA Fastbreak Linking Kit 58030 (a UART and line driver added to the Audio/Visual board and a cable on
J607); a linked game can also be played alone. PinMAME emulates that link's UART only in builds with
host serial support and a configured serial device; it uses no switch, lamp or solenoid address, so nothing
in this definition depends on it.

Evidence precedence: the retained known-working VPW script is runtime and mechanism-causality ground
truth; the May 1997 FINAL operations manual (16-50053.1-101, with schematics) controls physical
construction, part numbers, wiring and device presence, and the March 1997 edition was compared table by
table (its only differences are a lamp-matrix typo and a missing diode symbol); pinned PinMAME
`97aa922b` controls the controller generation and public addresses; the ROM's own service tests, run on
a legal `nbaf_31` ROM, settled polarity, names and every output's identity; the retained table supplies
coordinates and the factory location drawings check them. Every table used is transcribed under
`evidence/excerpts/bally.nba-fastbreak.1997/`, and the runs are summarized under
`evidence/runtime/wpc-95/nba-fastbreak-nbaf_31-*.json`.

## Controller platform and address topology

- WPC-95 (`GEN_WPC95`), a 128x32 DMD, and a second display: the two-digit shot clock (PinMAME layout
  index 1, `CORE_SEG7|CORE_NODISP`), which `nbaf.c` builds from solenoid writes (below).
- Switches: dedicated 1-8 (coin chutes and the four coin-door service buttons: 5 Escape, 6 Down, 7 Up, 8
  Enter), matrix 11-68 fitted, 71-88 printed NOT USED (the ROM's T.1 ignores them), and the Fliptronic
  column 111-118. Column 3 rows 1-7 (31-37) and the Fliptronic position F5 (115) are inverted by PinMAME's
  mask.
- Solenoids: 1-16 and 25-28 are the usual WPC-95 drivers; 17-24 the flashers; 33-36 are the upper-flipper
  Fliptronic circuits, which NBA Fastbreak uses for the four In The Paint shoot coils (`FLIP_SOL(FLIP_L)`
  only); 37-40 are the WPC-95 low-power lines (defender motor enable and direction, shot clock enable and
  count), mirrored by PinMAME at 41-44; 45-48 are the lower flippers (printed as circuits 29-32); 29-31
  are PinMAME state mirrors (31 is the fast-flip game-on flag, `wpc_set_fastflip_addr(0x7b)`).
- Lamps: the full 8x8 matrix 11-88; 87 and 88 light the SHOOT and Start buttons.
- GI: five strings; 1-3 (public 0-2) dim, 4 and 5 (public 3-4) are always on.

## Switch polarity: what the ROM's service tests settled

A T.1 SWITCH EDGES sweep set every public matrix and Fliptronic address to 1 and back to 0.

- Every fitted matrix switch is named by the ROM while its public level is 1, the masked optos 31-37
  included, so a consumer drives every switch active-high and never re-inverts. Through the mask, public
  1 on 31-37 is an open contact, so those optos rest closed (`normally_closed: true`), as their shaded
  "OPTO, TYPICALLY CLOSED" cells say.
- The defender optos 51-55 are shaded as optos too, but PinMAME does not mask them and the ROM names them
  at public 1, a closed contact: their matrix contacts rest open. The legend marks construction only.
- 24 (Always Closed) is held at 1 from power-up; the ROM names it on its 1 -> 0 edge.
- F5 BASKET MADE (115) is masked and also read through WPC-95's complemented flipper column, so the ROM
  sees the public level directly: it names it at 1, a raw open contact, so the opto rests closed. F7
  BASKET HOLD (117) is unmasked, so the ROM sees the complement as for the flipper buttons; named at 1, a
  closed contact, it rests open.
- 111 and 113 (end-of-stroke) read back 0 after a host write of 1: PinMAME rewrites them from the
  flipper coil state. 112 and 114 fire the lower flippers. 116 and 118, the second optos of the same
  cabinet buttons (wired on this game's own 3-11/3-13/3-14 pages although the parts list prints NOT USED),
  also fire the lower right and left flippers; drive both or either.
- The ROM fires a coil for its own switch even inside T.1: 23 -> 14, 57 -> 10, 58 -> 11, 61 -> 12,
  62 -> 13.
- The ROM's T.1 text prints matrix column 4's wire as GRN-WHT where the manual prints Green-Yellow
  (J206-4); a wiring-detail difference with no effect on addresses.

## The In The Paint shooters (headline mechanism)

Below the top lanes four saucers sit on a ring around the aerial hoop: positions 1-4 from left to right,
switches 68, 67, 66 and 65. Each is a Pass Assembly (A-21411-1 to -4) with a shoot coil on an upper
Fliptronic circuit (33-36) that throws the ball at the basket, and the pass coils move the ball along
the ring: Pass Right 1 (25) 1->2, Pass Left 2 (16) 2->1, Pass Right 2 (15) 2->3, Pass Left 3 (26) 3->2,
Pass Right 3 (27) 3->4, Pass Left 4 (28) 4->3. When IN THE PAINT is lit, a left or right loop shot feeds
the ring and the shot clock starts at 24; the shot map says to use the flippers to pass, and the player
must shoot from a position the defender does not block before the clock expires. A made basket breaks the Basket Made opto (115) and the ball comes to rest on Basket Hold
(117); a blocked shot drops into the jets. Each position's lamp (77, 78, 68, 67 for 1-4) lights when a
basket is made from it; all four start Around The World multiball. The Ball Catch Magnet (8, NBA Magnet
Assembly A-21520) sits at the middle of the ring under the basket; the manual does not describe its use, and
PinMAME's simulator uses it to catch a ball passed between positions 2 and 3 or leaving Basket Hold.

## The defender

The Defender Arm Assembly A-21413 swings a figure between the shooter positions and the basket. A 14-8034
motor on the High Current Driver Board C-13963-1 runs from two low-power lines: 37 enables it, 38 sets
the direction (on = toward POS 4, the right). Five optos on the Defender Switch Board A-21402 report POS 1
(55), POS 2 (54), LOCK (53), POS 3 (52) and POS 4 (51); the factory switch drawing points them along the
arc from left to right in that order. In T.16 MOTOR TEST, with PinMAME's defender model answering, the
self-test homes to POS 4, MOVE LEFT drives 37 alone to POS 3 and MOVE RIGHT drives 37 with 38 back to
POS 4, and AUTO RUN cycles. That model and the table's `cvpmMech` are synthetic: travel time, speed and
opto spacing are table-owned. A recreation needs: a figure on a path past the four positions, the five
position sensors in that order, 37 = run, 38 = direction right, and a stop at either end.

## Backbox basketball and the shot clock

The backbox holds a small flipper (Backbox Flipper A-21717, solenoid 7, lower right) and a basket at the
far left whose switch is 12. The ROM fires 7 after jet-bumper hit counts, in Hot Dog Mania, Egyptian
Soda and multiballs, and in Pizza Power Shots on the player's SHOOT or flipper presses. T.17 BACKBOX TEST
fires 7 on every SHOOT press (public 11) and marks BACKBOX while 12 is closed. Both are cabinet devices.

The shot clock is a two-digit LED display on the playfield Backboard Assembly A-21393 above the basket:
the 2 LED Driver Board A-21399 (4029B counters, 4511 decoders) counts down on each pulse of 40 and is
blanked or shown by 39. The ROM sets it to 24; PinMAME models the same counter as display 1 (it counted
23, 22, ... in T.16), and the retained table draws it from that display.

## Other mechanisms

- Trough: four balls over the Trough Ball 1-4 optos (32-35); the trough eject coil (9) kicks one past
  the Trough Eject opto (31) to the shooter lane. The Switch Locations list misprints 31 as "TROUGH ELECT".
- Auto plunger (1) and shooter lane (15): no manual plunger; SHOOT (11) launches. Service Bulletin 99
  fixes a ball trap at the plunger-lane entrance to the right ramp.
- Crazy Bob's eject (25, coil 5), the left eject that starts Stadium Goodies.
- Left ramp diverter (3) sends a left-ramp shot to the basket; right loop diverter (4) sends the right
  loop into the jets; loop gate (6) on the left loop sends the ball onto the left loop ramp exit (63)
  instead of into In The Paint.
- Jets: left 61/12, middle 62/13, right 23/14; Jets Ball Drain (56). Slingshots 57/10 and 58/11.

## Lamps, flashers and general illumination

The T.8 test lights lamps 11-88 in matrix order. Lamp 61 lights two bulbs (the RAMPS: 3 POINTS inserts
of the left and center ramps). The In The Paint lamps 67, 68, 77 and 78 are lamp assemblies at the four
saucers (the table draws them as domes). Flashers: 17 eject kickout, 18 left jet, 19 and 20 upper left and
right (each also lights an insert-panel bulb), 22 the trophy insert, 24 two lower flashers in parallel;
21 and 23 are not used. GI strings 1-3 dim (T.6 steps their brightness alone); 4 and 5 are always on, and
string 5 also feeds the coin door.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, checked against the three factory
location drawings (2-41, 2-43, 2-45) with independent callout reads; most switch, lamp and coil
placements are validated, the rest stay observed with a note saying what the drawing showed. The defender
optos, the defender motor, the shot clock lines and the trophy flasher have no table object and are
measured on the drawings. GI strings 4 and 5 have no placement and strings 1-3 rest on the table's own
grouping, which no drawing or count can check, so `spatial_placement` stays missing.

## Author construction checklist

1. WPC-95 controller with a DMD and a two-digit display for the shot clock.
2. Drive every switch active-high; never invert 31-37 or 115 again.
3. Flipper buttons: drive 112/114 (and optionally 116/118 with them); the lower flippers are 45-48.
4. In The Paint: four saucers with pass coils 25, 15/16, 26/27, 28 and shoot coils 33-36.
5. Defender: motor 37/38, position optos 55-51 left to right, stop at both ends.
6. Basket: Basket Made 115, Basket Hold 117, ball catch magnet 8, left ramp diverter 3 to the basket.
7. Backbox: flipper 7 and basket switch 12 (cabinet).
8. Shot clock: count pulses on 40, enable on 39, or read PinMAME's display 1.
9. Treat 41-44 as mirrors of 37-40; 29-31 are PinMAME state channels.

## Sources

- Operations manual May 1997 FINAL and March 1997 edition (IPDB 4023, via the Wayback Machine), Service
  Bulletin 99, the IPDB machine page.
- Pinned PinMAME `97aa922b` (`src/wpc/sims/wpc/full/nbaf.c`, `wpc.c`, `core.c`).
- The retained VPW mod table (v1.3 file) and its script; the ancestral v1.17.0 carries the same bindings.
- Nine LibPinMAME service-test runs of `nbaf_31` (T.1, T.4, T.5, T.6, T.8, T.12, T.16, T.17, and the
  blinked-name capture), plus two earlier runs at the previous pin.

## Procedural note

`tools/curate_nba_fastbreak.py` regenerates the definition, this note and the spatial report
byte-for-byte; `tools/nba_fastbreak_runtime_evidence.py` derives the runtime evidence from the retained
runs.
