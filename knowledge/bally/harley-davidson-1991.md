# Harley Davidson (Bally 1991)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.hd_l3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `hd_l3`, description "Harley-Davidson (L-3)", manufacturer
  "Bally", catalog year "1991".
- OPDB record `Gr2L0-MDz1W` (IPDB 1126) names this machine "Harley Davidson"
  (Bally, manufacture date 1991-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `hd_l3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `hd_d1` (1991, Bally, clone of `hd_l3`).
- `hd_d2` (1991, Bally, clone of `hd_l3`).
- `hd_d3` (1991, Bally, clone of `hd_l3`).
- `hd_l1` (1991, Bally, clone of `hd_l3`).
- `hd_l2` (1991, Bally, clone of `hd_l3`).
- `hd_l3` (1991, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `hd_l3` at `src/wpc/sims/wpc/full/hd.c:402` with machine module `hd`; no platform is declared (no reviewed profile covers that module yet).
- The driver source's named switch/solenoid symbols are carried as 60 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
