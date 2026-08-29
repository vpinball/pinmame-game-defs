# System 1 'T' Test Fixture (Gottlieb year unknown)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.sys1test` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `sys1test`, description "System 1 'T' Test Fixture", manufacturer
  "Gottlieb", catalog year "19??".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `sys1test`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `sys1test` (19??, Gottlieb, clone of `gts1`).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
