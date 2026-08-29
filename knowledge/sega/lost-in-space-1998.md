# Lost In Space (Sega 1998)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.lostspc` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `lostspc`, description "Lost in Space (1.01, Display 1.02)", manufacturer
  "Sega", catalog year "1998".
- OPDB record `GR91x-MLBZE` (IPDB 4442) names this machine "Lost In Space"
  (Sega, manufacture date 1998-05-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `lostspc`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `lostspc` (1998, Sega).
- `lostspc1` (1998, Sega, clone of `lostspc`).
- `lostspcf` (1998, Sega, clone of `lostspc`).
- `lostspcg` (1998, Sega, clone of `lostspc`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 98 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
