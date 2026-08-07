# Cirqus Voltaire (Bally, 1997) spatial review

Status: validated. Every spatial dimension audited here is complete, but the physical machine record itself remains `partial` at `machines/partial/bally/cirqus-voltaire-1997.json` because of an unresolved switch-polarity conflict outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Cirqus Voltaire (Bally 1997) VPW Mod v1.0.vpx` at SHA-256 `7aab0f175816f7bdee4114d5859cbfc70760aead8ef39ebf6481609b649207e5`. The retained extraction produced the embedded script at SHA-256 `2abdca0fb8870c995314c52d5e3931530f6c850b1c8ac5f11176aca58b87bfa4`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual has a present but column-shifted `pdftotext -layout` text layer. Every printed table used here was read from 300-600 dpi renders, not the OCR text layer alone.
- Trough switches 31-35 have no dedicated playfield trigger object because the retained script's cvpmBallStack class tracks them from internal ball-count state; they are documented projections onto the trough's own exit kicker (BallRelease). Ringmaster switches 42-44 are likewise projected onto the Ringmaster figure itself, since the retained script's cvpmMech class reads them from one continuous motor-position counter rather than three discrete sensor objects.
- Two solenoid-driven mechanisms (Diverter Power/Hold at 1.06-1.07 normalized x, Neon at 1.08) sit just past the retained table's own declared right edge; each is clamped to x=1.000000 with the raw offset disclosed rather than fabricating a different coordinate.
- GI strings 0-2 use the retained table's Gi_Pf_Right_01/Gi_Pf_Middle_02/Gi_Pf_Left_03 emitter collections, matching the retained script's `UpdateGI` dispatch exactly. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record; the manual disagrees with itself about which is 'Backbox 1' and which is 'Backbox 2' (conflict.gi-backbox-string-numbering), which does not affect either string's spatial disposition.
- Solenoids 41 and 51/52 are PinMAME's mirror/decaying-state duplicates of physical solenoids 39, 35, and 36 respectively and are declared `virtual` with a `virtual` spatial record so no duplicate device is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.
- A prior legacy-migrated record had the Left/Right Spinner labels (switches 115/117) reversed; the manual's own printed F5/F7 labels and the retained table's own left/right geometry both independently agree and correct it.

## Explicit projections

- Switch 31: Projected onto the ball-release kicker (BallRelease, table object center): the retained script's cvpmBallStack class (bsTrough) tracks trough switches 31-35 from internal ball-count state rather than five separate playfield trigger objects, and BallRelease is the trough's own exit kicker.
- Switch 32: Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.
- Switch 33: Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.
- Switch 34: Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.
- Switch 35: Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.
- Switch 42: Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center): the retained script's cvpmMech class (mechRM) reads switches 42/43/44 from a single 0-118 motor-position counter (AddSw 44,0,1 / AddSw 43,88,89 / AddSw 42,117,118), not three separate playfield sensor objects.
- Switch 43: Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center); see switch 42.
- Switch 44: Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center); see switch 42.

## Clamped coordinates

- Solenoid 6: raw x=1.062556, clamped to 1.000000
- Solenoid 7: raw x=1.067884, clamped to 1.000000
- Solenoid 8: raw x=1.067884, clamped to 1.000000
- Solenoid 34: raw x=1.062556, clamped to 1.000000
- Solenoid 37: raw x=1.080000, clamped to 1.000000

## Counts

- Placements: 177
- Located input addresses: 43
- Located output bindings: 103
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 8
- Inputs with a controlled `unused` record: 13
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 12

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. However, public switches 37 and 38 ('WOW' Targets, Top Targets) are printed normally-closed opto interrupters that pinned PinMAME's cvGameData inverted-switch mask does not normalize -- an unresolved polarity conflict recorded as `conflict.wow-top-targets-opto-not-normalized` -- and a second, independent manual self-contradiction about the two backbox GI strings' own numbering is recorded as `conflict.gi-backbox-string-numbering`. The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["polarity", "unresolved_conflicts"]` until a LibPinMAME harness trace against a legal cv_20h or cv_14 ROM observes the true idle public state of 37/38.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/cirqus-voltaire-1997/extracted-vpxtool.manifest.json`, SHA-256 `156520b390cbd3e9314d498ff3c6787e3511031093ca21597a82327d66d01660`, 1522 files, 297184998 bytes.
- Human transcription of every printed table read from the rendered manual pages under `external:pinmame-review-artifacts/cirqus-voltaire/`.
