# Orbitor 1 (Stern 1982)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.orbitor1` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `orbitor1`, description "Orbitor 1", manufacturer
  "Stern", catalog year "1982".
- OPDB record `Grx7Q-Mp45k` (IPDB 1725) names this machine "Orbitor 1"
  (Stern Electronics, manufacture date 1982-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `orbitor1`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `orbitofp` (1982, Stern, clone of `orbitor1`).
- `orbitor1` (1982, Stern).
- `orbitora` (1982, Stern, clone of `orbitor1`).
- `orbitorb` (1982, Stern, clone of `orbitor1`).
- `orbitorc` (1982, Stern, clone of `orbitor1`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `orbitor1` at `src/wpc/stgames.c:1341` with machine module `by35_mST200v`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
