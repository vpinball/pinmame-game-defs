# Pinbot (Williams 1986)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.pb_l5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pb_l5`, description "Pin-Bot (L-5)", manufacturer
  "Williams", catalog year "1986".
- OPDB record `G41Z8-MJKvP` (IPDB 1796) names this machine "Pinbot"
  (Williams, manufacture date 1986-10-06); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pb_l5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pb_j1` (2020, A.M. Thurnherr, clone of `pb_l5`).
- `pb_j2` (2023, idealjoker, clone of `pb_l5`).
- `pb_j3` (2023, idealjoker, clone of `pb_l5`).
- `pb_j5` (2026, idealjoker, clone of `pb_l5`).
- `pb_l1` (1986, Williams, clone of `pb_l5`).
- `pb_l2` (1986, Williams, clone of `pb_l5`).
- `pb_l3` (1986, Williams, clone of `pb_l5`).
- `pb_l5` (1986, Williams).
- `pb_l5h` (2012, Francis, clone of `pb_l5`).
- `pb_p4` (1986, Williams, clone of `pb_l5`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pb_l5` at `src/wpc/s11games.c:357` with machine module `s11_mS11XSL`; the definition declares controller platform `pinmame.system-11` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 56 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
