# S.A.M. III Board Tester (on-board) (Stern year unknown)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.sam_iii` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `sam_iii`, description "S.A.M. III Board Tester (on-board)", manufacturer
  "Stern", catalog year "19??".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `sam_iii`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `sam_iii` (19??, Stern).
- `sam_iv` (19??, Stern, clone of `sam_iii`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `sam_iii` at `src/wpc/stgames.c:1443` with machine module `by35_mST200`; no platform is declared (the drivers declare GEN_ASTRO, not the profile's generation).

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
