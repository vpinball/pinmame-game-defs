# Gilligan's Island (Bally 1991)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.gi_l9` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `gi_l9`, description "Gilligan's Island (L-9)", manufacturer
  "Bally", catalog year "1992".
- OPDB record `GRBxQ-MnKX7` (IPDB 1004) names this machine "Gilligan's Island"
  (Bally, manufacture date 1991-04-30); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `gi_l9`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `gi_d3` (1991, Bally, clone of `gi_l9`).
- `gi_d4` (1991, Bally, clone of `gi_l9`).
- `gi_d6` (1991, Bally, clone of `gi_l9`).
- `gi_d9` (1992, Bally, clone of `gi_l9`).
- `gi_l3` (1991, Bally, clone of `gi_l9`).
- `gi_l4` (1991, Bally, clone of `gi_l9`).
- `gi_l6` (1991, Bally, clone of `gi_l9`).
- `gi_l8` (1992, Bally, clone of `gi_l9`).
- `gi_l9` (1992, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `gi_l9` at `src/wpc/sims/wpc/full/gi.c:481` with machine module `wpc_mDMDS`; no reviewed profile covers that module yet, so no platform is declared.
- The driver source's named switch/solenoid symbols are carried as 71 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
