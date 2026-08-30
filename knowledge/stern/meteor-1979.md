# Meteor (Stern 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.meteor` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `meteor`, description "Meteor", manufacturer
  "Stern", catalog year "1979".
- OPDB record `G5b38-MDqkx` (IPDB 1580) names this machine "Meteor"
  (Stern Electronics, manufacture date 1979-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `meteor`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `meteor` (1979, Stern).
- `meteora2` (2019, Stern / Idleman, clone of `meteor`).
- `meteorb` (2003, Stern / Oliver, clone of `meteor`).
- `meteorbf` (1979, Stern, clone of `meteor`).
- `meteorc` (2003, Stern / Oliver, clone of `meteor`).
- `meteord` (2005, Stern / Oliver, clone of `meteor`).
- `meteore` (2019, Stern / Idleman, clone of `meteor`).
- `meteore7` (2019, Stern / Idleman, clone of `meteor`).
- `meteorf` (2020, Stern / Idleman, clone of `meteor`).
- `meteorf7` (2020, Stern / Idleman, clone of `meteor`).
- `meteorfp` (1979, Stern, clone of `meteor`).
- `meteorg` (2021, Stern / Idleman, clone of `meteor`).
- `meteorg7` (2021, Stern / Idleman, clone of `meteor`).
- `meteorns` (2011, Stern / Scott, clone of `meteor`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `meteor` at `src/wpc/stgames.c:351` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.
- The driver source's named switch/solenoid symbols are carried as 74 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 74 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
