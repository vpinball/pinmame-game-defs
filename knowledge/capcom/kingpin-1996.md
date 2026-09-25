# Kingpin (Capcom 1996)

Coverage: **partial.** The complete controller contract is validated: every public switch, solenoid
and lamp address, its name, its wiring colour code and connector pin, every fitted switch's contact
polarity (ten by ordinary construction) and the DMD. Most playfield devices carry observed
coordinates from one community table. Still open: validated spatial placement, the physical
behaviour of several mechanisms, one conflict about a flasher's position, and the recreation notes
that depend on those.

## Why this record has no manual

Kingpin was to be Capcom's next pinball machine after Big Bang Bar when Capcom closed its pinball
factory in 1996. Krellan's page puts Big Bang Bar at "10-or-so" machines and calls Kingpin "just as
rare, if not more so". No printed factory manual is known: pinned PinMAME's `capcom.c` says it "did
not find a manual for this one", and Krellan says the same. This definition replaces the manual with
the machine's own firmware plus one hands-on survey:

1. **The ROM's service menu.** Walked on fresh isolated state by the LibPinMAME harness
   (`tools/harness-scenarios/capcom/kpb105-*.json`). The Solenoid, Lamp and Switch Tests print each
   device's name, its wire colours and its connector pin. Each harness step pairs that text with the
   public address that changed (solenoids, lamps) or was held (switches). Every row is transcribed in
   `evidence/excerpts/capcom.kingpin.1996/service-*.md` beside a sheet of the frames, and the runs are
   pinned by hash in `evidence/runtime/capcom/kingpin-service-diagnostics.json`.
