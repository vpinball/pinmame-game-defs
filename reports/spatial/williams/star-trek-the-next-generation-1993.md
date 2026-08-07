# Star Trek: The Next Generation (Williams, 1993) spatial review

Status: validated. Every spatial dimension audited here is complete except three lamp positions with no resolvable world-space coordinate; the physical machine record stays `partial` at `machines/partial/williams/star-trek-the-next-generation-1993.json` for exactly that reason. See the promotion decision below.

The matching source is the retained known-working `Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx` at SHA-256 `bd00efe46f3ab2392f8c471e65177b348da8e9fcb5829e9f073ab23f69714d8c`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `073d9971157e822a246b2baf1e8f8033304d1b5272ffb2e9bd9581caf448cd24`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=1093 bottom=2162` (a wide-body "Superpin" table like Indiana Jones), and every canonical coordinate is x/1093 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The manual's own switch-matrix and custom-column silkscreen prints "column 9" as addresses 91-98, and the custom-solenoid board prints items 37-42; neither is the PinMAME public address. CORE_CUSTSWCOL/CORE_FIRSTCUSTSOL arithmetic places them at public 121-128 and 51-56 respectively, and the retained known-working script's own Controller.Switch(122/125/126/127) assignments and SolCallBack(51-54)/SolModCallBack(55/56) registrations confirm the arithmetic directly at runtime.
- The switch-matrix opto shading (2-42) and PinMAME's sttngGameData inverted-switch mask agree on every single opto address (columns 3, 4, and 6 rows 1-7) -- zero polarity conflicts, unlike Monster Bash or Indiana Jones.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from a ball-stack class's internal counter (trough, Borg lock) or from a gun assembly's continuous rotation angle (gun Home/Mark) rather than from a Hit/Trigger event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state; the projection notes are explicit that a motor's continuous rotation, not a solenoid pulse, drives the sensed position.
- GI addresses 1 and 2 ("Insert G.I.") drive only VR-backglass-room helper objects (VRBGGI*/VRBGGIarea*) in the retained table's own UpdateGI dispatch, confirming they are backbox-only circuits with no playfield bulb, matching the manual's own "Insert" (non-playfield) wording.
- GI addresses 0, 3, and 4 use the retained table's St1Shields/St4PFGI/St5ReLa emitter collections, nearest-neighbor deduplicated to exclude co-located Light/Flasher render-double pairs and already-counted solenoid-driven flasher devices incidentally swept into the ambient-dimming collection.
- Solenoid 7 (Knocker) is a backbox device (voltage and drive connections both on the backbox side of the harness) and takes a controlled `cabinet_or_service` record.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Explicit projections

- Switch 31: Projected onto the Borg Lock kicker (Kicker BorgKicker, table object center): the retained script's BorgLock ball-stack class (cvpmBallStack.InitSw 0,31,0,0,0,0,0,0) has no separate playfield trigger object for this position; the single lock ball rests directly at the kicker used to eject it.
- Switch 34: Projected onto the right gun kicker (Kicker Kicker2, table object center): the retained script's Kicker2_Hit handler sets Controller.Switch(34)=1 when a ball reaches the right gun barrel and RightCannonKicker clears it on launch (Controller.Switch(34)=0) -- there is no separate playfield sensor object beyond the kicker itself.
- Switch 38: Projected onto the left gun kicker (Kicker Kicker1, table object center); see switch 34's right-side counterpart -- Kicker1_Hit sets Controller.Switch(38)=1 and LeftCannonKicker clears it.
- Switch 61: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center): the retained script models the six-position trough purely as a cvpmBallStack ball counter (bsTrough.InitSw 0,66,65,64,63,62,61,0) with no discrete playfield trigger per position.
- Switch 62: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.
- Switch 63: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.
- Switch 64: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.
- Switch 65: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.
- Switch 66: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.
- Switch 67: Projected onto the trough ball-release kicker (Kicker BallRelease, table object center): the retained script's SolRelease handler pulses this switch (vpmTimer.PulseSw 67) in the same event that fires bsTrough.ExitSol_On, with no separate playfield sensor object.
- Switch 68: Projected onto the auto plunger (Kicker AutoPlunger, table object center): the retained script's AutoPlunger_Hit handler sets Controller.Switch(68)=1 directly on the plunger kicker object, with no separate playfield sensor.
- Switch 122: Projected onto the left gun's own rotating base (Primitive CannonBaseL, table object center): the retained script's CannonLTimer_Timer sets Controller.Switch(122)=1 while CannonBaseL.ObjRotZ sits in -20..9 degrees, directly from the gun's continuous rotation angle, not from a discrete cam-actuated sensor object. The motor (solenoid 17) drives the rotation continuously; it does not itself actuate this switch -- the switch senses the resulting mechanical position.
- Switch 125: Projected onto the right gun's own rotating base (Primitive CannonBaseR, table object center); see switch 122's left-side counterpart -- CannonRTimer_Timer sets Controller.Switch(125)=1 for -20..-17 degrees (Right Gun Home).
- Switch 126: Projected onto the right gun's own rotating base (Primitive CannonBaseR, table object center); see switch 125 -- CannonRTimer_Timer sets Controller.Switch(126)=1 for -20..9 degrees (Right Gun Mark).
- Switch 127: Projected onto the left gun's own rotating base (Primitive CannonBaseL, table object center); see switch 122 -- CannonLTimer_Timer sets Controller.Switch(127)=1 for -20..-17 degrees (Left Gun Home).
- Solenoid 15: Y clamped from -0.008688 (raw local coordinate -18.784, essentially at the rear playfield edge) to the schema-valid boundary 0.0; the retained table's Flipper-typed "Diverter" primitive sits fractionally above y=0, matching the manual's Top Divertor location near the very top of the playfield.
- Lamp 78: Centroid of the five l78a-e "Borg Ship" flight-path animation waypoints (same single physical bulb's own multi-primitive render effect, not a centroid of other devices).

## Counts

- Placements: 193
- Located input addresses: 62
- Located output bindings: 94
- Inputs with a controlled `cabinet_or_service` record: 17
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 5
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 9
- Outputs with a controlled `virtual` record: 14
- Unresolved output placements: 3

## Promotion decision

No unresolved semantic question, address-enumeration gap, or polarity conflict remains anywhere in this definition, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. `conflicts` is empty and `coverage.dimensions.physical_wiring = "validated"`. However, three playfield lamps (53 Advance in Rank, 85 Borg Lock, 86 Borg Jackpot) have no resolvable world-space coordinate in the retained extraction -- only a colored Primitive mesh at local origin, parented to a transform this curator does not resolve. Inventing a coordinate for them would violate the project's never-invent-a-coordinate rule, so the record stays `partial` with `coverage.missing = ["spatial_placement"]` until a further extraction pass resolves those three primitives' world transforms (or a photograph/service note independently fixes their playfield location).

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/extracted-vpxtool.manifest.json`, SHA-256 `c913342c6421558eead345703d08105db5b2779e936f898e56ec1fd177249542`, 1585 files, 247600334 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `07f57792c7f405a5e59607a73ac73bb00f9b7daa91ede63477337d4a9ce8f948`.
