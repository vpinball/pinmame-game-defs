# Theatre of Magic — General Illumination rows of the Solenoid/Flasher Table

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 2 (the unnumbered front-matter copy of the
Solenoid/Flasher Table), General Illumination block directly below the solenoid rows. The same block
is printed identically on printed page 2-44 (PDF page 120) and printed page 3-5 (PDF page 127). The committed crop shows only the
five G.I. rows; the column headers are in the crop of `solenoid-flasher-wiring.md`. Verified against
a native-resolution render of the page, not the OCR text layer.

Column headers, as printed at the top of the table: `Voltage Connections` (sub-columns `Playfield`,
`Backbox`, `Cabinet`), `Drive Xister`, `Drive Connections` (sub-columns `Playfield`, `Backbox`,
`Cabinet`), `Drive Wire Color`, `Solenoid Part number / Flashlamp Type` (sub-columns `Playfield`,
`Backbox`). Blank cells are printed blank.

| No. | Function | Type | Volt. Playfield | Volt. Backbox | Volt. Cabinet | Xister | Drive Playfield | Drive Backbox | Drive Cabinet | Wire | Lamp Playfield | Lamp Backbox |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | STRING 1 | G.I. | (blank) | J120-1 | (blank) | Q18 | (blank) | J120-7 | (blank) | Wht-Brn | (blank) | #555 |
| 02 | STRING 2 | G.I. | (blank) | J120-2 | (blank) | Q10 | (blank) | J120-8 | (blank) | Wht-Org | (blank) | #555 |
| 03 | STRING 3 | G.I. | J121-3 | (blank) | (blank) | Q14 | J121-9 | (blank) | (blank) | Wht-Yel | #44 | (blank) |
| 04 | STRING 4 | G.I. | J121-5 | (blank) | (blank) | Q16 | J121-10 | (blank) | (blank) | Wht-Grn | #44 | (blank) |
| 05 | STRING 5 | G.I. | J121-6 | (blank) | (blank) | Q12 | J121-11 | (blank) | (blank) | Wht-Vio | #44 | (blank) |

Footnote on the page: `J1xx=Power Driver Board; J9xx=Fliptronic II Board; 24-6549=#44 bulb;
24-8704=#89 bulb; 24-8768=#555 bulb; 24-8802=#906 bulb`.

## These rows are printed under the wrong location columns

The game's own Power Driver Board connector list (printed 3-27, PDF page 149; see
`power-driver-gi-connectors-j119-j120.md` and `power-driver-gi-connectors-j121.md`) reads every one
of these pins the other way round: J120-1/-2/-7/-8 go "to playfield" and J121-3/-5/-6/-9/-10/-11 go
"to insert". The same list agrees with this table's Playfield and Backbox columns on every flashlamp
row (J122 "to playfield flashlamps", J124 "to insert flashlamp"), so its playfield/insert vocabulary
is not in doubt and only the five G.I. rows are misprinted. The bulbs move with the connectors: #555
(24-8768, a wedge-base bulb) is the playfield string bulb, the same part the Jet Bumper Assembly
fits (printed 2-20, `jet-bumper-assembly.md`). That #44 (24-6549) is the insert-board bulb is an
inference from the connector list; no insert-board parts page is retained, and 24-6549 appears only
in the table legends.

The table also prints each string's return pin (J120-1 "Brown Return G.I." on the connector list)
under Voltage Connections and its 6.8VAC supply pin (J120-7 "White-Brown 6.8VAC") under Drive
Connections. The printed G.I. circuit (printed 3-10, PDF page 132) puts the triac on the return side.
The definition therefore records the return pin as each string's control connection and the 6.8VAC
pin as its power connection.

The retained known-working script's `UpdateGI` (lines 1658-1716) dims playfield Light collections for
cases 0-3. Cases 0 and 1 are the two real playfield strings. Cases 2 and 3 are insert strings 03 and
04; the manual controls their physical classification and the script their runtime binding, so the
disagreement is recorded as `conflict.gi-strings-3-4-insert-vs-script-playfield-binding`. It has no
case 4.
