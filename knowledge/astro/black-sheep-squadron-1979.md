# Black Sheep Squadron (Astro 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.blkshpsq` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `blkshpsq`, description "Black Sheep Squadron", manufacturer
  "Astro", catalog year "1978".
- OPDB record `G4j1L-MZerb` (IPDB 314) names this machine "Black Sheep Squadron"
  (Astro Games, manufacture date 1979-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `blkshpsq`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `blkshpsq` (1978, Astro).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `blkshpsq` at `src/wpc/stgames.c:32` with machine module `by35_mST100`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