2. **The ROM's I/O name-record table.** `tools/capcom_kingpin_rom_records.py` decodes the 199 records
   (123 lamps, 46 switches, 30 coils) the menu reads. The lamp and switch conversions reproduce the
   observed public addresses (the switch column pairing follows `capcom.c`'s `io_r`); the coil byte
   order is taken from the Solenoid Test walk. The record's opto flag marks exactly the nine optos.
3. **Pinned PinMAME** for transport: `cc_sw2m`/`cc_m2sw`, the solenoid words and legacy mirrors, the
   two lamp matrices, and the `capInvSw11` opto mask.
4. **Krellan's page** (krellan.com/pinball/kingpin). Its author checked every lamp position on a real
   machine in operator mode. The page also lists switches, solenoids, the slot-machine drum and
   several hardware notes.

The three retained community table scripts are one lineage, all marked "Table not verified yet", and
are used only as leads.

## Controller contract

- **Driver:** `kpb105`, the only Kingpin driver. The operator menu shows "KING PIN" version β1.5
  (Krellan: two known versions, 1.4 beta and 1.5 beta). `kpv106.zip` in the user's ROM library is
  byte-identical.
- **Switches:** cabinet 1-16, playfield 17-80; the ROM's own switch numbers equal PinMAME's public
  addresses. Unused per the ROM: 11, 12, 40, 56, 64-80. Nine optos (17, 36-39, 44, 48, 52, 61) are
  normalized by PinMAME, so do not invert them again. Their supply is connector J15 on the power
  board. Contact polarity: the ROM's Switch Test draws the nine optos as a beam and every other
  switch as a lever contact closed at public 1. Its C5 Troubleshooting report lists a switch it
  checks when the switch sits at a level other than the one it expects at rest: held at 1 from
  power-up it lists 1-4, 9, 10, 14, 19-24, 32, 33, 34, 41, 42, 49, 50, 53-55, 57-60, 62 and 63,
  and it lists 47 (ramp down) only when it is at 0. In a game the ROM resets a drop bank when all
  its targets (25-28 or 29-31) read 1. With PinMAME's opto mask and `capcom.c`'s complemented read,
  that makes all of those normally open, including the end-of-stroke switches 33/34 and slam
  switch 9, which are normally closed on some other platforms, and the masked optos normally
  closed. The ball holders 35, 43 and 51 are read as a ball present at 1. For ten switches, 13, 15
  and 16 (optional dispenser inputs), 18, 45, 46 and the menu inputs 5-8, normally open is ordinary
  construction. 81-88 are PinMAME's synthetic
  flipper column, 89-96 are empty.
- **Wiring:** the colours and pins the service menu prints come from the ROM's fixed colour tables.
  They are the manufacturer's standard harness code for each position, not a trace of a real
  harness, and this machine barely left prototype.
- **Flipper buttons:** the ROM reads them at 5 (left) and 6 (right). Under PinMAME a host must
  press them through the flipper-column button bits, **84** (left) and **82** (right), because
  `core_updateSw` copies those bits into 5/6 every frame. A direct write to 5 or 6 lasts at most one
  frame. The retained table scripts write 5/6 directly.
- **Solenoids:** 32 driver outputs:
  - 1-11, 13-17 and 32 are 50 V coils;
  - 12 is a 12 V motor;
  - 18-31 are 20 V flashers;
  - 9 and 10 are the CPU-driven flippers.

  PinMAME mirrors 9/10/11/12 at 45/47/33/35 for old DOF configurations. On Kingpin the 33 and 35
  mirrors carry the slot eject and slot motor, not flippers. 51 is the Fast Flips game-on state.
- **Lamps:** two 8x8 matrices, 1-64 (A) and 65-128 (B); 123-125 are NOT USED per the ROM. There is no
  GI channel: every light is a matrix lamp. That includes 35 numbered "G.I." positions (G.I. 1-36
  with no 18; the matrix slot between 17 and 19 is the captive standup) and a backbox G.I. The ROM's
  "(2)" marks an output with two bulbs and "RED" a red bulb. Krellan describes many of them as
  "behind above and red": a red light immediately behind the previous one on its own output. He
  notes that this gives the game "the capability to turn almost the entire GI to a red color".
  129/130 are the CPU and sound board diagnostic LEDs.
- **Operator menu:** making switch 8 (PinMAME's "Coin Door", Krellan's "operator's Advance button")
  enters it. The flipper buttons then step and Start selects. The ROM also warns about a 50 V door
  interlock switch ("Check 50V Interlock SW."); nothing ties that switch to a public address. At
  factory settings a credit costs two coins.

## Mechanisms

- **Trough.** Outhole switch 35 and OUTHOLE coil 1 (Krellan: "ball lift"), a four-opto trough
  (36-39), and TROUGH coil 2 serving the shooter lane. Install four balls. The ROM fires 1 when 35
  closes (again about every 1.2 s while it stays closed, once more about 0.7 s after it opens) and
  fires 2 when a game starts.
- **Auto plunger.** Shooter lane 43 and AUTO PLUNGER coil 32; the cabinet launch button is switch 14.
  Outside a game the ROM launches any ball it finds in the shooter lane.
- **Left ramp entrance lift.** RAMP coil 14 raises the entrance to reveal the Hideout, and switch 47
  reads the lowered position. While 47 is open the ROM drives 14 for about 1.3 s, rests about 1.0 s
  and repeats; it stops once 47 closes. Whether the lift latches or needs a held drive is not
  documented.
- **Hideout gun lock.** A three-ball lock under the ramp (44 opto, 45, 46) with GUN EJECT coil 8.
  Krellan: the playfield area near the left orbit is hinged at the rear, so the eject lifts it and
  the ball shoots down at the player from under the floor. The role of GUN TROUGH OPTO 48 is unknown.
- **Slot machine.** One drum, turned by SLOT MOTOR 12 and indexed by SLOT OPTO 52. It shows nine rows
  of three identical symbols; in spin order: Money, Goods, Sevens, Gangsters, Bars, Power, Guns,
  Crazy Cash, Cherries. The motor often stops between rows and the software rounds to the nearest
  row. How the opto is timed per row is not documented. The saucer (51, SLOT EJECT 11) is flanked by
  standups 49/50.
- **Drop targets.** KING bank 25-28 (reset 6) on the left, PIN bank 29-31 (reset 7) on the right. Both
  resets fire at game start.
- **Top diverter.** TOPGATES 13, behind and left of the top lanes, blocks the left orbit. It has no
  position switch.
- **Other devices:**
  - star bumpers: left 17/57, center 15/58, right 16/59;
  - slingshots: 4/41 and 5/42;
  - captive ball: switch 32;
  - spinners: 17 (right ramp) and 61 (left ramp), both optos.
- **Flippers** are CPU-driven, with end-of-stroke switches 33/34 read by the ROM. Their strength is
  software-adjustable. In the timed "power meter" game style they weaken and stop when the meter runs
  out (Krellan).

## Playfield layout

Coordinates come from SG1bsoN's 2021 "1920 Mod" v1.1 of the 2016 table by ICPjuggla, freneticamnesic
and dark (VPUniverse file 7039), whose script runs `kpb105` with the same switch, lamp and coil
bindings as the retained 1.2 script. Each placement is one table object's own centre (for a wall,
the centroid of its outline points), normalized over the table's 952 x 2162 playfield. The table is one unverified lineage, so every placement is
`observed`; Krellan's 41 photographs of a real machine agree with its overall layout but were not
measured.

