# Jack*Bot — Game Operation, Game Controls, DIP Switches, EPROM Jumper and ROM Summary

Transcribed by the curator, read from the rendered pages of `Williams_1995_Jack_Bot_English_Manual.pdf` (SHA-256 `8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`, a scan with no text layer; 300 dpi renders; PDF pages 30 and 37 re-rendered from the PDF at 300 dpi, grayscale). A first pass of Windows OCR was corrected word by word against the page images. Spelling, capitalization and punctuation are as printed. Underlining and bold type in the source are not marked. PDF page 2: the DIP Switch Settings and Jumpers block; PDF page 30 (printed 1-1): the WPC ROM summary; PDF pages 35-36 (printed 1-6, 1-7): Game Control Locations and Game Operation. The second half of PDF page 2, the Solenoid/Flasher Table, is not part of this excerpt. The page images are the authority; this transcription is unreviewed by a second reader.

## PDF page 2: DIP Switch Settings and Jumpers

The page title is `DIP SWITCH SETTINGS AND JUMPERS`. The `SW4` column heading of the DIP Switch Chart carries a hand-drawn pen scribble across its first letters; the column cells beneath it are printed normally. The text of the heading is read as `SW4`.

```
EPROM Jumper Settings for U6      | W1  | W2
1MEG, 2MEG, 4 MEG EPROM           | In  | Out

DIP Switch Chart
COUNTRY      SW1   SW2   SW3   SW4   SW5   SW6   SW7   SW8
AMERICA      Off   Off   On    On    On    On    On    On
EUROPEAN     Off   Off   On    On    On    Off   On    On
FRENCH       Off   Off   On    On    On    On    Off   Off
GERMAN       Off   Off   On    On    On    On    On    Off
SPAIN        Off   Off   On    On    Off   On    On    On
```

## PDF page 30 (printed 1-1): ROM summary

The upper half of the page is the Section One divider (`SECTION ONE`, `GAME OPERATION AND TEST INFORMATION`). The lower half:

```
(System WPC) ROM  SUMMARY

IC              TYPE     BOARD     LOCATION     PART NUMBER

Game 1          27c040   CPU       U6           A-5343-50051-1A (Domestic)
Game 1          27c040   CPU       U6           A-5343-50051-1X (Foreign)
Security Chip   27c040   CPU       U22          A-5400-50051-1
Music/Speech    27c040   Audio     SU2          A-5343-50051-S2
Music/Speech    27c040   Audio     SU3          A-5343-50051-S3
Music/Speech    27c040   Audio     SU4          A-5343-50051-S4
Music/Speech    27c040   Audio     SU5          A-5343-50051-S5
Music/Speech    27c040   Audio     SU6          A-5343-50051-S6

NOTICE
Order replacement ROMs from your authorized Williams Electronics Games, Inc. distributor.  Specify:
(1) part number (if available); (2) ROM level (number) on label; (3) game in which ROM is used.

1-1
```

## PDF page 35 (printed 1-6): Game Control Locations

```
GAME CONTROL LOCATIONS

Cabinet Switches
The On-Off Switch is on the bottom of the cabinet near the right front leg.
The Start Button is a push-button to the left of the coin door on the cabinet exterior.  Press the Start
button to begin a game, or during the diagnostic mode, to ask for HELP.

Coin Door Buttons
The operator controls all game adjustments, obtains bookkeeping information, and diagnoses problems,
using only four push-button switches mounted on the inside of the coin door.  The coin door buttons have
two modes of operation Normal Function and Test Function.

Normal Function
    The Service Credits button puts credits on the game that are not included in any of the game audits.
    The Volume Up (+) button raises the sound level of the game.  Press and hold the button until the
    desired level is reached.
    The Volume Down (-) button lowers the sound level of the game.  Press and hold the button until the
    desired level is reached.  See Adjustment  A.1  28 to shut sound Off completely.
    The Begin Test button starts the Menu System operation and changes the coin door buttons from
    Normal Function to Test Function.

Test Function
    The Escape button allows you to get out of  a menu selection or return to the Attract mode.
    The Up (+) button allows you to cycle forward through the menu selections or adjustment choices.
    The Down  (-) button allows you to cycle backward through the menu selections or adjustment
    choices.
    The *Enter button allows you to get into a menu selection or lock in an adjustment choice.

*To reset  High Score, hold down the Begin Test/Enter switch for five seconds while in the Attract
mode.

1-6
```

