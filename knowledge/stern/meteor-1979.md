# Meteor (Stern, 1979)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; no playfield lamp is placed, and which switch is each three-bank's middle target is unresolved**

## Identity and evidence precedence

This is the one physical Stern Meteor (IPDB 1580, September 1979, model 113, Stern M-200 MPU, 7,939 units; design Steve Kirk, art Leslie Kaip and Jorge Obregon, software Alan McNeil). Every PinMAME
Meteor driver runs on this machine, so one record carries all fifteen:

- `meteor` is the production ROM set and `meteora` Stern's factory fix of its U1 (`cpu_u1a.716`), which PinMAME declares as a second root rather than as a clone. `meteorbf` is an earlier,
  different bonus-count fix, `meteorfp` the free-play set, `meteora2` a community build with a sound-register fix and `meteorns` a community patch that removes the background sound.
- `meteore`, `meteorf` and `meteorg` are Idleman's free-play rules modifications (revisions 64-66, 2019-2021).
- `meteorb` (2003) is Oliver's seven-digit conversion, `meteorc` its free-play build and `meteord` (2005) a /10 scoring build on the same layout; `meteore7`, `meteorf7` and `meteorg7` are seven-digit
  builds of Idleman's modification (revisions 74-76). These six use PinMAME's `dispst7` layout (player displays at segment starts 1, 9, 17 and 25, width 7), recorded as display overrides; the
  conversion needs seven-digit player displays and changes nothing else.

All fifteen share the rest of the game data (`GEN_STMPU200`, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound). The authorized ROM library holds `meteor`, `meteora`, `meteorb`, `meteorbf`,
`meteorc`, `meteord` and `meteorfp`; each of the six besides `meteor` was run once. Before the drain each fired the same set of solenoids as `meteor` for the same steps (the thumper,
both slingshots, the stand-up target, the right three-bank and both flipper buttons; firing order, timing and lamps were not compared), except that in `meteorc` and `meteord`
(knock-down 8) and `meteorfp` (knock-down 14) the stand-up target spotted a different METEOR target from the one `meteor` spotted (knock-down 12). Across the drain and the next
serve taken together each fired the outhole kick (15) and the bank resets (3, 7, 9, 13), though not in the same windows: `meteor`'s run fired them before the served ball left the
outhole and only target restores after it, while each variant fired them again after it. No variant fired a knock-down coil there: no METEOR target switch closed in those runs,
while `meteor`'s run restored the four it had down.

Evidence order is the runbook's. The two pinned corpus scripts (whose `cGameName` is `meteorb`) give runtime bindings, this game's own 40-page manual and its self-test card give construction and
wiring, pinned PinMAME gives the controller topology, and eleven retained harness runs (burn-in, solenoid test, switch test, a coin and bookkeeping run, a scripted game and one run of each other
driver held) pair the printed numbers with public addresses and show the ROM's responses. The manual is a 300 dpi one-bit scan whose last pages are the schematic sheets lettered for METEOR.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the self-test
card's switch numbers are the public addresses. Positions 17, 18, 25 and 26 are not used (card `Open`, playfield sheet `N/U`). The cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilts) and 8 (slam)
are strobed on R-Y (A4J3-2) and return on MPU connector A4J3; the playfield sheet repeats 6, 7 and 8 and draws 1-3 as unlabelled contacts. Every matrix contact is normally open. The coin chutes, by
the bookkeeping counts of the retained coin run: public 1 is the hinge-side chute (credit table switches 28-30), 2 the center chute (switches 1-5) and 3 the right chute (switches 9-13); the cabinet
sheet's `CHUTE #3/#2/#1` labels run the other way. Service inputs are -7 (Self Test, inside the coin door), -6 and -5. Public -6 is S33, the pushbutton on the MPU assembly: the MPU schematic
wires it to the 6800's NMI input, the line PinMAME drives from -6; the manual names it only for zeroing a high score level while adjusting it. Public -5 is a virtual input: PinMAME passes it to the ST300 sound
board's diagnostic callback, which holds it as the voice-select state, and no fitted contact is established for it, so a recreation leaves it open. IPDB's schematic errata report a remote memory-clear switch wired to A4J3-5, which the interboard wiring diagram prints `N.U`, so no
remote contact is recorded. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' winding-shunt end-of-stroke contacts (physical direct inputs 1
and 2) and the upper right flipper's series `E.O.S.` contact (6) have only profile-local identities.

