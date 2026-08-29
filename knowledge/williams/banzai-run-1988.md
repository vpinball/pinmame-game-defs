# Banzai Run (Williams 1988)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.bnzai_l3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `bnzai_l3`, description "Banzai Run (L-3)", manufacturer
  "Williams", catalog year "1988".
- OPDB record `GR9lZ-MkP2j` (IPDB 175) names this machine "Banzai Run"
  (Williams, manufacture date 1988-05-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `bnzai_l3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bnzai_g3` (1988, Williams, clone of `bnzai_l3`).
- `bnzai_l1` (1988, Williams, clone of `bnzai_l3`).
- `bnzai_l3` (1988, Williams).
- `bnzai_pa` (1988, Williams, clone of `bnzai_l3`).
- `bnzai_t3` (2011, Williams / Francis, clone of `bnzai_l3`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `bnzai_l3` at `src/wpc/s11games.c:582` with machine module `s11_mS11BS`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
