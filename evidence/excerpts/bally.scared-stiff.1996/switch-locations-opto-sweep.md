# Scared Stiff — Switch Locations parts list (opto pairs swept exhaustively)

Transcribed from `Scared_Stiff_OPS.pdf`, PDF pages 109-110, printed pages 2-44/2-45, the Switch
Locations parts list. Produced by rendering the retained PDF at 300-600 dpi with `pdftoppm` and
reading the table directly; this scan's text layer is garbled multi-column OCR and was never
trusted.

An item with two "Switch Part No." rows, the first described `(LED)` and the second `(Trans.)`, is a
construction disclosure of an LED-plus-phototransistor opto pair — the same fact Monster Bash's
manual states with a separate "Opto Assembly Part Number" column, just formatted differently. Every
`(LED)/(Trans.)` pair was swept explicitly:

| Addr | LED part | Trans. part | Description |
| --- | --- | --- | --- |
| 31 | A-18617-1 | A-18618-1 | Trough Eject |
| 32 | A-18617-1 | A-18618-1 | Trough Ball 1 |
| 33 | A-18617-1 | A-18618-1 | Trough Ball 2 |
| 34 | A-18617-1 | A-18618-1 | Trough Ball 3 |
| 35 | A-18617-1 | A-18618-1 | Trough Ball 4 |
| 36 | A-16908 | A-16909 | Right Popper |
| 37 | A-16908 | A-16909 | Left Kickout |
| 38 | A-16908 | A-16909 | Crate Entrance |
| 41 | A-16908 | A-16909 | Coffin Left |
| 42 | A-16908 | A-16909 | Coffin Center |
| 43 | A-16908 | A-16909 | Coffin Right |
| 44 | A-16908 | A-16909 | Left Ramp Enter |
| 45 | A-16908 | A-16909 | Right Ramp Enter |
| 46 | A-16908 | A-16909 | Left Ramp Made |
| 47 | A-16908 | A-16909 | Right Ramp Made |
| 48 | A-16908 | A-16909 | Coffin Entrance |

That is exactly the entire column-3 (31-38) and column-4 (41-48) address range — 16 opto switches by
this construction cue. Switch 12 (Wheel Index) prints a single part `D-12046` with no `(LED)/(Trans.)`
pair, but its own name and function (a rotary home-position sensor for the 200-step Spider Wheel
mechanism defined in `ss.c`) is optical construction by function, not by this manual's LED/Trans
convention; it is the 17th opto in the address space. No other row on this page carries a
`(LED)/(Trans.)` pair or an unpaired opto part: 51/52 (slingshots) print `SW-1A-114 (Kicker)` +
`SW-1A-120 (Score)` — two ordinary leaf switches ganged to one matrix address, not an opto pair;
53-55 (jets) print `SW-11A-37`; 56 prints `SW-1A-120`; 57 (Crate Sensor) prints a single part
`A-19237` with no LED/Trans pair and no further assembly page found describing its internal
construction — recorded as `switch_type: "other"` rather than asserted as opto or magnetic; 58/61-74
print ordinary `5647-12693-19` / `A-12912-23` / `A-20783-7` rollover and standup-target parts.

The printed "Opto Theory" page 1-49 explains the same LM339-comparator opto interface used elsewhere
in the manual, but carries no additional switch-specific construction data beyond what the parts-list
sweep above already establishes.

## PinMAME opto cross-check — zero disagreement

Pinned `ss.c`'s `ssGameData` inverted-switch mask is
`{0x00, 0x02, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}`, indexed by the switch
address's own tens digit (`swNo/10` in effect, i.e. column number) with the bit at
`(units digit - 1)` (row number). Decoded:

- Index 1 (column 1), bit 1 (row 2) set → address 12 (Wheel Index) is normalized.
- Index 3 (column 3) = `0xff` → all eight of 31-38 are normalized.
- Index 4 (column 4) = `0xff` → all eight of 41-48 are normalized.
- Every other index is `0x00`.

That is exactly the 17-address opto set independently swept above:
`{12, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48}`. Zero disagreement.
`conflicts` for this dimension is empty, matching Bally The Addams Family, Bally Kiss, and Williams
Star Trek: The Next Generation.
