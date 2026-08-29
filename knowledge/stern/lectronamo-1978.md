# Lectronamo (Stern 1978)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.lectrono` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `lectrono`, description "Lectronamo", manufacturer
  "Stern", catalog year "1978".
- OPDB record `GRWd2-MQ4Ye` (IPDB 1429) names this machine "Lectronamo"
  (Stern Electronics, manufacture date 1978-01-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `lectrono`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `lectrofp` (1978, Stern, clone of `lectrono`).
- `lectrono` (1978, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `lectrono` at `src/wpc/stgames.c:152` with machine module `by35_mST100s`; no reviewed profile covers that module yet, so no platform is declared.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
