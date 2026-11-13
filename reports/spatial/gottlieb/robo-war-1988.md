# Robo-War spatial evidence

Coverage: **partial**. Do not promote: the trough switch, the playboard tilt contact, the playboard GI and the six #67 flashers sharing coil outputs have no placement, and the shooter-lane rollover, the outhole and right flipper switches, the left drop target's switch 43, the flashers on solenoids 4 and 7, the projected lamps and the coil anchors stay observed.

One normalized playfield: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron. Table bounds (0,0)-(1024,2240) from the retained extraction's gamedata.json; normalize by those bounds and round once to six decimals.

88 placements; 29 validated by the folio 48 callout check (29 of 32 checked), the rest observed.

## Remaining requirements

- Trough switch 56 has no table object (the script models the trough as a ball stack) and the factory drawing prints SW 56 without a leader beside the right return-lane rail, so its contact under the apron is unplaced.
- GI 0 (6.3 V playboard illumination through relay T) has no socket list in the retained manual pages and the table's GI collection is a render group, so no GI emitter is placed.
- No light in the retained table shows a bulb, so no lamp socket is measured. Each insert lamp's script-bound light is a textured overlay of its insert, and the bulb-mode lights the script also fades with lamps 5-11 and 19-22 (l5a-l11a, l19x-l22x) are glow lights 27-42 units beside their inserts; the reflection lights l32sc, l35sc, l37sc and L38sc lie outside the playfield on the side walls. Every insert lamp is projected onto its insert's centre (both bulbs of each multiplier lamp 15-18 onto their one oval) and each pop-bumper lamp onto its bumper's centre; all 41 lamps stay observed until their sockets are measured.
- The playboard tilt contact on switch 57 (part 9141), which the drawing prints without a leader in the drain area, has no table object and is unplaced; the two cabinet tilt contacts on the same address need no placement.
- The flashers on solenoids 4 and 7 are placed on the script-bound RPF and LPF lights and stay observed: the drawing prints SOL.4 and SOL.7 #67 without leaders, so no callout checks them.
- The left drop target's switch (43) stays observed: the drawing prints a second SW 42 at that target and no SW 43, so its callout cannot check it.
- Solenoids 1, 2, 5 and 6 also light the four dome flashers, and solenoid 3 the two Stargate flashers, when relay S is energized. The schema allows only effect placements on a coil output, so these #67 sockets have no placement; their drawn positions are in the knowledge note, and the table's dome objects LF61-LF63, RTF and the SGP lights are render helpers.
- The shooter-lane rollover (36) table trigger lies 0.098 normalized from the drawing's SW 36 callout, beyond the 0.07 limit, and stays observed. With only switch callouts left in the callout fit, the outhole (66) and the right flipper switch (46, projected onto the right flipper pivot) land 0.074 from their callouts under it, just beyond the limit, and stay observed too.
- Coil effect anchors (bank resets, hole, outhole, ball release, Stargate ramp) are placed on the mechanism the coil drives, not on a measured coil, and stay observed; the drawing marks none of these coils.

## Evidence and transformation

vpxtool git:v0.33.3 extracted the retained table completely with a canonical manifest. The embedded script's bindings choose each object; the session's extract_objects.py dumps every object's kind, stored point and file digest to objects.json, and the spatial-mapping excerpt lists every placement's object, raw point and normalized value. The factory location drawing on folio 48 was read independently (107 callouts) and fitted on its three pop-bumper caps and two flipper pivots (control RMS 0.003) and on its own callouts; agreeing placements are validated by tools/drawing_callouts.py.

- Bank reset coils are effect anchors at the mean of their targets' raw positions; the hole, outhole and ball-release coils at their kickers; the Stargate ramp coil at the drag-point centroid of the ramp. All stay observed.
- The kicking-rubber scoring switch (33) has one placement per kicking rubber at the slingshot wall's drag-point centroid; the right flipper switch (46) is placed on the right flipper pivot.
- The flasher outputs 4 and 7 are placed on the script-bound RPF and LPF lights; the drawing prints SOL.4 and SOL.7 #67 beside them without leaders.
- Each insert lamp is projected onto the centre of the script-bound light covering its insert; each multiplier lamp 15-18 has two placements there, one per bulb. Each pop-bumper lamp 45-47 is projected onto the centre of its Bumper object. None is a socket and none is checked against the drawing.

All raw coordinates and exact object bindings are retained in the machine's spatial-mapping excerpt. Coordinates are rounded once to six decimals. No render helper is counted as a physical socket.
