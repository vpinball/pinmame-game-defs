# Harley Davidson (Stern 1999)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.harl_a40` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `harl_a40`, description "Harley-Davidson (Stern, 4.00)", manufacturer
  "Stern", catalog year "2004".
- OPDB record `G56lO-MDXpW` (IPDB 4455) names this machine "Harley Davidson"
  (Stern, manufacture date 1999-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `harl_a40`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `harl_a18` (2003, Stern, clone of `harl_a40`).
- `harl_a30` (2004, Stern, clone of `harl_a40`).
- `harl_a40` (2004, Stern).
- `harl_f18` (2003, Stern, clone of `harl_a40`).
- `harl_f30` (2004, Stern, clone of `harl_a40`).
- `harl_f40` (2004, Stern, clone of `harl_a40`).
- `harl_g18` (2003, Stern, clone of `harl_a40`).
- `harl_g30` (2004, Stern, clone of `harl_a40`).
- `harl_g40` (2004, Stern, clone of `harl_a40`).
- `harl_i18` (2003, Stern, clone of `harl_a40`).
- `harl_i30` (2004, Stern, clone of `harl_a40`).
- `harl_i40` (2004, Stern, clone of `harl_a40`).
- `harl_l18` (2003, Stern, clone of `harl_a40`).
- `harl_l30` (2004, Stern, clone of `harl_a40`).
- `harl_l40` (2004, Stern, clone of `harl_a40`).

## VPX script candidates (candidate)

- 3 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 46 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
