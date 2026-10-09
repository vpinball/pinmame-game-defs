# Diner — Operator text: ROM summary, game controls, game operation, status displays, game-feature adjustments, test/diagnostic procedures and maintenance (printed pages 1, 4, 6, 7, 8, 9, 19, 20, 21, 30-39)

Source: `Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf` (106 pages,
SHA-256 `da75ffb79e6d6b8d1b332ce65f93ee1486a5a7ff8d9060878f07a91438b573aa`). Pages read: PDF 5 (printed
"DINER 1"), 8 (4), 10 (6), 11 (7), 12 (8), 13 (9), 23 (19), 24 (20), 25 (21), 34 (30), 35 (31), 36 (32),
37 (33), 38 (34), 39 (35), 40 (36), 41 (37), 42 (38) and 43 (39). On every page read, the printed folio
equals the PDF page number minus 4; there is no page where it differs. All text was read from the rendered
150 dpi page images (the OCR text layer was not trusted); dense areas were cropped and enlarged before
reading.

Conventions used throughout. The game name is printed in a stylised outline logotype ("D I N E R") inside
running text and headings; it is written "DINER" here. Emphasis (bold, italic, underline) is not marked.
Line breaks inside paragraphs are joined, and hyphenation at line ends is rejoined (for example "Con-servative"
is written "Conservative"). Straight quotation marks and apostrophes are used for the printed typographic
single and double quotation marks. The printed star-shaped bullet used as an "operator-adjustable feature"
marker is written `*`.

The tables printed on pages in this range that are transcribed elsewhere are not repeated here: the Lamp-Matrix
Table (PDF 35, printed 31), the Solenoid Table with its notes (PDF 36, printed 32) and the Switch-Matrix Table
with its "BL = Bottom Left  BR = Bottom Right" legend (PDF 38, printed 34). Their position on each page is
noted below.

Pages in Section 1 that were not part of this transcription: PDF 6 and 7 (connector identification, circuit
boards, Figure 1 locations diagram), PDF 9 (assembly steps 1-6), PDF 14-22 (adjustment items 1-30 and the
pricing text), PDF 26-33 (special preset adjustments, pricing tables) and PDF 44 (fuse listing).

---

## ROM Summary (PDF 5, printed page 1)

The page is the Section 1 title page. Heading text: "Section 1", "Game Operation & Test Information". The
bullet list reads:

- "DINER (System 11C) ROM Summary"
- "Pinball Game Assembly Instructions"
- "Game Play"
- "Game Status Displays"
- "Game Adjustment Procedure"
- "Game Pricing"
- "Test/Diagnostic Procedures"

Table heading: "DINER (System 11C) ROM Summary".

| IC | DESCRIPTION | TYPE | IDENTIFIER | BOARD | PART NUMBER |
| --- | --- | --- | --- | --- | --- |
| Game ROM 1 | 32K x 8 ROM | 27256 | U27 | CPU | A-5343-571-2 |
| Game ROM 2 | 32K x 8 ROM | 27256 | U26 | CPU | A-5343-571-1 |
| Music/Speech ROM 1 | 64K x 8 ROM | 27512 | U4 | Audio | A-5343-571-3 |
| Music/Speech ROM 2 | 64K x 8 ROM | 27512 | U19 | Audio | A-5343-571-4 |
| Music/Speech ROM 3 | 64K x 8 ROM | 27512 | U20 | Audio | A-5343-571-5 |

NOTICE: "To order a replacement ROM from your authorized WILLIAMS ELECTRONICS GAMES distributor, specify: (1)
part number (if available); (2) ROM label color; (3) ROM level (number) on the label; (4) which game the ROM is
used in."

Footer folio: "DINER 1".

---

## DINER Game Control Locations (PDF 8, printed page 4)

"Figure 2 shows the locations of the following switches, except for the last one (CPU Diagnostic switch, which is
shown in the Backbox portion of Figure 1, along the left edge of the CPU Board)."

"The On-Off switch is on the bottom of the cabinet near the right front leg."

"The Volume Control is on the left inner wall of the cabinet on the tilt mechanisms board. It is accessible by
opening the coin box door."

"The Credit switch (also called the START button) is a pushbutton to the left of the coin door on the cabinet
exterior."

"GAME ADJUSTMENT/DIAGNOSTIC SWITCHES. DINER allows the operator to control all game adjustments, obtain
bookkeeping information, and diagnose problems, using only three switches mounted on the inside of the coin
door, along with the Credit button beside the coin door."

"ADVANCE, AUTO-UP/MANUAL-DOWN, and HIGH-SCORE RESET are the switches located on the inside of the coin door.
Refer to the text discussing Game Status Displays and the Test/Diagnostic Procedures for details concerning
button operation."

"The Memory Protect switch is on the inside frame of the coin door. This interlock switch must be open to clear
bookkeeping totals and to make game adjustments. It automatically opens, when the coin door opens."

"Figure 1 shows the location of the CPU Board switch (left edge of CPU Board, Backbox View)."

"The CPU Diagnostic switch (SW 2) is the switch mounted on the left edge of the CPU Board near a large, socketed
microprocessor chip. This switch initiates the Memory Chip Test explained in the Test/Diagnostic Procedures."

Figure 2 labels (text labels of the drawing, as printed):

- "27-1111 Memory Protect Interlock Switch"
- "A-8550-1 Volume Control Assembly" and, beside it, "& 47Ω Resistor 5010-10170-00" (the figure prints these
  as the lines "A-8550-1", "Volume & 47Ω Resistor", "Control 5010-10170-00", "Assembly")
- "B-6390 Front Molding"
- "Molding Latch Lever, p/o D-9174-1"
- "A-5069 START (Credit) Button"
- "Plumb Bob Tilt Assembly:" with the list:

| Part | Description |
| --- | --- |
| 01-3444 | Upper Tilt Bracket |
| 01-3445 | Lower Tilt Bracket |
| 12-6231 | Wire Hanger |
| 20-6502-A | Plumb Bob Weight |
| 4406-01120-00 | Wingnut, #6-32 |

- "27-1008 Game Adjustment/ Diagnostic Switches"
- "5640-10932-00 On-Off Switch"
- Caption: "Figure 2. Pinball Game Controls Locations"

Footer folio: "DINER 4".

---

## Pinball Game Assembly Instructions (Continued) and Game Operation: power-up (PDF 10, printed page 6)

Included because it states the ball count and the power-up routine. Heading: "PINBALL GAME ASSEMBLY
INSTRUCTIONS (Continued)".

"7. Unlock and open the coin door. Locate the Molding Latch Lever (shown in Figure 2), and move the lever toward
the left side of the game, to release the Front Molding. Lift the Front Molding off the playfield cover glass;
return the Latch Lever toward the right, and close the coin door. Carefully slide the glass downward, until it
clears the grooves of the Left and Right Side Moldings. Lift the glass up and away from the game, storing it
carefully to avoid breakage."

