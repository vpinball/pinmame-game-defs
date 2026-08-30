# Evel Knievel (Bally 1977)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.evelknie` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `evelknie`, description "Evel Knievel", manufacturer
  "Bally", catalog year "1977".
- OPDB record `G59wx-MLnZ3` (IPDB 4499) names this machine "Evel Knievel"
  (Bally, manufacture date 1977-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `evelknie`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `evelknib` (2008, Bally / Oliver, clone of `evelknie`).
- `evelknic` (2019, Bally, clone of `evelknie`).
- `evelknie` (1977, Bally).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `evelknie` at `src/wpc/by35games.c:115` with machine module `by35_mBY17`; no platform is declared (no reviewed profile covers that module yet).
- The driver source's named switch/solenoid symbols are carried as 19 candidate devices in the definition.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 19 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