**Solenoids.** The self-test card's solenoid numbers are the SDU driver transistor numbers, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires,
pairing them as `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over four identical cycles. In public terms: 1 left
slingshot, 2 thumper bumper, 3 top left three-bank reset, 4 METEOR M knock-down, 5 first E knock-down, 6 knocker, 7 lower left three-bank reset, 8 T knock-down, 9 right three-bank reset, 10 right
slingshot, 11 second E knock-down, 12 O knock-down, 13 METEOR bank reset, 14 R knock-down, 15 outhole kicker, 18 coin lockout, 19 flipper enable relay. Public 16 is the decoder's unaddressable slot.
Public 17 (Q17) and 20 (Q18) are continuous drivers wired only to pins marked `N/U`, with no load in the card or the parts list: in the retained runs the ROM drives them only in the power-up initialisation
pulse it gives all four continuous lines (at power-up and after a slam) and in its own tests, so they are unused.

**Continuous outputs.** Public 18 (Q19) and 19 (Q15) are held. The coin lockout is energized from about 2.5 s after the power-up pulse and drops when the credits reach the maximum (5 at the default
option switches, in the retained coin run). The flipper relay is held on while a game is played and drops on a tilt and at game over; outside play the retained runs
show it raised only in the power-up initialisation pulse the ROM gives all four continuous lines (at power-up and after a slam) and in the ROM's burn-in and solenoid
tests, and off in steady attract mode.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this
game's lettered copy of sheet 12B-431S-113 was read for all sixty lines. The game's lamp assignment is the lamp list on the playfield sheet (a copy on the lamp driver sheet adds a handwritten Tilt row),
which names a load, wire, jack and pin for every output; its pins were checked against the lamp driver sheet's connector blocks, and every disagreement is stated on the lamp. The ROM proves the
METEOR drop lamps (M 58, first E 42, T 26, second E 10, O 57, R 41), the spot lamps 5 (stand-up target), 25 (upper rollover) and 9 (lower rollover), which went out as their switch spotted a
target, and the backbox TILT lamp (61); the lamp list and the scripts pair the same lamps with the middle rollover (5), the left return lane (25) and the right return lane (9), which the run exercised
with those lamps already out; GAME OVER (45), MATCH (63) and HIGH SCORE TO DATE (13) are the other backbox lamps. The bank WOW lamps 30, 46 and 62 and the stand-up WOW 14 changed state
only in the service runs; they are printed loads and stay used.

**General illumination** is uncontrolled: the playfield string from A2J1-8 (printed 6 VAC there, off the transformer's 7.3 VAC winding), the cabinet bus and the backbox buses, with no relay or driver in
any line.

## Ball lifecycle

The single ball rests on the outhole switch (33) under the apron in front of the outhole kicker (15). When a game starts the ROM raises the flipper relay (19) and fires the outhole kicker followed
by the four bank resets in sequence (15, then 3, 7, 9 and 13, about 0.6 s from the kick to the last reset) and repeats that sequence about every 1.7 s while 33 stays closed (retained runs); a real
ball leaves 33 on the first kick and rolls into the shooter lane. After a drain while play continues the bonus times the
multiplier is added (a tilted ball forfeits it, manual), the ball or player advances, the ROM restores the METEOR targets that player had made with their knock-down coils (the bank's memory, manual) and serves again; an extra ball is
played without advancing. A tilt drops the flipper relay and lights TILT (61); in the retained run a right slingshot hit while tilted fired nothing, and on the next ball the left
slingshot and the left flipper button both worked. A slam ends the
game, and the ROM repeats its power-up initialisation. After the last ball's drain the retained trace records no outhole kicker pulse in the 30 s the host then holds 33 closed before
crediting the next game, so the ball stays in the outhole; the ROM drops the flipper relay and lights GAME OVER (45) and MATCH (63). In the
retained run the final score 539,740 matched the match number 40, and the ROM fired the knocker (6) once as the credits went from 02 to 03; the match is played only with option switch 21 ON
(PinMAME's default).

## Mechanisms

- **METEOR bank**: six drop targets (32 M, 31 E, 30 T, 29 E, 28 O, 27 R from left to right) on one reset coil (13) with a knock-down coil each (M 4, first E 5, T 8, second E 11, O 12, R 14). The ROM
  spots targets with the knock-down coils and, after a drain that continues play, restores the targets the next ball's player had made (the bank's memory: the manual's rule, which IPDB
  notes is the only drop-target memory on the game). The retained single-player run restores T, second E, O and R after each of its first two drains (the second one tilted) and fires
  no restore after the last ball.
- **Three-banks**: right (9-11, reset 9), top left (19-21, reset 3) and lower left (22-24, reset 7), no knock-downs. Each controls one missile row: right bank the right row (rocket 3), top left the
  middle row (rocket 2), lower left the left row (rocket 1); each hit advances one lamp of its row.
- **Thumper bumper** (14 fires 2), **slingshots** (16 fires 1, 15 fires 10), two passive **scoring bumpers** (12, 13), the **spinner** (5), the center **stationary target** (4) and a passive ball gate.
- **Flippers**: three dual-winding coils on two buttons, gated by the flipper enable relay; the upper right flipper hangs off the right flipper's drive through a separate series contact labelled
  `E.O.S.`, drawn open, so it is energized only while that contact is closed. The sheet does not say which assembly carries it; PinMAME and the scripts move both right flippers together. PinMAME
  publishes 46 (right) and 48 (left) with 45 and 47 alongside.

## Rules summary

From the manual's feature pages: the METEOR end targets score 6,000 and the middle ones 2,000, and each down target adds 600 (end) or 200 (middle) to every spinner spin. Completing the bank advances the
bonus multiplier 1X-7X (carried over up to 6X; after 7X it resets to 3X for the next ball); from the 5th or 6th reset (option switches 23-24) a lamp steps across the bank for an extra ball. Lit star
rollovers (2,000 or 6,000), lit return lanes and the lit stationary target spot a METEOR target. Each three-bank hit advances its missile row and scores the value; three equal missile values light a
rotating WOW (extra ball), and a bank's special is awarded on its center target. The scoring bumpers score 500 or the missile value and advance missile rows 1 and 3 when lit; the outlanes score 3,000
plus 1,000 per missile lamp when lit; the thumper scores 1,000 (three-ball) or 100 (five-ball); the slingshots score 10 and move the lit features unless option switch 25 is ON.

## Option switches

The thirty-two MPU option switches (Figure 1 `DETAIL S1-S32 MPU ASS'Y.`) are assigned by the `METEOR SWITCH ASSIGNMENT` list on PDF page 10 and the charts on pages 11-15: S1-5 center chute, S9-13
right chute and S28-30 hinge-side chute credits, S6 high score award, S7 balls per game, S8 missile WOWs, S14/S31/S32 special award, S15-16 high game to date, S17-19 maximum credits, S20 credit display,
S21 match, S22 replays per ball, S23-24 METEOR bank WOW at 6X or 7X, S25 slingshot movement, S26 spot METEOR lamps per multiplier and S27 spot METEOR lanes. Pinned PinMAME boots with S20 and S21
ON and the rest OFF (by35.h BY35_COMPORTS), which gives the three-ball games, the 3/2 center-chute pricing, the 5-credit maximum, the credit display and the match of the retained runs. The page-10 list numbers the chutes `Coin Chute #1 Germany or #2 All Others` for 28-30 and
`No. 2 Germany or No. 1 All Others` for 1-5, while the credit chart calls 28-30 the chute `next to hinge` and 1-5 the center chute; the bookkeeping counts above settle which public input each counts.

