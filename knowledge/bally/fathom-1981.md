# Fathom (Bally, 1981) - recreation knowledge

Bally game number 1233. A four-player, three-ball-multiball, six-switch-column Bally MPU
AS-2518-35 machine with seven-digit displays, a Squawk & Talk AS-2518-61A sound board, an
AS-2518-52 auxiliary lamp driver and an AS-2518-66 solenoid expander. Physical release year 1981,
taken from the machine's own manual title page (`GAME 1233`, `(c) BALLY MFG. CORP 1981`) and from
the 1981 approval dates in every schematic title block; the two `fathoma` and `fathomb` drivers are
2004 Bally/Oliver free-play and modified-rules ROMs for the same physical machine, exactly as
`centaura` and `centaurb` are for Bally Centaur, and PinMAME reuses `init_fathom` for both.

## Reading the driver declaration

`src/wpc/by35games.c` line 1264 declares
`INITGAME2(fathom, GEN_BY35, dispBy7, FLIP_SW(FLIP_L), 8, SNDBRD_BY61B, 0)`. That fifth argument, 8,
is the **auxiliary lamp-column count**, not a switch-column count: the `INITGAME2` macro expands to
`core_tGameData {gen, disp, {flip, 0, lamps, 0, sb, db, BY35GD_NOSOUNDE}}` and `core_tGameData.hw` is
declared `{flippers, swCol, lampCol, custSol, ...}`, so the macro passes a literal `0` for `swCol`
and `8` for `lampCol`. Bally Centaur and Bally Kiss declare the same `lampCol = 8`. No Bally MPU game
declares a custom switch column at all: `by35.c` reads five strobes from PIA0:A and one more from
PIA1:B, so six columns and forty-eight matrix positions is the platform ceiling, and how many of them
a game wires is a property of its own harness rather than of its driver declaration.

`dispBy7` gives four seven-digit player score displays plus a two-digit credit display and a
two-digit Match / Ball in Play display. `BY35GD_NOSOUNDE` is set, and `BY35GD_SWVECTOR` is not, which
is what puts the sixth switch strobe on PIA1:B bit 7 rather than bit 4.

## What is unusual about this machine

**Nineteen printed momentary solenoid functions on fourteen driver outputs.** The Bally MPU
publishes fifteen momentary addresses, and Fathom needs more, because each of its two three-target
in-line drop banks has an individual coil per target position as well as a bank reset coil. The
Solenoid Expander (A15, AS-2518-66) closes the gap. A lamp-driver SCR output - public lamp address
47, printed `TO AUX. EXPANDOR J1-2` on the A5 sheet and `SCR ANODE LAMP DRIVER` on the expander's
own connector - drives a MOC3011 optocoupler which energizes a 48 V relay K1, and the relay's
contacts switch the 43 VDC solenoid bus between two groups of coils. Five driver outputs therefore
each reach one of two coils:

| public solenoid | relay de-energized | relay energized |
| --- | --- | --- |
| 1 | 3 Top Drop Target Reset (blue in-line bank) | 1st Green Inline Drop Target |
| 2 | 6 Drop Target Reset (left six-bank) | 2nd Green Inline Drop Target |
| 3 | 3 Middle Drop Target Reset | 3rd Green Inline Drop Target |
| 13 | Top Saucer Kicker | 1st Blue Inline Drop Target |
| 14 | Right Saucer Kicker | 2nd Blue Inline Drop Target |

Public 4 (Right Inline Drop Target Reset) and public 15 (3rd Blue Inline Drop Target) are not
shared. A table author has to model this: firing address 13 does one of two completely different
things depending on the state of lamp 47.

**The sixth switch-column strobe is public solenoid 20.** Fathom wires forty-eight switches, which
is six columns of eight, but the MPU's PIA0:A supplies only five strobes. The playfield wiring
diagram takes `ST 5` from `A4J4-8`, and that is the PIA1:B PB7 line that PinMAME publishes as
continuous solenoid 20. The A3 sheet's own Q18 driver output for that line reaches nothing but pins
printed `N/U`. So address 20 is permanently asserted in play and is not a coil. This differs from
both earlier BY35 machines in this project: Bally Centaur spends public 17 on its sixth strobe, and
Bally Kiss, a five-column game, spends 17 on a real coil.

**The flipper coils have no address of their own.** All three coils - lower left, lower right and
an upper right flipper wired in parallel with the lower right - hang on the 43 VDC bus behind the
contacts of relay K1, whose coil is public solenoid 19. Only the right flipper button is in the
switch matrix, at address 7; the left button is direct-wired into the relay circuit and the ROM
cannot read it. PinMAME's public 46 and 48 are synthetic ball-physics outputs.

## Mechanisms a table author has to build

- **Outhole and three-station trough.** Fathom is a multiball game, so the outhole carries three
  matrix stations: `Outhole` (1), `#1 Left of Outhole` (2) and `#2 Left and #1 Right of Outhole`
  (3). The third printed name records that one contact serves two ball positions. Public solenoid 7
  kicks a ball to the shooter lane.
- **Left six-bank drop targets**, printed A (top) to F (bottom), switches 32 down to 27, raised by
  public solenoid 2. A rebound rubber behind the bank scores on switch 19, which is shared with the
  10-point rubber elsewhere on the playfield.
- **Middle three-bank drop targets**, switches 35, 34, 33 for #1, #2, #3, raised by public
  solenoid 3. Knocking them down in order lights the extra-ball target.
