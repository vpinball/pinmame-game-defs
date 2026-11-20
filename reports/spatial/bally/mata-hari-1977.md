# Mata Hari spatial blockers

**Partial.** The machine definition records player-view
geometry from exact retained VPX objects. The factory location
drawing validates sixteen switch anchors. Other VPX anchors
remain observed. The photos distinguish physical fixtures from
render effects.

## Sources and transform

The two retained binaries are `Mata Hari (Bally 1977).vpx` and
`Mata Hari (Bally 1978).vpx` under
`vpx-sources/bally/mata-hari-1977`. Both use the same JPSalas
lineage, bounds `(0, 0, 952, 1927)`, and `matahari` ROM.
Player-view positions use the repository helper, with x/952,
y/1927 and six decimal places. The 1978 model supplies the retained
anchors. Its 1977 counterpart shows the lower bumper light meshes
at the same centres and supplies a lineage cross-check. The JSON
report gives both binary, script and full-extraction manifest
digests, counts and exact objects. [Spatial report data](mata-hari-1977.json)

UnclePaulie's independently placed v2.0.0 table supplies a third set of
model positions. Twenty round-insert controls transfer those positions
into the canonical 952 × 1927 frame. The fit has 0.729 VPU RMS and a
maximum leave-one-out distance of 6.793 VPU. Side and apron projections
extend beyond the calibration controls. Keep them observed.
[Independent fixture evidence](../../../evidence/excerpts/bally.mata-hari.1977/vpx-fixtures.md)

The full extraction hashes are recalculated by
`tools/build_external_evidence_manifest.py` from every retained
file, excluding the two manifests themselves. [VPX binding evidence](../../../evidence/excerpts/bally.mata-hari.1977/vpx-bindings.md)

## Factory register

Use the FO 579 printed-page-18 render (PDF 23) at 1530×1980.
Seven visual controls are the four thumper rims, saucer centre
and flipper pivots. The seed records manually read pixels, the
render hash and each VPX control object. The repository checks
the drop faces and rollover slots against the independent control
fit and the leave-one-out callout fit at 0.07 normalized. The
VPX coordinates supply the stored points. Both scripts reverse
the right bank. The right-side switch positions follow the
factory callouts using Target9/8/7/6 for 17/18/19/20.
[Factory drawing](../../../evidence/excerpts/bally.mata-hari.1977/factory-locations.md)

## Admitted anchors

- The hit-target and rollover centres have factory corroboration.
  Upper, slingshot-style wall centroids model the
  two physical rebound contacts on switch 27. The two lower wall
  centroids and four bumper centres stand in for their compact
  switch and actuator assemblies. The exact leaf mounting points
  remain unmeasured.
- The saucer uses the cup centre for both the ball sensor and
  the effect anchor. The outhole uses the drain position for
  the sensor and the kicker effect. `BallRelease` is a script
  feed proxy. The lower flippers use their pivot coordinates as
  effect anchors.
- The round bonus, award, two outlane, credit and drop-special
  fixtures each use one centre. Factory load rows and top photos
  distinguish them from the nearby lit artwork. The apron credit
  emitter uses the independently modeled `Bulb_Prim_028` at
  `(0.162939, 0.874696)`, projected into the canonical frame. Its
  two model lights and raised lens share that location. The original
  photo shows a nearby wired socket. Do not count the primitive's
  membership in the author's GI collection as another emitter.
  The lower thumper lamp anchors use the cap centres supported
  by the earlier build's bulb meshes, A6 wiring and photos.
  Their positions remain observed. Stock A/B gameplay confirms
  that 41 and 57 both publish. In five-ball play the left cap lights
  first. The factory assigns 41 to the right cap and 57 to the left.
- The original underside photo locates switch 7's weighted panel
  contact at its two-screw mount. Its observed projection is
  `(0.222, 0.578)`. The other two tilt contacts are cabinet-mounted.
  The same photo supports reset effect anchors `(0.14, 0.44)` and
  `(0.76, 0.45)` for public 13 and 15. Factory callouts identify
  the outer ends of the banks within 17 VPU per axis of those reads.
  The oblique exposures leave uncertainty in the actual coil axes.
- For 60, 44, 28 and 43, the measured underside socket apertures
  support the VPX arrowhead-side objects. Omitting the forward 1K
  control changes the factory-aperture fit by at most 6.2 VPU in x
  and 11.6 VPU in y and preserves all four choices. The complete
  fit's maximum leave-one-out component is 54.2 VPU in y at that
  1K control. The replacement panel and production photo provide
  separate views of these socket regions.
- The upper round and side arrow inserts for 36 and 52 each use
  two placements per letter. The potential lamps 26, 42 and 58 use
  one arrowhead-side placement each. The independent table models
  seven discrete bulbs at these anchors. The production art shows
  the corresponding seven inserts. The original underside does
  not show every terminal. [Fixture register](../../../evidence/excerpts/bally.mata-hari.1977/fixture-photo-register.md)
- Physical coin, service and backbox devices have controlled
  `not_applicable` records. Desktop proxy lights and the rendered
  segment layout represent displays and lamps outside the playfield.

## Remaining physical placements

- The observed reset projections and remaining modeled switch,
  coil and lamp locations need validation against physical fixtures.
  The five upper arrow and A/B circuits retain their observed
  anchors pending an underside wire-to-socket view.
- The factory 5.9 VAC playfield GI bus has no public address. The
  original underside shows four lower side-guide sockets with visible
  leads at the positions recorded in the JSON. The independently
  modeled rear-right bulb has a corresponding wide bore and a
  restoration photo shows an offset socket at a similar opening.
  The restored #3 photograph shows the fourth upper `3000` arrow
  and both yellow upper bumper caps lit. The independent recreation
  models all three in GI and their factory feed remains inferred.
  The complete original underside, including the apron, and the
  branch wiring are still needed for a factory socket count and
  complete placement inventory. [Lamp wiring](../../../evidence/excerpts/bally.mata-hari.1977/lamp-wiring.md) ·
  [Photo and VPX evidence](../../../evidence/excerpts/bally.mata-hari.1977/vpx-fixtures.md)
