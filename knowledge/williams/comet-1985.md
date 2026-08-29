# Comet (Williams 1985)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.comet_l5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `comet_l5`, description "Comet (L-5)", manufacturer
  "Williams", catalog year "1985".
- OPDB record `Gryd3-MLqjd` (IPDB 548) names this machine "Comet"
  (Williams, manufacture date 1985-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `comet_l5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `comet_l4` (1985, Williams, clone of `comet_l5`).
- `comet_l5` (1985, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `comet_l5` at `src/wpc/s11games.c:138` with machine module `s9_mS9S`; the definition declares controller platform `pinmame.system-11` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 107 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
