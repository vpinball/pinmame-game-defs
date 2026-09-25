# Firepower, Oliver System 7 conversion - recreation knowledge

This partial record holds the five PinMAME drivers for Oliver's System 7 conversions of Williams
Firepower (IPDB 856): `frpwr_a7`, `frpwr_e7` (six-digit, 2005, revision 31), `frpwr_b7` (seven-digit,
2003), `frpwr_c7` (seven-digit, 2006, revision 38) and `frpwr_d7` (seven-digit, 2005, revision 31).
No retained source documents the conversion hardware itself. An Oliver conversion replaces the CPU
board and ROMs, so the playfield and cabinet are presumably the production machine's (curated as
`williams.firepower.1980`), but that is an assumption to verify, not a sourced fact.

## Why a separate record

Each of these drivers declares PinMAME machine driver `s7_mS7S6`: a Williams System 7 CPU board
(`GEN_S7`) with the stock System 6 sound board. The production machine and the Oliver System 6 ROMs
run on a System 6 CPU board (`GEN_S6`). A different CPU board is a different controller platform, so
these drivers follow the rule that split the Kiss Intel-8035 and Eight Ball Deluxe Motorola-68701
prototypes into their own records. The machine identity (IPDB 856, OPDB `G5VDd-MJpqO`) belongs to the
production record, so `identity` stays missing here.

## What pinned PinMAME says

- `INITGAMEFULL` passes the production machine's flipper and special-switch arguments: no left
  flipper matrix switch, the right button copied into switch 45, and special solenoids 17-22 fired by
  switches 26, 25, 27, 28, 42 and 12.
- The game-on enable is published at solenoid 25 (`S7_GAMEONSOL`), not 23.
- The `sxx.ssSw` loop runs over eight entries. When the ROM fires a special solenoid itself, System 7
  maps each PIA control line to a slot (`setSSSol`), and slots 6 and 7 publish 23 and 24. Whether this
  ROM uses those two slots is unknown.
- `s7_dips_r` has the same body as `s6_dips_r`: both return both CPU-board DIP banks, by display
  strobe position, while Master Command Enter (-3) is held. What differs is not the emulator but the
  ROM: the production record's finding that only the D1-D3 Master Command switches matter rests on
  PinMAME's System 6 source comment and the booklet, and which banks the Oliver System 7 ROM samples
  is unverified.
- `frpwr_a7` and `frpwr_e7` use the production six-digit display layout; `frpwr_b7`, `frpwr_c7` and
  `frpwr_d7` use fp_7digit_disp, with the seven-digit players at 0, 7, 20 and 27 and the two-digit
  entries at 34 and 14.

## What has been observed

One retained harness run of `frpwr_b7`, the ROM the retained known-working Firepower table loads,
repeats the production gameplay sequence. The game-on enable asserts at 25, the coin credit appears
on the entry at position 34 and the ball number on the entry at 14, and matrix switches 26, 25, 27,
28, 42 and 12 publish 17-22 in order. That last pairing is PinMAME's switch-driven path, sequential
by construction; the run never makes the ROM fire a special solenoid, never enters a service test
and never reads a DIP switch. `frpwr_a7`, `frpwr_c7`, `frpwr_d7` and `frpwr_e7` have no retained run.

## What is needed to complete it

- A Williams System 7 controller profile, derived from `s7.c`/`s7.h`, covering game-on at 25, the
  eight special-solenoid slots and the DIP banks.
- Harness runs of each driver through its solenoid and switch tests, to establish which public
  solenoids the ROM fires for each special coil and whether 23 and 24 carry anything.
- Enumeration of every address against that profile, with the production record's physical facts
  reused for the devices themselves.