- **Ramps.** The left ramp starts in the centre by the lock entrance 44 and climbs past its spinner
  61 to the top right, where its exit switch 62 sits; a wireform returns the ball across the
  playfield to the left inlane. The right ramp (spinner 17) climbs to the top left, where its exit
  switch 18 sits, and its wireform crosses the other to the right inlane.
- **Slot machine.** Upper left: saucer 51 and slot eject 11, drum 12/52, the two slot standups 49/50
  with their gun lamps 72/73, and the Hotel Lex flasher 28 above it.
- **Drop banks.** KING (25-28) on the left and PIN (29-31) on the right, in the middle of the
  playfield well above the slingshots, each with its flasher (30, 31) beside it.
- **Projections and clamps.** The trough switches sit on a script ball stack, so they are projected
  onto the trough exit kicker. The three backpanel lamps (116, 119, 120) sit on the back panel and
  are clamped to the rear edge.
- **Not placed:** no source places gun locks 45/46 (Krellan puts gun lock 1 in the hideout; the
  table's lock ends at the gun eject by the left orbit); the ramp-down switch 47, gun trough opto
  48, knocker 3, drop resets 6/7 and ramp lift 14 have no usable table object; flasher 22 has only a
  wide glow light with no flasher dome; 29 is the open conflict.

## Things a table author will trip over

- **Table defects.** The retained script lineage's captive-ball target pulses 49 instead of 32. It
  names its flasher routines misleadingly: the routine on 23 is called RightRampFlash but lights a
  light beside the Hotel Lex building, which fits the ROM's 23 BUILDING FLASHER, and the routine on
  18 drives lights on the left ramp that its comments call right ramp flash. Go by what the routines
  light, not their names. It mirrors the kid flashers: Krellan puts 19 under "Sudden" by the left
  flipper and 24 under "Death" by the right, while the table binds its left-side object to 24. It also presses the
  flipper buttons by writing 5/6, which PinMAME overwrites every frame (use 84/82).
- **Flasher typing.** PinMAME's flasher typing for Kingpin (18-19, 21-31) came from a VPX table. The
  ROM prints 20 (Big Al) as a flasher too; Krellan puts Big Al on the backglass, and the retained
  table does not bind 20. Krellan reports #67 and #906 flasher bulbs rather than #89.
- **Output 20 in the service test.** During the ROM's Solenoid Test, public 20 pulses continuously
  whichever coil is selected.
- **Flasher 29.** The ROM names it "L.ORBIT (EAST)", although EAST is the right-orbit insert
  (`conflict.flasher-29-orbit-side`).

## What is still needed

- **Spatial placement:** an independent source for the observed coordinates (a second, unrelated
  recreation, a measured photograph or a playfield scan), and positions for the devices listed as
  not placed above.
- **Mechanism behaviour:** whether the ramp and top-diverter coils toggle latches or need a held drive,
  what GUN TROUGH OPTO does, and how the slot drum's opto is timed.
- **Flasher 29:** its actual orbit side.
