# Centaur

Coverage: **author_ready**

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
3. **Public 17 is the sixth switch-column strobe, not a coil.** The identification table accounts
   for only three continuous devices, at printed 16, 17 and 18, which are public 18, 19 and 20. The
   ROM asserts public 17 and never releases it, so it is not an empty slot either. It is resolved as
   ST5 on converging grounds: 48 switches is six columns while PIA0:A supplies five strobes and the
   schematic shows ST5 originating at a different MPU connector; PinMAME's LISY bridge special-cases
   Centaur (`lisy35.c` case 7) and masks that bit out of the coil data as a strobe line; and the
   trace shows it asserted continuously once scanning starts, which is exactly how a strobe looks
   through `by35.c`, which OR-accumulates solenoid state within each VBLANK window. Do not read the
   absence of a *pulse* on a continuous output as evidence that it is unused - a held line never
   pulses. Kiss corroborates the reading from the other direction: it is a five-column game, does
   not need a sixth strobe, and uses public 17 for a real playfield coil.

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
113-127, of which only sixteen are reachable: 65-68, 81-84, 97-100 and 113-116.

The board's schematic is printed in the Centaur manual itself, on page 51 of the *Installation and
General Game Operation Instructions*, with every J2 pin's function annotated. Tracing it settles the
auxiliary inventory completely. Each lamp data line enables one MC14555B decoder half - PD0 to U2A,
PD1 to U2B, PD2 to U3A, PD3 to U3B - and the two latched address bits select Q0, Q1 or Q2 of that
half. **Q3 is marked N/U on all four halves**, which is why four halves times three used outputs is
the twelve SCRs the parts list counts, and why latched address 3 reaches no bulb on any data line.
Public 68, 84, 100 and 116 are therefore bare matrix positions with no socket behind them. The
retained community table drives playfield star inserts from three of those addresses; that is the
table author's invention, not something the board can light.

| public | decoder | SCR | A9J2 | printed function |
| --- | --- | --- | --- | --- |
| 65 | U2A Q0 | Q6 | 7 | TOP LEFT LANE |
| 66 | U2A Q1 | Q5 | 6 | RIGHT SLINGSHOT |
| 67 | U2A Q2 | Q4 | 5 | #1 CHAMBER (2) (FROM BOTTOM) |
| 81 | U2B Q0 | Q1 | 1 | TOP MIDDLE LANE |
| 82 | U2B Q1 | Q2 | 2 | LEFT SLINGSHOT |
| 83 | U2B Q2 | Q3 | 3 | #2 CHAMBER (2) |
| 97 | U3A Q0 | Q12 | 18 | TOP RIGHT LANE |
| 98 | U3A Q1 | Q11 | 19 | RIGHT THUMPER BUMPER |
| 99 | U3A Q2 | Q10 | 20 | #3 CHAMBER (2) |
| 113 | U3B Q0 | Q7 | 11 | *(blank)* |
| 114 | U3B Q1 | Q8 | 12 | LEFT THUMPER BUMPER |
| 115 | U3B Q2 | Q9 | 17 | #4 CHAMBER (2) (TOP) |

Each circuit lights a pair of bulbs, so the twelve drive twenty-four lamps.

**The two outer top lanes are the opposite way round from the community table.** The table binds its
top right lane insert to public 65 and its top left lane insert to public 97; the factory sheet wires
A9J2-7 to TOP LEFT LANE and A9J2-18 to TOP RIGHT LANE. The manual is ground truth for physical
wiring, and the same traced chain reproduces the table's other nine auxiliary assignments exactly,
so this is a binding mistake in the table rather than a fault in the derivation. A recreation that
copies the table lights the wrong outer lane.

The legacy corpus bound sixty lamps spread across 2-114, which is neither the main board's sixty
outputs nor a coherent subset of both boards. That inventory is now closed from the schematics
rather than carried over: the main board's sixty circuits and the auxiliary board's twelve are
identified through the decoder-to-SCR-to-connector chain, and 68, 84, 100 and 116 are bare matrix
positions rather than lamps. The retained harness runs observed seventy-six addresses, sixteen of
which the legacy corpus never bound: 1, 11, 13, 27, 29, 43, 45 and 61 on the main board and 66, 67,
82, 83, 99, 113, 115 and 116 on the auxiliary board.

The parts list also names a Solenoid Expander (AS-2518-66) and an Aux. Driver (G.I. Flasher)
(AS-2518-68) that are not yet accounted for in the definition.

## Sound

Squawk & Talk (`SNDBRD_BY61B`). PinMAME carries a Centaur-specific `BY35GD_REVERB` flag, documented
in `by35.h` as the speech-reverb flag for this game, alongside `BY35GD_NOSOUNDE`. Centaur's growling
speech is the reason that flag exists.

## What still blocks author-ready, and what rests on reasoning

**Public lamp 113 has no known function and no known position. This is the blocker.** It is a
fitted circuit - decoder U3B output Q0 through SCR Q7 and resistor R15 to A9J2-11 - and the board
can certainly light it. But it is the only one of the twelve whose function the factory schematic
leaves blank, and the blank is deliberate: the genuinely unused pins printed beside it, A9J2-10 and
13 through 16, are all marked N/U explicitly, so Bally distinguished "unused" from "unlabelled" on
this very sheet. Nothing else names it. The switch table gives Centaur three top lanes, printed as
03 TOP RIGHT LANE, 04 TOP MIDDLE LANE and 05 TOP LEFT LANE, so there is no fourth lane for it to
complete, and none of the four retained community tables from 2020 to 2025 models the address at
all. An earlier draft of this record placed it at the arithmetic centroid of the three top-lane
inserts and called that placement validated; it was neither observed nor defensible - a centroid of
three lamps in a row lands on top of the middle one - and it has been withdrawn. The circuit is
enumerated with its wiring recorded and carries no coordinate, which is what keeps this machine
`partial`.

Resolving it needs either a Centaur playfield insert map that reaches A9J2-11, an unrestored machine
photographed with the A9 harness visible, or a lamp test on real hardware.

**Option switches 17-20 come from community documentation.** The printed credits-per-coin tables
cover chutes 1 and 3, on switches 1-5 and 9-13, and omit the centre chute even though the machine
has one - switch 11 is Coin II (Middle). The option-switch documentation carried identically by all
four retained tables, from 2020 to 2025, assigns 17-20 to it, and that documentation agrees with the
printed manual on every one of the 28 switches the manual does document. Note the asymmetry: the
outer chutes use five selector switches each and the centre chute four.

Searched in reaching this state: all three Centaur manuals, the Centaur and Centaur II schematic
sets, the Kiss manual with its schematic-omissions supplement, the Kings of Steel schematics,
archive.org, and four independently authored VPX recreations spanning fifteen years. The A9
schematic was found in the Centaur manual itself after an earlier pass had concluded it was absent
and had fallen back on the Kings of Steel sheet; the boards are identical, but the Centaur print
carries the per-pin lamp functions that the Kings of Steel print does not.
