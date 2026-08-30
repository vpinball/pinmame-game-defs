# WPC Test Fixture: Alphanumeric (L-3) (Bally 1990)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tfa_13` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tfa_13`, description "WPC Test Fixture: Alphanumeric (L-3)", manufacturer
  "Bally", catalog year "1990".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `tfa_13`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tfa_13` (1990, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tfa_13` at `src/wpc/wpcgames.c:217` with machine module `wpc_mAlpha`; no platform is declared (the record is classified diagnostic or system software, outside the physical-machine attachment scope).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
