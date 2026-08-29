# Eight Ball Deluxe (Bally 1981)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.eballdlx` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `eballdlx`, description "Eight Ball Deluxe (rev. 15)", manufacturer
  "Bally", catalog year "1981".
- OPDB record `G5KXk-MLB9V` (IPDB 762) names this machine "Eight Ball Deluxe"
  (Bally, manufacture date 1981-04-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- This is a split clone tree: the production drivers of `eballdlx` (including that root
  itself) belong to `bally.eight-ball-deluxe.1981`. This record holds only the residual drivers
  listed below, which may be physically different hardware such as prototypes; their fitment needs
  individual verification.

## Drivers this record holds

- `eballdp1` (1981, Bally, clone of `eballdlx`).
- `eballdp2` (1981, Bally, clone of `eballdlx`).
- `eballdp3` (1981, Bally, clone of `eballdlx`).
- `eballdp4` (1981, Bally, clone of `eballdlx`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `eballdlx` at `src/wpc/by35games.c:1130` with machine module `by35_mBY35_61S`; the definition declares controller platform `pinmame.by35` from it.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
