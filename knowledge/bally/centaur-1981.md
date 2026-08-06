# Centaur

Coverage: **partial - complete except for five auxiliary lamp addresses whose population the surviving documentation does not determine**

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

One thing, and it is a limit of the surviving documentation rather than of the analysis.

**Five auxiliary matrix positions, 68, 84, 100, 113 and 116, cannot be resolved.** The A9 Auxiliary
Lamp Driver parts list counts twelve SCRs, Q1 through Q12. The A9 harness wire list prints exactly
eleven functions - three top lanes, two slingshots, two thumper bumpers and four chambers - and all
eleven are assigned to other addresses. So exactly one of those five positions carries the twelfth
output and the other four have no bulb behind them, and nothing available says which.

Every route has been tried. The A9 board's decoder-output-to-connector wiring is not in the
Internet Archive scan, the maintainer-supplied schematic manual, or the German edition; the manual
carries the A9 parts list and its harness wire list but not the board sheet. The wire list leaves
the relevant pins unlabelled. Neither retained script references any of the five. The harness cannot
discriminate them: all sixteen auxiliary positions light together during the self-test lamp
sequence and none of the five ever appears outside it, because PinMAME reports lamp-matrix bits
rather than bulbs and the ROM drives the data line whether or not an SCR is fitted. And the retained
table cannot break the tie either - it parks 68, 84 and 100 in the bottom-left placeholder row and
models no light at all for 113 and 116.

Resolving it needs the A9 board schematic sheet, or someone with the physical machine.

That single gap keeps three coverage dimensions open - `output_enumeration`, `output_semantics` and
`spatial_placement` - and therefore keeps the record `partial`. Everything else is done: identity,
the full 48-position switch matrix with polarity, all 32 MPU option switches, twenty-one solenoid
outputs including the resolved sixth switch-column strobe, seventy-one of seventy-six lamps named
from the schematic, six displays, ten mechanisms, three driver variants, and spatial records for
177 of 182 devices.
