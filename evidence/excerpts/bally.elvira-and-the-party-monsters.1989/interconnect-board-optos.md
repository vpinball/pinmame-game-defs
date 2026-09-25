# Bally Elvira and the Party Monsters (1989) — Backbox Interconnect Board opto isolators

Source: Bally Midway *Elvira and the Party Monsters* Operations and Parts Information Manual
16-2011-101, IPDB machine 782 file `Elvira_and_the_Partymonsters_OCR_searchable.pdf`, PDF page 110
(printed 3-18, "Backbox Interconnect Board (D-12313-568) Schematic", Williams drawing 16-9052-1) and
PDF page 62 (printed 2-10, Backbox Interconnect Board parts list). Read from the native 300 dpi
renders. The crop is the opto section of the schematic with the J17/J18/J19 switch-matrix routing
above it.

Parts list, printed 2-10 (rows relevant to the optos):

| Description | Qty. | Designation No. | Part Number |
| --- | --- | --- | --- |
| Resistor, 3.3KΩ, 5w, 10% | 2 | R14, R15 | 5012-12238-00 |
| Resistor, 1.5KΩ, 5w, 10% | 1 | R13 | 5012-12337-00 |
| Opto Isolator 4N25 | 3 | U1 - U3 | 5490-10892-00 |

Schematic, printed 3-18, as drawn:

- **U1**: LED anode (pin 1) through a resistor printed `15K 5W`, whose designator is hard to read on the
  scan (it resembles `R15`) and is R13 by elimination from the parts list, from the line labelled
  `28V 'C' SIDE`;
  cathode (pin 2) to `GND`. Transistor collector (pin 5) to the `WHT/RED` line, emitter (pin 4) to
  the `GRN/BRN` line. `WHT/RED` joins the switch row reaching `J17-9`; `GRN/BRN` joins the switch
  column that the board brings in on `J1-8` and out on `J18-1`.
- **U2**, labelled `LT L.C.`: LED anode (pin 1) through `R14` printed `3.5K 5W` to the line reaching
  `J8-8`; LED cathode (pin 2) on a line that runs right, around the sheet edge and back along the
  bottom to `J8-14`, the row the sheet labels `BLU/GRY LT-L` at `J10-2`. Transistor collector (pin 5)
  joins the same `WHT/RED` row as U1; emitter (pin 4) runs right to a node shared with U3's emitter.
- **U3**, labelled `RT L.C.`: LED anode through `R15` (no value printed beside it) to the line reaching
  `J8-9`; LED cathode on a line that runs right and down to `J8-15`, labelled `BLU/VIO RT-L` at
  `J10-1`. Transistor collector (pin 5) runs up to the row reaching `J17-10` (`WHT/BRN`); emitter
  (pin 4) joins U2's emitter.
- `J8-9` and `J8-8` carry the `J5` lines labelled `50V RIGHT FLIPPER` (`BLU/YEL`) and `50V LEFT
  FLIPPER` (`GRY/YEL`); `BLU/VIO` and `BLU/GRY` are the lower right and lower left flipper coil wires
  the Solenoids & Flashers table prints between flipper switch and coil. Each LED therefore spans its
  flipper coil's supply and return.
- The shared U2/U3 emitter node runs up to the line reaching `J17-1`, which the board carries from
  `J1-11` (`GRN/GRY`, switch column 8) through `J19-7` and `J18-3`.
- On the same sheet the `J5` power pins are labelled, among others, `28V 'C' SIDE` (J5-9, `ORG`),
  `50V "A"&C SIDE` (J5-11, `YEL/VIO`), `50V RIGHT FLIPPER` (J5-2, `BLU/YEL`), `50V` (J5-10, `VIO/YEL`)
  and `50V LEFT FLIPPER` (J5-3, `GRY/YEL`). Each label is printed beside its pin, slightly above the
  wire-colour line.

Printed values disagree between the two pages: the schematic prints `15K` for U1's resistor and R14 `3.5K`, the
parts list prints R13 `1.5KΩ` and R14/R15 `3.3KΩ`.

Read against the switch matrix (printed 2-36): U1 closes column 1 (GRN) to row 2 (WHT/RED), which is
switch 2 "A/C Relay Position"; U3 closes column 8 (GRN/GRY) to row 1 (WHT/BRN), switch 57 "Right
Flipper"; U2 closes column 8 to row 2, switch 58 "Left Flipper".
