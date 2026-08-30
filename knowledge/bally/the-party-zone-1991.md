# The Party Zone (Bally 1991)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.pz_f4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pz_f4`, description "Party Zone, The (F-4 Fliptronic)", manufacturer
  "Bally", catalog year "1991".
- OPDB record `G5oBw-ML3Kw` (IPDB 1764) names this machine "The Party Zone"
  (Bally, manufacture date 1991-01-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pz_f4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pz_d1` (1991, Bally, clone of `pz_f4`).
- `pz_d2` (1991, Bally, clone of `pz_f4`).
- `pz_d3` (1991, Bally, clone of `pz_f4`).
- `pz_f4` (1991, Bally).
- `pz_f4pfx` (2018, Zen Studios, clone of `pz_f4`).
- `pz_f5` (1991, Bally, clone of `pz_f4`).
- `pz_l1` (1991, Bally, clone of `pz_f4`).
- `pz_l2` (1991, Bally, clone of `pz_f4`).
- `pz_l3` (1991, Bally, clone of `pz_f4`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pz_f4` at `src/wpc/sims/wpc/full/pz.c:594` with machine module `wpc_mFliptronS`; the definition declares controller platform `pinmame.wpc-fliptronic` from it.
- The driver source's named switch/solenoid symbols are carried as 67 candidate devices in the definition.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
