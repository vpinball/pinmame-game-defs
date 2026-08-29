# Jungle Lord (Williams 1981)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.jngld_l2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `jngld_l2`, description "Jungle Lord (L-2)", manufacturer
  "Williams", catalog year "1981".
- OPDB record `G5nkY-MDv88` (IPDB 1338) names this machine "Jungle Lord"
  (Williams, manufacture date 1981-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `jngld_l2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `jngld_l1` (1981, Williams, clone of `jngld_l2`).
- `jngld_l2` (1981, Williams).
- `jngld_nt` (2013, A.M. Thurnherr, clone of `jngld_l2`).
- `jngld_ntl2` (2022, idealjoker, clone of `jngld_l2`).
- `jngld_ntl2b` (2021, idealjoker, clone of `jngld_l2`).
- `jngld_ntl3` (2022, idealjoker, clone of `jngld_l2`).

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 49 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
