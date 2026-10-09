# Pin-Bot — Operator text: ROM summary, circuit boards, diagnostic procedures and game play

Source: `PinBot Instruction Manual & Schematics 600 dpi scan.pdf` (72 pages, SHA-256
`b20e98516ec75d5af42f2dff5304221d7eaea0e6bc7734898c64d98305d22e53`). Pages read: PDF 7 (printed
"PIN-BOT 1"), 8 (2), 10 (4), 11 (5), 12 (6), 31 (25), 32 (26), 33 (27), 34 (28), 35 (29) and 36 (30);
PDF page 2 (unnumbered) for the ROM and Jumper Table. All were read from rendered page images of the
600 dpi scan, which has no text layer. Text is transcribed verbatim except where a section is
summarised in a bracketed note; emphasis (underline, italic, bold) is not marked. Line breaks inside
paragraphs are joined; hyphenation at line ends is rejoined.

The tables printed in this range (Lamp-Matrix Table on printed page 26, Solenoid Table on printed
page 27, Switch-Matrix Table on printed page 29) are transcribed in `lamp-matrix.md`,
`solenoid-table.md` and `switch-matrix.md` and are not repeated here.

## PIN-BOT (System-11) ROM Summary (PDF 7, printed page 1)

The page is the Section 1 title page ("Game Operation & Test Information"), whose bullet list reads:
"PIN-BOT (System-11) ROM Summary", "Pinball Game Assembly Instructions", "Game Play", "Game Status
Displays", "Game Adjustment Procedure", "Game Pricing", "Test/Diagnostic Procedures". (The ROM
Summary table is on this page, not on PDF 8.)

| IC | DESCRIPTION | TYPE | IDENTIFIER | BOARD | PART NUMBER |
| --- | --- | --- | --- | --- | --- |
| Game ROM 1 | 32K x 8 ROM | 27256 | U27 | CPU | A-5343-549-2 |
| Game ROM 2 | 16K x 8 ROM | 27128 | U26 | CPU | A-5343-549-1 |
| Sound ROM 1 | 32K x 8 ROM | 27256 | U21 | CPU | A-5343-549-4 |
| Sound ROM 2 | 32K x 8 ROM | 27256 | U22 | CPU | A-5343-549-3 |
| Background (B/G) Sound/Speech ROM 1 | 32K x 8 ROM | 27256 | U4 | B/G Mus./Sp. | A-5343-549-5 |
| B/G Snd./Spch. ROM 2 | 32K x 8 ROM | 27256 | U19 | B/G Mus./Sp. | A-5343-549-6 |

The "Background (B/G)" label is printed on its own line above "Sound/Speech ROM 1" in the IC column,
and is joined here.

NOTICE: "To order a replacement ROM from your authorized WILLIAMS ELECTRONICS GAMES distributor,
specify: (1) part number (if available); (2) ROM label color; (3) ROM level (number) on the label; (4)
which game the ROM is used in."

## PIN-BOT ROM and Jumper Table (PDF 2, unnumbered)

Column headings: Game | System 11 CPU Rev. | P/N - U15 | P/N - U27 | P/N - U26 | P/N - U21 | P/N - U22 |
P/N - U24 | Jumpers. Down-arrows in the original mean "same as the row above"; they are written as
"(arrow)".

| Game | System 11 CPU Rev. | P/N - U15 | P/N - U27 | P/N - U26 | P/N - U21 | P/N - U22 | P/N - U24 | Jumpers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High Speed | A | 5400-09250-00 | A-5343-541-1 | A-5343-541-5 | A-5343-541-3 | A-5343-541-2 | 5400-09250-00 | W1, 2, 4, 5, and 7 |
| (arrow) | B, C, D | (blank) | (arrow) | (arrow) | (arrow) | (arrow) | (blank) | W1, 2, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17, and 18 |
| Alley Cats | A | (blank) | A-5343-1918-2 | A-5343-1918-1 | A-5343-1918-4 | A-5343-1918-3 | (blank) | W1, 3, 5, and 7 |
| (arrow) | B, C, D | (blank) | (arrow) | (arrow) | (arrow) | (arrow) | (blank) | W1, 3, 5, 7, 9, 11, 12, 14, 16, 17, and 18 |
| Grand Lizard | B, C, D | (blank) | A-5343-523-1 | A-5343-523-5 | A-5343-523-2 | A-5343-523-3 | (blank) | W1, 2, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17, and 18 |
| Road Kings | D-G | (blank) | A-5343-542-2 | A-5343-542-1 | A-5343-542-4 | A-5343-542-3 | (blank) | W1, 2, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17, and 18 |
| PIN-BOT | D-H | (arrow) | A-5343-549-2 | A-5343-549-1 | A-5343-549-4 | A-5343-549-3 | (arrow) | W1, 2, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17, and 18 |

