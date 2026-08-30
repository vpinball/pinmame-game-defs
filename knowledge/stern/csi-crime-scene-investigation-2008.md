# CSI: Crime Scene Investigation (Stern 2008)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.csi_240` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `csi_240`, description "CSI: Crime Scene Investigation (V2.4)", manufacturer
  "Stern", catalog year "2009".
- OPDB record `GRokz-ML8oW` (IPDB 5348) names this machine "CSI: Crime Scene Investigation"
  (Stern, manufacture date 2008-11-11); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `csi_240`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `csi_102` (2008, Stern, clone of `csi_240`).
- `csi_103` (2008, Stern, clone of `csi_240`).
- `csi_104` (2008, Stern, clone of `csi_240`).
- `csi_200` (2008, Stern, clone of `csi_240`).
- `csi_210` (2009, Stern, clone of `csi_240`).
- `csi_230` (2009, Stern, clone of `csi_240`).
- `csi_240` (2009, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `csi_240` at `src/wpc/sam.c:3051` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
