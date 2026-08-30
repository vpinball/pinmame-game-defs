# Black Knight 2000 (Williams 1989)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.bk2k_l4` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `bk2k_l4`, description "Black Knight 2000 (L-4)", manufacturer
  "Williams", catalog year "1989".
- OPDB record `GrxPP-Ml91r` (IPDB 311) names this machine "Black Knight 2000"
  (Williams, manufacture date 1989-01-04); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `bk2k_l4`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `bk2k_l4` (1989, Williams).
- `bk2k_la2` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_lg1` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_lg3` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_pa5` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_pa7` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_pf1` (1989, Williams, clone of `bk2k_l4`).
- `bk2k_pu1` (1989, Williams, clone of `bk2k_l4`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `bk2k_l4` at `src/wpc/s11games.c:836` with machine module `s11_mS11BS`; the definition declares controller platform `pinmame.system-11` from it.
- The driver source's named switch/solenoid symbols are carried as 83 candidate devices in the definition.

## VPX script candidates (candidate)

- 1 retained community table script(s) declare this machine's driver; their extracted switch/lamp/solenoid/GI candidates are carried as 83 candidate devices. When curator work weighs sources, a retained script outranks emulator-derived candidates for runtime semantics, but every device here is still a candidate until a known-working table is verified against this exact physical machine.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
