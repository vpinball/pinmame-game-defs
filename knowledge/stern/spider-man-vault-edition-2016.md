# Spider-Man Vault Edition

Coverage: **author-ready - full normalized spatial placement validated.**

This note supplements the canonical definition with the physical and behavioral information an author needs to reproduce the table. The adjacent JSON enumerates all 96 controller inputs, 126 outputs, the 128×32 DMD, four supported ROM variants, and 14 ball-device or moving assemblies.

## Evidence policy used for this machine

The known-working `Spider-Man_VE_2.2.vbs` script is ground truth for public controller addresses, callbacks, ball routing, initial logical states, and mechanism causality. Stern manual 500-55A0-01 is ground truth for the physical switch names, parts, assemblies, wiring, voltage, polarity, and lamp locations. PinMAME revision `4ec52ff0ac133ac251681518aed2249e19fe26eb` is ground truth for the SAM controller profile, 128×32 DMD, 12-output auxiliary board, LED output treatment, and supported ROM family.

The script and manual do not actually conflict when kept in those domains. For example, the VE manual installs and wires the Green Goblin coil at Q19, while the known-working VPX intentionally disables only its digital toy-animation callback. The canonical definition therefore retains output 19 as used physical hardware at the Green Goblin mount and records the disabled callback as a limitation of that VPX implementation.

## Controller and variants

This is a Stern S.A.M. machine using the standard 64-position switch matrix, 32 dedicated positions, an 80-lamp matrix, 32 main driver outputs, the 12-transistor auxiliary board 520-5326-02, one logical GI relay, and a 128×32 DMD. PinMAME normalizes switch activity, so consumers must not apply a second inversion; `normally_closed` in the definition describes only the physical contact.

The public SAM switch-address translation is important: matrix switches are 1–64, dedicated D1–D8 are 65–72, D9–D16 are exposed as 84, 83, 82, 81, 88, 87, 86, and 85, D17–D24 are -7 through 0, and D25–D32 are DIP addresses 1–8 in the separate DIP group. The used lower-flipper EOS contacts are physically normally closed; ordinary playfield, cabinet, and opto states are physically normally open. The optional slam-tilt loop is normally closed.

All four PinMAME drivers (`smanve_100`, `smanve_101`, `smanve_100c`, and `smanve_101c`) use the same physical machine definition. V1.0 versus V1.01 is firmware-only, and the `c` variants add colored DMD rendering without altering playfield I/O, mechanisms, wiring, or display dimensions.

## Ball inventory and trough

The machine uses four balls. The known-working script creates a four-ball `cvpmTrough`, orders occupied positions from shooter side to drain side as switches 21, 20, 19, and 18, and treats switch 22 as the stack/jam opto (`Spider-Man_VE_2.2.vbs`, lines 135–142). A drained ball enters the switch-18 end of the trough; output 1 ejects the switch-21 ball, and the script pulses switch 22 during the release (`Spider-Man_VE_2.2.vbs`, lines 429–434 and 540–549).

The trough assembly is Stern 500-6318-24-ND. It combines three roller switches with the shooter-side and stack/jam optos. The dual-opto theory on manual pages 64–66 establishes the physical polarity: uninterrupted light leaves the receiver open, and a blocked beam closes the switch. Output 2 is the automatic launcher, and switch 23 reports the shooter-lane ball.

## Doc Ock area

The Doc Ock hole is switch 36 and its VUK is output 4. The script adds the ball to a `cvpmSaucer` on switch 36 and ejects it when output 4 fires (`Spider-Man_VE_2.2.vbs`, lines 150–155 and 507–523). Output 3 directly controls the playfield magnet (`Spider-Man_VE_2.2.vbs`, lines 157–162 and 393–400).

The Doc Ock moving assembly is Stern 500-7061-00. It uses a 24 VAC synchronous motor, a driver disc, a relay driven by output 5, and two roller limit switches: 57 is down and 58 is up. Target opto 63 represents the target interaction. The script advances the assembly on each output-5 activation and updates switches 57/58 together with the exposed target state (`Spider-Man_VE_2.2.vbs`, lines 443–456). Its initial logical position is down, with switch 57 active (`Spider-Man_VE_2.2.vbs`, lines 189–191).

## Sandman area

