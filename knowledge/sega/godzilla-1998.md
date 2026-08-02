# Godzilla

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Sega (1998). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

## Playfield devices

Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.

## Custom mechanisms

No custom mechanism conclusion has been validated. Manuals, schematics, PinMAME source, and gameplay evidence still need to be checked.

## Ball-state transitions

Ball paths, trough ordering, locks, kickouts, and causal transitions have not yet been normalized. Relevant source notes follow under Evidence notes.

## Controller interactions

Controller callbacks and bindings are candidate evidence only until reconciled against PinMAME and physical documentation.

## Service and setup information

Unknown; locate operator/service documentation.

## Timing and tuning observations

Source timing values may describe a particular VPX implementation rather than physical hardware and require review.

## Recreation guidance

Do not treat this partial definition as a complete authoring specification. Resolve every coverage requirement and conflict before promotion.

## Evidence notes

- `games/godzilla.json#/switches/4._note`: Pulsed by SolRelease; ball kicked from sw14
- `games/godzilla.json#/coils/0._vbscript_callback`: SolRelease
- `games/godzilla.json#/coils/0._inferred_type`: ball_management
- `games/godzilla.json#/coils/1._vbscript_callback`: Auto_Plunger
- `games/godzilla.json#/coils/1._inferred_type`: ball_management
- `games/godzilla.json#/coils/2._inferred_type`: magnet
- `games/godzilla.json#/coils/2._note`: cvpmMagnet on MagTop, GrabCenter=True
- `games/godzilla.json#/coils/3._inferred_type`: magnet
- `games/godzilla.json#/coils/3._note`: cvpmMagnet on MagMid, GrabCenter=False
- `games/godzilla.json#/coils/4._inferred_type`: magnet
- `games/godzilla.json#/coils/4._note`: cvpmMagnet on MagBot, GrabCenter=False
- `games/godzilla.json#/coils/5._vbscript_callback`: SolShaker
- `games/godzilla.json#/coils/5._inferred_type`: toy
- `games/godzilla.json#/coils/6._vbscript_callback`: Flash07
- `games/godzilla.json#/coils/7._inferred_type`: magnet
- `games/godzilla.json#/coils/7._note`: cvpmMagnet on MagLeft, GrabCenter=True
- `games/godzilla.json#/coils/8._vbscript_callback`: SolRampDiverter
- `games/godzilla.json#/coils/8._inferred_type`: diverter
- `games/godzilla.json#/coils/9._vbscript_callback`: Flash18
- `games/godzilla.json#/coils/10._vbscript_callback`: Flash19
- `games/godzilla.json#/coils/11._vbscript_callback`: Flash20
- `games/godzilla.json#/coils/12._vbscript_callback`: Flash1
- `games/godzilla.json#/coils/13._vbscript_callback`: Flash2
- `games/godzilla.json#/coils/14._vbscript_callback`: Flash3
- `games/godzilla.json#/coils/15._vbscript_callback`: Flash4
- `games/godzilla.json#/coils/16._vbscript_callback`: Flash5
- `games/godzilla.json#/coils/17._vbscript_callback`: Flash6
- `games/godzilla.json#/coils/18._vbscript_callback`: Flash7
- `games/godzilla.json#/coils/19._vbscript_callback`: Flash8
- `games/godzilla.json#/coils/20._vbscript_callback`: SolRFlipper
- `games/godzilla.json#/coils/20._vbscript_name`: sLRFlipper
- `games/godzilla.json#/coils/20._inferred_type`: flipper
- `games/godzilla.json#/coils/21._vbscript_callback`: SolLFlipper
- `games/godzilla.json#/coils/21._vbscript_name`: sLLFlipper
- `games/godzilla.json#/coils/21._inferred_type`: flipper
- `games/godzilla.json#/_source/confidence_notes`: High confidence on switches/coils from VBScript event handlers and SolCallback assignments. Lamp IDs extracted from VLM insert array names (LM_inserts_L*); no per-lamp descriptions available from script alone. Flasher coils (7, 18-20, 25-32) use SolModCallBack for PWM control. Flipper solenoids 46/48 are framework-defined in core.vbs (sLRFlipper/sLLFlipper). Magnets mapped to solenoids 3, 4, 5, 14 via cvpmMagnet. IPDB URL in VBS header says 4443 (correct for Sega Godzilla). Platform uses SEGA.VBS (Sega/Stern WhiteStar).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.godzilla`: `games/godzilla.json` at the pinned migration revision.
