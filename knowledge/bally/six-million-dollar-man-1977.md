# Six Million Dollar Man (Bally 1977)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.smman` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
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

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
