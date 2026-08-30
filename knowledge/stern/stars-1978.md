# Stars (Stern 1978)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.stars` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `stars`, description "Stars", manufacturer
  "Stern", catalog year "1978".
- OPDB record `GrXEW-MDEwr` (IPDB 2366) names this machine "Stars"
  (Stern Electronics, manufacture date 1978-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `stars`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `stars` (1978, Stern).
- `starsb` (2024, Stern / slochar, clone of `stars`).
- `starsb7` (2025, Stern / slochar, clone of `stars`).
- `starsfp` (1978, Stern, clone of `stars`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `stars` at `src/wpc/stgames.c:100` with machine module `by35_mST100`; no platform is declared (no reviewed profile covers that module yet).
- The driver source's named switch/solenoid symbols are carried as 55 candidate devices in the definition.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 55 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
