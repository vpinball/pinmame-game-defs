# Theatre of Magic — Switch Locations (parts list)

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 119, printed page 2-43, the Switch Locations
parts list. The retained PDF carries a Paper Capture OCR text layer, but per project policy every
table was verified against a 300 dpi render of the page regardless of the text layer's presence.

## Manual self-contradiction, resolved by the parts list

The Switch Matrix page (2-42, see `switch-matrix.md`) labels the rightmost column's F5-F8 rows
"Upper Right/Left Flipper EOS/Opto" with real-sounding descriptions, but this Switch Locations parts
list (2-43) prints F5, F6, F7, F8 as `Not Used` with no switch part number, alongside 11, 12, 16, 17,
18 (`Not Used`, printed as a block). The parts list is preferred per project policy ("prefer the
parts list over the matrix page for labels"); this matches `tomGameData.hw.flippers =
FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`, which declares no upper flipper switch or solenoid bit at all.
The matrix page's F5-F8 text is stale generic Fliptronic-II-board template wording, not a description
of fitted hardware.

## Part numbers

F1/F3 `SW-1A-194` (EOS leaf), F2/F4 `A-17316` (button opto, "*Lower Right/Left Flipper Cabinet"); 13
`20-9663-1` (Start Button); 14 `A-15361` (*Plumb Bob Tilt); 15 `5647-12693-32` (Shooter Lane); 21
`A-17238` (*Slam Tilt); 22 `5643-09288-00` (*Coin Door Closed); 23 `20-9663-18` (Buy-In); 24
`5643-09112-00` (*Always Closed); 25-28 `5647-12693-19` (Left/Right Outlane/Return Lane); 31-35
two-line `A-18617-1`(LED)/`A-18618-1`(Trans) opto pairs (Trough Jam, Trough 1-4); 36
`A-16908`(LED)/`A-16909`(Trans) opto pair (Subway Opto); 37 `5647-12693-24` (Spinner, not an opto
part); 38 `A-17799-6` (Right Lower Target); 41-43 `5647-12693-3x` (Lock 1-3); 44 `5647-12693-11`
(Popper); 45 `A-18543-1` (Left Drain Eddy); 46 Not Used; 47 `5647-12693-13` (Subway Micro); 48
`A-18543-1` (Right Drain Eddy); 51 `A-18059-15` (Left Bank Target (2)); 52-54 `5647-12693-19`
(Captive Ball Rest, Right/Left Lane Enter); 55-58 `A-19749` (Cube Position 4/1/2/3); 61-62
`SW-1A-114`(kicker)/`SW-1A-120`(score) (Left/Right Sling); 63-65 `SW-11A-37` (Bottom/Middle/Top Jet);
66-67 `5647-12693-19` (Top Lane 1-2); 68 Not Used; 71 `5647-12693-13` (Center Ramp Exit); 72 Not
Used; 73-74 `5647-12693-13` (Right Ramp Exit 1-2); 75-76 `5647-12693-11` (Center/Right Ramp Enter);
77-78 `5647-12693-19` (Captive Ball Top, Loop Left); 81 `5647-12693-19` (Loop Right); 82 `A-20014-5`
(Center Ramp Targets (2)); 83-84 `5647-12133-1x` (Vanish Lock 1-2); 85 `A-18543-2` (Trunk Hit); 86-87
`5647-12693-1x` (Right/Left Lane Exit); 88 Not Used.

## Cube Position optos (55-58)

No LED/Trans split is printed for these four positions, but all four are shaded "OPTO, TYPICALLY
CLOSED" on the matrix page and the Magic Trunk teardown diagram (see `eddy-and-trunk-teardown.md`)
labels the same sensor assembly "Opto Board" / "Opto Interrupter" — shading plus the teardown diagram
are the basis for treating 55-58 as opto.
