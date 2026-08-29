# Big Bat (Bally Midway 1984)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.bigbat` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `bigbat`, description "Big Bat", manufacturer
  "Bally Midway", catalog year "1984".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `bigbat`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bigbat` (1984, Bally Midway).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `bigbat` at `src/wpc/bowlgames.c:201` with machine module `by35_mBY35_61S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
