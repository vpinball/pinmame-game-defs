# Rollergames (Williams 1990)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.rollr_l2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `rollr_l2`, description "Rollergames (LA-2)", manufacturer
  "Williams", catalog year "1990".
- OPDB record `Gr1Ko-MnKyx` (IPDB 2006) names this machine "Rollergames"
  (Williams, manufacture date 1990-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `rollr_l2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `rollr_d2` (1990, Williams, clone of `rollr_l2`).
- `rollr_e1` (1991, Williams, clone of `rollr_l2`).
- `rollr_ex` (1991, Williams, clone of `rollr_l2`).
- `rollr_f2` (1990, Williams, clone of `rollr_l2`).
- `rollr_f3` (1990, Williams, clone of `rollr_l2`).
- `rollr_g3` (1990, Williams, clone of `rollr_l2`).
- `rollr_l1` (1991, Williams, clone of `rollr_l2`).
- `rollr_l2` (1990, Williams).
- `rollr_l2c` (2019, Williams, clone of `rollr_l2`).
- `rollr_l3` (1990, Williams, clone of `rollr_l2`).
- `rollr_p2` (1991, Williams, clone of `rollr_l2`).
- `rollr_ta2` (2025, Williams, clone of `rollr_l2`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `rollr_l2` at `src/wpc/s11games.c:1310` with machine module `s11_mS11CS`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
