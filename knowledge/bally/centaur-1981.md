# Centaur

Coverage: **partial - identity, addressing, switch and solenoid semantics and displays are validated; mechanisms, polarity, lamp semantics and spatial placement are not, and one continuous output is an unresolved conflict**

Bally game #1239, 1981, IPDB 476. Four-player, five-ball, black-and-white playfield with a
Squawk & Talk speech board. This is the project's first Bally MPU AS-2518-35 machine, so it
introduced the `pinmame.by35` controller profile that every later BY35-driver machine should reuse.

## Physical family

`centaur` is the 1981 production ROM. `centaura` (2004) and `centaurb` (2008, rev. 27) are the
Bally/Oliver free-play ROMs: later firmware for the same physical machine, not new games. Their
release years do not create new physical titles.

`centauri` and `centaurj` are Inder's unrelated 1979 Spanish machine. They share only the name and
must stay a separate record.

## The solenoid numbering trap

This is the fact most likely to be got wrong, and it is worth stating plainly because the available
sources state it three different ways.

The manual's solenoid identification table is headed **"Self Test #"**. That column is the order in
which the ROM's solenoid test pulses each coil. It is *not* the PinMAME public solenoid address.
PinMAME writes a four-bit selector to PIA1:B and sets bit `selector`, so the public address is
`selector + 1`, and the ROM's test order is unrelated to that.

Printed page 13 gives the way to resolve it:

> Pressing the Self-Test button again causes each solenoid to be energized, one at a time, in a
> continuous sequence. ... The number appearing on the Player Score displays is the same as the
> number assigned to the solenoid.

Booting the ROM and watching that test therefore publishes the mapping directly, and it is the
mapping the definition carries:

| Self test | Device | Public address |
| ---: | --- | ---: |
| 01 | Outhole kicker | 7 |
| 02 | Knocker | 6 |
| 03 | Inline drop target reset | 8 |
| 04 | 4 right drop target reset | 9 |
| 05 | Left thumper bumper | 10 |
| 06 | Right thumper bumper | 11 |
| 07 | Left slingshot | 12 |
| 08 | Right slingshot | 13 |
| 09 | ORBS target reset | 1 |
| 10 | Right 4 drop target "1" (top) | 2 |
| 11 | Right 4 drop target "2" | 3 |
| 12 | Right 4 drop target "3" | 4 |
| 13 | Right 4 drop target "4" (bottom) | 5 |
| 14 | Ball release | 15 |
| 15 | Ball kick to playfield | 14 |
| 16 | Coin lockout door | 18 |
| 17 | K1 relay (flipper enable) | 19 |
| 18 | Magnet | 20 |

Three traps follow:

1. **Printed 14 and 15 are transposed against public 14 and 15.** The numbers collide but the
   devices swap. Ball release is public 15; ball kick to playfield is public 14.
2. **Public 7 is the outhole kicker.** Both retained community scripts label it a release to the
   shooter lane (`SolBallRelease`, `SRelease`), so the community naming is wrong here.
3. **Public 17 is driven, but nobody agrees what it does.** The identification table accounts for
   only three continuous devices, at printed 16, 17 and 18, which are public 18, 19 and 20. The ROM
   asserts public 17 and never releases it, so it is not an empty slot. PinMAME's LISY bridge
   special-cases Centaur (`lisy35.c` case 7) and masks continuous bit 0 out of the coil data as a
   strobe line, while `by35.c` takes the sixth switch-column strobe from PIA1:B bit 7, which is
   public 20, the magnet. Those cannot both be right, so the address is recorded as an unresolved
   conflict rather than guessed either way. Do not read the absence of a *pulse* on a continuous
   output as evidence that it is unused - a held line never pulses.

The continuous assignments are independently confirmed by PinMAME's own LISY bridge, which drives
real Bally hardware from this driver and names continuous bit 1 the coin lockout and bit 2 the
flipper-enable relay - public 18 and 19.

