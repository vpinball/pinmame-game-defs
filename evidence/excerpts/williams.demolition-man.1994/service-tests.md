# Demolition Man — Menu System, Test Menu, Error Messages and Cryoclaw/Elevator Theory of Operation

Transcribed from `Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf`, PDF pages 2, 11,
18, 19, 23, 24, 25, 26, 27, 28, 46, 47, 48 and 49 (printed folios: none visible on page 2,
`DEMOLITION MAN 1-1`, `1-8`, `1-9`, `1-13`, `1-14`, `1-15`, `1-16`, `1-17`, `1-18`, `1-36`, `1-37`, `1-38`,
`1-39`). The text was taken from the OCR layer and corrected against the rendered pages (308 dpi 1-bit
scans). Spelling, capitalization, punctuation and typos are kept as printed (for example `then` for
`than`, `Slngle`, `the the`). Drawings are not reproduced; only printed callout labels are listed.
Italic and bold emphasis is not reproduced except where noted. Page 2's solenoid/flasher table is outside
this excerpt.

## PDF page 2, no printed folio visible: ROM Jumper Chart and Country DIP Switch Chart

The same page carries the SOLENOID / FLASHER TABLE below these two charts; that table is not part of this
excerpt. Blank cells: none; every cell is printed.

### ROM Jumper Chart

| | W1 | W2 |
| --- | --- | --- |
| 1M / 2M / 4M ROM | In | Out |

### Country DIP Switch Chart

| | Sw4 | Sw5 | Sw6 | Sw7 | Sw8 |
| --- | --- | --- | --- | --- | --- |
| American | On | On | On | On | On |
| European | On | On | Off | On | On |
| French | On | On | On | Off | Off |
| German | On | On | On | On | Off |
| Spanish | On | Off | On | On | On |

## PDF page 11, printed folio `DEMOLITION MAN 1-1`: ROM SUMMARY

The page also carries the Section 1 title (`SECTION 1`, `Game Operation and Test Information`). All rows
are underlined in the render. Blank cells: none.

| IC | Type | Location | Board | Part Number |
| --- | --- | --- | --- | --- |
| Game ROM 1 (Domestic) | 27c040 | U6 | CPU | A-5343-50028-1A |
| Game ROM 1 (Foreign) | 27c040 | U6 | CPU | A-5343-50028-1X |
| Music/Speech ROM | 27c040 | SU2 | Audio | A-5343-50028-S2 |
| Music/Speech ROM | 27c040 | SU3 | Audio | A-5343-50028-S3 |
| Music/Speech ROM | 27c040 | SU4 | Audio | A-5343-50028-S4 |
| Music/Speech ROM | 27c040 | SU5 | Audio | A-5343-50028-S5 |
| Music/Speech ROM | 27c040 | SU6 | Audio | A-5343-50028-S6 |
| Music/Speech ROM | 27c040 | SU7 | Audio | A-5343-50028-S7 |

## PDF page 18, printed folio `DEMOLITION MAN 1-8`: MENU SYSTEM OPERATION

> MENU SYSTEM OPERATION
>
> The Main Menu allows you to choose from several categories, which in turn lead to other menus to choose
> from. To access the Main Menu, open the coin door and press the Begin Test button, then press the Enter
> button. Press the Up or Down buttons to cycle through the Main Menu. Press the Enter button to access a
> menu. Press the Escape button to return to the Main Menu. Press the Start button for HELP at any time.

The page prints a tree: the main menu entries `B. Bookkeeping Menu`, `P. Printouts Menu`, `T. Test Menu`,
`U. Utilities Menu` and `A. Adjustments Menu` run down the left, each followed by its sub-menu
list, printed to the right between horizontal rules. The lists, grouped by item prefix, are:

