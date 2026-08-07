# The Getaway: High Speed II — General Illumination Circuits wiring page

Transcribed from `Getaway_HSII_OPS.pdf`, PDF page 127, printed page 3-22, "General Illumination
Circuits". Rendered at 300 dpi with `pdftoppm` and read directly.

Connectors From Power Driver Board:

| Wire Color | Function | To Playfield | To Cabinet | To Insert | Triac |
| --- | --- | --- | --- | --- | --- |
| Brown | Illum. String 1 | J120-1 | | | Q18 |
| Orange | Illum. String 2 | J120-2 | | | Q10 |
| Yellow | Illum. String 3 | | | J121-3 | Q14 |
| Green | Illum. String 4 | | | J121-5 | Q16 |
| Violet | Illum. String 5 | | J-119-3 | J121-6 | Q12 |
| White/Brown | Return 1 | J120-7 | | | F110 |
| White/Orange | Return 2 | J120-8 | | | F109 |
| White/Yellow | Return 3 | | | J121-9 | F108 |
| White/Green | Return 4 | | | J121-10 | F107 |
| White/Violet | Return 5 | | J119-1 | J121-11 | F106 |

Public GI addresses are zero-based (`controllers/pinmame/wpc-fliptronic.json`, "Public GI addresses
are zero-based 0-4 and correspond to the manuals' printed strings 01-05"): GI 0 = Illum. String 1, GI
1 = Illum. String 2, GI 2 = Illum. String 3, GI 3 = Illum. String 4, GI 4 = Illum. String 5.

Illum. Strings 1 and 2 (GI 0, GI 1) route exclusively `To Playfield` (J120-1/2); Strings 3 and 4 (GI
2, GI 3) route exclusively `To Insert` (J121-3/5, backbox insert panel); String 5 (GI 4) routes both
`To Cabinet` (J-119-3) and `To Insert` (J121-6) — it is the only string with a cabinet connection.
This matches the Solenoid Table page's own General Illumination block (GI 01/02 = "Playfield G.I.",
03/04/05 = "Insert G.I.") and the Solenoid/Flasher Locations page's General Illumination block (items
01/02 "Playfield #44", 03/04/05 "Insert #555") exactly, on both bulb type (playfield uses #44,
insert/backbox uses #555) and count.

The retained known-working script's `GiCallback2 = GetRef("UpdateGI")` implements only one universal
`Sub UpdateGI(no, Enabled)` that ignores its own `no` (GI address) parameter entirely and toggles the
single `GI` object collection (25 members, see `vpx-geometry.txt`) for any GI address activation, so
this recreation cannot distinguish which specific playfield bulb belongs to GI address 0 versus GI
address 1 — both are wired exclusively to the playfield per this page, but the retained table does
not model them as separate emitter sets.
