# Nascar (Stern 2005)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.nascar` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `nascar`, description "NASCAR (4.50)", manufacturer
  "Stern", catalog year "2006".
- OPDB record `G5YWX-MQ4VW` (IPDB 5093) names this machine "Nascar"
  (Stern, manufacture date 2005-06-29); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `nascar`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `nas301` (2005, Stern, clone of `nascar`).
- `nas301l` (2005, Stern, clone of `nascar`).
- `nas340` (2005, Stern, clone of `nascar`).
- `nas340l` (2005, Stern, clone of `nascar`).
- `nas350` (2005, Stern, clone of `nascar`).
- `nas350l` (2005, Stern, clone of `nascar`).
- `nas352` (2005, Stern, clone of `nascar`).
- `nas352l` (2005, Stern, clone of `nascar`).
- `nas400` (2005, Stern, clone of `nascar`).
- `nas400l` (2005, Stern, clone of `nascar`).
- `nascar` (2006, Stern).
- `nascarl` (2006, Stern, clone of `nascar`).

## VPX script candidates (candidate)

- 2 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 121 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
