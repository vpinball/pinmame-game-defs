# Family Guy (Stern 2007)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.fg_1200ag` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `fg_1200ag`, description "Family Guy (V12.0 English, German)", manufacturer
  "Stern", catalog year "2008".
- OPDB record `G5LW9-MQ6N5` (IPDB 5219) names this machine "Family Guy"
  (Stern, manufacture date 2007-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `fg_1200ag`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `fg_1000af` (2007, Stern, clone of `fg_1200ag`).
- `fg_1000ag` (2007, Stern, clone of `fg_1200ag`).
- `fg_1000ai` (2007, Stern, clone of `fg_1200ag`).
- `fg_1000al` (2007, Stern, clone of `fg_1200ag`).
- `fg_1100af` (2007, Stern, clone of `fg_1200ag`).
- `fg_1100ag` (2007, Stern, clone of `fg_1200ag`).
- `fg_1100ai` (2007, Stern, clone of `fg_1200ag`).
- `fg_1100al` (2007, Stern, clone of `fg_1200ag`).
- `fg_1200af` (2008, Stern, clone of `fg_1200ag`).
- `fg_1200ag` (2008, Stern).
- `fg_1200ai` (2008, Stern, clone of `fg_1200ag`).
- `fg_1200al` (2008, Stern, clone of `fg_1200ag`).
- `fg_200a` (2007, Stern, clone of `fg_1200ag`).
- `fg_300ai` (2007, Stern, clone of `fg_1200ag`).
- `fg_400a` (2007, Stern, clone of `fg_1200ag`).
- `fg_400ag` (2007, Stern, clone of `fg_1200ag`).
- `fg_700af` (2007, Stern, clone of `fg_1200ag`).
- `fg_700al` (2007, Stern, clone of `fg_1200ag`).
- `fg_800al` (2007, Stern, clone of `fg_1200ag`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `fg_1200ag` at `src/wpc/sam.c:2611` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.
- The driver source's named switch/solenoid symbols are carried as 1 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
