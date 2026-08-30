# Embryon (Bally 1981)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.embryon` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `embryon`, description "Embryon", manufacturer
  "Bally", catalog year "1981".
- OPDB record `G4qk7-MNEjx` (IPDB 783) names this machine "Embryon"
  (Bally, manufacture date 1981-06-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `embryon`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `embryon` (1981, Bally).
- `embryona` (2004, Bally / Oliver, clone of `embryon`).
- `embryonb` (2002, Bally / Oliver, clone of `embryon`).
- `embryonc` (2004, Bally / Oliver, clone of `embryon`).
- `embryond` (2004, Bally / Oliver, clone of `embryon`).
- `embryone` (2011, Bally, clone of `embryon`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `embryon` at `src/wpc/by35games.c:1214` with machine module `by35_mBY35_61BS`; the definition declares controller platform `pinmame.by35` from it.
- The driver source's named switch/solenoid symbols are carried as 31 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 31 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
