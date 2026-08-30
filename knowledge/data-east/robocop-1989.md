# Robocop (Data East 1989)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.robo_a34` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `robo_a34`, description "Robocop (3.4)", manufacturer
  "Data East", catalog year "1989".
- OPDB record `Grlxe-MJ916` (IPDB 1976) names this machine "Robocop"
  (Data East, manufacture date 1989-11-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `robo_a34`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `robo_a29` (1989, Data East, clone of `robo_a34`).
- `robo_a30` (1989, Data East, clone of `robo_a34`).
- `robo_a34` (1989, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `robo_a34` at `src/wpc/degames.c:279` with machine module `de_mDEAS1`; the definition declares controller platform `pinmame.dataeast` from it.
- The driver source's named switch/solenoid symbols are carried as 36 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 36 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
