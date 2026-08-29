# Mysterian (Prototype) (Bally 1982)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.mysteria` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `mysteria`, description "Mysterian (Prototype)", manufacturer
  "Bally", catalog year "1982".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `mysteria`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `mysteria` (1982, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `mysteria` at `src/wpc/by35games.c:1531` with machine module `by35_mBY35_61S2`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
