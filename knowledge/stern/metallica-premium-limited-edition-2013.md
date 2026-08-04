# Metallica Premium / Limited Edition (Stern, 2013)

Coverage: **author-ready - complete physical inventory, public PinMAME bindings, custom mechanisms, recreation behavior, and spatial placements validated**

## Identity and evidence precedence

This definition covers the `mtl_*h` and `mtl_*hc` firmware family used by the Premium and Limited Edition playfields. Non-`h` drivers are the different Pro playfield and remain in a conspicuous partial record. The known-working `Metallica Premium Monsters (Stern 2013) VPW 2.0.2.vbs` is ground truth for controller callbacks, initial state, mechanism causality, timing, and active behavior. The official Stern manual governs physical inventory, wiring, assemblies, and service numbering. Pinned PinMAME source governs public custom-output serialization, board topology, DMD transport, and driver identity. The exact local VPX table resolves the final RGB connector-to-public-address mapping that cannot be recovered from lamp object names in the external script alone.

## Controller topology

Metallica uses the Stern SAM CPU/Sound and I/O Power Driver boards, a 520-5326-01 six-transistor auxiliary board exposed as public solenoids 51-56, a 520-6801-00 coffin-magnet processor whose two public mode bits are 57/58, and one 520-5331-00 RGB/GI board exposing public lamp channels 81-128. Physical main outputs are 1-32. PinMAME public solenoid 33 is the synthetic SAM game-on state, while optional physical ticket functions retain service identities 33-35 in the untransported `physical.output.ticket` group. The native display is a 128x32 four-bit DMD; exact-ROM runtime observed PinMAME layout type 14.

## Switch corrections and initial state

All matrix positions 1-64, dedicated D1-D24, and DIP inputs are explicit. The manual and working script establish switch 22 as the shooter-lane jam opto and 23 as the shooter lane; the old merged definition had these reversed. Switch 52 is the grave-marker opto and 53 is the electric-chair opto. The proven table creates four trough balls and initializes switches 18, 19, 20, and 21 active. Switch 22 is downstream and starts clear.

## Lamps, RGB connectors, and GI

Standard lamps 1-80 follow the Premium service table; unused matrix addresses are explicit. The RGB/GI board's public addresses are not sequential by physical connector. Exact table timer bindings prove CN4 blue/green/red at 87/88/89, CN5 at 90/91/92, CN9 at 99/100/101, CN11 at 102/103/104, CN13 at 108/109/110, and CN19 at 126/127/128. Every other address from 81 through 128 is an unused controller channel for this playfield. GI uses public lamp addresses 130 red, 132 blue, 134 white upper, and 136 white playfield; group `pinmame.output.gi/0` remains the aggregate compatibility state. All physical tri-color module centers are normalized from the exact working table and reconciled with the manual wiring map. Each RGB channel record shares its physical module point; never create one lamp per color channel.

## Grave marker, electric chair, hammer, and drop bank

The grave marker is a motorized two-position assembly: output 20 moves it between down switch 33 and up switch 34, output 3 controls its ball magnet, and switch 52 is its opto. The electric chair uses magnet output 4, ball opto 53, standup 35, and Sparky step-up output 18. Output 53 swings the hammer without a position sensor; captive-ball impacts pulse switch 42. Drop switches 60-62 start raised and output 54 resets the complete three-bank.

## Coffin lock and magnet processor

Optos 57-59 track three coffin lock positions and output 51 releases the lock post. Output 52 lowers the separate magnet and asserts position switch 64. The processor's public bits are output 57 as D0 and 58 as D1. The proven script defines 00 off, 10 detect/hold at reduced strength for up to 10 seconds, 11 detect on a 250 ms cadence, and 01 full centered grab for up to 1 second. Switch 63 reports ball presence only in detect/hold or detect mode. Preserve those bit combinations and timing; treating outputs 57/58 as ordinary independent coils breaks ball capture.

## Snake, loop post, and standard devices

The snake holds a ball at switch 54 and ejects it with output 5. Output 12 releases the jaw latch and switch 55 reports jaw open; output 56 closes the jaw and switch 56 pulses at the latch contact. Output 55 is the loop up post and has no position switch. Output 6 ejects the right scoop at approximately 39.5 degrees with strength 54, while output 2 auto-launches at power 55. The machine also has two lower flippers, three pop bumpers, two slingshots, two loop spinners, two ramps, fuel-lane targets, and the optional shaker on output 8.

