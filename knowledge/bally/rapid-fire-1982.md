# Rapid Fire (Bally 1982)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.rapidfir` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `rapidfir`, description "Rapid Fire", manufacturer
  "Bally", catalog year "1982".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `rapidfir`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `rapidfia` (2005, Bally / Oliver, clone of `rapidfir`).
- `rapidfir` (1982, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `rapidfir` at `src/wpc/by35games.c:1584` with machine module `by35_mBY35_61BS`; the definition declares controller platform `pinmame.by35` from it.
- The driver source's named switch/solenoid symbols are carried as 24 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 24 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
