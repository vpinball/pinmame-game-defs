# FunHouse — Switch/Lamp/Solenoid Circuits (printed page 3-16, "FUNHOUSE 3-16")

Source: `Funhouse_OPS.pdf`, PDF page 119, rendered at 300 dpi and read directly from the image.
This is the Section 3 "Interboard Wiring" tabular reference (distinct from the box-and-line
schematic on the preceding page, `Funhouse_OPS.pdf` page 118).

## Switch Circuits — connector from CPU board

| Wire Color | Function | To Playfield | To Cabinet | Transistor |
| --- | --- | --- | --- | --- |
| Green/Brown | Column 1 | J207-1 | J212-1 | U20-18 |
| Green/Red | Column 2 | J207-2 | J212-2 | U20-17 |
| Green/Orange | Column 3 | J207-3 | J212-3 | U20-16 |
| Green/Yellow | Column 4 | J207-4 | — | U20-15 |
| Green/Black | Column 5 | J207-5 | — | U20-14 |
| Green/Blue | Column 6 | J207-6 | — | U20-13 |
| Green/Violet | Column 7 | J207-7 | — | U20-12 |
| Green/Gray | Column 7 (sic, printed twice; matrix legend confirms the physical Column 8 wire) | J207-8 | — | U20-11 |
| White/Brown | Row 1 | J209-1 | J212-4 | U18-11 |
| White/Red | Row 2 | J209-2 | J212-6 | U18-9 |
| White/Orange | Row 3 | J209-3 | J212-7 | U18-5 |
| White/Yellow | Row 4 | J209-4 | J212-8 | U18-7 |
| White/Green | Row 5 | J209-5 | — | U19-11 |
| White/Blue | Row 6 | J209-7 | — | U19-9 |
| White/Violet | Row 7 | J209-8 | — | U19-5 |
| White/Gray | Row 8 | J209-9 | — | U19-7 |
| Orange/Brown | Direct 1, Left Coin | J205-1 | — | U17-5 |
| Orange/Red | Direct 2, Center Coin | J205-2 | — | U17-7 |
| Orange/Black | Direct 3, Right Coin | J205-3 | — | U17-11 |
| Orange/Yellow | Direct 4, 4th Coin | J205-4 | — | U17-9 |
| Orange/Green | Direct 5, Escape/Service | J205-6 | — | U16-9 |
| Orange/Blue | Direct 6, Down/Vol Down | J205-7 | — | U16-11 |
| Orange/Violet | Direct 7, Up/Vol Up | J205-8 | — | U16-7 |
| Orange/Gray | Direct 8, Enter/Test | J205-9 | — | U16-5 |
| Black | Ground | J205-10 | — | — |
| Orange/White | Enable | J205-12 | — | — |

## Lamp Circuits — connectors from Power Driver Board

| Wire Color | Function | To Playfield | To Cabinet | Transistor |
| --- | --- | --- | --- | --- |
| Yellow/Brown | Column 1 | J138-1 | — | Q98 |
| Yellow/Red | Column 2 | J138-2 | — | Q97 |
| Yellow/Orange | Column 3 | J138-3 | — | Q96 |
| Yellow/Black | Column 4 | J138-4 | — | Q95 |
| Yellow/Green | Column 5 | J138-5 | — | Q94 |
| Yellow/Blue | Column 6 | J138-6 | — | Q93 |
| Yellow/Violet | Column 7 | J138-7 | — | Q92 |
| Yellow/Gray | Column 8 | J138-9 | J136-3 | Q91 |
| Red/Brown | Row 1 | J133-1 | — | Q90 |
| Red/Black | Row 2 | J133-2 | — | Q89 |
| Red/Orange | Row 3 | J133-3 | J133-3 | Q88 |
| Red/Yellow | Row 4 | J133-5 | J133-5 | Q87 |
| Red/Green | Row 5 | J133-6 | J133-6 | Q86 |
| Red/Blue | Row 6 | J133-7 | J133-7 | Q85 |
| Red/Violet | Row 7 | J133-8 | J133-8 | Q84 |
| Red/Gray | Row 8 | J133-9 | J133-9 | Q83 |

