# White Water — Chase Lamp board (backbox placement and schematic)

Source: `Williams_1993_White_Water_English_Manual.pdf`. Three pages establish
that solenoid addresses 27/28 ("Chase Lamp Clock"/"Chase Lamp Data") drive a
backbox-only 16-lamp animation, not a playfield feature.

## PDF page 66, printed "Backbox Assembly" parts breakdown

The Backbox Assembly exploded-parts list enumerates, among other backbox
components (Knocker & Bracket Assy., Power Driver Assembly, WPC Sound
Board, WPC CPU Board, Dot Matrix Display/Driver Board, Speaker/Display
Assy., Backglass Assembly):

| Item | Part | Description |
| --- | --- | --- |
| 17 | A-15765 | 8-Lamp Board Assembly |
| 19 | A-15761 | Chase Light PC Board |

Both boards are listed **only** here, in the Backbox Assembly breakdown —
neither A-15765 nor A-15761 appears anywhere in the Lower Playfield Parts
(PDF page 101) or Upper Playfield Parts (PDF page 100) lists.

## PDF page 132, printed page 3-22, "A-15765 8-lamp Board Assembly & Schematic"

Two A-15765 8-lamp boards are wired from the Chase Lamp board's two output
connectors, "Left Side" from J2 and "Right Side" from J3, each carrying 8
lamp positions (L1-L8) on #194 bulbs:

```
Left Side                                       Right Side
J1 - 1  Red from Chase Lamp Board J2-11         J1 - 1  Red from Chase Lamp Board J3-2
J1 - 2  Red from Chase Lamp Board J2-10         J1 - 2  Red from Chase Lamp Board J3-1
J1 - 3  N/C                                     J1 - 3  N/C
J1 - 4  Blue-Yellow  from J2-8                  J1 - 4  Black-Yellow from J3-7
J1 - 5  Blue-Orange  from J2-1                  J1 - 5  Black-Orange from J3-4
J1 - 6  Blue-Red     from J2-3                  J1 - 6  Black-Red    from J3-9
J1 - 7  Blue-Brown   from J2-5                  J1 - 7  Black-Brown  from J3-11
J1 - 8  Blue-Green   from J2-7                  J1 - 8  Black-Green  from J3-6
J1 - 9  Blue-Gray    from J2-4                  J1 - 9  Black-Gray   from J3-10
J1 - 10 Blue-Violet  from J2-2                  J1 - 10 Black-Violet from J3-8
J1 - 11 Blue-Black   from J2-6                  J1 - 11 Black-Blue   from J3-5
```

Two independent 8-lamp boards (16 bulbs total, #194) driven from a shared
16-bit shift register match `ww_wpc_w`'s handling of `WPC_SOLENOID1`
GET_BIT2 (clock)/GET_BIT3 (data): a 16-bit `lamps` register is shifted in
serially and then split into two bytes written to
`coreGlobals.tmpLampMatrix[8]` and `tmpLampMatrix[9]` — PinMAME's public
lamp-column convention publishes these as addresses 91-98 (low byte) and
101-108 (high byte). The retained VPX table's `InitLights(InsertLights)`
collection contains no member named for any of these sixteen addresses, so
the retained recreation does not model this board's individual bulbs; only
its backbox placement is established from the manual.

There is no evidence in either printed page for which physical byte (low or
high) feeds the Left board versus the Right board, so the sixteen addresses
are enumerated generically here rather than split into "Left"/"Right"
groups the curator cannot substantiate.
