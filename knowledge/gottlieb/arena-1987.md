# Arena (Gottlieb 1987)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.arena` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `arena`, description "Arena", manufacturer
  "Gottlieb", catalog year "1987".
- OPDB record `G4EKb-MDx4p` (IPDB 82) names this machine "Arena"
  (Gottlieb, manufacture date 1987-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `arena`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `arena` (1987, Gottlieb).
- `arena2` (1987, Gottlieb, clone of `arena`).
- `arena_fp` (1987, Flipprojets, clone of `arena`).
- `arenaa` (1987, Gottlieb, clone of `arena`).
- `arenaafp` (1987, Flipprojets, clone of `arena`).
- `arenaf` (1987, Gottlieb, clone of `arena`).
- `arenaffp` (1987, Flipprojets, clone of `arena`).
- `arenag` (1987, Gottlieb, clone of `arena`).
- `arenagfp` (1987, Flipprojets, clone of `arena`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 47 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
