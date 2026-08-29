# Bobby Orr's Power Play (Bally 1977)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.pwerplay` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pwerplay`, description "Power Play", manufacturer
  "Bally", catalog year "1978".
- OPDB record `G4en0-MJ5vB` (IPDB 1858) names this machine "Bobby Orr's Power Play"
  (Bally, manufacture date 1977-02-24); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pwerplay`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pwerplab` (2008, Bally / Oliver, clone of `pwerplay`).
- `pwerplac` (2018, Bally, clone of `pwerplay`).
- `pwerplay` (1978, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pwerplay` at `src/wpc/by35games.c:176` with machine module `by35_mBY17`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 67 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
