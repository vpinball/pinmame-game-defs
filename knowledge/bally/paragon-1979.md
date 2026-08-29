# Paragon (Bally 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.paragon` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `paragon`, description "Paragon", manufacturer
  "Bally", catalog year "1979".
- OPDB record `GrXy3-ML0Ey` (IPDB 1755) names this machine "Paragon"
  (Bally, manufacture date 1979-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `paragon`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `paragon` (1979, Bally).
- `paragonb` (2004, Bally / Oliver, clone of `paragon`).
- `paragonc` (2008, Bally / Oliver, clone of `paragon`).
- `paragond` (2008, Bally / Oliver, clone of `paragon`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `paragon` at `src/wpc/by35games.c:537` with machine module `by35_mBY35_50S`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 23 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
