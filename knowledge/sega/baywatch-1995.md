# Baywatch (Sega 1995)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.baywatch` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `baywatch`, description "Baywatch (4.00)", manufacturer
  "Sega", catalog year "1995".
- OPDB record `Grxvy-M4oZj` (IPDB 2848) names this machine "Baywatch"
  (Sega, manufacture date 1995-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `baywatch`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bay_401` (2017, Sega, clone of `baywatch`).
- `bay_402` (2025, Sega, clone of `baywatch`).
- `bay_d300` (1995, Sega, clone of `baywatch`).
- `bay_d400` (1995, Sega, clone of `baywatch`).
- `bay_e400` (1995, Sega, clone of `baywatch`).
- `bay_f201` (1995, Sega, clone of `baywatch`).
- `bay_g300` (1995, Sega, clone of `baywatch`).
- `baywatch` (1995, Sega).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 102 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
