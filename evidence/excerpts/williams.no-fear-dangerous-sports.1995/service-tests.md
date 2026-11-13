# No Fear: Dangerous Sports — Test menu, service tests and error messages

From `Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf` (operations manual 16-50025-101, April 1995, a 144-page scan without a text layer; SHA-256 `176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b`), PDF pages 28-39 (printed 1-8 to 1-18, menu system and T.1-T.20) and 61-63 (1-41 to 1-43, error messages and opto theory). Transcribed by a delegated reader from the 200 dpi renders, with Windows OCR text where the reading basis says so; not yet checked line by line against the page by the curator. Reading basis per item: "image" = read from the 200 dpi render; "OCR+" = Windows OCR text with part numbers and key words partly checked against the image; "OCR" = OCR text only. Cells are kept as printed, including misspellings and abbreviations; `—` marks a cell that is blank on the page. `p-NNN` is the PDF page; the printed page number follows it.

## 1. Service tests (p-028..p-039)

### Menu (p-028, folio 1-8; OCR+, test list also image-checked on p-033)
"The Main Menu allows you to choose from several categories, which in turn lead to other menus to choose from. To access the Main Menu, open the coin door and press the Begin Test button, then press the Enter button. Press the Up or Down buttons to cycle through the Main Menu. Press the Enter button to access a menu. Press the Escape button to return to the Main Menu. Press the Start button for HELP at any time." Main menu groups: B. BOOKKEEPING MENU (B.1..B.6), P. PRINTOUTS MENU (P.1..P.8), T. TEST MENU, U. UTILITIES MENU (U.1..U.11), A. ADJUSTMENT MENU (A.1..A.5).

### T. TEST MENU (p-033, folio 1-13; image-checked list; body OCR+)
"Use the Service Switch Actuator to hold in the top interlock switch located in the bottom left corner of the coin door opening. The actuator must be in place in order to activate the solenoids and flashlamps."
"Press the Up or Down buttons to cycle through the menu. Press the Enter button to access a test. Press the Escape button to return to the Test menu. Note: During any test, press the Start button to obtain the wire color, driver number, connector number and fuse location."
List: T.1 Switch Edges Test; T.2 Switch Levels Test; T.3 Single Switch Test; T.4 Solenoid Test; T.5 Flasher Test; T.6 General Illumination Test; T.7 Sound & Music Test; T.8 Single Lamps Test; T.9 All Lamps Test; T.10 Lamps And Flasher Test; T.11 Display Test; T.12 Flipper Coil Test; T.13 Ordered Lamps Test; T.14 Lamp Row-Col; T.15 DIP Switch Test; T.16 Accelerated Ball Test; T.17 Drop Target Test; T.18 Underground Trough Test; T.19 Skull Test; T.20 Empty Balls Test. (p-028 menu lists T.16 as "Ball Accelerator Test"; p-033 prints "Accelerated Ball Test"; p-036 heading "Ball Accelerator Test".)
Switch matrix text: "The switch matrix, on the left side of the display, shows the state of all switches. A dot indicates the switch is open, a square indicates the switch is closed. The numbers assigned to each switch indicate where the switch is located in the matrix. The number on the left indicates the column, the number on the right indicates the row. Example - Switch 23 is 2nd column, 3rd row."
T.1 Switch Edges Test: "Press each switch one at a time. The name and number of the switch is shown in the display. If a switch other then the one pressed, or no switch at all is indicated, the system has detected a problem with the switch circuit."
T.2 Switch Levels Test: "This test automatically cycles through all switches that are detected closed. The name and number of each switch that is detected is shown in the display. A filled square indicates the switch's position in the matrix."
T.3 Single Switches Test: "The Single Switch test isolates a particular switch by blocking signals from all other switches. Use the Up or Down buttons to select the switch to be tested."

### T.4 Solenoid Test (p-034, folio 1-14; image)
"The Solenoid test has three modes - Repeat, Stop, and Run. Only one solenoid should pulse at a time. The system has detected a problem if more then one solenoid pulses, a solenoid comes on and stays on, or no solenoids pulse during the Repeat or Run modes."
"Repeat: The Repeat mode pulses a single solenoid. After entering this test, solenoid one shows in the display and the corresponding solenoid activates. Press the Up or Down button to cycle through the solenoids, one at a time. The same solenoid pulses until the Up or Down button is pressed. Either press the Escape button to return to the Test menu, or press the Enter button to move to the next mode."
"Stop: The Stop mode halts the Solenoid test. Press Enter during the Repeat mode and the Solenoid test stops. No solenoids should be activated while the test is stopped. Either press the Escape button to return to the Test menu, or the Enter button to move to the next mode."
"Run: The Run mode cycles through the solenoids automatically. The display shows the name and number of the solenoid currently being pulsed."

