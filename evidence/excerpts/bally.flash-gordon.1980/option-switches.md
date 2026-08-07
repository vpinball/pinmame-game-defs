# Flash Gordon - MPU option switches S1-S32 and self-test positions

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF pages 10 through 13, printed
pages 5 through 8, section `V. GAME ADJUSTMENTS`. Read from the retained PDF's text layer and
checked against 200 dpi renders. The two coin-ratio matrices reproduce badly and their individual
ON/OFF rows are deliberately not transcribed, because no assertion in this definition rests on them;
what is transcribed is which switches select each function.

> Each game has thirty-two switches located on A4, the MPU module, located in the back box, that
> allow play to be customized to the location. [...] The switches are contained in four-sixteen lead
> packages numbered S1-8, S9-16, S17-24, and S25-32 for easy identification. The "ON" toggle
> position is marked on the assembly. Turn off power before making adjustments.

| Switches | Function |
| --- | --- |
| S1-S5 | Credits per coin, coin chute #1 (hinge side). Thirty-one ratios available. |
| S6 | Saucer 10,000 lite adjustment. ON = 10K is on at start of game. |
| S7 | Saucer values lite adjustment. ON = any lit value will come on for next ball. |
| S8 | Saucer 2X, 3X arrow lite adjustment. ON = any lit arrow will come on for next ball. |
| S9-S13 | Credits per coin, coin chute #3 (right side). Thirty-one ratios available. |
| S14 | Outlane specials lite adjustment. ON = lit special lites will come on for next ball. |
| S15 | Top target special lite adjustment. ON = lit special lite will come on for next ball. |
| S16 | 2X, 3X, 4X, 5X bonus lite adjustment. ON = any lit bonus lite will come on for next ball. |
| S17-S20 | Credits per coin, coin chute #2 (center). All four OFF = same as coin chute #1 settings. |
| S21 | Game over attract adjustment. ON = voice says "Emperor Ming Awaits"; OFF = no voice. |
| S22 | 2 side targets and flipper feed lanes lite adjustment. |
| S23 | 4 drop target lite adjustment. |
| S24 | Top 3 target arrow lite adjustment. |
| S25-S26 | Maximum credits: 10, 15, 25 or 40. |
| S27 | Credit display. ON = credits displayed, OFF = not displayed. |
| S28 | Match feature. ON = match on. |
| S29 | Number of replays per game. ON = all replays earned collected; OFF = one per player per game. |
| S30 | In-line extra ball lite adjustment. ON = one extra ball per ball; OFF = one per game. |
| S31-S32 | Balls per game: 2, 3, 4 or 5. |

Thirty-two positions, all accounted for, no gaps.

`S33` is named separately on the same pages and is **not** an option switch: it is a momentary button
on the MPU assembly used to zero a high-score level ("Can be quickly set to '00' by pressing S33 on
the MPU assembly in the back box or Coin Chute switch #3").

Self-test positions 16 through 19 are ROM adjustments reached by pulsing the credit button, not
switches: 16 and 17 select replay / extra ball / novelty / no award for the two high-score levels,
18 selects one of four sound settings, and 19 selects the high-score-to-date award, 00 through 03
credits.
