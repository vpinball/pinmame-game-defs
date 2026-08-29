# Demolition Man (Williams 1994)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.dm_lx4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `dm_lx4`, description "Demolition Man (LX-4)", manufacturer
  "Williams", catalog year "1994".
- OPDB record `G5bv3-MLW68` (IPDB 662) names this machine "Demolition Man"
  (Williams, manufacture date 1994-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `dm_lx4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `dm_da1` (1994, Williams, clone of `dm_lx4`).
- `dm_dh5` (1995, Williams, clone of `dm_lx4`).
- `dm_dh5b` (1995, Williams, clone of `dm_lx4`).
- `dm_dt099` (2014, FreeWPC, clone of `dm_lx4`).
- `dm_dt101` (2014, FreeWPC, clone of `dm_lx4`).
- `dm_dx3` (1994, Williams, clone of `dm_lx4`).
- `dm_dx4` (1994, Williams, clone of `dm_lx4`).
- `dm_h5` (1995, Williams, clone of `dm_lx4`).
- `dm_h5b` (1995, Williams, clone of `dm_lx4`).
- `dm_h6` (1995, Williams, clone of `dm_lx4`).
- `dm_h6b` (1995, Williams, clone of `dm_lx4`).
- `dm_h6c` (2019, Williams, clone of `dm_lx4`).
- `dm_la1` (1994, Williams, clone of `dm_lx4`).
- `dm_lx3` (1994, Williams, clone of `dm_lx4`).
- `dm_lx4` (1994, Williams).
- `dm_lx4c` (2020, Williams, clone of `dm_lx4`).
- `dm_pa2` (1994, Williams, clone of `dm_lx4`).
- `dm_pa3` (1994, Williams, clone of `dm_lx4`).
- `dm_px5` (1994, Williams, clone of `dm_lx4`).
- `dm_px6` (1994, Williams, clone of `dm_lx4`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `dm_lx4` at `src/wpc/sims/wpc/full/dm.c:519` with machine module `wpc_mDCSS`; the definition declares controller platform `pinmame.wpc-dcs` from it.
- The driver source's named switch/solenoid symbols are carried as 63 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