The legacy import this record grew from had two defects that the self test exposes: it omitted
public solenoid 4 entirely, which shifted the right four-bank labels by one and left address 5
carrying the label for target "3", and it had no magnet at all.

## Flippers

Centaur's flipper coils are switched by the K1 relay rather than by a driver-board output, which is
why they carry no solenoid number of their own and why energising that relay is effectively the
game-on signal. The retained standalone script uses public 19 exactly that way, for nudge handling.
Both flipper buttons are wired to the single matrix address 21. PinMAME also maintains a generic
flipper-button column at 81-88, but Centaur declares `FLIP_SW(FLIP_L)` with no `FLIP_SWNO`, so
`FLIP_SWL` and `FLIP_SWR` are zero, `core_updateSw` never copies that column into the game matrix,
and the ROM - which strobes only columns 1-6 - never reads it. Those addresses are not a mirror of
21 and nothing populates them; they are retained only because the legacy corpus bound them.

## Shared switch addresses

Centaur wires several physical contacts in parallel onto one address, so a recreation cannot tell
which one closed. The manual prints the quantity in parentheses:

- **12** - the top left lane rollover button, the ORBS two back targets, and the target behind the
  right thumper bumper: three printed descriptions, four physical devices, one address.
- **15** Tilt (3), **16** Slam (2), **18** Left side rollover button (2), **34** 10 point rebound (5).
- **21** - both flipper buttons.

Matrix positions **07, 13, 14, 23, 35 and 36** are printed blank: the positions exist, Centaur wires
nothing to them. The seven label conflicts this record inherited from the two legacy sources are all
resolved from the manual, and in every case the platform-level source was right and the game-level
source wrong. Position 07 is the exception where neither was right: one called it Tilt, the other
left it generic, and the manual prints nothing there because tilt is position 15.

## Displays

`dispBy7`: four seven-digit player score displays and two two-digit displays for credits and for
match/ball-in-play. The parts list matches, with one AS-2518-54 and four AS-2518-58 display driver
modules. PinMAME also publishes a seventh display, a 128x32 composite it renders from the segment
data; that is an emulator artifact and not a physical device, so the definition declares six.

## Lamps

The AS-2518-23 lamp driver module carries sixty outputs, and its parts list counts exactly sixty
SCRs. PinMAME's lamp strobe ignores the decoder selector value 0x0f and advances two matrix columns
per data bit, so the public addresses are 1-15, 17-31, 33-47 and 49-63. Note that the skipped value
is a *selector*, not a public address: public lamp 15 is a real, addressable output. What the skip
produces is the gaps at 16, 32, 48 and 64, which are unreachable decoder slots rather than unused
lamps.

Centaur also carries an **Auxiliary Lamp Driver A9** (AS-2518-43), which `centaurGameData` declares
as `lampCol = 8`. That reserves a second board's worth of addresses at 65-79, 81-95, 97-111 and
113-127. Runtime observation shows sixteen auxiliary lamps in use, at 65-68, 81-84, 97-100 and
113-116, but absence of the rest is not proof that they are unused: the lamp inventory is still open
and is one reason this record is not author-ready.

The legacy corpus bound sixty lamps spread across 2-114, which is neither the main board's sixty
outputs nor a coherent subset of both boards. The retained harness runs observed seventy-six
addresses, sixteen of which the legacy corpus never bound: 1, 11, 13, 27, 29, 43, 45 and 61 on the
main board and 66, 67, 82, 83, 99, 113, 115 and 116 on the auxiliary board. Those are now declared
with an `observed` provenance and no semantic name, because this manual scan contains no lamp
identification table. Every declared lamp keeps a `candidate` naming status: the labels are legacy
carry-over and none of them has been checked against the machine.

The parts list also names a Solenoid Expander (AS-2518-66) and an Aux. Driver (G.I. Flasher)
(AS-2518-68) that are not yet accounted for in the definition.

## Sound

