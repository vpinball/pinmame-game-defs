# Super Mario Bros. (Gottlieb 1992)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.smb` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `smb`, description "Super Mario Bros.", manufacturer
  "Gottlieb", catalog year "1992".
- OPDB record `GRBzQ-MLO1j` (IPDB 2435) names this machine "Super Mario Bros."
  (Gottlieb, manufacture date 1992-04-25); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `smb`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `smb` (1992, Gottlieb).
- `smb1` (1992, Gottlieb, clone of `smb`).
- `smb2` (1992, Gottlieb, clone of `smb`).
- `smb3` (1992, Gottlieb, clone of `smb`).
- `smbv1` (1992, Gottlieb / Vifico, clone of `smb`).
- `smbv2` (1992, Gottlieb / Vifico, clone of `smb`).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 145 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
