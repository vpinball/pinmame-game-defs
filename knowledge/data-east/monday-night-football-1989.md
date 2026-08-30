# Monday Night Football (Data East 1989)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.mnfb_c29` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `mnfb_c29`, description "Monday Night Football (2.9, 50cts)", manufacturer
  "Data East", catalog year "1989".
- OPDB record `G5zZ7-Mp474` (IPDB 1616) names this machine "Monday Night Football"
  (Data East, manufacture date 1989-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `mnfb_c29`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `mnfb_c27` (1989, Data East, clone of `mnfb_c29`).
- `mnfb_c29` (1989, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `mnfb_c29` at `src/wpc/degames.c:258` with machine module `de_mDEAS1`; the definition declares controller platform `pinmame.dataeast` from it.
- The driver source's named switch/solenoid symbols are carried as 93 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 93 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
