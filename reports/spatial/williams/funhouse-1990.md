# FunHouse (Williams, 1990) spatial review

Status: partial. The physical machine record lives at `machines/partial/williams/funhouse-1990.json`.

The matching source is the retained known-working `Funhouse (Williams 1990)_1.3.vpx` at SHA-256 `69c37fa9a84e669a2934d6da0e5ee0277c4a0ef01e71eaa19e7271ba3396873e`. Its embedded script at SHA-256 `322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863` is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Williams manuals are the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The original operations manual has a usable but column-scrambled text layer, so its tables were read from rendered page images. The supplied November 1990 handbook was likewise visually checked at 250 dpi, with 600 dpi crops for small callouts.
- FunHouse's switch matrix has exactly two opto positions (51 and 55), both marked `(opto)` in the manual and both normalized by pinned PinMAME's inverted-switch mask.
- Lamp 12 is `Gangway 100,000`: two Williams lamp-matrix pages and the physical playfield photograph agree, resolving the older lamp-location page's isolated `10,000` as a typo.
- The handbook's lamp-location drawing identifies lamps 56, 55, and 54 as the top, middle, and bottom sockets in the Steps stack. The retained table's `_finger_1` objects are the physical hotspots; `_finger_2` through `_finger_4` are render layers.
- Printed flasher 20 has two Superdog bulbs. The retained table supplies distinct F20 and F20a objects, and the pinned community script assigns both to output 20, so both physical sockets retain their own measured coordinates.
- Switch 63 is placed on the retained `ballrelease` kicker because the handbook locates it at the right trough and the script asserts and clears that exact switch as the kicker receives and releases the ball.
- Runtime G.I. names and grouping follow the known-working script. GI_Upper's 19 render objects form 15 physical hotspots and GI_Lower's 45 render objects form 14; each coordinate is an actual smallest-radius named light, never a centroid.
- FunHouse is pre-Fliptronics WPC-Alpha hardware. It has lower-right, lower-left, and upper-left direct-wired physical flippers. PinMAME publishes two button-driven synthetic sides at 45-48 for digital animation; the left callback drives both fitted left bats, and those virtual states have no playfield coordinates of their own.
- Printed G.I. circuit 04 is a mixed center-backglass/right-rear-playfield branch. The playfield emitters are not identified by any retained known-working table, so output G.I. address 3 remains deliberately unresolved.

## Explicit projections

- pinmame.input.switch 76: Projected onto the trap door primitive's own rotation state (PrTrap.RotX); the retained script sets this switch programmatically rather than reading a separate contact-switch object.
- pinmame.output.solenoid 5: Projected onto the trap door primitive; open/close solenoids share the mechanism's own position with switch 76.
- pinmame.output.solenoid 6: Projected onto the trap door primitive; see solenoid 5.
- pinmame.output.solenoid 3: Projected onto switch 46's position; the retained script's bsHideout saucer helper shares switch 46's own kicker object.
- pinmame.output.solenoid 16: Projected onto switch 65's position; the retained script's bsRudy saucer helper shares switch 65's own kicker object.
- pinmame.output.solenoid 8: Projected onto switch 28's position; the retained script's MBRelease handler acts directly on the WaSw28 lock-wall object with no separate release-mechanism object.
- pinmame.output.gi 1: Projected onto Rudy's own sign/shade assembly (RudySign1, RudySign2, RudyShade); the retained script's GI Case 1 drives that collection directly rather than a generic playfield wash.
- pinmame.output.solenoid 21: Projected onto switch 51 (Dummy Jaw); no dedicated jaw-motor VPX object was identified separately from Rudy's head figure.
- pinmame.output.solenoid 22: Projected onto switch 51 (Dummy Jaw); see solenoid 21.
- pinmame.output.solenoid 25: Projected onto switch 51 (Dummy Jaw); the only fixed point recorded for Rudy's Head Assembly.
- pinmame.output.solenoid 26: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.output.solenoid 27: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.output.solenoid 28: Projected onto switch 51 (Dummy Jaw); see solenoid 25.
- pinmame.input.switch 73: Projected onto the retained table's Drain kicker object, shared with the outhole solenoid (1).

## Counts

- Placements: 180
- Located input addresses: 47
- Located output bindings: 93
- Unresolved input addresses: 0
- Unresolved output bindings: 1
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 16
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `virtual` record: 21

## Promotion decision

The record remains `partial`: its public contract, semantics, wiring, mechanisms, variants, and recreation knowledge are validated, but the individual right-rear-playfield emitters on mixed G.I. address 3 cannot be placed without guessing. `coverage.missing` is exactly `["spatial_placement"]`; a socket-level circuit-04 survey is the concrete promotion requirement.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json`, SHA-256 `85620e05458bd72bc57c2e203001a0f35db9806431e66e07ee08f05e90346ba9`, 2212 files, 219908807 bytes.
- Human transcription of every printed table read from the rendered original manual pages: `external:pinmame-review-artifacts/funhouse/manual-transcription.md`.
- Maintainer-supplied November 1990 operator handbook SHA-256 `bb30eacaac0ee7001f59339102da5a1bfe528c2a4dbd63d2247e00fba89f1b13` and lower-playfield photograph SHA-256 `b56821de487adc55f128e4a94d8d55a4ef2c2e23cd1c0291f1118363c6ecaa81`.
