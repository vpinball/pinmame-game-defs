# Star Trek: The Next Generation (Williams, 1993) spatial review

Status: partial. The physical machine record stays `partial` at `machines/partial/williams/star-trek-the-next-generation-1993.json` because one flasher (22) has no placement, one (28) is only observed, and lamps 13 and 14 carry a conflict. See the promotion decision below.

The matching source is the retained known-working `Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx` at SHA-256 `bd00efe46f3ab2392f8c471e65177b348da8e9fcb5829e9f073ab23f69714d8c`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `073d9971157e822a246b2baf1e8f8033304d1b5272ffb2e9bd9581caf448cd24`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=1093 bottom=2162` (a wide-body "Superpin" table like Indiana Jones), and every canonical coordinate is x/1093 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The manual's own switch-matrix and custom-column silkscreen prints "column 9" as addresses 91-98, and the custom-solenoid board prints items 37-42; neither is the PinMAME public address. CORE_CUSTSWCOL/CORE_FIRSTCUSTSOL arithmetic places them at public 121-128 and 51-56 respectively, and the retained known-working script's own Controller.Switch(122/125/126/127) assignments and SolCallBack(51-54)/SolModCallBack(55/56) registrations confirm the arithmetic directly at runtime.
- The switch-matrix opto shading (2-42) and PinMAME's sttngGameData inverted-switch mask agree on every single opto address (columns 3, 4, and 6 rows 1-7) -- zero polarity conflicts, unlike Monster Bash or Indiana Jones.
- Several switches have no dedicated playfield trigger object because the retained script sets their public state directly from a ball-stack class's internal counter (trough, Borg lock) or from a gun assembly's continuous rotation angle (gun Home/Mark) rather than from a Hit/Trigger event. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state; the projection notes are explicit that a motor's continuous rotation, not a solenoid pulse, drives the sensed position.
- GI addresses 1 and 2 ("Insert G.I.") drive only VR-backglass-room helper objects (VRBGGI*/VRBGGIarea*) in the retained table's own UpdateGI dispatch, confirming they are backbox-only circuits with no playfield bulb, matching the manual's own "Insert" (non-playfield) wording.
- GI addresses 0, 3, and 4 use the retained table's St1Shields/St4PFGI/St5ReLa emitter collections, keeping one member of each co-located Light pair at that object's own center (is_bulb_light first, then the smallest falloff radius, then the lexically first name) and excluding the side-wall reflection sprites swept into the ambient-dimming collection.
- Solenoid 7 (Knocker) is a backbox device (voltage and drive connections both on the backbox side of the harness) and takes a controlled `cabinet_or_service` record.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.
- Flasher glow sprites are render helpers, not sockets. Several sit on the cabinet side walls as reflections (f121 with f82s at x=0.998909; f125 with f52s, f85s and f86s at x=0.001161), and f128 has exactly the coordinates of solenoid 22's f122b. Every flasher placement now rests on a script-driven Light at a modelled dome or lens, or on a symbol in the factory drawings (flasher 28's lower bulb only on a leader endpoint, and therefore observed).

## Baked-mesh bulb covers (lamps 53, 26, 85, 86)

The bulb covers `l53yellow`, `l26blue`, `l85green` and `l86red` report position (0,0,0) because their geometry is baked into the exported mesh: each has size (1,1,1) and `rot_and_tra` X=90, so an OBJ vertex (x, y, z) is world (x, z) at height y. Control points for that mapping:

- `FlasherCapRed` [1027.88, 54.05] against Light l142 [1026.88, 54.5]
- `FlasherCapGreen` [152.47, 269.23] against Light l141 [156.02, 270.41]
- `borgshiporiginal` [643.84, 200.22] against Kicker BorgKicker (inside the ship) [642.72, 208.85]
- `Korpus` [1093.0, 2163.15] against table bounds [1093.0, 2162.0]

Each lamp is placed at its own mesh's bounding-box centre. Printed 2-41 draws 53 over 26 and 85 over 86 as two-socket brackets in an elevation inset, matching the meshes' height stacks. The 85/86 inset leader lands within 0.021 of the meshes. The 53/26 leader lands at (0.294, 0.178), across the left ramp, but printed 2-37's callout 22 (A-17330, lamp 53's own assembly) sits left of the ramp at about (0.158, 0.158), agreeing with the mesh, so the table position is kept and the 2-41 leader is recorded as a drawing inconsistency on the device. Lamp 26 now carries two placements: its centre insert and the sign bulb.

## Factory-drawing frame

Star_Trek_TNG_OPS.pdf PDF 93, printed 2-41, rendered at its native 308 dpi (2574x3622 px). Least-squares affine fit [x, y] = [px, py, 1] @ a on 16 printed insert centres against the retained table's lights of the same lamp numbers; RMS residual 0.0047, worst 0.01. Printed 2-37 and 2-45 reuse the artwork at the same scale with frame offsets [-520.5, 218.25] and [-5.25, 87.5] px, the mean shift of each page's left, right, outer-top and inner-top frame lines from printed 2-41's:

- printed 2-41 (PDF 93): left 1334.0, right 2347.5, top 449.0 (outer) / 470.0 (inner)
- printed 2-45 (PDF 97): left 1329.0, right 2342.0, top 536.0 (outer) / 558.0 (inner)
- printed 2-37 (PDF 89): left 813.5, right 1827.0, top 666.5 (outer) / 689.0 (inner)

The fit points all lie between x 0.40 and 0.84, so nine left-side lamps outside the fit check the extrapolation: the worst residual is 0.0161 (lamp 61, in x). Lamp 78's two sockets, the Borg flashers 26/27/28's bulbs and the holders of flashers 21/25 are measured on this frame and rounded to three decimals; the pixel readings are in the `lamp-locations-drawing` and `flasher-locations-drawing` excerpts and the reproduction script is retained in the working root's review artifacts.

## Changes in the 2026-09-25 pass

- Lamp 53: None -> [[0.159729, 0.173817]]. l53yellow baked-mesh centre; printed 2-37 callout 22 within 0.02; printed 2-41 inset leader disagrees (0.294, 0.178), recorded on the device.
- Lamp 85: None -> [[0.141092, 0.250557]]. l85green baked-mesh centre; printed 2-41 inset leader within 0.021.
- Lamp 86: None -> [[0.143581, 0.259851]]. l86red baked-mesh centre; printed 2-41 inset leader within 0.013.
- Lamp 26: [[0.50133, 0.621345]] -> [[0.50133, 0.621345], [0.161772, 0.174834]]. second bulb on the 53/26 sign bracket (printed 2-41 inset; NFadeObjm 26 l26blue baked-mesh centre).
- Lamp 78: [[0.5316, 0.10935]] -> [[0.784, 0.05], [0.407, 0.128]]. two printed 2-41 callouts on the Borg boards; printed 2-25 Red-Gry/Yel-Vio wiring; the old point was the centroid of five zero-intensity custom-model Lights.
- Solenoid 21: [[0.998909, 0.553857]] -> [[0.902, 0.563]]. holder symbol at the end of printed 2-45 item 21's short leader, mirroring flasher 25's holder, instead of the f121 right-wall reflection sprite; the wash Light l121 is 0.016 away.
- Solenoid 22: [[0.379666, 0.09429]] -> None. withdrawn: printed 2-45's item 22 callout forks into two prongs for one printed bulb, so neither prong nor their midpoint is a socket; the f122 glow sprite is not one either.
- Solenoid 23: [[0.2011, 0.53323]] -> [[0.342791, 0.552824], [0.505548, 0.525631], [0.654381, 0.552873]]. Lights ShieldGiBig8/10/7 driven only by Flash123; printed 2-45's three item-23 leaders within 0.02.
- Solenoid 25: [[0.001161, 0.610071]] -> [[0.108, 0.563]]. closed holder symbol at the end of printed 2-45 item 25's short leader instead of the f125 left-wall reflection sprite; the wash Light l125 is 0.023 away.
- Solenoid 26: [[0.808326, 0.068918]] -> [[0.755, 0.047], [0.809, 0.047]]. outer bulbs of the right Borg board measured on printed 2-41 (printed 2-25 Blu-Red wiring) instead of the f126 glow sprite.
- Solenoid 27: [[0.34538, 0.197502]] -> [[0.366, 0.1], [0.366, 0.156]]. upper and lower bulbs of the left Borg board measured on printed 2-41 (printed 2-25 Blu-Org wiring, printed 2-45 two item-27 leaders) instead of the f127 glow sprite.
- Solenoid 28: [[0.530916, 0.213812]] -> [[0.536, 0.053], [0.531972, 0.12796]]. item 16's flash lamp at the top of the Borg arch (device symbol on printed 2-41, validated) and the custom-model Flash128 Light l78a1, 0.009 from the lower item-28 leader endpoint (observed, because printed 2-25 draws the Borg kicker coil where that leader ends), instead of the f128 glow sprite that shares f122b's coordinates.
- Solenoid 51: unused, not_applicable -> [[0.450192, 0.395118]]. custom-board coil driven by UnderDiverterTop; kind corrected from motor to coil; projected onto Wall DiverterFRG.
- Solenoid 52: unused, not_applicable -> [[0.450256, 0.444442]]. custom-board coil driven by UnderDiverterBottom; kind corrected from motor to coil; projected onto Wall DiverterFLG.
- Solenoid 53: unused, not_applicable -> [[0.577522, 0.027112]]. custom-board coil driven by TopDrop.SolDropUp; kind corrected from motor to coil; projected onto the sw57 drop target.
- Solenoid 54: unused, not_applicable -> [[0.577522, 0.027112]]. custom-board coil driven by TopDrop.SolDropDown; kind corrected from motor to coil; projected onto the sw57 drop target.
- Solenoid 55: unused, not_applicable -> [[0.142741, 0.125072]]. Light l141 inside the FlasherCapGreen dome, not the f141 glow sprite the curator carried unemitted; printed 2-45 item 41 within 0.023.
- Solenoid 56: unused, not_applicable -> cabinet_or_service. printed 2-45 labels item 42 "(On Back Panel)"; the FlasherCapRed dome with Light l142 at (0.939505, 0.025209) is a rear-edge proxy and is not promoted.
- Lamp 13: [[0.396539, 0.6691]] -> [[0.396539, 0.6691]]. position kept, status validated -> conflicted: printed 2-41 puts 13 on the insert the table gives 14 (conflict.ship-mode-1-2-insert-positions).
- Lamp 14: [[0.338957, 0.621082]] -> [[0.338957, 0.621082]]. position kept, status validated -> conflicted: printed 2-41 puts 14 on the insert the table gives 13 (conflict.ship-mode-1-2-insert-positions).

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
- Solenoid 51: Projected onto the retained table's Wall DiverterFRG (drag-point centroid), the object UnderDiverterTop drops and raises; the diverter flap itself works under the playfield.
- Solenoid 52: Projected onto the retained table's Wall DiverterFLG (drag-point centroid), the object UnderDiverterBottom drops and raises; the diverter flap itself works under the playfield.
- Solenoid 53: Projected onto the top drop target it raises (retained table Wall sw57, drag-point centroid), so it shares switch 57's coordinate.
- Solenoid 54: Projected onto the top drop target it lowers (retained table Wall sw57, drag-point centroid), so it shares switch 57's coordinate.

## Open questions

- Solenoid 20 (Jets Flasher) sits on Light l120, within 0.0007 of lamp 83's insert; printed 2-45 draws the item 20 balloon beside the jet bumpers but its leader cannot be separated from the bumper art.
- Solenoid 15 (Top Divertor) uses the Flipper-typed Diverter object whose y (-0.008688) is clamped to 0.
- Solenoids 9/10, 51/52 and switches 57, 74/75 use drag-point centroids of one Wall or Rubber object each. Every GI placement is one retained Light's own center (from each co-located bulb/glow pair, the is_bulb_light member with the smallest falloff radius, then the lexically first name); the lbumperr GI bulbs sit under the jet-bumper caps, within 0.002 of the bumpers' own coordinates.

## Counts

- Placements: 207
- Located input addresses: 62
- Located output bindings: 101
- Located output bindings that are only observed: 3
- Inputs with a controlled `cabinet_or_service` record: 17
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 5
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `unused` record: 3
- Outputs with a controlled `virtual` record: 14
- Unresolved output placements: 1

## Promotion decision

No address-enumeration gap or polarity conflict remains anywhere in this definition, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. The record stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`:

