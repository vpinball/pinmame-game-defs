# Star Trek: The Next Generation — Switch Matrix

Transcribed from `Star_Trek_TNG_OPS.pdf`, PDF page 94, printed page 2-42, the SWITCH MATRIX table.
This scan carries a searchable OCR text layer, but it was visually confirmed against the rendered
page for every table here — the OCR text alone is never treated as authoritative. The accompanying
crop is the same region, rendered grayscale so the shaded opto cells stay visible.

`▦` marks a cell shaded "OPTO, TYPICALLY CLOSED" on the printed page, with the printed legend
`▦ = Opto Switch`. Dedicated grounded switches D1-D8 (left block) are the coin door / service block,
wired independently of the 8x8 matrix.

## Dedicated grounded switches

| Printed | Wire | Connector | Description |
| --- | --- | --- | --- |
| D1 | Orange-Brown | J205-1 / U18-11 | Left Coin Chute |
| D2 | Orange-Red | J205-2 / U18-9 | Center Coin Chute |
| D3 | Orange-Black | J205-3 / U18-5 | Right Coin Chute |
| D4 | Orange-Yellow | J205-4 / U18-7 | 4th Coin Chute |
| D5 | Orange-Green | J205-6 / U19-11 | Normal: Service Credits; Test: Escape |
| D6 | Orange-Blue | J205-7 / U19-9 | Normal: Volume Down; Test: Down |
| D7 | Orange-Violet | J205-8 / U19-5 | Normal: Volume Up; Test: Up |
| D8 | Orange-Gray | J205-9 / U19-7 | Normal: Begin Test; Test: Enter |

## Matrix switches (row = printed row 1-8, column = printed column 1-9)

| Addr | Description | Opto shaded |
| --- | --- | --- |
| 11 | Buy-in Button | no |
| 12 | Right Fire Button | no |
| 13 | Start Button | no |
| 14 | Plumb Bob Tilt | no |
| 15 | Left Outlane | no |
| 16 | Left Return Lane | no |
| 17 | Right Return Lane | no |
| 18 | Right Outlane | no |
| 21 | Slam Tilt | no |
| 22 | Coin Door Closed | no |
| 23 | Made Middle Ramp | no |
| 24 | Always Closed | no |
| 25 | Enter Right Ramp | no |
| 26 | Left 45° Target | no |
| 27 | Center 45° Target | no |
| 28 | Right 45° Target | no |
| 31 | Borg Lock | yes |
| 32 | Under Left Gun Sw. 2 | yes |
| 33 | Under Right Gun Sw. 2 | yes |
| 34 | Right Gun Shooter | yes |
| 35 | Under Left Lock Sw. 2 | yes |
| 36 | Under Left Gun Sw. 1 | yes |
| 37 | Under Right Gun Sw. 1 | yes |
| 38 | Left Gun Shooter | yes |
| 41 | Under Left Lock Sw. 1 | yes |
| 42 | Under Left Lock Sw. 3 | yes |
| 43 | Under Left Lock Sw. 4 | yes |
| 44 | Left Outer Loop | yes |
| 45 | Under Top Hole | yes |
| 46 | Under Left Hole | yes |
| 47 | Under Borg Hole | yes |
| 48 | Borg Entry | yes |
| 51 | Left Bank Top | no |
| 52 | Left Bank Middle | no |
| 53 | Left Bank Bottom | no |
| 54 | Right Bank Top | no |
| 55 | Right Bank Middle | no |
| 56 | Right Bank Bottom | no |
| 57 | Top Drop Target | no |
| 58 | Right Outer Loop | no |
| 61 | Trough L.R. 1 | yes |
| 62 | Trough L.R. 2 | yes |
| 63 | Trough L.R. 3 | yes |
| 64 | Trough L.R. 4 | yes |
| 65 | Trough L.R. 5 | yes |
| 66 | Trough L.R. 6 | yes |
| 67 | Trough Up | yes |
| 68 | Shooter | no |
| 71 | Left Jet | no |
| 72 | Right Jet | no |
| 73 | Bottom Jet | no |
| 74 | Right Sling | no |
| 75 | Left Sling | no |
| 76 | Top Lane Left | no |
| 77 | Top Lane Center | no |
| 78 | Top Lane Right | no |
| 81 | Time | no |
| 82 | Rift | no |
| 83 | Made Left Ramp | no |
| 84 | Q | no |
| 85 | Left 2X Shuttle | no |
| 86 | Right 2X Shuttle | no |
| 87 | Made Right Ramp | no |
| 88 | Enter Left Ramp | no |
| 91 | Not Used | no |
| 92 | Left Gun Mark | no |
| 93 | Not Used | no |
| 94 | Not Used | no |
| 95 | Right Gun Home | no |
| 96 | Right Gun Mark | no |
| 97 | Left Gun Home | no |
| 98 | Not Used | no |

## Column 9 addressing

The manual's own column header for column 9 reads "Violet-White / Q11 / J5-1" with no printed column
caption beyond the number "9". The Gun Circuit Diagram (see `gun-assembly.md`) independently labels
this same physical harness "8-driver Board J5-1 ... sw. col. 9" in its own schematic — the manual
itself calls it "column 9" throughout, printing addresses 91-98. This is not the PinMAME public
address. PinMAME's `CORE_CUSTSWCOL = CORE_STDSWCOLS = 12` places a driver's first declared custom
switch column two columns past the Fliptronic column (internal column 11), so
`sttngGameData.hw.swCol = 1` publishes at internal column 12: `CORE_CUSTSWNO(1, r) = (12-1+1)*10+r =
120+r`, i.e. public 121-128, not 91-98. `sttng.c`'s own macros carry a stale comment reflecting an
older core.h numbering (`CORE_CUSTSWNO(1,2) //92`), but the retained known-working script's own
`CannonLTimer_Timer` / `CannonRTimer_Timer` handlers assign `Controller.Switch(127)`,
`Controller.Switch(122)`, `Controller.Switch(125)`, `Controller.Switch(126)` directly — proving the
true runtime public addresses are 122/125/126/127, not 92/95/96/97. The printed "9N" numbers are
captured only as `manual.address` aliases.

## Flipper Grounded Switches column (Fliptronic, public 111-118, printed F1-F8)

| Printed | Wire | Description | Construction |
| --- | --- | --- | --- |
| F1 | Black-Green / J906-1 | Lower Right E.O.S. | leaf (SW-1A-194) |
| F2 | Blue-Violet / J905-1 | Lower Right Opto (cabinet button) | opto (A-17316) |
| F3 | Black-Blue / J906-3 | Lower Left E.O.S. | leaf (SW-1A-194) |
| F4 | Blue-Gray / J905-2 | Lower Left Opto (cabinet button) | opto (A-17316) |
| F5 | Black-Violet / J906-4 | Upper Right E.O.S. | leaf (SW-1A-194) |
| F6 | Black-Yellow / J905-3 | Upper Right Opto (cabinet button) | opto (A-17316) |
| F7 | Black-Gray / J906-5 | Spinner\* | leaf (5647-12693-11) |
| F8 | Black-Blue / J906-5 | Not Used\* | not fitted |

`*Note: Used as switches other than flipper switches in this game.` The footnote asterisk applies to
F7 and F8: F7 is printed "Spinner" on both the matrix page and the Switch Locations parts list (not
an upper-left flipper E.O.S.), and F8 is blank/Not Used on the parts list. This is the same
Fliptronic-block repurposing pattern documented for Monster Bash (F7 = Center Spinner) and Indiana
Jones (F5-F8 all repurposed) — check every WPC-DCS/Fliptronic game's block individually.
