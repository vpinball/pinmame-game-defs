# Wheel of Fortune (Stern 2007)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.wof_500` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `wof_500`, description "Wheel of Fortune (V5.0)", manufacturer
  "Stern", catalog year "2007".
- OPDB record `G417d-MJkXV` (IPDB 5254) names this machine "Wheel of Fortune"
  (Stern, manufacture date 2007-10-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `wof_500`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `wof_100` (2007, Stern, clone of `wof_500`).
- `wof_200` (2007, Stern, clone of `wof_500`).
- `wof_200f` (2007, Stern, clone of `wof_500`).
- `wof_200g` (2007, Stern, clone of `wof_500`).
- `wof_200i` (2007, Stern, clone of `wof_500`).
- `wof_300` (2007, Stern, clone of `wof_500`).
- `wof_300f` (2007, Stern, clone of `wof_500`).
- `wof_300g` (2007, Stern, clone of `wof_500`).
- `wof_300i` (2007, Stern, clone of `wof_500`).
- `wof_300l` (2007, Stern, clone of `wof_500`).
- `wof_400` (2007, Stern, clone of `wof_500`).
- `wof_400f` (2007, Stern, clone of `wof_500`).
- `wof_400g` (2007, Stern, clone of `wof_500`).
- `wof_400i` (2007, Stern, clone of `wof_500`).
- `wof_401l` (2007, Stern, clone of `wof_500`).
- `wof_500` (2007, Stern).
- `wof_500f` (2007, Stern, clone of `wof_500`).
- `wof_500g` (2007, Stern, clone of `wof_500`).
- `wof_500i` (2007, Stern, clone of `wof_500`).
- `wof_500l` (2007, Stern, clone of `wof_500`).
- `wof_602h` (2009, Stern, clone of `wof_500`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `wof_500` at `src/wpc/sam.c:2878` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
