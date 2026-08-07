# Twilight Zone — Solenoid/Flasher Locations

Transcribed from `Twilight_Zone_OPS.pdf`, PDF page 62, printed page 2-53, "SOLENOID / FLASHER
LOCATIONS", together with the Flipper Coils list printed on the same page. Read from the rendered
page; the retained scan is image-only. The General Illumination Circuits table printed on the same
page is transcribed separately as `general-illumination.md`. The retained scan is missing the
Solenoid/Flasher Table wiring page (printed 2-52), so drive transistors, connectors and voltage
rails are not available from this manual for these addresses.

| Item | Coil/Flasher Number | Assembly Number | Description |
| --- | --- | --- | --- |
| 01 | AE-24-900 | A-16434 | Slot Kickout |
| 02 | AL-23-800 | A-16647 | Rocket Kicker |
| 03 | AL-23-800 | A-16647 | Auto-Fire Kicker |
| 04 | AE-23-800 | A-16312 | Gumball Popper |
| 05 | AE-26-1200 | A-16361 | Right Ramp Diverter |
| 06 | AE-26-1500 | A-16313 | Gumball Diverter |
| 07 | AE-23-800 | B-10686-1 | Knocker |
| 08 | AE-27-1200 | A-8039-3 | Outhole |
| 09 | AE-26-1200 | A-16766 | Ball Release |
| 10 | AE-27-1200 | A-16645-R | Right Slingshot |
| 11 | AE-27-1200 | A-16645-L | Left Slingshot |
| 12 | AE-26-1200 | A-9415-2 | Lower Jet Bumper |
| 13 | AE-26-1200 | A-9415-2 | Left Jet Bumper |
| 14 | AE-26-1200 | A-9415-2 | Right Jet Bumper |
| 15 | AE-27-1200 | A-16307 | Lock Release |
| 16 | SZ-33-3000 | A-16338 | Shooter Diverter |
| 17 | 24-8802 | A-12336-1 | Bumpers (2) |
| 18 | 24-8802 | A-12336-1 / A-16060 | Power Payoff (2) |
| 19 | 24-8802 | A-12336-1 | Mini-playfield (2) |
| 20 | 24-8802 | A-16330 / A-16060 | Upper Left Ramp (2) |
| 21 | 20-9247 | ---- | Left Magnet |
| 22 | ---- | ---- | Not Used |
| 23 | 20-9247 | ---- | Lower Right Magnet |
| 24 | 14-7984 | A-16132 | Gumball Motor |
| 25 | 20-9247 | A-16749 | Left Mini-playfield Magnet |
| 26 | 20-9247 | A-16749 | Right Mini-playfield Magnet |
| 27 | AE-26-1500 | A-16064 | Left Ramp Diverter |
| 28 | 24-8802 | A-16060 | Inside Ramp / Gumball Machine High / Gumball Machine Middle / Gumball Machine Low |
| 37 | 24-8802 | A-12336-1 | Upper Right Flipper |
| 38 | 24-8802 | A-16651-4 | Gumball Machine High |
| 39 | 24-8802 | A-16651-4 | Gumball Machine Middle |
| 40 | 24-8802 | A-16651-4 | Gumball Machine Low |
| 41 | 24-8802 | A-16330 / A-16060 | Upper Right Ramp |
| 42 | ---- | A-16120 | Clock Reverse |
| 43 | ---- | A-16120 | Clock Forward |
| 44 | ---- | A-16100 | Clock Strobe |

## Printed board-callout numbers vs public addresses

Items 37-44 are the printed circuit-board callout numbers for the auxiliary solenoid board, not
PinMAME public addresses. The retained script's own comments map them explicitly: `SolModCallback(51)`
through `(55)` are annotated `'(37)` through `'(41)`, and the commented-out clock lines read
`'SolCallback(56)' '(42) Clock Reverse'`, `'SolCallback(57)' '(43) Clock Forward'`, `'SolCallback(58)'
'(44) Clock Switch Strobe'`. So printed 37-41 = public 51-55, and printed 42/43/44 = public 56/57/58.
Pinned PinMAME's own `#define sClockFwd CORE_CUSTSOLNO(6)` (=56) and `#define sClockRev
CORE_CUSTSOLNO(7)` (=57) name the *opposite* direction from this printed table and the script's own
cross-reference comment — recorded as `conflict.clock-motor-direction-naming`.

## Flipper Coils (same page)

| Coil | Color | Assembly | Description |
| --- | --- | --- | --- |
| FL-15411 | Orange | A-15205-L-4 | Lower Left Flipper |
| FL-15411 | Orange | A-15205-R-4 | Lower Right Flipper |
| FL-11753 | Yellow | A-15205-L-1 | Upper Left Flipper |
| FL-11722 | Green | A-15205-R-3 | Upper Right Flipper |

Confirms Twilight Zone genuinely has four flippers (two lower, two upper), matching `tzGameData`'s
`FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U)`.