Drawing on the page, labels as printed. A circled detail `Coin Door Button Locations` shows the coin-door button plate: the upper legend row reads `NORMAL MODE FUNCTION` over `SERVICE CREDITS`, `VOLUME` (with a row of slashes) and `BEGIN TEST`; four round buttons; the lower legend row reads `ESCAPE`, `-`, `+`, `ENTER` under `TEST MODE FUNCTION`. The cabinet-front view, with callouts:

```
Front Molding Assy.            D-12615
Extra Ball Button              20-9663-18
Lever Guide Assy.              A-16773-1
Flipper Button-Red             A-16883-4
Ball Shooter Assembly          A-20214
Start Button-Yellow            20-9663-1
Test Switch Assy.              27-4909
On-Off Switch                  5642-13935-00
```

## PDF page 36 (printed 1-7): Game Operation

The first caution paragraph is printed in bold type under a warning-triangle symbol.

```
GAME OPERATION

CAUTION
After assembly and installation at its site location, this game must be plugged into a properly
grounded outlet to prevent shock hazard, and to assure proper game operation.  DO NOT use a
'cheater' plug to defeat the ground pin on the line cord.  DO NOT cut off the ground pin.

POWERING UP.  With the coin door closed, plug the game in, and switch it On.  In normal operation,
  Testing shows in the displays as the game performs Start-up tests.  Once the Start-up tests have been
  successfully completed the last score is displayed and the game goes into the Attract mode.

  Note:  After the game has been on location for a time, the Start-up tests may contain messages
  concerning game problems.  The section entitled 'Error Messages' contains more details concerning
  messages displayed at each game turn-on.

  Open the coin door and press the Begin Test switch.  The display shows the game name, number, and
  software revision.  The message changes.  The display shows the sound software revision, the revision
  level of the system software, and the date the software was revised.

  Example:                JACK•BOT                                      Sound Rev. 1.0 A
                  50051            Rev. 1.0 A                   SY. 0.X0               X-X-95

  Press the Enter button to enter the WPC Menu System (refer to the section entitled "Menu System
  Operation" for more information).  Slide the Service Switch Actuator over the top interlock switch located
  in the bottom left corner of the coin door opening.  Perform the entire Test menu routine to verify that
  the game is operating satisfactorily.

ATTRACT MODE*.  After completing the Test menu routine, press the Escape button three times to enter
  the Attract mode.  During the Attract mode, the score display shows a series of messages informing the
  player concerning, recent highest scores*, "custom messages*", and the score to achieve to obtain a
  Replay award*.

CREDIT POSTING.  Insert coin(s).  A sound is heard for each coin, and the display shows the number of
  credits purchased.  So long as the number of maximum allowable credits* are NOT exceeded by coin
  purchase or high score, credits are posted correctly.

STARTING A GAME.  Press the Start button.  A startup sound plays, and the credit amount shown in the
  display decreases by one.  The display flashes 00 (until the first playfield switch is actuated), and
  shows ball 1.  If credits are posted, additional players may enter the game by pressing the Start button
  once for each player, before the end of play on the first ball.  Pull the ball shooter on the front of the
  cabinet to launch a ball.  Press the flipper buttons to operate the flippers.

TILTS.  Actuating the cabinet tilt switch inside the cabinet ends the current game and then proceeds to
  the Game Over mode.  With the third closure* of the plumb bob tilt switch, the player loses the
  remaining play of that ball, but can complete the game.

END OF A GAME.  All earned scores and bonuses are awarded.  If a player's final score exceeds the
  specified value, the player receives a designated award for achieving the current highest score.  A
  random digit set* appears in the display.  Credits* may be awarded, when the last two digits of any
  player's score match the random digits.  Match, high score, and game over sounds are made.

GAME OVER MODE.  The Game Over display shows the high scores and the game proceeds to the
  Attract Mode.

* - Operator-adjustable feature

1-7
```

Reading note: the two display lines of the example are laid out as two rows on the page, `JACK•BOT` and `Sound Rev. 1.0 A` on the upper row and `50051`, `Rev. 1.0 A`, `SY. 0.X0` and `X-X-95` on the lower row; the column positions above only approximate the page.
