# Nugent (Stern 1978)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.nugent` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `nugent`, description "Nugent", manufacturer
  "Stern", catalog year "1978".
- OPDB record `G5VWL-MLRjl` (IPDB 1687) names this machine "Nugent"
  (Stern Electronics, manufacture date 1978-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `nugent`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `nugent` (1978, Stern).
- `nugentfp` (1978, Stern, clone of `nugent`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `nugent` at `src/wpc/stgames.c:193` with machine module `by35_mST100s`; no reviewed profile covers that module yet, so no platform is declared.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 24 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