- **Two in-line drop target banks.** The blue bank (printed `3 Top`) lies across the top of the
  playfield: switches 44, 43, 42 for the 1st, 2nd, 3rd target, running left to right, reset by
  public solenoid 1, with individual drop coils at public 13, 14, 15. The green bank (printed
  `Right Inline`) runs up the right side: switches 48, 47, 46 for the 1st, 2nd, 3rd target, nearest
  the player first, reset by public solenoid 4, with individual drop coils at public 1, 2, 3. Only
  the front target of an in-line bank can be hit, so the ROM knocks each target down with its own
  coil to advance the sequence. Option switch S22 decides whether targets left down carry over.
- **Two saucers**, top and right, with a rollover button in each feeding lane (switches 25 and 26)
  separate from the saucer switch itself (4 and 5). Option switch S6 decides whether a ball left in
  a saucer is kicked out at end of game.
- **Three CPU-driven thumper bumpers** and **two slingshots**, all on ordinary switch-then-coil
  pairs.
- **Two captive balls**, Lagoon and Cave, each with its own release insert (public lamps 40 and 56)
  that lights when the ball may be freed. Nothing releases them electrically; the player does it by
  hitting the captive ball. That, and the three-station trough, is where the multiball comes from.
- **A spinner** on the left side (switch 18) with its own insert at public lamp 60.

## Lamp inventory

The AS-2518-23 lamp driver has four MC14514CP decoders, one per lamp data line, each using outputs
0 to 14 and leaving output 15 unconnected - which is exactly the selector value PinMAME's
`by35_lampStrobe` skips. So public lamp address = `16 * data_line + decoder_output + 1`, giving
four runs of fifteen: 1-15, 17-31, 33-47 and 49-63, with 16, 32, 48 and 64 unreachable decoder
slots rather than unused lamps.

The address-to-connector-pin part of that chain is a property of the board and is identical on
Centaur, Kiss and Fathom, including the eight outputs (11, 12, 27, 28, 43, 44, 59, 60) that branch
to a second connector pin. On Fathom every one of those second pins is printed `N/U`, which is a
useful self-check: Fathom's own A5 sheet draws arrows into exactly eight `N/U` pins, and they are
exactly those eight.

Public lamp 47 is not a lamp at all - it is the Solenoid Expander relay's control input. The other
fifty-nine main-board addresses are real: two ten-step bonus ladders (blue and green, 1K to 10K
plus 50K and 55K) with 3X to 5X multipliers, the A/B/C lanes, both out and return lane specials, the
three thumper bumper lamps, the spinner, the two captive-ball release inserts, `A-B-C Special`,
`In Sequence`, `Double`/`Triple Playfield Scores`, both saucer arrows, `Extra Ball`, `Bonus
Special`, `Same Player Shoot Again` and the credit indicator, plus the six fixed Bally back box
status lamps at the platform's usual addresses (11 Shoot Again, 13 Ball In Play, 27 Match, 29 High
Score To Date, 45 Game Over, 61 Tilt).

The auxiliary AS-2518-52 board is where the record is incomplete. It is **not** the AS-2518-43 that
Centaur and Kiss carry: four MC14028B decoders and twenty-eight SCRs against two and twelve, so no
derivation transfers. Its own U1 fourth flip-flop is not driven from J1, so only three latched
address bits reach it, each decoder uses outputs 0 to 6, and output 7 is printed `N/U` on all four.
Public auxiliary address = `64 + 16 * data_line + decoder_output + 1`, giving 65-71, 81-87, 97-103
and 113-119. Fathom's A9 sheet annotates only seven of the twenty-eight outputs with a function, and
those seven are a seven-step chase: `#1`, `#2`, `#3 Scan Rollover Button` at 65, 81, 97, and `#4`
through `#7 Back Scan` at 113, 66, 82, 98, with #5, #6 and #7 also scanning the three left lanes.
The three `Scan Rollover Button` lamps land exactly on the three rollover buttons of switch 20 in
the retained table, which independently confirms the arithmetic. The other twenty-one outputs are
fitted SCRs whose connector destinations the sheet leaves unlabelled; five of them (67, 83, 99, 114,
115) are proven driven by the ROM in the retained harness run and are enumerated as used with an
unresolved function, and sixteen more are enumerated with an unknown disposition rather than
declared unused, because failing to observe an address is not proof it is unused.

## General illumination

Fathom has no general-illumination controller channel. The playfield wiring diagram feeds the
general illumination from an unswitched 5.9 VAC transformer secondary at `A2J1-1/3/4/6`, with a
separate `FEATURE LAMP BUS` at `A2J1-5`. `coreGlobals.gi[]` is WPC, Whitestar and SAM only, so
there is nothing for a consumer to bind.

## Retained table caveats

The retained known-working table is a competent recreation but three of its bindings are wrong on
this platform and must not be copied:

1. Its `SolCallback(25)`, `(26)`, `(27)`, `(37)` and `(38)` assignments for five of the six
   individual in-line drop-target coils are dead code. Pinned `core_getSol`'s `solNo <= 28` branch
   reads `coreGlobals.solenoids`, where a Bally MPU driver only ever sets bits 0-14 and 16-19, and
   its 37-44 branch serves only WPC-95 and System 11. Those five callbacks can never fire. The real
   addresses are public 1, 2, 3 (green) and 13, 14 (blue); only its `SolCallback(15)` for the 3rd
   blue target is right.
2. It binds public lamps 12 and 28 to the bottom and right thumper bumpers respectively, which is
   the opposite of the printed wiring. See
   `conflict.thumper-bumper-lamp-address-swap`; the definition follows the manual.
3. It drives an apron light object at public lamp 11, where the printed wiring puts the back box
   `Shoot Again` socket; the playfield `Same Player Shoot Again` insert is public lamp 43.

Its `Const cGameName="Fathom"` line uses a capital F, which is not a PinMAME driver short name;
VPinMAME resolves the name case-insensitively, so it does bind the production `fathom` parent.
