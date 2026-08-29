# Hurricane (Williams 1991)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.hurr_l2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `hurr_l2`, description "Hurricane (L-2)", manufacturer
  "Williams", catalog year "1991".
- OPDB record `GrX09-M85bb` (IPDB 1257) names this machine "Hurricane"
  (Williams, manufacture date 1991-08-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `hurr_l2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `hurr_d2` (1991, Williams, clone of `hurr_l2`).
- `hurr_l2` (1991, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `hurr_l2` at `src/wpc/sims/wpc/full/hurr.c:342` with machine module `wpc_mFliptronS`; the definition declares controller platform `pinmame.wpc-fliptronic` from it.
- The driver source's named switch/solenoid symbols are carried as 47 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
