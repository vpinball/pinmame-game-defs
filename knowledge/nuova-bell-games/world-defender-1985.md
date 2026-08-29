# World Defender (Nuova Bell Games 1985)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.worlddef` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `worlddef`, description "World Defender", manufacturer
  "Nuova Bell Games", catalog year "1985".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `worlddef`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `worlddef` (1985, Nuova Bell Games).
- `worlddfp` (1985, Nuova Bell Games, clone of `worlddef`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `worlddef` at `src/wpc/nuova.c:373` with machine module `by35_mBY35_45S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
