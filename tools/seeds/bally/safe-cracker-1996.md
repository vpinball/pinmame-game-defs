# Safe Cracker (Bally, 1996)

Coverage: **partial - every I/O address, controller binding, polarity and wiring detail is
source-reconciled; `mechanism_behavior` is missing because the moving target's home levels of 56 and 57
and the ramp kickback's trigger edge on 41 are unsettled, and `spatial_placement` because no retained
source says which playfield G.I. bulbs belong to string 1 and which to string 3, and the left big kick opto
(42) has no table object**

## Identity and evidence precedence

This is the Midway Manufacturing Company (trade name Bally) WPC-95 physical machine released March 1996,
model 90003, IPDB 3782, 1,148 units, four balls, a Pat Lawlor design with a narrower and shorter playfield
than a standard game. It covers the ten `sc_*` drivers: `sc_18s11` (game ROM 1.8 with sound S1.1, the
parent), `sc_18n11` (1.8 No Percentaging), `sc_18s2` and `sc_18ns2` (the same with the German-speech sound
ROM S2.4), `sc_17`, `sc_17n`, `sc_14` and `sc_10` (earlier production ROMs with sound S1.0), `sc_091` (the
0.91 prototype) and `sc_18pfx` (Zen Studios' 2019 Pinball FX image of 1.8, four bytes different). All share
one `scGameData` on `wpc_m95S`. The percentaging builds limit how many tokens the game issues by its
earnings, so on free play they issue very few; the No Percentaging builds do not. An exploratory boot of the
prototype ROM shows the same test menu as 1.8 through T.17.

Evidence precedence: the retained known-working v1.0 table (fuzzel, flupper1, rothbauerw) is runtime and
mechanism-causality ground truth, and the pinned corpus's copy of UnclePaulie's v2.0.0 update of it is the
comparison script; the IPDB scan of the operations manual controls physical construction, part numbers,
wiring and device presence; pinned PinMAME `97aa922b` (`src/wpc/sims/wpc/prelim/sc.c`, a preliminary
simulator) controls the controller generation and public addresses; the ROM's own service tests, run on a
legal `sc_18s11` ROM, settled polarity, names and every output's identity; the retained table supplies
coordinates and the factory location drawings check them. Every table used is transcribed under
`evidence/excerpts/bally.safe-cracker.1996/`, and the runs are summarized under
`evidence/runtime/wpc-95/safe-cracker-sc_18s11-*.json`.

The manual describes an earlier ROM than 1.8: its test menu has a T.16 Wheel Test and a T.17 Vari Target
Test that the 1.8 ROM replaces with T.16 MOVING TGT., T.17 TOKEN TEST and so on, and its Section 3 reprint of
the switch matrix carries earlier labels (STANDUP 1-5, VARI TARGET A-C reversed, COIN CHUTE for 43, SCOOP
KICK for 77, TOKEN LEVEL 1 and 2). The definition follows the primary Section 2 tables, which the ROM's names
confirm.

## Controller platform and address topology

WPC-95 (`GEN_WPC95`, hardware generation 0x80) with a 128x32 DMD. Public switches are the eight dedicated
coin-door inputs 1-8, the 8x8 matrix 11-88 in column-first notation and the Fliptronic column 111-118.
Solenoids are 1-28 plus the WPC-95 low-power device controls 37-40 (mirrored at 41-44), the Fliptronic
circuits 33-36 and 45-48, and PinMAME's state channels 29-32. `scGameData` declares
`FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR)`: the lower flippers publish at 45-48 and the upper
right flipper at 33-34, while the upper-left flipper circuits drive the AUTO PLUNGER (35) and the LOCK UP
RELEASE (36).

The game has a second lamp system: the 48 Lamp & Driver P.C.B. A-20909 in the backbox lights the board game
on the backglass. The ROM shifts its states out on the four low-power device control lines (37 enable, 38
clock, 39 data 1, 40 data 2), and `scGameData` declares `lampCol = 6`, so PinMAME decodes the stream through
six 4094 shift registers into lamp columns 9-14, public lamps 91-148. The ROM's T.8 SINGLE LAMPS TEST walks
11-88 and then 91-148 and prints the auxiliary ones as the board's L-numbers: public 91-118 are L24 down to
L1 (data string 1) and 121-148 are L48 down to L25 (data string 2). G.I. strings 2, 4 and 5 (public GI 1, 3
and 4) power those lamps rather than the playfield.

## Switch polarity: what the ROM's service tests settled

The T.1 SWITCH EDGES sweep set every public matrix and Fliptronic address to 1 and back to 0. PinMAME's mask
inverts 31-37, 42, 43, 56-58, 61-66 and 71-76, the optos of the 10-opto board, the moving target and the
drop targets. The ROM named every one of them at public 1 except 43, so those contacts rest closed
(`normally_closed: true`), as the matrix's 'Opto, Typically Closed' shading says. The ROM marks the ten
10-opto-board switches (31-37, 41-43) with `*` in its names.

Two of those optos behave differently, and both retained scripts agree with the ROM about them:

- **41 KICKBACK** is not masked and the ROM names it at public 1 (a closed contact), yet both scripts hold
  public 41 at 1 while the ramp kickback lane is empty and write 0 while the ball passes. Both hold if this
  opto, like its nine neighbours, rests closed with the beam clear: the ROM's "active" state is the clear
  lane. The definition sets `initial_active: true` and states the convention on the device; under the
  platform rule its `normally_closed` is false. A gameplay probe that presented each edge with a ball in play
  drew no kickback coil either way (a ball search began), so which edge fires the ramp kickback is not
  settled.
- **43 TOKEN CHUTE JAM** (the ROM calls it TOKN CHUTE EXIT) is masked, and the ROM names it on the 1 -> 0
  edge: its active state is a closed contact, the clear chute. The scripts leave it at 0 and pulse it to 1
  as a token is dispensed.

Other polarity facts: 24 ALWAYS CLOSED rests at 1 and is named when it opens; the dedicated switches and
the Fliptronic buttons are normally open; the end-of-stroke bits 111, 113 and 115 are synthesized by
PinMAME from the flipper coils. The ROM names 23, 38, 87 and 88 'UNUSED' at public 1: they are scanned but
not fitted. F7 (117) is unused; F8 (118), which the manual's list prints Not Used, is the TOKEN COIN SLOT on
the coin door (CPU J212-9 to Coin Door Interface Board J13-2).

The right cabinet button's opto board carries two optos: F2 (112), which fires the lower right flipper, and
F6 (116), which fires the upper right flipper and the lower right one. A recreation writes both from the
right button.

## The token dispenser (headline mechanism)

When the player cracks the vault the game pays out a magic token. The backbox token mechanism has two
token tubes, each with a shuttle-plunger coil (04-10424): the left tube is solenoid 4 with level switch 81,
the right tube solenoid 2 with level switch 82. A dispensed token passes the token chute opto (43) and
reaches the player. The ROM's T.17 TOKEN TEST pulses 4 and 2 one after the other for each dispense and
ignores a press that arrives while a dispense is running. A token can be put back through the token slot
at the coin door (118, TOKEN COIN SLOT); the rules hint "Replay MAGIC TOKENS for surprising results!". IPDB
counts twenty tokens (19 gold, 1 silver). Service Bulletin 90 (May 1996) replaces the stop brackets
(04-10506) of both shuttle plungers on games built between 5/2/96 and 5/20/96 that dispensed
intermittently.

## The backbox board game and the rules

The backbox has doors that swing open to reveal a backglass printed with a board game; its 48 lamps show
the player's position on the way to the vault (IPDB). The rules (manual page B): the game is timed and shots
add time; at zero the player is in sudden death and the game ends with that ball. The flashing drop targets
light the LOCK on the ramp; locked balls light the bank entrances for a break-in. Inside the bank the
display's wheel moves the player and a guard chases. The wheel is lit from the right upper mini-flipper lane
(switch 25) or the ramp, and its value is collected at the main bank entrance when the yellow lamp is lit.
Multi-ball follows a break-in; guards, laser beams and exploding gifts can stop it, and cyber-dogs and alarms
need quick shots back into the bank entrances. The playfield's center timer is a ring of lamps (12 Center
Timer lamps from "0" to "55").

