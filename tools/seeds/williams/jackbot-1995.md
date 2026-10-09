# Jack•Bot (Williams, 1995)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism and
recreation note is source-reconciled; `spatial_placement` is missing because no retained source locates the
general-illumination bulbs except one community table's own grouping, and `variant_differences` because no
source describes the 0.4A sample machine**

## Identity and evidence precedence

This is the Williams Electronics Games physical machine of October 10, 1995, model 50051, IPDB 3619,
2,428 units, four players; the third robot game after Pin•Bot (1986) and The Machine: Bride of Pin•bot
(1991). It covers the five `jb_*` drivers: `jb_10r` (game ROM 1.0R, the parent), `jb_101r` (1.01R, the
"LED Ghost Fix"), `jb_10b` and `jb_101b` (the Belgian/Canadian releases of both) and `jb_04a` (the 0.4A
sample/prototype ROM with its own speech ROM). All five share one `jbGameData` on `wpc_m95DCSS`, so the four
production drivers are `identical`; shared game data proves only the routing, and no source describes the
sample cabinet, so the prototype's physical compatibility stays `unknown`.

Board set. IPDB names the MPU WPC Security and says some production games were built with WPC-95 board
sets; Service Bulletin 86 fixes the WPC-95 CPU board of Jack•Bot and Congo sample games built before
12-15-95. The retained manual is the May 1995 PRELIMINARY edition (16-50051-101) and documents the WPC
Security five-board set: CPU A-17651-50051 (switch columns J207, rows J209, dedicated switches J205), Power
Driver A-12697-3 (coils J130/J127/J126/J122, lamps J137/J134, G.I. J120/J121), Fliptronic II A-15472-1
(J902/J905/J906/J907), Dot Matrix Controller A-14039.1 and a separate DCS sound board. Pinned PinMAME runs
every `jb_*` ROM as its hybrid generation `GEN_WPC95DCS` (0x40, "Hybrid WPC95 driver + DCS sound", like
WHO dunnit), so the definition's `pinmame.wpc-95` platform describes the emulated public API while its
wiring fields cite the manual's WPC Security boards. A WPC-95 board-set game has other connector numbers,
which no retained source documents.

Evidence precedence: the retained known-working table script (bord's Jack·Bot, VPU 7953, version 1.1.2a;
the pinned script corpora carry the same bindings) is runtime and mechanism-causality ground truth; the
May 1995 manual controls physical construction, part numbers, wiring and device presence; pinned PinMAME
`97aa922b` controls the controller generation and public addresses (its `jb.c` is a preliminary simulator
whose switch and solenoid symbols are not this machine's wiring); the ROM's own service tests, run on a
legal `jb_10r` ROM, settled polarity, names and every output's identity; the retained table supplies
coordinates and the factory location drawings check them. Every table used is transcribed under
`evidence/excerpts/williams.jackbot.1995/`, and the runs are summarized under
`evidence/runtime/wpc-95/jackbot-jb_10r-*.json`.

## Controller platform and address topology

- Switches: dedicated 1-8 (coin chutes and the coin-door service buttons), matrix 11-68 (columns 7 and 8
  are NOT USED), Fliptronic 111-118. DIP 1-8 are the country bits.
- Fliptronic column: 111 and 113 are the lower end-of-stroke switches, which PinMAME synthesizes from the
  flipper coils (`FLIP_SOL(FLIP_L)`). 112/116 are the two optos of the right cabinet button and 114/118 of
  the left one; the ROM fires the lower flipper from either opto of a button. 115 (F5) and 117 (F7) are the
  upper-flipper end-of-stroke inputs reused as the visor closed and open switches; PinMAME does not
  synthesize them.
- Solenoids: 1-28 as printed (2 NOT USED), the lower flippers at 45-48 (printed circuits 29-32), the
  unfitted upper-flipper circuits 33-36, the unused positions 37-40 and PinMAME's LPDC mirrors 41-44,
  PinMAME state channels 29-31 and constant 32, PinMAME's simulator ball-shooter channel 49 (used only while
  PinMAME's own simulator runs) and reserved 50.
- Lamps 11-88 (87 Buy-In button, 88 Start button), five dimmable G.I. strings at public GI 0-4, one
  128x32 DMD.

## Switch polarity: what the ROM's service tests settled

The T.1 SWITCH EDGES sweep held every public address at 1 and back at 0. Every fitted switch is named at
public 1, including the eight addresses PinMAME's mask inverts (the drop-target optos 16-18 and the trough
optos 31-35), so those rest closed (`normally_closed` true) and everything else rests open. The manual
shades 16-18 and 41-45 as optos and leaves the trough cells unshaded; the trough pages and the mask make
31-35 optos, while the visor targets 41-45 carry leaf-switch part numbers and read active at public 1
unmasked, so they rest open whatever their construction. T.17 VISOR TEST confirms the visor switches: it
stops the motor on 117 when opening and on 115 when closing, each at public 1. T.16 RAMP TEST shows RAMP
DOWN SW. while 15 is 1. Always Closed (24) is named on its 1 -> 0 edge. Drive every switch active-high;
never invert the masked optos again.

## The visor (headline mechanism)

