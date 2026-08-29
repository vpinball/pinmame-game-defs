# Victory (Gottlieb 1987)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.victory` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `victory`, description "Victory", manufacturer
  "Gottlieb", catalog year "1987".
- OPDB record `GrdBk-Mq18w` (IPDB 2733) names this machine "Victory"
  (Gottlieb, manufacture date 1987-10-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `victory`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `victory` (1987, Gottlieb).
- `victoryf` (1987, Gottlieb, clone of `victory`).
- `victoryg` (1987, Gottlieb, clone of `victory`).
- `victr101` (1987, Gottlieb / Tom Collins, clone of `victory`).
- `victr11` (1987, Gottlieb / Tom Collins, clone of `victory`).
- `victr12` (1987, Gottlieb / Tom Collins, clone of `victory`).
- `victr13` (1987, Gottlieb / Tom Collins, clone of `victory`).
- `victrffp` (1987, Flipprojets, clone of `victory`).
- `victrgfp` (1987, Flipprojets, clone of `victory`).
- `victryfp` (1987, Flipprojets, clone of `victory`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 30 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
