# Galaxy (Stern 1980)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.galaxy` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `galaxy`, description "Galaxy", manufacturer
  "Stern", catalog year "1980".
- OPDB record `GrdDB-ML8xK` (IPDB 980) names this machine "Galaxy"
  (Stern Electronics, manufacture date 1980-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `galaxy`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `galaxy` (1980, Stern).
- `galaxyb` (2003, Stern / Oliver, clone of `galaxy`).
- `galaxyc` (2023, Stern / Idleman, clone of `galaxy`).
- `galaxyfp` (1980, Stern, clone of `galaxy`).
- `galaxyps` (2011, Stern / Scott, clone of `galaxy`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `galaxy` at `src/wpc/stgames.c:541` with machine module `by35_mST200`; the definition declares controller platform `pinmame.stern-mpu200` from it.
- The driver source's named switch/solenoid symbols are carried as 37 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 37 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
