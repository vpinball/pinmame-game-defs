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

The full extraction hash is recalculated by
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
  distinguish them from the nearby lit artwork. The apron
  credit indication is a physical lens on the assembly.
  The lower thumper lamp anchors use the cap centres supported
  by the earlier build's bulb meshes, A6 wiring and photos.
  Their positions remain observed. Stock A/B gameplay confirms
  that 41 and 57 both publish. The factory assigns 41 to the
  right cap and 57 to the left.
- Physical coin, service and backbox devices have controlled
  `not_applicable` records. Desktop proxy lights and the rendered
  segment layout represent displays and lamps outside the playfield.

## Remaining physical placements

- Switch 7 includes an under-playfield contact in parallel with
  two cabinet tilt contacts. Its normalized mounting position
  remains unknown.
- Reset outputs 13/15 control the two four-target banks.
  The partial underside image does not establish the number and
  position of the installed coil fixtures on each branch.
- A/B lamps 36 and 52 each have two physical positions on the
  factory A5/A6 drawings. The photo shows a distinct top and
  side insert for each letter. The two side lights overlap
  one silhouette. A clear underside image is needed to match
  the VPX centres to actual sockets.
- Potential arrows 26/42/58 and bonus/award arrows 28/43/44/60
  have render overlaps. Their individual lamp circuits are
  known and their socket centres remain unresolved. The
  unlabeled upper centre shape has no established ROM-controlled
  lamp. [Lamp evidence](../../../evidence/excerpts/bally.mata-hari.1977/lamp-wiring.md)
- The 5.9 VAC playfield GI bus has no public output. Its
  physical sockets require a complete underside with visible
  lamp harnesses or a factory socket-location drawing. The
  candidate lists preserve VPX bulb-mesh objects for later
  inspection. The VPX-only off-rail `Light4`/`Light5`, the
  upper bumper cap effects and near-duplicate
  `GI_Bulb31`/`GI_Bulb32` are insufficient to count fixtures.
