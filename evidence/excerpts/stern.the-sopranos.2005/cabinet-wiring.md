# The Sopranos — Cabinet / Coin Door Wiring Diagram

Transcribed from `Stern_2005_The_Sopranos_Service_Manual.pdf`, PDF page 131 (printed Section 5, Chapter 3, page 114,
"Cabinet / Coin Door Wiring Diagram"). The page is born-digital; its text layer was used and each item below was checked
against the rendered page. Only the parts a definition cites are transcribed; the speaker, transformer and power-interlock
wiring is left out.

## Matrix switches in the cabinet (CPU/SND BD. CN7 returns, CN5 drives, `All Above Switches Normally Open (N.O.)`)

| Return wire | CN7 pin | Item as printed |
| --- | --- | --- |
| WHT-GRY | 1 (`SW RETURN 8`) | PLUMB BOB TILT, N.O., SW. 56 |
| WHT-VIO | 2 (`SW RETURN 7`) | TOURNIE BUTTON, N.O., SW. 55; and `5th Coin Slot Future Use` |
| WHT-BLU | 3 (`SW RETURN 6`) | START BUTTON, N.O., SW. 54; and `Left Coin Slot` |
| WHT-GRN | 5 (`SW RETURN 5`) | `Center Coin Slot` / `U.S. Bill Acceptor` |
| WHT-YEL | 6 (`SW RETURN 4`) | `Right Coin Slot` |
| WHT-ORG | 7 (`SW RETURN 3`) | `6th Coin Slot Future Use` |
| WHT-RED | 8 (`SW RETURN 2`) | `4th Coin Slot European Use` |

Drives: `GRN-VIO SW DRIVE 7` (CN5 pin 8, the cabinet switches) and `GRN-BRN SW DRIVE 1` (`from CN5-P1 (Sw. Drive 1)`, the coin
door switches).

## Coin meter

`TO COIN METER`: `J16-7 +5V DC I/O DRVR BD 22 RED` and `J7-10 Q24 ... I/O DRVR BD 78 VIO-GRY`.

## Dedicated switches (CPU/SND BD. CN6)

- `Memory Protect Switch`, `BLK-RED`, `from CPU CN6` pin `12`.
- `PORTALS SERVICE BUTTONS`: `D.S. 8 GRY-BLK 10 BEGIN TEST / ENTER: BLACK`, `D.S. 7 GRY-VIO 9 SERVICE CREDITS / RT.: GREEN`,
  `D.S. 6 GRY-BLU 8 VOLUME / LEFT: RED`; `NOT USED` beside pin 7 (`GRY-GRN`).
- `RIGHT FLIPPER BUTTON` (N.O., GRY-ORG pin 4) and `LEFT FLIPPER BUTTON` (GRY-BRN pin 2), `DEDICATED SWITCHES`.

## Button lamps

`START / TOURNIE BUTTON LAMPS`: `Lamp 80 Start`, `Lamp 79 Tournie`, wired to the I/O PWR DRVR BD. lamp matrix `J12` (pin 11) and
`J13` (YEL-VIO pin 3, YEL-GRY pin 1).

## G.I. on the coin door

`G.I. LAMPS on COIN DOOR`, `G.I. 5.7V AC`, `WHT-GRN` / `GRN`, `YEL-WHT` / `YEL`, from `J15` on the I/O PWR DRVR BD.

## UK note (boxed, printed)

`UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are used. The Left Button operates the Left Outlane Ball
Deflector. The Right Button operates the Right Outlane Ball Deflector. Both buttons pushed together operate the Center
Up/Down Post. Both buttons are located under the Flipper Buttons.` The boxed `UK ONLY` drawing wires the `LEFT BUTTON` (N.O.) on `WHT-BRN` to CN7 pin 9 and the `RIGHT BUTTON` (N.O.) on
`WHT-GRY` to CN7 pin 1, both common to `GRN-BRN` on CN5 pin 1: matrix column 1, rows 1 and 8, i.e. switches 1 and 8.
