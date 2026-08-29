# TX-Sector (Gottlieb 1988)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.txsector` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `txsector`, description "TX-Sector", manufacturer
  "Gottlieb", catalog year "1988".
- OPDB record `GRLzj-MJPYK` (IPDB 2699) names this machine "TX-Sector"
  (Gottlieb, manufacture date 1988-03-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `txsector`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `txsecffp` (1988, Flipprojets, clone of `txsector`).
- `txsecgfp` (1988, Flipprojets, clone of `txsector`).
- `txsectfp` (1988, Flipprojets, clone of `txsector`).
- `txsector` (1988, Gottlieb).
- `txsectrf` (1988, Gottlieb, clone of `txsector`).
- `txsectrg` (1988, Gottlieb, clone of `txsector`).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
