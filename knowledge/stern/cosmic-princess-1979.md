# Cosmic Princess (Stern 1979)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.princess` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `princess`, description "Cosmic Princess", manufacturer
  "Stern", catalog year "1979".
- OPDB record `G4d9B-MJk65` (IPDB 3967) names this machine "Cosmic Princess"
  (Allied Leisure, manufacture date 1979-01-08); the selected identity rests on the reviewed
  machine-specific exception in `config/opdb-overrides.json`: OPDB catalogs the physical machine under Allied Leisure; the cited serial-number record identifies its Australian production under license from Stern.
- The definition's driver list is exactly the clone tree PinMAME declares under `princess`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `princefp` (1979, Stern, clone of `princess`).
- `princesb` (2022, Stern / Quench, clone of `princess`).
- `princess` (1979, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `princess` at `src/wpc/stgames.c:318` with machine module `by35_mST100bs`; the definition declares controller platform `pinmame.stern-mpu200` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 18 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
