# Star Trax (Domestic Prototype) (Williams 1990)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.strax_p7` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `strax_p7`, description "Star Trax (Domestic Prototype)", manufacturer
  "Williams", catalog year "1990".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `strax_p7`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `strax_p7` (1990, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `strax_p7` at `src/wpc/s11games.c:1586` with machine module `s11_mS11BS`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
