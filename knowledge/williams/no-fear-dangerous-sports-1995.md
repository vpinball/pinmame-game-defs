# No Fear: Dangerous Sports (Williams, 1995)

Coverage: **partial - every I/O address, controller binding, polarity and wiring detail is
source-reconciled from the manual, the ROM's own service tests and a retained known-working table;
`variant_differences` is missing because no source says what hardware the 0.8X prototype ROM was built
for, and `spatial_placement` because no placement has been checked against the manual's location drawings**

## Identity and evidence precedence

This is the Williams Electronics Games WPC-Security physical machine of May 1995, model 50025, IPDB 2852,
4,540 units, designed by Steve Ritchie, Greg Freres, Matt Coriale and Dwight Sullivan, with art by Greg Freres,
mechanics by Carl Biagi and software by Matt Coriale. It covers
the nine `nf_*` drivers: `nf_23x` (game ROM 2.3X Export, the parent; the ROM identifies itself as `NO FEAR
PINBALL / 50025 REV. 2.3 X`), `nf_23`, `nf_23f` (French), `nf_22`, `nf_20` and `nf_11x` (all with the S1.1
sound set), `nf_10f` (French 1.0 with the S1.0 sound set), `nf_101` (1.01F, which pinned `nf.c` names the
LED Ghost Fix of the French build) and `nf_08x` (an export prototype). All share one `nfGameData` on
`wpc_mSecurityS`. The prototype stays `unknown` for physical compatibility: nothing retained says what
playfield it ran on.

