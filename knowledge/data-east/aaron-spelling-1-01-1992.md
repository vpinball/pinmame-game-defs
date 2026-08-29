# Aaron Spelling (1.01) (Data East 1992)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.aar_101` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `aar_101`, description "Aaron Spelling (1.01)", manufacturer
  "Data East", catalog year "1992".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `aar_101`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `aar_101` (1992, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `aar_101` at `src/wpc/degames.c:806` with machine module `de_mDEDMD32S2A`; the definition declares controller platform `pinmame.dataeast` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
