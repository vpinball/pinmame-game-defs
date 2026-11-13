# Pool Player (Illinois Pinball, 2000)

Coverage: **partial - identity, driver and Capcom platform only. No input, output, display or mechanism inventory is
recorded yet.**

This record holds PinMAME's one Pool Player driver, `pp100` (Pool Player (1.0)). It was split from
`capcom.breakshot.1996`, whose curator `tools/curate_breakshot.py` writes and checks it.

## What is known

- IPDB 4495 lists Pool Player as Illinois Pin Ball Incorporated's game of 2000 (trade name IPB), a solid-state
  four-player game with an acrylic backglass. Its notes say the playfield is Breakshot's, reportedly slightly modified,
  and that none was ever sold to the public. Pinside lists it as a conversion kit with a dot-matrix display, three
  flippers and no ramps.
- Pinball News reported in October 2000 that Illinois Pinball's founder, Gene Cunningham, had bought Capcom's remaining
  stock, and that the company's Pool Player flyer shows three games that look like rebranded Breakshots with differences
  between them: two with automatic ball launchers and one with a manual launcher, and silver, black and gold legs with
  matching trim.
- PinMAME declares `pp100` a clone of Breakshot's `bsv103` with Breakshot's switch inversion mask, flipper set and sound
  ROMs, so it routes exactly as Breakshot does. Shared routing does not show that the cabinet matches.

The sources are excerpted under `evidence/excerpts/illinois-pinball.pool-player.2000/`.

## Why it is not part of the Breakshot record

`capcom.breakshot.1996` describes the machine Capcom's manual documents, whose ball is plunged by hand. Pool Player's
own sources describe a modified playfield and versions with an automatic ball launcher, hardware Breakshot does not have,
and none says which version `pp100` ran on. Until that is known the firmware cannot be called compatible with Breakshot,
so its driver is `unknown` here.

## What a curator must establish next

- The OPDB identity: the pinned snapshot has no Pool Player record.
- How the playfield differs from Breakshot's, and how each version's automatic launcher is fitted and driven, including
  which solenoid and switch addresses it uses under `pp100`. Photographs, an owner or the ROM itself could settle it;
  the authorized ROM library holds no copy.
- The full input, output and display inventory. Breakshot's record is a starting point only: every address has to be
  confirmed against this firmware.
- Wiring, polarity, mechanism behaviour and normalized placements.