## Solenoid Circuits — connectors from Power Driver Board

| Wire Color | Function | To Playfield | Transistor |
| --- | --- | --- | --- |
| Violet/Brown | Solenoid 1, High Power | J130-1 | Q82 |
| Violet/Red | Solenoid 2, High Power | J130-2 | Q80 |
| Violet/Orange | Solenoid 3, High Power | J130-4 | Q78 |
| Violet/Yellow | Solenoid 4, High Power | J130-5 | Q76 |
| Violet/Green | Solenoid 5, High Power | J130-6 | Q64 |
| Violet/Blue | Solenoid 6, High Power | J130-7 | Q66 |
| Violet/Black | Solenoid 7, High Power | J130-8 | Q68 |
| Violet/Gray | Solenoid 8, High Power | J130-9 | Q70 |
| Brown/Black | Solenoid 9, Low Power | J127-1 | Q58 |
| Brown/Red | Solenoid 10, Low Power | J127-2 | Q56 |
| Brown/Orange | Solenoid 11, Low Power | J127-4 | Q54 |
| Brown/Yellow | Solenoid 12, Low Power | J127-5 | Q52 |
| Brown/Green | Solenoid 13, Low Power | J127-6 | Q50 |
| Brown/Blue | Solenoid 14, Low Power | J127-7 | Q48 |
| Brown/Violet | Solenoid 15, Low Power | J127-8 | Q46 |
| Brown/Gray | Solenoid 16, Low Power | J127-9 | Q44 |
| Black/Brown | Flasher 1, No Diode | J126-1 | Q42 |
| Black/Red | Flasher 2, No Diode | J126-2 | Q40 |
| Black/Orange | Flasher 3, No Diode | J126-3 | Q38 |
| Black/Yellow | Flasher 4, No Diode | J126-4 | Q36 |
| Blue/Green | Special 1 Drive (Diode: J126-10) | J126-5 | Q28 |
| Blue/Black | Special 2 Drive (Diode: J126-11) | J126-6 | Q30 |
| Blue/Violet | Special 3 Drive (Diode: J126-12) | J126-7 | Q34 |
| Blue/Gray | Special 4 Drive (Diode: J126-13) | J126-8 | Q32 |
| Blue/Brown | Special 5 Drive (Diode: J122-5) | J122-1 | Q26 |
| Blue/Red | Special 6 Drive (Diode: J122-6) | J122-2 | Q24 |
| Blue/Orange | Special 7 Drive (Diode: J122-8) | J122-3 | Q22 |
| Blue/Yellow | Special 8 Drive (Diode: J122-9) | J122-4 | Q20 |

This table's "Solenoid 1-16" rows map 1:1 to the printed solenoid addresses on
`solenoid-locations.md` and are used directly for the promoted definition's `wiring` field on
those sixteen devices. The "Flasher 1-4" and "Special 1-8 Drive" rows use a generic driver-board
naming convention (this appears to be a standardized Special Solenoid Driver board reused across
multiple WPC titles) that does not correspond 1:1 with FunHouse's own printed flasher/motor
addresses (17-28); the box-and-line schematic on the preceding page (`Funhouse_OPS.pdf` page 118)
shows the actual game-specific harness instead, routing J107/J122/J126 to the Eyes (25-28),
Flasher (17-20, 23-24), Mouth Motor (21), and Up/Down Driver (22) circuits by function rather than
by this table's generic "Special N" numbering. Because reconciling this table's generic connector
numbering with the specific public addresses 17-28 pin-for-pin was not completed, the promoted
definition does not assert a `wiring` connector/transistor value for solenoids 17-28; their
existence, printed part numbers, and general driver-board grouping are still recorded from
`solenoid-locations.md` and the page-118 schematic.
