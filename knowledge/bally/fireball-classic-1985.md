# Fireball Classic (Bally 1985)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.fbclass` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `fbclass`, description "Fireball Classic", manufacturer
  "Bally", catalog year "1984".
- OPDB record `G48ZN-MLONl` (IPDB 853) names this machine "Fireball Classic"
  (Bally, manufacture date 1985-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `fbclass`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `fbclass` (1984, Bally).
- `fbclassa` (2004, Bally / Oliver, clone of `fbclass`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `fbclass` at `src/wpc/by35games.c:1818` with machine module `by35_mBY35_45S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
