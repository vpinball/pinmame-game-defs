# Silverball Mania (Bally 1978)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.slbmania` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `slbmania`, description "Silverball Mania", manufacturer
  "Bally", catalog year "1980".
- OPDB record `GRD2P-MDX5b` (IPDB 2156) names this machine "Silverball Mania"
  (Bally, manufacture date 1978-06-29); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `slbmania`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `slbmania` (1980, Bally).
- `slbmanib` (2004, Bally / Oliver, clone of `slbmania`).
- `slbmanic` (2013, Bally / Idleman, clone of `slbmania`).
- `slbmanid` (2013, Bally / Idleman, clone of `slbmania`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `slbmania` at `src/wpc/by35games.c:741` with machine module `by35_mBY35_51S`; the definition declares controller platform `pinmame.by35` from it.
- The driver source's named switch/solenoid symbols are carried as 29 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 29 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
