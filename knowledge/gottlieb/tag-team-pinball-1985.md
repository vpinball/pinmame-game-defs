# Tag-Team Pinball (Gottlieb 1985)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.tagteam` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `tagteam`, description "Tag-Team Pinball", manufacturer
  "Gottlieb", catalog year "1985".
- OPDB record `G5Yyo-ML3Wo` (IPDB 2489) names this machine "Tag-Team Pinball"
  (Gottlieb, manufacture date 1985-01-09); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `tagteam`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `tagteam` (1985, Gottlieb).
- `tagteam2` (1985, Gottlieb, clone of `tagteam`).
- `tagteamg` (1985, Gottlieb, clone of `tagteam`).
- `tagtem2f` (1985, Flipprojets, clone of `tagteam`).
- `tagtemfp` (1985, Flipprojets, clone of `tagteam`).
- `tagtmgfp` (1985, Flipprojets, clone of `tagteam`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 68 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
