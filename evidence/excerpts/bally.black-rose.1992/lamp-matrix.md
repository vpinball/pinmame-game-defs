# Black Rose — Lamp Matrix

Transcribed from `Bally_1992_Black_Rose_Manual.pdf`, PDF page 106, printed page `BLACK ROSE 3-2`, the
`LAMP MATRIX` (column header, row header and the 8 x 8 lamp grid, with the `LAMP CIRCUIT` drawing below it). Read from the rendered page (300 dpi image-only scan), not from the OCR text.

Each cell prints its name on up to three lines at the top and its two-digit lamp number at the bottom left (column digit, then row digit); the name lines are joined here with single spaces and the printed line breaks are not otherwise preserved. Every column header prints one transistor, one wire and one connector pin (no column is printed with two connectors); every row header prints one transistor, wire and connector. Column 8 prints connector pin `J137-9` (no `J137-8` is printed) and row 3 prints `J133-4` (no `J133-3` is printed). No cell is blank. Spellings are as printed, for example `S (I) NK`, `SI (N) K`, `SIN (K)`, `(S) HIP`, `S (H) IP`, `SH (I) P`, `SHI (P)`, `Multi-ball`, `Outlane`, `Walk The Plank`. In cell 18 the word `Standup` is partly overprinted by the lamp symbol and in cell 52 the word `Middle` touches the symbol, but both read unambiguously. Nothing is illegible.

## (a) Column headers

| Column | Driver transistor | Wire | Connector pin |
| --- | --- | --- | --- |
| 1 | Q98 | Yel-Brn | J137-1 |
| 2 | Q97 | Yel-Red | J137-2 |
| 3 | Q96 | Yel-Org | J137-3 |
| 4 | Q95 | Yel-Blk | J137-4 |
| 5 | Q94 | Yel-Grn | J137-5 |
| 6 | Q93 | Yel-Blu | J137-6 |
| 7 | Q92 | Yel-Vio | J137-7 |
| 8 | Q91 | Yel-Gry | J137-9 |

## (b) Row headers

| Row | Driver transistor | Wire | Connector pin |
| --- | --- | --- | --- |
| 1 | Q90 | Red-Brn | J133-1 |
| 2 | Q89 | Red-Blk | J133-2 |
| 3 | Q88 | Red-Org | J133-4 |
| 4 | Q87 | Red-Yel | J133-5 |
| 5 | Q86 | Red-Grn | J133-6 |
| 6 | Q85 | Red-Blu | J133-7 |
| 7 | Q84 | Red-Vio | J133-8 |
| 8 | Q83 | Red-Gry | J133-9 |

## (c) Cells (Address = column digit then row digit)

| Address | Printed name |
| --- | --- |
| 11 | Special |
| 12 | Jet Enter 8K |
| 13 | Jet Enter 4K |
| 14 | Jet Enter 2K |
| 15 | Jet Enter 1K |
| 16 | Jet Enter Jewel |
| 17 | Combo Shot Right |
| 18 | Right Single Standup |
| 21 | Letter (S) INK |
| 22 | Letter S (I) NK |
| 23 | Letter SI (N) K |
| 24 | Letter SIN (K) |
| 25 | Letter (S) HIP |
| 26 | Letter S (H) IP |
| 27 | Letter SH (I) P |
| 28 | Letter SHI (P) |
| 31 | Bottom Standup Bottom |
| 32 | Bottom Standup Middle |
| 33 | Bottom Standup Top |
| 34 | Right Ramp 100K |
| 35 | Right Ramp 200K |
| 36 | Right Ramp 300K |
| 37 | Right Ramp 400K |
| 38 | Right Ramp Million |
| 41 | Middle Standup Top |
| 42 | Middle Standup Middle |
| 43 | Middle Standup Bottom |
| 44 | Left Outlane |
| 45 | Left Return Lane |
| 46 | Right Return Lane |
| 47 | Right Outlane |
| 48 | Shoot Again |
| 51 | Top Standup Bottom |
| 52 | Top Standup Middle |
| 53 | Top Standup Top |
| 54 | Lockup 1 |
| 55 | Lockup 2 |
| 56 | Lockup Jewel |
| 57 | Left Ramp Coins |
| 58 | Bottom Standup Jewel |
| 61 | Middle Ramp Jewel |
| 62 | Top Loop Jewel |
| 63 | Top Standup Jewel |
| 64 | Broadside Jewel |
| 65 | Bottom Standup Jewel |
| 66 | Right Ramp Coins |
| 67 | Sequence Shot 1 |
| 68 | Multi-ball Ready |
| 71 | Millions |
| 72 | Rigging Swing |
| 73 | Treasure Chest |
| 74 | Walk The Plank |
| 75 | Instant Multi-ball |
| 76 | Knife Throw |
| 77 | Polly |
| 78 | Insert Left |
| 81 | Skill (Open) |
| 82 | Skill (Locker) |
| 83 | Middle Ramp 200K |
| 84 | Middle Ramp 300K |
| 85 | Middle Ramp 400K |
| 86 | Jackpot |
| 87 | Insert Right |
| 88 | Credit Button |

