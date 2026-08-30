# WPC Test Fixture: WPC-95 (1.2) (Bally 1996)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tf95_12` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tf95_12`, description "WPC Test Fixture: WPC-95 (1.2)", manufacturer
  "Bally", catalog year "1996".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `tf95_12`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tf95_12` (1996, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tf95_12` at `src/wpc/wpcgames.c:197` with machine module `wpc_m95S`; no platform is declared (the record is classified diagnostic or system software, outside the physical-machine attachment scope).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
