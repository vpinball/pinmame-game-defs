# Whirlwind GI branches and flipper circuits

Read from the factory `Whirlwind_OPS.pdf`, PDF page 106, printed page 96,
Power Wiring Diagram. These are the complete four GI load branches at the
D-12313-574 Backbox Interconnect Board. Wire labels and connector order
are source-literal; wrapped load labels are joined.

| Board connector / pin | Wire | Mating harness connector | Printed destination |
| --- | --- | --- | --- |
| 2J7-10 | BRN | 2P7 | To Insert Board (B'box) General Illumin Ckt via Insert Bd Relay (Sol. 16) |
| 2J7-9 | GRN | 2P7 | same grouped destination |
| 2J7-8 | WHT-BRN | 2P7 | same grouped destination |
| 2J7-7 | WHT-GRN | 2P7 | same grouped destination |
| 2J10-10 | YEL | 2P10 | To Coin Door Gnlb Illumination Ckt |
| 2J10-9 | WHT-YEL | 2P10 | same grouped destination |
| 2J9-7 | WHT-YEL | 2P9 | To Lwr Playfield Gnl Illumin Ckt via Relay (Sol. 16) |
| 2J9-6 | YEL | 2P9 | same grouped destination |
| 2J9-5 | VIO | 2P9 | To Upr Playfield Gnl Illumin Ckt via Relay (Sol. 11) |
| 2J9-1 | WHT-VIO | 2P9 | same grouped destination |

The grouped destination is printed once for each branch; its repetition in
the table above is normalization. Both playfield branches explicitly pass
through relays. The coin-door branch does not pass through either relay.
The diagram does not enumerate GI sockets or split the backbox insert
board into its controlled and constant portions, so it cannot establish
controlled bulb quantities.

The same sheet's complete Left Flipper Circuitry and Right Flipper
Circuitry drawings show these physical coils and EOS switches:

| Cabinet button | Coil label | Coil return to button | Shared button wire |
| --- | --- | --- | --- |
| L Flipper Button | Lwr Left Flipper | BLU-GRY | ORN-GRY |
| R Flipper Button | Lwr Right Flipper | BLU-VIO | ORN-VIO |
| R Flipper Button | Upr Right Flipper | BLK-YEL | ORN-VIO |

Each flipper has a separate coil symbol and EOS switch. The right button
connects both right-hand circuits; it does not make their coils one device.
The input LEDs of lane-change optocouplers 2U2 (left) and 2U3 (right) are
on resistor-fed sensing branches between the flipper supply and the
switched lower-coil returns (BLU-GRY left, BLU-VIO right), in parallel
with the coil loads. Their output transistors are optically isolated on
the switch-matrix side, reporting lower-flipper activation at 58 (left)
and 57 (right). The lower-coil returns run directly via 2P8/2J8 to the
cabinet buttons; the linked upper-right BLK-YEL return is not monitored
by 2U3. An open button removes the return path, leaving the opto off at
rest. Coil power flows through the hardware circuit with no independent
CPU coil drive.
Both `L Flipper Button` and `R Flipper Button` symbols show a gap at rest
in the cabinet-button return contact, establishing normally-open physical
buttons (`normally_closed=false`). Their parallel suppression capacitors
do not close that contact. This construction evidence supplies polarity
for the host-facing button counterparts 82/84; their public levels and
copies into lane-change 57/58 are derived separately from PinMAME/script.

## Back Panel Lamp Board

PDF page 62, printed page 52, Lamp Boards. Complete D-13356 parts table:

| Part Number | Description |
| --- | --- |
| 24-8767 | Twist Lamp Socket |
| 24-8768 | Bulb #555 (6.3V., 0.25A.) |
| 24-8802 | Bulb #906 (13V., 0.69A.) |
| 24-8803 | Twist Lamp Socket |
| 5768-12583-00 | Lamp PCB |
| 5791-10871-03 | Connector, 3-pin Sq. |
| 5791-10871-06 | Connector, 6-pin Sq. |

The adjacent Speaker Panel Lamp Board D-12501 table is:

| Part Number | Description |
| --- | --- |
| 24-8767 | Twist Lamp Socket |
| 24-8768 | Bulb #555 (6.3V., 0.25A.) |
| 5070-09054-00 | Diode, 1N4004, 1.0A. |
| 5768-12377-00 | Lamp PCB |
| 5791-10871-09 | Connector, 9-pin Sq. |

PDF page 52, printed page 42, Circuit Board Locations, draws D-13356 on
the upright panel at the rear of the playfield. Together with the Solenoid
Table legend `bp = Bk Panel`, this establishes rear-playfield location
for sound-overlay flashers 37/39/40. It is distinct from the backbox insert
board. These parts tables print no socket quantities.