"8. Place a level or an inclinometer on the playfield surface. Adjust the leg levellers for proper playfield level
(side-to-side) and playfield pitch angle (incline) of approximately 6-7 degrees. NOTE: It is recommended that
these measurements be made ON the playfield, not the cabinet nor the playfield cover glass. Tighten the nut on
each leg leveller shaft to maintain this setting, as shown in Figure 3."

CAUTION: "Playfield pitch angle adjustments can affect the operation of the plumb bob tilt, inside the cabinet.
The plumb bob weight is among the parts in the cash box; the operator should install the weight and adjust this
tilt mechanism for proper operation, after completion of the desired playfield pitch angle setting."

"9. Move the game into the desired location; recheck the level and pitch angle of the playfield."

"10. Verify that the required number of balls are installed in the game. (DINER: Install 3 balls; however, only 2
are used in game play!)"

"11. Clean and reinstall the playfield cover glass, reversing the procedure of step 7. Prepare the game for
player operation."

Heading: "GAME OPERATION".

WARNING: "After assembly and installation at its site location, this game must be plugged into a properly
grounded outlet to prevent shock hazard, and to assure proper game operation. DO NOT use a 'cheater' plug to
defeat the ground pin on the line cord. DO NOT cut off the ground pin."

"POWERING UP. Perform the following 'power up' routine upon completion of the assembly and installation
procedure, as well as at the beginning of each period of game operation. Initially, it will confirm that the game
is in proper operating condition; later, it will aid the operator via its messages (refer to later text entitled
"Problem Analysis Messages")."

"Procedure. With the coin door closed, plug the game in, and switch it ON, using the On-Off switch. In normal
operation, the player 1 score display initially shows 00. Then, the game goes into the Attract Mode (playfield
and backbox lamps flashing, sounds being heard, etc., if the operator does not change the Factory Setting)."

"Open the coin door and press the AUTO-UP/MANUAL-DOWN switch to MANUAL-DOWN. Press the ADVANCE button to begin
the game test routine. Return to AUTO-UP and perform the entire test routine to verify that the game is
operating satisfactorily. Successful completion of the tests shows that the game is ready to begin earning your
investment return."

Footer folio: "DINER 6".

---

## Game Operation (Continued) (PDF 11, printed page 7)

"After the game has been on location for a period of time, the test routine may be preceded by messages
concerning game problems. The text entitled 'Problem Analysis Messages' at the end of the Text/Diagnostic
Procedures contains more details concerning messages displayed at each game turn-on."

"ATTRACT MODE*. Playfield and backbox lamps blink. The player score displays exhibit a series of messages
informing the player concerning:"

- "A. Recent highest scores*;"
- "B. A "custom message" ("YOU CAN EAT ... YOUR HEART OUT ... AT THE DINER")*;"
- "C. The score to achieve to obtain a Replay award*;"

"These (or similar) displays reappear occasionally, accompanied by sounds and music, until a player initiates game
play by inserting a coin or, when credits are available, pressing the START button."

"CREDIT POSTING. Insert coin(s). A sound is heard for each coin, and the player score displays show the number of
credits purchased. So long as the number of maximum allowable credits* are NOT exceeded by coin purchase or high
score, credits are posted correctly."

"STARTING A GAME. Press the START button once. A startup sound plays, and the Credit amount shown in the player
score display decreases by one. The upper Player Score Display flashes 00 (until the first playfield switch is
actuated), and the lower Player Score Display shows ball 1, except for 4-player games where the ball # shows in
the individual player's display. Additional players may enter the game by pressing the START button once for each
player, before the end of play on the first ball."

"TILT. Actuating the Slam Tilt switch on the coin door inside the cabinet ends the current game; DINER then
proceeds to the Game Over Mode. With the third closure* of the plumb bob tilt switch, the player loses the
remaining play of that ball, but can complete the game."

"END OF GAME. All earned scores and bonuses are awarded. If a player's final score exceeds the specified value,
the player receives a designated award for achieving the current highest score. A random digit set* appears in
the Match display. Credit* may be awarded, when the last two digits of any player's score display (1 through 4)
match the random digits of the Match display. Match, high score, and game over sounds are made, as appropriate."

"GAME OVER MODE. The GAME OVER display shows in the player score displays. Then, the high scores flash on the
appropriate player score displays. The game proceeds to the Attract Mode."

"* - operator-adjustable feature"

Footer folio: "DINER 7".

---

## DINER Game Status Displays (PDF 12, printed page 8)

"DINER provides the game owner/operator with a display of information concerning the game's bookkeeping and game
play feature adjustments. Basically, three classes of information now become available in this status display
mode: Id (Identification); Au (Audit); Ad (Adjustment). Each of the underscored two-letter abbreviations for these
classes appears in the Player Score Displays, while the system microprocessor for the DINER game is displaying
the items within each class."

Identification Information—Id

"With the game turned on, the coin door open, and the AUTO-UP/MANUAL-DOWN switch in the AUTO-UP position, the
operator can press the ADVANCE switch once, briefly. Player displays immediately change from the Attract Mode to
the Game Status Display or Identification (Id) Mode. This is evident by the following display, shown in columnar
form. The column headings refer to the two backbox displays."

| Upper Player Score Display | Lower Player Score Display |
| --- | --- |
| DINER | Id 00     571     L-x* |

"* x - indicates ROM revision level; e.g., 1 is initial issue; 2, 3, etc. for later revisions."

"The game is named in the upper Player Score display. The game's identification number, the ROM revision level,
and the Id Mode stage (Id 00) shows in the Lower Player Score display."

"Pressing ADVANCE once more causes the Id 01 display to appear. This display describes the installed software
more fully; that is, country; development stage; date of revision."

"Pressing ADVANCE once more causes the Id 02 display to appear. This display describes which of the "Install"
options is currently in effect. For example, if the YES option of the INSTALL FACTORY Adjustment Item (Ad 68) was
last selected, FACTORY SETTING appears on the player score displays. Changing the setting of any other game
adjustment item, after selecting the YES option for Ad 68 causes the display to change to FACTORY ALTERED.
Similarly, if the operator selects the YES option for INSTALL HARD (Ad 65), the display indicates HARD SETTING.
Changing a game adjustment item later then causes the display to show HARD ALTERED."

Audit Information—Au

"While the AUTO-UP switch remains in the Up position, the operator can press the ADVANCE switch once, briefly, to
begin the backbox displays of Audit (sometimes called "bookkeeping") Information. Fifty-four audit entries are now
available. Calculation of the various factors is no longer necessary because the System 11C game program now
performs all the mathematical factor computations. This information is intended to aid the owner/operator in
evaluating how the game is performing in each location, by providing knowledge about which game features are
receiving the most play. With this information, the owner/operator can determine whether adjusting the game
features to other settings will contribute to increased game earnings."

"The operator can press the ADVANCE button once to view each Audit Information display item. To proceed more
rapidly through this information, the operator only has to press and hold the ADVANCE button. If a desired item is
passed, the operator can use the MANUAL-DOWN switch position with the ADVANCE button to back up to the desired
item."