### T.5 Flasher Test (p-034, folio 1-14; image)
"This tests the flashlamp part of the solenoid circuit exclusively. This, like the Solenoid test, has three modes - Repeat, Stop, and Run. During this test only one flashlamp circuit should pulse at a time. The system has detected a problem if more then one circuit pulses, a circuit stays on or no circuits pulse during the Repeat or Run modes."
"Repeat: The Repeat mode pulses a single flashlamp. After entering this test the name and number of the first flashlamp circuit shows in the display and the corresponding bulb(s) flash. Press the Up or Down buttons to cycle through all of the flashlamps circuits one at a time. The same circuit pulses until press the Up or Down button is pressed. Either press the Escape button to return to the Test menu, or press the Enter button to advance to the next mode."
"Stop: The Stop mode halts the Flasher test. No flashlamp circuit should be active during this mode. Either press the Escape button to return to the Test menu, or press the Enter button to advance to the next mode."
"Run: The Run mode cycles through the flashlamps automatically. The display shows the name and number of the flashlamp circuit currently being pulsed as the corresponding bulb(s) flashes."

### T.6 General Illumination Test (p-034, folio 1-14; image)
"This test checks all of the General Illumination circuits. There are two modes of operation - Stop and Run."
"Stop: Press the Up or Down buttons to cycle through the General Illumination test manually. All illumination is tested first, followed by an individual circuit test. The circuit name and number shows in the display while the corresponding lamps lights. If any other results occur the system has detected an error."
"Run: Press the Enter button any time during Stop mode and the General Illumination test cycles through automatically. For each circuit shown in the display the corresponding bulbs should light. If any other results occurs the system has detected a problem."

### T.7 Sound and Music Test (p-035, folio 1-15; OCR only, partly garbled)
"The Sound and Music test checks the audio circuits. This test has three [modes] for sound and music circuits - Run, Repeat, and Stop." Run: steps through a sequence of sounds and music; Repeat: Enter during Run repeats a sound; Stop: "Nothing should be heard." (not transcribed verbatim; OCR corrupt.)

### T.8 Single Lamp / T.9 All Lamps / T.10 / T.11 (p-035, folio 1-15; OCR+, partly garbled)
- "Single Lamp Test  The number assigned to each lamp indicates the lamp's position in the matrix. The number on the left indicates the column. The number on the right indicates the row. [Lamp 23] means 2nd column, 3rd row. This test checks each lamp circuit individually. Press the Up or Down button [to] cycle [through the] test. For each name and number that is shown in the display the corresponding lamp [should] light. Any other results indicates the system has detected a problem."
- "All Lamps Test  This test causes all the controlled lamps to flash at the same time. Every controlled lamp [should] flash. Any other results indicates the system has detected a problem."
- "T.10 Lamp and Flasher Test  This test causes all the flashlamps and the controlled lamps to flash at the same time. [The] controlled lamps blink, while the flashlamps cycle from highest to lowest. Any other [results] indicates the system has detected a problem."
- "T.11 Display Test  This test automatically checks every dot in the Dot Matrix Display board. A series of [patterns] appear in sequence. Each pattern turns on and off a section of dots. Every dot on [the] display should be turned on and off during this test."
(Square brackets = words lost in OCR, supplied only where structurally obvious; verify against image before quoting.)

### T.12 Flipper Coil Test (p-036, folio 1-16; image)
"The Flipper Coil test has three modes - Repeat, Stop, and Run. Only one flipper should pulse at a time. The system has detected a problem if more then one flipper pulses, a flipper comes on and stays on, or no flippers pulse during the Repeat or Run modes."
"Repeat: The Repeat mode pulses a single flipper. After entering this test, flipper coil 01 shows in the display and the corresponding coil activates. Press the Up or Down button to cycle through the flipper coils, one at a time. The same solenoid pulses until the Up or Down button is pressed. Either press the Escape button to return to the Test menu, or press the Enter button to move to the next mode."
"Stop: The Stop mode halts the Flipper Coil test. Press Enter during the Repeat mode and the test stops. No coils should be activated while the test is stopped. Either press the Escape button to return to the Test menu, or the Enter button to move to the next mode."
"Run: The Run mode cycles through the flippers automatically. The display shows the name and number of the flipper coil currently being pulsed."

