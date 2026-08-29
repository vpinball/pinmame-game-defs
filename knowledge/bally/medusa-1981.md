# Medusa (Bally 1981)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.medusa` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `medusa`, description "Medusa", manufacturer
  "Bally", catalog year "1981".
- OPDB record `G4xXQ-MDWW1` (IPDB 1565) names this machine "Medusa"
  (Bally, manufacture date 1981-02-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `medusa`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `medusa` (1981, Bally).
- `medusaa` (2004, Bally / Oliver, clone of `medusa`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `medusa` at `src/wpc/by35games.c:1306` with machine module `by35_mBY35_61BS`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 3 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 117 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
