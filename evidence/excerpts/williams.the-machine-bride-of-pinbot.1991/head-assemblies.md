# The Machine: Bride of Pinbot — Head coil, face, and drive assemblies (printed pages 2-23 to 2-25, 3-3)

Source: `the_machine_operations_manual.pdf`, PDF pages 91-93 (printed 2-23, 2-24, 2-25) and PDF
page 117 (printed "PAGE 3-3"), read from 110 dpi overview renders of the native 300 dpi scan.

## A-14125 Head Mouth Assembly (printed 2-23)

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-14135 | Coil Switch Bracket Assy. |
| 2 | A-14134 | Bell Armature Assembly |
| 3 | 23-6420 | Rubber Grommet |
| 4 | 03-7067-5 | Tubing Coil |
| 5 | 01-8-508-T | Solenoid Bracket |
| 6 | 10-135 | Spring |
| 7 | AE-30-2000 | Coil Sub-Assembly |
| 8 | 5647-12693-39 | Mini Microswitch |
| 9 | 4002-01105-06 | Mach. Screw, 2-56 x 3/8 |
| 10 | Not Used | |
| 11 | 5070-09054-00 | Diode, 1N4004 |
| 12 | 4008-01017-04 | Mach. Screw, 8-32 x 1/4 |

Boxed note: `For Coil Assemblies A-14123 and A-14124, refer to diagram above Item #8 is the only one
that changes.` The drawing shows the coil and bell armature on a bracket, with the microswitch
mounted beside the plunger path.

## A-14123 Head-Right Eye Assembly and A-14124 Head-Left Eye Assembly (printed 2-23)

Both lists repeat the mouth list for items 1-7, 9, 11, and 12 (coil sub-assembly AE-30-2000 in
each) and differ only in these rows:

| Item | A-14123 Head-Right Eye | A-14124 Head-Left Eye |
| --- | --- | --- |
| 8 | 5647-12693-48 Mini Microswitch | 5647-12693-47 Mini Microswitch |
| 10 | 01-10112 Switch Bracket Adjustment | 01-10112 Switch Bracket Adjustment |

## A-14121 Complete Face Assembly (printed 2-24)

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-14130 | Face Plate - 1 Assembly: 31-1626-1 Screened Face Plate; 03-8482 and 03-8498 Rail Ball Guide; 01-9993 Stop Plate |
| 2 | A-14131 | Face Plate - 2 Assembly: 31-1626-2 Screened Face Plate; 01-10164 Y-Diverter-Eye Lane Select; 03-8482 and 03-8498 Rail Ball Guide; 03-8044-13 Mini Plastic Post; 01-9992 Stop Plate |
| 3 | A-14132 | Face Plate - 3 Assembly: 31-1626-3 Screened Face Plate; 03-8482 and 03-8498 Rail Ball Guide |
| 4 | A-14133 | Face Plate - 4 Assembly: 31-1626-4 Screened Face Plate; 03-8482 and 03-8498 Rail Ball Guide |
| 5 | A-14136 | Bracket Assembly - Top |
| 6 | 01-9832 | Face Plate Bracket - Bottom |
| 7 | 4006-01027-06 | Mach. Screw, 6-32 x 3/8 |

The drawing shows a square box carrying the four face plates on its four sides around a central
four-lobed hub.

## Face Plate Assemblies (printed 2-25)

- Face Plate - 1 (A-14130): two upper and two lower ball-guide rails around one central round
  opening behind the 01-9993 Stop Plate.
- Face Plate - 2 (A-14131): the triangular 01-10164 `Y-Eye Lane Select` above two round openings
  side by side, with the 03-8044-13 Mini Plastic Post and the 01-9992 Stop Plate.
- Face Plate - 3 (A-14132) and Face Plate - 4 (A-14133): no opening; two lower ball-guide rails only.

## Relay Assembly A-14423-1 and Motor Regulator Board A-13892-2 (printed "PAGE 3-3")

- Motor Regulator Board A-13892-2: J1-1 `+20V DC IN` (RED/WHT), J1-2 GND (BLK), J1-3 KEY; regulated
  `+12V DC OUT` on J2-1, J2-2 KEY, J2-3 ground.
- Relay Assembly A-14423-1: relay coil between J1-1 `GRY/YEL +12V DC` and J1-2 `BLU/ORG DRIVER`.
  Two change-over contacts: COM-1 (J2 pin 1) switches between NC1 (J2 pin 4) and NO1 (J2 pin 6);
  COM-2 (J2 pin 2) switches between NC2 (J2 pin 5) and NO2 (J2 pin 7). NC1 and NO2 are joined to
  `+12V DC GRY/YEL`; NO1 and NC2 are joined to `BLU/YEL DRIVER`. J2 pin 3 is KEY.
- COM-1 leaves as BLU and COM-2 as BLK through a three-pin plug (pin 3 BLU, pin 2 BLK, pin 1 NC) to
  the `+12V DC MOTOR`.

Reading of the drawing: with the relay released the motor's BLU lead is on +12 V and its BLK lead on
the BLU/YEL driver line; energizing the relay swaps the two leads, reversing the motor.
