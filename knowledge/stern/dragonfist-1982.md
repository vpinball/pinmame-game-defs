# Dragonfist (Stern 1982)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.dragfist` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `dragfist`, description "Dragonfist", manufacturer
  "Stern", catalog year "1982".
- OPDB record `GRQkJ-MDxpK` (IPDB 731) names this machine "Dragonfist"
  (Stern Electronics, manufacture date 1982-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `dragfist`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `dragfib2` (1982, Stern, clone of `dragfist`).
- `dragfifp` (1982, Stern, clone of `dragfist`).
- `dragfis14` (2021, Stern / Idleman, clone of `dragfist`).
- `dragfis15` (2023, Stern / slochar, clone of `dragfist`).
- `dragfis16` (2024, Stern / slochar, clone of `dragfist`).
- `dragfis17` (2026, Stern / slochar, clone of `dragfist`).
- `dragfis3` (2020, Stern / Idleman, clone of `dragfist`).
- `dragfis3b` (2020, Stern / Idleman, clone of `dragfist`).
- `dragfisb` (1982, Stern, clone of `dragfist`).
- `dragfist` (1982, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `dragfist` at `src/wpc/stgames.c:1236` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 27 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
