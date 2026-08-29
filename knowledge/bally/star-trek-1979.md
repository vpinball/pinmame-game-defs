# Star Trek (Bally 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.startrek` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `startrek`, description "Star Trek", manufacturer
  "Bally", catalog year "1979".
- OPDB record `GRVnd-MQZzx` (IPDB 2355) names this machine "Star Trek"
  (Bally, manufacture date 1979-04-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `startrek`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `startreb` (2004, Bally / Oliver, clone of `startrek`).
- `startrec` (2008, Bally / Oliver, clone of `startrek`).
- `startred` (2008, Bally / Oliver, clone of `startrek`).
- `startrek` (1979, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `startrek` at `src/wpc/by35games.c:501` with machine module `by35_mBY35_50S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