## Other mechanisms

- **Moving (vari) target**: Vari-Target Assembly A-20851, pushed back by the ball and read by the three
  optos of the 3 Opto Vari Target P.C.B. (56 C, 57 B, 58 A). The reset coil's armature bracket holds the
  pivot arm's teeth; freed, the target snaps forward to home. The manual's adjustment procedure (1-52, 1-53)
  has Opto 3 clear with the target rear-most and completely broken with it forward-most, and the board wires
  OPTO3 to row 8, so 58 reads OPEN (public 1) at home; the procedure gives no home level for 56 and 57. T.16
  MOVING TARGET TEST shows each switch CLOSED at public 0 and OPEN at 1 and decodes the three as the Gray code
  of a position 0-7 with A as the least significant bit: 0 none open, 1 A, 2 B+A, 3 B, 4 C+B, 5 all, 6 C+A,
  7 C. Enter fires the reset coil (3). Pushed fully back the target lets the ball into the underground trough
  at 12. The two scripts encode the depth differently (v1.0 its own code table with 56 alone at home, v2.0.0
  one-hot with nothing at home); take the code from the ROM's decoding and 58's home level from the manual.
- **Top popper and underground trough**: the top popper (68) pops a ball up into the underground trough with
  6 or ejects it back to the playfield with 25. The underground trough's switches are TR1 (11, from the roof
  entrance), TR2 (12, behind the moving target) and TR3 (77, at the bank), where BANK KICK (5) kicks the ball
  out. T.20 TOP TROUGH TEST pulses 6 while 68 is held and 5 while 77 is held.