| Main menu entry | Items printed in its list |
| --- | --- |
| B. Bookkeeping Menu | B.1 Main Audits; B.2 Earning Audits; B.3 Standard Audits; B.4 Feature Audits; B.5 Histograms; B.6 Time-stamps |
| P. Printouts Menu | P.1 Earnings Data; P.2 Main Audits; P.3 Standard Audits; P.4 Feature Audits; P.5 Score Histograms; P.6 Time Histograms; P.7 Time-Stamps; P.8 All Data |
| T. Test Menu | T.1 Switch Edges Test; T.2 Switch Levels Test; T.3 Single Switches Test; T.4 Solenoid Test; T.5 Flasher Test; T.6 General Illumination Test; T.7 Sound and Music Test; T.8 Single Lamps Test; T.9 All Lamps Test; T.10 Lamp & Flasher Test; T.11 Display Test; T.12 Flipper Coil Test; T.13 Ordered Lamps Test; T.14 Claw Test; T.15 Empty Balls Test |
| U. Utilities Menu | U.1 Clear Audits; U.2 Clear Coins; U.3 Reset H.S.T.D.; U.4 Set Time & Date; U.5 Custom Message; U.6 Set Game I.D.; U.7 Factory Adjustments; U.8 Factory Resets; U.9 Presets; U.10 Clear Credits; U.11 Auto Burn-in |
| A. Adjustments Menu | A.1 Standard Adjustments; A.2 Feature Adjustments; A.3 Pricing Adjustments; A.4 H.S.T.D. Adjustments; A.5 Printer Adjustments |

Right-hand legend, printed as five short paragraphs:

> Press Escape
> To move out of a menu selection.
>
> Press Enter
> To get into a menu selection.
>
> Press Up
> Increases sequence; (ex. A.1 A.2, A.3, A.4).
>
> Press Down
> Decreases sequence; (ex. A.4, A.3, A.2, A.1).
>
> Use Up or Down to cycle through the selections in a menu.
>
> Use Escape and Enter to move into and out of the selected menu.

## PDF page 19, printed folio `DEMOLITION MAN 1-9`: B. BOOKKEEPING MENU

> Press the Up or Down buttons to cycle through the menu. Press the Enter button to access an audit menu.
> Press the Escape button to return to the Bookkeeping Menu.
>
> B. BOOKKEEPING MENU
>
> B.1 Main Audits
> B.2 Earning Audits
> B.3 Standard Audits
> B.4 Feature Audits
> B.5 Histograms
> B.6 Time-Stamps
>
> One Button Audit System. The Bookkeeping Menu is obtainable directly from the Attract Mode. Repeatedly
> pressing the Enter button, while in the Attract Mode, will cycle through all of the game audits.

### B.1 Main Audits

| Audit | Name | Value shown |
| --- | --- | --- |
| B.1 01 | Total Earnings | 00 |
| B.1 02 | Recent Earnings | 00 |
| B.1 03 | Free Play Percent | 00 |
| B.1 04 | Average Ball Time | 00 |
| B.1 05 | Time Per Credit | 00 |
| B.1 06 | Total Plays | 00 |
| B.1 07 | Replay Awards | 00 |
| B.1 08 | Percent Replays | 00 |
| B.1 09 | Extra Balls | 00 |
| B.1 10 | Percent Extra Ball | 00 |

### B.2 Earning Audits

| Audit | Name | Value shown |
| --- | --- | --- |
| B.2 01 | Recent Earnings | 00 |
| B.2 02 | Recent Left Slot | 00 |
| B.2 03 | Recent Center Slot | 00 |
| B.2 04 | Recent Right Slot | 00 |
| B.2 05 | Recent 4th Slot | 00 |
| B.2 06 | Recent Paid Credits | 00 |
| B.2 07 | Recent Service Credits | 00 |
| B.2 08 | Total Earnings* | 00 |
| B.2 09 | Total Left Slot* | 00 |
| B.2 10 | Total Center Slot* | 00 |
| B.2 11 | Total Right Slot* | 00 |
| B.2 12 | Total 4th Slot* | 00 |
| B.2 13 | Total Paid Credits* | 00 |
| B.2 14 | Total Service Credits* | 00 |

> \* These audits are NOT resettable. They are a record of the earnings of the game since the "CLOCK 1ST
> SET" Time-stamp.