In the High Speed rows the U15 and U24 cells print a vertical arrow line from the first row down
through the "B, C, D" row; on the PIN-BOT row the U15 and U24 cells print a downward arrowhead (the
same continuation). The cells marked "(blank)" print nothing, or the column's continuation line. The
page also carries a second printing of the Solenoid Table (see `solenoid-table.md`).

## CONNECTOR IDENTIFICATION (PDF 8, printed page 2)

"WILLIAMS ELECTRONICS GAMES uses a special technique to identify connectors. Each plug or jack
receives a prefix number (which identifies the circuit board), a letter, and a number.
J-designations refer to the male part of a connector. P-designations refer to the female part of a
connector. For example, 1J1 designates jack 1 of board 1 (a CPU Board jack); 3P6 designates plug 6 of
board 3 ( a Power Supply Board plug).

Identifying the specific pin number of a connector involves a hyphen, which separates the pin number
from the plug or jack designation. For example, 1J1-3 refers to pin 3 of jack 1 on board 1."

## PIN-BOT CIRCUIT BOARDS (PDF 8, printed page 2)

"All PIN-BOT Circuit Boards are in the backbox. They are accessible by removing the backbox glass,
unlatching the insert board, and swinging it open.

CPU BOARD. The System-11 CPU Board (p/n D-10881) must be equipped with the ROMs specified in the
PIN-BOT (System-11) ROM Summary. For this ROM complement, on Revision B (or later) CPU boards (having
jumpers W1 through W18): jumpers W1, W2, W4, W5, W7, W8, W11, W12, W13, W14, W16, W17, and W18 must
be connected. Jumper W7 is cut/removed for West German games.

BACKGROUND MUSIC & SPEECH BOARD. The Background Music & Speech Board is p/n D-11297, as supplied
with ROM and microprocessor.

DISPLAY BOARDS. The Alphanumeric Master Display Board is p/n D-10877. Two of the 7-digit Player Score
Displays (player 1 and 2) are p/n C-10866. The player 3 and 4 Displays are p/n C-8364-1. The 2-digit
Credit (also BALL IN PLAY), 2-digit MATCH Display is p/n C-8365-1.

POWER SUPPLY BOARD. The Power Supply Board is p/n D-8345 -549.

Prefix numbers for PIN-BOT System-11 circuit boards and major assemblies are listed below. A prefix
number may precede a component designator to identify the unit (e.g., connector 1J1)."

Prefix table (three columns as printed):

| Prefix | Unit | Prefix | Unit | Prefix | Unit |
| --- | --- | --- | --- | --- | --- |
| 1 | CPU | 6 | Backbox | 11 | B/G Music/Speech |
| 2 | (not assigned) | 7 | Cabinet | 12 | (not assigned) |
| 3 | Backbox Power Supply | 8 | Playfield | 13 | (not assigned) |
| 4 | Alphanumeric Display | 9 | Insert Board | 14 | (not assigned) |
| 5 | Player Score Displays | 10 | (not assigned) | 15 | Flipper Power Supply |

## PIN-BOT GAME CONTROL LOCATIONS (PDF 8, printed page 2)

"The On-Off switch is on the bottom of the cabinet near the right front leg.

The Volume Control is on the left inner wall of the cabinet on the tilt mechanisms board. It is
accessible by opening the coin box door.

The Credit switch is a pushbutton to the left of the coin door on the cabinet exterior.

GAME ADJUSTMENT/DIAGNOSTIC SWITCHES. PIN-BOT allows the operator to program virtually all game
adjustments, obtain bookkeeping information, and diagnose problems, using only three switches mounted
on the inside of the coin door and the Credit button beside the coin door.

ADVANCE, AUTO-UP/MANUAL-DOWN, and HIGH-SCORE RESET are the switches located on the inside of the
coin door. Refer to the Game Status Displays text and the Text/Diagnostic Procedures for details
concerning their operation.

