# Galaxy (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; every placement rests on one community table with no independent check, and general illumination is unplaced**

## Identity and evidence precedence

This is the one physical Stern Galaxy (IPDB 980, January 1980, model 114, Stern M-200 MPU, 4,947 units; LAI built it under licence in Australia from knock-down kits). PinMAME `galaxy` is the production
root and `galaxyfp` its free-play build; `galaxyps` (Planet Skillshot, 2011) changes the rules only. All three use the same game-data line (`GEN_STMPU200`, six-digit `dispst6` displays,
`FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound). `galaxyb` (2003) and `galaxyc` (2023) are seven-digit conversions: the same machine with seven-digit display hardware (`dispst7`, recorded
as display overrides).

Evidence order is the runbook's. The pinned corpus script (bord's table 1.2, byte-identical to the retained table's own script) gives runtime bindings, this game's own manual gives construction and
wiring (its Playfield Wiring Diagram, Solenoid Driver and Lamp Driver sheets are drawn for Galaxy; the cabinet and transformer sheets are standard and general-use drawings), pinned PinMAME gives the
controller topology, and six retained harness runs (burn-in, solenoid test, switch test, a scripted game, and a game-over and slam run of `galaxy`, plus the solenoid test of `galaxyb`) pair the
printed numbers with public addresses. The manual prints each schematic in two halves on consecutive pages.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty, so the Switch Identification numbers
are the public addresses. Positions 17, 25, 27, 28, 31, 32 and 34 are printed `OPEN` (`N/U` on the matrix sheet) and are unused. Position 33 is printed `OPEN` in the identification table, but the
matrix sheet labels it `OUT-HOLE`, the location drawing points at the out-hole, and the ROM kicks the out-hole while it is closed: it is the out-hole switch. Every matrix contact is normally open; the
playfield sheet draws a series diode on every cell, and the cabinet sheet draws coin chutes 2 and 3 without one. Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); the
last two are PinMAME routes with no documented button. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke contacts and the door's S33
memory-clear button are hard-wired and have only profile-local identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them
as `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over three identical cycles, and the `galaxyb` test gives the
same pairs. In public terms: 1 right slingshot, 2 left slingshot, 3 top thumper, 4 drop-target bank reset, 5 kicker-lane ball kicker, 6 knocker, 7 lower right thumper, 8 saucer eject, 9 red, 10 blue,
13 yellow and 14 black drop-target knock-down coils, 11 out-hole kicker, 12 lower left thumper, 17 general-illumination relay, 18 coin lockout, 19 flipper enable relay. Public 15 (driver 16) is printed
OPEN and unused; 16 is an unaddressable decoder slot; 20 (driver 18) is wired only to N/U pins and is driven only in the power-up pulse and the tests, so it is unused. The gameplay run independently
confirms 1-5, 7-14, 17 and 19.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this
game's own sheet was read for all sixty lines. The connector blocks give each SCR its pin; several of their hand-written pin numbers are blotted, and each is settled by the lamp list and the ROM
(the device notes say which). The two typed lamp lists, on the Playfield Wiring Diagram and the Lamp Driver Schematic, print the same 53 lines; they land on 52 public addresses (SAME PLAYER SHOOTS AGAIN is
braced over two pins of one SCR). `SPOT No` prints J1 pin 8, which is the pin of `SPOT "X"`; it is read as J2 pin 8 (SCR Q23, public 27), the only connected SCR without a row, which the ROM and the
script agree on. The eight SCRs without a row, public 14, 15, 29, 30, 31, 46, 47 and 62, change only in the burn-in and lamp tests and are unused. Four backbox lamps are listed with the rest: GAME OVER
45, HIGH SCORE TO DATE 13, MATCH 63 and TILT 61.

**General illumination.** IPDB notes that Galaxy has computer-controlled general illumination, perhaps the first machine to have it. The Solenoid Driver Schematic wires continuous driver Q17 (public 17) to
J5 pin 7 `GEN. ILLUM. RELAY`, and the cabinet sheet draws the relay coil beside the coin lockout and the knocker. No sheet draws the relay's contacts: the playfield sheet draws the 6 VAC `GEN. ILLUM`
string, the cabinet sheet the front-door lamp and the transformer sheet the backbox strings, all straight from the transformer. The known-working script switches all of the table's general illumination off
while 17 is on, and the ROM flickers 17 for about two seconds when a game starts, when the top-right star completes G-A-L-A and at game over. The definition records 17 as a relay that turns the general
illumination off while energized (relationship `inverted`); which strings the real relay switches is not documented.

## Ball lifecycle

Galaxy is a single-ball game with no trough. The ball starts on the out-hole switch (33). When a game starts the ROM resets the drop-target bank (4) and kicks the out-hole (11), repeating the kick for as
long as 33 stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane, where the player launches it through the ball gate at the top of the lane. After a drain the bonus is
added, the ball-in-play digit advances and the kick repeats. Tilt drops the flipper enable relay (19) and lights TILT; a slam (8) ends the game and the ROM restarts through its power-up test.

## Mechanisms

- **Four-bank drop targets** on the left, top to bottom black (switch 9), yellow (10), blue (11) and red (4). One reset coil (4) raises the bank; each target also has its own knock-down coil (14 black,
  13 yellow, 10 blue, 9 red) that the ROM fires to spot it: the upper, middle and lower stand-ups (30, 29, 26) knock down black, yellow and blue, and the return lanes knock down red. The ROM resets the bank
  when its fourth target goes down and at every serve; each completion advances the planet ladder Mercury (54), Venus (38), Mars (22), Jupiter (6), Saturn (53), Uranus (37), Neptune (21), Pluto (5).
- **Eject pocket (saucer)** at the top, inside the loop: switch 40, eject coil 8, about three seconds after the closure. Its value (2,000 to 10,000, lamps 60, 12, 28, 44, 59) is advanced by the top
  thumper and the spinner.
- **Kicker lane (kickback)** at the upper left: switch 35, kicker coil 5 about four seconds after the closure; it scores 3,000 plus 2,000 for each G-A-L-A-X-Y letter spotted.
- **Spinner** across the passage below the eject pocket: switch 5, no coil.
- **Thumper bumpers** 12 (top), 13 (lower right), 14 (lower left) fire public 3, 7 and 12; **slingshots** 16 (left) and 15 (right) fire 2 and 1.
- **Flippers**: one per side, each a dual-winding coil on its cabinet button, gated by the flipper enable relay. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside).
- **Passive gates**: the ball gate where the shooter lane meets the top arch and a one-way gate at the left end of the top lanes.

