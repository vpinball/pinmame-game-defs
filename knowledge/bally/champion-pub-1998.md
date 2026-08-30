# Champion Pub (Bally 1998)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.cp_16` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `cp_16`, description "Champion Pub, The (1.6)", manufacturer
  "Bally", catalog year "1998".
- OPDB record `G42k0-MQ6w9` (IPDB 4358) names this machine "Champion Pub"
  (Bally, manufacture date 1998-01-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `cp_16`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `cp_15` (1998, Bally, clone of `cp_16`).
- `cp_16` (1998, Bally).
- `cp_16pfx` (2019, Zen Studios, clone of `cp_16`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `cp_16` at `src/wpc/sims/wpc/prelim/cp.c:271` with machine module `wpc_m95S`; the definition declares controller platform `pinmame.wpc-95` from it.
- The driver source's named switch/solenoid symbols are carried as 22 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
