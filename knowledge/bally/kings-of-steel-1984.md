# Kings of Steel (Bally 1984)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.kosteel` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `kosteel`, description "Kings of Steel", manufacturer
  "Bally", catalog year "1984".
- OPDB record `GR67j-M7ZYy` (IPDB 1382) names this machine "Kings of Steel"
  (Bally, manufacture date 1984-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `kosteel`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `kosteel` (1984, Bally).
- `kosteela` (2004, Bally / Oliver, clone of `kosteel`).
- `tigerrag` (1984, Bell Games, clone of `kosteel`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `kosteel` at `src/wpc/by35games.c:1755` with machine module `by35_mBY35_45S`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 32 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
