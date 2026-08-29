# Cyclone (Williams 1988)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.cycln_l5` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `cycln_l5`, description "Cyclone (L-5)", manufacturer
  "Williams", catalog year "1988".
- OPDB record `G4O2b-MJpn4` (IPDB 617) names this machine "Cyclone"
  (Williams, manufacture date 1988-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `cycln_l5`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `cycln_l1` (1988, Williams, clone of `cycln_l5`).
- `cycln_l4` (1988, Williams, clone of `cycln_l5`).
- `cycln_l5` (1988, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `cycln_l5` at `src/wpc/s11games.c:512` with machine module `s11_mS11BS`; the definition declares controller platform `pinmame.system-11` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 54 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
