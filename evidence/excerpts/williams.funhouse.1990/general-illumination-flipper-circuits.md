# FunHouse — General Illumination, Flipper, and Power Circuits (printed page 3-17, "FUNHOUSE 3-17")

Source: `Funhouse_OPS.pdf`, PDF page 120, rendered at 300 dpi and read directly from the image.

## General Illumination Circuits — connectors from Power Driver Board

| Wire Color | Function | To Playfield | To Cabinet | To Insert | Transistor |
| --- | --- | --- | --- | --- | --- |
| Green | Feed 1 | J120-5 | — | J121-5 | Q12 |
| Violet | Feed 2 | J120-6 | J119-3 | J121-6 | Q10 |
| Brown | Feed 3 | J120-1 | — | J121-1 | Q18 |
| Yellow | Feed 4 | J120-3 | — | J121-3 | Q14 |
| Orange | Feed 5 | J120-2 | — | J121-2 | Q16 |
| White/Green | Return 1 | J120-10 | — | J121-10 | F7 |
| White/Violet | Return 2 | J120-11 | — | J121-11 | F6 |
| White/Brown | Return 3 | J120-7 | — | J121-7 | F10 |
| White/Yellow | Return 4 | J120-9 | — | J121-9 | F8 |
| White/Orange | Return 5 | J120-8 | — | J121-8 | F9 |

Five feeds, matching the five printed G.I. strings on `solenoid-locations.md` in the same 1-5
order (Feed N assumed to correspond to printed G.I. address N by position; this table does not
itself repeat the G.I. string names).

## Flipper Circuits — connectors from Power Driver Board

| Wire Color | Function | To Playfield |
| --- | --- | --- |
| Gray/Yellow | Left Flipper Power | J109-5 |
| Blue/Yellow | Right Flipper Power | J109-7 |
| Black/Blue | Upper Left Flipper | J109-1 |
| Blue/Gray | Lower Left Flipper | J109-3 |
| Black/Yellow | Upper Right Flipper | J109-2 |
| Blue/Violet | Lower Right Flipper | J109-4 |
| Black/Blue | Upper Left Flipper | J110-9 |
| Blue/Gray | Lower Left Flipper | J110-7 |
| Black/Yellow | Upper Right Flipper | J110-8 |
| Blue/Violet | Lower Right Flipper | J110-6 |
| Orange/Gray | Left Flipper Ground | J110-2, 1 |
| Orange/Violet | Right Flipper Ground | J110-4, 3 |

This is a generic flipper-driver-board connector template: FunHouse has exactly two flippers (per
the switch table, addresses 11/12, and the solenoid table, which lists no upper-flipper coil at
all), so the "Upper Left Flipper" / "Upper Right Flipper" rows describe unpopulated positions on a
board layout shared with other WPC titles that do have four flippers. Critically, no row on this
page carries a public solenoid address (1-50) — flipper coils on this pre-Fliptronics WPC-Alpha
generation are wired directly through this dedicated flipper driver board and the flipper
buttons/EOS switches, not through the CPU-addressable solenoid matrix; `fhGameData` in pinned
PinMAME source declares `FLIP_SWNO(12,11)` (flipper switches only) with no `FLIP_SOL()` call, so
`core_getSol` never routes anything to the standard flipper-coil addresses 33/34/35/36/45/46/47/48
for this driver. See `knowledge/williams/funhouse-1990.md`.

## Power Circuits — connectors from Power Driver Board (two printed tables on this page)

| Wire Color | Function | To Playfield | To Cabinet | To Insert |
| --- | --- | --- | --- | --- |
| Gray | Digital +5V | J117-4 | J116-4 | — |
| Gray/Green | Switch +12V | — | — | — |
| Gray/Yellow | Analog +12V | J117-2 | J116-2 | — |
| Black | Ground | J117-3 | J116-3 | — |
| Violet/Yellow | High Power 50V | J107-3 | — | — |
| Violet/Orange | Low Power 50V | J107-2 | — | — |
| Violet/Green | Other 50V | J107-1 | — | — |
| Red | Flasher 20V | J107-5 | — | — |
| Red/White | Flasher 20V | J107-6 | — | — |
| White/Blue | 50VAC | — | — | — |
| White/Blue | 50VAC | — | — | — |
| Black | Ground | — | — | J103-1 to 4 |

## Logic and Display Circuits (transcribed for completeness; cabinet/backbox only, no playfield relevance)

Logic Circuits: four ribbon-cable data connectors (`J201` extended board, `J202` sound board,
`J204` display driver, `J211`) plus `J210-1/3` ground, `J210-4/5` +5VDC, `J210-6/7` +12VDC.

Display Circuits: `J301` ribbon to Dual Display Board glass 1, `J304` ribbon to Dual Display Board
glass 2, `J305` ribbon to CPU, `J306-1` +5VDC / `J306-3` ground from CPU/Power Driver Board, and
`J307-1`/`J307-4` 100VAC from the transformer. This confirms the display hardware is a "Dual
Display Board" driving two physically separate alphanumeric glass units, matching pinned
`wpc_dispAlpha`'s two six teen-character layout groups.
