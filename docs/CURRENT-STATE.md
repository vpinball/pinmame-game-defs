# Current state

This file is the short, mutable companion to `docs/INSTRUCTIONS.md`: the project state that the
generic runbook must not hold and that has no better home. Every curation session reads it, so every
line costs every agent context. Keep it under about 8 KB, keep it current, and never use it as a log.

It does not hold:

- per-game narratives, partial-status reasons, or mechanism and edition knowledge: those belong in
  the game's knowledge note, spatial report and `coverage.missing`;
- session diaries, model runs, or review rounds: those belong in commit messages, the PR
  description and `review-artifacts` under the working root;
- coverage counts: read the generated `reports/coverage.md` or the `summary` of
  `catalog/pinmame.json`, never a copied literal;
- claims: the per-game branch and worktree are the claim (runbook step 1);
- general rules and lessons: write them into the runbook, or into the topic doc for the task they
  govern (the runbook's documentation map lists them).

The ledger as it stood before this compaction, with every per-game section and review round up to
2026-10-01, is frozen at `docs/archive/current-state-ledger-until-2026-10-01.md`. Search it with
`rg` for the history behind a past decision; never read it whole, and never append to it.

## Pinned baseline

| Input | Required revision | Baseline role |
| --- | --- | --- |
| `vpinball/pinmame` | `97aa922bf8e4b6970126192ec1ac1fb0305a4f62` | Authoritative LibPinMAME build and driver catalog (2,962 reported drivers before scope exclusions); since 2026-10-05, replacing `b7a60eb0` (which had replaced `8371478a` the same day); records keep citing an earlier revision where they were read there |
| `sverrewl/vpxtable_scripts` | `0c036bb61b4b4e8c778c37559f6795df8cd1521e` | First pinned known-working VPX script corpus |
| `jsm174/vpx-standalone-scripts` | `15d112648a1b94b9f59eb8b3c335d57283653c50` | Second pinned known-working VPX script corpus |
| `vpinball/pinmame-dotnet` | `e3e31eea6cd8eb046b4a8ea3110a31bb19c32b45` | Historical: managed interop reference for the migrated compatibility fixtures; no local checkout needed |
| Legacy managed integration | `cf2030710f9a6ee19fdbeec9cc9fccaba2032a6f` | Historical: migration evidence for the 11 legacy game classes, aliases and direct wires; fetch only to change or revalidate that migration |

The first three are operational and match the clone script in `docs/SETUP.md`. Changing any of them is a
scope change; follow the runbook's pinned-input procedure.

## Scope exceptions

The reviewed virtual-only exclusion set is `OUT_OF_SCOPE_DRIVER_REASONS` in
`src/pinmame_game_defs/scope.py`; do not regenerate records for those drivers. Ordinary firmware
modifications and physical conversions stay in scope when they run on documented hardware (for
example `clash`, a physical Rock Encore conversion, and `mac_zois`, the physical machinaZOIS
installation). Adding or removing an exclusion needs evidence, tests, a catalog diff, high-tier
model review and maintainer PR review.

## Standing priorities

- Since 2026-09-25 the maintainer priority is the Pinside Top 100 solid-state list of 2026-09-20,
  worked highest rank first: `docs/pinside-top100.md` lists every ranked title that has a PinMAME
  record, with its current completion score. Keep that file current: regeneration refreshes the
  scores and a test fails when they are stale, but a split, merged or renamed record needs its row
  updated by hand. Titles on hardware pinned PinMAME has no driver for (SPIKE, JJP, Spooky after its four pinHeck games, CGC
  remakes, Barrels of Fun, Dutch Pinball, American Pinball, Pinball Brothers, Heighway, DPX) are out
  of scope. A title's open requirements are its `coverage.missing`.
- Otherwise follow the runbook's default order.

## Open cross-machine corrections

Unclaimed sweeps that span several records. Claim one with a branch like any game, and delete its
entry in the commit that finishes it.

- **WPC flipper buttons 112/114.** The runbook's Fliptronic read-path rule makes these contacts
  normally open, but several WPC records, some of them `author_ready`, still set
  `normally_closed: true` on switch inputs 112 and 114 (archive L452 lists the ones known then).
  Find them by scanning `machines/` for that pair, and correct each through its curator and seed.
- **Harness-reachable conflicts still open.** A 2026-10-01 pass triaged every conflict whose resolution path names a harness run and ran the probes the authorized ROM library allowed; it settled fourteen machines and left these: Elvira's flip-up roles (complete both targets and collect the award), 24's suitcase stepper order (re-derive the S.A.M. key navigation to the Suitcase Motor Test), the STTNG ship-mode mission run, and the ROM half of Judge Dredd's L-1 switch fitment, Scared Stiff's auxiliary lamp columns and Flash Gordon's lamp 100. The full triage is in the working root's `review-artifacts/harness-conflicts-2026-10-01/triage.md`.
- **Ali lamps 24, 25, 42 and 58, and the Stern MPU-200 flipper outputs.** `curate_ali.py` pairs public lamps 24 and 25 with transistors Q24 and Q25. Star Gazer's ROM proves the pair is crossed on the same LDA-100 board (public 24 reaches Q25 and the 3000 value lamp, public 25 reaches Q24), and Quicksilver's Lamp Driver Schematic reads the same crossing (decoder `U2` S7/S8 drive Q25/Q24) plus a second one (`U3`/`U4` S9 drive Q41/Q46, so public 42 is Q41 and public 58 is Q46, which would swap Ali's left and right extra-ball lamps; Star Gazer's record carries Ali's 42/58 pairing, which gives its zodiac target value lamps 3000 and 4000 the opposite public addresses to the ladder order every other value row follows, so check it with a ROM probe of the zodiac target values). Ali leaves 24 and 25 unused, so nothing there tested it; compare its chart rows and its own lamp-driver schematic's connector pins before correcting them through its curator. Separately, `controllers/pinmame/stern-mpu200.json` omits the synthetic flipper power outputs 45 and 47 that a flipper press publishes.
- **Out-of-range clamps.** `curate_cirqus_voltaire.py` clamps sole objects that lie 6-8 % beyond the
  right rail. Check each against the out-of-range lesson in `docs/SPATIAL.md`; the record is
  `author_ready`.
