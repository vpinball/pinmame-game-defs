# Trident (Stern 1979)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.trident` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `trident`, description "Trident", manufacturer
  "Stern", catalog year "1979".
- OPDB record `GR0KD-MJpnr` (IPDB 2644) names this machine "Trident"
  (Stern Electronics, manufacture date 1979-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `trident`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tridenfp` (1979, Stern, clone of `trident`).
- `trident` (1979, Stern).
- `tridenta` (1979, Stern, clone of `trident`).
- `tridentb` (2009, Stern / Idleman, clone of `trident`).
- `tridentc` (2022, Stern / Quench, clone of `trident`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `trident` at `src/wpc/stgames.c:235` with machine module `by35_mST100bs`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
