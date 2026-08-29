# Elvis (Stern 2004)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.elvis` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `elvis`, description "Elvis (5.00)", manufacturer
  "Stern", catalog year "2004".
- OPDB record `G4qbX-MJw5r` (IPDB 4983) names this machine "Elvis"
  (Stern, manufacture date 2004-08-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `elvis`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `elv100` (2004, Stern, clone of `elvis`).
- `elv302` (2004, Stern, clone of `elvis`).
- `elv302f` (2004, Stern, clone of `elvis`).
- `elv302g` (2004, Stern, clone of `elvis`).
- `elv302i` (2004, Stern, clone of `elvis`).
- `elv302l` (2004, Stern, clone of `elvis`).
- `elv303` (2004, Stern, clone of `elvis`).
- `elv303f` (2004, Stern, clone of `elvis`).
- `elv303g` (2004, Stern, clone of `elvis`).
- `elv303i` (2004, Stern, clone of `elvis`).
- `elv303l` (2004, Stern, clone of `elvis`).
- `elv400` (2004, Stern, clone of `elvis`).
- `elv400f` (2004, Stern, clone of `elvis`).
- `elv400g` (2004, Stern, clone of `elvis`).
- `elv400i` (2004, Stern, clone of `elvis`).
- `elv400l` (2004, Stern, clone of `elvis`).
- `elvis` (2004, Stern).
- `elvisf` (2004, Stern, clone of `elvis`).
- `elvisg` (2004, Stern, clone of `elvis`).
- `elvisi` (2004, Stern, clone of `elvis`).
- `elvisl` (2004, Stern, clone of `elvis`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `elvis` at `src/wpc/sims/se/prelim/elvis.c:426` with machine module `de_mSES3`; no reviewed profile covers that module yet, so no platform is declared.
- The driver source's named switch/solenoid symbols are carried as 19 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
