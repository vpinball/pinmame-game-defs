# The Simpsons (Data East 1990)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.simp_a27` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `simp_a27`, description "Simpsons, The (2.7)", manufacturer
  "Data East", catalog year "1990".
- OPDB record `G5VBJ-MLy4l` (IPDB 2158) names this machine "The Simpsons"
  (Data East, manufacture date 1990-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `simp_a27`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `simp_a20` (1990, Data East, clone of `simp_a27`).
- `simp_a27` (1990, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `simp_a27` at `src/wpc/degames.c:396` with machine module `de_mDEAS1`; the definition declares controller platform `pinmame.dataeast` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 97 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