## Displays and sound

Four six-digit player displays (indices 0-3, segment starts 2, 10, 18 and 26), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME
`dispst6`. The six seven-digit drivers move the player displays to starts 1, 9, 17 and 25, width 7. Sound is the Stern SB-300 sound module (parts list `Sound Module C-605`; PinMAME `SNDBRD_ST300`);
sound commands add no playfield devices.

## Disagreements between this game's own documents

- **Three-bank middle and lower targets (unresolved).** The playfield sheet prints each bank's cells top, lower, middle in matrix order (9, 10, 11; 19, 20, 21; 22, 23, 24); both known-working scripts
  bind the middle object to 10, 20 and 23. The special a bank awards on its center target depends on it. A harness run with a special award set by option switches 14, 31 and 32 would settle it, but
  `tools/run_pinmame_harness.py` cannot set option switches yet; an owner pressing each middle target in the switch test would also settle it.
- The SDU sheet and the playfield coil sheet swap the flipper return pins (J1-8 and J1-9) while agreeing on the colours; the thumper's `A3J2-4` on the coil sheet repeats the left slingshot's pin where
  its colour is the SDU's J2-9; the first E knock-down is Y-B on the SDU sheet and Y-W on the coil sheet; the right slingshot's colour is struck through on the SDU sheet. Wiring-detail readings only;
  the SDU sheet is followed except where its own entry is struck out.
