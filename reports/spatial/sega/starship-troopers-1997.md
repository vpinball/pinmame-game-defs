# Starship Troopers (Sega, 1997) spatial blockers

Retained VPX SHA-256 `0d7020ac848dc66f12d5faf2a12961bde69a606d154511947755bd0ac9b4731a`; script `e97088ef82faf82205fbb080dac0f8489370ec03364cedc7d5b3f26bd5b03c3a`; 1294-file extraction manifest `8b75f4b4810f47bfdfc06598e46e89a7a6891494808e7a23a9bbc74e73739cde`; manual `0b773570c3ddaa38f6d63f7a590d4a8986f34facf70064cf3446cfc44ae22d09`.

Bounds: `left=0 top=0 right=952 bottom=2133.17`. Every canonical coordinate is x/952 and y/2133.17 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 154 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 57
- used devices with no placement record: 4

  - `device.q23-brain-bug-flashers-x2`
  - `device.q30-f6-left-ramp-flashers-x4`
  - `device.q31-f7-right-ramp-flashers-x4`
  - `device.q32-f8-pop-flashers-x2`

## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, target wall, kicker, bumper). The trough switches, which the table does not model, are projected onto the release kicker BallRelease; the under-trough switches onto the hole objects that pulse them; the stepper end switches onto the end walls the warrior bug mech raises and the bug target onto their midpoint; the brain bug switches 37 and 39 onto the wall sw38a; each end-of-stroke contact onto its flipper; and the slingshot switches onto the slingshot wall on the manual's side, across the table's crossed handlers.
- **lamp:** The 42 lamps DR. 5 draws below the playfield are projected onto the bulb light UpdateLamps drives for each, at the insert it lights: the table models no bulb or socket under the playfield, so each point is the insert's position, not a measured socket. The lamps whose Lights sit on a bulb the table models (the turbo bumpers 28-30, the ramp nukes 47 and 48 and the Tanker Bug sign's 35, 36 and 39) are placed at the centre of that bulb's piece of the world-space mesh export, which they cite with its height; the sign stands upright, so its lamp 39 is the bulb below 35 and 36, as the Tanker Bug Assembly (printed pages 59 and 61) and DR. 5 draw it. Each 7-segment LED segment is the lit centroid of its segment texture on the Flasher quad UpdateLamps drives, checked against the A-G key and the two-by-two layout on DR. 5. Lamp 34, which the table does not bind, is projected onto the rearmost bug wall at the head of the warrior bug track.
- **solenoid:** The kicker, bumper, slingshot wall or flipper the script fires, the magnet triggers, and for a flasher each script-driven Light that sits on a part the table models. No flasher Light draws a bulb mesh of its own, so the world-space mesh export decides: each of the sixteen F1-F4 Lights sits on one Caps<Color> Mini-Mars dome and one KabeSockel socket piece (0.3-7.7 VPU from their centres), and F5's l129 and l129a each sit on one of the two bulbs modelled on WarriorBugAssembly006 (5.1 and 7.4 VPU); each is placed at the centre of that socket or bulb piece, not at its render Light. The brain bug, ramp and pop flasher Lights (l123a, l123b, l130b-l130d, l131b-l131d, l132) sit on no modelled bulb, dome or socket and place nothing, and neither do the table's VPX Flasher glow sprites (lf129, f130a-f130d, f131a-f131d, lf132 and the strobe overlays) or the wide-falloff ambient lights l129b, l130e and l131e. The auto launch is placed on the table's Plunger, the brain bug coil on the wall sw38a and the four stepper phases on the rear wall BWall24, where the Warrior Bug Assembly drawing mounts the motor, each projection citing the manual drawing that locates the part.
- **gi:** The 28 Light members of the table's GILamps collection, each drawing its bulb; observed only, without per-circuit assignment.

## Unresolved physical geometry

- The trough switches 12-15 and the under-trough switches 9, 10 and 40 are not modelled as switches by the table; their placements are projections onto mechanism and hole objects.
- The warrior bug's stepper motor and end switches, its target, the brain bug coil and its two up switches are projections onto the walls the script moves, not the parts under or on the playfield.
- Lamp 34 is unbound in the table and projected onto the bug track's rear wall from the lamp location drawing.
- The 42 insert lamps DR. 5 draws below the playfield (43 bulbs) are projected onto the bulb lights the table drives at their inserts; the table models no bulb or socket under the playfield, so their sockets are not measured.
- Each 7-segment LED segment is placed at the lit centre of the table's segment texture, which agrees with the manual's A-G key but was not measured on a real display; the four one-inch displays sit over the flippers.
- Flasher bulbs without a placement: the brain bug flasher (Q23) 0 of 2 placed; F5 (Q29) 2 of 4 placed; F6 (Q30) 0 of 4 placed; F7 (Q31) 0 of 4 placed; F8 (Q32) 0 of 2 placed. The table models none of these bulbs, only render lights and glow sprites near some of them, and the flash lamp location drawing (DR. 7) has not been measured for them.
- No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.
- The table models 28 G.I. sockets against the 34 playfield bulbs the G.I. page prints. That page gives each bulb's circuit and a broad region (upper or lower, left or right), not a socket position, so the six sockets the table lacks need a factory G.I. socket drawing or photographs of a real playfield.

## Promotion decision

partial: the brain bug, ramp and pop flashers have no placement, and projections and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.