## Recreation checklist

- Construct all physical inputs and outputs, including unused addresses, the six-transistor board, coffin processor, RGB/GI board, cabinet options, and native DMD.
- Initialize four balls on trough switches 18-21; keep shooter-jam 22 clear until a ball enters that path.
- Preserve PWM or sustained behavior for both magnets and preserve the coffin processor's two-bit state machine.
- Model the grave marker's motor limits, electric-chair capture and Sparky step-up, hammer and captive ball, drop bank, loop post, three-position coffin lock, lowering coffin magnet, snake latch/jaw/eject, scoop, auto-launcher, pops, slings, and flippers.
- Bind node LEDs and processor bits to the public JSON addresses; retain connector and service numbers only as physical aliases.
- Use the VPX force, angle, timing, and state transitions as proven authoring baselines, then align geometry to the official assemblies without changing controller causality.

## Spatial coordinate model

Every physical playfield sensor, actuator, controlled lamp, and GI authoring anchor uses one normalized player-view frame from the exact 952.941 by 2117.647 VPW table: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. Exact object centers are accepted only after the proven script establishes controller semantics and the official manual confirms the physical assembly. Cabinet, service, back-panel, virtual, DIP, unused, and compatibility-only records never receive fake playfield points. The trough-jam opto, moving-assembly contacts, slingshot contacts/coils, EOS contacts, and bank reset are explicitly identified as regional or assembly projections rather than fabricated internal component centers.

The grave marker is one moving assembly with separate magnet output 3, motor output 20, down/up switches 33/34, ball opto 52, and flasher 19. The electric-chair/Sparky area keeps magnet 4, standup 35, ball opto 53, step-up 18, and its flashers separate. The coffin mechanism likewise separates three lock optos 57-59 and lock release 51 from magnet position/detection switches 64/63, lowering output 52, and virtual processor bits 57/58. Snake eject 5, latch release 12, jaw close 56, ball switch 54, jaw-open 55, and latch 56 remain distinct controller devices even where only one defensible rest-state assembly pivot exists.

Physical lighting multiplicity follows the manual, not the render-object count. Standard lamps 25 (Mystery) and 53 (Shoot Again) each drive two physical bulbs while the exact table supplies one composite anchor, so their quantities remain two without invented bulb separation. Red GI is nine wedge plus two bayonet fixtures; the table supplies ten calibrated GIR anchors and the manual retains the eleventh without invented precision. Blue GI is nine wedge plus two bayonet and matches 11 GIB anchors. CN22 drives five exact front spot-lamp anchors plus six back-panel fixtures outside playfield space. CN23 drives 22 wedge and two bayonet playfield fixtures plus four bottom-arch fixtures; the exact table supplies 22 GIW anchors, while the remaining six are retained in physical quantity and located by the cited manual map rather than guessed. Public `pinmame.output.gi/0` is only an aggregate compatibility callback and creates no additional bulbs. Back-panel flashers 21/22 each have three physical bulbs outside playfield space. Coffin flasher 31 has two physical bulbs but one defensible composite F31 anchor.

## Sources

- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; RGB/GI driver and physical lighting maps on PDF pages 45-50 (pages 47-50 are LE-titled sheets applied to this combined Premium/LE record because the editions share the playfield), Premium switch/lamp/coil location maps on pages 104, 106, and 108, and auxiliary output map on page 110.
- `vpx.metallica-premium-monsters-vpw-2.0.2`: pinned known-working script, SHA-256 `3be5af3f6b05c4f1445c391aab42713bf9e76af87d563bfb061e7bc5daedfd64`.
- `vpx-table.metallica-premium-monsters-vpw-2.0`: exact known-working `Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx`, 424,071,168 bytes, SHA-256 `afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f`; retained externally under `pinmame-vpx-sources/stern/metallica-premium-limited-edition-2013/source` and extracted read-only with vpxtool git:v0.33.3 for the sole normalized geometry frame.
- `runtime.metallica-premium.boot-start`: exact `mtl_180h` ROM run, raw SHA-256 `a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510`, ROM archive SHA-256 `141018225cdf51421b579b319b925b6dfd6a2fda98471e16998bd648abd86488`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, custom-board routing, DMD, and driver configuration.
