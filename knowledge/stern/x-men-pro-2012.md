# X-Men Pro (Stern, 2012)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, public PinMAME bindings, lamp semantics, mechanisms, and edition differences validated**

## Identity and evidence precedence

This definition covers non-LE drivers `xmn_100`, `xmn_104`, `xmn_105`, `xmn_130`, `xmn_150`, `xmn_151`, and `xmn_151c`, using Stern model I-00D1 and IPDB 5822. Those revisions use one physical Pro playfield; `xmn_151c` only changes ROM colorization. The authenticated `XMen FS (physmod5).vpt` table running `xmen_150` is ground truth for controller callbacks, object placement, playfield labels, mechanisms, and active-high rendering behavior. The independent known-working Pro script corroborates public addresses. The combined Stern manual supplies common SAM service topology and shared assemblies but its edition-specific lamp and low-current output charts describe the LE, so those labels are deliberately not transferred to the Pro. Pinned PinMAME source governs driver identity, SAM serialization, and the native 128x32 four-bit DMD.

## Controller topology and initial state

The SAM switch matrix is public 1-64; dedicated cabinet inputs occupy 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough initializes switches 18-21 closed, and switch 22 is its jam opto. Standard lamps are public 1-80 and GI is public 0. Main outputs are public 1-32. The Pro does not install the LE auxiliary eight-transistor board or its public 51-58 output range.

## Lamps and physical placement

All public lamp addresses 1-80 are explicit in the JSON. The authenticated table consumes exactly 3-25, 28-31, 33-38, 43-57, 60-62, and 65-71; every other address is explicitly unused. Each used lamp was correlated with an extracted VPX coordinate during curation, but those coordinates have not yet been normalized and promoted into this definition. Semantic labels come from the table's playfield art. Descriptive location labels are retained for otherwise unlabeled red route arrows and the two Magneto completion medallions so an author can identify them without inventing rule terminology. Lamps 11 and 38 carry left/right Nightcrawler feature artwork but are ordinary static inserts on the Pro, not moving toys. Lamp callbacks and GI 0 are active-high in the proven scripts.

## Coils, flashers, and the upper flipper exception

Outputs 1-18 are the common trough, launcher, eject, magnets, lock, optional shaker, pops, three physical flippers, slings, and left/right flashers. Outputs 19, 20, 23, and 30 are unused on the Pro; in particular there is no spinning Magneto disc motor. Output 21 flashes Wolverine, 22 Magneto, 25 the pop area, 26 moves the orbit diverter, 27 is a center-left red flasher, 28/29 drive left/right backpanel groups, 31 is the Magneto center red flasher, and 32 is the Wolverine playfield magnet. The JSON records every observed flasher object's coordinates, including multi-object groups.

The physical upper-right flipper is output 12 with staged dedicated button 86/D15. The legacy table comments out callback 12 and rotates its upper flipper object together with lower-right output 16. That is a table shortcut, not machine wiring; authors must implement the physical 12/86 channel pair. Lower flippers are outputs 15/16 with buttons 84/82 and normally-closed EOS inputs 83/81.

## Magneto lock, Wolverine, and ball devices

PWM output 4 controls the Magneto playfield magnet. Output 26 routes the orbit shot into the four-position vertical Magneto lock. Occupancy switches are 53 at the bottom, followed by 38, 39, and 40 at the top; outputs 6 and 7 operate the linked up-post and latch mechanism. Wolverine is a passive wobbling bash toy on switch 36 plus a separate output-32 playfield magnet. The proven table disables center-grab so the magnet deflects the ball rather than pinning it rigidly.

The Power Scoop holds a ball at switch 4 and ejects with output 3. The left vertical up-kicker holds at switch 55 and output 5 sends the ball onto the left ramp. Output 2 auto-launches from shooter switch 23 while the cabinet also retains a manual plunger. Pops use output/switch pairs 9/30, 10/31, and 11/32; slings use 13/26 and 14/27. The passive Cyclops spinner pulses switch 47.

## Important Pro differences

The Pro omits the LE motorized Iceman Ice Slide, both latched Nightcrawler pop-up mechanisms, the spinning Magneto disc, red/blue/white subtractive color-GI channels, and auxiliary driver board. It retains two printed Nightcrawler lamp features and ordinary Iceman inserts, which must not be mistaken for the missing LE mechanisms. The Wolverine magnet moves from LE public 51/physical Q41 to Pro main output 32. Output 27 is a flasher instead of the LE Iceman motor, and output 31 is a different red feature flasher. Never apply the combined manual's LE lamp table or these LE output labels to a Pro recreation.

## Author construction checklist

- Build the four-ball trough, shooter/manual plunger, auto launcher, Power Scoop eject, left VUK, four-level Magneto lock and diverter, two playfield magnets, passive Wolverine bash toy, three flippers, three pops, two slings, Cyclops spinner, seven standup/bash targets, two molded ramps, inner loop, and both outer orbits.
- Bind every public input and output from the JSON, including explicit unused lamp and coil channels, GI 0, the 128x32 DMD, and the upper-right physical flipper exception.
- Recover and normalize the 58 standard-lamp and flasher-group placements from the authenticated table and pinned playfield art before authoring; these coordinates are not yet stored in the definition. Do not invent LE hardware where the Pro art retains only a themed insert.
- Treat working-table kick force, angle, animation, capture, and magnet values as proven authoring baselines, while preserving controller causality and physical channel assignments.
