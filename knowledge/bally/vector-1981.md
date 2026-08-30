# Vector (Bally 1981)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.vector` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `vector`, description "Vector", manufacturer
  "Bally", catalog year "1982".
- OPDB record `G486B-MrRwE` (IPDB 2723) names this machine "Vector"
  (Bally, manufacture date 1981-03-24); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `vector`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `vector` (1982, Bally).
- `vector4` (2004, Bally / Oliver, clone of `vector`).
- `vectora` (2004, Bally / Oliver, clone of `vector`).
- `vectorb` (2004, Bally / Oliver, clone of `vector`).
- `vectorc` (2008, Bally / Oliver, clone of `vector`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `vector` at `src/wpc/by35games.c:1424` with machine module `by35_mBY35_61S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
