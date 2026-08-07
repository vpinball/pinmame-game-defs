# Creature from the Black Lagoon (Bally, 1992) spatial review

Status: partial. This audit itself finds several genuinely unresolved gaps -- this is the smallest retained VPX extraction curated in this project to date (856 files), and its fidelity does not stretch to cover every documented device -- so the physical machine record at `machines/partial/bally/creature-from-the-black-lagoon-1992.json` stays `partial` for reasons that include, but are not limited to, this audit's own findings.

The matching source is the retained known-working `Creature From The Black Lagoon (Bally 1992).vpx` at SHA-256 `0527ebf5d66a6fa45d40a1ce2bdf1f395af7a3d77aed9bd4eb437399ee0bbb34`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `e6393a87a33c1e53e3b32c3cff2af19dc14b2b4c8764f71dbb57736cadb98df8`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW-style script is the runtime address and causality authority; the Bally operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF carries a real (Adobe Paper Capture) OCR text layer, but it garbles every multi-column table used here. Every printed table used in this definition was read from 300 dpi renders and transcribed into `evidence/excerpts/bally.creature-from-the-black-lagoon.1992/`, indexed by `external:pinmame-review-artifacts/creature/manual-transcription.md`.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from another mechanism's own event (a jet-bumper Hit, the ramp motor's own up/down command) rather than from a Hit/Trigger event on a fixed object. Those addresses are documented projections onto the real table object that carries the underlying mechanism state.
- Switch 18 has a script handler with no matching object anywhere in the extraction (not even under a different type), so it is left genuinely unresolved rather than projected onto anything.
- Fliptronic switches 115-118 have unconfirmed fitment (two pages of the same manual disagree) and are recorded with neither a location nor a not_applicable spatial record, since either would assert something not yet established.
- Solenoids 20 and 24 are the Sequential G.I. board's own 2-bit decoder address-select lines, not coils or bulbs, and take a controlled `internal_nonvisual` record. Solenoids 27 and 28 are printed cabinet-bottom hardware and take `cabinet_or_service`. Solenoid 7 (Knocker) is the standard WPC cabinet-mounted knocker and also takes `cabinet_or_service`.
- Lamp addresses 91-98 are a real, PinMAME-computed public address group (the true Sequential G.I. chase-light bulbs, per pinned wpc.c's WPC_CFTBL handling) that the retained table's script never reads, so none has a coordinate.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 33: Projected onto the Bumper3 jet-bumper object (table object center): the retained script's Bumper3_Hit handler pulses switch 33 directly from the bumper ring's own collision event, matching Bottom Jet.
- Switch 38: Projected onto the moveRamp Primitive (table object center), the mechanism's own moving ramp section: the retained script sets Controller.Switch(38) directly from the ramp motor's up/down state inside the SolRampUp/SolRampDown handlers, not from a Hit event on a fixed object, and pinned cftbl_handleMech does the same via core_setSw(swRampUpDown, locals.creaturerampPos).
- Switch 45: Projected onto the Bumper1 jet-bumper object (table object center): Bumper1_Hit pulses switch 45 (Left Jet) directly from the bumper ring's own collision event.
- Switch 46: Projected onto the Bumper2 jet-bumper object (table object center): Bumper2_Hit pulses switch 46 (Right Jet) directly from the bumper ring's own collision event.
- Solenoid 1: Projected onto the sw34 Kicker object: solenoid 1 (RightUpperKicker) fires the same Top Right Popper kicker that switch 34 (Right Popper) senses -- the same physical hole.
- Solenoid 3: Projected onto the sw37 Kicker object: solenoid 3 (RightLowerKicker) fires the same Lower Right Popper kicker that switch 37 senses -- the same physical hole.
- Solenoid 4: Projected onto the sw56 Kicker object: solenoid 4 (ReleaseBall) fires the trough-release kicker at the Right Trough position (switch 56).
- Solenoid 12: Projected onto the sw55 Kicker object: solenoid 12 (SolOuthole) fires the Outhole kicker at the same position switch 55 senses.
- Solenoid 13: Projected onto the Bumper1 jet-bumper object: solenoid 13 (Left Jet) is the coil inside the same bumper ring switch 45 senses.
- Solenoid 14: Projected onto the Bumper2 jet-bumper object: solenoid 14 (Right Jet) is the coil inside the same bumper ring switch 46 senses.
- Solenoid 15: Projected onto the Bumper3 jet-bumper object: solenoid 15 (Bottom Jet) is the coil inside the same bumper ring switch 33 senses.
- Solenoid 21: Projected onto the Flasher 'creature' object (the hologram's own on-table position); see mechanism.hologram.

## Counts

- Placements: 161
- Located input addresses: 29
- Located output bindings: 67
- Unresolved input addresses: 11
- Unresolved output bindings: 24
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 24
- Outputs with a controlled `cabinet_or_service` record: 12
- Outputs with a controlled `internal_nonvisual` record: 2

## Promotion decision

This record cannot be promoted to `author_ready`. Beyond the unresolved spatial gaps this audit itself reports (switch 18, switches 115-118, GI address 3, lamp addresses 91-98, and five unbound flasher solenoids), the record carries a non-empty `conflicts` array (`conflict.upper-flipper-switches-unconfirmed-fitment`) and `coverage.dimensions.physical_wiring = "conflicted"`. The definition stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]` until a clearer photograph or parts listing of an unrestored machine's Fliptronic II board settles the upper-flipper question and a LibPinMAME gameplay-harness trace against a legal cftbl ROM (or a richer retained VPX recreation) resolves the remaining spatial gaps.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/extracted-vpxtool.manifest.json`, 856 files.
- Human transcription index of every printed table read from the rendered manual pages at `external:pinmame-review-artifacts/creature/manual-transcription.md`, plus the underlying VPX geometry dump at `external:pinmame-review-artifacts/creature/vpx-geometry.txt`.
