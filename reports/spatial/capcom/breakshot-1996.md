# Breakshot (Capcom, 1996) spatial review

Status: partial. The physical machine record is `partial` at `machines/partial/capcom/breakshot-1996.json`, and `spatial_placement` is its only missing requirement: every address carries a validated placement or a controlled `not_applicable` record and the record has no conflicts, but seven fixed G.I. sockets have only the lamp drawing's position.

## Blockers

- Seven of the 54 fixed G.I. sockets the lamp location drawing P62400 (PDF 74) marks have no checked position: 67A, 67B and 67F across the top arch, 68B at the top right and 68K on the right side, for which the retained table models no light, and 65A and 65B, printed just inside the playfield outline's front edge beside the start button on no drawn part, so what they light, the apron perhaps, is not established. Each keeps its disc's position through the drawing's control fit, observed only, so the uncontrolled lighting of the playfield is not fully placed. Resolution path: a recreation that models these sockets, or a drawing that locates them, checked against a photograph of a Breakshot playfield showing them, with the apron removed for 65A and 65B, which any owner can take.

Promotion decision: partial: seven fixed G.I. sockets have only the lamp drawing's position. Otherwise every switch, coil, lamp and display address carries a validated placement or a controlled not-applicable record, every placement the factory drawings mark agrees with its callout, the other 47 G.I. sockets sit on the table light their own disc checks, and the definition carries no conflict.

The coordinate source is the retained known-working `Breakshot (Capcom 1996) VPW v1.1.vpx` at SHA-256 `5b038fc3411647d405e43b0f56802e61067479a2ace702a5b3aca97835961932`, whose embedded script (SHA-256 `4d231b5737073c4df944b495a7c9bfe3b175ff42420872edf437099f538a7178`) binds each switch, coil and lamp to a table object. Playfield bounds are `left=0 top=0 right=952 bottom=2162`; every coordinate is x/952 and y/2162 at no more than six decimals.

## Evidence decisions