## PDF page 23, printed folio `DEMOLITION MAN 1-13`: P. PRINTOUTS MENU

> Press the Up or Down buttons to cycle through the menu. Press the Enter button to access a menu.
> Press the Escape button to return to the Printouts Menu.
>
> P. PRINTOUTS MENU
> (optional board required)
>
> P.1 Earnings Data
> P.2 Main Audits
> P.3 Standard Audits
> P.4 Feature Audits
> P.5 Score Histograms
> P.6 Time Histograms
> P.7 Time-Stamps
> P.8 All Data
>
> The Printouts Menu is a combination of the other menus. This menu allows you to access and print
> information in the available menu selections.
>
> If no printer is attached the the message "Waiting for Printer" appears in the displays.
> NOTE: Set the print specification from the Adjustment Menu, A.5 Printer Adjustments.

## PDF page 24, printed folio `DEMOLITION MAN 1-14`: T. TEST MENU, T.1 to T.3

The first paragraph is printed in bold italic at the top of the page.

> Use the Service Switch Actuator to hold in the top Interlock switch located in the bottom left corner of
> the coin door opening. The actuator must be in place in order to activate the solenoids and flashlamps.
>
> Press the Up or Down buttons to cycle through the menu. Press the Enter button to access a test. Press
> the Escape button to return to the Test Menu. NOTE: During any test, press the Start button to obtain
> the wire color, driver number, connector number and fuse location.
>
> T. TEST MENU
>
> T.1 Switch Edges Test
> T.2 Switch Levels Test
> T.3 Single Switch Test
> T.4 Solenoid Test
> T.5 Flasher Test
> T.6 General Illumination Test
> T.7 Sound & Music Test
> T.8 Single Lamps Test
> T.9 All Lamps Test
> T.10 Lamp & Flasher Test
> T.11 Display Test
> T.12 Flipper Coil Test
> T.13 Ordered Lamps Test

This page's Test Menu list ends at T.13. The page 18 menu tree (above) lists two further tests, T.14 Claw
Test and T.15 Empty Balls Test, which are described on PDF pages 27 and 28. T.3 is `Single
Switch Test` in this list and `Single Switches Test` on page 18 and in its own heading below; T.8 is
`Single Lamps Test` here and in page 18 and `Single Lamp Test` in its own heading on page 26; T.7 is
`Sound & Music Test` here, `Sound and Music Test` on page 18 and in its heading.

