# Big Guns (Williams 1987)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.bguns_l8` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `bguns_l8`, description "Big Guns (L-8)", manufacturer
  "Williams", catalog year "1987".
- OPDB record `G4d8k-MJ5Z8` (IPDB 250) names this machine "Big Guns"
  (Williams, manufacture date 1987-10-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `bguns_l8`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bguns_l7` (1987, Williams, clone of `bguns_l8`).
- `bguns_l8` (1987, Williams).
- `bguns_la` (1987, Williams, clone of `bguns_l8`).
- `bguns_lac` (2019, Williams, clone of `bguns_l8`).
- `bguns_p1` (1987, Williams, clone of `bguns_l8`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `bguns_l8` at `src/wpc/s11games.c:448` with machine module `s11_mS11AS`; the definition declares controller platform `pinmame.system-11` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
