# Black Knight (Williams 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.bk_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `bk_l4`, description "Black Knight (L-4)", manufacturer
  "Williams", catalog year "1980".
- OPDB record `GrO7w-M9R03` (IPDB 310) names this machine "Black Knight"
  (Williams, manufacture date 1980-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `bk_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bk_f4` (1980, Williams, clone of `bk_l4`).
- `bk_l2` (1980, Williams, clone of `bk_l4`).
- `bk_l3` (1980, Williams, clone of `bk_l4`).
- `bk_l4` (1980, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `bk_l4` at `src/wpc/sims/s7/full/bk.c:285` with machine module `s7_mS7S`; no platform is declared (no reviewed profile covers that module yet).
- The driver source's named switch/solenoid symbols are carried as 58 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
