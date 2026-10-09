# Black Hole — Bookkeeping and self test (printed pages 12-13)

Source: the idoc.pub copy of the Gottlieb *Black Hole Instruction Manual* (document jlk9z9rz1545), viewer pages 14 and
15 (printed pages 12 and 13), section "VII. BOOKKEEPING AND SELF TEST"; the Scribd copy has the same pages. Quoted from
the page images; the flow chart's boxes are transcribed in order.

## Printed page 12 (section VII text)

"The circuitry in this game helps the operator perform many bookkeeping and game test functions. The information is
shown one step at a time in the first player's score display, while the step number is shown in the credit display
(refer to flow chart Section VII, C for order and function)."

A. Bookkeeping: "Pressing the SELF-TEST button inside the front door begins the bookkeeping which are steps 01 through
15." "The data in any of these steps may be reset to zero while it is displayed by pressing the replay button on the
front door." "THE SELF-TEST BUTTON MUST THEN BE PRESSED TO ENTER ZERO INTO MEMORY." "All bookkeeping information is
checked against itself to insure that it is correct. If any data is invalid or bad, that information will flash while
it is displayed." "If the SELF-TEST button is not pressed within 60 seconds of each step, the game will return to the
attract mode."

B. Self-test: "Steps 16 through 20 are SELF-TEST or game tests the operator can use for quick troubleshooting." "Each
test can be repeated by pressing the replay button on the front door. This starts the test for another 60 seconds."
"If the SELF-TEST button or the replay button is not pressed within 60 seconds, the game will return to the attract
mode."

## Printed page 13 (section VII, C. Flow chart)

Header boxes: "BOOKKEEPING CAN BE ENTERED IN THE ATTRACT MODE OR DURING GAME PLAY." / "Press SELF/TEST button on front
door. Credit display should read "00". Player score displays should be blank." / bookkeeping: "PRESS SELF/TEST BUTTON";
self/test: "PRESS CREDIT BUTTON".

Bookkeeping steps: 1 COINS THRU LEFT CHUTE; 2 COINS THRU RIGHT CHUTE/NOTE 1; 3 COINS THRU CENTER CHUTE/NOTE 2; 4 TOTAL
PLAYS; 5 TOTAL REPLAYS; 6 GAME PERCENTAGE/NOTE 3; 7 EXTRA BALLS; 8 TOTAL TILTS; 9 TOTAL SLAMS; 10 TIMES HGTD HAS BEEN
BEATEN; 11 FIRST HIGH SCORE LEVEL; 12 SECOND HIGH SCORE LEVEL; 13 THIRD HIGH SCORE LEVEL; 14 HIGH GAME TO DATE SCORE;
15 AVERAGE PLAYING TIME/NOTE 4.

Self-test steps:

- "STEP 16—LAMP DRIVER TEST: Q, T, U & L relays and coin lockout coil are pulsed. All controlled lamps, plus the ball
  gate and ball release, are sequentially turned on."
- "STEP 17—SOLENOID TEST: Specific controlled solenoids are pulsed while its assigned number appears in the status
  display. See NOTE A and NOTE B."
- "STEP 18—SWITCH TEST: All switches in the switch matrix are inspected. If all switches are open, "99" will appear on
  the status display. If one or more are closed, their assigned matrix number will appear in the display."
- "STEP 19—DISPLAY TEST: Each digit of each display is turned on individually, and all numbers, zero thru nine, are
  sequenced."
- "STEP 20—MEMORY TEST: Each control board memory device is inspected. Any defective device is indicated by its part
  number displayed in Player number one. If all are OK, 99 is displayed in status display. See NOTE C."
- "TO EXIT SELF/TEST: a) Wait 60 seconds b) Turn power off/on c) Open slam switch d) Close tilt switch"

"NOTE A: SOLENOID ASSIGNMENTS" as printed:

| No. | As printed |
| --- | --- |
| 1 | Drop Target Bank (4) Lower Playfield |
| 2 | Drop Target Bank (3) Lower Playfield |
| 3 | Outhole |
| 4 | Drop Target Bank (4) Upper Playfield |
| 5 | Drop Target Bank (5) Upper Playfield |
| 6 | Ball Gate |
| 7 | Capture Hole Lower Playfield |
| 8 | Capture Hole Upper Playfield |
| 9 | Kicker Lower Playfield |
| 10 | Outhole |
| 11 | Ball Gate |

"NOTE B: Mechanical coin counters are optional and are not pulsed during solenoid test."
"NOTE C: James Bond and later System 80 games will display 7641-1 for a bad 2716 game prom."
"NOTE D: FOR GERMAN GAMES ONLY, solenoid #4 is assigned to center coin chute and solenoid #7 is assigned to right coin
chute."

Footnotes 1-4: "1. If control board switch #14 is on, Steps 01 and 02 are added together and displayed in Step 01."
"2. IN GERMAN GAMES ONLY, Step 02 displays total coins thru center chute, and Step 03 displays total coins thru right
chute." "3. If Step 06 is reset, Steps 04 and 05 must also be reset." "4. If Step 15 is reset, Step 04 must also be
reset."

Note A does not agree with this manual's own driver-board and playfield schematics (pages 26 and 44), which wire
solenoid #1 to the upper 4-position bank, #2 to the upper 5-position bank, #5 and #6 to the lower 4- and 3-position
banks and #9 to the outhole; it is transcribed as printed.
