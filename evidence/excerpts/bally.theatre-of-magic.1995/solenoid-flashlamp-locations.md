# Theatre of Magic — Solenoid/Flashlamp Locations (parts list)

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF pages 120-121, printed pages 2-44/2-45, the
Solenoid/Flashlamp Locations parts list. The retained PDF carries a Paper Capture OCR text layer, but
per project policy every table was verified against a 300 dpi render of the page regardless of the
text layer's presence.

Confirms every part number in the printed Solenoid/Flasher Table (see `solenoid-flasher-wiring.md`)
with an associated assembly number and a playfield location circle (or `*Not Shown` for
cabinet/backbox devices — Knocker (07), Return Lane Flasher assemblies, etc.). Notable multi-line
entries: 24 Trap Door Flasher combines assemblies `A-17983`/`A-17803`; 25 Spirit Ring Flasher
`A-17983`; 26 Saw Flasher `A-17903`; 27 Jet Flasher `A-17803`; 28 Box Flasher `A-17983`/`A-17803`.
Flipper Coils: `FL-11629` (blue) `A-15849-R-2` Lower Right Flipper, `A-15849-L-2` Lower Left Flipper.

## Item 23 self-contradiction

Unlike the Solenoid/Flasher Table (which marks item 23 `NOT USED`, with dashes only for the part
number while the voltage/drive connections through Q34/J126-7 remain populated — a wired but
unpopulated position per the "blank voltage AND blank drive connections" test), this Locations page
assigns item 23 a real bulb and assembly: `24-8704` (#89) / `A-17803`, "Save Post Flasher". The
retained known-working script resolves this by implementing `SolCallback(23)` only when a
table-author toggle `CenterPost` is enabled (`CenterPost = 0 'default off`, comment "Magic Post
Flasher (\*\*\*)"), and the same toggle also gates solenoid 36 (`SolCallback(36) = "SolMagicPost"`,
"Magic Post Up/Down (\*\*\*)"). Since the toggle defaults off in the retained table and the
Solenoid/Flasher Table's own printed fitment (dashes) agrees, this definition treats solenoids 23 and
36 as `unused` on the production machine and documents the disagreement in `conflicts`.
