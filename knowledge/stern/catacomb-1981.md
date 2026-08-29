# Catacomb (Stern 1981)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.catacomb` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `catacomb`, description "Catacomb", manufacturer
  "Stern", catalog year "1981".
- OPDB record `GRoQ6-MLx0X` (IPDB 469) names this machine "Catacomb"
  (Stern Electronics, manufacture date 1981-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `catacomb`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `catacofp` (1981, Stern, clone of `catacomb`).
- `catacomb` (1981, Stern).
- `cataconb` (2021, Stern / Idleman, clone of `catacomb`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `catacomb` at `src/wpc/stgames.c:1154` with machine module `by35_mST200v`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 51 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
