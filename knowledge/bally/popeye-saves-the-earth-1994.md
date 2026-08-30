# Popeye Saves the Earth (Bally 1994)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.pop_lx5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pop_lx5`, description "Popeye Saves The Earth (LX-5)", manufacturer
  "Bally", catalog year "1994".
- OPDB record `GR0lW-MJPVV` (IPDB 1851) names this machine "Popeye Saves the Earth"
  (Bally, manufacture date 1994-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pop_lx5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pop_dx5` (1994, Bally, clone of `pop_lx5`).
- `pop_la4` (1994, Bally, clone of `pop_lx5`).
- `pop_lx4` (1994, Bally, clone of `pop_lx5`).
- `pop_lx5` (1994, Bally).
- `pop_pa3` (1993, Bally, clone of `pop_lx5`).
- `pop_pa4` (1993, Bally, clone of `pop_lx5`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pop_lx5` at `src/wpc/sims/wpc/prelim/pop.c:280` with machine module `wpc_mDCSS`; the definition declares controller platform `pinmame.wpc-dcs` from it.
- The driver source's named switch/solenoid symbols are carried as 31 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
