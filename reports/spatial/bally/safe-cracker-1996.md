# Safe Cracker (Bally, 1996) spatial blockers

Retained VPX SHA-256 `3f1e77be9e64dc202576dec9c07681e40b19c3e666824b0d3b85267358ac645b`; script `e224e815280ce8e74ec1d2dfe1562dee9e5675b3f379cb5031ff69c39007fa0a`; 825-file extraction manifest `1746e58c6a386940c6692454ecbadc149c694bd64a25b8bac07a1b93d5a007a3`; manual `a51dd1611ff135878d082f124aafa215907ff0f13b4dd105f9e6c4864de01c04`.

Bounds: `left=0 top=0 right=862 bottom=1875`. Every canonical coordinate is x/862 and y/1875 rounded to at most six places.

## Placement status

- `validated`: 56 devices
- `observed`: 89 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 108
- used devices with no placement record: 3 (`gi.string-1`, `gi.string-3`, `switch.matrix-42`)

## Projection classes

- **switch:** The retained table's object for the switch (trigger, target, kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are the trough slot kickers; the lock optos 36/37 are projected onto the hidden lock trigger that writes them; the moving-target optos 56-58 onto the target's pivot and the spin-disc optos 85/86 onto the disc centre, because the table derives those switches from the mechanism's motion.
- **lamp:** The script-bound Light's own centre (for 27 and 28 the crossed lights the script binds), the bumper-cap lights for 81-83 and the world-space mesh centres of the baked lamp primitives for 84-87; observed only, because the lamp drawing is a symbol diagram with no flipper or other mechanism feature a control fit can use. The 48 backbox lamps are not applicable (backbox).
- **solenoid:** The object the solenoid callback moves (kicker, flipper, plunger, lock pin, diverter pivot, moving target) or, for the slingshots and jet bumpers, the object that fires the coil, the middle target of each drop bank for its reset coil, and the Flupper dome base each flasher callback lights (two bulbs for 18); validated where the solenoid drawing's callout agrees.
- **gi:** None: the retained table drives all its GI bulbs from public GI 0 and has no consumer for the other strings, so it cannot tell string 1's bulbs from string 3's, and no retained drawing or count locates GI bulbs. Strings 2, 4 and 5 power the backbox lamps only and are not applicable.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 57 of the 67 table placements it checks ([seed](../../../tools/seeds/bally/safe-cracker-1996-callouts.json)); the rest keep their observed status:

- `device.auto-plunger.effect`: callout 35 on 2-45, 0.110 normalized away.
- `device.bank-kick.effect`: callout 5 on 2-45, 0.147 normalized away.
- `device.ramp-diverter.effect`: callout 7 on 2-45, 0.080 normalized away.
- `device.top-popper-eject.effect`: callout 25 on 2-45, 0.178 normalized away.
- `device.trough-eject.effect`: callout 9 on 2-45, 0.091 normalized away.
- `switch.matrix-12.sensor`: callout 12 on 2-43, 0.112 normalized away.
- `switch.matrix-73.sensor`: callout 73 on 2-43, 0.139 normalized away.
- `switch.matrix-77.sensor`: callout 77 on 2-43, 0.077 normalized away.
- `switch.matrix-78.sensor`: callout 78 on 2-43, 0.071 normalized away.
- `switch.matrix-83.sensor`: callout 83 on 2-43, 0.091 normalized away.

## Unresolved physical geometry

- General illumination strings 1 and 3 (public GI 0 and 2) light #44 playfield bulbs, but neither the retained table nor any retained drawing or count says which bulb belongs to which string, so they have no placement.
- The left big kick opto (switch 42) has no table object: the v1.0 script's VariTargetTimer_Timer derives it from a ball-position rectangle (raw 50,1005 to 100,1055; the v2.0.0 script uses 50,990 to 110,1055) around the LeftKickBack kicker, a script surrogate rather than the opto, so it has no placement. The switch drawing's callout 42 marks it at the left kickback lane; placing it from the drawing needs a reproducible measurement under the spatial measurement rule.
- The lamp drawing (2-47) cannot validate lamp placements: it shows lamp symbols in an outline with no flippers or other mechanism feature for an independent control fit, so every lamp placement stays observed.
- Placements the switch and solenoid drawings do not confirm keep their observed status; the drawing callout check lists them with the distance or reason.

## Promotion decision

partial: every fitted playfield device has an observed or validated placement or a controlled not-applicable record except the general-illumination strings 1 and 3, whose bulbs no retained source assigns to a string, and the left big kick opto (switch 42), which the retained table only synthesises from a ball-position rectangle.