### T.13 / T.14 / T.15 (p-036, folio 1-16; image)
"T.13 Ordered Lamps Test  The number assigned to each lamp indicates the lamp's position in the matrix. The number on the left indicates the column. The number on the right indicates the row. Example - Lamp 23 means 2nd column, 3rd row. This test checks each lamp circuit individually. Press the Up or Down button to cycle through the lamps. Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of the playfield. Direction depends on which button, Up or Down, is pressed. For each name and number that is shown in the display the corresponding lamp should light. Any other results indicates the system has detected a problem."
"T.14 Lamp Row-Col  This test allows individual rows and columns in the lamp matrix to be operated. This is useful for trouble-shooting wiring and driver problems. Press the Up and Down buttons to cycles through the different rows and columns."
"T.15 DIP Switch Test  This test is used to show the positions of the DIP switches on the CPU board (U27)."

### T.16 Ball Accelerator Test (p-036 folio 1-16 and continuation p-037 folio 1-17; image)
"This tests the accelerator's ability to throw the ball up the ramp. During this test, if any of the three opto switches on the ramp (#46, #47, or #48) do not work, a message, shown on the display, will indicate the broken switch(es). Each opto switch must be working properly for the corresponding magnet to be able to capture and throw the ball."
"While this test is active, a ball thrown up the ramp is accelerated. The display shows the state of the opto switches and the magnet coils."
Continued (p-037): "During this test, the diagnostic test buttons on the coin door act as follows: Escape - Returns to the previous menu. Up - Chooses the next magnet. Down - Chooses the previous magnet. Enter - Activates/Deactivates the magnet for acceleration"

### T.17 Drop Target Test (p-037, folio 1-17; image)
"This test has three modes - Repeat, Stop, and Run. These modes allow the target to be activated while the state of the drop target's switch is shown on the display. During this test, if the drop targets switch (#51) does not work, a message, shown on the display, indicates the broken switch."
"Repeat: The Repeat test pulses either the Drop Target Up coil or the Drop Target Down coil, until the Up or Down button is pressed to move to the next coil."
"Stop: The drop target coils are not activated."
"Run: The Run test cycles the Drop Target Up coil and the Drop Target Down coil automatically."
"During this test, the diagnostic test buttons on the coin door act as follows: Escape - Returns to the previous menu. Up - During Repeat: changes to the next coil. Down - During Repeat: changes to the previous coil. Enter - Cycles the test between the three modes: Repeat, Stop, and Run."

### T.18 Underground Trough Test (p-037 folio 1-17, continuation p-038 folio 1-18; image)
"This test may be used to test all of the critical switches in the trough leading from the top of the playfield (behind the drop target and under the skull) to the lower right popper. The display shows the four critical switches that are in the ball's path. During this test, if any of these switches do not work (#37, #38, #41, or #42), a message, shown on the display, indicates the broken switch(es). The test has two modes - Automatic and Manual."
"Automatic: The automatic operation allows a ball to be cycled through the trough automatically, with the state of each switch being displayed."
"Manual: Manual operation will not eject balls from the right popper or the lower trough; it relies on the operator to check the switches manually and/or feed balls by hand."
"During this test, the diagnostic test buttons on the coin door act as follows: Escape - Returns to the previous menu. Up - Does nothing. Down - Does nothing. Enter - Cycles the type of operation between automatic and manual."
"Errors during automatic operation:"
"Unable To Load Underground Trough  This error occurs when a ball is plunged from the auto-plunger and is not seen in the underground trough."
Continued p-038: "Left Trough Entrance Not Seen  This error occurs during the automatic test when the ball is plunged and seen by the center entrance opto, but not seen by the drop target entrance."
"Center Trough Entrance Not Seen  This error occurs during the automatic test when the ball is plunged and seen by the left entrance opto and the right popper opto, but not seen by the center trough entrance."
"Popper Opto 2 Not Seen  This error occurs during automatic test when the ball is plunged and seen by the center entrance opto and the right popper 1 opto, but not seen by the right popper 2 opto."
"Popper Opto 1 Not Seen  This error occurs during automatic test when the ball is plunged and seen by the center entrance opto and the right popper 2 opto, but not seen by the right popper 1 opto after several seconds."