## (d) Footnotes and circuit drawing text

The matrix itself has no footnotes. Below it is a `LAMP CIRCUIT` drawing; its printed text is:

- Left half: `COLUMN (example)`, `Power Driver Board`, `+18V`, `1.2kΩ`, `560Ω`, `TIP 107`, node labels `A` and `B`, parts `LS240`, `LS374`, `ULN-2803`, connector `J113` with `To CPU Board`, connector `J137`.
- Centre: a dashed `Playfield` box holding a bulb and a diode, labelled `Yel-xxx` (bulb side) and `Red-xxx` (diode side).
- Right half: `ROW (example)`, `Power Driver Board`, connector `J133`, `VCC`, `10KΩ`, `1.4V ref`, `LM339`, `TIP102`, `1KΩ`, `.2Ω`, `.22µf`, `74LS74` with `VCC`, node labels `C`, `D`, `E`, `F`, `G`, `Q`, `Q` (overbar on the second), `Clk`, connector `J113` with `To CPU Board`.
- Column truth table (`Column | A | B |`): `H | L | Off` and `L | H | On`.
- Row truth table (`Row | C | D | E | F | G |`, with `(normal operation)` printed beside the first value row): `H | L | H | L | H | Off` and `H | L | L | H | L | On`. The first row of values carries the label `(normal operation)`.

The circuit drawing is not otherwise transcribed.

## Comparison with the reprint on PDF page 141

PDF page 141 carries a reprint of the same `LAMP MATRIX` (above a `SWITCH MATRIX`). The scan shows no printed page number on it (no footer text; the section 4 attribution comes from the page position only). The `LAMP CIRCUIT` drawing is not reprinted. Compared cell by cell against page 106 on the rendered pages:

- All 64 cell names and lamp numbers are identical.
- All 8 column transistors, wires and connector pins are identical (including `J137-9` for column 8, no `J137-8`).
- All 8 row transistors, wires and connector pins are identical (including `J133-4` for row 3, no `J133-3`).
- The only difference is layout: on page 141 row 5's wire wraps onto two lines (`Red-Gr` over `n`), which reads `Red-Grn`, the same as page 106. Line breaks inside some cell names also differ slightly, but not the words or numbers.

No cell, wire or connector differs.

## Lamp Locations versus Lamp Matrix (PDF page 99 against this page)

Every address 11-88 appears in both tables. For almost every address the two descriptions name the same feature (differences of only `Standups`/`Standup`, a missing `Right`, the `#44`/`#555` suffix, `S I N K` versus `SIN K` spacing, or `Ramp 100K` versus `Right Ramp 100K`). The addresses where the Lamp Locations description and the Lamp Matrix name use different words for the feature, and so do not trivially denote the same lamp, are:

| Address | Lamp Locations description | Lamp Matrix name | Note |
| --- | --- | --- | --- |
| 17 | Sequence Shot 2 | Combo Shot Right | Different feature words. Address 67 reads `Sequence Shot 1` in both tables, so Locations pairs 17 with the second sequence shot while the matrix calls it a combo shot. |
| 66 | Right Ramp Jewel | Right Ramp Coins | `Jewel` versus `Coins`. Both tables call 57 `Left Ramp Coins`. |
| 68 | Multiball Release | Multi-ball Ready | `Release` versus `Ready`. |
| 81 | Skill Shot 1 | Skill (Open) | Numbered skill shot versus a parenthesized location word. |
| 82 | Skill Shot 2 | Skill (Locker) | Same. |
| 83 | Middle Ramp Left | Middle Ramp 200K | Position word versus score-value word. |
| 84 | Middle Ramp Middle | Middle Ramp 300K | Same. |
| 85 | Middle Ramp Right | Middle Ramp 400K | Same. |

These are wording differences that may or may not be the same lamp; nothing on these two pages settles it. Other differences that read as alternate names for one lamp: 44 `Left Drain` / `Left Outlane`, 47 `Right Drain` / `Right Outlane`, 54 `Lock 1` / `Lockup 1`, 55 `Lock 2` / `Lockup 2`, 18 `Single Standup` / `Right Single Standup`. Also, Lamp Locations lists a second bulb row for item 11 (`Special #555`, `C-12982`) where the matrix has the single cell `11 Special`.
