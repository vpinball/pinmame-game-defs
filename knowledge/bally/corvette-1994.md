# Corvette (Bally 1994)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.corv_21` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `corv_21`, description "Corvette (2.1)", manufacturer
  "Bally", catalog year "1994".
- OPDB record `GrjDz-MJKN6` (IPDB 570) names this machine "Corvette"
  (Bally, manufacture date 1994-01-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `corv_21`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `corv_21` (1994, Bally).
- `corv_dx1` (1994, Bally, clone of `corv_21`).
- `corv_f61` (1994, FreeWPC, clone of `corv_21`).
- `corv_la1` (1994, Bally, clone of `corv_21`).
- `corv_la2` (1994, Bally, clone of `corv_21`).
- `corv_lx1` (1994, Bally, clone of `corv_21`).
- `corv_lx2` (1994, Bally, clone of `corv_21`).
- `corv_px3` (1994, Bally, clone of `corv_21`).
- `corv_px4` (1994, Bally, clone of `corv_21`).
- `corv_px5` (1994, Bally, clone of `corv_21`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `corv_21` at `src/wpc/sims/wpc/prelim/corv.c:405` with machine module `wpc_mSecurityS`; the definition declares controller platform `pinmame.wpc-security` from it.
- The driver source's named switch/solenoid symbols are carried as 62 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
