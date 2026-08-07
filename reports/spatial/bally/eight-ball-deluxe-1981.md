# Bally Eight Ball Deluxe (1981) spatial audit

Status: **partial**. Format `pinmame-spatial-blockers`.

## Coordinate convention

- Space: `playfield`
- x: x/952; 0=left, 1=right
- y: y/1974; 0=rear/backglass, 1=apron/player
- Source bounds: {'left': 0.0, 'top': 0.0, 'right': 952.0, 'bottom': 1974.0}

## Extraction identity

- Source ref: `vpx-extraction.ebd-bord-1-0-1`
- Manifest SHA-256: `e72bfe3918dfdd1e76a4af8fb02352a60cbebb0a3036195f8541bc5ec7451946`
- Files: 977, bytes: 74250817
- vpxtool: vpxtool git:v0.33.3

## Placements: 128

- Resolved input addresses: 34
- Resolved output bindings: 90

## Not-applicable inputs

- `cabinet_or_service`: [-7, -6, -5, 6, 7, 9, 10, 11, 16]
- `dip_switch`: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

## Not-applicable outputs

- `cabinet_or_service`: [{'address': 19, 'group': 'pinmame.output.solenoid'}]
- `unused`: [{'address': 16, 'group': 'pinmame.output.solenoid'}, {'address': 17, 'group': 'pinmame.output.solenoid'}, {'address': 20, 'group': 'pinmame.output.solenoid'}]

## Excluded object classes

- Light.LED1-LED286 and Light.Light1-Light24 (backglass scoreboard/decorative render objects with no NFadeLm public-lamp binding in the retained script) -- render-only, not addressable controlled devices.
- Primitive.BulbFil1-28/BulbTop1-28 (filament/glass primitive render doubles of the l<N> Light objects) -- cosmetic doubles of an already-placed emitter, not a distinct address.

## Unresolved

- lamp.97-116 auxiliary-board SCR/connector pin identity (see blockers)
- dip.option-switch-6, dip.option-switch-7, dip.option-switch-15, dip.option-switch-29, dip.option-switch-30 function

## Blockers

- Auxiliary lamp-board addresses 97-116 are enumerated and spatially placed from the retained known-working script's own address bindings, but their individual A5J1/A5J3-to-A9J2/A9J3 SCR/connector pin assignments were not traced against the playfield wiring schematic (W-1192-28C) the way Centaur's and Kiss's auxiliary lamp boards were.
- DIP option switches 6, 7, 15, 29, and 30 have a confirmed public address and cabinet location but no resolved function; the manual's Section V.B game-adjustment tables were not exhaustively transcribed for every one of the 32 option switches.
- conflict.retained-table-year-vs-driver is recorded for transparency though this definition already resolves it (1981, matching pinned driver.c) rather than leaving the machine year itself unresolved.
- The mandatory independent high-tier cross-provider review (docs/INSTRUCTIONS.md) has not run against this exact tree.
