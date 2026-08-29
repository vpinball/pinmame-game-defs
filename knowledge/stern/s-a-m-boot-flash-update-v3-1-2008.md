# S.A.M. Boot Flash Update (V3.1) (Stern 2008)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.sam1_flashb_0310` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `sam1_flashb_0310`, description "S.A.M. Boot Flash Update (V3.1)", manufacturer
  "Stern", catalog year "2008".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `sam1_flashb_0310`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `sam1_flashb_0102` (2006, Stern, clone of `sam1_flashb_0310`).
- `sam1_flashb_0106` (2006, Stern, clone of `sam1_flashb_0310`).
- `sam1_flashb_0210` (2007, Stern, clone of `sam1_flashb_0310`).
- `sam1_flashb_0230` (2007, Stern, clone of `sam1_flashb_0310`).
- `sam1_flashb_0310` (2008, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `sam1_flashb_0310` at `src/wpc/sam.c:2439` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.
- The driver source's named switch/solenoid symbols are carried as 1 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
