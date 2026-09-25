# Elvira and the Party Monsters (Bally 1989)

Coverage: **partial**. Every switch, lamp, solenoid, flasher, relay, display and mechanism is
enumerated, named and wired from the factory manual, and the runtime bindings are taken from a
known-working table. The record stays partial for three concrete reasons:

- the manual puts the two slingshot lamps on opposite sides in its matrix and its drawing;
- two flasher bulb counts differ between the solenoid table and the location drawing; and
- the flip-up targets' switch roles differ between the manual's parts pages and the retained script.

Each has a resolution path in the definition's `conflicts`. Playfield general illumination has no
bulb inventory in the manual and carries no placement.

## Identity and drivers

- IPDB 782, OPDB `Grlxp-MVKBW`: Bally (Midway), model 2011, production start September 5, 1989,
  System 11B, 4,000 units. Designed by Dennis Nordman and Jim Patla, art by Greg Freres.
- Eight PinMAME drivers, all `CORE_GAMEDEF`/`CORE_CLONEDEF` in
  `src/wpc/sims/s11/prelim/eatpm.c` sharing `eatpmGameData`: `eatpm_l4` (LA-4, parent, the ROM both
  retained scripts run), `eatpm_l1` (LA-1), `eatpm_l2` (LA-2), `eatpm_f1` (LF-1 French), `eatpm_4u`
  (LU-4 Europe), `eatpm_4g` (LG-4 German), `eatpm_3g` (LG-3 German, U26 flagged `BAD_DUMP`) and
  `eatpm_p7` (PA-7 prototype). The production and localized sets are the same machine. The LG-3
  reconstruction and the prototype are recorded as compatible rather than identical.

## Controller contract

- `GEN_S11B` on `controllers/pinmame/system-11.json`. The switch and lamp matrices are
  column-major, `address = (column - 1) * 8 + row`, 1-64, exactly as the manual prints them.
- `hw.gameSpecific1 = S11_MUXSW2` and `sxx.muxSol = 12`. Solenoid 12 is the A/C Select Relay, and
  PinMAME overwrites **switch 2** with the relay's state on every switch update. On the machine it
  is opto isolator U1 on the Backbox Interconnect Board, lit from the 28 V C-side supply. Do not
  drive switch 2 from a recreation: it is relay feedback, not a playfield device.
- **A/C multiplexing**. Eight driver transistors each serve an A circuit (public 1-8, relay off)
  and a C circuit (public 25-32, relay on). On this machine every C circuit is a flasher group and
  every A circuit except 4 is a coil. Circuit 04A is printed with no function and no part and is
  recorded as unfitted.
- **General illumination is two relays, not a GI channel.** Solenoid 10 is the Insert GI relay on
  the backbox insert board, and solenoid 11 is the Playfield GI relay mounted on the playfield
  (both C-11998-1). PinMAME's per-game output-typing comments call 10 "Playfield GI" and 11
  "Backbox GI". That is the reverse of the manual, but both addresses get the same bulb model, so
  published values are unaffected. The retained script treats 11 as playfield GI, as the manual
  does.
- **Special solenoids 17-22** are Special #1-#6 in the manual's order: left thumper, left
  slingshot, right thumper, right slingshot, bottom thumper, flip-up reset. The Williams
  `setSSSol` permutation maps the six PIA handlers (commented F SS6, E SS5, B SST2, C SST3, A SS1,
  D SS4) back to exactly that order. `sxx.ssSw` is empty, so PinMAME does not model the hardware
  path where a bumper or slingshot switch fires its own coil; public 17-21 reflect the ROM's PIA
  writes only. A recreation should fire the bumpers and slingshots from their own switches (35,
  33, 36, 34, 37), as the retained table does.
- **Flippers** are cabinet-wired: the buttons switch the coils directly and the CPU only enables
  them through 1P19. The CPU reads the right button on switch 57 and the left on 58 through two
  4N25 opto isolators on the Backbox Interconnect Board (schematic printed 3-18): U3 "RT L.C." closes
  column 8 to row 1 and U2 "LT L.C." closes column 8 to row 2, with each LED spanning its flipper
  coil's 50 V supply and coil return. The physical sense therefore closes only while the flipper circuit conducts.
  **In PinMAME, drive 82 (right) and 84 (left), not 57/58.** With keyboard handling off,
  `core_updateSw` rewrites 57/58 every update from PinMAME's flipper switch column, which on this
  platform is public 82/84 (`CORE_SWLRFLIPBUTBIT`/`CORE_SWLLFLIPBUTBIT`). The VPinMAME `S11.VBS`
  library the table loads sets exactly those (`swLRFlip = 82`, `swLLFlip = 84`), and its
  `core.vbs` binds the table's flipper callbacks to the hold addresses 46/48. The definition
  enumerates PinMAME's whole flipper column, 81-88: 82 and 84 are used, and the end-of-stroke and
  upper-button positions (81, 83, 85-88) are unused: `FLIP_SWNO(58,57)` sets no `FLIP_EOS` or
  upper `FLIP_SW` bit, so PinMAME never copies them anywhere, and the ROM cannot read them because
  `s11.c`'s `pia4a_r` reads the switch matrix only through `core_getSwCol` with an eight-bit column
  strobe, which reaches columns 1-8. The table's own `Controller.Switch(57/58)` writes are
  overwritten on the next update and have no effect.
  `FLIP_SWNO(58,57)` without `FLIP_SOL` makes PinMAME fabricate 45-48 from the buttons. No
  end-of-stroke switch exists in the matrix.