"The DINER Audit Table lists the 54 Audit Items of the DINER Game Status Displays. Presentation of these Audit
Items again utilizes the player score displays: The Audit Item entry appears in the lower Player Score Display
accompanied by the Item's data, while the upper display shows the Item description. A few example entries are
shown in the table. Detection of erroneous data affecting any of the counters used in these audit items causes the
message, ERROR, to be displayed during display of any audit item associated with that particular counter. (The
program does not analyze the cause of the error; it merely alerts the operator of the error's existence by the
message.)"

Footer folio: "DINER 8".

---

## DINER Audit Table (PDF 13, printed page 9)

Included beyond the requested page list because its descriptive phrases name game features (Rush, Dine-Time,
Grill, Cup, E-A-T lanes, Multi-Ball, drains). Page heading: "DINER GAME STATUS DISPLAYS (Continued)"; table
title: "DINER Audit Table". Column headings: "Audit Item (Lower)" | "Descriptive Phrase (Upper Display)" | "Audit
Item Value^1 (Lower Display)". Items are printed "AU 01" for the first row and bare numbers below it. A vertical
rule from the Value column's left edge runs down through the right-hand part of several long phrases (rows 17,
37 and 38, 40 and neighbours); it is a ruling artifact, not text.

| Audit Item | Descriptive Phrase | Audit Item Value |
| --- | --- | --- |
| AU 01 | LEFT COINS [chute next to coin door hinge] | 432 |
| 02 | CENTER COINS | 0 |
| 03 | RIGHT COINS | 398 |
| 04 | PAID CREDITS | 830 |
| 05 | TOTAL PLAYS | (blank) |
| 06 | TOTAL FREE (Total Free Plays) | (blank) |
| 07 | PERCENT FREE (% Free Plays) | (blank) |
| 08 | REPLAY AWARDS | (blank) |
| 09 | PERCENT REPLAY (% Replay Awards) | (blank) |
| 10 | SPECIAL AWARDS | (blank) |
| 11 | PERCENT SPECIAL (% Special Awards) | (blank) |
| 12 | MATCH AWARDS | (blank) |
| 13 | HSTD ( High Score to Date) CREDITS | (blank) |
| 14 | PERCENT HSTD (% HSTD Credits) | (blank) |
| 15 | EXTRA BALLS | (blank) |
| 16 | PERCENT EX. BALL (% Extra Balls) | (blank) |
| 17 | AV. BALL TIME (Average Time in Seconds) | (blank) |
| 18 | MINUTES OF PLAY (Minutes of Play) | (blank) |
| 19 | BALLS PLAYED | (blank) |
| 20 | REPLAY1 AWARDS | (blank) |
| 21 | REPLAY2 AWARDS | (blank) |
| 22 | REPLAY3 AWARDS | (blank) |
| 23 | REPLAY4 AWARDS | (blank) |
| 24 | 1 PLAYER GAMES | (blank) |
| 25 | 2 PLAYER GAMES | (blank) |
| 26 | 3 PLAYER GAMES | (blank) |
| 27 | 4 PLAYER GAMES | (blank) |
| 28 | BURN IN CYCLES | (blank) |
| 29 | MULTIBALLS ( # of Multi-Ball™ plays) | (blank) |
| 30 | RUSH AWARDS (# of "Rush" awards) | (blank) |
| 31 | DINE TIME AWARDS (# of "Dine-Time" awards) | (blank) |
| 32 | 1,500,000 GRILL (# of 1.5Mil awards via Grill) | (blank) |
| 33 | CUP AWARDS (# of 'CUP' plays) | (blank) |
| 34 | EAT COMPLETE (# of completions of E-A-T lanes) | (blank) |
| 35 | Not Used | (blank) |
| 36 | Not Used | (blank) |
| 37 | CONSOL. EX. BALLS (# of Consolation Extra Balls Awarded) | (blank) |
| 38 | EARNED EX. BALLS ( # of 'Earned' Extra Balls) | (blank) |
| 39 | H.S.RESET COUNTER | (blank) |
| 40 | 0.0-0.4 MIL. SCORE (# of games <500K) | (blank) |
| 41 | 0.5-0.9 MIL. SCORE (# of games ≥500K, <1M) | (blank) |
| 42 | 1.0-1.4 MIL. SCORE (# of games ≥1M, <1.5M) | (blank) |
| 43 | 1.5-1.9 MIL. SCORE (# of games ≥1.5M, <2.0M) | (blank) |
| 44 | 2.0-2.9 MIL. SCORE (# of games ≥2.0M, <3.0M) | (blank) |
| 45 | 3.0-3.9 MIL. SCORE (# of games ≥3.0M, <4.0M) | (blank) |
| 46 | 4.0-4.9 MIL. SCORE (# of games ≥4.0M, <5.0M) | (blank) |
| 47 | 5.0-5.9 MIL. SCORE (# of games ≥5.0M, <6.0M) | (blank) |
| 48 | 6.0-6.9 MIL. SCORE (# of games ≥6.0M, <7.0M) | (blank) |
| 49 | 7.0-7.9 MIL. SCORE (# of games ≥7.0M, <8.0M) | (blank) |
| 50 | 8.0-99.9 MIL. SCORE (# of games ≥8.0M, <100M) | (blank) |
| 51 | AV. MIN. GAME TIME (Average Game in Minutes) | (blank) |
| 52 | LEFT DRAINS (# of drains via Left Outlane) | (blank) |
| 53 | RIGHT DRAINS (# of drains via Right Outlane) | (blank) |
| 54 | MINUTES ON | (blank) |

"NOTE: 1. The numbers shown in this column for Items 1 through 4 are examples. Entries for all items depend on
the amount of play; thus, they will vary from location to location."

Footer folio: "DINER 9".

---

## Game Adjustment Procedure (Continued): items 33-38 (PDF 23, printed page 19)

Included beyond the requested page list because items 33-38 describe game features. Page heading: "GAME
ADJUSTMENT PROCEDURE (Continued)". Items 31 and 32 on the same page (1/2 price buy-in and % extra balls per game)
are pricing/extra-ball-percentage adjustments and are not transcribed.

"33 EX. BALL LIT MEMORY
The operator can choose (via the START button) whether any lighted Extra Ball lamps are retained in memory for
'Next Ball' play. The choices are:"

- "Yes - Lighted Extra Ball lamps are retained in memory for 'Next Ball' play."
- "No - Lighted Extra Ball lamps are NOT retained in memory for 'Next Ball' play."

"34 SPOT MULTIBALL
The operator can choose (via the START button) whether a shot into TODAY'S SPECIAL (Sub-Playfield Shooter
Assembly) starts Multi-Ball play, when the first ball is locked under the left Elevator Ramp. The choices are:"

- "Yes - Multi-Ball play starts with a Today's Special shot."
- "No - Player must earn Multi-Ball in the usual manner."

"35 RUSH TIMER
The operator can choose (via the START button) the time period for making the two RUSH shots to light the RUSH
lamps. (During 2-ball Multi-Ball play, while the RUSH lamps are lighted, all Left and Right Ramp shots score
500,000 points.) The range of setting is 4 Seconds (Conservative) through 25 Seconds (Liberal). This adjustment
cannot be turned off."

"36 NOT USED"

"37 CUSTOMER MEMORY
The operator can choose (via the START button) whether the number of customers lighted (via drop target bank
completions) is retained in memory for 'Next Ball' play. The choices are:"

- "Yes - Lighted Customer lamps are retained in memory for 'Next Ball' play."
- "No - Lighted Customer lamps are NOT retained in memory for 'Next Ball' play."

"38 FOOD ITEM MEMORY
The operator can specify (via the START button) whether lighted Food Items are retained in memory for 'Next Ball'
play. The choices are:"

- "Yes - Food Items ARE retained in memory for 'Next Ball' play."
- "No - Food Items are NOT retained in memory for 'Next Ball' play ."

Footer folio: "DINER 19".

---

## Game Adjustment Procedure (Continued): items 39-45 (PDF 24, printed page 20)

Page heading: "GAME ADJUSTMENT PROCEDURE (Continued)".

"39 TODAY'S SPECIAL
The operator can choose (via the START button) the operating conditions for the TODAY'S SPECIAL feature. A shot
into Today's Special obtains a random of one of the following: Mystery Score, Extra Ball, Advance Dine-Time,
Start Multi-ball, and Spot Customer. The choices are:"

- "Ex. Easy - Always on during single ball (Not Multi-ball) play."
- "Easy - On at each ball start and relighted via Left Return lane with no timer."
- "Medium - On at each ball start and relighted via Left Return WITH timer."
- "Hard - On at first ball start and relighted via Left Return WITH timer."
- "Ex. Hard - Off at each ball start and relighted via Left Return WITH timer."

"40 E - A - T LANE MEMORY
The operator can choose (via the START button) whether lighted E - A - T lane lamps are retained in memory for
'Next Ball' play. The choices are:"

- "Yes - Lighted E - A - T lane lamps ARE retained in memory for 'Next Ball' play."
- "No - Lighted E - A - T lane lamps are NOT retained in memory for 'Next Ball' play."

"41 NOT USED"

"42 CASH REG. RAMP
The operator can choose (via the START button) the time period that the player has to make the next Cash
Register (left) Ramp shot to advance the Cash Register value. The range of settings is 5 Seconds (Conservative)
- 20 Seconds (Liberal), and 0, for Off."

"43 DINER RAMP
The operator can choose (via the START button) the difficulty associated with operating the diverter to 'open'
the cup and lighting Lock 1. By spelling D-I-N-E-R, the player raises the Cash Register Ramp to 'lock' a ball,
and 'opens' the Cup for the Cup Bonus shot. The choices are:"

- "Ex. Easy - First shot always lights Lock 1 and 'opens' the Cup. D-I-N-E-R always stays lighted."
- "Easy - Game starts with D-I-N-E-R lighted. After the Cup Bonus is awarded, only D-I-N will be lighted."
- "Medium - Game starts with D-I-N-E-R lighted. After the Cup Bonus is awarded, the player must spell D-I-N-E-R to
  'open' the Cup."
- "Hard - Game starts with D-I-N lighted. After the Cup Bonus is awarded, the player must spell D-I-N-E-R to
  'open' the Cup."
- "Ex. Hard - The player must always spell D-I-N-E-R."

"44 & 45 NOT USED"

Footer folio: "DINER 20".

---

## Game Adjustment Procedure (Continued): items 46-50 (PDF 25, printed page 21)

Page heading: "GAME ADJUSTMENT PROCEDURE (Continued)".

"46 TOP EJECT AWARD
The operator can choose (via the START button) whether the Top Left Eject awards are available via a shot from
the Sub-Playfield Shooter. The choices are:"

- "Yes - (Liberal) Awards are available via a shot from the Sub-Playfield Shooter."
- "No - (Conservative) Awards are NOT available via a shot from the Sub-Playfield Shooter."

"47 CONSOL. BALL TIME
The operator can choose (via the START button) the time period that causes the award of a Consolation Extra
Ball. This Consolation Extra Ball enables less-skilled players to enjoy the game. The range of this setting is 0
(No Consolation Extra Ball play is allowed), and 1 Second (Conservative) through 99 Seconds (Liberal)."

"48 ATTRACT SOUNDS
The operator can choose (via the START button) whether the Attract Mode sounds occur. The choices are:"

- "On - Sounds ARE heard during the Attract Mode."
- "Off - Sounds are NOT heard during the Attract Mode."

"49 CUSTOM MESSAGE
The operator can choose (via the START button) whether to display a message during the Attract Mode. (When
display of a message is selected, the operator can either utilize the message provided or change the message.)
Three choices are available:"

- "1 - Display a message during the Attract Mode. The lower display shows this choice as ON. The 3-line message
  provided is: YOU CAN EAT ... YOUR HEART OUT ... AT THE DINER."
- "2 - Do NOT display a message during the Attract Mode. (Lower display shows OFF.)"
- "3 - The lower display shows this choice as CHANGE. The operator can enter a special ("custom") message, as
  follows:"
  - "A. Press ADVANCE once. The operator can now enter as many as three 16-character lines for display during the
    Attract Mode."
  - "B. Use the flipper button(s) to select each message character (alphabet, numbers, and special symbols are
    available). In case of error, enter a "back arrow" (just before "space") to correct, followed by correct
    character. For a period after any letter, use letters with periods (following the special symbols). The
    entire character set is the following:"

    `A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 < > ? - / * '`

    `A. B. C. D. E. F. G. H. I. J. K. L. M. N. O. P. Q. R. S. T. U. V. W. X. Y. Z. _`

  - "C. Move to the next character via the Credit button. The game program does not allow entirely blank lines to
    be displayed."

"50 DISPLAY AU 01 - 04
The operator can choose (via the START button) how to display the coinage audit information, Au 01 - 04. No
information is lost; it remains stored in the CPU memory. The information is now available for readout via the
player score displays. Three choices are available:"

- "Yes - Both the audit text (slot identification) and the value is displayed."
- "Nbr - Only the numerical value is displayed."
- "No - NO display occurs."

Footer folio: "DINER 21".

---

## Test/Diagnostic Procedures: introduction, Music Test, Display Test, Sound Test (PDF 34, printed page 30)

Page heading: "TEST/DIAGNOSTIC PROCEDURES".

"WILLIAMS ELECTRONICS GAMES also provides a series of diagnostic tests to aid the operator in determining game
condition (that is, whether the game's features and highlights are operating satisfactorily). These tests activate
virtually all the electronic and electromechanical devices comprising the game, so that the operator can readily
locate a malfunctioning device or simply verify that all devices are working properly. In order, these tests deal
with the music, the displays, the game sounds, the lamps, the solenoids, and the switches."

"In addition to the diagnostic testing, a feature called the Auto Burn-in Mode is available. Activating this mode
enables the operator to observe the game while all of the diagnostic tests, except the switch tests, occur. This
can be very helpful in locating 'intermittent' problems."

"Activating either the entire test series or one of the individual tests requires use of the Game Adjustment/
Diagnostic switches. Open the coin door for access to these switches. To proceed to the Diagnostic Tests, the
operator must simply switch the game On, set the AUTO-UP/MANUAL- DOWN switch to MANUAL-DOWN, and press the
ADVANCE button."

CAUTION: "The System 11C game program greatly aids the operator and service personnel: At the beginning of the
Test/Diagnostic Procedures (and also at game Turn-On), the player score displays now signal, with a message
("Press ADVANCE for Report") that the game program has detected a problem that affects game play. Messages for
DINER include "Check Switch ##", "Pinball Missing", etc. Refer to the text on Problem Analysis Messages at the
end of the Test/Diagnostic Procedures for more details concerning the messages' meaning. To proceed with the
Test/ Diagnostic Procedures, use AUTO-UP, and press ADVANCE."

"MUSIC TEST."

"1. In the Music Test, observe that the upper displays show the message, MUSIC TEST. Switching to AUTO-UP,
observe that the message now reads MUSIC OFF, and that the lower display shows 00 00. Press the Credit button to
select the desired music selection: 01 through 07 (the selections repeat). Adjust the volume control for proper
sound level for the game location."

"2. Use the AUTO-UP position."

"DISPLAY TEST."

"1. To initiate the Display Test, press ADVANCE. Observe that upper display briefly shows the message, DISPLAY
TEST, and that the lower display shows 01 (the Display Test identifier)."

"2. Use AUTO-UP. Observe that all displays begin a display cycle of all 0s through all 9s, one digit at a time.
Verify that the proper comma segments light during display of the odd-numbered digits. Next, a special "all
segments" character 'walks' from left to right across each player score display."

"3. To halt the display cycle, use MANUAL-DOWN. Then, press ADVANCE to step through the sequential digit display,
digit by digit, and the subsequent "all segments" characters display test. Use AUTO-UP to resume cycling, and to
proceed to the next test."

"SOUND TEST."

"1. (From Display Test) To initiate the Sound Test, press ADVANCE. Observe that the upper displays show the
message, SOUND TEST, and that the lower display shows 02 (the Sound Test identifier). The lower display shows a
series of test steps from 00 through 07."

"2. To repeatedly pulse a single sound, use MANUAL-DOWN. Verify that one particular sound repeats. Press ADVANCE
to step to the next sound, which repeats until ADVANCE is pressed again. Use AUTO-UP to resume cycling the
sounds, and to proceed to the next test."

Footer folio: "DINER 30".

---

## Test/Diagnostic Procedures (Continued): Lamp Tests (PDF 35, printed page 31)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)".

"LAMP TESTS."

"1. All Lamps.
(From Sound Test) To initiate the first Lamps Test, press ADVANCE. Observe that the upper displays show the
message, ALL LAMPS, and that the lower display shows 03 (All Lamps Test identifier) and that all feature lamps
(playfield and backbox) blink on and off. (Note, however, that the General Illumination lamps remain lighted
steadily.) To locate the wiring associated with a particular feature lamp, refer to the Lamp-Matrix Table. CPU
Board connections at jacks 1J6 (columns) and 1J7 (rows) are also listed in the table."

"2. Single Lamps.
From the All Lamps test, using AUTO-UP, press ADVANCE to initiate the Single Lamps Test. The upper displays
initially show the message, SINGLE LAMPS, and the lower display shows 04. Then, the lower display shows 04 01, and
the upper displays change to show "W", the name of the lamp currently blinking. Press the START button to proceed
through an ascending series of designator numbers (01 through 64), with the upper displays showing the
individual lamp's name. (To proceed through a descending series of lamp identifiers, use MANUAL-DOWN.) Press and
hold the START button to proceed rapidly to the desired lamp."

The "DINER Lamp-Matrix Table" (with its legend "BR = Bottom right; BL = Bottom Left  ○ = Multiple Lamps") fills
the lower part of this page; it is not repeated here.

Footer folio: "DINER 31".

---

## Test/Diagnostic Procedures (Continued): Solenoid Test (PDF 36, printed page 32)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)".

"SOLENOID TEST."

"1. (From Lamp Test) Using AUTO-UP, press ADVANCE. Observe that the upper display shows the message, COIL TEST,
the lower display shows 05 (Solenoid Test identifier). Next, the lower display shows a series of test steps from
01 through 27, while the upper display shows the solenoid/circuit name. During each of these steps, pulsing of
the respective solenoid/circuit occurs. The test cycles repeatedly, unless halted via the MANUAL-DOWN switch.
Refer to the Solenoid Table for solenoid numbers and wiring information. CPU Board connections at 1P11, 1P12, and
1P19 are also listed in the table."

"To continuously pulse a single solenoid/circuit, use MANUAL-DOWN. Press ADVANCE to sequence through the
switched, controlled, and special solenoids. Use AUTO-UP to resume test cycling, and to proceed to the next
test."

The "DINER Solenoid Table" and its numbered notes fill the rest of this page; it is not repeated here.

Footer folio: "DINER 32".

---

## Test/Diagnostic Procedures (Continued): solenoid on-state logic, A/C select relay (PDF 37, printed page 33)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)". The upper half holds two circuit diagrams; their text
labels, as printed, are listed. Waveform pulse shapes, resistors, grounds and connector symbols carry no text.

Left diagram, title: ""On" State Logic - Special Solenoid". Labels: "From PIA"; "7407"; "+5V" (three times, at the
three supply arrows); "7402"; "Spl Sol. Trigger"; "1J18"; "Low, with flippers enabled"; "2N 4401"; "TIP 122";
"Sol. B+"; "+25V"; "1J19"; "Special Solenoid "ON"".

Right diagram, title: ""On" State Logic - Controlled Solenoid". Labels: "From PIA"; "BLANKING" (printed with an
overbar); "7408"; "+5V" (two times); "2N 4401"; "TIP 122"; "Sol. B+"; "+25V"; "1J19"; "Cntrld Solenoid "ON"".

Beneath the diagrams (left): "Off" State - Special Solenoid:" (the opening quotation mark is not printed in this
heading)
"The Special Switch Trigger Input goes low. Meanwhile, the PIA line remains high. The remaining signals reverse
their states."

Beneath the diagrams (right): ""Off" State - Controlled Solenoid:"
"The Enable Input (from the PIA) goes low. Meanwhile, the BLANKING signal remains high. The rest of the signals
reverse their states."

"NOTE
As directed by the game program, the Solenoid A/C Select Relay (solenoid 12) switches the solenoid B+ power
between two power busses to permit actuating two groups of solenoids at the proper times. In its de-energized
state, the Relay connects the 'circuit A power' to 16 "controlled" and "switched" solenoids (identified in the
table with no suffix letter or the letter A, after the solenoid number). Individual solenoid operation then
depends on the game program enabling the ground path for solenoid actuation via the driver transistor associated
with each solenoid circuit. For example, the game program can actuate the Outhole Kicker solenoid (sol. 01A), via
the driver transistor Q33."

"When the game program determines that the Solenoid A/C Select Relay (sol. 12) must be energized, the relay
connects 'circuit C power' to eight group C solenoids (01C through 08C). Now, driver transistor Q33 can actuate
the Haji Flash circuit (sol. 01C). Using this "multiplexing" technique, the same driver transistor can control
actuation of two separate (A side and C side) solenoid circuits."

Figure 4 (text labels of the drawing, as printed): "System 11C CPU Board D-11883"; "1J11-1"; "Gry-Brn"; "Q33";
"Driver, Sol. 1, A & C"; "1J12-5"; "Brn-Yel"; "Q8 ckt"; "Driver, Sol. 12"; "part of Aux Pwr Driver Bd D-12247";
"5J1-9"; "D1"; "+25V"; "D46"; "D45"; "5J5-9"; "Blk-Brn" (twice, either side of the resistor); "part of Master
Interconnect Bd D-12313-571"; "R1=5.6Ω"; "Sol. 12"; "5"; "3"; "1"; "W1"; "K1"; "D23"; "A"; "B"; "5J2-5"; "5J4-9";
"F2C 5A, S-B"; "F2A 2.5A, S-B"; "5J11-1"; "Orn"; "5J11-5"; "Vio-Brn"; "Brn"; "Sol. 01A Outhole Kicker"; "Sol. 01C";
"#89 & #906 Bulbs"; "FL"; "Haji Flash".

Caption: "Figure 4. Typical Solenoid A/C Select Relay Circuit, showing the function of Solenoid 12, the Solenoid A/C
Select Relay."

Footer folio: "DINER 33".

---

## Test/Diagnostic Procedures (Continued): Switch Levels Test (PDF 38, printed page 34)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)".

"SWITCH TESTS."

"1. Switch Levels.
(From Solenoid Test) To initiate the Switch Levels Test, press ADVANCE. Observe that the upper display shows the
message, SWITCH LEVELS, and the lower display shows 06 (Switch Levels Test identifier). Normally, the right
portion of the lower display remains blank, indicating that no switch is actuated."

"If, however, a switch is actuated (possibly stuck closed), the lower display shows that switch's number, while
the upper displays indicate the switch's name. A sound also accompanies the displays. (This is another facet of
the DINER game program's switch testing capability.) If more than one switch is closed, a series of displays show
each actuated switch's name and number."

"(In addition, either of these problems could result in the reporting of a switch problem (or problems) at game
Turn-On or at the beginning of Diagnostic Tests.)"

"As soon as the operator opens a closed switch, its name and number are eliminated from the Switch Levels display
series. For DINER, switch numbers can range from 01 through 64. Refer to the Switch-Matrix Table for switch
numbers and wiring information. CPU Board connections at jacks 1J8 (columns) and 1J10 (rows) are also listed in
the table."

The "DINER Switch-Matrix Table" (with its legend "BL = Bottom Left  BR = Bottom Right") follows here on the
page; it is not repeated here.

"Row Problems. If a display of two (or more) switch numbers of a row occurs, although only one switch is closed,
check for a short circuit between the column wires."

"Multiple Switch Number Indications. Check the associated column wire for a short circuit to ground."

"Column Problems. If display of two (or more) switch numbers in a column occurs (while only one switch is
actuated), check for a short circuit between the row wires."

"Use AUTO-UP to proceed to the next test."

Footer folio: "DINER 34".

---

## Test/Diagnostic Procedures (Continued): Switch Edges, C-Side Test, Wheel Test (PDF 39, printed page 35)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)". Sub-heading: "SWITCH TESTS (Continued)."

"2. Switch Edges.
From the Switch Levels Test, press ADVANCE. Observe that the upper display shows the message, SWITCH EDGES; the
lower display shows 07 (Switch Edges Test identifier). The right portion of the lower display is blank,
indicating that no switch is actuated."

"This test permits the operator to test whether actuating a switch provides the proper signal to the System 11C
switch testing program. When actuating a switch, the operator should see the switch's name and number in the
displays. If no indication appears at the time the switch is actuated, the operator then knows that there is a
malfunction associated with that switch."

"Using this technique, the operator can test each switch appearing in the DINER switch problem reporting displays
(either at game Turn-On or at the beginning of the Diagnostic Tests) to determine whether the switch can be
actuated. If the switch's name and number are displayed while the operator checks its operation, the operator
then knows that the reported problem with that switch is NOT currently caused by a switch malfunction. The
operator can then seek other causes for the reported problem, being almost certain now that the switch did not
fail. This test is also useful when the operator is adjusting the sensitivity of a particular switch's actuation
mechanism."

"Among the possibilities is the fact that the players have not actuated that switch because of some other
problem; the operator should try to analyze what could cause the switch to be missed during game play, and
remedy that problem cause. With these new tests, switch problems are, therefore, more easily isolated."

"3. Playfield or CPU Board? To determine whether a switch problem is in the playfield or the CPU Board, remove
connectors 1P8 and 1P10 from the CPU Board. Begin the Switch Test. Use a jumper wire to simulate switch
actuation. For example, placing a jumper between 1J10-9 and 1J8-2 should (based on the Switch-Matrix Table)
should produce an indication of switch 09 being actuated."

"C-SIDE TEST
From the Switch Test, press ADVANCE. Observe that the upper display shows a message, C-SIDE TEST, and that the
lower displays shows 08 (C-Side Test identifier). This test confirms that Solenoid A/C Select Relay (Sol. 12)
does alternate between the "A" and "C" sides of the circuitry."

"The upper display then changes to show the 'side' of the circuit being tested, alternating between "SELECTED
A-SIDE' and "SELECTED C-SIDE", while the lower display shows the state of the C-Side Switch. While the "SELECTED
C-SIDE" test is occurring, when the C-Side Switch closes, the lower display shows "C-SIDE". When the "SELECTED
A-SIDE" message appears, the word "Err" appears in the lower display to indicate that there is no electrical
connection from the C-Side to the A-Side. The message "Err" also appears whenever the C-Side Switch is not
operating properly. Causes of improper operation can be: (1) blown fuses (F8 or F2C) or a faulty relay on the Aux
Pwr Driver Board; (2) failure of the 12- or 24-volt power circuits; (3) a switch matrix failure; or (4) faulty
connections between the circuit boards in the game's backbox (CPU Board, Aux Power Driver Board, Backbox
Interconnect Board). To halt the A/C Relay's operational test, press MANUAL-DOWN and press ADVANCE to activate the
A/C Relay manually."

"WHEEL TEST (Backbox DINE-TIME Clock)
From the C-Side Test, press ADVANCE. Observe that the upper display shows the message, WHEEL TEST, and the the
lower display shows 09 (Wheel Test identifier). Use AUTO-UP to automatically test the DINE-TIME Wheel (backbox
clock). The clock hand moves to '12 o'clock' position (lower display shows 001), and then moves clockwise
step-by-step, until it reaches '11:59' (lower display shows 191). The clock hand then travels all the way around
the clockface to begin the "pendulum test" at the 001 position. From 001, the hand moves to 191, then reverses to
021, forward to 181, reverses to 031, forward to 171, etc., until it reaches position 111, completing the entire
test cycle. It then begins the cycle again. Any detected errors will appear in the display."

Footer folio: "DINER 35".

---

## Test/Diagnostic Procedures (Continued): Wheel Test continued, ending the tests, Auto Burn-in, Memory Chip Test (PDF 40, printed page 36)

Page heading: "TEST/DIAGNOSTIC PROCEDURES (Continued)".

"WHEEL TEST (Backbox DINE-TIME Clock) (Continued)
To test the DINE-TIME Wheel manually, use MANUAL-DOWN. Then, pressing the right flipper switch moves the wheel
one position clockwise (1/10 of a step), and pressing the left flipper switch then moves the wheel
counterclockwise one position. Pressing ADVANCE causes the wheel to move clockwise completely around to the next
step."

"ENDING THE DIAGNOSTIC TESTS.
To end the Diagnostic Tests, reach the Wheel Test (09 in the lower display), use AUTO-UP and press ADVANCE. The
backbox displays should show the DINER game's Identification Information (the Id 00 screen). Use MANUAL-DOWN, and
press ADVANCE to reach Adjustment Item 70 (Clear Coins). Use AUTO-UP, and press ADVANCE to go to the Attract
Mode."

"AUTO BURN-IN MODE.
The Auto Burn-in Mode permits the operator to check intermittent (or nonrecurring) problems associated with most
portions of the game's circuitry. Repeatedly cycling through a group of tests can sometimes bring a problem,
which occurs only randomly or occasionally, to exhibit itself more frequently, thereby aiding in the isolation of
the problem. To activate the Auto Burn-in Mode:"

"1. While in the Game Adjustments, reach Ad 67 and change the Factory Setting of NO to YES, via the Credit
button. Set the AUTO-UP/MANUAL-DOWN switch to AUTO-UP."

"2. Press ADVANCE to start the Auto Burn-in Mode. This mode repeatedly sequences through the Music Test, the
Display Test, the Sound Test, the All Lamps portion of the Lamp Test, and the Solenoid Test."

"3. To halt the Auto Burn-in Mode, switch the game Off and then On. DINER now starts in the Attract Mode. (If a
switch problem is now reported by the displays, perform the Switch Tests again to determine the nature of the
problem; then, perform necessary repairs.)"

"SYSTEM 11C MEMORY CHIP TEST.
A new feature is now included in the Memory Chip Test for System 11C. During power-up, the CPU performs a
self-testing routine. When all tests are satisfactory, the game proceeds to the Attract Mode, allowing players to
use the game. Whenever a portion of the testing does not produce satisfactory results, the game displays a
message, before proceeding to the next portion of the testing. ONLY after all tests are satisfactory does the game
allow play to begin."

"In addition to the displayed message, when any part of the self-test routine fails, LED2 ('DIAGNOSTIC'), mounted
on the CPU Board, can be observed to determine the probable cause of the problem. This LED blinks, or flashes, a
certain number of times to identify the probable cause, as described in the CPU LED Indicator Codes Table. The
operator can also start the self-test routine by pressing the CPU Diagnostic Switch (SW 2) on the edge of the CPU
Board."

Footer folio: "DINER 36".

---

## CPU LED Indicator Codes Table and System 11C Sound Circuitry Tests (PDF 41, printed page 37)

Table title: "CPU LED Indicator Codes Table". Spanning heading: "Diagnostic LED". Column headings: "Blinks/
Flashes" | "CPU Problem" | "Explanation".

| Blinks/Flashes | CPU Problem | Explanation |
| --- | --- | --- |
| 1 | U25 RAM FAILURE | U25 RAM could not be used properly (NO other tests are performed; the game is locked here, until the game is turned off). |
| 2 | MEM. PROT. FAILURE | This message means that (A) the Coin Door may be shut; (B) the Memory Protect Switch may be stuck in the ON position; (C) the memory protect logic is protecting the memory; or (D) a U25 RAM failure is occurring. (See Note 1) |
| 3 | U51 PIA FAILURE | U51 has a malfunction. (See Note 2) |
| 4 | U38 PIA FAILURE | U38 has a malfunction. (See Note 2) |
| 5 | U41 PIA FAILURE | U41 has a malfunction. (See Note 2) |
| 6 | U42 PIA FAILURE | U42 has a malfunction. (See Note 2) |
| 7 | U54 PIA FAILURE | U54 has a malfunction. (See Note 2) |
| 8 | U10 PIA FAILURE | U10 has a malfunction. (See Note 2) |
| 9 | IRQ FAILURE | IRQ has a malfunction. It may be missing or too fast or too slow. |
| 10 | U27 ROM FAILURE | U27's internal checksums do not match. It may be a ROM failure, or its associated connections and connectingdevices are causing it to appear to have a problem. (The following U26 test is skipped.) |
| 11 | U26 ROM FAILURE | U26's internal checksums do not match. |

"Notes: 1. This test assumes that the Coin Door is OPEN; it is initiated ONLY by pressing the CPU Diagnostic
Switch (SW2)."
"2. Alternatively, its associated connections or connecting devices are causing the IC to appear to have
problems."

In row 10 the word "connectingdevices" is printed as one word (no space).

Below the table, heading "TEST/DIAGNOSTIC PROCEDURES (Continued)":

"SYSTEM 11C SOUND CIRCUITRY TESTS.
Testing of the System 11C Sound circuitry, including the Audio Board, is possible only after successful
completion of the System 11C Memory Chip Test."

"Audio Board Test. The game program conducts a brief check of the Audio Board (D-11581) circuitry at game
Turn-on; the game program reports the test results by brief sounds, as follows: No sound = Audio Board is not
operating, or a failure is affecting the sound circuitry (broken cable; dead amplifier; etc.); 1 sound = system
OK; 2 sounds = RAM problem; 3 sounds = U4 problem; 4 sounds = U19 problem; 5 sounds = U20 problem."

"NO SOUND DURING THIS TEST (but sound can be heard during the Diagnostic Tests).
Check the -12 V supply voltage on the Audio Board. If this -12V dc voltage is low (or AC ripple seems too high),
perform the following checks:"

- "1. The gray and gray-green transformer secondary wires for 19.4 V ac."
- "2. The CPU Board filter capacitor C26 for -12 V dc."
- "3. The filter capacitor C26 for excessive AC ripple (over 0.75V ac)."

"If the previous checks did not isolate the problem, turn the Volume Control for maximum output. Momentarily touch
a powered-up AC soldering pencil on the center tap of the Volume Control."

CAUTION: "DO NOT use a soldering iron over 40 watts. Note also that cordless soldering irons will NOT work for
this test."

"Hearing a low hum or a 'click' indicates that the power amplifier (U1, TDA2002), the Volume Control, and the
speaker are operating satisfactorily, as is the sound circuit cabling. Not hearing a sound requires repeating the
test with the Volume Control turned part way down, to determine whether the Volume Control is faulty. Also, check
the cable connectors for proper mating, and that no broken wires affect this circuit ."

Footer folio: "DINER 37".

---

## Problem Analysis Messages (PDF 42, printed page 38)

"The System 11C game program has a great capability to aid the operator and service personnel: At Game Turn-on
(and also at the beginning of the Test/Diagnostic Procedures) after the game has been operating for an extended
period, the player score displays now may signal with a message, "Press ADVANCE for Report", that the game
program has detected a possible problem with the game."

"To obtain details of the problem, open the coin door and press the AUTO-UP/MANUAL-DOWN switch to MANUAL-DOWN.
Press the ADVANCE button to begin displaying the message(s). The following messages apply to your DINER game."

"Adjust Failure. This message indicates a problem with the setting of Game Adjustments. For example, if the game
operator changes Adjustment Item settings by selecting Yes for AD 68 (Install Factory) and then closes the coin
door before the appearance of the FACTORY SETTING message, the game will display the ADJUST FAILURE message to
indicate that the resetting of the Adjustment Items did not occur properly. As mentioned earlier in the Game
Adjustment Procedure text (near Ad 68), other factors can also cause this message to appear."

"Check Switch ##. This message indicates that at least one switch was stuck 'On' at game turn-on or has NOT been
actuated during ball play (for 90 balls or ≈30 games) by displaying the message "Check Switch ##", listing each
problem switch by number. (The game program compensates the game play requirements affected by each disabled
switch to allow 'nearly normal' play. This helps keep DINER earning, until the service technician can repair the
problem, bringing the game back to its normal good profits!)"

"To verify the problem, refer to the Test/ Diagnostic Procedures text describing Switch Testing, and check each
reported switch using applicable Switch Levels and Switch Edges tests. Always check switch operation using a
ball, to simulate game conditions. (Switch problems may often be resolved by adjusting the wire switch actuators,
fixing switch circuitry problems, securing loose connectors, etc. Mechanisms using 'opto switches' (drop targets,
etc.) need to be checked for proper power connections (+12V dc and ground)."

"Pinball Missing. DINER normally uses three balls; however, it will operate with two balls. This message
announces that a ball is missing or stuck somewhere. When the ball is located, return it to the game via the
Outhole. Other possibilities for this problem could be malfunctions of the Ball Trough switches (#11, #12, or #13)
or the Shooter Lane switch (#14)."

Footer folio: "DINER 38".

---

## Maintenance Information (PDF 43, printed page 39)

"MAINTENANCE INFORMATION
Regular maintenance is essential to a game's continuing contribution to the operator's earnings."

"LUBRICATION
The two main lubrication points of the Left and Right Kickers ("Slingshots") mechanism are the pivots for the
Kicker Arm. Because of the functional design (arm-actuated via solenoid plunger operation), the pivot points of
the Left and Right Kickers ("Slingshots") all require lubrication as a regular servicing procedure. MBI
Instrument Grease, also known as Drop Target Switch Lubricant, with a Williams' part number of 20-8886, is a
recommended lubricant. A medium viscosity oil (20W or 30W) is satisfactory for these devices; however, oil tends
to vaporize, leaving a sticky film."

"Lubrication to ensure proper operation also applies to the target blades of the 3-Bank Drop Target. MBI
Instrument Grease, also known as Drop Target Switch Lubricant, with a Williams' part number of 20-8886, is a
recommended lubricant."

"SWITCH CONTACTS
For proper game operation, switch contacts should be free of dust, dirt, contamination, and corrosion. Blade
switch contacts are plated to resist corrosion. Cleaning blade switch contacts requires gentle closing of the
contacts on a clean business card or piece of paper, and then pulling the paper about 2 inches, which should
restore the clean contact surface. Adjust the switch contacts to a 1/16-inch gap."

"Flipper button switches and the End of Stroke (EOS) switch on the flipper tend to suffer from pitting caused by
the high current in this circuit. Weak or "slow" flipper action is the result of this pitting. Carefully restore
the surface of the flipper switch contact with a very fine contact file; finish the surface restoration with a
contact burnishing tool. This should bring the flipper action back to its usual 'snappy' action. The contact
surfaces of these switches should be adjusted to enable the maximum area of contact during switch closure. This
allows the current flowing through these switches to be at the designed, peak value for best flipper action."

"CLEANING
Good game action and extended playfield life are the results of regular playfield cleaning. During each collection
stop, the playfield glass should be removed and thoroughly cleaned. The playfield should be wiped off with a
clean, lint-free cloth. The game balls should be cleaned and inspected for any chips, nicks, or pits. Replace any
damaged balls to prevent playfield damage."

"Regular, more extensive, playfield cleaning is recommended. However, avoid excessive use of water and caustic or
abrasive cleaners because they tend to damage the playfield surface. Playfield wax or polish may be used
sparingly, to prevent a buildup on the playfield surface. Do not use cleaners containing petroleum distillates on
any playfield plastics because they may dissolve the plastic material or damage the artwork."

Footer folio: "DINER 39".

---

Normalization: game-name logotype written "DINER"; printed typographic quotation marks written as straight
quotation marks; line-end hyphenation rejoined; paragraph line breaks joined; emphasis not marked. Spelling,
capitalization, punctuation (including the printed doubled "the the" and "should ... should" on PDF 39, and the
mismatched quotation marks in "SELECTED A-SIDE'") and all digits are as printed. Word spacing is normalised
where the scan runs words together (for example "afaulty" on PDF 39 is written "a faulty"); the one run-together
word kept as printed is "connectingdevices" in the CPU LED table, row 10.

Uncertain cells:

- PDF 8, Figure 2: the pairing of "A-8550-1" and "5010-10170-00" with "Volume Control Assembly" and "& 47Ω
  Resistor" is a layout reading; the four printed lines are "A-8550-1", "Volume & 47Ω Resistor", "Control
  5010-10170-00", "Assembly". Alternative: A-8550-1 is the Volume Control Assembly and 5010-10170-00 is the 47Ω
  resistor.
- PDF 12: the manual says the two-letter abbreviations Id, Au, Ad are "underscored"; no underscore is visible in
  the scan, so none is shown.
- PDF 13, Audit Table, row 32: a small speck sits between "1,500,000" and "GRILL" in the scan; it was read as a
  speck, not a printed character. Alternative: a printed centre dot.
- PDF 13, Audit Table: the vertical Value-column rule crosses the text of rows 17, 37, 38 and 40 in the scan; the
  phrases were read as printed and were not affected, but the letters touching the rule ("Extra" in rows 37 and
  38, "Seconds)" in row 17) are partly overprinted.
- PDF 25, item 49: the last character of the second character-set line is an underscore ("_") after "Z."; it
  could be a blank-space symbol shown as an underscore, and the manual does not label it.
- PDF 37, Figure 4: small labels ("5", "3", "1", "A", "B") sit beside the relay contacts; they were read at 1.8x
  magnification and the contact numbers 3, 1 and 5 are certain, while the A/B coil-side letters are read as
  printed.
- PDF 35 and 36 and 38: the tables not transcribed here are covered by their own excerpt files; no cell from them
  was read for this file.
