# Road Kings (Williams 1986)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.rdkng_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `rdkng_l4`, description "Road Kings (L-4)", manufacturer
  "Williams", catalog year "1986".
- OPDB record `G4NKJ-Mo1Xj` (IPDB 1970) names this machine "Road Kings"
  (Williams, manufacture date 1986-07-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `rdkng_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `rdkng_l1` (1986, Williams, clone of `rdkng_l4`).
- `rdkng_l2` (1986, Williams, clone of `rdkng_l4`).
- `rdkng_l3` (1986, Williams, clone of `rdkng_l4`).
- `rdkng_l4` (1986, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `rdkng_l4` at `src/wpc/s11games.c:244` with machine module `s11_mS11XS`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
