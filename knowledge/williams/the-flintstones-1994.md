# The Flintstones (Williams 1994)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.fs_lx5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `fs_lx5`, description "Flintstones, The (LX-5)", manufacturer
  "Williams", catalog year "1994".
- OPDB record `GRK95-MQ674` (IPDB 888) names this machine "The Flintstones"
  (Williams, manufacture date 1994-07-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `fs_lx5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `fs_dx2` (1994, Williams, clone of `fs_lx5`).
- `fs_dx4` (1994, Williams, clone of `fs_lx5`).
- `fs_dx5` (1994, Williams, clone of `fs_lx5`).
- `fs_la5` (1994, Williams, clone of `fs_lx5`).
- `fs_lx2` (1994, Williams, clone of `fs_lx5`).
- `fs_lx3` (1994, Williams, clone of `fs_lx5`).
- `fs_lx4` (1994, Williams, clone of `fs_lx5`).
- `fs_lx5` (1994, Williams).
- `fs_sp2` (1994, Williams, clone of `fs_lx5`).
- `fs_sp2d` (1994, Williams, clone of `fs_lx5`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `fs_lx5` at `src/wpc/sims/wpc/prelim/fs.c:284` with machine module `wpc_mSecurityS`; the definition declares controller platform `pinmame.wpc-security` from it.
- The driver source's named switch/solenoid symbols are carried as 29 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
