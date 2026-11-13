---
source: pinball_robowar_gottlieb_instruction_manual_2_of_2.pdf
source_sha256: f96ce0b20bebce7fdd085809e00c2eef6cc044957ec3942353f48fd053debb83
locator: PDF page 12; printed folio 42; X. WIRING AND SCHEMATIC DIAGRAMS, PARTS LISTS - PLAYBOARD "NON-CONTROLLED" SOLENOIDS (lamp list at left); title block PLAYBOARD SOLENOIDS AND ILLUMINATION, drawing E-25887
method: Visual transcription from the 600 dpi native page render, checked against Windows OCR
transcribed_by: curator transcription
reviewed: true
status: curator transcription checked row by row against the rendered page; uncertain readings are marked
---

# Page 42 - Playboard lamps and "non-controlled" solenoids

Page heading (left part): `C DIAGRAMS, PARTS LISTS` (the left part `X. WIRING AND SCHEMATI` is on page 41, so the word is cut at the page edge). Section heading above the right-hand part: `PLAYBOARD "NON-CONTROLLED" SOLENOIDS`. Folio `42`.

Conventions: `[nnn]` is a wire colour code box. Lamps are drawn as a bulb symbol on each lamp line; all lamp lines (except the Sound 16 line and the Launch Attack lamp) end at one vertical rail at the right of the lamp block, which carries the arrow label `+6V DC` with wire box `[255]`. The page prints no bulb type on the lamps; the page 41 note 5 states "UNLESS OTHERWISE SPECIFIED, ALL LAMPS ARE TYPE #44" and note 2 names the driver transistors (see page 41 transcription). No transistor notes are printed on this page.

## 1. Lamp list (left block)

Printed literally. "Bulbs" is the number of bulb symbols drawn on that line.

### Connector A3J2 and A3J3 (first group)

| Lamp | Connector pin | Wire | Printed name | Bulbs |
| --- | --- | --- | --- | --- |
| L4 | A3J2 pin 2 | [500] | SOUND 16 | none drawn; the line runs to `A9P1` pin 5, labelled `FROM BOTTOM CABINET` |
| L3 | A3J3 pin C (printed with an overbar) | [588] | "SHOOT AGAIN" | 1 |
| L5 | A3J2 pin 3 | [511] | #1 BONUS "R" | 1 |
| L6 | A3J2 pin 5 | [522] | #2 BONUS "O" | 1 |
| L7 | A3J2 pin 4 | [533] | #3 BONUS "B" | 1 |
| L8 | A3J2 pin 10 | [544] | #4 BONUS "O" | 1 |
| L9 | A3J2 pin 9 | [555] | #5 BONUS "W" | 1 |
| L10 | A3J2 pin 7 | [577] | #6 BONUS "A" | 1 |
| L11 | A3J2 pin 8 | [566] | #7 BONUS "R" | 1 |