- **Four 3-bank drop target sets**: top left 61-63 (reset 15), top right 64-66 (16), bottom left 71-73 (27)
  and bottom right 74-76 (28), each with three lamps (64-66, 61-63, 74-76 and 71-73 respectively).
  T.19 DROP TARGET TEST shows each bank's switches by position, flashes its lamps and fires its reset.
- **Spinning disc (the wheel)**: the Spin Target Assembly A-20911, a free-spinning disc read in quadrature by
  the two optos of the Spin Disc Opto P.C.B. (85, 86); no coil.
- **Ramp lock-up**: the Multi-Ball Assembly A-20935 holds two balls (36 front, 37 rear) and LOCK UP RELEASE
  (36) lets them go. The ramp has an entrance switch (83), a made switch (84) and a diverter (7).
- **Kickbacks**: BIG KICK (1) at the left with the left big kick opto (42), KICKBACK (RAMP) (8) at the right
  with opto 41.
- **Ball trough** (31 eject, 32-35 balls 1-4, eject coil 9), **shooter lane** (switch 18, manual ball shooter
  and AUTO PLUNGER 35), **slingshots** (47/48, coils 10/11), **jet bumpers** (left 44/12, right 45/13, top
  46/14, with cap lamps 82 clear, 83 red and 81 yellow).
- **Top light and motor** (26): a motor-driven rotating light on top of the backbox; T.4 holds it on while
  selected. **Light ropes** 1 and 2 (23, 24) are backbox flasher circuits; T.18 LIGHT ROPE TEST flashes them.

## Lamps, flashers and general illumination

