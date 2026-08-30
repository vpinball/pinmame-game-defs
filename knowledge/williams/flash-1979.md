# Flash (Williams 1979)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.flash_l1` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `flash_l1`, description "Flash (Sys.6 L-1)", manufacturer
  "Williams", catalog year "1978".
- OPDB record `Grypn-MQdbe` (IPDB 871) names this machine "Flash"
  (Williams, manufacture date 1979-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `flash_l1`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `flash_l1` (1978, Williams).
- `flash_l1ff` (1978, Williams, clone of `flash_l1`).
- `flash_l2` (1978, Williams, clone of `flash_l1`).
- `flash_t1` (1978, Williams, clone of `flash_l1`).
- `flash_t1ff` (1978, Williams, clone of `flash_l1`).

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 38 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
