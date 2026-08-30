# Safe Cracker (Bally 1996)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.sc_18s11` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `sc_18s11`, description "Safe Cracker (1.8 / S1.1)", manufacturer
  "Bally", catalog year "1998".
- OPDB record `GRBxq-MJpOP` (IPDB 3782) names this machine "Safe Cracker"
  (Bally, manufacture date 1996-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `sc_18s11`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `sc_091` (1996, Bally, clone of `sc_18s11`).
- `sc_10` (1996, Bally, clone of `sc_18s11`).
- `sc_14` (1996, Bally, clone of `sc_18s11`).
- `sc_17` (1996, Bally, clone of `sc_18s11`).
- `sc_17n` (1996, Bally, clone of `sc_18s11`).
- `sc_18n11` (1998, Bally, clone of `sc_18s11`).
- `sc_18ns2` (1998, Bally, clone of `sc_18s11`).
- `sc_18pfx` (2019, Zen Studios, clone of `sc_18s11`).
- `sc_18s11` (1998, Bally).
- `sc_18s2` (1998, Bally, clone of `sc_18s11`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `sc_18s11` at `src/wpc/sims/wpc/prelim/sc.c:288` with machine module `wpc_m95S`; the definition declares controller platform `pinmame.wpc-95` from it.
- The driver source's named switch/solenoid symbols are carried as 26 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
