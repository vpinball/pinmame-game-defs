# Six Million Dollar Man (Bally 1977)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.smman` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `smman`, description "Six Million Dollar Man, The", manufacturer
  "Bally", catalog year "1978".
- OPDB record `GrEke-ML8qN` (IPDB 2165) names this machine "Six Million Dollar Man"
  (Bally, manufacture date 1977-08-31); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `smman`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `smman` (1978, Bally).
- `smmanb` (2004, Bally / Oliver, clone of `smman`).
- `smmanc` (2008, Bally / Oliver, clone of `smman`).
- `smmand` (2008, Bally / Oliver, clone of `smman`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `smman` at `src/wpc/by35games.c:354` with machine module `by35_mBY35_32S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
