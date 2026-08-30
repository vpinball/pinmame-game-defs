# Monopoly (Stern 2001)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.monopoly` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `monopoly`, description "Monopoly (3.20)", manufacturer
  "Stern", catalog year "2001".
- OPDB record `G48w3-Mq1Zk` (IPDB 4505) names this machine "Monopoly"
  (Stern, manufacture date 2001-09-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `monopoly`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `monoi251` (2002, Stern, clone of `monopoly`).
- `monop233` (2002, Stern, clone of `monopoly`).
- `monop251` (2002, Stern, clone of `monopoly`).
- `monop301` (2002, Stern, clone of `monopoly`).
- `monopole` (2002, Stern, clone of `monopoly`).
- `monopolf` (2002, Stern, clone of `monopoly`).
- `monopolg` (2002, Stern, clone of `monopoly`).
- `monopoli` (2002, Stern, clone of `monopoly`).
- `monopoll` (2002, Stern, clone of `monopoly`).
- `monopoly` (2001, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `monopoly` at `src/wpc/sims/se/prelim/monopoly.c:441` with machine module `de_mSES1`; no platform is declared (the de_mSES1 module serves several manufacturers and this record's catalog manufacturer (Stern) is not Data East).
- The driver source's named switch/solenoid symbols are carried as 23 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
