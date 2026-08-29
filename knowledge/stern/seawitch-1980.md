# Seawitch (Stern 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.seawitch` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `seawitch`, description "Seawitch", manufacturer
  "Stern", catalog year "1980".
- OPDB record `GR6kB-MDz81` (IPDB 2089) names this machine "Seawitch"
  (Stern Electronics, manufacture date 1980-05-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `seawitch`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `seawitch` (1980, Stern).
- `seawitcha` (2021, Stern / Idleman, clone of `seawitch`).
- `seawitchb` (2021, Stern / Idleman, clone of `seawitch`).
- `seawitchc` (2021, Stern / Idleman, clone of `seawitch`).
- `seawitchd` (2021, Stern / Idleman, clone of `seawitch`).
- `seawitche` (2023, Stern / slochar, clone of `seawitch`).
- `seawitchf` (2024, Stern / slochar, clone of `seawitch`).
- `seawitfp` (1980, Stern, clone of `seawitch`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `seawitch` at `src/wpc/stgames.c:710` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