Squawk & Talk (`SNDBRD_BY61B`). PinMAME carries a Centaur-specific `BY35GD_REVERB` flag, documented
in `by35.h` as the speech-reverb flag for this game, alongside `BY35GD_NOSOUNDE`. Centaur's growling
speech is the reason that flag exists.

## What is still missing

- **Mechanisms.** The inline drop-target bank, the right four-bank with its four individual down
  coils plus one reset, the ORBS bank, the trough and sub-trough ball path, and the upper-right
  magnet all need topology, causality and home-state documentation. The parts list fixes the coil
  complement they must account for: three drop target reset coils, four individual drop target
  coils, two thumper bumpers, two slingshots, one outhole kicker, one kick to playfield, one ball
  release, one magnet, one knocker, one coin lockout and two flippers.
- **Polarity.** Normally-open versus normally-closed construction is not yet recorded per switch.
- **Continuous output 1.** What public 17 drives is an open conflict, recorded in the definition.
  Resolving it needs either the schematic sheet for the solenoid driver and switch-strobe wiring or
  a harness run that watches switch column 6 while that line is toggled.
- **Lamp semantics, nearly resolved.** The Internet Archive scan contains no lamp identification
  table, which long made lamp identity the hard blocker. A maintainer-supplied schematic set carries
  the names as wire lists of the form wire number, connector pin, function: the A9 sheet names all
  sixteen auxiliary lamps (four chambers of two, plus the thumper bumpers, slingshots and top lanes)
  and the A5 sheet names the sixty playfield lamps.

  The addressing chain is now closed. `by35_lampStrobe` collapses to
  `public = 16 * d + lampadr + 1`, and page 52 gives the output-to-SCR table for all four MC14514
  decoders. Three checks pass: every (output, IC pin) pair matches the MC14514 pinout, all sixty
  SCRs are used exactly once, and output 15 is unconnected on each decoder - which is precisely the
  selector the driver skips.

  Grouping the legacy labels by decoder output then shows the board's organisation: each output
  drives the same class of lamp on all four decoders - the bonus ladder on outputs 1-2, the four
  rollovers on 5, the drop-target arrows on 6-7, the chambers on 8, the captive orbs on 11, and the
  backbox indicators on 10 and 12. The legacy corpus and the schematic were produced independently
  and agree on that structure, which is far stronger evidence than either alone. It also decodes the
  legacy naming scheme: "Middle N" is the N,000 bonus, "Left Lane N" is the N chamber, "Bottom N" is
  captive orbs #N, and "5K N" are the four rollover lanes numbered right to left.

  Two legacy labels look wrong: public 15, 31, 47 and 63 are labelled "Bonus 2x/3x/4x/5x" but sit
  hard against the right edge at x about 0.85, and the schematic's right-hand group is RIGHT LANE
  2X/3X/5X, while the real bonus multipliers are public 5/21/37/53 - public 5 traces directly to
  J1-14 "2X BONUS". The two multiplier groups appear to have been swapped in the legacy import.

  The J1, J2 and J3 connector lists are now read in full, which completes the chain. Fifty-seven
  of the sixty main-board addresses carry their printed schematic name, and the seven addresses
  the retained script binds by name all agree with the derivation - Shoot Again, Ball in Play,
  Match, High Score to Date, Tilt Warning, Game Over and Tilt. Public 1 turns out not to be a
  lamp at all: it feeds pin 3 of the Aux. Driver (G.I. Flasher) module, which is why the legacy
  corpus never bound it.

  On the auxiliary board, seven of the sixteen lamps are now named from geometry rather than a
  traced wire: three sit directly above the three top-lane switches in the same left-to-right order,
  and four form a vertical column up the left edge in exactly the bottom-to-top order the wire list
  prints for "#1 CHAMBER (2) (FROM BOTTOM)" through "#4 CHAMBER (2) (TOP)". Each chamber address
  drives two bulbs, which the wire list marks with (2). The A9 board's decoder-output-to-pin wiring
  has not been traced, so these rest on geometry and group ordering, not on a wire.

  A caution discovered while doing that: the retained table parks the auxiliary lamps its author
  never mapped in a row of seven at x 0.11-0.24, y 0.950, evenly spaced along the bottom-left
  corner. That is a modelling placeholder, not a bulb location, and an earlier pass had wrongly
  promoted those coordinates to validated placements. They have been withdrawn. When mining a
  community table for geometry, check for rows of equally spaced lamps before trusting them.

  Three main-board addresses stay unresolved: 17, 59 and 62, against the three unassigned printed functions
  Spot 1-4 (A5J2-7), Credit Indicator (A5J3-13) and Release Orb (A5J1-1). Which is which needs
  the last few SCR-to-connector rows traced. Those three keep their unverified legacy labels and
  a `candidate` status, and the sixteen auxiliary lamps are still unnamed, so `output_semantics`
  and `output_enumeration` remain in `coverage.missing`. See
  `external:pinmame-review-artifacts/centaur-1981/lamp-identity-research.md`.
