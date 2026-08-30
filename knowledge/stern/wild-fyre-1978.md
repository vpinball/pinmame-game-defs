# Wild Fyre (Stern 1978)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.wildfyre` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `wildfyre`, description "Wild Fyre", manufacturer
  "Stern", catalog year "1978".
- OPDB record `GrOwV-Ml9kO` (IPDB 2783) names this machine "Wild Fyre"
  (Stern Electronics, manufacture date 1978-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `wildfyre`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `wildfyfp` (1978, Stern, clone of `wildfyre`).
- `wildfyrc` (2022, Stern / Idleman, clone of `wildfyre`).
- `wildfyre` (1978, Stern).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `wildfyre` at `src/wpc/stgames.c:169` with machine module `by35_mST100s`; no platform is declared (no reviewed profile covers that module yet).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
