# Grand Lizard (Williams 1986)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.grand_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `grand_l4`, description "Grand Lizard (L-4)", manufacturer
  "Williams", catalog year "1986".
- OPDB record `G4XPZ-M7Zob` (IPDB 1070) names this machine "Grand Lizard"
  (Williams, manufacture date 1986-01-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `grand_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `grand_l1` (1986, Williams, clone of `grand_l4`).
- `grand_l3` (1986, Williams, clone of `grand_l4`).
- `grand_l4` (1986, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `grand_l4` at `src/wpc/s11games.c:214` with machine module `s11_mS11XS`; the definition declares controller platform `pinmame.system-11` from it.

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 37 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
