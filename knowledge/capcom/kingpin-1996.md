# Kingpin (Capcom 1996)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.kpb105` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `kpb105`, description "Kingpin (Beta 1.05)", manufacturer
  "Capcom", catalog year "1996".
- OPDB record `G48od-MJNnn` (IPDB 4000) names this machine "Kingpin"
  (Capcom, manufacture date 1996-12-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `kpb105`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `kpb105` (1996, Capcom).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `kpb105` at `src/wpc/capgames.c:351` with machine module `cc2`; the definition declares controller platform `pinmame.capcom` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 164 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