Evidence precedence: the retained known-working table `No Fear (Williams 1995) VPW v1.1.1.vpx` (VPW, after
Ninuzzu's original; `cGameName = "nf_23x"`, `HandleMechanics = 0`) controls runtime binding and the coils'
causal contract, and its objects give the placements. The IPDB scan of the operations manual 16-50025-101
(April 1995) controls physical construction, part numbers, wiring and device presence. Pinned PinMAME
`46e1a01a` (`src/wpc/sims/wpc/prelim/nf.c`, a preliminary simulator) controls the controller generation and
public addresses. The ROM's own service tests, run on a legal `nf_23x` ROM, settled polarity, names and
every output's identity. Every table used is transcribed under
`evidence/excerpts/williams.no-fear-dangerous-sports.1995/`, and the runs are summarized under
`evidence/runtime/wpc-security/no-fear-nf_23x-*.json`.

The legacy import labelled solenoid 19 `ROM Started`. No WPC generation has a game-on output there: the
ROM's T.5 FLASHER TEST pulses 19 as `FLS. NO FEAR`, an earlier pinned run had already shown the same, and
the definition records it as the No Fear flasher.

## Controller platform and address topology

- WPC-Security (`GEN_WPCSECURITY`, hardware generation `0x20`), 128x32 DMD, DCS sound, Fliptronic II.
- Switches: coin door 1-8, matrix 11-88, Fliptronic 111-118; no custom switch column. The ROM's switch
  test reports nothing in matrix columns 7 and 8 (in T.1 no address there drew an edge), and the manual
  prints them NOT USED.
- PinMAME's inverted switch mask `{0x00,0x00,0x00,0xff,0xe3,...}` inverts public 31-38, 41, 42 and
  46-48. The matrix shades all of columns 3 and 4 as optos; 36 and 43-45 are unused positions inside
  those columns.
- Solenoids: 1-28 on the power driver board (9 and 13 not fitted; 22, 26 and 27 light the insert panel
  only). 29-32 are PinMAME state channels; 31 is the WPC game-on state, as `nf.c` sets no fast-flip
  address. 33/34 are the upper right flipper, 35/36 the unfitted upper left circuit, 37-44 unused on
  this generation, 45-48 the lower flippers and 49/50 reserved. There are no custom outputs.
- Lamps 11-88 (58 not fitted; 86-88 are the BALL LAUNCH, BUY-IN and START button lamps), five G.I.
  strings 0-4.

## Switch polarity: what the ROM's service tests settled

T.1 SWITCH EDGES (a sweep of every matrix and Fliptronic address with mechanisms disabled) names every
switch on its top line while it reads it as active. Every masked opto is named at public 1, so its matrix
contact rests closed (`normally_closed: true`); every other matrix switch is named at public 1 unmasked
and rests open. 24 (Always Closed) rests at 1 and is named on its 1 -> 0 edge. 12, 36, 43, 44, 45, 52,
53, 65 and 68 show `UNUSED`: the ROM scans the positions with no device behind them. Closing 27 and 28
fired the slingshot coils 11 and 10 even inside T.1. 22 (coin door closed) was held open throughout, as
the service buttons require.

The Fliptronic column is read complemented (`WPC_FLIPPERS` returns `~swMatrix`), so public 1 is a pressed
button on every opto position. Each cabinet button carries two optos on one A-17316 board: the right
button F2 (112) and F6 (116), the left button F4 (114) and F8 (118). The ROM fires the lower right
flipper (45, 46) from 112, the lower right and upper right flippers (45, 46, 33, 34) from 116, and the
lower left flipper (47, 48) from either 114 or 118. A recreation writes 112 and 116 from the right
button and 114 and 118 from the left. The manual prints F8 `NOT USED`, but the left opto board's own
pin list wires it and the ROM uses it. The end-of-stroke bits 111, 113 and 115 are synthesized by
PinMAME from the `FLIP_SOL(FLIP_L | FLIP_UR)` flippers; F7 (117) has nothing fitted (J906-5 N/C) and the
ROM ignores it.

## The magnetic ball accelerator (headline mechanism)

Three magnets sit on the Back Panel Assembly A-20033 behind the jump ramp: left (6, Coil
Magnet/Breaker 20-10197), centre (5, 20-10197-1) and right (3, 20-10197-2). Each is mounted on an
Opto Mounting Bracket A-20034 with its own opto ahead of it: left 46, centre 47, right 48. Each magnet
carries a thermal breaker in its bulge that cuts it off when it overheats, and uses a wave spring washer
20-9612.

What the ROM does, from T.16 BALL ACCELERATOR TEST: a 150 ms block of 46 fires 6 once, of 47 fires 5
once, of 48 fires 3 once, each only while that magnet is enabled; a magnet that Enter has disabled fires
nothing for its opto. So each magnet pulls the ball forward the moment the ball reaches its opto, and the
three in turn throw it up the jump ramp. The rules' skill shot and the JUMP THIS and SUPER JACKPOT jump
shots are shots up this ramp. The manual's T.16 page notes that a magnet cannot capture and throw the
ball without a working opto.

The retained table approximates the throw instead of modelling magnetism: while a magnet's output is on,
a ball over its trigger (`LeftMagnet`, `CenterMagnet`, `RightMagnet`) moving right is set to a fixed
speed, and a ball leaving the right trigger is stopped when the centre magnet is on and the right one off.
The ROM decides when each magnet fires; a recreation only needs the opto pulse to reach PinMAME and the
magnet output to accelerate the ball.

## The underground trough, drop target and right popper

The Underside Ball Trough Assy. A-19948 carries a ball from the top of the playfield, behind the drop
target and under the skull, to the lower right popper (manual T.18). It has two entrances, the left one
behind the drop target (38, LEFT ENTR.) and the centre one (37, CTR. ENTR.). The ball passes POPPER 2 (42)
and settles on POPPER 1 (41) in the Ball Popper Assembly A-19965, which carries two LED and
photo-transistor pairs; the RIGHT POPPER coil (1, AE-23-800) kicks it back onto the playfield.

The single drop target (1-Bank Drop Target Assembly A-14615; the playfield list calls the target A-20202)
stands in front of the left entrance at the SKYDIVE shot. DROP TARGET DOWN (8, SM1-26-600) knocks it down
and DROP TARGET UP (12, AE-26-1200) resets it; its switch is 51. Hitting it lights the locks at the SKULL
and SKYDIVE, and three locks start three-ball multiball (rules, PDF page 20).

T.18 UNDERGROUND TROUGH TEST shows the causality. MANUAL pulses 8 as it starts and again when 38 closes,
so a ball can reach the left entrance, and it marks 38, 37, 42 and 41 as they close. AUTOMATIC ejected a
ball from the trough (14), fired the auto plunger (2) while the shooter lane switch (15) was closed, and
fired the popper (1) once 41 was held after 38, 37 and 42. The retained table holds the ball on its
trigger `sw41` and kicks it upward from there.

## The talking skull

The Skull Assembly A-20142 is in two pieces: the face and the Skull Base Assembly A-20144, which carries
the lower jaw. The SKULL MOUTH coil (16, SM-30-1100-DC with a compression spring) opens the jaw. Inside
the skull are two #906 bulbs on the SKULL flasher circuit (21) and the two #44 eye lamps (82, 85). The skull
has no switch of its own. T.19 SKULL TEST pulses 16 with 21 while it plays speech calls, and nothing else.
The retained table rotates its jaw primitives from 16 through an invisible flipper.

## Other mechanisms

- Ball trough: the Outhole Ball Trough Assembly A-19963 (the locations list prints A-19663) holds four
  balls over BALL 1-4 (32-35, position 1 at the eject end); the trough coil (14, AE-26-1500) kicks the
  eject-end ball into the shooter lane, and the JAM BALL opto (31, TROUGH STACK) sees a ball stacked over
  it. In T.18 the ROM held 14 until position 4 (35) opened.
- Auto plunger (2, AE-23-800, Kicker Bracket Assembly A-14525): launches the ball resting on the shooter
  lane switch (15). The cabinet BALL LAUNCH button (11, lamp 86) asks for it; there is no manual plunger.
- Kickback (4, AE-23-800, Bottom Arch Kicker Assembly B-11873): fires a ball on the left kickback lane
  switch (25) back into play when lamp 68 KICKBACK is lit; the two CLIFF targets (LIGHT KICKBACK TOP 57 and
  BOTTOM 56, lamps 71 and 72) relight it.
- Eject hole (15, AE-27-1200, Eject Assembly A-20134): kicks the ball out of the eject hole (61).
- Slingshots: Kicker Arm Assembly A-17811 with AE-26-1200 coils, left 11 and right 10, switches 27 and 28
  (kick and score switches share each address).
- Flippers: lower right A-14876-R-3 (45/46), lower left A-15849-L-2 (47/48), upper right A-19945 (33/34),
  all FL-11629 (blue). The upper left circuit (35/36) is wired on the Fliptronic II board but fitted with
  nothing.
- Buy-in: the BUY EXTRA BALL button (23, lamp 87) buys unlimited extra balls per player as an operator
  option. Pinned `nf.c` names switch 23 `swTicket`; the matrix, the switch list and the ROM's T.1 all
  name it the buy-in button.

## Lamps, flashers and general illumination

The playfield inserts sit on four lamp boards: the 16-Lamp Board A-20043 (11-28), the 12-Lamp PCB A-20041,
the 8-Lamp Board A-20044 and the 3-Lamp Board A-20042. 38, 83 and 84 are B-12224 sign lamps raised above the
playfield; 37 and 48 (RIGHT and LEFT AUTOFIRE) are two bulbs each. The Raceway award ladder runs 13, 12, 11,
22, 23 (5, 10, 15 and 20 million, then LIGHT EXTRA BALL), which is why the labels carry the award values the
ROM prints.

Flashers 17-28 are all ROM-identified by T.5. Three circuits light two places from one driver: 20 RIGHT
RAMP and 23 LEFT RAMP (one #89 on the playfield, two #906 on the insert panel) and 21 SKULL (two #906 in
the skull, one on the insert panel). 22 INSERT EXPLODE, 26 TOP LEFT INSERT and 27 TOP RIGHT INSERT are on
the insert panel only. 24 TOP LEFT is on the back panel. Flasher 19's bulb count is the one printed
disagreement: the Solenoid/Flashlamp Table, its two copies and the wiring drawing print one #906, the
locations list two; the record follows the table.

The G.I. has five strings. 0 PLAYFIELD TOP, 1 PLAYFIELD RIGHT and 2 PLAYFIELD LEFT light the playfield,
and string 1 also feeds #44 bulbs on the insert panel. 3 INSERT TITLE and 4 INSERT BACKGROUND (which also
reaches the coin door through J119) light the insert panel. The ROM's T.6 names and dims each alone in
that order. The retained table switches its `GI_Top`, `GI_Right` and `GI_Left` collections from strings
0-2 and has no active case for 3 or 4.

