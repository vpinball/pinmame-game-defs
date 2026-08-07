# Cirqus Voltaire — Solenoid/Flasher Table, General Illumination, Flipper Circuits, Motor Circuit

Transcribed from `Bally_1997_Cirqus_Voltaire_Manual.pdf`, PDF page 156, printed page 2-50. Unlike the
switch/lamp pages, Cirqus Voltaire prints solenoids, GI, flipper circuits, and the motor circuit as
one combined page rather than separate locations/wiring pages. Read directly from a 300 dpi
`pdftoppm` render; every row below was visually confirmed against the rendered page, not taken from
`pdftotext` alone (its column-shifted OCR was used only to find the page).

## Solenoid/Flasher table (01-28)

| Sol | Function | Type | Voltage conn. (Pf/BB/Cab) | Drive Xistor | Drive conn. (Pf/BB/Cab) | Wire | Part number |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Plunger | High Power | J133-2 | Q72 | J116-1 | VIO-BRN | AE-23-800 |
| 02 | Backbox Kick | High Power | / J134-3 | Q68 | / J118-2 | VIO-RED | AE-23-800 |
| 03 | Left Loop Magnet | High Power | J133-2 | Q71 | J116-4 | VIO-ORG | 20-10197 |
| 04 | Middle Jet Bumper | High Power | J133-2 | Q67 | J116-5 | VIO-YEL | AE-23-800 |
| 05 | Ramp Magnet | High Power | J133-2 | Q70 | J116-6 | VIO-GRN | 20-10197 |
| 06 | Diverter Power | High Power | J133-2 | Q66 | J116-7 | VIO-BLU | FL-11753 |
| 07 | Jet Up | High Power | J133-2 | Q69 | J116-8 | VIO-BLK | FL-11630 |
| 08 | Jet Release | High Power | J133-2 | Q65 | J116-9 | VIO-GRY | SM1-26-600 |
| 09 | Trough Eject | Low Power | J133-3 | Q44 | J114-1 | BRN-BLK | AE-26-1500 |
| 10 | Left Slingshot | Low Power | J133-3 | Q48 | J114-3 | BRN-RED | AE-26-1200 |
| 11 | Right Slingshot | Low Power | J133-3 | Q43 | J114-4 | BRN-ORG | AE-26-1200 |
| 12 | Upper Jet Bumper | Low Power | J133-3 | Q47 | J114-5 | BRN-YEL | AE-26-1200 |
| 13 | Lower Jet Bumper | Low Power | J133-3 | Q42 | J114-6 | BRN-GRN | AE-26-1200 |
| 14 | Left Saucer | Low Power | J133-3 | Q46 | J114-7 | BRN-BLU | AE-27-1200 |
| 15 | Right Saucer | Low Power | J133-3 | Q41 | J114-8 | BRN-VIO | AE-27-1200 |
| 16 | Lock Post | Low Power | J133-3 | Q45 | J114-9 | BRN-GRY | AE-26-1500 |
| 17 | Join Flashers | Flasher | J133-6 | Q28 | J111-1 | BLK-BRN | #906 |
| 18 | Ring #1 Flashers | Flasher | J133-6 | Q32 | J111-2 | BLK-RED | #906 |
| 19 | Ring #2 Flashers | Flasher | J133-6 | Q27 | J111-3 | BLK-ORG | #906 |
| 20 | Ring #3 Flashers | Flasher | J133-6 | Q31 | J111-4 | BLK-YEL | #906 |
| 21 | Right Playfield Flasher | Flasher | J133-6 | Q26 | J111-5 | BLU-GRN | #906 |
| 21 | Upper Right Backbox Fls | Flasher | / J134-5 | Q26 | / J112-6 | BLU-GRN | #906 (insert) |
| 22 | Motor Enable | Flasher | J133-6 | Q30 | J111-6 | BLU-BLK | A-15680 |
| 23 | Jet Flasher | Flasher | J133-6 | Q25 | J111-7 | BLU-VIO | #906 |
| 24 | Left Playfield Flasher | Flasher | J133-6 | Q29 | J111-8 | BLU-GRY | #906 |
| 24 | Upper Left Backbox Fls | Flasher | / J134-5 | Q29 | / J112-9 | BLU-GRY | #906 (insert) |
| 25 | Upper Left Flasher | Gen. Purpose | J133-6 | Q16 | J109-1 | BLU-BRN | #906 |
| 26 | Up. Right Playfield Fls | Gen. Purpose | J133-6 | Q15 | J109-2 | BLU-RED | #906 |
| 26 | Lower Left Backbox Fls | Gen. Purpose | / J134-5 | Q15 | / J107-3 | BLU-RED | #906 (insert) |
| 27 | Ringmaster Flashers (2) | Gen. Purpose | J133-6 | Q14 | J109-3 | BLU-ORG | #906 |
| 28 | Bear Playfield Flasher | Gen. Purpose | J133-6 | Q13 | J109-4 | BLU-YEL | #906 |
| 28 | Lower Right Backbox Fls | Gen. Purpose | / J134-5 | Q13 | / J107-5 | BLU-YEL | #906 (insert) |

Solenoids 21, 24, 26, 28 each drive one playfield flasher and one backbox insert-panel flasher off
the same driver transistor -- one physical control line, two flashlamps. Only the playfield bulb gets
a playfield coordinate. Solenoid 22 (Motor Enable) is printed inside the Flasher address block and
uses the same driver-transistor/connector columns as a flasher, but it is not a flashlamp: the
retained script's `MotorEnable` sub only plays/stops a motor sound, and the part number `A-15680`
matches the DC gearmotor part reused at solenoid 39 (Motor Direction) below -- it is the Ringmaster
motor's continuous enable line for the A-21953 Ring Master Assembly, not a bulb.

