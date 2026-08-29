# Elvira and the Party Monsters (Bally 1989)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.eatpm_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `eatpm_l4`, description "Elvira and the Party Monsters (LA-4)", manufacturer
  "Bally", catalog year "1989".
- OPDB record `Grlxp-MVKBW` (IPDB 782) names this machine "Elvira and the Party Monsters"
  (Bally, manufacture date 1989-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `eatpm_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `eatpm_3g` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_4g` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_4u` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_f1` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_l1` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_l2` (1989, Bally, clone of `eatpm_l4`).
- `eatpm_l4` (1989, Bally).
- `eatpm_p7` (1989, Bally, clone of `eatpm_l4`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `eatpm_l4` at `src/wpc/sims/s11/prelim/eatpm.c:281` with machine module `elvira`; no reviewed profile covers that module yet, so no platform is declared.
- The driver source's named switch/solenoid symbols are carried as 58 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
