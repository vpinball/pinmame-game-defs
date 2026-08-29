# Phantom of the Opera (Data East 1990)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.poto_a32` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `poto_a32`, description "Phantom of the Opera, The (3.2)", manufacturer
  "Data East", catalog year "1990".
- OPDB record `Grq1D-MQokp` (IPDB 1777) names this machine "Phantom of the Opera"
  (Data East, manufacture date 1990-01-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `poto_a32`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `poto_a29` (1990, Data East, clone of `poto_a32`).
- `poto_a31` (1990, Data East, clone of `poto_a32`).
- `poto_a32` (1990, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `poto_a32` at `src/wpc/degames.c:308` with machine module `de_mDEAS1`; the definition declares controller platform `pinmame.dataeast` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
