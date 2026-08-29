# Nine Ball (Stern 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.nineball` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `nineball`, description "Nine Ball", manufacturer
  "Stern", catalog year "1980".
- OPDB record `G4jjx-MDbz2` (IPDB 1678) names this machine "Nine Ball"
  (Stern Electronics, manufacture date 1980-12-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `nineball`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `ninebafp` (1980, Stern, clone of `nineball`).
- `ninebala` (2020, Stern / Idleman, clone of `nineball`).
- `ninebalb` (2007, Stern / Oliver, clone of `nineball`).
- `ninebalc` (2021, Stern / Idleman, clone of `nineball`).
- `ninebald` (2021, Stern / Idleman, clone of `nineball`).
- `nineball` (1980, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `nineball` at `src/wpc/stgames.c:974` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