- **Variant differences.** Nothing beyond "free play" distinguishes `centaura` and `centaurb` from
  the production ROM in this record.
- **DIP switches.** The MPU carries four eight-position option banks, S1-S32, and none of them is
  enumerated here. `MDRV_DIPS(35)` reserves three further emulator-side positions that are not
  physical switches and must not be presented as such.
- **Flipper coils.** Public 46 and 48 are now declared as the PinMAME-synthesised handles on the two
  direct-wired flipper coils, but their real drive path - the K1 relay and the button contacts -
  is documented only in prose and has no typed wiring record.
- **Spatial placement, mostly done.** 143 of the 150 devices now carry a spatial record. Positions
  come from the retained table, normalized as x/952.941 and y/1976.471: lamp coordinates are the
  centers of the Light objects named `l<address>`, each of which carries `timer_interval` equal to
  its PinMAME lamp address (verified for all 67), and switch coordinates are the centers of objects
  named `sw<address>`. Figure V corroborates independently - the bumpers, flippers, outhole, trough
  and upper-right magnet all land where the printed diagram puts them - and it supplies the
  off-playfield classification, so the cabinet, door and backbox devices take controlled
  `not_applicable` records instead of invented coordinates. The seven backbox indicator lamps
  (Shoot Again, Ball in Play, Match, High Score, Warning, Game Over, Tilt) are exactly the lamps for
  which the table has no playfield light, which is a satisfying cross-check rather than a gap.

  Seven devices remain unplaced, deliberately. The four trough switches and End of Trough would
  need a judgement about which modelled slot is which physical trough position; the five-contact
  10 Point Rebound address needs five separate rebound locations; and the two unnamed auxiliary
  lamps 113 and 116 have no light object at all. Guessing any of these would be worse than leaving
  them named as missing.

  Note the drop-target coils: an individual down coil takes its own target switch's position,
  because they are one assembly, but each bank's single reset coil is a **documented projection** -
  the centroid of that bank's target switches - and is marked as such rather than presented as an
  observed socket.

## Sources

- `manual.bally.centaur.1981`: Bally game #1239 Centaur installation and operation manual, retained
  as an Internet Archive scan. Solenoid and switch identification tables on printed page 17, Figure
  V playfield location diagram on printed page 18, self-diagnostic description on printed page 13,
  parts list on printed page 20, lamp driver module parts list on printed page 23.
- `runtime.centaur.solenoid-self-test`: LibPinMAME harness run against the `centaur` ROM capturing
  the ROM's own solenoid test, retained under `review-artifacts/centaur-1981/harness/`.
- `pinmame.core.4ec52ff0ac13`: `centaurGameData` and the BY35 driver.
- `vpx-script.centaur-2-0-0` and `vpx-script.centaur-standalone`: two independent known-working
  table scripts, used as runtime corroboration and as the source of the mislabelling noted above.
- `legacy.game.centaur` and `legacy.platform.bally`: the migration inputs this record grew from.