## Open mechanism behaviour

- The magnets' real dynamics (pull strength, duty, how the breakers trip) are not in any retained source;
  the table's fixed-speed approximation is what a recreation consumes.
- The skull jaw's travel and spring return are not dimensioned; T.19 proves only which outputs fire.
- What the 0.8X prototype ROM expects. Its own test menu, or a description of a prototype playfield, would
  settle whether it matches production hardware.

## Wiring notes

These printed disagreements touch only connectors, pins or table columns; the devices, their public
addresses and their fitment agree, so each record follows the reading named here and notes the other.

- The G.I. block of the Solenoid/Flashlamp Table prints the playfield and backbox columns swapped against
  the Power Driver Board's pin list (J121 to the playfield, J120 to the insert panel), the string names, the
  ROM's T.6 names and the bulb types. The record follows the board list.
- The Lamp Matrix prints the columns on J137; the Power Driver Board's pin list prints J137 Not Used and
  the playfield columns on J138. The record follows the matrix. The matrix also prints Q87 for both rows 4
  and 5 and no Q85; the record keeps the printed designators.
- The Solenoid/Flashlamp Table prints the low-power coils' supply on J107-3, which the board list prints
  N/C (it gives +50V on J107-1 and J107-2). The record follows the table.
- The right flipper circuit page prints the right side's J902 pins as the left side's numbers; the table,
  the Section 3 copy and the circuit diagram agree on the pins recorded.