Pinbot's visor covers his eyes, the two eye locks (left 47, right 48). Its five targets (41-45, left to
right) face the playfield. One motor (14-8023, solenoid 28) turns in one direction through the Motor EMI
w/Brake board A-15340 and moves the visor through a cam (04-10080) and its lever arm and link from one end to
the other; the micro-switches
Visor Closed (115) and Visor Open (117) on the motor bracket A-20100 report the ends. The ROM runs the
motor until the wanted end switch closes and ignores the other one. Rules: hits on the visor targets and on
the 5-bank standups (51-55) light the 25 chest lamps (five colour columns, rows 1 HIGH to 5 LOW, lamps
12-16, 22-26, 32-36, 42-46, 52-56, with the coloured arrows 11-51 above); completing the chest opens the
visor and reveals the eye locks, whose balls start multiball; after 15 Jack•Bots Mega Visor raises it
again. The right and left visor flashers (15, 16) carry two bulbs each; the center visor flasher is 17.
The retained table models the visor as a 58-step reversing linear mech on solenoid 28 with 115 at the
closed end and 117 at the open end; that model is synthetic, and no source gives the travel time.

## The lifting ramp and the mini-playfield

The left ramp lifts. Ramp Lifting Mechanism B-11304: lift coil AE-26-1200 (solenoid 6, RAISE RAMP), a
smaller coil SM1-26-600 (solenoid 14, DROP RAMP) and the micro-switch 15 (RAMP IS DOWN, made while the ramp
is down). Down, the ramp is a shot past the ramp entrance (37) to the mini-playfield and out past the ramp
exit (36); raised, it opens the way to the Cashier target under it (38). T.16 RAMP TEST cycles RAMP UP (6)
and RAMP DOWN (14). Shooting the ramp lights the Game Saucer and starts the Vortex Millions count; the
mini-playfield exit awards rotate among Cashier, Mega Ramp, Light Extra Ball and Jack•Bot (lamps 71-74);
lamps 75 and 76 light the Game Saucer and Mega Ramp sign over the ramp entrance.

## Other mechanisms

- Game Saucer: the eject hole at the far upper left (46, coil 3, which the ROM names GAME SAUCER); the jet
  bumpers and the left flipper button move the flashing game among Pinbot Poker, Slot Machine, Roll The
  Dice and Keno (81-84), and after those Casino Run (66).
- 3-bank drop targets 16-18 (optos on board A-13609) with one reset coil (4); a moving target lamp (77, 78,
  68) advances the bonus multiplier and completing the bank awards a card (61-65).
- Vortex skill shot: three holes 56-58 at the top right; the center scores three times the Vortex value.
- Trough: four balls on optos 32-35 (32 at the right), jam opto 31, ball release coil 1, shooter lane 68;
  the plunger is manual.
- Jet bumpers: upper 61/13, left 62/12, lower 63/11; slingshots: left 65/9, right 64/10; the 10-point
  rubber switches 11, 12 and 66; the Hit Me target 67; the target under the ramp 38.
- Knocker (7) in the backbox; Buy Extra Ball button 23 with lamp 87.

## Lamps, flashers and general illumination

The ROM's T.8 names every lamp. The preliminary manual's lamp matrix and lamp list print 28 BONUS 3X, 38
BONUS 4X and 47 BONUS 5X; the ROM names them 4X, 5X and 3X, the retained table's lights sit on the 4X, 5X
and 3X inserts of its playfield art (2X upper left, 3X upper right, 4X lower left, 5X lower right around
Shoot Again), and the manual's own lamp drawing puts 28 at the lower-left and 47 at the upper-right insert;
the definition follows them. The lamp list also swaps 71, 73 and 74 against the matrix and the ROM. The
flashers are 15-27: visor 15-17, Pinbot face 18, jet bumpers 19, lower left 20, middle left 21, lower right
22 and five back-panel domes 23-27. G.I.: PLAYFIELD LOWER, LEFT, UPPER and RIGHT (#44) and INSERT (#555,
the backbox insert panel, with a coin-door branch); all five dim in T.6.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, checked against the three factory
location drawings (2-35, 2-37, 2-39) with independent callout reads; most switch, lamp and coil placements
are validated, the rest stay observed with a note saying what the drawing showed. The rubber switches 11,
12 and 66, the ramp switch 15, the visor switches 115 and 117, the ramp coils 6 and 14, the visor motor 28
and the visor flashers 15-17 have no usable table object and are measured on the drawings. The four
playfield G.I. strings rest on the table's own grouping, which no drawing or count can check, so
`spatial_placement` stays missing. PinMAME's simulator channel 49 (the manual-shooter release pulse) is a
virtual output with no placement.

## Author construction checklist

1. WPC-95 controller with a 128x32 DMD.
2. Drive every switch active-high; never invert 16-18 or 31-35 again.
3. Flipper buttons: drive 112/114 (and optionally 116/118 with them); the lower flippers are 45-48. There
   are no upper flippers.
4. Visor: one motor output 28; close 115 at the closed end and 117 at the open end; eye locks 47/48 with
   coils 8/5 behind it; targets 41-45 on it.
5. Ramp: 6 raises, 14 drops, 15 is made while the ramp is down.
6. Drop targets 16-18 with reset 4; Game Saucer 46/3.
7. Treat 41-44 as mirrors; 29-31 are PinMAME state channels; 33-40 are unfitted.

## Sources

- Operations manual May 1995 PRELIMINARY, Service Bulletin 86 and the IPDB machine page (IPDB 3619, via the
  Wayback Machine).
- Pinned PinMAME `97aa922b` (`src/wpc/sims/wpc/prelim/jb.c`, `wpc.c`, `core.c`).
- The retained table (bord, VPU 7953, version 1.1.2a) and its script.
- Eight LibPinMAME service-test runs of `jb_10r` (T.1, T.4, T.5, T.6, T.8, T.12, T.16, T.17).

## Procedural note

`tools/curate_jackbot.py` regenerates the definition, this note and the spatial report byte-for-byte;
`tools/jackbot_runtime_evidence.py` derives the runtime evidence from the retained runs.
