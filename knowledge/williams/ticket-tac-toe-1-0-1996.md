# Ticket Tac Toe (1.0) (Williams 1996)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.ttt_10` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `ttt_10`, description "Ticket Tac Toe (1.0)", manufacturer
  "Williams", catalog year "1996".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `ttt_10`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `ttt_10` (1996, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `ttt_10` at `src/wpc/wpcgames.c:43` with machine module `wpc_m95S`; the definition declares controller platform `pinmame.wpc-95` from it.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