- Solenoid 22 (Middle Ramp Flasher): no placement. Printed 2-45's item 22 callout forks into two prongs in the wire-ramp art, at (0.356, 0.053) and (0.389, 0.054), while the solenoid table prints one #89 playfield bulb and no bulb symbol is drawn under either prong; the retained table models only glow sprites. The midpoint the previous pass used is withdrawn.
- Solenoid 28 (Center Borg Flasher): observed. The upper bulb is item 16's single flash lamp at the top of the Borg arch, a validated device symbol at (0.536, 0.053); the lower item-28 leader ends at (0.533, 0.137) on a part printed 2-25 identifies as the Borg kicker coil (DETAIL 1, Brn-Gry), so item 17's flash lamp is not drawn, and the second placement is only the table's custom-model Flash128 Light l78a1, 0.009 from that leader endpoint.
- Lamps 13 and 14 (Ship Mode 1/2): conflicted. Printed 2-41 labels the two ring inserts the other way round from the retained table (conflict.ship-mode-1-2-insert-positions).

Promotion needs the Middle Ramp Flasher's socket and the Center Borg Flasher's lower bulb, from a photograph of the ramp area and the Borg bracket or a service drawing that shows those bulbs, and the ship-mode ring order for lamps 13 and 14, from a lamp test on a real machine or a harness run.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/extracted-vpxtool.manifest.json`, SHA-256 `c913342c6421558eead345703d08105db5b2779e936f898e56ec1fd177249542`, 1585 files, 247600334 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `07f57792c7f405a5e59607a73ac73bb00f9b7daa91ede63477337d4a9ce8f948`.
- Committed drawing excerpts: `lamp-locations-drawing`, `flasher-locations-drawing`, `borg-bracket-assembly`, `upper-playfield-parts-drawing`.