> The switch matrix, on the left side of the display, shows the state of all switches. A dot indicates the
> switch is open, a square indicates the switch is closed. The numbers assigned to each switch indicate
> where the switch is located in the matrix. The number on the left indicates the column, the number on
> the right indicates the row. Example - Switch 23 is 2nd column, 3rd row.
>
> A short to ground - on either the row or column wire - appears as a shorted row(s). However, a column
> wire shorted to ground disappears when all of the indicated row switches are open. A row wire shorted
> to ground does not disappear.
>
> A shorted diode in the switch matrix can cause other switches to appear closed. These "phantom"
> switches (though not actually closed), complete a rectangle in the switch matrix. Therefore, if two
> switches in the same column are closed (example; #22 and #24), and a third switch is pressed in another
> column but in the same row as one of the first two (example; #32), the "phantom" switch #34 is falsely
> indicated as closed. The switch with the shorted diode is diagonally opposite the "phantom" switch (in
> this case #22).
>
> T.1 Switch Edges Test Press each switch one at a time. The name and number of the switch is shown in
> the display. If a switch other then the one pressed, or no switch at all is indicated, the system has
> detected a problem with the switch circuit.
>
> T.2 Switch Levels Test This test automatically cycles through all switches that are detected closed.
> The name and number of each switch that is detected is shown in the display. A filled square indicates
> the switch's position in the matrix.
>
> T.3 Single Switches Test The Single Switch Test isolates a particular switch by blocking signals from
> all other switches. Use the Up or Down buttons to select the switch to be tested.

## PDF page 25, printed folio `DEMOLITION MAN 1-15`: T.4 to T.6

> T.4 Solenoid Test The Solenoid Test has three modes - Repeat, Stop, and Run. Only one solenoid should
> pulse at a time. The system has detected a problem if more then one solenoid pulses, a solenoid comes
> on and stays on, or no solenoids pulse during the Repeat or Run modes.
>
> Repeat The Repeat mode pulses a single solenoid. After entering this test, Solenoid 1 shows in the
> display and the corresponding solenoid activates. Press the Up or Down button to cycle through the
> solenoids, one at a time. The same solenoid pulses until the Up or Down button is pressed. Either press
> the Escape button to return to the Test Menu, or press the Enter button to move to the next mode.
>
> Stop The Stop mode halts the Solenoid Test. Press Enter during the Repeat mode and the Solenoid Test
> stops. No solenoids should be activated while the test is stopped. Either press the Escape button to
> return to the Test Menu, or the Enter button to move to the next mode.
>
> Run The Run mode cycles through the solenoids automatically. The display shows the name and number of
> the solenoid currently being pulsed.
>
> T.5 Flasher Test This tests the flashlamp part of the solenoid circuit exclusively. This, like the
> Solenoid Test, has three modes - Repeat, Stop, and Run. During this test only one flashlamp circuit
> should pulse at a time. The system has detected a problem if more then one circuit pulses, a circuit
> stays on, or no circuits pulse during the Repeat or Run modes.
>
> Repeat The Repeat mode pulses a single flashlamp. After entering this test the name and number of the
> first flashlamp circuit shows in the display and the corresponding bulb(s) flash. Press the Up or Down
> buttons to cycle through all of the flashlamps circuits one at a time. The same circuit pulses until
> press the Up or Down button is pressed. Either press the Escape button to return to the Test Menu, or
> press the Enter button to advance to the next mode.
>
> Stop The Stop mode halts the Flasher Test. No flashlamp circuit should be active during this mode.
> Either press the Escape button to return to the Test Menu, or press the Enter button to advance to the
> next mode.
>
> Run The Run mode cycles through the flashlamps automatically. The display shows the name and number of
> the flashlamp circuit currently being pulsed as the corresponding bulb(s) flashes.
>
> T.6 General Illumination Test This test checks all of the General Illumination circuits. There are two
> modes of operation - Stop and Run.
>
> Stop Press the Up or Down buttons to cycle through the General Illumination Test manually. All
> illumination is tested first, followed by an individual circuit test. The circuit name and number shows
> in the display while the corresponding lamps lights. If any other results occur the system has detected
> an error.
>
> Run Press the Enter button any time during Stop mode and the General Illumination Test cycles through
> automatically. For each circuit shown in the display the corresponding bulbs should light. If any other
> results occurs the system has detected a problem.

## PDF page 26, printed folio `DEMOLITION MAN 1-16`: T.7 to T.12 (start)

> T.7 Sound and Music Test The Sound and Music Test checks the audio circuits. This test has three modes
> for testing the sound and music circuits - Run, Repeat, and Stop.
>
> Run The Run mode steps through a sequence of sounds and music. Press the Up or Down buttons during this
> portion of the Sound and Music test to advance to a particular sound or tune without having to wait for
> the program to play all the sounds available in the test. A sound or tune should be heard for each name
> and number that appears in the display. Any other results indicates the system has detected a problem.
>
> Repeat Press the Enter button at any time during the Run mode to cause the program to stop and repeat a
> particular sound/tune. The same sound should repeat continuously until the Up or Down button is
> pressed. Any other results indicates the system has detected a problem.
>
> Stop Press the Enter button at any time during the Repeat mode to stop this test altogether. Nothing
> should be heard. Any other results indicates the system has detected a problem.
>
> T.8 Single Lamp Test The number assigned to each lamp indicates the lamp's position in the matrix. The
> number on the left indicates the column. The number on the right indicates the row. Example - Lamp 23
> means 2nd column, 3rd row.
>
> This test checks each lamp circuit individually. Press the Up or Down button to cycle through this test.
> For each name and number that is shown in the display the corresponding lamp should light. Any other
> results indicates the system has detected a problem.
>
> T.9 All Lamps Test This test causes all the controlled lamps to flash at the same time. Every controlled
> lamp should flash. Any other results indicates the system has detected a problem.
>
> T.10 Lamp and Flasher Test This test causes all the flashlamps and the controlled lamps to flash at the
> same time. The controlled lamps blink, while the flashlamps cycle from highest to lowest. Any other
> results indicates the system has detected a problem.
>
> T.11 Display Test This test automatically checks every dot in the Dot Matrix Display. A series of
> patterns appear in sequence. Each pattern turns on and off a section of dots. Every dot on the matrix
> display should be turned on and off during this test.
>
> T.12 Flipper Coil Test The Flipper Coil Test has three modes - Repeat, Stop, and Run. Only one Flipper
> should pulse at a time. The system has detected a problem if more then one flipper pulses, a flipper
> comes on and stays on, or no flippers pulse during the Repeat or Run modes.
>
> Repeat The Repeat mode pulses a single flipper. After entering this test, flipper coil 01 shows in the
> display and the corresponding coil activates. Press the Up or Down button to cycle through the flipper
> coils, one at a time. The same solenoid pulses until the Up or Down button is pressed. Either press the
> Escape button to return to the Test Menu, or press the Enter button to move to the next mode.

## PDF page 27, printed folio `DEMOLITION MAN 1-17`: T.12 (end), T.13, T.14 Claw Test (start)

> T.12 Flipper Coil Test Continued...
> Stop The Stop mode halts the Flipper Coil Test. Press Enter during the Repeat mode and the test stops.
> No coils should be activated while the test is stopped. Either press the Escape button to return to the
> Test Menu, or the Enter button to move to the next mode.
>
> Run The Run mode cycles through the flippers automatically. The display shows the name and number of
> the flipper coil currently being pulsed.
>
> T.13 Ordered Lamps Test The number assigned to each lamp indicates the lamp's position in the matrix.
> The number on the left indicates the column. The number on the right indicates the row. Example - Lamp
> 23 means 2nd column, 3rd row.
>
> This test checks each lamp circuit individually. Press the Up or Down button to cycle through the
> lamps. Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of the
> playfield. Direction depends on which button, Up or Down, is pressed. For each name and number that is
> shown in the display the corresponding lamp should light. Any other results indicates the system has
> detected a problem.
>
> T.14 Claw Test The Claw test aids in troubleshooting the Cryoclaw/Elevator mechanism. The claw test
> provides several functions for activating the mechanism, while simultaneously displaying the states of
> the opto switches associated with the mechanism. For more information on claw operation, see Theory of
> Operation.
>
> Switch display -
> The states of the following switches are constantly monitored and displayed during the Claw test:
> Elevator Index, Elevator Hold, Claw Left, Claw Right. The box next to each switch name contains an X
> when the switch is activated (blocked).
>
> Claw Test Functions
> Use the diagnostic Up and Down buttons to step through the available Claw test functions. The functions
> operate only when the diagnostic Enter button is pressed. When a function is active its name is
> inverted on the display screen. To stop claw function at any time simply release the Enter button.
>
> Auto Run
> During the Auto Run function the elevator is continuously monitored for the presence of a pinball. When
> a ball is placed on the platform the test cycles the claw and the elevator causing the ball to be
> picked up by the claw magnet and dropped on the far left ramp.
>
> Claw Left
> The Claw Left function moves the claw arm to the left (away from the elevator). This function does not
> move the arm out of range.
>
> Claw Right
> The Claw Right function moves the claw arm to the right (toward the elevator). This function does not
> move the arm out of range.
>
> To move the claw arm when it is out of range select Claw Left or Claw Right, as appropriate, and hold in
> either flipper button before pressing Enter. Do not move the claw arm by hand.
>
> Run Elevator
> The Run Elevator function runs the elevator motor continuously.

The heading `T.12 Flipper Coil Test Continued...` is printed in bold italic; the paragraph `To move the claw
arm when it is out of range ...` is printed in italic.

## PDF page 28, printed folio `DEMOLITION MAN 1-18`: T.14 Claw Test (end), T.15

> Park Elevator
> The Park Elevator function runs the elevator motor until the elevator index position is detected. The
> motor is then shut off.
>
> Magnet On
> The Magnet On function turns on the claw magnet. The magnet is turned on solidly for a short period and
> then pulsed for a longer period. The Magnet On function times out after several seconds and shuts off
> the magnet to avoid overheating it.
>
> Claw Test Error Messages
> During the various claw test functions the CPU may detect an error condition. The messages are
> explained below.
>
> Elevator Error
> The Claw test displays this message when the elevator motor is running and the elevator index switch is
> not detected after several seconds.
>
> Claw Out of Range
> The Claw test displays this message when it detects that the claw arm is out of range (see Theory of
> Operation later in this section).
>
> To move the claw arm when it is out of range select Claw Left or Claw Right, as appropriate, and hold in
> either flipper button before pressing Enter. Do not move the claw arm by hand.
>
> Claw Movement Error
> The Claw test displays this message when the claw motor is running and neither position switch is
> detected after several seconds.
>
> Magnet Error
> The Claw test displays this message after it has tried several times to pick up the ball from the
> elevator.
>
> T.15 Empty Balls Test The Empty Balls test clears all balls from any lock-up device, including the
> outhole trough. Press the Enter button to begin the test and the Escape button to stop it.

The `To move the claw arm when it is out of range ...` paragraph is printed in italic, as on page 27.

## PDF page 46, printed folio `DEMOLITION MAN 1-36`: ERROR MESSAGES (start)

> ERROR MESSAGES
>
> The WPC game program has the capability to aid the operator and service personnel. At game turn-on, or
> after pressing the Begin Test switch, once the game has been operating for an extended period, the
> display may signal with a message, "Press ENTER for Test Report". This indicates the game program has
> detected a possible problem with the game.
>
> To obtain details of the problem open the coin door and press the Begin Test switch. Press the Enter
> button to begin displaying the message(s). The following messages apply to your game.
>
> Check Switch ##.
> This message indicates that at least one switch was stuck 'On' at game turn-on or has NOT been actuated
> during ball play (for 90 balls or ≈30 games). The game program compensates the game play requirements
> affected by each disabled switch to allow 'nearly normal' play. This helps keep your game earning, until
> the service technician can repair the problem.
>
> To verify the problem, refer to the Test Menu text describing Switch Testing, and check each reported
> switch using applicable switch tests. Always check switch operation using a ball, to simulate game
> conditions. Switch problems may often be resolved by adjusting the wire switch actuators, fixing switch
> circuitry problems, securing loose connectors, etc. Mechanisms using 'opto switches' (drop targets,
> etc.) need to be checked for proper power connections (+12V dc and ground).
>
> Pinball Missing.
> This game normally uses six balls, however, it will operate with less. This message announces that a
> ball is missing or stuck. When the ball is located, return it to the game via the Outhole. Other
> possibilities for this problem could be malfunctions of the Ball Trough switches or the Ball Shooter
> switch.
>
> xxxxx Sw. Is Stuck On.
> This message indicates that a switch, which is not usually On, remains in the On position after the game
> is switched On. The stuck switch is essential for game play (for example, a coin chute switch, the slam
> tilt switch, the plumb bob tilt switch), and should be cleared to permit proper game operation.
>
> Ground Short Row-N, Wht-xxx.
> This message indicates that the switch wires being called out are touching a grounded part on the
> playfield or coin door. The following should be checked:
> 1. Slam tilt (or other coin door switch) touching the grounded coin door.
> 2. A leaf-type, playfield switch touching a grounded part.
> 3. Players poking metallic objects (wires, coat hangers, etc.) into the game.
> 4. Switch cable insulation pierced or damaged allowing bare wire contact with a grounded part.
> 5. All switches in a row closing at the same time. Note: This is NOT a switch problem; however, for most
> games it is a very rare possibility.
>
> U6 Checksum Error.
> The game ROM checksum is invalid. If this occurs replace the game ROM.
>
> Time and Date Not Set.
> The real time clock is not running. Go to U.4 of the Utilities Menu and set the time and date.

Internal disagreement: this page says `This game normally uses six balls`, while the assembly page (PDF
page 12, `DEMOLITION MAN 1-2`) is headed `IS A 5 BALL GAME.` and step 11 on PDF page 13 says `This game
uses five balls.` The `≈` in `≈30 games` is read from the render as an approximately-equal sign.

## PDF page 47, printed folio `DEMOLITION MAN 1-37`: Factory Settings Restored, Opto Theory, CPU LEDs, beep codes

> Factory Settings Restored.
> This message indicates that the CMOS RAM (U8) no longer retains any custom Pricing or Game Adjustment
> settings and has reverted to factory default settings. Generally, the following CPU checks will isolate
> the cause of the CMOS RAM memory failure. The voltages at pin 28 and pin 26 of U8 should be +5V (game
> turned On) and at least +4V (game turned Off). When the voltage drops below +4V, memory reset occurs.
> Check the batteries and battery holder. Be sure that the batteries are good and that there is no
> contamination on the battery holder terminals. Turn the game OFF, and use an ohmmeter to check diodes D1
> and D2 on the CPU Board. D1 should read 0 ohms when forward-biased and infinite ohms when
> reverse-biased. D2 should read 15 ohms when forward-biased and infinite ohms when reverse-biased.
> (Readings taken with an analog meter.)This message can also indicate that there is an open diode on a
> 50V coil and noise is entering the circuit.
>
> Opto Theory
> The opto receiver (Photo Transistor) should be approximately 0.1 - 0.7 volts when the opto beam is
> unblocked and approximately 11 - 13 volts when the opto beam is blocked. The opto transmitter (LED)
> should always be approximately 1.4 volts. Note: The transmitter (LED) is larger than the receiver (Photo
> Transistor); it protrudes further from its case.

Drawing labels for the opto drawing, left to right: `LED Board Transmitter` with `1.0 - 1.4 Volts`; board
terminal labels `A` and `K`; wire-colour labels `GREEN` (top), `GRAY` and `BLACK` (bottom, two lead wires),
`WHITE` (top of the transmitter side view); `SOLDER` on the board; `INFRARED BEAM` (arrow from the
transmitter side view to the receiver side view); receiver side view labelled `BLACK` at the top;
`Photo Transistor Board Receiver` with `0.1 - 0.7 Volts Unblocked` and `11 - 13 Volts Blocked`; board
terminal labels `C` and `E`; wire-colour labels `BLUE` (top), `GRAY` and `ORANGE` (bottom); `SOLDER`.
The text says the transmitter is approximately 1.4 volts while the drawing prints `1.0 - 1.4 Volts`.

> CPU L.E.D.'s
> The CPU has three L.E.D.s located on the upper left side of the board D19, D20, and D21. On game power-up
> D19 and D21 turn on for a moment then, D19 turns off and D20 starts to blink rapidly. D21 remains on.
> The system has detected a problem if the following happens:
>
> CPU Board L.E.D. Error Codes

| Condition | | Meaning |
| --- | --- | --- |
| Center L.E.D. blinks one time | - | U6 ROM Failure |
| Center L.E.D. blinks two times | - | U8 RAM Failure |
| Center L.E.D. blinks three times | - | U9 Custom Chip Failure |

> Sound Board Beep Error Codes Upon Game Turn-On:

| Beeps | | Meaning |
| --- | --- | --- |
| 1 Beep | = | Sound Board O.K. |
| 2 Beeps | = | U2 Failure |
| 3 Beeps | = | U3 Failure |
| 4 Beeps | = | U4 Failure |
| 5 Beeps | = | U5 Failure |
| 6 Beeps | = | U6 Failure |
| 7 Beeps | = | U7 Failure |
| 8 Beeps | = | U8 Failure |
| 9 Beeps | = | U9 Failure |

## PDF page 48, printed folio `DEMOLITION MAN 1-38`: Cryoclaw/Elevator Theory of Operation and error messages

> Cryoclaw/Elevator
>
> THEORY OF OPERATION
>
> The Cryoclaw/Elevator mechanism consists of two gear-reduced motors controlled by the game CPU. Several
> opto switches are used to detect the positioning of the motors. Attached to the claw is an
> electromagnet, which is used to pick up the pinball during game play.
>
> Elevator:
> The elevator motor runs in only one direction. The CPU pulses the motor control input, rather than
> turning it on solid, in order to slow its speed. The elevator has a single opto (index) switch for
> detecting the DOWN position of the elevator. Due to the inertia of the motor, it is normal for the
> elevator motor to be stopped with the switch activator just beyond the index switch.
>
> Claw:
> The claw motor runs in both directions. The CPU pulses the motor control inputs to vary the speed of the
> claw arm. The claw has two opto switches for detecting the position of the claw arm. The switch states
> for the arm positions are:

| Claw Right Switch | Claw Left Switch | Arm position |
| --- | --- | --- |
| OFF (blocked) | OFF (blocked) | arm out of range |
| OFF (blocked) | ON (open) | arm at right (above the elevator) |
| ON (open) | OFF (blocked) | arm at left (away from elevator) |
| ON (open) | ON (open) | arm within range of motion |

The third column has no printed header; the labels are printed to the right of the two switch columns.

> When both position switches are OFF (blocked) the CPU cannot determine the position of the arm. In this
> case, the CPU will not turn on the claw motor, since it does not know whether to move the arm to the
> left or the right. To reposition the arm when it is out of range, use the CLAW TEST. Do not attempt to
> move the claw by hand.
>
> Note that if the position switches are disconnected, the CPU will think that the claw arm is out of
> range.
>
> During game play, the Cryoclaw/Elevator is operated both automatically, and under player control. During
> multiball play, the claw is always operated automatically. The claw is also operated automatically
> during ball search.
>
> The CPU monitors the operation of the Cryoclaw/Elevator to detect malfunctions. When the CPU has
> detected a malfunction, it will not open the diverter on the right ramp leading to the
> Cryoclaw/Elevator. The Cryoclaw/Elevator can also be disabled by option setting, in case of an
> intermittent error.
>
> ERROR MESSAGES
>
> The game test report will display an error message when the CPU has detected a malfunction of the
> Cryoclaw/Elevator. These error messages are explained below.
>
> Claw Disabled
> This message is displayed when the Cryoclaw/Elevator is disabled by option adjustment.
>
> Arm Out of Range
> This message is displayed when the claw arm is positioned out of range. This message can also be caused
> by one or more broken claw position opto switches.
>
> Elevator Broken
> This message is displayed when the CPU cannot detect an activation of the elevator index opto switch.
> This can be caused by either a broken switch, or a non-functional elevator motor.

The heading `Cryoclaw/Elevator` is underlined in the render.

## PDF page 49, printed folio `DEMOLITION MAN 1-39`: Cryoclaw/Elevator error messages (end)

> Magnet Broken
> This message is displayed when the game is unable to pick up a ball from the elevator platform with the
> claw magnet. This can be caused by the magnet being non-functional, or by the Elevator Hold switch being
> broken.
>
> Claw Motor Error
> This message is displayed when the CPU is unable to detect movement of the claw arm. This can be caused
> by a non-functional claw motor, or either of the position optos being broken.
>
> Ramp Diverter Is Stuck Open
> This message is displayed when the CPU detects balls going to the Cryoclaw/Elevator when it expects the
> diverter to be closed, and thus directing balls down the right ramp.
>
> Ramp Diverter Is Stuck Closed
> This message is displayed when the CPU detects balls rolling down the right ramp when it expects the
> diverter to be open, and thus directing balls to the Cryoclaw/Elevator.

Nothing else is printed on the page.
