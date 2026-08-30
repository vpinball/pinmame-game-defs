# Simpsons Kooky Carnival, The (Redemption) (V2.0) (Stern 2008)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.scarn200` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `scarn200`, description "Simpsons Kooky Carnival, The (Redemption) (V2.0)", manufacturer
  "Stern", catalog year "2008".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `scarn200`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `scarn103` (2006, Stern, clone of `scarn200`).
- `scarn105` (2006, Stern, clone of `scarn200`).
- `scarn200` (2008, Stern).
- `scarn9nj` (2006, Stern, clone of `scarn200`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `scarn200` at `src/wpc/sam.c:2579` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.
- The driver source's named switch/solenoid symbols are carried as 1 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