- **Polarity.** `wpc.invSw` is all zero, so PinMAME normalizes nothing. The three JAM drop targets
  are optos, but the C-12559 board converts each through an LM339 comparator into an ordinary
  diode-isolated matrix closure. The known-working script drives 1 for a dropped target, and a
  recreation should do the same.
- Displays: two 16-character 16-segment alphanumeric displays. Controller index 0 at segment 0 is
  the left board (Player 1/2), index 1 at segment 20 the right board (Player 3/4). The manual's
  status-display text refers to them as the Player 1-4 displays.

## Mechanisms

- **Trough**: outhole (9) and kicker (1), three balls on 11/12/13 with 11 nearest the shooter,
  ball eject into the shooter lane (2), shooter lane switch 21.
- **Skull ball lock**: lock entry 29, three positions 49/50/51 above lock safety 52, lock release
  8. The rules call this "the Skull": B-A-T or JAM completion enables the lock.
- **Eject hole** 48 with coil 5, where Hold Bonus, Million, Barbeque and Boogie (lamps 41-44) are
  collected.
- **Ball popper** 32 with coil 6: it pops the ball up onto the popper wire ramp.
- **JAM drop targets** 41-43 with reset coil 3.
- **Flip-up targets**: two targets below the left ramp, each a standup target switch (53, 54) plus
  a position switch on the flip-up bracket (55, 56, "Flip Up Open"), and one shared reset coil
  (22). The retained script holds 53/54 closed until the reset and pulses 55/56 once; the parts
  layout suggests 55/56 are the switches that report the flipped state. Which address the ROM
  expects held is open.
- **Boogie Monsters**: one coil (14) moves a rocker link so both rubber boogie men move together,
  with a spring return and no switch. Solenoid 16 flashes their lamps.
- **Ramps**: the left Monster Slide ramp (entry 30, end 31) and the right Party Punch ramp (entry
  44). No coil acts on either.
- **Thumper bumpers** 35/36/37 (coils 17/19/21, lamps 54/55/56), **slingshots** 33/34 (coils
  18/20), **knocker** 7 in the backbox.

## Lamps

- Lamps 1-56 are playfield inserts. 1-6 spell ELVIRA, 38-40 are J-A-M, 45-47 are B-A-T, and 17/18
  are the skull eyes.
- Lamps 57-59 (Dead Head 1-3) are on the **backboard**: the rules light "one Dead Head on
  Backboard", and the lamp boards list a 3-Lamp Back Stop.
- Lamps 60-64 (Barbeque 1-5) are **backbox** lamps. The manual's Circuitboards text (printed 1-2)
  says "Lamp circuit boards are mounted on the Playfield and the Insert Board", neither group
  appears on the playfield lamp drawing, and the retained script comments them "BackGlass" and
  places their objects beyond the playfield.
- The manual prints lamps 11 and 20 on opposite slingshots in its matrix (11 left) and its drawing
  (11 right). Resolve with a real-machine lamp test before placing them.

## Retained table notes

The only retained `.vpx` is an artwork variant of the 32assassin table. The pinned corpus's
`v1.03.vbs` is the same lineage with newer physics, so it corroborates the bindings but is not an
independent source. Both scripts share three table defects to keep out of a recreation:

- lamp 54's state drives the bodies of the 55 and 56 bumper lamps;
- the skull-eye glow flashers fl17/fl18 each sit beside the other eye's bulb cover; and
- backboard and backglass lamps are drawn as rear-edge and off-table proxies.

The scripts' flip-up switch pattern (53/54 held, 55/56 pulsed) is not listed as a defect. It is the
open question in `conflict.flip-up-switch-roles`, since the ROM may accept either pattern.

## Manual notes

The manual is IPDB's 118-page OCR-searchable scan of operations manual 16-2011-101 (August 1989).
Its text layer shifts some table columns, so every cited table was read from the rendered page.

- **Carryovers from other machines**: the A/C relay example calls 01C "the Transporter Flashers
  circuit", and the Single Lamps text says lamp 01 shows "BONUS 1K".
- **Internal inconsistencies, transcribed as printed**:
  - the bumper assembly is p/o C-12872 on the switch list but C-12842 in the parts list;
  - the flip-up switch part is 5674-12073-30 on its assembly page but 5647-12073-30 on the switch
    list; and
  - three connector or pin cells break the table's own pattern (05C `5J4-5`, 15 `5J5-2`,
    17 `1P10-7`).

## Runtime harness

Exploratory LibPinMAME runs (pinned library 3.7.0, SHA-256 `deb2c99f…`) of `eatpm_l4`, `eatpm_l1`,
`eatpm_l2` and `eatpm_4u` from fresh NVRAM all stop after the FACTORY SETTING message:

- no lamp or solenoid activity follows;
- only ADVANCE (the PIA interrupt input) is serviced;
- coin and start are ignored; and
- stepping through every Id/Au/Ad status item wraps back to Id without reaching the diagnostic
  tests.

Black Knight 2000, Police Force, Jokerz and Whirlwind behave the same way in this harness, so this
is a harness/platform limitation, not an Elvira fact. The runs are retained under the working root
as diagnostics and are not cited as evidence. The special-solenoid mapping above comes from static
source analysis, which settles it without a trace.
