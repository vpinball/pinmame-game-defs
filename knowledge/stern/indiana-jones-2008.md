# Indiana Jones (Stern 2008)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.ij4_210` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `ij4_210`, description "Indiana Jones (V2.1)", manufacturer
  "Stern", catalog year "2009".
- OPDB record `G4e1d-MJ5Bj` (IPDB 5306) names this machine "Indiana Jones"
  (Stern, manufacture date 2008-05-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `ij4_210`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `ij4_113` (2008, Stern, clone of `ij4_210`).
- `ij4_113f` (2008, Stern, clone of `ij4_210`).
- `ij4_113g` (2008, Stern, clone of `ij4_210`).
- `ij4_113i` (2008, Stern, clone of `ij4_210`).
- `ij4_113l` (2008, Stern, clone of `ij4_210`).
- `ij4_114` (2008, Stern, clone of `ij4_210`).
- `ij4_114f` (2008, Stern, clone of `ij4_210`).
- `ij4_114g` (2008, Stern, clone of `ij4_210`).
- `ij4_114i` (2008, Stern, clone of `ij4_210`).
- `ij4_114l` (2008, Stern, clone of `ij4_210`).
- `ij4_116` (2008, Stern, clone of `ij4_210`).
- `ij4_116f` (2008, Stern, clone of `ij4_210`).
- `ij4_116g` (2008, Stern, clone of `ij4_210`).
- `ij4_116i` (2008, Stern, clone of `ij4_210`).
- `ij4_116l` (2008, Stern, clone of `ij4_210`).
- `ij4_210` (2009, Stern).
- `ij4_210f` (2009, Stern, clone of `ij4_210`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `ij4_210` at `src/wpc/sam.c:2980` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
