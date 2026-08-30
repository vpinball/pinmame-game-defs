# Space Shuttle (Williams 1984)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.sshtl_l7` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `sshtl_l7`, description "Space Shuttle (L-7)", manufacturer
  "Williams", catalog year "1984".
- OPDB record `G4q3L-MKN50` (IPDB 2260) names this machine "Space Shuttle"
  (Williams, manufacture date 1984-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `sshtl_l7`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `sshtl_l3` (1984, Williams, clone of `sshtl_l7`).
- `sshtl_l7` (1984, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `sshtl_l7` at `src/wpc/s11games.c:80` with machine module `s9_mS9S`; the definition declares controller platform `pinmame.system-11` from it.
- The driver source's named switch/solenoid symbols are carried as 104 candidate devices in the definition.

## VPX script candidates (candidate)

- 3 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 104 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
