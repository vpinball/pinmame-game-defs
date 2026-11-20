# Bad Cats

Coverage: **partial — the L-5 public I/O and factory assemblies are documented. Lamp 32 fitment, some contact polarities, measured motor behavior, and several socket positions remain open.**

## Machine and firmware

Williams model 575 began production in November 1989. The two-flipper single-ball machine uses System 11B, two 16-character alphanumeric rows, a manual shooter, and a physical three-jet cluster. One machine record covers L-5, LA-2, LF-1 French, LG-4 German, and the three listed versions of idealjoker's Cat's Meow replacement firmware. Cat's Meow replaces U26/U27 on the original hardware. Its ball saver and selectable rules are ROM behavior. LA-2 and L-5 differ in the opto transitions that score at the Fish Bone-Us target. [IPDB machine 127](https://www.ipdb.org/machine.cgi?id=127) · [Cat's Meow author thread](https://pinside.com/pinball/forum/topic/the-cat-s-meow-a-new-home-rom-for-bad-cats)

## Controller routing

The 8×8 switch and lamp matrices are sequential and column-major. Bad Cats uses the full 64 positions in each inventory, one country jumper, four service inputs, the eight-position emulator flipper column, and 50 public solenoid slots. The matrix has no PinMAME inversion mask. Cabinet buttons 82 and 84 are copied to lane-change switches 57 and 58. Supply 82 and 84 from the host. The wired flippers operate directly from the buttons under game enable, with their own end-of-stroke circuits. Public 45/46 and 47/48 are synthetic state pairs. They are useful for animation and carry no winding timing. The CPU's A/C relay feedback is switch 2 and follows output 12.

The A/C relay multiplexes the first eight power outputs. Bank A is public 1–8 and bank C is 25–32. Both banks share the eight driver transistors. The L-5 Coil Test names the channels and its three complete sweeps exercise both banks, the controlled outputs, and the six special positions. The unfitted outputs at 7, 8, and 22 pulse as part of that test under `NOT USED`. Runtime confirms the left, right, and lower jets on 17, 19, and 21 and the slings on 18 and 20. The board routes the latter as special outputs and the emulator's own enable appears at 23.

General illumination is controlled by two C-11998-1 relay boards. Output 10 is the playfield circuit on the underside of the board. Output 11 is the backbox circuit on the insert board. The local VPX approximates GI and backbox behavior through combined visual effects. Use the factory distinction for physical recreation.

## Ball paths and devices

- **Drain and serve.** A ball falls to the runway under the apron and sits on switch 10. The B-8039-2 kicker lifts it into the manual shooter lane on output 1. Contact 14 detects the ball in the shooter lane. The VPX's release kicker is at the shooter end for simulation convenience.
- **Doghouse and garbage can.** Contact 22 senses the ball in the Doghouse plastic. Output 3 operates the C-11987-1 kick arm. In the upper-left garbage can, contact 24 senses the ball for Fish Bone-Us collection. Output 5 drives its eject arm and sends the ball back toward the upper playfield. These are separate traps with different exit paths.
- **Targets.** Five Bird Cage blades report on 25–29 and lift together on output 6. The three Milk Bottle blades report on 37–39 and lift on output 4. Both banks have optical readout boards. The separate B-13016 linear target moves against its return force and presents optical transitions on 19. The old VPX stages the movement with four triggers. These triggers are the virtual model for one physical opto.
- **Ramps and rubbers.** The left Tiger ramp is entered on 23 and exits on 41. The central Fishbowl or Goldfish ramp uses 16 and 43. The T–O–Y lanes are 11–13. Switches 33, 34 and 40 are rubber contacts elsewhere around the upper mechanisms.

## Seafood Wheel and backbox animation

The Seafood Wheel has eight labelled awards around a circular moving wheel. The two motor inputs drive phases of one stepper. Brown-grey from 16 feeds D-12046 J1-4 Input A. Brown-violet from 15 feeds J1-5 Input B. The movement depends on the phase sequence. The board schematic lists two compatible motor part variants and their different winding wire colors.

The wheel opto on switch 44 returns its matrix signal through the D-12046 board. In the factory Wheel Test, H marks an interrupted beam and an open matrix contact. The service display reports the last known wheel position and a count of 1–200. A bad home signal can produce an 08Err and counts up to 256. In Auto-Up the test spins, waits approximately two seconds, and repeats. In Manual-Down, Advance spins to the next counterclockwise position and Credit steps an idle wheel. Both local tables use a 200-step circular model and a simulated 0–99 sensor window. The physical marker width and startup alignment require direct measurement.

Backbox motors 9 and 13 are separate 14-7954 units for the cat and the woman. The Cat Test is test 09. Match the figures and motor panel shown in the factory drawing and the physical insert-board photo. They have no documented position feedback through the public switch matrix.

## Lamp reconciliation and remaining work

The later factory location list identifies lamp 31 as DOGHOUSE, and the local VPX puts its corresponding light at that assembly. Lamp 55 is the backbox Barbecue lamp, supported by the location list and the L-5 Single Lamps Test. The same test drives lamp 32 but supplies no label. The earlier matrix calls it Seafood Arrow 2, the location list leaves it blank, and neither retained local table supplies a socket for it. Trace the populated lamp harness on a physical machine to settle its fitment.

The individually recorded placements come from the table's switch/collider and lighting objects with projections disclosed in the spatial audit. Photographs corroborate the upper playfield arrangement and several flasher domes. The factory lamp list locates 9–13 on the Tiger Ramp and 17–19 on the rear playfield panel. Their perspective and the obstructions beneath the plastics leave some socket centers, especially the three Seafood flashers, the Tiger Ramp and rear-panel bulbs, and the playfield GI inventory, unverified. The two local VPX copies are related and provide no independent geometric confirmation. Direct contact checks or circuit drawings are still needed for any polarity left unspecified in the definition.

The factory manual excerpts, retained VPX extraction and pinned L-5 service traces are the evidence underlying this partial record. The diagnostic probes establish public behavior in service mode. Gameplay timing, the stepper's true home interval and the backbox figures' motor travel remain open.
