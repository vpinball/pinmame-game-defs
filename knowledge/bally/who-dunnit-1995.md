# WHO dunnit (Bally 1995)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.wd_12` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `wd_12`, description "WHO Dunnit (1.2)", manufacturer
  "Bally", catalog year "1995".
- OPDB record `G50kj-MDqpv` (IPDB 3685) names this machine "WHO dunnit"
  (Bally, manufacture date 1995-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `wd_12`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `wd_03r` (1995, Bally, clone of `wd_12`).
- `wd_048r` (1995, Bally, clone of `wd_12`).
- `wd_10f` (1995, Bally, clone of `wd_12`).
- `wd_10g` (1995, Bally, clone of `wd_12`).
- `wd_10r` (1995, Bally, clone of `wd_12`).
- `wd_11` (1995, Bally, clone of `wd_12`).
- `wd_12` (1995, Bally).
- `wd_12g` (1995, Bally, clone of `wd_12`).
- `wd_12gp` (2020, Bally, clone of `wd_12`).
- `wd_12p` (2020, Bally, clone of `wd_12`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `wd_12` at `src/wpc/sims/wpc/prelim/wd.c:327` with machine module `wpc_m95DCSS`; the definition declares controller platform `pinmame.wpc-95` from it.
- The driver source's named switch/solenoid symbols are carried as 27 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
