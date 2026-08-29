# Teenage Mutant Ninja Turtles (Data East 1991)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tmnt_104` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tmnt_104`, description "Teenage Mutant Ninja Turtles (1.04)", manufacturer
  "Data East", catalog year "1991".
- OPDB record `Gr8xn-MKN66` (IPDB 2509) names this machine "Teenage Mutant Ninja Turtles"
  (Data East, manufacture date 1991-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `tmnt_104`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tmnt_101` (1991, Data East, clone of `tmnt_104`).
- `tmnt_103` (1991, Data East, clone of `tmnt_104`).
- `tmnt_104` (1991, Data East).
- `tmnt_104g` (1991, Data East, clone of `tmnt_104`).
- `tmnt_200` (2025, Data East, clone of `tmnt_104`).
- `tmnt_a07` (1991, Data East, clone of `tmnt_104`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tmnt_104` at `src/wpc/degames.c:436` with machine module `de_mDEDMD16S1`; the definition declares controller platform `pinmame.dataeast` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 113 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
