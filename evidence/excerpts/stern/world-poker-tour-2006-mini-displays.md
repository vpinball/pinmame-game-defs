# World Poker Tour fourteen playfield card displays

Visually checked by GPT-6-Sol on 2026-09-30 against the retained factory PDF renders and both extracted VPX scripts. The source PDF is `World_Poker_Tour_Manual.pdf` SHA-256 `4cf31702805e75d37aef1c0c1624426000fec6cabf71a47e27691f5d5f8b6d01`; external table `wpt 062018a.vpx` SHA-256 `baa4e6e2ec618ed667afc397dea2ee6cdc5c444f811395b42dd537cfec98c443`, `vpxtool git:v0.33.3` extraction manifest SHA-256 `e15aefc9e7a736528882c6e6b89cf051103d4edbbcf73f7ce7c0a21d9c7dccfd`. Stern owns the manual; the VPX table belongs to its authors; redistribution rights are NOASSERTION. This excerpt records derived factual mapping only.

The manual's PDF page 7 / printed DR.5 switch-location drawing depicts fourteen card-display blocks in two rows of seven above the apron. PDF pages 166–167 / printed Sec.5 Ch.4 pp.140–141 identify their `14-Block LED PCB (520-5250-14)` and its fourteen LED units. Pinned `src/wpc/sam.c` lines 923–1009 multiplex two rows of seven blocks with ten row strobes and a 49-bit column chain; lines 2361–2378 place the fourteen 5×7 mini raster callbacks after the main DMD. WPT `INITGAME` at line 2448 selects this layout. `CORE_NODISP` controls emulator rendering and does not relocate the physical board.

The retained 2018 VPX script lines 1318–1389 maps `LED(0..69)` to seven pixel objects each, `D1..D490`. Five consecutive legacy segment groups form each 5×7 block. In the native compatibility path, `dmd_x=(layout->left-10)/7`, `dmd_y=(layout->top-34)/9`, and `drawSeg[35*dmd_y+5*dmd_x+4-x]` in `sam.c` lines 994–1000 map callback index 1–7 to the first seven groups of five and 8–14 to the next seven. The reversed `4-x` order changes columns within a block, not block order. Every group of 35 exact `Light.Dn.json#/Light/center` objects forms a rectangular five-column, seven-row pixel grid. The fourth pixel in its middle segment group, `D(18+35*i)`, is the stored central pixel of that block. The same table's `wptpf.png` image shows the two rows of card displays in this physical playfield region. These are exact central-pixel centres, not centroids, bulb locations, or segment transport positions.

| Native callback index | Legacy groups | Central pixel | Raw VPU x,y | Normalized x,y |
| ---: | --- | --- | --- | --- |
| 1 | 0–4 | D18 | 243.25, 1298.7798 | 0.255515, 0.577235 |
| 2 | 5–9 | D53 | 303.75, 1298.7798 | 0.319065, 0.577235 |
| 3 | 10–14 | D88 | 366.75, 1298.7798 | 0.385242, 0.577235 |
| 4 | 15–19 | D123 | 429.25, 1298.7798 | 0.450893, 0.577235 |
| 5 | 20–24 | D158 | 489.75, 1298.7798 | 0.514443, 0.577235 |
| 6 | 25–29 | D193 | 551.75, 1298.7798 | 0.579569, 0.577235 |
| 7 | 30–34 | D228 | 614.25, 1298.7798 | 0.645221, 0.577235 |
| 8 | 35–39 | D263 | 243.25, 1378.7798 | 0.255515, 0.612791 |
| 9 | 40–44 | D298 | 303.75, 1378.7798 | 0.319065, 0.612791 |
| 10 | 45–49 | D333 | 366.75, 1378.7798 | 0.385242, 0.612791 |
| 11 | 50–54 | D368 | 429.25, 1378.7798 | 0.450893, 0.612791 |
| 12 | 55–59 | D403 | 489.75, 1378.7798 | 0.514443, 0.612791 |
| 13 | 60–64 | D438 | 551.75, 1378.7798 | 0.579569, 0.612791 |
| 14 | 65–69 | D473 | 614.25, 1378.7798 | 0.645221, 0.612791 |

Normalization uses the exact table bounds 0..952 x 0..2250, rounded once to six places. Each spatial placement is `observed`: the table models the physical display pattern, and the manual confirms count and playfield topology. This does not assert that the model's millimetre geometry matches every original cabinet or that every LED pixel is an independent canonical lamp.
