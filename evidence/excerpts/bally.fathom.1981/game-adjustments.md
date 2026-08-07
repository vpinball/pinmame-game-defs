# Bally Fathom — self-test procedure and MPU option switches S1-S32

Source: `Bally_1981_Fathom_English_Manual.pdf`. Transcribed by hand from 200 dpi renders of PDF
pages 11, 12, 13, 19 (printed pages 5, 6, 7 and the `VIII. ROUTINE MAINTENANCE ON LOCATION` page).

## Self-test procedure, printed verbatim (excerpt)

> Game Self-Diagnostic Tests:
> 1. Pressing the Self-Test button inside the door initiates the Self-Test routine. See Figures III
>    and IV. All switched lamps flash off and on continuously.
> 2. Pressing the Self-Test button again causes each digit on each display to cycle from 0 thru 9,
>    and repeat continuously.
> 3. Pressing the Self-Test button again causes each solenoid to be energized, one at a time, in a
>    continuous sequence. Hold both flipper buttons 'in' during this test. The number appearing on
>    the Player Score displays is the same as the number assigned to the solenoid. The sound of a
>    solenoid pulling-in as a number appears indicates proper operation. The absence of sound is
>    improper. If sound is absent, see Page 17 for help in Solenoid identification.
> 4. Pressing Self-Test button again causes the sound module to play the "Game Over" tune repeatedly.
> 5. Pressing the Self-Test button again causes the MPU to search each switch assembly for stuck
>    contacts. If any are found, the number of the first set encountered is flashed on the Player
>    Score displays. [...] See Page 17 for help in Stuck Switch identification.
> 6. Pressing the Self-Test button 22 more times causes the MPU to step thru the threshold and
>    bookkeeping functions described previously and finally to repeat the power-up test.

This is the sentence that makes the printed `Self Test #` column meaningful: the ROM pulses the
coils in printed order, one at a time, in a continuous sequence. Recording the order in which
addresses fire during test 3 therefore resolves the printed-number to public-address mapping without
guessing.

## Option switches

Printed on page 5: "Each game has thirty-two switches located on A4, the MPU module, located in the
back box [...] The switches are contained in four-sixteen lead packages numbered S1-8, S9-16,
S17-24, and S25-32 for easy identification. The 'ON' toggle position is marked on the assembly.
Turn off power before making adjustments."

| switch | printed function |
| --- | --- |
| S1-S5 | Credits per coin, coin chute #1 (hinge side). Thirty-one ratios; the manual gives a combination table, not a per-switch meaning. |
| S6 | End of game balls in saucer. `SW. 6 ON` liberal: any ball in saucer will not kick out at end of game. `SW. 6 OFF` conservative: any ball in saucer will kick out at end of game. |
| S7 | Collect bonus special. `ON` liberal: reaching both 55 bonus lites and completing blue **or** green bonus lites will score 1 replay. `OFF` conservative: blue **and** green. |
| S8 | Extra ball lite flashing time. `ON` liberal: lite will flash for 10 seconds. `OFF` conservative: 6 seconds. |
| S9-S13 | Credits per coin, coin chute #3 (right side). Same combination table as S1-S5. |
| S14 | *not documented in this manual* |
| S15 | *not documented in this manual* |
| S16 | A-B-C special lite. `ON` liberal: lite will alternate to collect more than 1 replay. `OFF` conservative: lite will come on for 1 replay per ball. |
| S17-S20 | Credits per coin, coin chute #2 (center). Sixteen settings; `S20 S19 S18 S17` all OFF means "Same as Coin Chute #1 Settings", then 1/1 through 15/1 coin. |
| S21 | *not documented in this manual* |
| S22 | Blue and green inline drop target. `ON` liberal: any blue or green inline drop target down will drop down for next ball. `OFF` conservative: it will not. |
| S23 | 1 to 10 bonus lite recall. `ON` liberal: any 1-10 lit bonus lite will come on for next ball. `OFF`: it will not. |
| S24 | A-B-C lane lite recall. `ON` liberal: any lit lite will come on for next ball. `OFF`: it will not. |
| S25, S26 | Maximum credits. `26 25`: OFF OFF = 10, OFF ON = 15, ON OFF = 25, ON ON = 40. |
| S27 | Credit display. `ON` = credits displayed YES, `OFF` = NO. |
| S28 | Match feature. `ON` = match on, `OFF` = off. |
| S29 | Number of replays per game. `ON` liberal: all replays earned will be collected. `OFF` conservative: only 1 replay per player per game. |
| S30 | Game over attract. `ON` liberal: voice says "Help! Surface, Surface, Fathom" or "Danger, Sea Nymph Await Fathom". `OFF`: no voice. |
| S31, S32 | Balls per game. `32 31`: OFF ON = 5, ON OFF = 4, OFF OFF = 3, ON ON = 2. |

Note that S25/S26 and S31/S32 are printed with the higher-numbered switch as the left-hand
(most significant) column of the combination table.

## Score-level and sound adjustments

Not option switches: the high score levels, the high-score-to-date award and the sound option are
set from the front door with the Self-Test and Credit buttons, at self-test positions 01 (score
level), 16, 17, 18 (sound option) and 19 (high score to date award). Page 7 gives the four sound
settings `00`/`01` (chimes without background), `02` (noise effect without background) and `03`
(noise effect with background).
