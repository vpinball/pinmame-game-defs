# Frontier (Bally 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.frontier` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `frontier`, description "Frontier", manufacturer
  "Bally", catalog year "1980".
- OPDB record `GRwjq-MJwrd` (IPDB 959) names this machine "Frontier"
  (Bally, manufacture date 1980-11-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `frontier`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `frontiea` (2004, Bally / Oliver, clone of `frontier`).
- `frontieg` (2011, Bally / Scott, clone of `frontier`).
- `frontier` (1980, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `frontier` at `src/wpc/by35games.c:916` with machine module `by35_mBY35_51S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
