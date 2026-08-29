# Eight Ball (Bally 1977)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.eightbll` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `eightbll`, description "Eight Ball", manufacturer
  "Bally", catalog year "1977".
- OPDB record `GrN7J-MJ78q` (IPDB 760) names this machine "Eight Ball"
  (Bally, manufacture date 1977-01-17); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `eightbll`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `eightblb` (2008, Bally / Oliver, clone of `eightbll`).
- `eightblc` (2018, Bally, clone of `eightbll`).
- `eightbll` (1977, Bally).
- `eightblo` (1977, Bally, clone of `eightbll`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `eightbll` at `src/wpc/by35games.c:139` with machine module `by35_mBY17`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 87 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
