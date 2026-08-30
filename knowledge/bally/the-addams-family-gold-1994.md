# The Addams Family Gold (Bally 1994)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tafg_lx3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tafg_lx3`, description "Addams Family Special Collectors Edition / Gold, The (LX-3)", manufacturer
  "Bally", catalog year "1994".
- OPDB record `G4ODR-MLzY7` (IPDB 21) names this machine "The Addams Family Gold"
  (Bally, manufacture date 1994-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `tafg_lx3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tafg_da2` (1994, Bally, clone of `tafg_lx3`).
- `tafg_da3` (1994, Bally, clone of `tafg_lx3`).
- `tafg_dx3` (1994, Bally, clone of `tafg_lx3`).
- `tafg_h3` (1994, Bally, clone of `tafg_lx3`).
- `tafg_i3` (1994, Bally, clone of `tafg_lx3`).
- `tafg_i3bs` (2026, Bally / RedBall, clone of `tafg_lx3`).
- `tafg_la2` (1994, Bally, clone of `tafg_lx3`).
- `tafg_la3` (1994, Bally, clone of `tafg_lx3`).
- `tafg_lx3` (1994, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tafg_lx3` at `src/wpc/sims/wpc/full/taf.c:557` with machine module `wpc_mFliptronS`; the definition declares controller platform `pinmame.wpc-fliptronic` from it.
- The driver source's named switch/solenoid symbols are carried as 69 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 69 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
