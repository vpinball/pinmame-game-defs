# Hot Hand (Stern 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.hothand` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `hothand`, description "Hot Hand", manufacturer
  "Stern", catalog year "1979".
- OPDB record `GRvNk-MQkro` (IPDB 1244) names this machine "Hot Hand"
  (Stern Electronics, manufacture date 1979-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `hothand`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `hothand` (1979, Stern).
- `hothanfp` (1979, Stern, clone of `hothand`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `hothand` at `src/wpc/stgames.c:277` with machine module `by35_mST100bs`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
