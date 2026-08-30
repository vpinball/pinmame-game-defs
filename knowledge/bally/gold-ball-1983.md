# Gold Ball (Bally 1983)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.goldball` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `goldball`, description "Gold Ball", manufacturer
  "Bally", catalog year "1983".
- OPDB record `Grjlx-MQkz3` (IPDB 1024) names this machine "Gold Ball"
  (Bally, manufacture date 1983-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `goldball`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `goldbalb` (2004, Bally / Oliver, clone of `goldball`).
- `goldbalc` (2005, Bally / Oliver, clone of `goldball`).
- `goldball` (1983, Bally).
- `goldbaln` (1983, Bally, clone of `goldball`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `goldball` at `src/wpc/by35games.c:1697` with machine module `by35_mBY35_51S`; the definition declares controller platform `pinmame.by35` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 34 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
