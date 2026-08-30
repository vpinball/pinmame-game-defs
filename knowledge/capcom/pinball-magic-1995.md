# Pinball Magic (Capcom 1995)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.pmv112` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pmv112`, description "Pinball Magic (1.0.12)", manufacturer
  "Capcom", catalog year "1995".
- OPDB record `GrZnn-MJj46` (IPDB 3596) names this machine "Pinball Magic"
  (Capcom, manufacture date 1995-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pmv112`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pmv112` (1995, Capcom).
- `pmv112r` (1995, Capcom, clone of `pmv112`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pmv112` at `src/wpc/capgames.c:131` with machine module `cc2`; the definition declares controller platform `pinmame.capcom` from it.
- The driver source's named switch/solenoid symbols are carried as 128 candidate devices in the definition.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 128 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
