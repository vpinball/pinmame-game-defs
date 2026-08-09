# Playboy 35th Anniversary spatial-resolution report

Exact retained-table bounds: `left=0`, `top=0`, `right=952`, `bottom=1974`.

Both extents are asserted, and no other machine geometry was reused.

## Extraction identity

- Manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Manifest SHA-256: `408ba0ec4e18187f0f86c1970c33cc31b93af53df24ad83f2eeea599822bb672`

## Promotion decision

Keep partial. The record enumerates every public address and resolves the major topology, but output annotations/typing, physical polarity, special-coil behavior, lamp socket placement, and ten preserved conflicts prevent author-ready promotion.

## Blockers

### controller_platform

Data East uses a System 11-derived emulator implementation, but its board family and diagnostics are not represented by the Williams-only pinmame.system-11 profile.

Would resolve: A reviewed Data East controller profile derived from the pinned core and original board documentation.

Devices: `pinmame.dataeast`

### output_semantics

Callback aliases/comments disagree with printed groups, one public special-solenoid state is also a background proxy, core PWM typing disagrees with the physical C-bank fitment, and unfitted address 31 lacks a decoded-state trace.

Would resolve: Original-machine lamp/coil-test video synchronized with public output traces and a harness endpoint survey.

Devices: `coil.driver-4`, `coil.driver-5`, `coil.driver-13`, `coil.driver-14`, `coil.driver-15`, `coil.driver-19`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-30`, `coil.driver-31`, `coil.driver-32`

### mechanism_behavior

Script establishes event edges but not the hidden Grotto transfer geometry or hardware-triggered special-coil pulse behavior.

Would resolve: Original-machine captures of the Grotto ball path and each special-solenoid switch/coil waveform.

Devices: `mechanism.grotto-kicker`, `mechanism.left-slingshot`, `mechanism.right-slingshot`, `mechanism.left-pop`, `mechanism.center-pop`, `mechanism.right-pop`

### polarity

The core publishes cabinet buttons at manual EOS addresses and decoded mux states, but no at-rest/end-of-stroke or relay electrical trace proves physical polarity.

Would resolve: Bench capture of cabinet button, EOS, K1 relay, raw A/C driver and public output states.

Devices: `switch.matrix-15`, `switch.matrix-16`, `coil.driver-10`, `coil.driver-45`, `coil.driver-46`, `coil.driver-47`, `coil.driver-48`

### spatial_placement

Lamp and mechanism coordinates remain retained-table candidates; the manual supplies broad flash groups and backbox/playfield splits but not registered socket centers, and seven routed PINBALL lamps have no physical location in its drawing. Output 12 is classified as backbox-only and needs no playfield coordinate.

Would resolve: A dimensionally registered original playfield/backbox survey or address-by-address photographs correlated with lamp, coil, and mechanism tests.

Devices: `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-56`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`, `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-9`, `coil.driver-11`, `coil.driver-13`, `coil.driver-14`, `coil.driver-15`, `coil.driver-16`, `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-21`, `coil.driver-22`, `coil.driver-25`, `coil.driver-26`, `coil.driver-27`, `coil.driver-28`, `coil.driver-29`, `coil.driver-30`

### unresolved_conflicts

Ten machine-specific source disagreements remain first-class and promotion-critical.

Would resolve: Independent original-machine observations or corrected authoritative sources that explicitly settle each recorded conflict.

Devices: `conflict.shared-port-position-2-vs-unfitted`, `conflict.left-eos-vs-public-button-state`, `conflict.right-eos-vs-public-button-state`, `conflict.shooter-laser-switch-part-numbers`, `conflict.outputs-4-and-5-share-pseudo-lamp-105`, `conflict.outputs-13-through-15-script-comments-vs-manual`, `conflict.muxed-c-bank-core-bulb-type-vs-manual-coils`, `conflict.drop-reset-coil-type-print`, `conflict.special-solenoid-19-vs-background-proxy`, `conflict.flash-location-drawing-vs-playfield-proxies`

## Resolver controls

- Asserted both exact gamedata.json bounds (0,0)-(952,1974) before normalization; neither dimension permits borrowing geometry from another machine.
- Read every decisive switch-, lamp-, and coil-table cell from rendered manual pages. Text extraction and OCR were only location and second-reading aids.
- Established runtime visual consumption only from executable SetLamp callbacks and UpdateLamps routing after whole-line VBScript comments were removed.
- Treated numeric object names as candidates. Explicit routing establishes a consumer binding, but object centers remain candidate physical placements unless an executable sensor supplies observed geometry.
- Used script for causal topology and rendered manual construction pages for assemblies. A printed feature label alone never created a mechanism edge.
- Used the printed-page-26 coil/flash plan and separate backbox inset for physical-plane classification and broad feature locations. Repeated group callouts, unresolved small inset digits, and the unregistered drawing frame do not provide normalized socket centers; disagreements with retained playfield effect objects remain explicit.

## Excluded helpers

- `numeric-light-gap`: The nine absent numeric Light names are 26, 32 and 57-63. Each address is explicitly routed to a same-number Flasher proxy and the manual places it in its separate backbox/back-panel box; none is a missing controller output.
- `pinball-backglass-row`: Same-number Light objects 41, 49, 53-56 and 64 are executable consumers and are flagged is_backglass=true, but the manual location drawing does not show those seven addresses in either its backbox box or playfield plan. Their presentation-row centers are withheld because no physical source establishes the socket plane.
- `laser-helper`: The off-bounds sw17 helper and unbound visible sw17a are excluded. Kicker001_Hit explicitly publishes switch 17 from an in-bounds kickback object, whose center is retained at candidate strength.
- `gi-and-flash-proxies`: The 47 aGiLights entries and grouped flasher objects are visual effects, not surveys of physical bulb sockets.
- `synthetic-flipper-states`: Public outputs 45-48 are PinMAME-generated winding states mapped to two physical flipper assemblies. They are virtual addresses with no independent quantity or placement.
