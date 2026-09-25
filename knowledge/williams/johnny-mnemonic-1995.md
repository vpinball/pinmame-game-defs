# Johnny Mnemonic (Williams 1995)

Coverage: **partial**. Every address is enumerated and named, and construction, polarity, mechanism
and variant facts are validated from the factory operations manual, its service bulletins, pinned
PinMAME and the retained known-working table, and no conflict is open. It stays partial on spatial
placement alone: the retained table has no flasher sockets, so seven flashers and the Clear Matrix
coil are measured on the manual's location drawing and stay observed; G.I. string 4 has no
coordinate at all; and the playfield G.I. sockets come only from the table's G.I. collections.

## Identity and drivers

- Williams Electronics Games, model 50042, date of manufacture August 8, 1995, 2,756 units (IPDB 3683,
  OPDB `GR6W8-Mb55B`). Designed by George Gomez.
- WPC-Security (WPC-S) hardware with a DCS sound board and a 128x32 DMD.
- PinMAME drivers: `jm_12r` (1.2R, parent), `jm_12b` (1.2 Belgian) and `jm_05r` (0.5R prototype). All
  three are declared in `src/wpc/sims/wpc/prelim/jm.c` with the `wpc_mSecurityS` machine driver and
  share one `jmGameData`, so the controller contract is identical. The prototype's physical build is
  undocumented, so it is recorded as compatible rather than identical.
- Manual Addendum 1 (October 13, 1995) covers the first 100 sample games: game code 1.0 or 1.1 must be
  paired with sound code 1.0, the back-panel flash lamp terminals need insulating, and the magnet needs
  a retaining wire clip.

## Evidence used

- The September 1995 operations manual (IPDB's "English Manual", 142 pages, image-only 300 dpi scan),
  retrieved from the Internet Archive's capture of the IPDB file because IPDB is Cloudflare-gated. A
  local Windows OCR text layer helped find pages; every cited cell was read from the render. Printed
  page 2-N is PDF page N + 68, 1-N is N + 20 and 3-N is N + 108.
- The manual's power driver board connector list (printed 3-29 to 3-31) and flashlamp wiring page
  (printed 3-7), which settle where each flasher and G.I. string goes.
- Service Bulletins SB 85 (Data Glove troubleshooting) and SB 87 (hand magnet fuse), and Manual
  Addenda 1 and 2, all text PDFs from the same IPDB page.
- Pinned PinMAME `jm.c`, `wpc.c` and `core.c`.
- The retained known-working VPW Johnny Mnemonic v1.2.2 table and its script, and, as corroboration
  from the same lineage, the corpus script `Johnny_Mnemonic_1.3.vbs`.

## Controller facts a recreation needs

- Switch matrix 11-78, sequential WPC column-times-ten addressing; column 8 (81-88) is not used.
  Dedicated coin-door inputs D1-D8 are public 1-8.
- Optos: the trough (31-35), the popper (36) and the four hand encoders (74-77). `jmGameData`'s
  inverted-switch mask normalizes exactly these ten, so every public switch is already normalized;
  do not invert again.
- Fliptronic column: 111/113 are the lower flipper end-of-stroke leaves, which PinMAME recomputes
  from the flipper coils every update (do not drive them); 112/114 are the cabinet flipper optos;
  115 is **Ball In Hand**, a leaf in the magnet can, which PinMAME never overwrites. 116-118 are not
  fitted.
- The cabinet hand-control buttons are matrix switches **67 (right)** and **68 (left)**. With
  LibPinMAME's default of mechanics handling off, the host drives 67/68 directly. With mechanics
  handling on, `jm_handleMech` copies 116 into 67 and 118 into 68 on every update, so the host must
  then press 116/118 instead.
- Solenoids 1-28 on the power driver board. 4 and 8 are not used. 21-24 are not lamps but the four
  control lines into the A-20532 Dual Relay Motor Driver board. 33-36 are the Fliptronic upper
  circuits carrying the two diverters, published raw because `FLIP_SOL` covers only the lower
  flippers. The lower flippers are 45-48 (odd power, even power-or-hold).
- 29-31 carry WPC state (31 is game-on, since `jm.c` sets no fast-flip address); 32, 37-44, 49 and 50
  are dead or reserved.
- 64 lamp positions, all fitted except 37. Lamps 86-88 are the cabinet Ball Launch, Buy-In and Start
  buttons. The lamp matrix page prints the rows on J133 and the columns on J137; the connector list
  puts them on J134/J138 (playfield) and J135/J136 (cabinet rows 6-8 and column 8).
- Five G.I. strings: 1-3 feed #44 playfield and #555 backbox bulbs, 4 is playfield only, and 5 is
  backbox and cabinet. Each string's triac switches its return pin (Brown, Orange, Yellow, Green,
  Violet); the White-colour pins are the 6.8Vac feeds. The connector list agrees (J121 to the playfield, J120 to the insert panel),
  except that it prints string 4's J121-5 return 'G.I. to insert panel'; every other J121 pin runs to
  the playfield, so that is read as a misprint.
- The country DIP chart on the quick-reference sheet sets SW1/SW2 Off and SW3/SW4 On for every
  country; America is all On from SW3 to SW8.

## Mechanisms

### Trough and launch

Four balls sit on trough optos 32 (at the shooter end) to 35; Trough Jam (31) is a fifth opto past
ball 1. Solenoid 1 kicks ball 1 into the shooter lane (78), and solenoid 2, the autoplunger, fires
when the player presses Ball Launch (11) or automatically: the rules call it the AUTOFIRE and use it
for the Mnemonic Recovery "virtual kickback" and to relaunch every ball in Powerdown Multiball. The
retained script pulses 31 on every eject; treat that as a table stand-in, not a jam.

