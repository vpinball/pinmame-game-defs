# Firepower (Williams 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.frpwr_l6` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `frpwr_l6`, description "Firepower (L-6)", manufacturer
  "Williams", catalog year "1980".
- OPDB record `G5VDd-MJpqO` (IPDB 856) names this machine "Firepower"
  (Williams, manufacture date 1980-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `frpwr_l6`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `frpwr_a6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_b6` (2003, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_b7` (2003, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_c6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_c7` (2006, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_d6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_l2` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_l2ff` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_l6` (1980, Williams).
- `frpwr_l6ff` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_t6` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_t6ff` (1980, Williams, clone of `frpwr_l6`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 10 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
