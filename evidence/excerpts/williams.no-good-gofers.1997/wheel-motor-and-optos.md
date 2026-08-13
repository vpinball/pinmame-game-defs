# Williams No Good Gofers operations manual - Wheel motor, DC Motor Control Board and Motor 2-Opto Board

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: PDF page 137, printed page 3-23, `Motor 2-Opto Board A-22026` with its connector list
and the `Wheel Spin Motor Wiring Diagram` beneath it. Transcribed by hand from a 300 dpi
`pdftoppm` render.

## Motor 2-Opto Board A-22026, connector list printed verbatim

```
J1-1  GRY-YEL   +12V from Power Driver board J139-2
J1-2  BLK       Ground from Power Driver board J139-3
J1-3  KEY
J1-4  GRN-BLU   Switch Column #6 from CPU board J206-6
J1-5  WHT-YEL   Switch Row #4 from CPU board J208-4
J1-6  WHT-ORG   Switch Row #3 from CPU board J208-3
```

The board drawing labels its two opto channels `SW1` and `SW2` with photo-transistors `PT1`
and `PT2`, and annotates the J1 header `COLUMN / SW1 / SW2`. The board carries the annotation
`Switch 64 Outer Wheel (opto 2)` beside the second channel.

Switch column 6 with return rows 3 and 4 is public switch matrix positions 63 and 64, matching
the switch-locations parts list on 2-48 (`63 A-22026 INNER WHEEL OPTO`, `64 A-22026 OUTER
WHEEL OPTO`) and the shaded matrix cells on 2-51/3-1. Both wheel optos are therefore on one
two-channel board bolted to the wheel mechanism, not at two separate playfield locations.

## Wheel Spin Motor Wiring Diagram

The diagram shows the power driver board's J110 feeding the DC Motor Control Board and that
board driving the wheel spin motor:

```
POWER DRIVER BOARD  J110-1  BRN-WHT  SOL. 37  -> DC MOTOR CONTROL BOARD -> WHEEL SPIN MOTOR
                    J110-3  ORG-WHT  SOL. 38
                    J139    GRY-YEL  +12V     -> DC MOTOR CONTROL BOARD J1
```

with the motor's own leads drawn `RED` and `BLK`.

Page footer: `3-23`.

## Related printed evidence, same manual

Printed page 2-53 (`solenoid-flasher-wiring.md` in this directory) prints solenoid 37 as
`WHEEL SPIN (counter clock-wise)` and 38 as `WHEEL SPIN (clock-wise)`, both `Low Power`, both
fed from `J139-2` and driven through gates `U3A, U3B` and `U3C, U3D`, and records the device
part numbers `Motor, 14-7955-1`, `DC Motor Control Board, A-16120` and `Motor 2-Opto Board,
A-22026`.

Printed page 2-14 (PDF page 74) is the `A-16120 DC Motor Control Assembly (4 Way)` parts page.
