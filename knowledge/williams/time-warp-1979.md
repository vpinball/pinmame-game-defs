# Time Warp (Williams 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tmwrp_l3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tmwrp_l3`, description "Time Warp (L-3)", manufacturer
  "Williams", catalog year "1979".
- OPDB record `G5wJo-MQdvv` (IPDB 2568) names this machine "Time Warp"
  (Williams, manufacture date 1979-09-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `tmwrp_l3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tmwrp_l2` (1979, Williams, clone of `tmwrp_l3`).
- `tmwrp_l2ff` (1979, Williams, clone of `tmwrp_l3`).
- `tmwrp_l3` (1979, Williams).
- `tmwrp_l3ff` (1979, Williams, clone of `tmwrp_l3`).
- `tmwrp_t2` (1979, Williams, clone of `tmwrp_l3`).
- `tmwrp_t2ff` (1979, Williams, clone of `tmwrp_l3`).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
