# Theatre of Magic — General Illumination

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 2 (continuation), the General Illumination
table printed directly below the Solenoid/Flasher Table (see `solenoid-flasher-wiring.md`). The
retained PDF carries a Paper Capture OCR text layer, but per project policy every table was verified
against a 300 dpi render of the page regardless of the text layer's presence.

| No. | String | Volt. conn. | Xister | Drive conn. | Wire | Bulb |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | String 1 | Backbox J120-1 | Q18 | Backbox J120-7 | Wht-Brn | #555 (backbox) |
| 02 | String 2 | Backbox J120-2 | Q10 | Backbox J120-8 | Wht-Org | #555 (backbox) |
| 03 | String 3 | Playfield J121-3 | Q14 | Playfield J121-9 | Wht-Yel | #44 (playfield) |
| 04 | String 4 | Playfield J121-5 | Q16 | Playfield J121-10 | Wht-Grn | #44 (playfield) |
| 05 | String 5 | Playfield J121-6 | Q12 | Playfield J121-11 | Wht-Vio | #44 (playfield) |

Strings 1-2 are wired exclusively through Backbox-column connectors with `#555` bulbs; strings 3-5
are wired exclusively through Playfield-column connectors with `#44` bulbs. `J1XX = Power Driver
Board; J9XX = Fliptronic II Board`.

**Conflict with the retained script.** The retained known-working script's `UpdateGI` (lines
1658-1716) implements only cases 0-3 ("top", "bottom left", "bottom right", "middle"), each driving a
genuine playfield `Light` collection plus a colour-grade LUT swap. This contradicts the wiring table
above, which wires GI strings 1 and 2 (PinMAME addresses 0 and 1) through Backbox connectors (J120)
with `#555` bulbs and only strings 3-5 (addresses 2-4) through Playfield connectors (J121) with `#44`
bulbs — recorded as a conflict in the generated definition. No case 4 exists in the script, so GI
address 4 (String 5) has no VPX object binding despite being playfield-wired per the manual.
