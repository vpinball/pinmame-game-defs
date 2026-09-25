# Williams Firepower (game 497) — Instruction Booklet: board requirements, game operation, diagnostics

Source: `Williams_1980_Firepower_Instruction_Booklet.pdf` (IPDB 856), cover `16P-497-103`,
`Game No. 497`, `January, 1980`; PDF pages 1, 2, 3 and 7. Read from native-resolution renders; the
scan's own OCR text layer was used only to locate passages, and every quoted line below was checked
against the rendered page.

A second copy of the booklet, Internet Archive item `arcademanual_Firepower_OPS`
(`Firepower_OPS.pdf`, "Firepower Instruction Booklet", scanned 1999 by gamearchive.com), is a
different printing: where this copy says `flashing "1-6" drop targets`, `*lit drop target arrows`
and `Making "1-6" drop targets`, that copy says `flashing "1-6" targets`, `*lit target arrows` and
`Spotting "1-6" lamps`, and its Figure 6 and Figure 4 use `TARGET` throughout, as this copy's
Figures do.

## Page 1 — SPECIAL CONSIDERATIONS WHEN REPLACING CIRCUIT BOARDS

- CPU Board: `1. Revision level 6 CPU Boards (batteries located on lower right corner of board) or
  later boards must be used.` `2. Must be equipped with green-labeled FIREPOWER PROMs,
  green-labeled game ROM and green-labeled flipper ROMs.` `3. Jumper J4 must be connected and J3
  removed.`
- Sound Board: `1. Model D 8224 required for speech.` `2. Must be jumpered for white-labeled sound
  ROM operation and be equipped with Sound ROM 3. (Jumpers W2, W5, W7, W9, W10, and W15 connected;
  W3, W4, W6, W8, W11, W12, and W13 removed)`
- Power Supply Board: `1. Fuse F4 (10A SB) for flipper solenoids must be installed.`
- Optional Speech Module: `1. Requires 5T4971 (IC7), 5T4972 (IC5), and 5T4973 (IC6) speech ROMs.`

## Pages 1-2 — GAME OPERATION (excerpts)

- `Game Over Mode - Turn game ON; player scores show zero, high score to date* alternates with
  player 1 score, player 1 up lamp flashes, game over lamp lights, all playfield lamps except for
  credit lamp cycle in attract mode.`
- `Credit Posting - Insert coin; knocker sounds, number of credits displayed. If maximum credits*
  exceeded by coin or high score to date*, credits are posted correctly, coin lockout deenergized
  until remaining credits are below maximum.`
- `Game Start - Push credit button; start-up tune played, ball served, credit display reduced by
  one, player 1 up lamp flashes until first scoring switch is made, ball in play shows 1.`
- `Bonus Advance - "F-I-R-E" rollovers when not lit, flashing "1-6" drop targets, left and right
  inside rollovers (3 advances when lit), and left and right outside rollovers. Bonus multiplier
  advanced and FIRE insert lit by spotting "F-I-R-E". "F-I-R-E" lamps rotate by actuating right
  flipper (LANE CHANGE feature).`
- `FIREPOWER - Making three power targets scores 10,000 and lites POWER insert, left and right
  inside rollovers, and *ball saver kicker ON. Liting FIRE and POWER inserts scores and advances
  FIREPOWER bonus (5,000 or lit values of 10, 30, and 50,000). Outlane Special lit when *30, or
  50,000 bonus collected.`
- `Eject Holes - Making eject hole when flashing locks up ball and new ball released per following
  order: from ball ramp, flashing eject hole, unlit eject hole. Locking up all balls in eject holes
  initiates MULTI-BALL play.`
- `Extra Ball - Maximum of two Extra Balls per ball. Lighting *5x or making "F-I-R-E" with 5x lit
  lights center POWER target for Extra Ball.`
- `Tilts - Ball in play tilted on first closure of Playfield and Ball Roll tilts and third* closure
  of Plumb Bob. Slam Tilt returns game to game over.`
- `End of Game - Match Digits* appears in ball in play display ... Balls released from eject holes
  and are placed on ball ramp before new game can be started.`
- Footnote: `MULTI-BALL and LANE CHANGE are trademarks of Williams Electronics, Inc.`

## Page 2 — BOOKKEEPING (step 1)

`In game over mode, set alternate-action switch to AUTO-UP (out) and depress ADVANCE pushbutton.
Test 04 is indicated in number of credits display, Function 00 in ball in play display, and game
identification in Player 1 display.`

## Page 3 — DIAGNOSTIC PROCEDURES (Display Digits, Lamp, Solenoid, and Switch Tests)

1. `In game over mode, set alternate-action switch to MANUAL-DOWN (in) and depress ADVANCE. All
   displays should go blank.`
2. `Momentarily depress ADVANCE and set switch to AUTO-UP (out). Display Digits test is performed.`
3. `Momentarily depress ADVANCE. Test 01 is indicated on number of credits display and Lamp Test
   is performed.`
4. `Set switch to MANUAL-DOWN (in) and momentarily depress ADVANCE. Test 02 is indicated on number
   of credits display and solenoid 01 on the ball in play display; solenoid 01 is pulsed by driver
   board.`
5. `Operate ADVANCE to pulse each solenoid (see Figure 3). Pulse solenoid 08 three times to remove
   balls from ramp before proceeding to switch test.`
6. `Set switch to AUTO-UP (out) and momentarily depress ADVANCE. Test 03 is indicated on number of
   credits display and stuck switches on ball in play display.`
7. `See Figure 4. Operate switches; switch number is indicated on ball in play display.`
8. `Turn game OFF and back ON to return to game over mode.`

## Page 7 — RESETTING AUDIT TOTALS AND ADJUSTMENTS; INITIATING AUTO-CYCLE MODE

3. `Set all switches on the MASTER COMMAND slide switch to OFF (move to the right).`
4. `Set switch on MASTER COMMAND switch to ON (move to left):` `a. To zero audit totals (Functions
   01-11) set switch 8 to ON.` `b. To restore factory settings and zero audit totals, set switch 7
   to ON. Coin Door must remain open to restore factory settings.` `c. For Auto-Cycle Mode set
   switch 6 to ON.`
5. `Momentarily depress MASTER COMMAND ENTER pushbutton. The LEDs should blink once.`
6. `c. ... Each cycle of this mode sequences through display digits test, flashes all multiplexed
   lamps 64 times and pulses each solenoid.`

`Figure 1. Coin Door Diagnostic Switches` labels the coin-door `HIGH SCORE RESET`, `ADVANCE` and
`AUTO-UP / MANUAL-DOWN` switches. `Figure 2. Master Command Settings Switch` shows two eight-position
slide-switch banks beside two LEDs, a `MASTER COMMAND ENTER` pushbutton and a `DIAGNOSTIC`
pushbutton. On the upper bank the three positions nearest the top are labelled `ZERO AUDIT TOTALS`,
`RESTORE FACTORY SETTINGS` and `AUTO-CYCLE MODE`; the lower bank is labelled `NOT USED`.
