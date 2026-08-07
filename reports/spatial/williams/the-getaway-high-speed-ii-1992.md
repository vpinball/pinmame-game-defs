# The Getaway: High Speed II (Williams, 1992) spatial review

Status: partial. This is a comparatively thin retained table (875 extracted files, a 39,497-byte script) and several authoring-relevant addresses have no VPX geometry at all; see Blockers below.

The matching source is the retained known-working `Getaway, The - High Speed II v1.2.vpx` at SHA-256 `22e7257316dcb3c414f62a0543f6a68063e8f50524ad9559f1ff98bd38184efc`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `4f91dbf71bf134b1113939a517900c27d87fa1a142109e79ad64306a40aeb78e`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW-style script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry. The pinned driver source's own #define comment labels are treated with reduced authority for semantic device identity specifically, because the driver's own header comment states its author had no access to the physical machine and guessed most switch/solenoid labels from a photo and the rulesheet; its numeric public addresses remain real hardware regardless.
- The retained manual PDF carries an Adobe Acrobat Pro Paper Capture OCR text layer that is present but garbled for the multi-column wiring tables. Every printed table used here was read from rendered pages and transcribed into `external:pinmame-review-artifacts/getaway/manual-transcription.md`.
- Several addresses have no VPX geometry at all in this recreation: the gear-shifter switches (33/34) are driven purely from unrelated keyboard keys with no modeled lever object; the individual trough positions (56/57/58) are abstracted inside a ball-stack helper class; the Enable relay solenoids (25/26/28) and Diverter High (1) have no SolCallback-bound visual object. These are recorded as named gaps rather than projected or invented.
- Switches 31/32 (slingshots) and solenoid 54's causing pair (2/3, the ramp lift) are documented projections onto the mechanism object the retained script actually manipulates in the same event that sets the switch/solenoid state, not onto an unrelated placeholder.
- GI addresses 0 and 1 are both playfield-wired per the manual, but the retained script's UpdateGI ignores its own GI-address parameter and drives one shared 25-member object collection for any GI address; neither address carries a validated per-address placement as a result.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- pinmame.input.switch 31: Projected onto the Wall.LeftSlingshot collision wall's centroid: the retained script's LeftSlingShot_Slingshot handler pulses switch 31 on collision with this wall (vpmTimer.pulseSw 31), and no separate switch-31 trigger object exists.
- pinmame.input.switch 32: Projected onto the Wall.RightSlingshot collision wall's centroid; see switch 31.
- pinmame.input.switch 54: Projected onto the div_ramp Primitive (the ramp-lift flap object the retained script rotates in the same handler): SolRampUp/SolRampDown set Controller.Switch(54) directly in code (RampaMovil.Collidable / div_ramp.ObjRotY are toggled together in the same Sub), matching the manual's own finding that the physical sensor is the B-12576 Ramp Lifting Mechanism's own microswitch (part 5647-12001-00, identical to the part this manual prints for switch 54) rather than a separate playfield object.
- pinmame.input.switch 55: Projected onto the Kicker.Drain object (the retained table's drain/outhole entry kicker): the cvpmBallStack class (bsTrough.InitSw 55,58,57,56) manages switches 55-58 internally with no individually named trigger object per address; Kicker.Drain is the one physically-modeled object at the outhole/drain position.
- pinmame.output.solenoid 2: Projected onto the RampaMovil moving-ramp object's centroid: SolRampUp/SolRampDown directly toggle RampaMovil.Collidable and rotate the div_ramp flap in the same handler; there is no separate coil-plunger object modeled.
- pinmame.output.solenoid 3: Projected onto the RampaMovil moving-ramp object's centroid; see solenoid 2.
- pinmame.output.solenoid 4: Projected onto the postlock Primitive (the retained script's LockPost sub raises/lowers PosteArriba and repositions postlock.z in the same event).
- pinmame.output.solenoid 5: Projected onto the Wall.LeftSlingshot collision wall's centroid, the object the retained script's LeftSlingShot_Slingshot handler animates on the same event that pulses switch 31.
- pinmame.output.solenoid 6: Projected onto the Wall.RightSlingshot collision wall's centroid; see solenoid 5.
- pinmame.output.solenoid 8: Projected onto the retained table's literal Plunger1 object (near the left outlane, raw x=53.5 next to switch 25's raw x=53.3): the retained script's SolKickback handler calls Plunger1.Fire/Plunger1.PullBack directly, confirming this VPX Plunger-type object -- not the shooter-lane plunger -- is the kickback mechanism.
- pinmame.output.solenoid 9: Projected onto the Kicker.sw77 object, the same physical captive-ball saucer switch 77 senses.
- pinmame.output.solenoid 10: Projected onto the sc_div Primitive (the visible Supercharger loop diverter flap the retained script's SuperchargerDiverter handler rotates); the companion Wall29 collision wall shares the same mechanism.
- pinmame.output.solenoid 12: Projected onto the Trigger.ShooterLane position: the retained script's cvpmImpulseP plunger instance (plungerIM) is initialized against the ShooterLane object at the same physical shooter-lane location as switch 78.

## Counts

- Placements: 136
- Located input addresses: 45
- Located output bindings: 82
- Unresolved (no spatial key) input addresses: 5
- Unresolved (no spatial key) output bindings: 9
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 10
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `internal_nonvisual` record: 6
- Outputs with a controlled `unused` record: 2
- Outputs with a controlled `virtual` record: 14

## Promotion decision

This record stays `partial`. Two first-class conflicts remain unresolved (`conflict.switch-84-85-manual-vs-script-semantics`, `conflict.solenoid-31-fastflip-address-not-declared`), several authoring-relevant addresses have no spatial placement at all in this thin retained table, and `recreation_notes` is withheld from `coverage` because this pass did not obtain the mandatory independent high-tier cross-provider review described in `docs/INSTRUCTIONS.md`. `coverage.missing = ["output_semantics", "recreation_notes", "spatial_placement", "unresolved_conflicts"]` names each gap explicitly.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/the-getaway-high-speed-ii-1992/extracted-vpxtool.manifest.json`, 875 files.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `a450922126d99280fb9accedbe3c40cf00a70fde102ad541fb322b0521f0743f`.