### T.19 / T.20 (p-038, folio 1-18; image)
"T.19 Skull Test  This test exercises the skull by cycling through several speech calls."
"T.20 Empty Balls  This test kicks out all balls loaded in troughs, lockups, poppers, and kickouts until no balls remain in those locations. Note - As balls roll down the playfield and into the outhole, they will be continually kicked out of the trough."

## 2. Error messages and opto theory (p-061..p-063)

p-061 (folio 1-41 presumed; OCR+): "ERROR MESSAGES  The WPC game program has the capability to aid the operator and service personnel. At game turn-on, or after pressing the Begin Test switch, once the game has been operating for an extended period, the display may signal with a message, "Press ENTER for Test Report". This indicates the game program has detected a possible problem with the game. To obtain details of the problem open the coin door and press the Begin Test switch. Press the Enter button to begin displaying the message(s). The following messages apply to your game."
- "Check Switch ##. This message indicates that at least one switch was stuck 'On' at game turn-on or has NOT been actuated during ball play (for 90 balls or apx. 30 games). The game program compensates the game play requirements affected by each disabled switch to allow 'nearly normal' play. ... Mechanisms using 'opto switches' (drop targets, etc.) need to be checked for proper power connections (+12V dc and ground)."
- "Check Fuses F115 and F116 and Opto 12V Supply  This message will be displayed if the game senses that all optical switches are not functioning. This usually occurs when there is no 12V supply to the playfield optics. The problem is likely to be a blown fuse (F115 or F116), or at connectors J112, J116, J117 or J118 on the power driver board." (fuse numbers OCR "Fl 15/Fl 16"; read as F115/F116, unverified.)
- "Opto Trough Bad Check Connectors, Wires and 12V Supply.  This message will be displayed if all of the optics in the playfield ball trough are not functioning. This is usually caused by a problem with a ball trough connector supplying 12V and ground for the optical circuits."
- "Pinball Missing.  This game normally uses four balls, however, it will operate with less. This message announces that a ball is missing or stuck. When the ball is located, return it to the game via the Outhole. Other possibilities for this problem could be malfunctions of the Ball Trough switches or the Ball Shooter switch."
- "xxxxx Sw. is Stuck On.  This message indicates that a switch, which is not usually On, remains in the On position after the game is switched On. The stuck switch is essential for game play (for example, a coin chute switch, the slam tilt switch, the plumb bob tilt switch), and should be cleared to permit proper game operation."
p-062 (folio 1-42; OCR+): "Ground Short Row-N, Wht-xxx" (switch wires touching a grounded part; five checks), "U6 Checksum Error. The game ROM checksum is invalid. If this occurs replace the game ROM.", "Time and Date Not Set", "Factory Settings Restored", CPU LEDs D19, D20, D21 and codes: "Center L.E.D. blinks one time U6 ROM Failure [OCR '136']; two times U8 RAM Failure; three times U9 Custom Chip Failure". Sound Board beep codes: 1 beep Sound Board O.K.; 2 U2; 3 U3; 4 U4; 5 U5; 6 U6; 7 U7; 8 U8; 9 U9 Failure (OCR). No message on these pages names a No Fear-specific switch, opto or mechanism beyond the generic opto messages above.
p-063 (folio 1-43; image): "Opto Theory  The opto receiver (Photo Transistor) should be approximately 0.1 - 0.7 volts when the opto beam is unblocked and approximately 11 - 13 volts when the opto beam is blocked. The opto transmitter (LED) should always be approximately 1.4 volts. Note: The transmitter (LED) is larger than the receiver (Photo Transistor); it protrudes further from its case." Diagram labels: "LED Board Transmitter 1.0-1.1 Volts" [as printed, image reads "1.0-1.1"], "Photo Transistor Board Receiver 0.1-0.7V Unblocked 11-13V Blocked", wire labels Green, WHT, BLK, Blue, Gray-XXX, Black, Gray-Yellow, Orange-XXX, "Infrared Ray".

## Transcription notes

- p-035 (T.7 to T.11 text): OCR is badly corrupted; bracketed words in the transcription are inferred. Re-read the image before quoting.
- p-061 fuse labels "Fl 15"/"Fl 16" read as F115/F116 (OCR only). Connectors J112, J116, J117, J118 also OCR only.
- p-062 CPU LED code "136 ROM Failure" is likely "U6 ROM Failure" (OCR); sound board beep list digits are OCR.
- p-061 to p-063 folio numbers (1-41 for p-061) inferred from the sequence (1-42 and 1-43 are printed on p-062/p-063).
