# Baywatch mechanism and physical-construction readings

Curator; visually checked against retained `Baywatch_Manual.pdf` (SHA-256 `9545ae03f7ef1bcc41f3e5e08b6be996d581f9141b1f70228fe9969ba9ace400`). Page references below are PDF / printed. These are factual descriptions of the drawings and operating rules; no table-owned tuning is promoted to a factory specification.

- 10 / 6, Playfield Overview: the lower right automatic launch feeds the shooter wire ramp, whose exit leads to the rear three rollover lanes. A separate upper ball launch is at mid-right under the butyrate, near the Shark Fin flipper. The upper and lower control gates are separate mini-coils, one under the left ramp near the top lanes and one under the mid-right butyrate. The left metal ramp carries a trapdoor into the under-playfield ramp. That ramp returns to the front-left Super VUK under the arch. The rear-left upper VUK has its own wire-ramp return. The left Shark Super Scoop is a third, separate capture/eject device. The drawing explicitly omits the lock tower for clarity.
- 10-11 / 6-7, instruction card and Laser Kick rules: three drops light a lock at the left-ramp trapdoor; three collected locks start multiball. The left outlane Laser Kick starts lit and is relit from the two-bank stand-up targets above the upper-right flipper. A Shark skill shot goes from the Shark Fin flipper to the left Super Scoop. SPF lanes and the upper-left flipper/side-ramp shot are other skill-shot routes.
- 37 / 33, Shark Fin Flipper Flip test: a ball is placed above the wire-form actuator of switch 54 and released to roll in front of the upper-right flipper. The flipper fires toward the Shark Super Scoop. Left/right cabinet buttons adjust the value, also exposed as Adjustment 50, SHARK FLIPPER CONTROL. Switch 54 is consequently a ball rollover, not EOS.
- 63 / 59, 5-Ball Trough (OPTO) Assembly 500-5965-00-33: the drawing shows five discrete mechanical switch positions and a separate transmitter/receiver at the up-kicker. Lock Ball Assembly 500-5684-01-33 is a separate 25-1240 coil/cam; the up-kicker is a 23-800 coil at the opto end. The exit scoop is 535-7329-00-33. The same printed switch parts list independently enumerates all five 180-5119-00 switches and the 520-5124-00 / 520-5125-00 opto pair.
- 65-66 / 61-62, upper flipper drawings: upper right 500-5971-01-33 has 23-1100 printed on its coil; upper left 500-5983-02-33 has 24-1570. These drawings have no EOS assembly. The TOC's upper-right part number differs from the assembly heading; the assembly itself is followed.
- 70 / 66, launch assembly drawings: Auto Ball Launch 500-5969-00-33 has coil 23-800; Upper Ball Launch (Kick Big) 500-5862-06-33 has coil 24-940. These separate assemblies settle the switched-driver chart versus coil-schematic part-number/label disagreement.
- 71-73 / 67-69: separate Laser Kick 500-5838-01-33 and Vertical Up-Kicker 500-5839-01-33; separate Super Scoop (VUK) 500-5953-00-33 and under-arch Super VUK 500-5880-00-33; upper gate mini-coil 500-5968-00-33 and lower gate mini-coil 500-5957-00-33. These are not alternate names for a single ball stack.
- 74-75 / 70-71: one three-bank drop-target assembly 500-5970-00-33, reset by one coil. Top/middle/bottom switches have individual identities 22/23/24 in the location list.
- 76 / 72, Left Metal Ramp (Tower) Assembly 500-5943-00-33: a 27-950 coil, plunger, shaft and crank arm operate the trapdoor cover in the ramp. The entrance rollunder is separate from the door; its assembly uses a microswitch. Opening the door selects the under-playfield return; it is not a three-position mechanical tower lock.
- 109 / 105, complete upper SSFB wiring drawing: CPU CN12 pin 6, Q26, BRN/GRN joins the two upper-flipper enable lines through cabinet-mounted isolation diodes. The cabinet flipper switches are explicitly drawn N.O. and join the same enable paths. SSFB CN1 pin 10 is left enable, pin 7 right enable; upper left/right coils are 24-1570 and 23-1100. The drawing labels upper EOS enable wiring but the circuit table says physical upper EOS Not Used; this is a wiring path, not an additional switch-matrix EOS input.
- 111 / 107, opto theory: clear beam acts as an open matrix contact; blocked beam acts as a closed contact. The independent bench-test output is high with the beam clear and low when blocked, which is an electrical voltage convention rather than a request for consumers to invert PinMAME's normalized public state.

## Complete Lock Tower assembly table (77 / 73)

Heading: Baywatch Lock Tower Assembly †, 500-6006-00-33. The drawing shows a light bracket behind the front openings. The dagger on item 3 belongs to the mounting-plate exclusion; `*` means screws not drawn and not part of the assembly. Line wraps are joined; the subassembly explanation is a printed merged row rather than a part.

| Item | Description | Part No. |
| --- | --- | --- |
| 1 | Baywatch Lock Tower | 545-5606-00 |
| 2 | Light Bracket Sub-Assembly | 515-6340-00 |
| [merged explanation] | Ordering above (Item 2) Sub-Assembly Part Nº will include: | [blank] |
| 2A | Light Bracket | 535-7398-00 |
| 2B | 1/8 X 1" Foam Tape (3/4" X .06") | 626-5033-00 |
| 2C | 1/8 X 5/32 Rivet (Qty. 3) | 249-5009-00 |
| 2D | Wedge Base Socket (Qty. 3) | 077-5029-00 |
| 2E | #555 Bulb (Qty. 3) | 165-5002-00 |
| 2F | Rubber Lite Cover-Teal Green (Qty. 3) | 545-5014-13 |
| 2G | Wire Harness | 036-5371-18-33 |
| 3 † | Mounting Plate | 535-7417-00 |
| [note under 3] | The mounting plate is not a part of this assembly. If replacement is required, use 535-7417-00. The plate is screwed on the above part of the Left Ramp with 3 of the below screws. The Lock Tower then slides on this plate and is secured with the remaining 2 screws at the front sides. | [blank] |
| 4 * | #6 X 1/2 PTH Screw (Qty. 5) | 237-5809-00 |

## Socket-count limitation

The lamp drawing labels two outlane Special bulbs at address 25 and one for every other matrix address, with cabinet lamps 7/8/64 identified separately. The coil table and location drawing give four flash bulbs per circuit, split across playfield/rear panel and backbox. The general chart calls all of them #89, while the detailed PDF 88 wiring drawing specifies mixed #89/#906 populations on six branches (complete readings in `coils.md`). Generic parts illustrations are not a circuit-specific socket survey; their production-change caveat and inherited other-game footnote prevent using the unsplit totals to settle individual circuit populations. No count from those generic tables is promoted here. The two G.I. feed symbols on the lamp schematic do not establish a physical socket count or distinguish every backbox, rear-panel and cabinet branch. The definition therefore does not assert a total G.I. quantity.
