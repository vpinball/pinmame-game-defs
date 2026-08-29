# Meteor (Stern 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.meteora` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `meteora`, description "Meteor (Bonus Count Offical Fix)", manufacturer
  "Stern", catalog year "1979".
- OPDB record `G5b38-MDqkx` (IPDB 1580) names this machine "Meteor"
  (Stern Electronics, manufacture date 1979-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `meteora`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `meteora` (1979, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `meteora` at `src/wpc/stgames.c:399` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