- The retained script decides which table object stands for an address, except where the ROM proves the table wrong: its slingshots (41/42), its three star bumpers (57-59) and its right drop bank (48-51 against the ROM's 49-52) report other addresses than the machine, so those placements follow the ROM's names and the manual's drawings, not the table's switch numbers.
- The factory location drawings P62500, P62600 and P62400 check the placements: 120 of the 120 checked placements land within 0.07 normalized of their own disc under both the control fit and the leave-one-out callout fit (`tools/drawing_callouts.py`, seed `tools/seeds/capcom/breakshot-1996-callouts.json`). The drawings print every number in a disc without a leader, so each read is recorded as a label beside its part.
- The switch drawing numbers the right drop bank one lower than its own table, the ROM and the harness, so the bank's placements are checked against discs 48-51.
- The solenoid drawing's disc 16 sits beside the left top gate's coil bracket; its read takes the bracket.
- The lamp drawing prints no 27: the right top-lane insert, its only unlabelled lamp insert, is read as 27.
- The trough (35-38) and its two coils (S1, S2) lie under the apron, where the drawings print their numbers in open space without a part. They are documented projections onto the script's trough objects, excluded from the check.
- Lamp 11 has two bulbs under one Jackpot insert (the lamp matrix sheet's `(23) Jackpot (two)`). Its first placement is checked against disc 11; the second is a documented projection onto the first, excluded from the check.
- The 54 fixed G.I. sockets (65A-68Q) have no PinMAME output, so the definition has no device to carry them; `uncontrolled_lighting` places them. 47 take the centre of the retained table's G.I. light that their own disc on the lamp drawing checks, and 7 that the table does not model keep the drawing's position, observed only, which is the record's blocker. See the fixed general illumination section below.
- Cabinet and backbox devices (coin switches, flipper and start buttons, slam and tilt, the knocker, the start lamp, the diagnostic LEDs and the DMD) carry controlled `cabinet_or_service` records.

## Explicit projections

- pinmame.input.switch 35: Under the apron, where the switch drawing prints 35 and the opto circles 36-38 without leaders in open space below the apron's edge (35 at the centre, then 38, 37 and 36 rising towards the shooter lane) and draws no part, so the drawing confirms the order but checks no coordinate. The placement is the known-working script's trough object for this position (it creates the three balls in sw38, sw37 and sw36, kicks the outhole ball from sw35 and serves from sw36), which spaces the trough about twice as widely as the drawing's circles; a documented projection.
- pinmame.input.switch 36: Under the apron, where the switch drawing prints 35 and the opto circles 36-38 without leaders in open space below the apron's edge (35 at the centre, then 38, 37 and 36 rising towards the shooter lane) and draws no part, so the drawing confirms the order but checks no coordinate. The placement is the known-working script's trough object for this position (it creates the three balls in sw38, sw37 and sw36, kicks the outhole ball from sw35 and serves from sw36), which spaces the trough about twice as widely as the drawing's circles; a documented projection.
- pinmame.input.switch 37: Under the apron, where the switch drawing prints 35 and the opto circles 36-38 without leaders in open space below the apron's edge (35 at the centre, then 38, 37 and 36 rising towards the shooter lane) and draws no part, so the drawing confirms the order but checks no coordinate. The placement is the known-working script's trough object for this position (it creates the three balls in sw38, sw37 and sw36, kicks the outhole ball from sw35 and serves from sw36), which spaces the trough about twice as widely as the drawing's circles; a documented projection.
- pinmame.input.switch 38: Under the apron, where the switch drawing prints 35 and the opto circles 36-38 without leaders in open space below the apron's edge (35 at the centre, then 38, 37 and 36 rising towards the shooter lane) and draws no part, so the drawing confirms the order but checks no coordinate. The placement is the known-working script's trough object for this position (it creates the three balls in sw38, sw37 and sw36, kicks the outhole ball from sw35 and serves from sw36), which spaces the trough about twice as widely as the drawing's circles; a documented projection.
- pinmame.output.solenoid 1: Under the apron: the solenoid drawing prints disc 1 below the flippers at the outhole, in open space below the apron's edge with no leader and no part drawn, so it checks no coordinate. The placement is the outhole kicker sw35 that the known-working script kicks on S1; a documented projection, like the trough switches.
- pinmame.output.solenoid 2: Under the apron: the solenoid drawing prints disc 2 towards the lower right at the trough, in open space below the apron's edge with no leader and no part drawn, so it checks no coordinate. The placement is trough position 1, kicker sw36, which the known-working script ejects into the shooter lane on S2; a documented projection, like the trough switches.
- pinmame.output.lamp 11: The second of the Jackpot's two bulbs (the lamp matrix sheet's '(23) Jackpot (two)'), placement lamp.matrix-11.emitter.2. Both bulbs sit under the one Jackpot insert, which the lamp drawing marks with a single disc 11 that checks the first placement, the centre of light l11; no source shows where the bulbs sit under the insert, so the second is projected onto the first and excluded from the callout check.

## Counts

- Placements: 127 (127 validated)
- Located input addresses: 41
- Located output bindings: 84
- Inputs with a controlled `cabinet_or_service` record: 11
- Inputs with a controlled `unused` record: 20
- Inputs with a controlled `virtual` record: 24
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `unused` record: 10
- Outputs with a controlled `virtual` record: 25

## Drawing callout check

- pdf-74 (Capcom_1996_Breakshot_Manual.pdf PDF 74, printed 70: Cabinet, Backbox, & Playfield Lamps drawing P62400): 9 controls, control RMS 0.0021, 62 callout pairs, worst leave-one-out offset 0.014
- pdf-82 (Capcom_1996_Breakshot_Manual.pdf PDF 82, printed 78: Playfield & Cabinet Switches & Optos drawing P62500): 7 controls, control RMS 0.0016, 37 callout pairs, worst leave-one-out offset 0.0387
- pdf-84 (Capcom_1996_Breakshot_Manual.pdf PDF 84, printed 80: Playfield and Backbox Solenoids and Flashers drawing P62600): 9 controls, control RMS 0.0035, 21 callout pairs, worst leave-one-out offset 0.0441

## Fixed general illumination

The lamp table (PDF 75): 54 #44 G.I. bulbs (LP00104) on strings 65 (ORG/WHT, 14), 66 (BLU/WHT, 13), 67 (GRN/WHT, 12) and 68 (BLK/WHT, 15), lettered without I and O, and the backbox fluorescent 69. The lamp drawing (PDF 74) marks each socket with its string and letter, so string membership is the machine's own, not the table's grouping. Each socket's disc on pdf-74 pairs one-to-one, nearest first under the control fit, with a light of the retained table's GI collection. The socket takes the light's centre (status validated) when the disc lands within 0.07 normalized of it under both the control fit and the callout fit; otherwise it keeps the disc's position through the control fit at three decimals (status observed). A disc is printed on or beside its socket and is about 0.05 of the playfield width across. The table's GI collection has 47 distinct lights (render double: gi014 = gi011); every one is paired. The backbox fluorescent 69 carries a `cabinet_or_service` disposition.

| Socket | Wire | x | y | Status | Coordinate source | Control offset | Callout offset |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| 65A | ORG/WHT | 0.218 | 0.987 | observed | lamp drawing pdf-74, control fit | - | - |
| 65B | ORG/WHT | 0.278 | 0.987 | observed | lamp drawing pdf-74, control fit | - | - |
| 65C | ORG/WHT | 0.719227 | 0.731173 | validated | Light.gi04 | 0.0075 | 0.006 |
| 65D | ORG/WHT | 0.681409 | 0.775839 | validated | Light.gi03 | 0.0054 | 0.0032 |
| 65E | ORG/WHT | 0.749976 | 0.811944 | validated | Light.gi02 | 0.0026 | 0.003 |
| 65F | ORG/WHT | 0.68459 | 0.83202 | validated | Light.gi01 | 0.0016 | 0.0049 |
| 65G | ORG/WHT | 0.222659 | 0.832005 | validated | Light.gi05 | 0.0023 | 0.0037 |
| 65H | ORG/WHT | 0.156754 | 0.811838 | validated | Light.gi06 | 0.0018 | 0.0037 |
| 65J | ORG/WHT | 0.225452 | 0.776547 | validated | Light.gi07 | 0.0037 | 0.0033 |
| 65K | ORG/WHT | 0.18831 | 0.731663 | validated | Light.gi08 | 0.0038 | 0.0045 |
| 65L | ORG/WHT | 0.045357 | 0.640573 | validated | Light.gi001 | 0.0015 | 0.0028 |
| 65M | ORG/WHT | 0.046325 | 0.606177 | validated | Light.gi002 | 0.0013 | 0.0039 |
| 65N | ORG/WHT | 0.045034 | 0.578318 | validated | Light.gi003 | 0.0014 | 0.0013 |
| 65P | ORG/WHT | 0.042129 | 0.549037 | validated | Light.gi004 | 0.0026 | 0.0046 |
| 66A | BLU/WHT | 0.045679 | 0.457784 | validated | Light.gi005 | 0.0014 | 0.0031 |
| 66B | BLU/WHT | 0.072795 | 0.426514 | validated | Light.gi006 | 0.0007 | 0.0026 |
| 66C | BLU/WHT | 0.062788 | 0.389273 | validated | Light.gi007 | 0.0023 | 0.0006 |
| 66D | BLU/WHT | 0.076345 | 0.353739 | validated | Light.gi008 | 0.0007 | 0.0027 |
| 66E | BLU/WHT | 0.039869 | 0.272008 | validated | Light.gi009 | 0.0021 | 0.0048 |
| 66F | BLU/WHT | 0.04116 | 0.134987 | validated | Light.gi010 | 0.002 | 0.0028 |
| 66G | BLU/WHT | 0.050844 | 0.102863 | validated | Light.gi011 | 0.003 | 0.0037 |
| 66H | BLU/WHT | 0.085384 | 0.079979 | validated | Light.gi012 | 0.0058 | 0.0069 |
| 66J | BLU/WHT | 0.151773 | 0.03267 | validated | Light.gi048 | 0.0034 | 0.0068 |
| 66K | BLU/WHT | 0.337517 | 0.373536 | validated | Light.gi043 | 0.0035 | 0.0037 |
| 66L | BLU/WHT | 0.307068 | 0.345846 | validated | Light.gi044 | 0.0566 | 0.0562 |
| 66M | BLU/WHT | 0.569371 | 0.373206 | validated | Light.gi046 | 0.0029 | 0.0038 |
| 66N | BLU/WHT | 0.599293 | 0.346424 | validated | Light.gi045 | 0.0565 | 0.0551 |
| 67A | GRN/WHT | 0.211 | 0.032 | observed | lamp drawing pdf-74, control fit | - | - |
| 67B | GRN/WHT | 0.285 | 0.023 | observed | lamp drawing pdf-74, control fit | - | - |
| 67C | GRN/WHT | 0.361001 | 0.016396 | validated | Light.gi022 | 0.0069 | 0.0076 |
| 67D | GRN/WHT | 0.471435 | 0.017461 | validated | Light.gi023 | 0.0042 | 0.0062 |
| 67E | GRN/WHT | 0.558492 | 0.017816 | validated | Light.gi024 | 0.005 | 0.0032 |
| 67F | GRN/WHT | 0.63 | 0.022 | observed | lamp drawing pdf-74, control fit | - | - |
| 67G | GRN/WHT | 0.211139 | 0.136301 | validated | Light.gi013 | 0.0042 | 0.0049 |
| 67H | GRN/WHT | 0.254243 | 0.131809 | validated | Light.gi015 | 0.0096 | 0.0094 |
| 67J | GRN/WHT | 0.253064 | 0.205888 | validated | Light.gi047 | 0.0023 | 0.0028 |
| 67K | GRN/WHT | 0.291225 | 0.100363 | validated | Light.gi12 | 0.002 | 0.0025 |
| 67L | GRN/WHT | 0.398687 | 0.100163 | validated | Light.gi11 | 0.0033 | 0.0045 |
| 67M | GRN/WHT | 0.506602 | 0.100163 | validated | Light.gi10 | 0.0035 | 0.0047 |
| 68A | BLK/WHT | 0.801125 | 0.026689 | validated | Light.gi025 | 0.0046 | 0.0097 |
| 68B | BLK/WHT | 0.755 | 0.039 | observed | lamp drawing pdf-74, control fit | - | - |
| 68C | BLK/WHT | 0.88197 | 0.05177 | validated | Light.gi026 | 0.0031 | 0.0038 |
| 68D | BLK/WHT | 0.656835 | 0.080996 | validated | Light.gi021 | 0.0026 | 0.0024 |
| 68E | BLK/WHT | 0.613609 | 0.099964 | validated | Light.gi09 | 0.006 | 0.0038 |
| 68F | BLK/WHT | 0.634013 | 0.141093 | validated | Light.gi020 | 0.0023 | 0.002 |
| 68G | BLK/WHT | 0.778516 | 0.147564 | validated | Light.gi13 | 0.0079 | 0.003 |
| 68H | BLK/WHT | 0.939216 | 0.367124 | validated | Light.gi028 | 0.0136 | 0.0087 |
| 68J | BLK/WHT | 0.9315 | 0.39401 | validated | Light.gi029 | 0.0297 | 0.0248 |
| 68K | BLK/WHT | 0.889 | 0.443 | observed | lamp drawing pdf-74, control fit | - | - |
| 68L | BLK/WHT | 0.791936 | 0.460388 | validated | Light.gi031 | 0.0051 | 0.0087 |
| 68M | BLK/WHT | 0.880506 | 0.456449 | validated | Light.gi030 | 0.0105 | 0.0129 |
| 68N | BLK/WHT | 0.850088 | 0.576601 | validated | Light.gi032 | 0.0042 | 0.0086 |
| 68P | BLK/WHT | 0.831301 | 0.602208 | validated | Light.gi033 | 0.003 | 0.0062 |
| 68Q | BLK/WHT | 0.867981 | 0.619936 | validated | Light.gi034 | 0.0033 | 0.008 |

- 65A: Printed just inside the outline's front edge beside disc 1 (the start button), where the drawing shows no part and the table models no light, so what the bulb lights there, such as the apron, is not established.
- 65B: Printed just inside the outline's front edge beside disc 1 (the start button), where the drawing shows no part and the table models no light, so what the bulb lights there, such as the apron, is not established.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/capcom/breakshot-1996/extracted-vpxtool.manifest.json`, SHA-256 `0315f2b749cf9446af5a88a649417dc7e8935820629147627286f0d988778318`, 1586 files, 436686215 bytes.
- Table archive SHA-256 `ea49fea1ad86eaba1d712f1231f9d2c76c4af80624efc2cad53f99c9da95ec09` from VPUniverse file 20471.
- Callout reads and the seed generator under `external:pinmame-review-artifacts/breakshot-1996/callout-check`, manifest SHA-256 `b0674ebddd2b89d9b86e2554590ab6f256e410f3f45b52ad67f012f64033c1fc`.
