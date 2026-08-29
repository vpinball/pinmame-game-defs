# Dirty Harry (Williams 1995)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.dh_lx2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `dh_lx2`, description "Dirty Harry (LX-2)", manufacturer
  "Williams", catalog year "1995".
- OPDB record `GrJ2Z-M61Xd` (IPDB 684) names this machine "Dirty Harry"
  (Williams, manufacture date 1995-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `dh_lx2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `dh_dx2` (1995, Williams, clone of `dh_lx2`).
- `dh_lf2` (1995, Williams, clone of `dh_lx2`).
- `dh_lx2` (1995, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `dh_lx2` at `src/wpc/sims/wpc/prelim/dh.c:277` with machine module `wpc_mSecurityS`; the definition declares controller platform `pinmame.wpc-security` from it.
- The driver source's named switch/solenoid symbols are carried as 29 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
