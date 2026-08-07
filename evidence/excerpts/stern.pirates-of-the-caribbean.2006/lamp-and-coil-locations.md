# Lamp Locations and Coil & Flash Lamp Locations

Transcribed from `Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf`,
PDF page 9 (printed "DR. 7", header `LAMP LOCATIONS {Lamp Matrix Grid (01-80) on the
previous page}`) and PDF page 11 (printed "DR. 9", header `COIL & FLASH LAMP LOCATIONS
{Coils Detailed Chart Table on the previous page}`).

Both pages are drawings: a plan view of the playfield with numbered callout boxes, plus a
separate inset drawing of the back panel. The transcription below records every legend,
every printed note, and which callouts appear on which drawing. A rendered crop of the
back-panel inset accompanies this transcription because the fact it fixes -- that lamps
33-39 and 78-80 are back-panel devices -- is carried by the drawing, not by prose.

## Lamp Locations page (PDF page 9)

Legend, four entries, printed with a white / black / grey swatch strip:

```
[white] = Lamps above Playfield.
[black] = Lamps below Playfield.
[grey]  = Lamps on Back Panel.
        = LEDs on PCB.
```

Lamp Part Notes printed beside the legend:

```
Lamp Part Notes:  #555 Wedge Base (W.B.) Bulb Clear = 165-5002-00.
#44 Bayonet Bulb (Heavy Filament) Clear = 165-5000-44-HF.

See Section 4, Chapter 1, Parts Identification & Location.
Pages 62-64 for more details on bulbs and corresponding sockets.
Some Lamp Diodes may be located under the playfield, in the Cabinet
or Backbox on Terminal Strips and not on or with the Lamp Socket.

DOTS:  Diode On Terminal Strip.
```

Notes printed inside the drawing:

```
THERE ARE 10 LAMPS (7 RED / 3 GREEN) LOCATED ON THE BACK PANEL.

THE TOP TEN CLEAR BULBS ARE G.I.s; NOT CONTROL LAMPS.

THE 3 LEDS MODULES ON THE RIGHT RAMP ARE G.I.s; NOT CONTROL LAMPS.
```

Callouts drawn inside the **back-panel inset**: `33`, `34`, `35`, `36`, `37`, `38`, `39`,
`78`, `79`, `80` -- ten grey-shaded boxes, matching the ten back-panel lamps the inset's own
note counts as `7 RED / 3 GREEN`. Lamps 33-39 are the seven red ones and 78-80 the three
green ones, which is also the split the Lamp Matrix Grid's own bulb-type column prints
(`#44 Red` for 33-39, `#44 Green` for 78-80).

Callouts drawn on the **playfield**: every remaining lamp number 3-32 and 40-77, plus
`27` drawn three times (one per pop bumper, matching the matrix's `POP BUMPER (X3)`),
`8` drawn twice at the centre of the compass ring (matching `FOUR WINDS (X2)`), and the
group `24 32 40 48 56` together with `64 72` drawn as one grey strip at the Heart Chest --
the `520-5258-00` LED PCB. Lamps `1` and `2` (START BUTTON, TOURNAMENT START BUTTON) are
not drawn on the playfield at all; they are cabinet button lamps.

Also printed on the page: `LAMP MENU: ONE, ALL, ROW, COLUMN & ORDERED` and a
`Typical Lamp Schematic & Wiring` inset showing `Column: 18V YEL-XXX` -> bulb ->
`Row: Ground RED-XXX` with a `1N4004 DIODE` and a `CATHODE banded side` note, and
`-XXX = Varying Wire Color. See Matrix Grid for color.`

## Coil & Flash Lamp Locations page (PDF page 11)

Legend, four entries:

```
[white] = Coils / Flash Lamps above Playfield.
[black] = Coils / Flash Lamps below Playfield.
[grey]  = Coils / Flash Lamps on Back Panel.
[Color] = Color of Mini-Mars or Flash Lamp Bulb.
```

Notes printed beside the legend:

```
Coil Q24 is Optional.  If either a Coin Meter, Token Dispenser or Knocker
(all optional equipment) is required, call Technical Support for more
information, 1-800-542-5377 or 1-708-345-7700.

DOTS:  Diode On Terminal Strip.
```

Callouts drawn on the **playfield**: `1`, `2`, `3`, `4`, `5`, `6`, `9`, `10`, `11`, `15`,
`16`, `18`, `19`, `20`, `21`, `22`, `23`, `25`, `26`, `27`, `28`, `29`, `30` (twice),
`31`, `32`.

Callouts drawn inside the **back-panel inset**: `30` and `22`, both grey-shaded.

Also printed on the page: `COIL MENU: SINGLE COIL & CYCLING COIL` and a `Typical Coil
Wiring & Schematic` inset worked through coil #1: `FROM YEL-VIO Voltage Outputs 50v DC`,
`J10-P4/5 I/O BD.`, `#1 Trough Up-Kicker 26-1200 Gauge - Turn`, `1N4004 DIODE LOCATED ON
I/O PWR. DRV. BD.`, `Conn. J8-P1 I/O Pwr. Drv. Bd.`, `Q1 I/O Bd. Drive Transistor`,
`I/O Bd. +50v`, `BRN-BLK`, `YEL-VIO`, `Power Voltage Supply 50vdc`.

## The three bumper callouts, and why they matter

The three pop-bumper coil callouts `9` (LEFT BUMPER), `10` (RIGHT BUMPER) and `11`
(BOTTOM BUMPER) are drawn at three distinct positions of one triangular bumper cluster in
the rear-right third of the playfield. Reading the drawing's own geometry against the
printed names: `9` sits at the cluster's left-hand position, `10` at its right-hand
position, and `11` at the position nearest the player. The matching switch names
(`SW. #30 LEFT BUMPER`, `SW. #31 RIGHT BUMPER`, `SW. #32 BOTTOM BUMPER`) describe the same
three physical bumpers.

## Flasher quantities as this page draws them

- `22` (`FLASH: REAR CENTER (X2)`) is drawn once on the playfield and once in the
  back-panel inset.
- `30` (`FLASH: BACK RIGHT [X3]`) is drawn twice on the playfield and once in the
  back-panel inset.

Both counts add up to the quantities the Coils Detailed Chart prints. This disagrees with
the Back Panel Assembly parts page (printed page 91), which lists exactly two `#89` bulb
sockets on the back panel and labels **both** of them `Q22 FLASH`. The disagreement is
recorded as an unresolved conflict rather than resolved here.
