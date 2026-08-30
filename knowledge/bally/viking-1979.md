# Viking (Bally 1979)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.viking` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `viking`, description "Viking", manufacturer
  "Bally", catalog year "1980".
- OPDB record `G57kN-MQ71K` (IPDB 2737) names this machine "Viking"
  (Bally, manufacture date 1979-12-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `viking`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `viking` (1980, Bally).
- `vikingb` (2004, Bally / Oliver, clone of `viking`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `viking` at `src/wpc/by35games.c:868` with machine module `by35_mBY35_51S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
