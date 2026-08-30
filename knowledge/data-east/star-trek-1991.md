# Star Trek (Data East 1991)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.trek_201` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `trek_201`, description "Star Trek 25th Anniversary (2.01)", manufacturer
  "Data East", catalog year "1992".
- OPDB record `G42qQ-MLn3y` (IPDB 2356) names this machine "Star Trek"
  (Data East, manufacture date 1991-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `trek_201`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `trek_110` (1992, Data East, clone of `trek_201`).
- `trek_117` (1992, Data East, clone of `trek_201`).
- `trek_11a` (1992, Data East, clone of `trek_201`).
- `trek_120` (1992, Data East, clone of `trek_201`).
- `trek_200` (1992, Data East, clone of `trek_201`).
- `trek_201` (1992, Data East).
- `trek_300` (2020, Data East, clone of `trek_201`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `trek_201` at `src/wpc/degames.c:577` with machine module `de_mDEDMD16S2A`; the definition declares controller platform `pinmame.dataeast` from it.
- The driver source's named switch/solenoid symbols are carried as 75 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 75 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
