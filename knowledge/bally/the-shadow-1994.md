# The Shadow (Bally 1994)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.ts_lx5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `ts_lx5`, description "Shadow, The (LX-5)", manufacturer
  "Bally", catalog year "1995".
- OPDB record `G4jPX-M85YZ` (IPDB 2528) names this machine "The Shadow"
  (Bally, manufacture date 1994-11-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `ts_lx5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `ts_da2` (1994, Bally, clone of `ts_lx5`).
- `ts_da4` (1995, Bally, clone of `ts_lx5`).
- `ts_da6` (1995, Bally, clone of `ts_lx5`).
- `ts_df6` (1995, Bally, clone of `ts_lx5`).
- `ts_dh6` (1995, Bally, clone of `ts_lx5`).
- `ts_dm6` (1995, Bally, clone of `ts_lx5`).
- `ts_dx4` (1995, Bally, clone of `ts_lx5`).
- `ts_dx5` (1995, Bally, clone of `ts_lx5`).
- `ts_la2` (1994, Bally, clone of `ts_lx5`).
- `ts_la4` (1995, Bally, clone of `ts_lx5`).
- `ts_la6` (1995, Bally, clone of `ts_lx5`).
- `ts_lf4` (1995, Bally, clone of `ts_lx5`).
- `ts_lf6` (1995, Bally, clone of `ts_lx5`).
- `ts_lh6` (1995, Bally, clone of `ts_lx5`).
- `ts_lh6p` (1995, Bally, clone of `ts_lx5`).
- `ts_lm6` (1995, Bally, clone of `ts_lx5`).
- `ts_lx4` (1995, Bally, clone of `ts_lx5`).
- `ts_lx5` (1995, Bally).
- `ts_pa1` (1994, Bally, clone of `ts_lx5`).
- `ts_pa2` (1994, Bally, clone of `ts_lx5`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `ts_lx5` at `src/wpc/sims/wpc/prelim/ts.c:293` with machine module `wpc_mSecurityS`; the definition declares controller platform `pinmame.wpc-security` from it.
- The driver source's named switch/solenoid symbols are carried as 24 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
