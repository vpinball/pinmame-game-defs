# Truck Stop (Bally 1988)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.trucksp3` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `trucksp3`, description "Truck Stop (P-3 Prototype)", manufacturer
  "Bally", catalog year "1988".
- OPDB record `G5Y6O-MLn90` (IPDB 2667) names this machine "Truck Stop"
  (Bally, manufacture date 1988-01-01); the selected identity rests on the reviewed
  machine-specific exception in `config/opdb-overrides.json`: PinMAME identifies the physical machine as a prototype; OPDB's sole Bally Truck Stop record uses the unsuffixed title for that prototype.
- The definition's driver list is exactly the clone tree PinMAME declares under `trucksp3`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `trucksp2` (1988, Bally, clone of `trucksp3`).
- `trucksp3` (1988, Bally).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 48 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
