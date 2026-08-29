# Jack•Bot (Williams 1995)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.jb_10r` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `jb_10r`, description "Jack*Bot (1.0R)", manufacturer
  "Williams", catalog year "1995".
- OPDB record `GRKOX-MLyrW` (IPDB 3619) names this machine "Jack•Bot"
  (Williams, manufacture date 1995-01-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `jb_10r`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `jb_04a` (1995, Williams, clone of `jb_10r`).
- `jb_101b` (1995, Williams, clone of `jb_10r`).
- `jb_101r` (1995, Williams, clone of `jb_10r`).
- `jb_10b` (1995, Williams, clone of `jb_10r`).
- `jb_10r` (1995, Williams).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `jb_10r` at `src/wpc/sims/wpc/prelim/jb.c:299` with machine module `wpc_m95DCSS`; the definition declares controller platform `pinmame.wpc-95` from it.
- The driver source's named switch/solenoid symbols are carried as 27 candidate devices in the definition.

## What a curator must establish next

full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
