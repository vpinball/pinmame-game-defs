# FunHouse — Rudy/Trap Door mechanism parts (printed pages 2-24 and 2-32)

Source: `Funhouse_OPS.pdf`, PDF pages 85 and 93 (printed "2-24" and "2-32"), rendered at 300 dpi
and read directly from the image.

## A-13752 Jaw Drive Assembly (PDF page 85, printed 2-24)

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | 01-9686-L | Bracket Jaw Drive Assy. |
| 2 | A-13751 | Bracket Assembly |
| 3 | A-13997 | Jaw Motor Assembly |
| 4 | 03-8471 | Gear |
| 5 | 03-8470 | Sector |
| 6 | 4004-01003-03 | Mach. Screw, #4-40 x 3/16 |
| 7 | 4008-01017-06 | Mach. Screw, #8-32 x 3/8 |

The drawing shows the motor (item 3) driving a worm-style gear/sector pair (items 4/5) rather than
a simple push-pull solenoid — Rudy's jaw is opened and closed by a continuously-running DC
gearmotor (A-13997, matching solenoid 21 "Mouth Motor"'s printed part number), not by a coil
stroke. This confirms `fh_handleMech`'s logic in pinned PinMAME source (motor solenoid 21 plus a
direction relay, solenoid 22 "Up/Down Driver", together determine whether the jaw opens or
closes) against real hardware: a motor needs a separate direction signal, which is exactly what
solenoid 22 provides.

## A-13941 Eject Assembly (PDF page 85, printed 2-24; generic kickout-coil template, reused for
multiple FunHouse kickout holes — not specific to Rudy)

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-13942 | Bracket Assembly |
| 2 | AE-26-1500 | Coil Assembly |
| 3 | 03-7067 | Coil Tubing |
| 4 | 10-135 | Solenoid Spring |
| 5 | 23-6420 | Rubber Grommet |
| 6 | 01-9784 | Coil Bracket |
| 7 | A-13270 | Bell Armature Assy. |
| 8 | 4408-01119-00 | Nut, #8-32 ESN |

## Unique Parts (PDF page 93, printed 2-32) — mechanism assemblies relevant to Rudy, the trap door,
and the diverter

| Part No. | Description |
| --- | --- |
| A-13718 | Head Assembly |
| A-13735 | Coil Bracket Assembly |
| A-13752 | Jaw Drive Assembly |
| A-13941 | Eject Assembly |
| A-13942 | Bracket Assembly |
| A-13961 | Trap Door Mech Assembly |
| A-13962 | Trap Door Assembly |
| A-13993 | Loop Assembly |
| A-13994 | Loop Weld Assembly |
| A-13995 | Drain Weld Assembly |
| A-13997 | Motor Assembly |
| A-14107 | Kicker Assembly |
| A-14138 | 3-Switch Assembly |
| A-14143 | Kickbig Assembly |
| A-14147 | Diverter Assembly |
| A-14151 | Disc Assembly |
| A-14155 | Trapdoor Hinge Assy |
| A-14156 | Shooter Ramp Assy |
| A-14161 | Lift Assembly |
| A-14163 | Lift Assembly |
| A-14190 | Drain Assembly |
| A-14196 | Shooter Gate Assembly |
| A-14231 | LED Assembly |
| A-14254 | Ball Dispenser Assembly |
| H-14252-3 | Rudy Eye Cable |
| H-14252-4 | Rudy Kicker Cable |
| 31-1588-50003-1 | Face, Screened |
| 31-1588-50003-2 | Back Of Head Screened |

`A-14138` ("3-Switch Assembly") is the same part number printed against switches 25, 27, and 28
(Lock Mech Right/Center/Left) on `switch-locations.md` — a single physical 3-switch bank assembly,
not three separate switch parts, matching the retained script's shared `WaSw25`/`WaSw27`/`WaSw28`
wall-target objects.
