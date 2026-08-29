# Speakeasy (Bally 1982)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.speakesy` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `speakesy`, description "Speakeasy", manufacturer
  "Bally", catalog year "1982".
- OPDB record `GRbl7-ML8EY` (IPDB 2270) names this machine "Speakeasy"
  (Bally, manufacture date 1982-01-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `speakesy`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `speake4a` (2004, Bally / Oliver, clone of `speakesy`).
- `speakes4` (1982, Bally, clone of `speakesy`).
- `speakesa` (2004, Bally / Oliver, clone of `speakesy`).
- `speakesy` (1982, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `speakesy` at `src/wpc/by35games.c:1542` with machine module `by35_mBY35_51S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
