# Williams Firepower (game 497) — Sound Board Logic Diagram, option switch DS1

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 15, printed page 15, sheet marked `497`, title block `SCHEMATIC, SOUND BOARD` /
`16D-8224`. Transcribed by hand from a 300 dpi render of the lower left quarter of the sheet.

Caption, verbatim: `Sound Board Logic Diagram`.

## Sound/speech select input

`J3` is labelled `SOUND/SPEECH SELECT INPUT`: `J3-1` `KEY`; `J3-3`, `J3-2`, `J3-5`, `J3-4`, `J3-7`,
`J3-8` each through a 100 ohm resistor (R9, R10, R7, R8, R5, R6) with a 470 pF capacitor to ground
into a `4050` buffer section of `IC5`; `J3-6` through `R3 100` / `C3 470 PFD.` into two `14069`
inverter sections of `IC7`; `J3-9` `N.C.`. Resistor pack `SR1` (`ALL 4.7 K`) pulls the lines up.

## DS1

A two-position switch block labelled `DS1`, positions `1` and `2`, marked `OFF -> ON`. One side of
both positions is tied to ground. Position 2 runs through `R2 100` (with `C2 470 PFD.` to ground)
and jumper `W9`, beside jumper `W4` from the `IC7` output; position 1 runs through `R4 100` (with
`C4 470 PFD.`). Both lines are pulled up by `SR1` and continue into the same input bus as the
`J3` sound-select lines.

The sheet gives DS1 no function name. Pinned PinMAME models two sound-board option inputs as the
`S6_COMPORTS` DIPs `Sound Dip 1` and `Sound Dip 2` (bank 0 bits 0 and 1), which `src/wpc/wmssnd.c`
folds into bits 5 and 6 of the command byte the sound CPU reads; DS1 is the only two-position
option switch drawn on this sound board.