## General Illumination

| Item | Function | Type | Voltage conn. (Pf/BB/Cab) | Drive Xistor | Drive conn. (Pf/BB/Cab) | Wire | Bulb |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Playfield Right | G.I. | J105-1 | Q5 | J105-7 | WHT-BRN | #44 |
| 02 | Playfield Middle | G.I. | J105-2 | Q4 | J105-8 | WHT-ORG | #44 |
| 03 | Playfield Left | G.I. | J105-3 | Q3 | J105-9 | WHT-YEL | #44 |
| 04 | **Backbox 2 | G.I. | / J106-5 | Q2 | / J106-10 | WHT-GRN | #555 |
| 05 | **Backbox 1 | G.I. | / J106-6 + J104-3 | Q1 | / J106-11 + J104-1 | WHT-VIO | #555 |

`**THESE G.I. STRINGS DO NOT BRIGHTEN AND DIM, THEY ARE ALWAYS ON.` GI item 05 additionally reaches a
cabinet connector (`J104-1`/`J104-3`), the only GI row with a cabinet leg, so it feeds cabinet bulbs
as well as backbox bulbs. This page's own item numbers ("04"/"05") are the printed public GI address
plus one (public GI 3 = "04 Backbox 2", public GI 4 = "05 Backbox 1"); the retained script's
`UpdateGI` only ever dispatches `no = 0, 1, 2` (Playfield Right/Middle/Left), so GI addresses 3 and 4
have no runtime handler and no playfield coordinate. The separate Solenoid/Flashlamp Locations list
(`solenoid-flashlamp-locations.md`, printed page 2-46) prints the SAME two items with the connector
numbers omitted and the "Backbox 1"/"Backbox 2" labels swapped relative to this page; see
`conflict.gi-backbox-string-numbering` in the machine definition.

## Flipper Circuits

| Printed | Type | Voltage conn. (Playfield) | Power Xistor | Hold Xistor | Drive conn. (Playfield) | Wire (Power/Hold) | Coil part | Coil color |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | Power | J119-1 (RED-GRN) | Q90 | -- | J120-13 | YEL-GRN | FL-11630 | RED |
| 30 (Lower Right Flipper) | Hold | J119-1 (RED-GRN) | -- | Q92 | J120-11 | ORG-GRN | FL-11630 | RED |
| 31 | Power | J119-4 (RED-BLU) | Q87 | -- | J120-9 | YEL-BLU | FL-11630 | RED |
| 32 (Lower Left Flipper) | Hold | J119-4 (RED-BLU) | -- | Q89 | J120-7 | ORG-BLU | FL-11630 | RED |
| 33 (Popper) | Power | J119-6 (RED-VIO) | Q84 | -- | J120-6 | YEL-VIO | AL-25-1000 | BROWN |
| 34 (Diverter Hold) | Hold | J119-6 (RED-VIO) | -- | Q86 | J120-4 | ORG-VIO | FL-11730 | YELLOW |
| 35 (Ringmaster Magnet) | Power | J119-8 (RED-GRY) | Q81 | -- | J120-3 | YEL-GRY | 20-10197 | (n/a) |
| 36 (Upper Post) | Hold | J119-8 (RED-GRY) | -- | Q83 | J120-1 | ORG-GRY | AE-27-1200 | WHITE |

Printed 29-32 are the lower-flipper power/hold pairs; PinMAME's `CORE_FIRSTLFLIPSOL = 45` publishes
them at public 45-48 (29->45, 30->46, 31->47, 32->48), a +16 offset from the printed number. Printed
33-36 sit in the upper-flipper Fliptronic slot (`CORE_FIRSTUFLIPSOL = 33`) and equal their public
address unchanged, but the printed function names show all four are repurposed non-flipper devices
(Popper, Diverter Hold, Ringmaster Magnet, Upper Post) -- Cirqus Voltaire has no upper flippers,
matching `cvGameData`'s `FLIP_SOL(FLIP_L)` (lower flippers only).

## Motor Circuit

| Sol | Function | Type | Voltage conn. (Playfield) | Drive Gates | Drive conn. (Playfield) | Wire | Device part |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 37 | Neon | Low Power | J139-2 | U3A, U3B | J110-1 | BRN-WHT | A-21577 |
| 38 | Not Used | -- | -- | -- | -- | -- | -- |
| 39 | Motor Direction | Low Power | J133-6 | U3G, U3H | J110-4 | YEL-WHT | A-15680 |
| 40 | Eddy Board | Low Power | J139-2 | U3E, U3F | J110-5 | BLU-WHT | A-22151-2 |

Solenoid 39 (Motor Direction) is the Ringmaster motor's direction line, confirmed independently by
the retained script's own `cvpmMech` configuration (`mechRM.Sol1 = 22`, `mechRM.Sol2 = 39`). Pinned
PinMAME's own preliminary `cv_ringMech` table (`src/wpc/sims/wpc/prelim/cv.c`) instead names its
second solenoid public address 43, which is PinMAME's own WPC-95 LPDC mirror of 39
(`core_getSol`: `solNo` 41-44 read back at `solNo - 4`); both name the same physical drive line. The
device part `A-15680` is reused from solenoid 22 (Motor Enable) above, confirming both control the
same DC gearmotor assembly. Solenoid 40 (Eddy Board, part A-22151-2) is a control-board circuit for
the eddy-current sensor boards (switches 17/26/75/76's A-18008-1 assemblies use the closely related
part A-22149-2, "Auto Adjust Eddy Sensor PCB", per the Lower Playfield Parts list) rather than a
discrete moving playfield device.

`J1XX = POWER DRIVER BOARD`. `24-6549 = #44 BULB; 24-8768 = #555 BULB; 24-8802 = #906 BULB`.
