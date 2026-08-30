# Tic-Tac-Strike (Shuffle) (L-2) (Williams 1986)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.tts_l2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tts_l2`, description "Tic-Tac-Strike (Shuffle) (L-2)", manufacturer
  "Williams", catalog year "1986".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `tts_l2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tts_l1` (1986, Williams, clone of `tts_l2`).
- `tts_l2` (1986, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `tts_l2` at `src/wpc/bowlgames.c:341` with machine module `s11_mS11S`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
