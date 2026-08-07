# Tales of the Arabian Nights — General Illumination

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, PDF page 122, printed page
2-40, the General Illumination table printed on the same page as the Solenoid/Flasher Table (see
`solenoid-flasher-wiring.md`). The retained PDF carries a genuine OCR text layer, but the layout
extraction badly garbles multi-column tables, so this was re-verified against the 300 dpi rendered
page image, which is the source of record.

| GI printed | Description | PF conn. | BB conn. | Cab conn. | Xistor | Bulb |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Illumination String 1 | — | J106-1/J106-7 | — | Q5 | #44 |
| 02 | Illumination String 2 | — | J106-2/J106-8 | — | Q4 | #44 |
| 03 | Illumination String 3 | — | J106-3/J106-9 | — | Q3 | #44 |
| 04\* | Illumination String 4 | J105-5/J105-10 | — | — | Q2 | #555 |
| 05\* | Illumination String 5 | J105-6/J105-11 | — | J104-3/J104-1 | Q1 | #555 |

`*` These G.I. strings do not brighten and dim, they are always on (asterisk scoped to strings 4 and
5 only, matching every other Williams manual's footnote-scoping pattern). Strings 1-3 (public GI 0-2)
are wired to the backbox insert panel only (#44 bulbs, `J106` connectors, no `Playfield` column
entry); strings 4-5 (public GI 3-4) are wired to the playfield (#555 bulbs, `J105` connectors), with
string 5 additionally feeding a cabinet connection (`J104`).

**Conflict with the retained script.** The retained known-working script's `Sub UpdateGI(no, step)`
only implements `Case 2` (public GI address 2 = printed String 3), driving a playfield-wide dimming
value, and has no case at all for GI addresses 0, 1, 3 or 4. This directly conflicts with the wiring
table above, which documents GI address 2 (String 3) as backbox-only while the genuinely
playfield-wired strings are addresses 3 and 4 (Strings 4-5). Recorded as
`conflict.gi-string-3-playfield-binding`; no playfield coordinate is attributed to GI address 2 per
this manual, and GI addresses 3/4 have no validated placement because no VPX object binds
specifically to them.