The Sandman hole is switch 59 and its VUK is output 12. The script adds the ball to a `cvpmSaucer` on switch 59 and ejects it on output 12 (`Spider-Man_VE_2.2.vbs`, lines 144–148 and 488–505).

The Sandman moving gate uses assembly 500-7061-00, the same synchronous-motor and driver-disc principle as Doc Ock. Output 13 drives the motor relay, switch 53 reports down, switch 54 reports up, and target opto 42 reports the target. The known-working script advances between those states on each activation (`Spider-Man_VE_2.2.vbs`, lines 458–471), and initializes the mechanism down with switch 53 active (`Spider-Man_VE_2.2.vbs`, lines 189–191).

The Sandman webslinger is motorized 3-bank assembly 500-7056-01 on motor-frame assembly 500-7057-01. Output 20 drives its relay; switches 9, 10, and 11 are the three target contacts; switch 49 is the down limit; and switch 50 is the up limit. The script sets switch 50 when it raises the bank and switch 49 when it lowers it (`Spider-Man_VE_2.2.vbs`, lines 473–486), and initializes the bank up with switch 50 active (`Spider-Man_VE_2.2.vbs`, lines 189–191).

## Gates, diverter, and flippers

Outputs 7 and 8 directly control the left and right magnetic control gates, assemblies 511-7033-00 and 511-7033-01. Output 22 controls the loop diverter; the script initializes it dropped, raises it when energized, and returns it to the dropped route when de-energized (`Spider-Man_VE_2.2.vbs`, lines 164–165 and 526–538).

Output 15 drives the lower-left flipper, with button 84 and normally-closed EOS 83. Output 16 drives the lower-right flipper, with button 82 and normally-closed EOS 81. Output 14 drives the upper-right flipper; dedicated D15/D16 upper-right button/EOS positions are explicitly unused, so the upper flipper has no separate cabinet button or EOS input in this definition. All three flipper coils are 22-1080 / 090-5032-ND.

## Other controlled devices

Outputs 9–11 are the three pop bumpers, 17–18 are the slingshots, and outputs 21, 23, and 25–31 are PWM-controlled LED flasher circuits. Output 6 is the optional shaker motor and remains optional because the working script leaves its callback commented out. Output 24 is physically an optional 5 V auxiliary device position in the manual and is used as the knocker callback by the working VPX script, so its portable semantic label records both facts.

Output 19 deserves special treatment: the VE manual's driver table physically installs and wires the Green Goblin coil at Q19, while the known-working VPX explicitly leaves `SolCallback(19)` disabled. A faithful physical recreation must retain the Q19 coil at mount 511-5302-05; an author using that VPX as behavior evidence must separately implement or validate its movement because the table script does not animate it.

Optional physical ticket-service identities 33–35 use the untransported `physical.output.ticket` group. They must not be confused with PinMAME public solenoid 33, which is SAM's synthetic game-on/fast-flip state and has no physical wiring.

## Lighting and display

The manual's lamp table on page 16 defines all 80 matrix positions; 55, 56, 73, 79, and 80 are unused, and lamp 2 is the optional tournament-start button. PinMAME marks the complete 1–80 range as LED strobes for `smanve_*` and marks output flashers 21, 23, and 25–31 as 20 V bulb-style modulated outputs (`src/wpc/sam.c`, lines 1529–1533). Preserve intensity/PWM behavior rather than treating those flashers as simple binary lamps.

PinMAME exposes one logical GI output. Physically, the GI relay feeds four separately fused 5.7 VAC circuits shown on manual page 55: brown/white for the middle and upper-left playfield with 8 bulbs; yellow/white for the right playfield with 11 bulbs; green/white for the back panel and coin door with 10 back-panel plus 2 coin-door bulbs; and violet/white for the upper-right playfield with 13 bulbs. The manual notes that production bulb quantities may vary, so geometry should follow the specific cabinet reference while all four circuits share controller GI address 0.

The display is a single 128×32 dot-matrix display. Colored ROM variants change rendering only and do not imply a different physical display topology.

## Spatial reconstruction

