# Transformers Pro (Stern, 2011)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, PinMAME bindings, mechanism behavior, and edition differences validated**

## Identity and evidence precedence

This definition covers non-`h` PinMAME drivers `tf_120`, `tf_140`, `tf_150`, `tf_160`, `tf_170`, and `tf_180`. They are mutually compatible Pro firmware even though the clone graph points at the `tf_180h` Limited Edition root; that parent records software lineage, not physical compatibility. The known-working `Transformers Pro (Stern 2011) v.2.3.1.vbs` is ground truth for public controller addresses, callbacks, ball routing, and mechanism causality. The official Pro service supplement governs physical channels and wiring. Pinned PinMAME governs SAM serialization and the native 128x32 four-bit DMD.

## Controller topology and initial state

The SAM switch matrix is public 1-64. Dedicated cabinet inputs are 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough starts with switches 18-21 closed and jam opto 22 downstream. Main outputs are public 1-32, standard lamps 1-80, and aggregate GI 0. The Pro does not install the Limited Edition auxiliary board.

## Resolved output-4 VPX exception

The proven script registers callbacks for two orbit gates at outputs 4 and 5 because it shares mechanism code with fuller editions. The official Pro coil chart marks output 4 unused, and physical-machine review states that the additional left rollover-lane gate is an LE feature. A physical Pro recreation must therefore leave Q4 unused and build only the right/top orbit gate on output 5. This is a narrow physical-wiring correction; all other public controller semantics continue to follow the working script.

## Megatron mini-trough

The Megatron assembly is a four-position vertical mini-trough, not a single saucer. Balls stack at switches 41, 40, 39, and 38, with switch 42 guarding the exit. Output 3 ejects one ball at a time and may be pulsed in rapid succession for multiball. Build the complete stack and single-file exit so ROM lock accounting matches physical occupancy. The manual identifies the ball-trap assembly as `511-6977-00`.

## Optimus Prime

Output 30 powers the ramp motor relay. With the ramp down, the shot enters a curved lane and continues toward the right orbit; when raised, the rear of the ramp becomes a jump into Optimus Prime. Switches 43/44 are the full-up/full-down limits and both should be open in transit. The working script models intermediate collision ramps rather than teleporting the ball, which is the correct construction principle for a digital recreation. Switch 51 in the left leg senses the hit, and output 12 actuates a solenoid under the right foot to rock the figure. Output 12 is a toy coil, not a third flipper.

## Allspark, Bumblebee, and standard ball devices

The Allspark saucer holds a ball on switch 3 and ejects through output 22. Output 2 auto-launches from shooter switch 23 while retaining a manual plunger path. Bumblebee uses standup switch 1 and captive-ball switch 45; the car and captive ball have no controlled actuator. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 13/26 and 14/27. The passive right-orbit spinner pulses switch 34. The two physical flippers are outputs 15/16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed.

## Ramps, targets, lamps, and flashers

Switches 4/10 bracket the left ramp. The Pro right ramp uses entrance 35, back-door 13, and exit 14. The left orbit uses 5/6, right orbit 12, top lanes 7/8, and center lane 11. Energon standups are 2/46/49, the right two-bank is 37/50, and Bumblebee is 1. All 80 lamp addresses are explicit: 1-55 and 57-62 are used according to the Pro chart; 56 and 63-80 are unused. Flashers and toy/ball-device outputs are enumerated separately from lamps so authors do not infer physical type from PinMAME transport group.

## Author construction checklist

- Build the four-ball trough, shooter/manual plunger, auto launcher, Megatron four-ball stack/eject, Allspark eject, single orbit gate, motorized Optimus ramp with two limits, Optimus bash toy, Bumblebee captive-ball area, two flippers, three pops, two slings, spinner, both ramps, both orbits, top lanes, center lane, targets, and optional shaker.
- Bind every input, main output, lamp, GI 0, and DMD from the JSON; retain explicit unused channels and the physical Q4 exception.
- Preserve ball occupancy and endpoint causality. Do not replace the Megatron stack with a pulse-only toy or the Optimus ramp with a cosmetic animation.
- Use the proven VPX force, timing, and animation choices as starting values while keeping the service-manual wiring and physical edition boundary.

## Sources

- `manual.transformers-pro-le.2011`: official combined Stern manual, SHA-256 `9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8`; Pro switch/coil/lamp charts on PDF pages 129/131/133.
- `vpx.transformers-pro-vpw-2.3.1`: known-working Pro script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b`.
- `review.pinball-news.transformers.2011`: contemporaneous physical mechanism and edition-difference review.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and driver family.
