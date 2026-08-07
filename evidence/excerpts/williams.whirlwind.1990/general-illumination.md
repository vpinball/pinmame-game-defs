# Whirlwind — General Illumination (GI Relay Boards)

Transcribed from `Whirlwind_OPS.pdf`, PDF page 63, printed page 53, "Lamp
Boards" (Section 2), the two GI relay board entries. Read from the 300 dpi
rendered page.

## Playfield Relay Boards (Solenoids 11 & 16 Gen. Illum) p/n C-11902-1

| Part Number | Description |
| --- | --- |
| 5768-12221-00 | PC Board |
| 5070-09054-00 | Diode, 1N4004, 1.0A. |
| 5580-12145-00 | Relay, 24vdc, 30A. |
| 5791-12273-02 | Header, 2-pin Sq post (J1) |
| 5791-12273-07 | Header, 7-pin Sq post (J2) |

## Backbox Relay Board (Solenoid 16 Gen. Illum) p/n C-11998-1

| Part Number | Description |
| --- | --- |
| 5768-12243-00 | PC Board |
| 5070-09054-00 | Diode, 1N4004, 1.0A. (D1) |
| 5580-09555-01 | Relay, 24vdc, 30A. (K1) |
| 5010-09534-00 | Resistor, 0-ohm (W1, W2) |
| 5791-12273-02 | Header, 2-pin Sq post (J1) |
| 5791-12273-07 | Header, 7-pin Sq post (J2) |

The board title itself states solenoid 11 and solenoid 16 both drive the
C-11902-1 "Playfield Relay Boards" (its one part number, `5580-12145-00`,
appears footnoted `*`/`(4b)` twice in the Solenoid Table — once for solenoid
11's own relay, once for solenoid 16's playfield-side relay). Solenoid 16
*additionally* drives a second, separate relay on the C-11998-1 "Backbox
Relay Board" (footnoted `***`/`(4a)`, part `5580-09555-01`). This confirms
solenoid 16 energizes two physically separate relays simultaneously — one on
the playfield-side board (lower playfield GI) and one on the backbox board
(backbox/backglass GI) — while solenoid 11 drives only the single
upper-playfield relay.
