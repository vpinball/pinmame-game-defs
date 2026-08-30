# Millionaire (Williams 1987)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.milln_l3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `milln_l3`, description "Millionaire (L-3)", manufacturer
  "Williams", catalog year "1987".
- OPDB record `G5n38-M1rw3` (IPDB 1597) names this machine "Millionaire"
  (Williams, manufacture date 1987-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `milln_l3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `milln_l3` (1987, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `milln_l3` at `src/wpc/sims/s11/full/milln.c:390` with machine module `s11_mS11AS`; the definition declares controller platform `pinmame.system-11` from it.
- The driver source's named switch/solenoid symbols are carried as 76 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
