# Indianapolis 500 (Bally 1995)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.i500_11r` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `i500_11r`, description "Indianapolis 500 (1.1R)", manufacturer
  "Bally", catalog year "1995".
- OPDB record `Gr8l3-MDWr0` (IPDB 2853) names this machine "Indianapolis 500"
  (Bally, manufacture date 1995-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `i500_11r`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `i500_10r` (1995, Bally, clone of `i500_11r`).
- `i500_11b` (1995, Bally, clone of `i500_11r`).
- `i500_11r` (1995, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `i500_11r` at `src/wpc/sims/wpc/prelim/i500.c:303` with machine module `wpc_mSecurityS`; the definition declares controller platform `pinmame.wpc-security` from it.
- The driver source's named switch/solenoid symbols are carried as 29 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
