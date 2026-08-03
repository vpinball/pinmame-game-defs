# X-Men Limited Edition (Stern, 2012)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers both artwork packages of the Limited Edition hardware: Magneto LE (IPDB 5823, 250 units) and Wolverine LE (IPDB 5824, 300 units), Stern model I-00D2. They share the same playfield and I/O. Drivers `xmn_*h`/`xmn_*hc` are LE firmware, and early `xmn_102` is also explicitly identified as Limited Edition by PinMAME even though it predates the `h` naming convention. Non-`h` Pro revisions have materially different hardware and are not compatible with this definition.

The known-working `X-Men LE (Stern 2012) VPW v1.0.6.vbs` is ground truth for public PinMAME addresses, callbacks, initial states, and mechanism causality. The Stern manual governs physical inventory, diagnostic numbering, wiring, and assemblies. Pinned PinMAME source governs the SAM transport, 128x32 DMD, driver identities, and the eight-transistor board's public custom-output range.

## Controller topology and initial state

The SAM switch matrix is 1-64; dedicated cabinet switches use PinMAME public values 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough closes switches 18-21 at initialization. General illumination is public GI 0. Physical main-driver Q1-Q32 are public solenoids 1-32. PinMAME public 51-58 map in order to physical auxiliary Q41-Q48. Public solenoid 33 is a software flipper-enable event used by the proven VPX table and is not a cabinet transistor.

## Edition-only devices

LE-only switches are 12 left Nightcrawler down, 34/35 Iceman endpoints, 50/51 Nightcrawler hit sensors, and 56 right Nightcrawler down. LE-only public auxiliary outputs are 51 Wolverine magnet, 52/53 Nightcrawler raise coils, 54/55/56 white/red/blue GI dim channels, and 57/58 Nightcrawler latch releases. The LE also uses main output 23 for the Magneto disc motor and output 27 for the Iceman ramp motor. Do not transfer these devices to a Pro recreation.

## Magneto disc and lock

The Magneto disc motor and magnet are independent. Output 23 spins the disc without a position sensor; PWM output 4 controls its magnet. Behind it, the orbit diverter on output 26 routes balls into a four-level vertical lock. Lock sensors are 53 at the bottom, then 38, 39, and 40 at the top. Outputs 6 and 7 operate the dual linked up-post and latch mechanism; the proven model raises both posts and schedules their return after 500 ms.

## Nightcrawler pop-ups

Each Nightcrawler has separate raise and latch-release coils. Output 52 raises the left figure and output 53 the right; the down switches 12/56 clear immediately. The figures mechanically latch at full height without upper sensors. Switches 50/51 register ball strikes. Outputs 57/58 release the latches, after which the figures fall and close their down switches only at the bottom. A faithful simulation must model the un-sensed upper latch and should move a resting ball out of the travel envelope before raising, as the proven table does.

## Iceman Ice Slide

Output 27 drives a two-position motorized ramp that transfers the ball from the right side toward the left. The known endpoints are 14 degrees home and 60 degrees away. Switch 34 is home, switch 35 away, and both remain open during travel. The ROM energizes the motor toward the next endpoint; the working implementation remembers direction and reverses it after each limit. Move any ball already on the ramp with the rotating surface.

## Wolverine, ejects, and standard playfield

The Wolverine assembly combines a passive bash toy on switch 36 with a separate playfield magnet on public output 51/physical Q41. The toy should wobble from impact rather than behave like a drop target. The Power Scoop at switch 4 ejects through output 3. The vertical up-kicker at switch 55 fires with output 5 and diverts the ball onto the left ramp. Output 2 auto-launches from shooter switch 23. The upper-right flipper is output 12 with dedicated button 86; lower flippers are 15/16 with buttons 84/82 and normally-closed EOS contacts 83/81.

## Lamps and GI

The standard lamp matrix is exactly 1-80; 1-16, 40, 44, and 61-64 are explicitly unused in the service chart. The remaining addresses and names are enumerated in the JSON. GI 0 is the master supply. Public modulated outputs 54-56 are active subtraction/dimming channels: the proven table computes each color as `255 - output` while GI is on. This polarity matters when recreating red, blue, white, and mixed illumination.

## Other physical inventory

The machine has four balls, three flippers, three pops, two slings, a passive Cyclops spinner, two main molded ramps, the Iceman transfer ramp, seven standup/bash targets, the Magneto diverter/lock, two playfield magnets, two eject devices, and an optional shaker. The left pair 1/2 are Hellfire targets, right pair 7/8 Brotherhood, 41/42 Light Lock, and 36 Wolverine. None of these target banks is a resettable drop-target bank.
