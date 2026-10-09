# Williams Black Knight (game 500) - Instruction Booklet 16P-500-103: operation, bookkeeping, adjustments, diagnostics

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf`, Instruction Booklet 16P-500-103 (cover text: `Game No. 500`, `December, 1980`, `16P-500-103`), read from the 300 dpi renders `render\man300-06.png` ... `man300-13.png` and `man300-19.png` at native resolution (`crops2\p06-*.png`, `p07-*.png`, `p08-*.png`, `p09-*.png`, `t2-*.png`, `t3-*.png`, `p12-*.png`, `p13-*.png`, `p19-*.png`). The 400 dpi handbook render (`render\hb400-01.png` ... `hb400-04.png`) was OCR'd (Windows OCR) and compared with the booklet; wording agreed wherever compared (CPU jumpers cross-read visually).

| PDF page | Printed page | Content | Orientation |
|---|---|---|---|
| 6 | none (cover/title page; the printed `2` starts on the next page) | Title, introduction, special considerations, start of Game Operation | upright |
| 7 | `2` | Game Operation sections, speech phrases (first table) | upright |
| 8 | `3` | Speech phrases (second column), Bookkeeping, Table 1 | upright |
| 9 | `4` | Audit steps 5-8, Game Adjustment Procedure, Resetting High Score, Factory Audit Totals | upright |
| 10 | `5` | Table 2 Game Adjustments, notes, Recommended Score Levels | upright |
| 11 | `6` (printed sideways) | Table 3 Standard and Custom Price Settings | rotated: read after `Image.rotate(270, expand=True)` |
| 12 | `7` | Diagnostic Procedures: Display Digits Test, Sound Test | upright |
| 13 | `8` | Lamp Test | upright |
| 19 | `14` | Initiating Auto-Cycle Mode, CPU and Sound Board Self-Tests, vocabulary | upright |

(PDF pages 14-18 are Figure 1 / Figure 2 / Table 4 / Figure 3 / Figure 5 and are transcribed in the other files; the Solenoid Test is on PDF 15, the Switch Test on PDF 16-17.)

Normalization: none to wording. `¢` is the printed cent sign; `‑` hyphenation as printed. A trailing `*` in the sections below is printed in the source and marks "adjustable feature" (the page 6 legend: `*Indicates adjustable features.`). Italic-bold names (`Magna-Save`, `Multi-Ball`, `Multi-ball`) are italic bold as printed; the `Magna-Save` on PDF 7 carries a superscript trademark mark `TM` in places (see uncertainty list; page 6 states `Multi-Ball and Magna-Save are trademarks of Williams Electronics, Inc.`).

---

## PDF page 6: front matter

Header block (centred, above the title; the ornamental logo `WILLIAMS` scroll and the lines): `ELECTRONICS, INC.` (the OCR of the handbook cover also shows `16P-500-103`, `Game No. 500`, `December, 1980` at the top right of the cover page). The heading, bold, centred: `INSTRUCTION BOOKLET`.

Introductory paragraph, verbatim:

This booklet provides game operation, bookkeeping, game adjustment, and diagnostic and self-test procedures for BLACK KNIGHT. For installation information refer to the blue-covered game manual. For detailed information refer to Williams Solid State Flipper maintenance Manual.

### SPECIAL CONSIDERATIONS WHEN REPLACING CIRCUIT BOARDS (verbatim)

**CPU Board**
1. Revision level 7 CPU Boards (batteries located on lower left corner at board) or later boards must be used.
2. Must be equipped with blue-labeled Flipper ROMs and blue-labeled Game ROMs.
3. Jumpers W3, W10, W11, W14, W17, W19, W20, and W22 must be connected. Jumpers W4, W9, W12, W15, W16, W18, W21, and W23 must be removed. With the exception of W25, (Factory Setting Jumper) all other jumpers are not changed.

**Driver Board**
Either earlier model D 7997 or later model D 8341 boards may be used. When earlier boards are used, switch matrix series resistors R196 thru R211 must be zero-ohm or be replaced with wire jumpers. Later D 8341 boards do not use series resistors in the switch matrix.

**Sound Board**
1. D 8224 required for speech
2. Must be jumpered for white-labeled sound ROM operation and be equipped with Sound ROM 5. (Jumpers W2, W5, W7, W9, W10, W12, and W15 connected; W3, W4, W6, W8, W11, and W13 removed).

**Power Supply Board**
1. When transformer is mounted in cabinet, D 8345 board (equipped with relay) is required. When transformer is mounted in backbox, earlier D 7999 board is required.
2. F4 (20A SB) for flipper solenoids and magnets must be installed.

**Display Boards**
Model C 8363 Master Display and 7-digit Slave Displays required.

**Optional Speech Module**
Requires 5T5001 (IC7), 5T5002 (IC5), 5T5003 (IC6), and 5T5004 (IC4) Speech ROMs.

### GAME OPERATION (heading; verbatim)

*Indicates adjustable features.

**Game Over Mode** - Turn game ON; player 1 score shows 00, all player scores alternate the high score to date, Game Over lights, all playfield lamps cycle in attract mode.

Footer, italic: *Multi-Ball* and *Magna-Save* are trademarks of Williams Electronics, Inc.

---

## PDF page 7 (printed page 2): game operation sections (verbatim)

**Credit Posting** - Insert coin; sound produced, number of credits displayed. If maximum credits* exceeded by coin or high score to date*, credits are posted correctly, coin lockout de-energizes until remaining credits are below maximum. No credits may be won and coins are rejected while lockout is de-energized.

**Game Start** - Three balls must be resting on ball ramp, locking mechanism, or ball shooter switches (maximum of one ball in ball shooter trough) before game will start. Push credit button, startup tune played, ball served, credit display reduced by 1, player 1 score flashes 00 until first scoring switch is made, ball in play shows 1. Pushing credit button before ball 2 displayed allows additional players.

**Bonus Advance** - The bonus is advanced (from 1,000 to 49,000) one time by making left ramp rollover, twice by making left and right inside rollovers or outlanes, three times by completing a bank of drop targets, and five times by making left or right inside rollovers as a result of *Magna-Save*(TM) feature. With bonus at maximum and multiplier at 5x, completing a bank of drop targets or making one of the advance switches scores 5,000. Bonus multipliers are advanced from 2X to 5X by making the Turnaround.

*Magna-Save* **Feature*** - Completing a drop target 3-bank while associated lamp is still flashing scores 10,000, lights a target arrow, and lights a magnet. If the associated lamp goes out before the bank is completed, the bank is reset. With a magnet lamp lit, operating the corresponding *Magna-Save* button on the side of the cabinet energizes the magnet for a *few seconds and a ball held stationary by the magnet will tend to go through the inside rollover.

**Mystery and Spinner** - Making the left inside rollover flashes the right ramp rollunder for a mystery value. Making the rollunder while still flashing awards the mystery value which will be indicated on other player display(s). Making the right inside rollover flashes the spinner.

*Multi-Ball*(TM) **Play** - Making a ball in the lock mechanism when a lock arrow is flashing, lights a lock arrow steadily and lights the lower playfield eject hole. Locking three balls in the mechanism or making the eject hole when lit releases the balls from the mechanism. All scoring and mystery values are tripled while three balls are in play and doubled while two balls are in play. Lock arrows do not flash until turnaround is made.*

**Extra Ball** - A maximum of four * Extra Balls may be accumulated at one time. Spotting three arrows for both top and/or* both bottom banks lights the left ramp rollover for the first possible extra ball. Spotting all 3-bank arrows lights the Turnaround for the second possible Extra Ball. Spotting all 3-bank arrows alternately lights the left ramp rollover and Turnaround for additional Extra Balls. Making left ramp rollover or Turnaround when lit awards an Extra Ball.

**Last Chance*** - With locked balls on the last ball of the game, the left and right outside rollovers are lit for a "last chance." Making the rollover when lit releases any locked balls (no *Multi-Ball* scoring). If Extra Ball(s) is won during "last chance", the rollovers are not relit.

**Bonus Ball*** - With two or more players, a player with the highest score is awarded a bonus ball*. All three balls are released and play is allowed for 30* seconds with both magnet lamps lit. There is no *Multi-Ball* or mystery scoring or playfield Extra Ball feature during the bonus ball. Extra Balls won from Special or high score levels are awarded as additional bonus balls.

**Special** - Completing all four drop target 3-banks during the bonus ball lights the Turnaround for a possible Special. Making the Turnaround when lit awards a Special.

**Memory** - 3-bank drop target arrows, locked balls, magnet lamps, and Extra Ball lamps.

**Tilt** - Ball in play tilted on first closure of ball roll tilt and third* closure of Plumb Bob and playfield tilts. Slam tilt return game to game over.

**End of Game** - Match Digits* appears in ball in play display, *credit awarded for match. Exceeding high score to date awards *three credits. Match, High Score to Date, and Game Over sounds made as appropriate. A new game cannot be started with more than one ball resting in the ball shooter trough; excess balls must be returned to the playfield and rest on the ball ramp switches.

With Speech Module, the following phrases are produced during game play.

**Game start, add players 2, 3, and 4; Random phrase:**

- Defend thyself, Knight.
- I challenge thee to fight me.
- You cannot fight and win.
- I will slay you, my enemy.
- The BLACK KNIGHT will win again.
- The BLACK KNIGHT will slay you.
- Fight against me, the BLACK KNIGHT.
- I will slay thee, Knight.

Printed page number `2` at the lower left.

## PDF page 8 (printed page 3): speech phrases, bookkeeping, Table 1

Continuation of the speech phrases, as a two-column list. The page has no heading above it; it continues directly from the list on the previous page. Column headings, bold: `Achievement` | `Response`.

| Achievement | Response |
|---|---|
| 2-ball *Multi-ball* Play | Fight against 2 enemies. |
| 3-ball *Multi-ball* Play | Fight against 3 enemies. |
| *Magna-Save* drain | Laughter. |
| Win free game | I cannot slay you. You win. |
| Win Extra Ball | Fight me again, Knight. |
| **After last regular ball: (heading line, no response on that line) | (blank) |
| 1-player | One enemy cannot fight the BLACK KNIGHT again. (printed on two lines: `One enemy cannot fight the` / `BLACK KNIGHT again.`) |
| 2-,3-, or 4-players | You win the right to fight the BLACK KNIGHT again. (two lines: `You win the right to fight the` / `BLACK KNIGHT again.`) |
| High Score to Date | You win one fight. I challenge thee again. |
| Match | The BLACK KNIGHT will win again. |
| Game Over | Will you challenge the BLACK KNIGHT again? |

Footnote under the table, verbatim: `**Produced only if "Bonus Ball" enabled.`

(In the table, the `**` in `**After last regular ball:` is printed at the start of that line; the footnote line begins with `**`, written `**Produced only if "Bonus Ball" enabled.`)

### BOOKKEEPING AND GAME EVALUATION (Functions 01-17) (verbatim)

1. Set AUTO-UP/MANUAL-DOWN switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in the credits display, Function 00 in Match display, and Game Identification in Player 1 display.
2. Operate the ADVANCE pushbutton to display Functions 01 thru 04 on the Match display (See Table 1) and record the corresponding totals (number of coins and total paid credits) from the Player 1 display. (To review a total that has been advanced past, set switch to MANUAL-DOWN and operate the ADVANCE pushbutton).
3. Operate the ADVANCE pushbutton to display Functions 05, 06, and 07 in the Match display and record the corresponding free credit totals from the Player 1 display.
4. Operate the ADVANCE pushbutton to display Function 08 in the Match display. Total credits is indicated in the Player 1 display, total free credits in the Player 2 display, and percentage of free credits in the Player 4 display.

Steps 5-8 continue on PDF page 9.

### Table 1. Audit Totals

Caption (italic, centred): `Table 1. Audit Totals`. Column headings: `FUNCTION` | `DESCRIPTION` spanning `PLAYER 1` | `PLAYER 2` | `PLAYER 4`. A long dash `—` means a dash is printed in that cell.

| FUNCTION | PLAYER 1 | PLAYER 2 | PLAYER 4 |
|---|---|---|---|
| 00 | Game Identification (2500 2) | — | — |
| 01 | Coins, Left chute (closest to coin door hinge) | — | — |
| 02 | Coin, center chute | — | — |
| 03 | Coin, right chute | — | — |
| 04 | Total Paid Credits | — | — |
| 05 | Special Credits | — | — |
| 06 | Replay Score Credits | — | — |
| 07 | Match Credits | — | — |
| 08 | Total Credits | Free Credits | % Free Credits |
| 09 | Total Extra Balls | — | — |
| 10 | Ball Time in Minutes | — | — |
| 11 | Total Balls Played | — | — |
| 12 | Current High Score to Date | — | — |
| 13 | Backup High Score to Date | High Score to Date Credits Awarded | — |
| 14 | Replay 1 Score | Times exceeded | — |
| 15 | Replay 2 Score | Times exceeded | — |
| 16 | Replay 3 Score | Times exceeded | — |
| 17 | Replay 4 Score | Times exceeded | — |

(18 rows, Functions 00-17. Rows 01, 12 and 13 wrap onto a second line in the Description column: `(closest to coin door hinge)`, `to Date`, `to Date`; row 13's Player 2 cell wraps as `High Score to Date` / `Credits Awarded`.) Printed page number `3` at the lower right.

## PDF page 9 (printed page 4): audit steps 5-8, Game Adjustment Procedure, High Score reset, Factory Audit Totals (verbatim)

5. Operate the ADVANCE pushbutton to display Function 09 thru 12 in the Match display and record the corresponding totals from the Player 1 display.
6. Operate the ADVANCE pushbutton to display Functions 13 thru 17 in the Match display and record the corresponding totals from the Player 2 display.
7. With switch set to MANUAL-DOWN operate ADVANCE to display Function 50 in the Match Display. From Function 50 you can return to game over or zero audit totals and return to game over. Perform step 8.a. or 8.b. as desired.
8. a. To return to game over, set the switch to AUTO-UP and depress ADVANCE.
   b. To zero audit totals and return to game over set switch to AUTO-UP, operate the credit button to display 35 in the Player 1 display, and depress ADVANCE.

**GAME ADJUSTMENT PROCEDURE**
(Functions 13-41)

**Coin door must be open to change settings.**

1. Set AUTO-UP/MANUAL-DOWN switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in the Credits display, Function 00 in Match display, and game identification in Player 1 display.
2. To raise Function number in Match display, operate ADVANCE pushbutton with switch set to AUTO-UP. To lower Function number operate ADVANCE with it set to MANUAL-DOWN.
3. With desired Function indicated in Match display, raise value in player 1 display by operating credit button with switch set to AUTO-UP; lower value by operating credit button with it set to MANUAL-DOWN. Value left in Player 1 display is new setting. For values see Table 2 and (for pricing) Table 3.
4. Repeat sets 2 and 3 until all required adjustments have been made.
5. Operate ADVANCE until Function 50 is indicated in Match display. From Function 50 you can return to game over or restore factory settings. Perform step 6 or 7 as desired.
6. To return to game over, depress ADVANCE with switch set to AUTO-UP.
7. To restore factory settings and zero audit totals:
   a. Operate Credit button with switch set to AUTO-UP until 45 is indicated in Player 1 Display.
   b. Depress ADVANCE. The game returns to Test 04, Function 00.
   c. Set switch to MANUAL-DOWN and depress ADVANCE to indicate Function 50.
   d. Set switch to AUTO-UP and depress ADVANCE.

(`sets 2 and 3` in step 4 is printed `sets`, as written. In the printed text step 1's `Credits display` and step 3 bold words `raise`, `lower` are bold as printed.)

**RESETTING HIGH SCORE TO DATE**
1. Using game adjustment procedure, set Function 13 to the desired reset value.
2. Depress HIGH SCORE RESET pushbutton.

**FACTORY AUDIT TOTALS**
(Functions 42-49)
The following factory audit functions are assigned:
42 - Total "Last Chance" won
43 - Total times *Multi-ball* achieved
44 - Total times "Mystery" score won
45 - Total "Bonus" balls awarded
49 - Number of Auto Cycle Test Passes.

Printed page number `4` at the lower left.

## PDF page 10 (printed page 5): Table 2. Game Adjustments

Caption (italic, centred): `Table 2. Game Adjustments`. Column headings: `FUNCTION` | `DESCRIPTION` | `NOTES` | `*FACTORY SETTING`. A long dash `—` in the NOTES column means a dash is printed (no note). Where two factory settings are shown separated by `/`, the second applies with jumper W25 connected (footnote below).

| FUNCTION | DESCRIPTION | NOTES | *FACTORY SETTING |
|---|---|---|---|
| 13 | Backup High Score to Date [HSTD Credits Awarded] | 1 | 2,500,000 |
| 14 | Replay 1 Score [Times exceeded] | 2 | 1,000,000 |
| 15 | Replay 2 Score [Times exceeded] | 2 | 2,000,000 |
| 16 | Replay 3 Score [Times exceeded] | 2 | 0 |
| 17 | Replay 4 Score [Times exceeded] | 2 | 0 |
| 18 | Maximum Credits | 3 | 30 |
| 19 | Standard and Custom Pricing Control (00-08) | 4 | 01/03 |
| 20 | Left Coin Slot Multiplier | 4 | 03/09 |
| 21 | Center Coin Slot Multiplier | 4 | 12/45 |
| 22 | Right Coin Slot Multiplier | 4 | 03/18 |
| 23 | Coin Units Required for Credit | 4 | 04/05 |
| 24 | Coin Units Bonus Point | 4 | 15/45 |
| 25 | Minimum Coin Units | 4 | 00 |
| 26 | Match: 00 = Match ON; 01 = Match OFF | — | 00 |
| 27 | Special: 00 = Awards Credit; 01 = Awards Bonus Ball; 02 = Awards Points | — | 00 |
| 28 | Replay Scores: 00 = Awards Credit; 01 = Awards Extra Ball or Bonus Ball | — | 00 |
| 29 | Maximum Plumb Bob Tilts | — | 03 |
| 30 | Number of Balls(03 or 05) | — | 03 |
| 31 | *Magna-Save* Feature: 03-09 = on time in seconds | 5 | 05 |
| 32 | Attract Mode Sound; 00 = ON; 01 = OFF | — | 00 |
| 33 | Drop Target Timing: 00-09 = 6-15 seconds | — | 03 |
| 34 | "Bonus Ball" Time: 00 = not allowed; 01-99 = Time in seconds | — | 30 |
| 35 | Bell: 00 = Bell OFF; 01 Bell ON | — | 01 |
| 36 | Extra Ball Difficulty 00 = 1st EB from pair of drop target banks / 01 = All EBs from four drop target banks | — | 00 |
| 37 | Multi-Ball Difficulty: 00 = Liberal; 01 = Moderate | — | 00 |
| 38 | Locked Ball lamps: 00 = Memory; 01 = No Memory | — | 01 |
| 39 | Background Sound: 01 = ON; 00 = OFF | — | 01 |
| 40 | High Score Credits | 1 | 03 |
| 41 | Maximum Extra Balls at one time (00 = No Extra Ball) | — | 04 |

(29 rows, Functions 13-41; row 36 wraps onto a second printed line: `Extra Ball Difficulty 00 = 1st EB from pair of drop target banks` / `01 = All EBs from four drop target banks`; the header cell for the last column is printed `*FACTORY SETTING`.) Note: the printed descriptions use the spelling `Locked Ball lamps` (lower-case l in `lamps`), `Number of Balls(03 or 05)` with no space before the parenthesis, and `01 Bell ON` with no `=`.

Notes below the table, verbatim (the first two lines are preceded by `*` and `[ ]` markers hanging at the left):

- `*  Second Factory Setting value is with jumper W25 connected.`
- `[ ]  Description in brackets shown in Player 2 Display.`
1. Function 13 may be set to any multiple of 100,000 points. Setting Function 40 to zero with Function 13 set to any score but zero permits the High Score to Date feature to operate but no credits are awarded.
2. Functions 14-17 (Replay Scores) may be set to any multiple of 100,000 points. Setting a function to zero disables the replay score point.
3. Setting Maximum Credits (Function 18) to zero places the game in a free play mode.
4. With Function 19 set to 00, Functions 20-25 must be set manually. Refer to Table 2 for eight standard pricing schemes (selected by values of 01-08 for Function 19) and custom pricing values.
5. Magnets always enabled during "Bonus Ball".

**RECOMMENDED SCORE LEVELS** (bold, centred)
**CREDIT GAMES** (centred)
3-Ball: *1,000,000; 2,000,000
5-Ball: 2,000,000; 3,000,000
**EXTRA BALL** (centred)
3-Ball: 700,000
5-Ball: 1,000,000
*Factory Setting

Printed page number `5` at the lower right.

(Note 4 refers to `Table 2` for the pricing schemes, although the pricing schemes are in Table 3 on the next page; transcribed as printed.)

## PDF page 11 (printed page 6, printed sideways): Table 3. Standard and Custom Price Settings

Caption (italic): `Table 3. Standard and Custom Price Settings`. Rotated 270 degrees with PIL to read upright. Column headings: `COIN DOOR MECHANISM` | `CREDITS` | `FUNCTION` spanning `19` `20` `21` `22` `23` `24` `25`. A bullet `•` before a CREDITS entry marks the footnote's "standard price setting"; those rows are printed in bold type (numbers bold). Rows in the same coin-door group are separated by hairlines only between groups; a group label with no new label line below applies to the rows beneath it.

| COIN DOOR MECHANISM | CREDITS | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|
| Twin-Quarter / Quarter, Dollar, Quarter (label printed on two lines, spanning rows 1-15) | 1/25¢, 3/50¢, 7/$1 | 00 | 03 | 12 | 03 | 02 | 12 | 00 |
| (same) | 1/25¢, 3/50¢, 7/$1 coin only | 00 | 03 | 14 | 03 | 02 | 00 | 00 |
| (same) | 1/25¢, 7/$1 coin only | 00 | 01 | 07 | 01 | 01 | 00 | 00 |
| (same) | 1/25¢, 3/50¢, 6/$1 | 00 | 01 | 04 | 01 | 01 | 02 | 00 |
| (same) | 1/25¢, 6/$1 coin only | 00 | 01 | 06 | 01 | 01 | 00 | 00 |
| (same) | 1/25¢, 5/$1 | 00 | 01 | 04 | 01 | 01 | 04 | 00 |
| (same) | 2/50¢, 5/$1 | 00 | 01 | 04 | 01 | 01 | 04 | 02 |
| (same) | 1/25¢, 5/$1 coin only | 00 | 01 | 05 | 01 | 01 | 00 | 00 |
| (same) | •1/25¢, 4/$1 | 03 | 01 | 04 | 01 | 01 | 00 | 00 |
| (same) | 2/50¢, 4/$1 | 00 | 01 | 04 | 01 | 01 | 00 | 02 |
| (same) | •1/50¢, 2/75¢, 3/4 x 25¢ (line 2: `4/$1 or 5 x 24¢`) | 05 | 03 | 15 | 03 | 04 | 15 | 00 |
| (same) | 1/50¢, 3/$1, 4/$1.25 | 00 | 03 | 12 | 03 | 04 | 15 | 00 |
| (same) | 1/50¢, 3/$1, 7/$2 | 00 | 12 | 48 | 12 | 14 | 96 | 18 |
| (same) | •1/50¢, 3/$1, 6/$2 | 01 | 01 | 04 | 01 | 02 | 04 | 00 |
| (same) | 1/50¢ | 00 | 01 | 04 | 01 | 02 | 00 | 00 |
| 1DM, 5DM, 2DM (printed `1DM, 5DM,2DM`; on the scan the first character may read `I`) | •1/1DM, 3/2DM, 10/5DM | 02 | 09 | 45 | 18 | 05 | 45 | 00 |
| (same) | 2/1DM, 5/2DM, 14/5DM | 00 | 13 | 65 | 26 | 05 | 65 | 00 |
| 20-Cent, 50-Cent | 1/20¢, 3/50¢ | 00 | 06 | 00 | 15 | 05 | 00 | 00 |
| 1 Franc, 10 Franc, 5 Franc | •1/2F, 3/5F only, 8/10F only | 04 | 01 | 16 | 06 | 02 | 00 | 00 |
| 25 Cent, / 1 Guilder, (label on two lines) | •1/25¢, 4/1G | 06 | 01 | 00 | 04 | 01 | 00 | 00 |
| (same) | 1/25¢, 5/1G | 00 | 01 | 00 | 04 | 01 | 04 | 00 |
| Twin 100 Yen | 2/100Y | 00 | 02 | 00 | 02 | 01 | 00 | 00 |
| 1 Franc or / Twin-1 Franc | 1/1F, 3/2F | 00 | 01 | 01 | 01 | 01 | 02 | 00 |
| (same) | 1/1F | 00 | 01 | 01 | 01 | 01 | 00 | 00 |
| 5 Franc, / 10 Franc | •1/5F, 2/10F | 07 | 01 | 00 | 02 | 01 | 00 | 00 |
| (same) | •1/10F | 08 | 01 | 00 | 02 | 02 | 00 | 00 |
| Twin-2 Franc | •1/2F | 03 | 01 | 04 | 01 | 01 | 00 | 00 |
| 10, 20 Franc | •1/10F, 2/20F | 07 | 01 | 00 | 02 | 01 | 00 | 00 |
| Twin-1 Sucre | 1/3S, 2/5S | 00 | 02 | 00 | 02 | 05 | 00 | 00 |

(30 rows. The `5 Franc, / 10 Franc` label is printed on two lines and applies to two rows: `1/5F, 2/10F` and `1/10F` - its horizontal rules are drawn so that the label `5 Franc,` sits on the first row and `10 Franc` on the second. Same for `1 Franc or / Twin-1 Franc`, `25 Cent, / 1 Guilder,`.)

Footnote, verbatim: `•Indicates standard price settings by adjusting only Function 19. For other price settings, set Function 19 to 00 and set Functions 20 through 25 to the values indicated in the chart.`

Some cell digits in the 24 column of the first group are printed in bold in the scan even where the row is not a `•` row (rows `1/50¢, 3/$1, 4/$1.25`, the `04` and `15` of that row): this is scan weight, not a marker.

## PDF page 12 (printed page 7): DIAGNOSTIC PROCEDURES (verbatim)

**DIAGNOSTIC PROCEDURES**

**Display Digits Test**
1. Set AUTO-UP/ to MANUAL-DOWN switch and depress ADVANCE. Displays should indicate all 0's.
2. Set the switch to AUTO-UP. Displays should sequence from all 0's thru all 9's. Comma segments should come on when odd digits are displayed.
3. To stop cycling, set switch to MANUAL-DOWN. Operate ADVANCE pushbutton to step tests one number at a time. Set switch to AUTO-UP to resume cycling.

**Sound Test**
1. From Display Digits Test depress ADVANCE with the switch set to AUTO-UP. Test 00 should be indicated in the number of Credits display and the Match display sequences from 00 thru 06. Different sounds should be produced for 00, 01, 02, 03, and 04.
2. To continuously pulse a single sound, set the toggle switch to MANUAL-DOWN. Operate ADVANCE pushbutton to sequence through sounds one at a time. Set toggle switch to AUTO-UP to resume sequencing.

Printed page number `7` at the lower right. (Step 1 of Display Digits Test is printed `Set AUTO-UP/ to MANUAL-DOWN switch`, as written; the text reads `Set AUTO-UP/` (a dangling slash) `to MANUAL-DOWN switch`.)

## PDF page 13 (printed page 8): Lamp Test (verbatim)

**Lamp Test**
From Sound Test depress ADVANCE with the switch set to AUTO-UP Test 01 should be indicated in the Credits display and all multiplexed lamps should flash.

(`AUTO-UP Test 01` has no full stop between `AUTO-UP` and `Test`, as printed.) Printed page number `8` at the lower right.

The Solenoid Test (Test 02) follows on PDF page 15 and the Switch Test (Test 03) on PDF pages 16-17 (see `solenoid-locations.md` and `switch-locations.md`).

## PDF page 19 (printed page 14): Auto-Cycle mode and board self-tests (verbatim)

**INITIATING AUTO-CYCLE MODE**

1. Set AUTO-UP/MANUAL-DOWN switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in Credit display and Function 00 in Match Display.
2. Set switch to MANUAL-DOWN and depress ADVANCE to indicate Function 50 in the Match Display.
3. Set switch to AUTO-UP and operate Credit button to indicate 15 in Player 1 Display.
4. Depress ADVANCE pushbutton to start Auto-Cycle mode. Each cycle of this mode sequences thru the Display Digits Test, Sound Test (00), Lamp Test (01), and Solenoid test (02).
5. To terminate the test and return to game over, turn the game OFF and back ON.

**CPU BOARD SELF-TEST**
Depress the DIAGNOSTIC pushbutton on the left side of the CPU Board. The following indications are provided for a few seconds and then the game attempts to go to game over:

| Code | Indication (verbatim) |
|---|---|
| 0 | Test Passed |
| 1 | IC13 RAM Faulty |
| 2 | IC16 RAM Faulty |
| 3 | IC17 ROM 2 Faulty |
| 4 | IC17 ROM 2 Faulty |
| 5 | IC20 ROM 1 Faulty |
| 6 | IC14 Game ROM 1 Faulty |
| 7 | IC26 Game ROM 0 Faulty |
| 8 | IC19 CMOS RAM or Memory Protect Circuit Faulty |
| 9 | Coin-door closed, Memory Protect Circuit Faulty, or IC19 CMOS RAM Faulty. |

Note that "0" remaining after power turn-on indicates CPU Board lockup.

**SOUND BOARD SELF-TEST**
Depress DIAGNOSTIC pushbutton on the top of the Sound Board. Several electronic sounds should be produced and then the BLACK KNIGHT vocabulary is produced. This sequence is repeated until the game is turned OFF and back ON.

Vocabulary table (columns `Vocabulary` | `Located in ROM`, underlined headings):

| Vocabulary | Located in ROM |
|---|---|
| KNIGHT | 5T 5001 (IC7) |
| BLACK | 5T 5001 |
| DEFEND | 5T 5001 |
| CHALLENGE | 5T 5001 |
| THEE (THE) | 5T 5002 (IC5) |
| WILL | 5T 5002 |
| YOU | 5T 5002 |
| I | 5T 5002 |
| AGAIN | 5T 5002 and 5T 5003 (IC6) |
| SLAY | 5T 5003 |
| CANNOT | 5T 5003 |
| SELF | 5T 5003 |
| ENEMY | 5T 5003 and 5T 5004 (IC4) |

The IC4 Speech ROM contains laughter and "F" and "R" sounds. The laughter, "F" and "R" sounds, and the following partial or composite words produced in game play are not produced in diagnostics.

| | | |
|---|---|---|
| WIN | ENEMIES | THREE |
| ME | THYSELF | AND |
| TO (TWO) | FIGHT | MY |
| AGAINST | RIGHT | (blank) |

Printed page number `14` at the lower left.

## Observations (internal inconsistencies and oddities, all as printed)

1. CPU self-test codes 3 and 4 both read `IC17 ROM 2 Faulty` (code 3 `IC17 ROM 2 Faulty`, code 4 `IC17 ROM 2 Faulty`); the two lines are identical in the booklet scan. (Compare the handbook printing: not separately verified for these two lines.)
2. Table 2 note 4 says `Refer to Table 2 for eight standard pricing schemes` while the pricing schemes are in Table 3. Table 3 has ten rows marked with a bullet (standard price settings); their Function 19 values are 03, 05, 01, 02, 04, 06, 07, 08, 03, 07 (in table order), so the values 01-08 each occur and 03 and 07 occur twice.
3. Table 2 gives two-valued factory settings for Functions 19-24 (`01/03`, `03/09`, `12/45`, `03/18`, `04/05`, `15/45`) with the second value for jumper W25 connected. The Table 3 rows do not reproduce these combinations: the Table 3 row with Function 19 = 01 reads 20=01, 21=04, 22=01, 23=02, 24=04, and the row with Function 19 = 03 reads 20=01, 21=04, 22=01, 23=01, 24=00 (two such rows), while Table 2's Functions 20-24 first values are 03, 12, 03, 04, 15 (matching the Table 3 row `1/50¢, 3/$1, 4/$1.25`, 19 = 00) and second values 09, 45, 18, 05, 45 (matching the row `•1/1DM, 3/2DM, 10/5DM`, whose Function 19 is 02). Recorded as an observation only; no cell was changed.
4. The `Special` adjustment (Function 27) and `Replay Scores` (Function 28) wording `Awards Credit`/`Awards Bonus Ball`/`Awards Points`/`Awards Extra Ball or Bonus Ball` is as printed.
5. The Game Adjustment Procedure heading says `(Functions 13-41)`, while Table 2 lists functions 13-41 (29 rows) and the Factory Audit Totals heading says `(Functions 42-49)` listing only 42, 43, 44, 45 and 49 (46, 47, 48 not listed). Table 1's heading says `(Functions 01-17)` (the table lists 00-17).
6. The Lamp Test text says `Test 01`, the Sound Test `Test 00`, Bookkeeping `Test 04`, matching the Auto-Cycle list (`Sound Test (00), Lamp Test (01), and Solenoid test (02)`) and the Solenoid Test text (`Test 02`) and Switch Test text (`Test 03`) on pages 15-17. The Solenoid Test text on PDF 15 says the display sequences `01 thru 25`.
7. In the Game Over speech table the response to `Match` is `The BLACK KNIGHT will win again.` and to `Win free game` is `I cannot slay you. You win.`; the vocabulary table on PDF 19 lists `WIN` as a composite word not produced in diagnostics, consistent with `win` being formed from parts.
8. The vocabulary list says `KNIGHT, BLACK, DEFEND, CHALLENGE` are in 5T 5001 (IC7); the Special Considerations list on PDF 6 names the ROMs `5T5001 (IC7), 5T5002 (IC5), 5T5003 (IC6), and 5T5004 (IC4)` (printed without a space between `5T` and the number there, with a space `5T 5001` in the vocabulary table).

## Uncertain readings (this file)

- `TM` after `Magna-Save` in `Bonus Advance` (PDF 7) and after `Multi-Ball` in `Multi-Ball(TM) Play`: printed as a small raised mark; read as `TM` (the page 6 footer states they are trademarks). [uncertain: `TM` vs. a stray raised mark]
- Table 3 first column of the DM row reads `1DM` or `IDM` (letter I vs digit 1). Credits column reads `1/1DM`. [uncertain: `1DM, 5DM, 2DM` vs. `IDM, 5DM, 2DM`]
- PDF 11 printed page number: a rotated mark in the upper left of the sideways scan reads `6` (could be `9` if viewed upside down; by sequence 5 -> 6 -> 7 it is `6`). [uncertain: `6`]
- Table 3: bold weight on some non-bullet cells (row `1/50¢, 3/$1, 4/$1.25`, columns 23 and 24) is as scanned.
