# Addams Family Values (Coin Dropper) (L-4) (Williams 1993)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.afv_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `afv_l4`, description "Addams Family Values (Coin Dropper) (L-4)", manufacturer
  "Williams", catalog year "1993".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `afv_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `afv_d4` (1993, Williams, clone of `afv_l4`).
- `afv_l4` (1993, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `afv_l4` at `src/wpc/bowlgames.c:624` with machine module `wpc_mDCSS`; the definition declares controller platform `pinmame.wpc-dcs` from it.
- The driver source's named switch/solenoid symbols are carried as 1 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