## Rules summary

From the manual's feature pages: spotting G-A-L-A-X-Y lights the letters in the kicker lane; the top lanes and the top-right star spot G-A-L-A, and the left and right inner return lanes spot X and Y. The
outer return lanes score 2,000 and spot a drop target when lit; the outlane stars score 5,000 (10,000 when lit). Completing the drop-target bank advances the planets; the drop-target special lights at the
planet the option switches choose. The stand-ups score 500 and spot their drop target; the star roll-overs score 10 and advance the bonus. Option switch 24 lets the two A's light together.

## Scoring checkpoints from the retained gameplay run

Thumpers 1,000; slingshots 10; top lanes 5,000 with X and Y made; stand-ups 500; the spinner 1,000 when lit; the outer return lanes 2,000; the inner return lanes 500; the outlanes 5,000; the
center stars 10. These are first-ball ROM scores and only checkpoints.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 9). Coin chutes 2, 3 and 1 take S1-5, S9-13 and S27-30. S6 high-score award, S7 balls per game, S8 spot lights,
S14 background sound, S15-16 high game to date, S17 extra ball, S18-19 maximum credits, S20 credit display, S21 match, S22 special replay limit, S23 attract sound, S24 the A feature, S25-26 the planet
that lights the drop-target special, S31-32 special award. S33 on the MPU is a memory-clear pushbutton, repeated on the coin door.

## Displays and sound

Four six-digit player displays (indices 0-3, segment starts 2, 10, 18 and 26), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME
`dispst6`. The seven-digit conversions move the player displays to starts 1, 9, 17 and 25. Sound is the Stern C-605 sound module (ST300); sound commands add no playfield devices.

## Disagreements between this game's own documents

- The Switch Identification table calls drop target 9 and stand-up 30 GREEN; the matrix sheet calls both BLACK, and the feature text calls the upper target black. One colour, two names.
- The Switch Identification table prints 33 as OPEN; the matrix sheet, the location drawing and the ROM make it the out-hole.
- Both lamp lists print `SPOT No` on the pin of `SPOT "X"`; see the address translations.
- The credit text says coin chute 1 uses switches 28-30; the switch assignment braces 27-30 and the chute 1 table has four columns, 30 to 27.

## Recreation checklist

- Build the full inventory: 33 used and seven unused matrix positions, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two
  flipper callbacks, the sixty SCR lamp addresses and the six displays.
- Start with the ball on the out-hole switch, all four drop targets up, the saucer empty and the flipper enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the bank reset and the four knock-down coils, the saucer eject, the kicker-lane kickback, the out-hole serve loop and the tilt behaviour as the harness runs show.
- Turn the general illumination off while public 17 is on.
- Treat the manual and the ROM as the rules authority; the community ROMs change rules or displays, not the playfield.
- Placements come from the retained table only; the spatial report lists what still needs an independent check.

## Sources

- `manual.stern.galaxy.1980`: the 35-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches, operating text and wiring sheets.
- `vpx-script.galaxy-bord-1-2`: the pinned corpus script.
- `vpx-table.galaxy-bord-1-2`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.galaxy.*` and `runtime.galaxyb.solenoid-test`: six isolated harness runs on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
