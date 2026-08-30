# Pinball 2000: Star Wars Episode I (1.50) (Midway 2003)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.swep1_150` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `swep1_150`, description "Pinball 2000: Star Wars Episode I (1.50)", manufacturer
  "Midway", catalog year "2003".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `swep1_150`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `swep1_130` (1999, Midway, clone of `swep1_150`).
- `swep1_140` (2000, Midway, clone of `swep1_150`).
- `swep1_150` (2003, Midway).
- `swep1_200` (2025, Midway / mypinballs, clone of `swep1_150`).
- `swep1_201` (2025, Midway / mypinballs, clone of `swep1_150`).
- `swep1_210` (2025, Midway / mypinballs, clone of `swep1_150`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `swep1_150` at `src/wpc/p2k.c:1584` with machine module `p2k`; the definition declares controller platform `pinmame.p2k` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
