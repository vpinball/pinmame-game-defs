# Pinball (Stern 1977)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.pinball` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `pinball`, description "Pinball", manufacturer
  "Stern", catalog year "1977".
- OPDB record `GrZXj-Mq11k` (IPDB 1792) names this machine "Pinball"
  (Stern Electronics, manufacture date 1977-01-08); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `pinball`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `pinbalfp` (1977, Stern, clone of `pinball`).
- `pinball` (1977, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `pinball` at `src/wpc/stgames.c:54` with machine module `by35_mST100`; no reviewed profile covers that module yet, so no platform is declared.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 70 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