### Data Glove

The A-20500 Hand Assembly sits at the rear left in front of a screened back panel: a molded left
hand on a magnet carriage, moved left and right by an X screw and in and out by a Y screw. Each screw
has a 14-8025 DC gear motor, a home micro switch (12 for X, 37 for Y) and an A-20533 position encoder
board whose two slotted optos read an opto wheel as a quadrature pair (74/75 for X, 76/77 for Y; the
matrix prints the Y pair as 76 "B" then 77 "A").

The A-20532 board takes each axis's enable (22 X, 24 Y) on a TIP102 Darlington and its direction (21
X, 23 Y) on a 12 V DPDT relay that reverses the motor. PinMAME reads these four lines straight from
the raw WPC_SOLENOID3 register because its smoothed solenoid state is too slow for the motor.

Per Service Bulletin SB 85, the popper (3) is designed to shoot the ball straight up to the hand, and
the magnet (solenoid 6) is turned on at full power to catch it; once the ball's weight closes Ball In
Hand (115), the ROM duty-cycles the magnet so it does not overheat or magnetize the ball. SB 85's
troubleshooting asks the technician to verify that the magnet sits approximately over the popper. The ROM then
carries the ball over the Cyberspace Matrix, drops it into a hole, and can pick a ball back up. The
player steers with the hand-control buttons; Video Mode also uses all four cabinet buttons.

Travel limits, speeds and encoder pitch are not printed and are table-owned. Pinned PinMAME's model
(mechanics bits 0 and 1) steps a counter per axis while its enable is on, closes home below position
1, derives the quadrature pair from the two low bits and starts both axes at home. The retained table
leaves PinMAME's mechanics off and runs its own two `cvpmMech` objects instead.

### Cyberspace Matrix

The A-20447 Cyber Space Assembly at the upper right has nine holes, each over a red rollover button on
a spring and a switch: 51/52/53 across the rear row, 61/62/63 across the middle and 71/72/73 across
the front. The switch labels read column then row ("Cyber Matrix 21" is switch 52, rear centre). The
lamp matrix numbers the nine lamps in the opposite order (lamp 51 is "Cyber Matrix 13", under switch
71), so pair lamps to holes by label, not by number.

Per the rules, three locked balls start Cyberspace Multiball and the placement of the locked balls
determines its jackpot shots. Solenoid 5, Clear Matrix, drives a plunger, link and pivot arm on the
assembly's base, which rides two nylined bearings; the location drawing puts the coil at the matrix's
right rear corner. The retained script models the stroke as kicking every held ball out.

### Diverters

Two A-20497 diverters run on the Fliptronic upper flipper circuits: the Left Diverter on the
upper-right circuit (33 power, 34 hold) and the Right Diverter on the upper-left circuit (35/36). Each
is an FL-11753 coil turning a drive arm on the blade shaft, sprung back when off, and has no position
switch. The rules say the left standup target opens "the diverter which channels SPINNER and RIGHT
LOOP shots into the JET BUMPERS". The retained script binds only the hold windings; its left diverter
sits at the top of the left orbit and its right diverter at the rear, just right of the popper.

### Crazy Bob's, drop target, jets, slingshots and flippers

- Crazy Bob's (47) is an eject hole with an AE-26-1500 coil (14) that the table models as a vertical
  up-kicker.
- The single controlled drop target (43) beside the popper is raised by 15 and knocked down by 16.
- The three jets (44 left, 45 bottom, 46 right) sit below the three jet lanes (64-66); the flipper
  buttons lane-change those lamps.
- The slingshots each carry a kick and a score switch on one address and a #906 flasher.
- Two Fliptronic flippers with blue FL-11629 coils.

## Manual discrepancies worth knowing

- The switch matrix's row-6 header prints `U209-7`; every other row prints `J209-n`.
- Switch 36's parts entry prints A-16909 for both LED and transistor; the popper assembly gives
  A-16908 (LED) and A-16909 (phototransistor).
- The matrix labels F6-F8 with the generic upper-flipper names; the switch-locations list prints them
  Not Used.
- Lamp 87's assembly is printed `20-663-21`, the switch list prints `20-9663-21`.
- Pinned `wpc.c` types flashers 17-20 and 25-28 as #89 bulbs for its brightness model; the manual
  prints #89 only for 17 and 27 and #906 for the rest.
- Flashers 18, 20, 25 and 28 also light a backbox insert-panel bulb (the list prints "Inset Panel"
  once). The connector list calls 28's backbox drive (J124-5) 'solenoid 28 drive to back panel
  flasher'; the solenoid table, the locations list, the flashlamp wiring page and the J106-5 'insert
  panel flashers' supply all put that bulb in the backbox, so the wording is read as the device's
  name. The playfield bulb of 28 is on the back panel of the hand assembly.
- The connector list prints J125-5 as 'solenoid 21' (it is solenoid 20's Black-Yellow backbox
  drive), and the flashlamp wiring page prints that wire BLK-ORG.
- The solenoid table repeats the header 'Voltage Connections' over its drive-connection columns.

## What would complete the record

A socket-level survey of a real machine (or a table that models the flasher and G.I. sockets) giving
positions for flashers 17-20 and 25-28, the Clear Matrix coil and every playfield G.I. bulb by
string, including string 4 (the table's string-4 lightmap covers the upper-left playfield, a region
lead only). The location drawing shows an unlabelled dome at the far left beside the
jets; the record places the Left Ramp Flasher (25) there because the 2020 archive table (Alessio) drives its
solenoid-25 glow at the same spot, but no source confirms it.
