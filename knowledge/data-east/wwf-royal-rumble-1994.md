# WWF Royal Rumble (Data East 1994)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.wwfr_106` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `wwfr_106`, description "WWF Royal Rumble (1.06)", manufacturer
  "Data East", catalog year "1994".
- OPDB record `G57y6-MLej6` (IPDB 2820) names this machine "WWF Royal Rumble"
  (Data East, manufacture date 1994-05-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `wwfr_106`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `wwfr_103` (1994, Data East, clone of `wwfr_106`).
- `wwfr_103f` (1994, Data East, clone of `wwfr_106`).
- `wwfr_106` (1994, Data East).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `wwfr_106` at `src/wpc/degames.c:1248` with machine module `de_mDEDMD32S2A`; the definition declares controller platform `pinmame.dataeast` from it.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 107 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.
## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
