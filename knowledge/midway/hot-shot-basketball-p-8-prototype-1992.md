# Hot Shot Basketball (P-8 Prototype) (Midway 1992)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.hshot_p8` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `hshot_p8`, description "Hot Shot Basketball (P-8 Prototype)", manufacturer
  "Midway", catalog year "1992".
- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes
  from the PinMAME catalog alone and is unverified.
- The definition's driver list is exactly the clone tree PinMAME declares under `hshot_p8`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `hshot_p8` (1992, Midway).
- `hshot_p9` (1992, Midway, clone of `hshot_p8`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `hshot_p8` at `src/wpc/bowlgames.c:552` with machine module `wpc_mFliptronS`; the definition declares controller platform `pinmame.wpc-fliptronic` from it.

## What a curator must establish next

Full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