- The lamp list and the lamp driver connector blocks disagree on several pins, and the list prints the lower left bank WOW twice and `2X` on another row's pin; each case is stated on its lamp.
- The playfield sheet draws credit (6) and coin chute 1 without a diode where the cabinet sheet draws one; the cabinet sheet's chute numbers run opposite to the credit table's.
- The playfield sheet prints the playfield G.I. string as 6 VAC; the transformer sheet's G.I. winding is 7.3 VAC.

## Recreation checklist

- Build the full inventory: 36 used matrix switches and four unused positions, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 (17 and 20
  unused) with the two flipper callbacks, the sixty SCR lamp addresses and the six displays (with the seven-digit overrides for the drivers that need them).
- Start with the ball on the outhole (33 closed), every drop target up and the flipper relay off in steady attract mode, after the power-up
  initialisation pulse, until a game starts.
- Make each knock-down coil put its METEOR target down so that its switch closes; the ROM spots targets and restores each player's made targets after a drain with them.
- Bind the right flipper callback to both right flippers.
- Treat the manual's feature pages and the ROM as the rules authority; the community ROMs change rules or scoring, not hardware.
- Placements: switches, coils and general illumination come from the retained table and are `observed` (the three-banks' middle and lower targets `conflicted`); lamps are unplaced until a table or
  drawing marks their sockets.

## What would complete the record

- **Spatial placement**: a Meteor table that models its insert bulbs (or a lamp-location drawing), a second independent table or a factory-drawing callout check for the switches and coils, and an
  outhole model with an object at 33.
- **Three-bank middle targets**: the harness probe or owner check described above.

## Retained table and its defects

The geometry comes from `Meteor (Stern 1979).vpx` by bord with a VR room by Uncle_Paulie (1.0, December 2020), downloaded for this curation. Its script is the pinned corpus script with whitespace
differences. Its defect, stated on the stand-up target: the target's handler also pulses switch 12 (the upper right scoring bumper) on every hit. With `UseSolenoids=2` the loaded VPinMAME
libraries (stern.vbs `GameOnSolenoid = 19`, core.vbs `vpmFlips.TiltSol` and `EnableFlippers`, `TiltObjects` left at 1) follow the flipper enable output 19, so on a tilt the table's flippers
go dead and its thumper bumper and slingshots stop kicking; the retained run exercised only the right slingshot while tilted, and the ROM fired nothing for it.
That makes the script's `SolCallback(16) = "vpmNudge.SolGameOn"` redundant; it hangs on an address the MPU-200 never drives and never fires. Its insert lights show no bulb mesh, so they place
no lamp.

## Sources

- `manual.stern.meteor.1979`: the 40-page IPDB manual with its schematic sheets, with transcribed excerpts of its operating text, option switches, parts pages, switch matrix, coil wiring, solenoid
  driver, lamp driver and lamp list, cabinet wiring and general illumination.
- `manual.stern.meteor.self-test-card`: the self-test card's procedure and solenoid and switch lists.
- `vpx-script.meteor-corpus` and `vpx-script.meteor-standalone`: the pinned known-working corpus scripts.
- `vpx-table.meteor-bord-1-0`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.meteor.*`: eleven isolated harness runs on the pinned `pinmame64.dll`, five of `meteor` (ROM archive SHA-256 `ee849e28a5edd2832012c433e6e71713f8c8773c874139ea24bc6d4bb9529438`) and one each of
  `meteora`, `meteorb`, `meteorbf`, `meteorc`, `meteord` and `meteorfp`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layouts.
