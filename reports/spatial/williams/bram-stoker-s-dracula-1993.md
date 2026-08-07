# Bram Stoker's Dracula (Williams, 1993) spatial review

Status: validated. Every spatial dimension audited here is complete except one lamp with no retained geometry, but the physical machine record itself remains `partial` at `machines/partial/williams/bram-stoker-s-dracula-1993.json` because of that gap plus an unresolved wiring-provenance conflict outside this audit's scope; see the promotion decision below.

The matching source is the retained known-working `Bram Stokers Dracula (Williams 1993) VPW 1.0.vpx` at SHA-256 `e291eb0ab61eb8940aba6f54d16efd512d4565cbb6af29fcae5530035de7575e`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `32f4f0ed85702cc015563eb262ea6c5b7cb7c90f6d30fa6b73c36f3c37c42c5f`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=2117.647`, and every canonical coordinate is x/952.941 and y/2117.647 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- This manual marks opto-construction switches by writing "Opto" directly into the printed switch-matrix label rather than by shading. Columns 5 and 7 match pinned PinMAME's inverted-switch mask exactly; column 8's single opto (switch 82) is resolvable only from the Switch Locations parts list, where 81 and 83 use the plain leaf part 5647-12693-14 -- zero polarity disagreement across the whole matrix.
- Switches 61-65 (jets and slingshots) and 77 (Right Ramp Up) have no dedicated playfield trigger object; the retained script pulses their public state directly from the Bumper/Wall objects' Hit events or from solenoid commands, so they are documented projections onto the real mechanism object.
- Switches 81/82/83 (Mist Magnet) have no fixed sensor object: the motorized carriage's position is tracked purely in software, so all three are projected onto the fixed Trigger.Magnet detection zone.
- Flasher addresses with two manual-printed functions per circuit (19, 20, 21) drive two distinct retained Light objects and get two placements; addresses with one manual-printed function pair sharing a single retained Light object (17, 18, 22, 23, 24) get one placement, disclosed in physical.notes.
- GI strings 0-2 use the retained table's GIBOT/GITOP/GIMID emitter collections, matching the retained script's GIUpdate2 dispatch exactly with zero script-vs-manual disagreement. GI strings 3 and 4 are backbox-only circuits and take a controlled `cabinet_or_service` record.
- Four lamps (58, 61, 62, 63) are drawn only inside the manual's separate "Back Panel Assy." box; the retained table corroborates this independently (all four normalize to y < 0.011). They take a controlled `cabinet_or_service` record.
- Lamp 53 (Magnet) has no retained Light object and no script reference; its `spatial` key is omitted entirely rather than a coordinate being invented, and it is the sole entry in `coverage.missing`'s spatial gap.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 34: Projected onto the retained Plunger object (Plunger.Plunger): the Launch Ball switch is a mechanical switch on the plunger assembly itself, not a separate playfield sensor.
- Switch 61: Projected onto the retained Bumper2 object, which the retained script's Bumper2_Hit handler pulses as switch 61 (Left Jet).
- Switch 62: Projected onto the retained Bumper3 object, which the retained script's Bumper3_Hit handler pulses as switch 62 (Right Jet).
- Switch 63: Projected onto the retained Bumper1 object, which the retained script's Bumper1_Hit handler pulses as switch 63 (Bottom Jet).
- Switch 64: Projected onto the retained LeftSlingShot wall, which the retained script's LeftSlingShot_Slingshot handler pulses as switch 64.
- Switch 65: Projected onto the retained RightSlingShot wall, which the retained script's RightSlingShot_Slingshot handler pulses as switch 65.
- Switch 77: Projected onto the Right Ramp mechanism (Ramp.RightRamp): the retained script sets public switch 77 directly from the SolRRampUp/SolRRampDown solenoid commands (Controller.Switch(77) = True/False) rather than from a discrete sensor object, even though the Switch Locations parts list prints a real part number (5647-12693-36) for it.
- Switch 81: Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): the motorized magnet carriage has no single resting position (see the Mist Magnet mechanism), and switch 81 is set from the carriage's software-tracked position (MagnetPos > 490) rather than a discrete sensor object at a fixed location.
- Switch 82: Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): the retained script's MistTimer_Timer sets switch 82 from a ball-crossing line test against this same zone rather than a Hit event on a separate object; see switch 81.
- Switch 83: Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): switch 83 is set from the carriage's software-tracked position (MagnetPos < 10); see switch 81.

## Counts

- Placements: 173
- Located input addresses: 46
- Located output bindings: 89
- Unresolved inputs (no spatial key): []
- Unresolved outputs (no spatial key): [{'group': 'pinmame.output.lamp', 'address': 53}]
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 17
- Outputs with a controlled `cabinet_or_service` record: 10
- Outputs with a controlled `unused` record: 5
- Outputs with a controlled `virtual` record: 14

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this audit covers except lamp 53, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Lamp 53 (Magnet, #44) is a genuine bulb per the manual with no resolvable geometry in the retained extraction, and solenoids 33-36 carry an unresolved disagreement between pinned PinMAME's own macro naming and this manual's printed circuit-side label about which upper-flipper driver pair underlies each address (`conflict.upper-flipper-circuit-side-naming`). The definition therefore carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = "conflicted"`, so promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/extracted-vpxtool.manifest.json`, SHA-256 `ea69203a05b34f6eeb7572e17d1185e2d42be87b8ebd5593bf9efe44baa28da0`, 2484 files, 597253321 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `46fae8a9e5b625634576dd280d0cf8ce78106ecd71aafdee0f921784f5105548`.
