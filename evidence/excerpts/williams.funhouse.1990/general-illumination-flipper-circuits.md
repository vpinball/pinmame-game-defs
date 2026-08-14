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
| White/Violet | Return 2 | J120-11 | J119-1 | J121-11 | F6 |
| White/Brown | Return 3 | J120-7 | — | J121-7 | F10 |
| White/Yellow | Return 4 | J120-9 | — | J121-9 | F8 |
| White/Orange | Return 5 | J120-8 | — | J121-8 | F9 |

This interboard table numbers five generic feed/return pairs but does not repeat the game-specific G.I. circuit names. The November 1990 operator handbook supplies that missing association through its named circuit table: printed 01 Upper Backglass is Brown/White-Brown through Q18/F10; 02 Front Playfield is Violet/White-Violet through Q10/F6; 03 Rear Playfield is Yellow/White-Yellow through Q14/F8; 04 Center Backglass / Right Rear Playfield is Orange/White-Orange through Q16/F9; and 05 Top Playfield is Green/White-Green through Q12/F7. Generic feed number is therefore not the printed FunHouse circuit number. The handbook's `J119-1` connector for circuit 02 agrees with the White/Violet Return 2 cabinet branch on this page; its earlier omission from this transcription was a transcription error.

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

The handbook's coil inventory identifies three fitted physical flipper assemblies: lower right FL-11630, lower left FL-11630, and upper left FL-11753. The upper-right connector position in this generic flipper-driver-board table is unfitted on FunHouse. Critically, no row on this page carries a public solenoid address (1-50): flipper coils on this pre-Fliptronics WPC-Alpha generation are wired directly through the dedicated flipper driver board and the cabinet buttons/EOS switches, not through the CPU-addressable solenoid matrix. `fhGameData` in pinned PinMAME declares `FLIP_SWNO(12,11)` with no `FLIP_SOL()` call, so `core_getSol` never routes a physical flipper coil to public outputs 33-36 or 45-48. The retained script independently confirms the three-bat layout because its left callback rotates both `LeftFlipper` and `LeftFlipper1`, while the right callback rotates one right bat. See `knowledge/williams/funhouse-1990.md`.

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
