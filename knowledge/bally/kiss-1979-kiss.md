# KISS (Bally 1979)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.kiss` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `kiss`, description "Kiss", manufacturer
  "Bally", catalog year "1979".
- OPDB record `G4jXr-MQ6kz` (IPDB 1386) names this machine "KISS"
  (Bally, manufacture date 1979-06-01); identity is unresolved: OPDB record shared with bally.kiss.1979, so the mapped record is treated as a lead
  rather than a resolved identity.
- This is a split clone tree: the production drivers of `kiss` (including that root
  itself) belong to `bally.kiss.1979`. This record holds only the residual drivers
  listed below, which may be physically different hardware such as prototypes; their fitment needs
  individual verification.

## Drivers this record holds

- `kissp` (1979, Bally, clone of `kiss`).
- `kissp2` (1979, Bally, clone of `kiss`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `kissp` at `src/wpc/kissproto.c:176` with machine module `by8035`; no platform is declared (the record does not hold its own root driver, so the root's module cannot describe its hardware).

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
