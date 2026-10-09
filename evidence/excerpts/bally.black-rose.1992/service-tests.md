# Black Rose — Game Control Locations, Test Menu, Error Messages and Maintenance

Transcribed from `Bally_1992_Black_Rose_Manual.pdf`, PDF pages 22 (printed `BLACK ROSE 1-4`), 30-32 (printed `1-12` to `1-14`) and 52-57 (printed `1-34` to `1-39`). Windows OCR with obvious character errors corrected against the rendered pages, read from the rendered page for everything the OCR dropped (300 dpi image-only scan).

Reading notes: text is reproduced as printed, including the printer's typographical slips, which are not corrected: the T.4 sentence `more then one solenoid pulses`, the T.11 sentence `This test automatically every dot in the Dot Matrix Display` (a verb is missing in the print), `mechanisim` on PDF 57, and the lowercase `L.E.D.` spellings. Line breaks inside paragraphs are not preserved. Drawings are summarized in one line. Internal inconsistencies noticed: (a) the Test Menu list on PDF 30 names `T.12 Motor Test` but the T.12 description on PDF 32 is headed `T.12 Cannon Test`; the contents page (PDF 3) also says `T.12 Motor Tests`; (b) the list names `T.4 Solenoid Test`, `T.8 Single Lamps` and `T.10 Lamp & Flasher Tests` while the descriptions are headed `T.8 Single Lamp Test` and `T.10 Lamp and Flasher Test`; (c) PDF 55 prints the fuse `F114` as `+18V Lamp Matrix 8A, N.B.` while all other fuses read `S.B.`; (d) the CPU LED text names `D19, D20, and D21` and describes the `Center L.E.D.` as the error indicator, i.e. D20.

---

## PDF page 22, printed `BLACK ROSE 1-4` — GAME CONTROL LOCATIONS

**Cabinet Switches**

The On-Off switch is located on the bottom of the cabinet near the right front leg.

The Start Button is the pushbutton to the left of the coin door on the cabinet exterior. Press the Start button to begin a game, or during the diagnostic mode, to ask for HELP.

**Coin Door Switches**

The operator controls all game adjustments, obtains bookkeeping information, and diagnoses problems, using only four pushbutton switches mounted on the inside of the coin door. The Coin Door Switches have two modes of operation Normal Function and Test Function.

*Normal Function*

The Service Credits button puts credits on the game that are not included in any of the game audits.

The Volume Up button raises the sound level of the game. Press and hold the button until the desired level is reached.

The Volume Down button lowers the sound level of the game. Press and hold the button until the desired level is reached. See Adjustment A.1 28 to shut sound OFF completely.

The *Begin Test button starts the Menu System Operation and changes the Coin Door Switches from Normal Function to Test Function.

*Test Function*

The Escape button exits a menu selection or returns to the Attract Mode.

The Up button cycles forward through the menu selections or adjustment choices.

The Down button cycles backward through the menu selections or adjustment choices.

The *Enter button enters a menu selection or locks in an adjustment choice.

Drawing: `Coin Door Button Locations` — an inset of the coin-door switch plate with four round buttons. Printed labels, upper band `NORMAL MODE FUNCTION`: `SERVICE CREDITS`, `VOLUME` (with a slanted-line hatch mark), `BEGIN TEST`; lower band: `ESCAPE`, `-`, `+`, `ENTER`, then `TEST MODE FUNCTION`. A cabinet-front drawing with callouts `Front Molding Assy.`, `Lever Guide Assy.`, `Flipper Button`, `Ball Shooter Assy.` and `On-Off Switch`.

*To reset High Score, hold down the Begin Test/Enter switch for 5 seconds, while in the Attract Mode.

(This page prints no `Fire` button; the only cabinet-front controls named are the Start Button in the text and the `Flipper Button` and `Ball Shooter Assy.` callouts in the drawing.)

---

## PDF page 30, printed `BLACK ROSE 1-12` — Test Menu

Press the Enter button to activate the Test Menu, once the menu name is shown under the Main Menu. Then, use the Up or Down button to cycle through the Test Menu selections. Press the Enter button to activate a test. Press the Escape button to return to the Test Menu. Press again to return to the Main Menu. Note: During any test, press the Start button to obtain the wire color, driver number, connector number, and fuse location.