Every physical playfield switch, actuator effect, insert, flasher, and GI emitter has a reviewed normalized placement in VPX/player view (`x=0` left, `x=1` right, `y=0` rear/backglass end, `y=1` front/apron end). The exact known-working `Spider-Man_VE_2.2.vpx` supplies gameitem geometry, while the VE manual supplies physical quantity, assembly topology, and the distinction between playfield, back-panel, and cabinet hardware.

The five trough switches are projected along the real under-apron 500-6318-24-ND assembly in drain-to-eject order because the working VPX exposes only a shared release kicker rather than five physical trough gameitems. The motorized three-bank up/down contacts share the bank assembly center; the Sandman and Doc Ock gate limits likewise share their respective moving-assembly centers. These are different state contacts on one mechanism, not multiple playfield devices. The synthetic VPX use of switch 86 to drive the upper flipper does not create a physical D15 button: the manual's unused physical address remains explicitly `unused`.

Physical emitter counts override render fanout. Outputs 23 and 25 each have two reviewed flasher points; output 31 has one at each of the three pop bumpers. Output 28 contains two physical 113-5034-08 LED flashers inside one drilled Green Goblin toy, so its quantity is two while one normalized assembly point honestly represents the shared three-dimensional mount; the manual does not expose two distinct playfield-plane coordinates and the VPX collapses both into one broad overlay. The Sandman dome flasher is placed at the physical Sandman assembly rather than at the VPX's out-of-bounds whole-table glow helper. Lamps 66–71 are rear-panel groups projected at the `y=0` boundary. Flashers 29 and 30 retain their measured VPX rear-panel coordinates at `y=0.044681` and `y=0.041844`; they are near the rear boundary, not exactly on it.

GI 0 records 42 canonical emitter placements measured directly from the color-coded physical bulb markers on manual page 55: 32 playfield bulbs on the brown (8), yellow (11), and violet (13) circuits, plus ten individually measured green-circuit rear-panel bulbs projected to `y=0`. The underside playfield drawing is normalized against its outline and reversed only along y to produce player-view coordinates. The manual's one-line circuit-4 legend says "Upper Right Playfield," but all of its violet physical markers are plotted on the upper left; the definition intentionally follows the plotted markers because the independent brown and yellow legends and marker regions validate the drawing orientation. The rear-panel sub-drawing is explicitly a rear view, so those ten measured x positions are mirrored into player view before projection. The circuit's remaining two physical bulbs are inside/on the coin door and therefore retain their quantity and location in `physical` metadata without invented playfield coordinates. VPX's 58 `LA`/`LB`/`LAPiano` collection objects and eight wall overlays are rendering fanout, not 66 physical bulbs.

## Recreation sequence

An implementation can be brought up deterministically by creating four trough balls, asserting initial position switches 50, 53, and 57, leaving the loop diverter dropped, and then handing switch and output state to PinMAME. Recreate the causal paths before tuning motion: drain → four-ball trough → output-1 release → shooter lane → output-2 launch; switch-36 Doc Ock capture → output-4 eject; switch-59 Sandman capture → output-12 eject; output-5 Doc Ock position toggle; output-13 Sandman position toggle; and output-20 three-bank toggle.

The VPX angles, magnet strength, kick velocity, animation intervals, and mesh translations are proven implementation values for that known-working table, not universal physical measurements. They are excellent starting values for a digital twin, but tune them against the manual drawings and playfield geometry after the controller causality above is working.

## Sources

- Stern Pinball, *Spider-Man Vault Edition Manual*, 500-55A0-01, especially PDF pages 14, 16, 18, 40–46, 55, and 64–66; cached externally with SHA-256 `905e30eab1ddadedcf70f113613f0353fd064a276f8b11324e7831e75baadb9b`.
- Exact known-working `Spider-Man_VE_2.2.vpx`, 85,819,392 bytes, ROM `smanve_101`, SHA-256 `b258efeecc3dcbffd7dae79c52fdd39bba8c9a82e918034f170ab75c90764f11`; retained in the organized external VPX cache and verified/extracted with vpxtool `git:v0.33.3`.
- `sverrewl/vpxtable_scripts`, `Spider-Man_VE_2.2.vbs` at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `3d885c099bb54fe2bf67405bb35562b68d775748d7d76192b01f30c133e0ff36`.
- `vpinball/pinmame`, `src/wpc/sam.c` at revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`, especially lines 79, 1529–1533, 2356–2362, and 3621–3636.
