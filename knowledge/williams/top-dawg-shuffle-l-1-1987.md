# Top Dawg (Shuffle) (L-1) (Williams 1987)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.tdawg_l1` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tdawg_l1`, description "Top Dawg (Shuffle) (L-1)", manufacturer
  "Williams", catalog year "1987".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `tdawg_l1`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tdawg_l1` (1987, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tdawg_l1` at `src/wpc/bowlgames.c:369` with machine module `s11_mS11S`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
