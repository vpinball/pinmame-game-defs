# Dr. Dude And His Excellent Ray (Bally 1990)

Coverage: **partial - machine identity plus candidate-only I/O attachments. Playfield devices,
wiring, mechanisms, and behavior are evidenced only as unverified candidates.**

This record was promoted from the generated catalog stub `stub.pinmame.dd_l2` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, the platform and device attachments below were added by the 2026-08-29/30 candidate passes and assert nothing beyond candidate provenance. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `dd_l2`, description "Dr. Dude (LA-2)", manufacturer
  "Bally", catalog year "1990".
- OPDB record `GRVEJ-MDq1w` (IPDB 737) names this machine "Dr. Dude And His Excellent Ray"
  (Bally, manufacture date 1990-01-01); the selected identity rests on the reviewed
  machine-specific exception in `config/opdb-overrides.json`: PinMAME abbreviates the title to Dr. Dude; OPDB carries the full title Dr. Dude And His Excellent Ray.
- The definition's driver list is exactly the clone tree PinMAME declares under `dd_l2`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `dd_l2` (1990, Bally).
- `dd_l3c` (2016, Bally, clone of `dd_l2`).
- `dd_lu1` (1990, Bally, clone of `dd_l2`).
- `dd_p06` (1990, Bally, clone of `dd_l2`).
- `dd_p6` (1990, Bally, clone of `dd_l2`).
- `dd_p7` (1990, Bally, clone of `dd_l2`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `dd_l2` at `src/wpc/sims/s11/full/dd.c:419` with machine module `s11c_one`; no platform is declared (no reviewed profile covers that module yet).
- The driver source's named switch/solenoid symbols are carried as 65 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, schematic, or runtime-harness evidence is retained for this machine yet; the candidate sections above are the only retained I/O evidence so far.
