# Dracula (Stern 1979)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.dracula` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `dracula`, description "Dracula", manufacturer
  "Stern", catalog year "1979".
- OPDB record `G4Zl2-Ml90d` (IPDB 728) names this machine "Dracula"
  (Stern Electronics, manufacture date 1979-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `dracula`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `dracula` (1979, Stern).
- `draculc` (2022, Stern / Idleman, clone of `dracula`).
- `draculfp` (1979, Stern, clone of `dracula`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `dracula` at `src/wpc/stgames.c:211` with machine module `by35_mST100s`; no platform is declared (no reviewed profile covers that module yet).

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 23 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