**T. TEST MENU**

| Number | Name as printed |
| --- | --- |
| T.1 | Switch Edges |
| T.2 | Switch Levels |
| T.3 | Single Switch |
| T.4 | Solenoid Test |
| T.5 | Flasher Test |
| T.6 | General Illumination |
| T.7 | Sound & Music Test |
| T.8 | Single Lamps |
| T.9 | All Lamps |
| T.10 | Lamp & Flasher Tests |
| T.11 | Display Test |
| T.12 | Motor Test |

The switch matrix, on the left side of the display, shows the state of all switches. A dot indicates the switch is open, and a square indicates the switch is closed. The numbers assigned to each switch indicate where the switch is located in the matrix. The number on the left indicates the column, and the number on the right indicates the row. Example: Switch 23 is 2nd column, 3rd row.

A short to ground, on either the row or column wire, appears as a shorted row(s). However, a column wire shorted to ground disappears when all the indicated row switches are open. A row wire shorted to ground does not disappear.

A shorted diode in the switch matrix can cause other switches to appear closed. These "phantom" switches (though not actually closed) complete a rectangle in the switch matrix. Therefore, if two switches in the same column are closed (example; #22 and #24), and a third switch is pressed in another column but in the same row as one of the first two (example; #32), the "phantom" switch #34 is falsely indicated closed. The switch with the shorted diode is diagonally opposite the "phantom " switch (in this case#22).

**T.1 Switch Edges**

Press each switch one at a time. The name and number of the switch is shown in the display. If a switch other than the one pressed, or no switch at all is indicated, the system has detected a problem with the switch circuit.

**T.2 Switch Levels**

This test automatically cycles through all switches that are detected closed. The name and number of each switch that is detected is shown in the display. A filled square indicates the switch's position in the matrix.

**T.3 Single Switches**

The Single Switch Test isolates a particular switch by blocking signals from all other switches. Use the Up or Down buttons to select the switch to be tested.

---

## PDF page 31, printed `BLACK ROSE 1-13` — T.4 to T.6

**T.4 Solenoid Test**

The Solenoid Test has three modes: Repeat, Stop, and Run. Only one solenoid should pulse at a time. The system has detected a problem if; more then one solenoid pulses, a solenoid comes On and stays On, or during the Repeat or Run modes, no solenoid pulses.

Repeat - The Repeat mode pulses a single solenoid. After entering this test, Solenoid 1 shows in the display. and the corresponding solenoid activates. Press the Up or Down button to cycle through the solenoids, one at a time. The same solenoid pulses until the Up or Down button is pressed. Either press the Escape button to return to the Test Menu, or press the Enter button to advance to the next mode.

Stop - The Stop mode halts the Solenoid Test. Press Enter during the Repeat mode and the Solenoid Test Stops. No solenoids should be activated while the test is stopped. Either press the Escape button to return to the Test Menu, or the Enter button to advance to the next mode.

Running - The Run mode cycles through the solenoids automatically. The display shows the name and number of the solenoid currently being pulsed. Either press the Escape button to return to the Test Menu, or the Enter button to advance to the next mode.

**T.5 Flasher Test**

This tests the flashlamp part of the solenoid circuit exclusively. This, like the Solenoid Test has three test modes: Repeat, Stop, and Run. During this test, only one flashlamp circuit should pulse at a time. The system has detected a problem if more than one circuit pulses, a circuit stays On, or during the Repeat or Run modes, no circuit pulses.

Repeat - The Repeat mode pulses a single flashlamp. After entering this test, the name and number of the first flashlamp circuit will show in the display and the corresponding bulb(s) flash. Press the Up or Down button to cycle through all of the flashlamp circuits one at a time. The same circuit pulses until the Up or Down button is pressed. Either press the Escape button to return to the Test Menu, or press the Enter button to advance to the next mode.

Stop - The Stop mode halts the Flasher Test. No flashlamp circuit should be active during this mode. Either press the Escape button to return to the Test Menu, or the Enter button to advance to the next mode.

Running - The Run mode cycles through the flashlamps automatically. The display shows the name and number of the flashlamp circuit currently being pulsed and the corresponding bulb(s) flash. Either press the Escape button to return to the Test Menu, or the Enter button to advance to the next mode.

**T.6 General Illumination**

This test checks all of the General Illumination circuits. There are two modes of operation: Stop and Run.

Stop - Press the Up or Down buttons to cycle through the General Illumination Test manually. All illumination is tested first, followed by an individual circuit test. The circuit name and number will show in the display while the corresponding lamps light. If any other results occur the system has detected an error.

Run - Press the Enter button any time during Stop test mode and the General Illumination Test cycles through automatically. For each circuit shown in the displays the corresponding bulbs should light. If any other results occurs the system has detected a problem.

---

## PDF page 32, printed `BLACK ROSE 1-14` — T.7 to T.12

**T.7 Sound and Music Test** The Sound and Music Test allows you to check the audio circuits. This test has three modes for testing the sound and music circuits: Run, Repeat, and Stop.

Run - This Run mode steps through a sequence of sounds and music. Pressing the Up or Down button during this portion of the Sound and Music test advances to a particular sound/tune without having to wait for the program to play all the sounds available in the test. A sound/tune should be heard for each name and number that appears in the display. Any other results indicate the system has detected a problem.

Repeat - Press the Enter button at any time during the Run mode to cause the program to stop and repeat a particular sound/tune. The same sound should repeat continuously until the Up or Down button is pressed. Any other results indicates the system has detected a problem.

Stop - Press the Enter button at any time during the Repeat mode to stop this test altogether. No sound/tune should be heard. Any other results indicates the system has detected a problem.

**T.8 Single Lamp Test** The number assigned to each lamp indicates the lamp's position in the matrix. The number on the left indicates the column. The number on the right indicates the row. Example: Lamp 23 means 2nd column, 3rd row.

This test checks each lamp circuit individually. Press the Up or Down button to cycle through this test. For each name and number that is shown in the display the corresponding lamp should light. Any other results indicate the system has detected a problem.

**T.9 All Lamps Test** This test causes all the controlled lamps to flash at the same time. Every controlled lamp should flash. Any other results indicate the system has detected a problem.

**T.10 Lamp and Flasher Test** This test causes all the flashlamps and the controlled lamps to flash at the same time. The controlled lamps blink, while the flashlamps cycle from highest to lowest. Any other results indicates the system has detected a problem.

**T.11 Display Test** This test automatically every dot in the Dot Matrix Display. A series of patterns appear in sequence. Each pattern turns On and Off a section of dots. Every dot on the display should be turned On and Off during this test.

**T.12 Cannon Test** This test allows the operator to toggle the cannon motor on and off. It also activates the cannon kicker and left lockup coils to allow balls to be kicked out of these devices when testing. The display will show the status of the cannon kicker switch (SW.35 CANNON = OPEN, or SW.35 CANNON = CLOSED), and the motor (MOTOR = ON, or MOTOR = OFF). This test allows for easier adjustment of the cannon kick out range. The cannon should be able to kick the ball out and make the far right shot to the jets, and the far left shot to the lockup. The test buttons are used as follows:

The ENTER, UP, and DOWN buttons will toggle the cannon motor ON or OFF.
The ESCAPE button will return to the Test Menu when pressed at anytime during the test.

---

## PDF page 52, printed `BLACK ROSE 1-34` — ERROR MESSAGES (first page)

The WPC game program has the capability to aid the operator and service personnel. At Game Turn-on, or after pressing the Begin Test switch, (once the game has been operating for an extended period), the display may signal with the message, "Press ENTER for Test Report". This indicates the game program has detected a possible problem with the game.

To obtain details of the problem, open the coin door and press the Begin Test switch. Press the Enter button to begin displaying the message(s). The following messages apply to your game.

**Check Switch ##.**
This message indicates that at least one switch was stuck 'On' at game turn-on or has NOT been actuated during ball play (for 90 balls or ≈30 games). The game program compensates the game play requirements affected by each disabled switch to allow 'nearly normal' play. This helps keep the game earning, until the service technician can repair the problem.

To verify the problem, refer to the Test Menu text describing Switch Testing, and check each reported switch using applicable switch tests. Always check switch operation using a ball, to simulate game conditions. Switch problems may often be resolved by adjusting the wire switch actuators, fixing switch circuitry problems, securing loose connectors, etc. Mechanisms using 'opto switches' (drop targets, etc.) need to be checked for proper power connections (+12V dc and ground).

**Pinball Missing.**
This game normally uses three balls; however, it will operate with one ball. This message announces that a ball is missing or stuck. When the ball is located, return it to the game via the Outhole. Other possibilities for this problem could be malfunctions of the Ball Trough switches or the Ball Shooter switch.

**xxxxx Sw. is Stuck On.**
This message indicates that a switch, which is not usually On, remains in the On position after the game is switched On. The stuck switch is essential for game play (for example, a coin chute switch, the slam tilt switch, the plumb bob tilt switch), and should be cleared to permit proper game operation.

**Ground Short Row-N, Wht-xxx.**
This message indicates that the switch wires being called out are touching a grounded part on the playfield or coin door. The following should be checked:
1. Slam Tilt (or other coin door) switch touching the grounded coin door.
2. A leaf-type, playfield switch touching a grounded part.
3. Players poking metallic objects (wires, coat hanger, etc.) into the game
4. Switch cable insulation pierced or damaged allowing bare wire contact with a grounded part
5. All switches in a row closing at the same time. Note: This instance is NOT a switch problem; however, for most games this is a very rare possibility.

**Factory Settings Restored.**
This message indicates that the CMOS RAM no longer retains any custom Pricing or Game Adjustment settings and has reverted to factory default settings. Generally, the following CPU checks will isolate the cause of the CMOS RAM memory failure. The voltage at pin 28 and pin 26 of U8 should be +5V (game turned On) and at least +4V (game turned Off). When the voltage drops below +4 V, memory reset occurs. Check the batteries and battery holder. Be sure that the batteries are good and that there is no contamination on the battery holder terminals. Turn the game OFF, and use an ohmmeter to check diodes D1 and D2 on the CPU Board. D1 should read 0 ohms when forward-biased and infinite ohms when reverse-biased. D2 should read 15 ohms when forward-biased and infinite ohms when reverse-biased. Note: Readings taken from Analog Meter. This message can also indicate that there is an open diode on a 50V coil and noise is entering the circuit.

---

## PDF page 53, printed `BLACK ROSE 1-35` — ERROR MESSAGES (second page) and error codes

**U6 Checksum Error.**
The game ROM checksum is invalid. If this occurs replace the game ROM.

**Time and Date Not Set.**
The real time clock is not running. If this occurs go to U.4 of the Utilities Menu and set the time and date.

**Warning Ramp Open/Closed Not Reliable**
This message indicates there is a problem with the up/down ramp reliably opening or closing. This means the ramp will sometimes not close or open when told to. Check to make sure switch 54, ramp down, is definitely closed when the ramp is down, and positively open when the ramp is up. Check the wires for loose connections or improper wiring. Also, check to make sure the ramp up coil (10), and the ramp down coil (11), are functioning properly. Make sure the mechanical mechanism is working smoothly. The ramp flap should be able to move up and down freely.

**Error-Ramp not opening/closing-check sw./CL.**
This message indicates there is a problem with the up/down ramp opening or closing. The ramp has failed to open or close after three tries in a row. Check to make sure switch 54, ramp down, is definitely closed when the ramp is down, and positively open when the ramp is up. Check the wires for loose connections or improper wiring. Also, check to make sure the ramp up coil (10), and the ramp down coil (11), are functioning properly. Make sure the mechanical mechanism is working smoothly. The ramp flap should be able to move up and down freely.

**CPU L.E.D.'s**
The CPU has three L.E.D.'s located on the upper left side of the board: D19, D20, and D21. On game power-up D19 and D21 turn On for a moment then, D19 turns Off and D20 starts to blink rapidly. D21 remains On. The system has detected a problem if the following happens:

**CPU Board L.E.D. Error Codes**

| Pattern | Meaning |
| --- | --- |
| Center L.E.D. blinks one time | ROM Error U6 |
| Center L.E.D. blinks two times | RAM Error U8 |
| Center L.E.D. blinks three times | Custom Chip Failure U9 |

**Sound Board Beep Error Codes Upon Game Turn-On:**

| Beeps | Meaning |
| --- | --- |
| 1 Beep | Sound Board O.K. |
| 2 Beeps | U9 Failure (RAM) |
| 3 Beeps | U18 Failure (ROM) |
| 4 Beeps | U15 Failure (ROM), if used |
| 5 Beeps | U14 Failure (ROM), if used |

(The printed `=` between the two columns is replaced by the table separator.)

---

## PDF page 54, printed `BLACK ROSE 1-36` — LED List (summary)

Drawing: a `CPU Board` outline showing chips `U4`, `U6`, `U8`, `U9`, battery positions `B1`, `B2`, `B3` and three LEDs `D19`, `D20`, `D21`; below it a `Power Driver Board` outline showing fuses `F101` to `F116` and `LED 1` to `LED 7`.

CPU Board
- D19, Blanking
- D20, Diagnostic
- D21, +5vdc
- At Game Turn-On = D19 & D21 On, D20 Off
- During Normal Operation = D19 Off, D20 flashing, D21 On

Power Driver Board
- LED 1, +12vdc, Switch Circuit, Normally On
- LED 2, High/Low Line Voltage Sensor, Normally On
- LED 3, High/Low Line Voltage Sensor, Normally Off
- LED 4, +5vdc, Digital Circuit, Normally On
- LED 5, +20vdc, Flashlamp Circuit, Normally On
- LED 6, +18vdc, Lamps Circuit, Normally On
- LED 7, +12vdc, Power Circuit (Motors, Relays, Etc.), Normally On

---

## PDF page 55, printed `BLACK ROSE 1-37` — Fuse List

Drawing: board outlines `Fliptronic II Controller Board` (F901-F904), `Audio Board` (F501, F502), `Dot Matrix Controller Board` (F601, F602) and `Power Driver Board` (F101-F116).

| Board | Fuse | Circuit | Rating |
| --- | --- | --- | --- |
| Audio Board | F501 | -25V Circuit | 3A, S.B. |
| Audio Board | F502 | +25V Circuit | 3A, S.B. |
| Dot Matrix Controller Board | F601 | +62V Circuit | 3/8A, S.B. |
| Dot Matrix Controller Board | F602 | -113V and -125V Circuits | 3/8A, S.B. |
| Power Driver Board | F101 | Left Flipper | 3A, S.B. (Not Used) |
| Power Driver Board | F102 | Right Flipper | 3A, S.B. (Not Used) |
| Power Driver Board | F103 | Solenoid #25-#28 | 3A, S.B. |
| Power Driver Board | F104 | Solenoid #9-#16 | 3A, S.B. |
| Power Driver Board | F105 | Solenoid #1-#8 | 3A, S.B. |
| Power Driver Board | F106 | G.I. #5 Wht-Vio | 5A, S.B. |
| Power Driver Board | F107 | G.I. #4 Wht-Grn | 5A, S.B. |
| Power Driver Board | F108 | G.I. #3 Wht-Yel | 5A, S.B. |
| Power Driver Board | F109 | G.I. #2 Wht-Org | 5A, S.B. |
| Power Driver Board | F110 | G.I. #1 Wht-Brn | 5A, S.B. |
| Power Driver Board | F111 | Flasher Secondary | 5A, S.B. |
| Power Driver Board | F112 | Solenoid Secondary | 7A, S.B. |
| Power Driver Board | F113 | +5V Logic | 5A, S.B. |
| Power Driver Board | F114 | +18V Lamp Matrix | 8A, N.B. |
| Power Driver Board | F115 | +12V Switch Matrix | 3/4A, S.B. |
| Power Driver Board | F116 | +12V Secondary | 3A, S.B. |
| Fliptronic II Controller Board | F901 | Upper Left Flipper | 3A, S.B. |
| Fliptronic II Controller Board | F902 | Upper Right Flipper | 3A, S.B. |
| Fliptronic II Controller Board | F903 | Lower Left Flipper | 3A, S.B. |
| Fliptronic II Controller Board | F904 | Lower Right Flipper | 3A, S.B. |
| Line Filter | U.S., Canada | | 8A |

---

## PDF page 56, printed `BLACK ROSE 1-38` — MAINTENANCE INFORMATION

**LUBRICATION**

The two main lubrication points of the Ball Shooter Lane Feeder mechanism are the pivots for the arm. The mechanism of other playfield devices are somewhat similar and have the same lubrication requirements. A medium viscosity oil (switch target grease) is satisfactory for these devices.

Because of the functional design (arm-actuated via solenoid plunger operation), the pivot points of the Left and Right Kickers ("Slingshots") all require lubrication as a regular servicing procedure.

Lubrication to ensure proper operation also applies to the target blades of Drop Targets. MBI Instrument Grease, also known as Drop Target Switch Lubricant, (Williams' part number of EI 165), is a recommended lubricant.

**SWITCH CONTACTS**

*Playfield Switches*
For proper game operation, switch contacts should be free of dust, dirt, contamination, and corrosion. Blade switch contacts are plated to resist corrosion. Cleaning blade switch contacts requires gentle closing of the contacts on a clean business card or piece of paper, and then pulling the paper about 2 inches, which should restore the clean contact surface. Adjust the switch contacts to a 1/16-inch gap.

*Flipper Switches*
This game uses the new Fliptronic II Electronic Flipper System. The end-of-Stroke switches are NORMALLY OPEN and should close when the flipper is energized. All end-of-stroke switches and flipper button cabinet switches are gold flashed computer grade leaf switches. Only low computer current is carried through these switches. DO NOT FILE or abrasively clean these switches! DO NO REPLACE these switches with the old style tungsten high current type switches, as intermittent operation could occur. Please note that unlike the old style of flipper, an end-of-stroke switch failure will not harm the flipper. The game will notify the operator of a switch being mis-adjusted in the test report, but will continue to play. The end-of-stroke switches are a means by which the new electronic flippers feel and play with all of the subtleties of the old flippers.

(`DO NO REPLACE` is printed so; the second `NOT` appears to have been lost at the line end.)

**CLEANING**

Good game action and extended playfield life are the results of regular playfield cleaning. During each collection stop, the playfield glass should be removed and thoroughly cleaned and the playfield should be wiped off with a clean, lint-free cloth. The game balls should be cleaned and inspected for any chips, nicks, or pits. Replace any damaged balls to prevent playfield damage.

Regular, more extensive, playfield cleaning is recommended. However, avoid excessive use of water and caustic or abrasive cleaners because they tend to damage the playfield surface. Playfield wax (or any carnauba based wax), or polish may be used sparingly, to prevent a buildup on the playfield surface. Do not use cleaners containing petroleum distillates on any playfield plastics because they may dissolve the plastic material or damage the artwork.

---

## PDF page 57, printed `BLACK ROSE 1-39` — CANNON ASSEMBLY (Cannon Maintenance)

**CANNON ASSEMBLY**
READ ALL INSTRUCTIONS BEFORE BEGINNING

**CLIP INSTALLATION**
It is a necessity that the Cannon Mounting Ring have the reinforcing clips attached prior to screwing in the Post Assembly. Missing clips could result in permanent damage to the unit during the cannon level adjustment.

To install and/or replace clips:

1. Remove Cannon Assembly from playfield.
2. Remove Post Assembly from plastic ring.
3. Insert clips.
4. Assemble Post Assembly to plastic ring.
5. Return Cannon Assembly to same position on playfield and make the necessary adjustments.

Drawing (right of the clip text): exploded view of the `Cannon Mounting Ring` with three clips, each with a screw and washer, and a `Post Assembly` threaded post below; callouts `Cannon Mounting Ring`, `Clip 01-10942 [?] (3-Places)` and `Post Assembly`. The middle digits of the printed clip number are blurred in the scan; `01-10942` is the most likely reading.

**CANNON LEVEL ADJUSTMENT**

1. Secure large leveling guide with vice grips (or comparable tool) while using an open-end wrench to loosen lock nut. Be careful not to let the entire locked screw/shaft assembly turn! This may result in permanent damage to the unit.
2. Once the lock nut is loose, use an allen-wrench to loosen leveling guide set screw.
3. Rotate leveling guide (clockwise to raise, counter-clockwise to lower) to align the top of the mechanisim with the top of the playfield. Adjust the remaining two guides if necessary. To check adjustment, return playfield to the horizontal playing position.
4. Reverse step sequence to re-secure the assembly.

Drawing (left of the level-adjustment text): cross-section of the leveling guide with callouts `Large Leveling Guide`, `Set Screw`, `Lock Nut` and `Screw/Shaft`.