- The Flipper Opto Board's pin list crosses J905-1 and J905-3 against the Fliptronic II list; the wire
  colours and opto positions agree.

## Spatial status and why the record stays partial

Fitted playfield switches, coils, flashers and lamps are placed from the
retained table's objects (964 x 2162 units). The object for each device is the one the script binds: the
trigger, spinner, target, kicker or slingshot wall for a switch; the light `lNN` that `vpmMapLights
AllLamps` maps for a lamp; the kicker, impulse-plunger trigger, magnet trigger, drop target wall, skull jaw
primitive, flipper or flasher light for an output. One projection is disclosed: the jam opto 31, which the
table does not model, sits on the trough kicker `sw32` at the eject end, where the manual's trough boards
put it.

Switch, coil and insert lamp placements are `observed`: an insert lamp's light sits on its insert, over the
socket. The flasher lights, the raised sign lights 38, 83 and 84, the skull's eye lights 82 and 85 and the
lights of the table's `GI_Top`, `GI_Right` and `GI_Left` collections are invisible light-map sources with no
bulb, set where the table throws the light, so those placements are only candidates; the G.I. lights neither
locate nor count the strings' bulbs. No factory location drawing has been checked against any placement yet;
the manual's lamp (2-35), switch (2-37) and solenoid/flashlamp (2-39) drawings carry numbered callouts that a
callout check could compare. Lamps 37 and 48 have one table light each for two bulbs, and the skull flasher
21 has one light for its two playfield bulbs. `reports/spatial/williams/no-fear-dangerous-sports-1995.md`
lists the open items.

## Author construction checklist

1. Wire every matrix switch as the manual's matrix and the ROM's T.1 names; the masked optos (31-35, 37,
   38, 41, 42, 46-48) are normally closed and active at public 1.
2. Write 112 and 116 from the right flipper button and 114 and 118 from the left.
3. Pulse 46, 47 and 48 as the ball passes each accelerator opto and accelerate the ball while 6, 5 and 3
   are on.
4. Route the underground trough from 38 (behind the drop target) and 37 through 42 to 41, and fire the
   popper (1) from 41.
5. Drop and reset the drop target from 8 and 12, and open the skull jaw from 16.
6. Light flasher circuits 20, 21 and 23 in both places they reach, and drive the insert panel from G.I.
   strings 3 and 4.

## Sources

- Manual `Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf` (IPDB 2852), transcribed under
  `evidence/excerpts/williams.no-fear-dangerous-sports.1995/`.
- Pinned PinMAME `46e1a01a` `src/wpc/sims/wpc/prelim/nf.c`, `src/wpc/wpc.c`, `src/wpc/core.c`.
- ROM service tests T.1, T.4, T.5, T.6, T.8, T.12, T.16, T.18 and T.19 on `nf_23x`, summarized under
  `evidence/runtime/wpc-security/`.
- The retained table `No Fear (Williams 1995) VPW v1.1.1.vpx` (SHA-256 `3523285c...`) and its embedded
  script, with a 1,703-file extraction manifest; the placement seed
  `tools/seeds/williams/no-fear-dangerous-sports-1995-spatial.json`.

## Procedural note

The DMD menus give no text checkpoint, so every run is counted button presses; each reading is the
curator's view of a retained frame pinned by its pixel SHA-256.
