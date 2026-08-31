# Firepower (Williams 1980)

Coverage: **partial - machine identity validated plus VPX script candidate I/O. Playfield
devices, wiring, mechanisms, and behavior are evidenced as candidates from the retained
community VPX table; physical wiring, polarity, and recreation knowledge are outstanding.**

This record was promoted from the generated catalog stub `stub.pinmame.frpwr_l6` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged. The 2026-08-31 VPX script pass attached
runtime I/O candidates from the retained `vpxtable_scripts` corpus (`firepower-1980.vpx`,
VPX 10.4, by 3rdaxis/Slydog43/G5K) to the partial definition. Every requirement in the
definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `frpwr_l6`, description "Firepower (L-6)", manufacturer
  "Williams", catalog year "1980".
- OPDB record `G5VDd-MJpqO` (IPDB 856) names this machine "Firepower"
  (Williams, manufacture date 1980-02-01); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `frpwr_l6`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `frpwr_a6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_b6` (2003, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_b7` (2003, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_c6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_c7` (2006, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_d6` (2008, Williams / Oliver, clone of `frpwr_l6`).
- `frpwr_l2` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_l2ff` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_l6` (1980, Williams).
- `frpwr_l6ff` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_t6` (1980, Williams, clone of `frpwr_l6`).
- `frpwr_t6ff` (1980, Williams, clone of `frpwr_l6`).

## VPX script candidates (candidate)

- 1 retained community table script (`vpxtable_scripts: Firepower (Williams 1980).vpx`,
  SHA-256 `8d0ec27855bf80407a6efb54e28cf9fee476d2e8ec2d630a3c2016981f8e58dc`) declares
  this machine's driver; its extracted candidates are carried below. When curator work weighs
  sources, a retained script outranks emulator-derived candidates for runtime semantics, but
  every device here is still a candidate until a known-working table is verified against this
  exact physical machine.
- **52 switches** enumerated (50 playfield switches plus 2 VPM framework switches
  `USELITEBOOST`/`USESHADOW` filtered out): 4 eject-hole switches, 2 eject-hole ejectors,
  1 ball-save kicker, 1 ball-ramp thrower, 1 out-hole/drain, 6 rollovers, 2 kickers, 1
  spinner, 7 standup targets, 4 bumper switches, 2 slingshots, 4 power targets, 4 letter
  rollovers (F/I/R/E), 1 ball shooter/plunger, 1 playfield tilt, 2 ball ramps, 2 eject
  rollovers.
- **12 solenoids/outputs**: SolOn, LBank Reset, RBank Reset, Left/Right/Upper Eject Holes,
  Ball Save Kick, Ball Ramp Thrower, Credit Knocker, Flash Lamps, Left/Right Sling Shots.
- **14 mechanisms**: flippers, bumpers, slingshots, power targets, standup targets, hit
  targets, kickers, drain, plunger, spinner, ball release, eject holes, ramps, score reels.
- Controller platform: **Williams System 6/7** — no existing profile in the repository covers
  this generation; `controller_platform` remains `coverage.missing`.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source (`src/wpc/frpwr.c` or equivalent
System 6/7 module); full input, output, and display enumeration with validated semantic names;
physical wiring and polarity; mechanism inventory and behavior; variant differences across the
clone tree; recreation knowledge from a manual, schematic, or known-working table; runtime
provenance; and a normalized spatial placement for every physical device. No manual, schematic,
or runtime-harness evidence is retained for this machine yet; the VPX script candidates above
are the only retained I/O evidence so far.