Playfield lamps 11-87 are inserts and lane lamps (#555 or #44); 88 is the Start button. The manual's matrix
prints lamps 75 and 76 as BOTTOM R. where the Lamp Locations list, the ROM's names (BL. 3BANK) and the drop
target test put them on the bottom left bank; it also prints INVISIBLE CODE (53) and VARI BREAK IN (86) where
the 1.8 ROM says VAULT LETTER and MOVNG BREAK IN. The v1.0 script crosses lamps 27 and 28 onto lights l28 and
l27; the v2.0.0 change log says the manual picture had those inserts reversed.

Flashers 17-22 are playfield #906 domes (18 adds a #89 bulb among the jet bumpers). The ROM's T.4 and T.5
print the wires of 21-28 in the standard WPC-95 colours (21 BLU-GRN ... 28 BLU-YEL), where this game's
solenoid table and power driver list print them exchanged between the two groups (21 Blu-Brn ... 28 Blu-Gry);
the devices and addresses agree, so the definition follows the game's own pages and notes the ROM text.

G.I.: string 1 (public GI 0) and string 3 (GI 2) light #44 playfield and #555 backbox bulbs and dim in T.6.
String 2 (GI 1) is AUX. LAMP 1 POWER: the manual's footnote calls it always on, but the ROM dims it in T.6.
Strings 4 and 5 (GI 3, 4) are always on.

## Open mechanism behaviour

Two mechanism facts a recreation consumes are unsettled, so `mechanism_behavior` stays in
`coverage.missing`:

- The moving target's home reading. The manual fixes only Opto 3 (58) at home, broken; it gives no home level
  for 56 and 57, so which Gray-code position is home (1 if both are clear) is not established. Resolution path:
  a harness run that holds each candidate reading while the ROM starts a ball and records whether it keeps
  firing the reset coil (3), or a reading of a physical machine's T.16 with the target home.
- The ramp kickback's trigger. Whether KICKBACK (RAMP) (8) fires on 41's clear-to-blocked or blocked-to-clear
  edge is not settled: the retained gameplay probe drew no coil either way. Resolution path: a harness run
  with a ball in play that presents each edge of 41 under different game states, or a physical machine.

## Spatial status and why the record stays partial

Placements come from the retained v1.0 table's script-bound objects; the switch and solenoid location
drawings check them through `tools/drawing_callouts.py` (jet bumper caps and flipper pivots as controls).
The lamp drawing is a symbol diagram with no flippers, so lamp placements stay observed. The jet bumpers
pair as the v1.0 script binds them (Bumper1 left 44, Bumper2 top 46, Bumper3 right 45), which the bumper
cap lamps and the drawing confirm; the v2.0.0 script swaps 44 and 46. The record stays partial because the
table drives all its G.I. bulbs from one channel and no retained drawing or count splits the playfield G.I.
between strings 1 and 3, and because the left big kick opto (42) has no table object: the v1.0 script derives
it from a ball-position rectangle around the LeftKickBack kicker, which is a script surrogate, not the opto.
The switch drawing's callout 42 marks it at the left kickback lane; placing it needs a reproducible drawing
measurement.

## Author construction checklist

- Wire public 1-8, 11-88 and 111-118 as above; hold 22 at 1 with the coin door closed, 24 at 1 always and 41
  at 1 while the ramp kickback lane is clear; write 0 to 41 and 1 to 43 while the ball or a token passes.
- Write the right flipper button to both 112 and 116; the left button to 114.
- Drive the backbox board game from public lamps 91-148 (L24-L1, L48-L25), not from 37-40.
- Model the moving target with the ROM's Gray-code decoding of 56-58, with 58 at 1 while the target is home,
  the spin disc as a quadrature pair, the drop banks with one reset coil each, and the top popper's two coils.
- The token mechanism, light ropes, top light and board-game lamps are backbox devices.

## Sources

- Manual: `Bally_1996_Safe_Cracker_Manual.pdf` (IPDB 3782, via the Wayback Machine), transcribed excerpts in
  `evidence/excerpts/bally.safe-cracker.1996/`.
- Service Bulletin 90 and the IPDB machine page (Wayback captures).
- Retained table `Safe Cracker (Bally 1996) v1.0.vpx` and its extraction; the pinned corpus's v2.0.0 script.
- Pinned PinMAME `97aa922b` and the runs under `evidence/runtime/wpc-95/safe-cracker-sc_18s11-*.json`.

## Procedural note

The service-test runs, the exploratory runs (test-menu listings, the prototype ROM's menu and the kickback
gameplay probe) and the drawing callout reads are retained under the working root's
`review-artifacts/safe-cracker-1996/`.