The Memory Protect switch is on the inside frame of the coin door. This interlock switch must be open
to clear bookkeeping totals and to make game adjustments. It automatically opens, when the coin door
opens."

## GAME OPERATION (Continued) (PDF 10, printed page 4)

The page prints Figure 1 "Pinball Assembly, Playfield Pitch Angle, and Leg Leveler Details" (a side
drawing with the labels "APPROXIMATE PLAYFIELD PITCH", "0° LEVEL", "EXTEND 2/3 LENGTH", "SEE DETAIL
VIEW", "Detail View- Leg Leveler", "LEG LEVELER", "NUT", "LEVELER FOOT PAD"), then:

"CAUTION. PIN-BOT's System 11 game program has a new capability to aid the operator and service
personnel: At game Turn-On (and also when the operator is beginning the Test/Diagnostic Procedures),
a display now signals when a switch has NOT been actuated during ball play for 60 balls (20 games).
Up to three switches can be displayed during this Switch Problem reporting activity. Moreover,
PIN-BOT compensates the game play requirements affected by each disabled switch to allow 'nearly
normal' play. This helps keep PIN-BOT earning good profits! More information is available in the
Diagnostic Procedures text describing the Switch Testing.

ATTRACT MODE*. Playfield and backbox lamps blink. All player score displays exhibit a series of
messages informing the player concerning: A. Recent highest scores*; B. A "custom message" ("GIVE ME
SIGHT ... LOCK MY ... EYE BALLS.")*; C. The score to achieve to obtain a Replay award*; D. Brief game
feature instructions.

These displays (or variations of them) reappear occasionally, accompanied by sounds and music, until
a player initiates game play by inserting a coin or, when credits are available, pressing the Credit
button.

CREDIT POSTING. Insert coin(s). A sound is heard for each coin, and the Credits display shows the
number of credits purchased. So long as the number of maximum allowable credits* are NOT exceeded by
coin purchase or high score, credits are posted correctly. However, after this maximum credits value
is reached, posting of additional credits won (not purchased) by the player does not occur. ONLY
posting of purchased credits occurs beyond the maximum credits value."

## GAME OPERATION (Continued) and PIN-BOT GAME PLAY (PDF 11, printed page 5)

"STARTING A GAME. Press the Credit button once. A startup sound plays, and the amount shown in the
Credit display decreases by one. Player display 1 flashes (until the first playfield switch is
actuated), and the BALL IN PLAY display shows 1. Additional players may enter the game by pressing the
Credit button once for each player, before the end of play on the first ball.

TILT. Actuating the Slam Tilt switch on the coin door inside the cabinet ends the current game;
PIN-BOT then proceeds to the Game Over Mode. With the actuation of the ball-roll or playfield tilt
switches, or the third closure* of the plumb bob tilt switch, the player loses the remaining play of
that ball, but can complete the game.

END OF GAME. All earned scores and bonuses are awarded. If a player's final score exceeds the
specified value, the player receives a designated award for achieving the current highest score. A
random digit set* appears in the MATCH display. Credit* may be awarded, when the last two digits of any
player's score display (1 through 4) match the random digits of the MATCH display. Match, high score,
and game over sounds are made, as appropriate.

GAME OVER MODE. The GAME OVER indicator lights. The player 1 and 2 score displays show GAME OVER
(printed in the display font as "GAME OUER"). Then, the high scores flash on the appropriate player
score displays. The game proceeds to the Attract Mode.

* - operator-adjustable feature"

PIN-BOT GAME PLAY (a two-column table: feature name at the left, description at the right):

| Feature | Description |
| --- | --- |
| Right Flipper Return & Eject | Right Flipper Return Lane flashes Eject value (Adj. for timed interval, or until made): 25K - 50K- 75K - Lites Extra Ball. Entering Eject Hole, when flashing, scores value and turns on light. Hitting Return Lane again flashes next value. Lighting Extra Ball lights one of four lower lanes (on Lane Change) for Extra Ball. |
| Jet Bumpers & "Energy Value" | Every hit on a Jet Bumper increases "Energy Value" by 2000; starting at 50,000, "Energy Value" carries over from ball to ball. Hitting flashing Drop Target raises Ramp and lights target to collect "Energy Value" for timed interval (Adj. 1 - 90 sec). "Energy Value" maximum is 500,000. |
| 5-Bank Teeth & Right 5-Bank Targets | Hitting Teeth targets lights "Chest Panel" lamps vertically. Hitting Right 5-bank targets lights "Chest Panel" lamps horizontally. Lighting all 5 rows opens Visor and drops Teeth targets. "Eye" Eject Holes are now flashing to lock balls for Multi-Ball(TM). During Multi-Ball(TM), all scores are doubled (2X). Lighting all 5 rows a second time lights one Extra Ball light. Hitting target lit by flashing light bar (on 1st shot only) opens Visor automatically. |
| Ramp Shot Bonus Multiplier - Solar Value | Ramp shot advances Bonus X (Bonus Multiplier): 2X-3X-4X-5X. Every shot up the Ramp, when NOT lit, increases "Solar" value by 50K (Adj. 25K to 99K).Starting at 100K (up to 5 million max.), this feature carries over ball-to-ball, player-to-player, and game-to-game, until collected. During Multi-Ball(TM), locking one ball in Eye-Eject lights Ramp to "Collect Solar Value". |
| 3-Bank Targets & Planets | Making 3-bank targets within time limit scores 25,000 and advances to next planet: Pluto - Neptune - Uranus - Saturn - Jupiter - Mars - Earth - Venus - Mercury - The SUN). |
| Left Flipper Return Lane | Left Flipper Return Lane lights lower right Bullseye (Adj. On, until made, or for timed interval) to advance Planets. |

("Multi-Ball(TM)" prints the trademark symbol as a superscript.)

## PIN-BOT GAME PLAY (Continued) (PDF 12, printed page 6)

An unlabelled paragraph continues the 3-Bank Targets & Planets / Left Flipper Return Lane entries (no
feature name in the left column):

"At Game Start, PIN-BOT selects a destination (planet) for the player. Reaching selected planet scores
Special. Reaching The SUN lights lower right target for an additional Special (and a super light
show). Planets score 20,000 each at Bonus Collect."

| Feature | Description |
| --- | --- |
| VORTEX | VORTEX Hole values range from 5,000 (easy) to 20,000 (medium) to 100,000 (hard). Every ball shooter shot entering VORTEX multiplies Hole values, starting at X1 up to X10 for the tenth time, then back to X1. Examples: 50,000 = 5,000 X10; 200,000 = 20,000 X 10; 1 million = 100,000 X 10. |
| BONUS | Bonus goes from 1,000 to 99,000 max., and is displayed when bonus is advanced, when ball drains, and also when a flipper button is held for a status report. |

The remainder of the page is the start of "PIN-BOT GAME STATUS DISPLAYS" (Identification
Information--Id, Audit Information--Au); it is not transcribed here.

## TEST/DIAGNOSTIC PROCEDURES (PDF 31, printed page 25)

"WILLIAMS ELECTRONICS GAMES provides a series of diagnostic tests to aid the operator in determining
game condition (that is, whether the game's features and highlights are operating satisfactorily).
These tests activate virtually all the electronic and electromechanical devices comprising the game,
so that the operator can readily locate a malfunctioning device or simply verify that all devices are
working properly. In order, these tests deal with the music, the displays, the game sounds, the lamps,
the solenoids, and the switches.

In addition to the diagnostic testing, a feature called the Auto Burn-in Mode is available. Activating
this mode enables the operator to observe the game while all of the diagnostic tests, except the
switch test, occur. This can be very helpful in locating intermittent problems.

Activating either the entire test series or one of the individual tests requires use of the Game
Adjustment/ Diagnostic switches. Open the coin door for access to these switches. To proceed to the
Diagnostic Tests, the operator must simply switch the game On, set the AUTO-UP/MANUAL-DOWN switch to
MANUAL-DOWN, and press the ADVANCE button.

CAUTION. PIN-BOT's System 11 game program has a new capability to aid the operator and service
personnel: When the operator is beginning the Test/Diagnostic Procedures (and also at game Turn-On), a
display now signals when a switch has NOT been actuated during ball play for a lengthy period of time
(60 balls, or 20 games). However, for the Switch Problem Reporting activity at the beginning of the
Test/Diagnostic Procedures, the display of problem switches is not limited to just three switches; it
now includes ALL switches exhibiting problems. Refer to the text on Switch Tests for additional
information. To proceed with the Test/Diagnostic Procedures, use AUTO-UP, and press ADVANCE.

MUSIC TEST.
1. In the Music Test, observe that the player 1 and 2 displays show the message, MUSIC TEST. Switching
   to AUTO-UP, observe that the message now reads MUSIC OFF, and that the BALL IN PLAY/MATCH display
   shows 00. Press the Credit button to select the desired music selection: 01 - 'Game Theme' through
   07 - 'Hi. Score Theme' (the selections repeat). Adjust the volume control for proper sound level
   for the game location.
2. Use the AUTO-UP position.

DISPLAY TEST.
1. To initiate the Display Test, press ADVANCE. Observe that player 1 and 2 displays briefly show the
   message, DISPLAY TEST, and that the Credits display shows 00 (the Display Test identifier).
2. Use AUTO-UP. Observe that all displays begin a display cycle of all 0s through all 9s, one digit at
   a time. Verify that the proper comma segments light during display of the odd-numbered digits.
   Next, a special "all segments" character 'walks' from left to right across each display (player 1,
   2, 3, 4, BALL IN PLAY/MATCH, Credits).
3. To halt the display cycle, use MANUAL-DOWN. Then, press ADVANCE to step through the sequential
   digit display, digit by digit, and the subsequent "all segments" characters display test. Use
   AUTO-UP to resume cycling, and to proceed to the next test.

SOUND TEST.
1. (From Display Test) To initiate the Sound Test, press ADVANCE. Observe that the player 1 and 2
   displays show the message, SOUND TEST, and that the Credit display shows 01 (the Sound Test
   identifier). The BALL IN PLAY/MATCH display shows a series of test steps from 00 through 07. Verify
   that a different sound is heard each time the number in the BALL IN PLAY/MATCH display changes."

## TEST/DIAGNOSTIC PROCEDURES (Continued) (PDF 32, printed page 26)

(The Lamp-Matrix Table on this page is in `lamp-matrix.md`.)

"SOUND TEST (Continued)
2. To repeatedly pulse a single sound, use MANUAL-DOWN. Verify that one particular sound repeats.
   Press ADVANCE to step to the next sound, which repeats until ADVANCE is pressed again. Use AUTO-UP
   to resume cycling the sounds, and to proceed to the next test.

LAMP TESTS.
1. All Lamps. (From Sound Test) To initiate the first Lamps Test, press ADVANCE. Observe that the
   player 1 and 2 displays show the message, ALL LAMPS, and that the Credit display shows 02 (All Lamps
   Test identifier) and that all feature lamps (playfield and backbox) blink on and off. (Note,
   however, that the General Illumination lamps remain lighted steadily.) To locate the wiring
   associated with a particular feature lamp, refer to the Lamp-Matrix Table. CPU Board connections at
   jacks 1J6 (columns) and 1J7 (rows) are also listed in the table.
2. Single Lamps. From the All Lamps test, using AUTO-UP, press ADVANCE to enable PIN-BOT to initiate
   the Single Lamps Test. The player 1 and 2 displays initially show the message, SINGLE LAMPS, and the
   Credit display shows 03. Then, the BALL IN PLAY/ MATCH display shows 01 and the player 1 and 2
   show GAME OVER, the name of the lamp currently blinking. Press the Credit button to proceed through
   an ascending series of designator numbers (01 through 64), with the player 1 and 2 displays showing
   the individual lamp's name. Press and hold the Credit button to proceed rapidly to the desired
   lamp."

## TEST/DIAGNOSTIC PROCEDURES (Continued), Solenoid Test (PDF 33, printed page 27)

The Solenoid Test text and the PIN-BOT Solenoid Table are in `solenoid-table.md` (the text there is
the verbatim paragraph preceding the table: COIL TEST message, Credit display 04, BALL IN PLAY/MATCH
steps 01 through 22, MANUAL-DOWN to pulse one solenoid continuously, ADVANCE to sequence through the
switched, controlled, and special solenoids).

## TEST/DIAGNOSTIC PROCEDURES (Continued), Solenoid Test and Switch Tests (PDF 34, printed page 28)

The page prints two small logic diagrams captioned ""On" State Logic - Special Solenoid" and ""On"
State Logic - Controlled Solenoid" (drawn with a 7407 buffer fed from the PIA, jack 1J18 "S.S.
TRIGGER INPUT", a 7402 gate marked "LOW WHEN FLIPPERS ENABLED", a 2N4401 and a TIP 122 driver, jack
1J19, +5V and +34V, and "SPECIAL SOLENOID "ON"" for the left diagram; a 7408 gate fed "FROM PIA" and
"BLANKING", a 2N4401 and TIP 122, jack 1J11 OR 1J12, +34V and "CONTROLLED SOLENOID "ON"" for the right
diagram), followed by:

""Off" State - Special Solenoid: The Special Switch Trigger Input goes low. Meanwhile, the PIA line
remains high. The remaining signals reverse their states.

"Off" State - Controlled Solenoid: The Enable Input (from the PIA) goes low. Meanwhile, the BLANKING
signal remains high. The rest of the signals reverse their states.

NOTE. As directed by the game program, the Solenoid Select Relay (solenoid 14) switches the solenoid
B+ power between two power busses to permit actuating two groups of solenoids at the proper times. In
its de-energized state, the Relay connects the 'circuit A power' to 16 "controlled" and "switched"
solenoids (identified in the table with no suffix letter or the letter A, after the solenoid number).
Individual solenoid operation then depends on the game program enabling the ground path for solenoid
actuation via the driver transistor associated with each solenoid circuit. For example, the game
program can actuate the Ramp Raise solenoid (sol. 05A), via the driver transistor Q31.

When the game program determines that the Relay (sol. 14) must be energized, the relay then connects
'circuit C power' to eight group C solenoids (01C through 08C). Now, driver transistor Q31 can actuate
the Lower Playfield and Backbox Flashers (sol. 05C). Using this "multiplexing" technique, the same
driver transistor can control actuation of two separate solenoids.

SWITCH TESTS.
1. Switch Levels. (From Solenoid Test) To initiate the Switch Levels Test, press ADVANCE. Observe that
   the player 1 and 2 displays show the message, SWITCH LEVELS, the Credit display shows 05 (Switch
   Levels Test identifier), and the BALL IN PLAY/MATCH display is blank, indicating that no switch is
   actuated.

   If, however, a switch is actuated (possibly stuck closed), the BALL IN PLAY/MATCH display shows that
   switch's number, while the player 1 and 2 displays indicate the switch's name. A sound also
   accompanies the displays. (This is another facet of the new PIN-BOT System-11 switch testing
   capability.) If more than one switch is closed, each switch's name and number becomes a member of a
   series of displays, each showing the switches' names and numbers.

   (In addition, either of these problems could result in the reporting of a switch problem (or
   problems) at game Turn-On or at the beginning of Diagnostic Tests.)

   As soon as the operator opens a closed switch, its name and number are eliminated from the Switch
   Levels display series. For PIN-BOT, switch numbers can range from 01 through 48. Refer to the
   Switch-Matrix Table for switch numbers and wiring information. CPU Board connections at jacks 1J8
   (columns) and 1J10 (rows) are also listed in the table.

   Row Problems. If a display of two (or more) switch numbers of a row occurs, although only one
   switch is closed, check for a short circuit between the column wires.

   Multiple Switch Number Indications. Check the associated column wire for a short circuit to
   ground."

(The Switch Levels paragraph prints "01 through 48" although the Switch-Matrix Table numbers switches
01 through 64; transcribed as printed.)

## TEST/DIAGNOSTIC PROCEDURES (Continued), Switch Tests (PDF 35, printed page 29)

(The Switch-Matrix Table on this page is in `switch-matrix.md`.)

"SWITCH TESTS (Continued).

Column Problems. If display of two (or more) switch numbers in a column occurs (while only one switch
is actuated), check for a short circuit between the row wires.

Use AUTO-UP to proceed to the next test.

2. Switch Edges. From the Switch Levels Test, press ADVANCE. Observe that the player 1 and 2 displays
   show the message, SWITCH EDGES, the Credit display shows 06 (Switch Edges Test identifier), and the
   BALL IN PLAY/MATCH display is blank, indicating that no switch is actuated.

   This test permits the operator to test whether actuating a switch provides the proper signal to the
   System-11 switch testing program. When actuating a switch, the operator should see the switch's
   name and number (in the player 1 and 2, and the BALL IN PLAY/MATCH displays, respectively). If no
   indication appears at the time the switch is actuated, the operator then knows that there is a
   malfunction associated with that switch.

   [PIN-BOT Switch-Matrix Table]

   Using this technique, the operator can test each switch appearing in the PIN-BOT switch problem
   reporting displays (either at game Turn-On or at the beginning of the Diagnostic Tests) to
   determine whether the switch can be actuated. If the switch's name and number are displayed while
   the operator checks its operation, the operator then knows that the reported problem with that
   switch is NOT currently caused by a switch malfunction. The operator can then seek other causes for
   the reported problem, being almost certain now that the switch did not fail. This test is also
   useful when the operator is adjusting the sensitivity of a particular switch's actuation
   mechanism."

## TEST/DIAGNOSTIC PROCEDURES (Continued) (PDF 36, printed page 30)

"SWITCH TESTS (Continued).

Among the possibilities is the fact that the players have not hit that switch because of some other
problem; the operator should try to analyze what could cause the switch to be missed, and remedy that
problem cause. With these new tests, switch problems are, therefore, more easily isolated.

Coin Chute Switches. During the Switch Edges test, the System-11 switch testing program energizes the
coin lockout relays, to prevent testing actuations of the coin chute switches from affecting the data
contained in the audit counters, thereby maintaining accurate records of the game's earnings.

3. Playfield or CPU Board? To determine whether a switch problem is in the playfield or the CPU Board,
   remove connectors 1P8 and 1P10 from the CPU Board. Begin the Switch Test. Use a jumper wire to
   simulate switch actuation. For example, placing a jumper between 1J10-9 and 1J8-2 should (based on
   the Switch-Matrix Table) should produce an indication of switch 09 being actuated.

ENDING THE DIAGNOSTIC TESTS. To end the Diagnostic Tests, reach the Switch Edges Test (06 in the
Credits display), use AUTO-UP and press ADVANCE. The backbox displays should show the PIN-BOT game's
Identification Information. Use MANUAL-DOWN, and press ADVANCE to reach Adjustment Item 70 (INSTALL
FACTORY). Use AUTO-UP and press ADVANCE to obtain the Attract Mode.

AUTO BURN-IN MODE. The Auto Burn-in Mode permits the operator to check intermittent (or nonrecurring)
problems associated with most portions of the game's circuitry. Repeatedly cycling through a group of
tests can sometimes bring a problem, which occurs only randomly or occasionally, to exhibit itself
more frequently, thereby aiding in the isolation of the problem. To activate the Auto Burn-in Mode:
1. While in the Game Adjustments, reach Ad 67 and change the Factory Setting of NO to YES, via the
   Credit button. Set the AUTO-UP/MANUAL-DOWN switch to AUTO-UP.
2. Press ADVANCE to start the Auto Burn-in Mode. This mode repeatedly sequences through the Music
   Test, the Display Test, the Sound Test, the All Lamps portion of the Lamp Test, and the Solenoid
   Test.
3. To halt the Auto Burn-in Mode, switch the game Off and then On. PIN-BOT now starts in the Attract
   Mode. (If a switch problem is now reported by the displays, perform the Switch Tests again to
   determine the nature of the problem; then, perform necessary repairs.)

SYSTEM-11 MEMORY CHIP TEST. A new feature is now included in the Memory Chip Test for System 11.
During power-up, the CPU performs a self-testing routine. When all tests are satisfactory, the game
proceeds to the Attract Mode, allowing players to use the game. Whenever a portion of the testing
does not produce satisfactory results, the game displays a message, before proceeding to the next
portion of the testing. ONLY after all tests are satisfactory does the game allow play.

In addition to the displayed message, when a test fails, the lower LED mounted on the CPU Board can
be observed to determine the probable cause of the problem. The LED blinks, or flashes, a certain
number of times to identify the probable cause, as described in the CPU LED Indicator Codes Table. The
operator can also start the self-testing routine by pressing the CPU Diagnostic Switch (SW 2) on the
edge of the CPU Board."

Normalization: paragraph line breaks joined and end-of-line hyphenation rejoined; quotation marks
are straight; underline/italic/bold emphasis is dropped; the trademark superscript is written "(TM)";
the Switch-Matrix Table and the Lamp-Matrix Table are referenced rather than repeated.