(L3's connector label `A3J3` is printed above its pin; the block of L5-L11 is labelled `A3J2`. L4 is labelled `A3J2`.)

### Connector A3J3 (second group)

| Lamp | A3J3 pin | Wire | Printed name | Bulbs |
| --- | --- | --- | --- | --- |
| L15 | 23 | [111] | 1X | 2, drawn in parallel |
| L16 | 13 | [144] | 2X | 2, in parallel |
| L17 | 14 | [155] | 4X | 2, in parallel |
| L18 | 16 | [177] | 8X | 2, in parallel |
| L19 | 15 | [166] | #1 TOP ROLLOVER, EXTRA BALL | 1 |
| L20 | 21 | [333] | #2 TOP ROLLOVER, EXTRA BALL | 1 |
| L21 | 20 | [322] | #3 TOP ROLLOVER, EXTRA BALL | 1 |
| L22 | 18 | [300] | #4 TOP ROLLOVER, EXTRA BALL | 1 |
| L23 | 19 | [311] | #1 TOP ROLLOVER, "R" | 1 |
| L24 | 9 | [344] | #2 TOP ROLLOVER, "O" | 1 |
| L25 | 10 | [355] | #3 TOP ROLLOVER, "B" | 1 |
| L26 | 12 | [377] | #4 TOP ROLLOVER, "O" | 1 |
| L27 | 11 | [366] | #1 TOP DROP TARGET, "B" | 1 |
| L28 | Y | [533] | #2 TOP DROP TARGET, "E" | 1 |
| L29 | X | [522] | #3 TOP DROP TARGET, "T" | 1 |
| L30 | V | [500] | #4 TOP DROP TARGET, "A" | 1 |
| L31 | W | [511] | TOP DROP TARGETS, "BASE" | 1 |
| L32 | 5 | [544] | RIGHT DROP TARGETS, "ALPHA III" | 1 |
| L33 | 6 | [555] | CENTER DROP TARGETS, "ALPHA II" | 1 |
| L34 | K | [566] | LEFT DROP TARGETS, "ALPHA I" | 1 |
| L35 | 7 | [577] | LEFT SIDE SPOT TARGET, SPECIAL | 1 |

### Connector A3J4

| Lamp | A3J4 pin | Wire | Printed name | Bulbs |
| --- | --- | --- | --- | --- |
| L36 | 1 | [700] | RIGHT SIDE ROLLOVER, SPECIAL | 1 |
| L37 | 2 | [711] | LEFT OUT ROLLOVER, SPECIAL | 1 |
| L38 | 4 | [722] | RIGHT OUT ROLLOVER, SPECIAL | 1 |
| L39 | 3 | [733] | LEFT SIDE SPOT TARGET, ADVANCE MULTIPLIER | 1 |

### Connector A3J3 (third group)

| Lamp | A3J3 pin | Wire | Printed name | Bulbs |
| --- | --- | --- | --- | --- |
| L40 | 4 | [777] | TOP RIGHT ROLLUNDER, ADVANCE MULTIPLIER | 1 |
| L41 | 3 | [755] | RIGHT RETURN ROLLOVER, ADV. MULTIPLIER | 1 |
| L42 | T | [766] | STARGATE, ADVANCE MULTIPLIER | 1 |
| L43 | 2 | [744] | STARGATE, "BATTLE STATION" | 1 |
| (no lamp number) | none | [300] | STARGATE, "LAUNCH ATTACK" | 1 |
| L44 | D | [800] | SPINNER | 1 |
| L45 | F | [822] | TOP LEFT POP BUMPER | 1 |
| L46 | P | [866] | TOP RIGHT POP BUMPER | 1 |
| L47 | M | [844] | BOTTOM POP BUMPER | 1 |

### Uncontrolled lamp: STARGATE, "LAUNCH ATTACK"

This lamp has no lamp number and no A3 connector pin. It has one bulb, whose right side goes to the +6V DC lamp rail. Its left side runs down and left to wire box `[300]`, then through a contact labelled `ON RAMP SW.` (two parallel plates, normally-open symbol) to wire box `[9]`, with an arrow label `GROUND FROM 1A18J2-8`.

### Lamp-driver numbers absent from this page (between L0 and L51)

L0, L1, L2, L12, L13, L14, L48, L49, L50, L51.

- L0, L1, L12 and L13 are printed on page 41 beside the relay coils (L0 Q relay, L1 T relay, L12 S relay, L13 A relay); L2 and L14 appear on page 41 as the 2A16 driver inputs (A9P1 pin 6 and A3J3 pin 22).
- L48-L51 are not drawn anywhere on page 42 (the ground list names `L44-L51`, but no lamp lines past L47 are drawn on this page).

Lamp numbers present on this page: L3 to L11 and L15 to L47 (42 numbered lamp lines, including the bulb-less L4 Sound 16 line), plus the unnumbered Launch Attack lamp.

## 2. Ground returns from A3 master driver board (bottom centre)

Bracket label `GROUND RETURNS FROM A3 MASTER DRIVER BOARD`. Each is a [9] wire to the connector `A9P2`.

| A3 connector pin | Printed text | A9P2 pin |
| --- | --- | --- |
| A3J2 pin 6 | GROUND (L0-L11) | 1 |
| A3J3 pin Z | GROUND (L12-L19) | 2 |
| A3J3 pin 17 | GROUND (L20-L27) | 3 |
| A3J3 pin U | GROUND (L28-L35) | 4 |
| A3J3 pin S | GROUND (L40-L43) | 5 |
| A3J3 pin C | GROUND (L44-L51) | 6 |
| A3J6 pin 4 | GROUND (SOLENOIDS 3,4, AND 7) | 12 |
| A3J4 pin 5 | GROUND (L36-L39) | 7 |
| A3J4 pin 9 | GROUND (SOLENOIDS 1 AND 9) | 8 |
| A3J4 pin 10 | GROUND (SOLENOID 2) | 9 |
| A3J4 pin 11 | GROUND (SOLENOID 6) | 10 |
| A3J4 pin 14 (?) | GROUND (SOLENOID 5) | 11 |

All wire boxes read `[9]`. Printed spacing in the solenoid line is "(SOLENOIDS 3,4, AND 7)" and "(SOLENOIDS 1 AND 9)". The pin of the last row is hard to read (see Uncertain readings).

## 3. Grounds from the transformer panel (connector 1A18J2, right edge)

Bracket label `GROUNDS FROM TRANSFORMER PANEL`. All wires `[9]`.

| 1A18J2 pin | Connects to (as drawn / printed) |
| --- | --- |
| 6 | the first kicking rubber coil ground loop |
| 7 | the second kicking rubber coil ground loop |
| 1 | `GROUND` line of the 1A8 pop bumper driver board (1A8J1 pin 2) |
| 2 | `GROUND` line of the 2A8 pop bumper driver board (2A8J1 pin 2) |
| 3 | `GROUND` line of the 3A8 pop bumper driver board (3A8J1 pin 2) |
| 9 | `1A11J1` pin 2 (`TO AUX. LAMP DRIVER`) |
| 8 | arrow label `GROUND TO "ON" RAMP SWITCH` |
| 5 | arrow label `GROUND TO 2A16J1-1 COLLECTORS` |
| 4 | arrow label `GROUND TO 1A16J1-1 COLLECTORS` |

`1A11J1` (label `TO AUX. LAMP DRIVER`): pin 2 joined to the [9] ground of 1A18J2 pin 9; pin 4 carries wire `[688]` (the +5V line below).

## 4. Flippers (top right; connector A9P1, label FROM BOTTOM CABINET)

| A9P1 pin | Wire | Printed label | Coil | Part | Other end / switch |
| --- | --- | --- | --- | --- | --- |
| 1 | [033] | FLIPPER GROUND | FLIPPER COIL (left), diode across | 20095 | LEFT FLIPPER SW. (ON) |
| 2 | [044] | FLIPPER GROUND | FLIPPER COIL (right), diode across | 20095 | RIGHT FLIPPER SW. (ON) |

Drawing detail: the right-hand end of each flipper coil runs straight to the vertical rail at the right (the rail is labelled with a curved arrow `"Q" SWITCHED +24V DC`, wire box `[388]`). A second line from the centre of each coil symbol (below the part number) goes down and right through a contact drawn as two parallel plates with a diagonal slash (normally-closed symbol) to the same rail; an arrow from the printed text `LEFT FLIPPER SW. (ON)` / `RIGHT FLIPPER SW. (ON)` points at that contact. No fuse is drawn on the flipper circuits.

## 5. Kicking rubbers (two coils)

Two circuits, each: `KICKING RUBBER COIL`, part `1496`, a diode across the coil, the left end of the coil connected by a loop line to ground wire [9] (first coil: 1A18J2 pin 6; second coil: 1A18J2 pin 7), and the right end of the coil connected to two switch contacts in parallel, each drawn as two parallel plates (normally-open symbol), each labelled `KICKING RUBBER SW.`, each going to the +24V "Q" switched rail (see section 4). Total: 2 coils, 4 switches.

## 6. Pop bumpers (1A8, 2A8, 3A8 driver boards) and +5V DC

Each driver board connector (`1A8J1`, `2A8J1`, `3A8J1`) has the same five pins:

| Board | Pin 4 (switch wire) | Pin 6 | Pin 1 | Pin 5 | Pin 2 |
| --- | --- | --- | --- | --- | --- |
| 1A8J1 (TO 1A8 POP BUMPER DRIVER BOARD) | [077] to `TOP LEFT POP BUMPER` switch contact | [333] DC GROUND | [188] OUTPUT | [688] INPUT (+5V DC) | [9] GROUND |
| 2A8J1 (TO 2A8 POP BUMPER DRIVER BOARD) | [011] to `TOP RIGHT POP BUMPER SW.` switch contact | [333] DC GROUND | [488] OUTPUT | [688] INPUT (+5V DC) | [9] GROUND |
| 3A8J1 (TO 3A8 POP BUMPER DRIVER BOARD) | [022] to `BOTTOM POP BUMPER SW.` switch contact | [333] DC GROUND | [888] OUTPUT | [688] INPUT (+5V DC) | [9] GROUND |

(Literal switch labels: the first is printed `TOP LEFT POP BUMPER` without "SW."; the others `TOP RIGHT POP BUMPER SW.` and `BOTTOM POP BUMPER SW.`.)

- Pop bumper switch: drawn as two parallel plates (normally-open symbol) in series with pin 4; its far side is tied to the DC GROUND [333] line (pin 6) and to the vertical DC ground line at the right.
- Pop bumper coils: each labelled `POP BUMPER COIL`, part `5194`, with a diode across it. Left end = the OUTPUT wire (pin 1); right end goes to a fuse:

| Board | Output wire | Right-end wire | Fuse | Rating | Other fuse side wire |
| --- | --- | --- | --- | --- | --- |
| 1A8 | [188] | [200] | F15 | 2 AMP SLO-BLO | [388] |
| 2A8 | [488] | [211] | F16 | 2 AMP SLO-BLO | [388] |
| 3A8 | [888] | [233] | F17 | 2 AMP SLO-BLO | [388] |

- The three [388] wires join the `"Q" SWITCHED +24V DC` rail.
- The three [688] INPUT (+5V DC) lines join a vertical line fed by `A1J6` pin 18, wire [688], printed `+5V DC (SOURCE)`, label `FROM A1 CONTROL BOARD`; `A1J6` pin 9, wire [333], printed `DC GROUND`, feeds the DC ground vertical line. The [688] line also runs to `1A11J1` pin 4 (`TO AUX. LAMP DRIVER`).

## 7. General illumination and other uncontrolled lamps

No general-illumination strings are drawn on page 42. The playboard illumination lamps (6.3V AC, wires 066/000 with the T contact) and the +6V DC feed are on page 41. The only uncontrolled lamp on this page is the Stargate "Launch Attack" lamp (section 1) powered through the `ON RAMP SW.` contact, wire [300] and ground wire [9] from `1A18J2-8`.

## 8. Title block (bottom right)

| Field | Printed |
| --- | --- |
| Company | Premier Technology (with the registered mark) |
| TITLE | PLAYBOARD SOLENOIDS AND ILLUMINATION |
| DRAWN | handwritten initials, read as "G.P.D." (?) |
| APPROVED | handwritten "R.H.M." |
| DATE | APR-2-88 (printed `APR·2·88`) |
| Drawing number | E-25887 |

No revision letters are printed. Folio `42` at the page bottom.

## Counts

- Lamp lines transcribed: 42 numbered (L3-L11 and L15-L47) plus 1 unnumbered (Launch Attack) = 43. Of the numbered ones, L4 (Sound 16) has no bulb, L15-L18 have 2 bulbs each and the other 37 have 1, so 41 numbered lines drive 45 bulbs.
- Non-controlled coils: 2 flipper coils (20095), 2 kicking rubber coils (1496), 3 pop bumper coils (5194) = 7; fuses F15, F16, F17.
- Relays: none on this page.

## Uncertain readings

1. A3J4 pin for `GROUND (SOLENOID 5)`: the connector label prints `14` with the 1 partly obscured (OCR and render read `:4` / `14`); I read 14.
2. Drawn-by initials in the title block are handwritten; "G.P.D." is a best reading.
3. Which A3J3 connector label belongs to L3: the render prints `A3J3` above pin `C` (overbar) and `A3J2` above the L5-L11 block; L4 is labelled `A3J2` pin 2.
4. Which of the four possible connections the second end of each flipper coil makes (see section 4): the coil's right end runs straight to the rail, and a separate line from the coil centre goes through the slashed contact to the rail; I could not tell from the drawing alone whether the line from the centre is a tap of the coil.
5. Diode arrow directions on the flipper, kicking rubber and pop bumper coils were not transcribed.
