# Safe Cracker — Test Menu and Mechanism Tests
Windows OCR (Windows.Media.Ocr over 200 dpi renders of `Bally_1996_Safe_Cracker_Manual.pdf`, which has no text layer), laid out by word position and reproduced as recognized: OCR character errors are left in place and runs of spaces collapsed. It is unreviewed OCR; every device fact the definition takes from these pages was read against the rendered page or confirmed by the ROM's own service tests. PDF pages 32-36, printed 1-16 to 1-20: the Test menu and the T.1-T.22 descriptions of the manual's software revision, whose T.16 Wheel Test and T.17-T.22 numbering differ from the retained 1.8 ROM's menu.

## PDF page 32

```
 Use the Service Switch Actuator to hold in the top interlock switch located in the bottom left
 of the coln door opening. The actuator must be in place in order to activate the solenoids
 corner
 and flashlamps.
 Press the up Down buttons to cycle through the menu. Press the Enter button to access a test. Press
 or
 the Escape button to return to the Test Menu.
 Note: During any test, press the Start button to obtain the wire color, driver number, connector number
 and fuse location.
 T. TEST MENU
 T.I Switch Edges
 T.2 Switch Levels
 Single Switch
 Solenoid Test
 Flasher Test
 General Illumination
 T.7 Sound & Music Test
 T.8 Single Lamps
 T.9 All Lamps
 T.IO Lamp & Flasher Tests
 T.II Display Test
 T.12 Flipper Test
 T.13 Ordered Lamps Test
 T.14 Lamp Row-Col Test
 T.15 Dip Switch Test
 T.16 Wheel Test
 T.17 Vari Target Test
 T.18 Token Tube Test
 T.19 Light Rope Test
 T.20 3-Bank Drop Target Test
 T.21 Top Trough Test
 T .22 Empty Balls Test
 The switch matrix, the left side of the display, shows the state of all switches. A dot indicates
 on
 the switch is open, and indicates the switch is closed. The numbers assigned to each switch
 a square
 indicate where the switch is located in the matrix. The number on the left indicates the column, and the
 number the right indicates the row. Example: Switch 23 is 2nd column, 3rd row.
 on
 A short to ground, either the column wire, appears as a shorted row(s). However, a
 on row or
 column wire shorted to ground disappears when all the indicated row switches are open. A row wire
 shorted to ground does not disappear.
 A shorted diode in the switch matrix can cause other switches to appear closed. These
 "phantom" switches (though not actually closed) complete a rectangle in the switch matrix. Therefore, if
 two switches in the column closed (example; #22 and #24), and a third switch is pressed in
 same are
 another column but in the of the first two (example; #32), the "phantom" switch #34 is
 same row as one
 falsely indicated closed. The switch with the shorted diode is diagonally opposite the "phantom
 as
 switch (in this case #22).
 T.I Switch Edges Press each switch one at a time. The name and number of the switch is
 shown in the display. If switch other than the one pressed, or no switch at all is indicated, the
 a
 system has detected a problem with the switch circuit.
 T.2 Switch Levels This test automatically cycles through all switches that are detected
 closed. The and number of each switch that is detected is shown in the display. A filled
 name
 square indicates the switch's position in the matrix.
 1-16
```

## PDF page 33

```
 T.3 Single Switches The Single Switch Test isolates a particular switch by blocking signals
 from all other switches. Use the up or Down buttons to select the switch to be tested.
 T.4 Solenoid Test The Solenoid Test has three modes: Repeat, Stop, and Run. Only one
 solenoid should pulse at a time. The system has detected a problem if; more then one solenoid
 pulses, solenoid comes On and stays On, or no solenoids pulse during the Repeat or Run
 a
 modes.
 Repeat The Repeat Mode pulses a single solenoid. After entering this test, Solenoid 1 shows in
 the display. and the corresponding solenoid activates. Press the Up or Down button to
 cycle through the solenoids, one at a time. The same solenoid pulses until the Up or
 Down button is pressed. Either press the Escape button to return to the Test Menu, or
 press the Enter button to advance to the next mode.
 Stop The Stop Mode halts the Solenoid Test. Press Enter during the Repeat mode and the
 Solenoid Test Stops. No solenoids should be activated while the test is stopped. Either
 press the Escape button to return to the Test Menu, or the Enter button to advance to the
 next mode.
 Run The Run Mode cycles through the solenoids automatically. The display shows the name
 and number of the solenoid currently being pulsed. Either press the Escape button to
 return to the Test Menu, or the Enter button to advance to the next mode.
 T.5 Flasher Test This tests the flashlamp part of the solenoid circuit exclusively. This, like
 the Solenoid Test has three test modes: Repeat, Stop, and Run. During this test, only one
 flashlamp circuit should pulse at a time. The system has detected a problem if more than one
 circuit pulses, a circuit stays On, or no circuits puise during the Repeat or Run modes.
 Repeat The Repeat mode pulses a single flashlamp. After entering this test, the name and
 number of the first flashlamp circuit will show in the display and the corresponding
 bulb(s) flash. Press the Up or Down button to cycle through all of the flashlamp circuits
 at time. The same circuit pulses until the Up or Down button is pressed. Either
 one a
 press the Escape button to return to the Test Menu, or press the Enter button to advance
 to the next mode.
 Stop The Stop Mode halts the Flasher Test. No flashlamp circuit should be active during this
 mode. Either press the Escape button to return to the Test Menu, or the Enter button to
 advance to the next mode.
 Run The Run Mode cycles through the flashlamps automatically. The display shows the
 name and number of the flashlamp circuit currently being pulsed and the corresponding
 bulb(s) flash. Either press the Escape button to return to the Test Menu, or the Enter
 button to advance to the next mode.
 1-17
```

## PDF page 34

```
 T .6 General Illumination This test checks all of the General Illumination circuits. There
 are two
 modes of operation: Stop and Run. Note: G.I strings 4 and 5 do not dim and brighten, they
 are always ON.
 Stop Press the Up or Down buttons to cycle through the General Illumination Test manually.
 All illumination is tested first, followed by an individual circuit test. The circuit and
 name
 number will show in the display while the corresponding lamps light. If any other results
 occur the system has detected an error.
 Run Press the Enter button any time during Stop mode and the General Illumination Test
 cycles through automatically. For each circuit shown in the displays the corresponding
 bulbs should light. If any other results occurs the system has detected problem.
 a
 T.7 Sound and Music Test The Sound and Music Test allows to check the
 you audio
 circuits. This test has three modes for testing the sound and music circuits: Run, Repeat, and
 Stop.
 Run The Run Mode steps through a sequence of sounds and music. Pressing the Up
 or
 Down button during this portion of the Sound and Music test advances to particular
 a
 sound/tune without having to wait for the program to play all the sounds available in the
 test. A sound/tune should be heard for each name and number that appears in the
 display. Any other results indicate the system has detected problem.
 a
 Repeat Press the Enter button at any time during the Run Mode to the to stop
 cause program
 and repeat a particular sound/tune. The same sound should repeat continuously until
 the Up or Down button is pressed. Any other results indicates the system has detected
 a
 problem.
 Stop Press the Enter button at any time during the Repeat Mode to stop this test altogether.
 No sound/tune should be heard. Any other results indicates the system has detected
 a
 problem.
 T .8 Single Lamp Test The number assigned to each lamp indicates the lamp's position in the
 matrix. The number on the left indicates the column. The number the right indicates the
 on row.
 Example: Lamp 23 means 2nd column, 3rd row.
 This test checks each lamp circuit individually. Press the Up Down button to cycle through this
 or
 test. For each name and number that is shown in the display the corresponding lamp should
 light. Any other results indicate the system has detected a problem.
 T .9 All Lamps Test This test all the controlled lamps flash the
 causes to at same time. Every
 controlled lamp should flash. Any other results indicate the system has detected problem.
 a
 T .10 Lamp and Flasher Test This test all the flashlamps and the controlled lamps
 causes to
 flash at the same time. The controlled lamps blink, while the flashlamps cycle from highest to
 lowest. Any other results indicates the system has detected problem.
 a
 1-18
```

## PDF page 35

```
 T.11 Display Test This test automatically lights every dot in the Dot Matrix Display. A series of
 patterns appear in sequence. Each pattern turns On and Off a section of dots. Every dot on the
 display should be turned On and Off during this test.
 T.12 Flipper Coil Test The Flipper Coil Test has three modes: Repeat, Stop, and Run.
 Only one flipper should pulse at a time. The system has detected a problem if more than one
 flipper pulses, a flipper comes On and stays On, or no flippers pulse during the Repeat or Run
 modes.
 Repeat The Repeat Mode pulses a single flipper. After entering this test, coil 01 shows in the
 display and the corresponding flipper activates. Press the Up or Down button to cycle
 through the flipper coils, one at a time. The same flipper coil pulses until the Up or Down
 button is pressed. Either press the Escape button to return to the Test Menu, or press
 the Enter button to advance to the next mode.
 Stop The Stop Mode halts the Flipper Coil Test. Press Enter during the Repeat mode and the
 Flipper Coil Test stops. No flipper coil should be activated while the test is stopped.
 Either press the Escape button to return to the Test Menu, or the Enter button to
 advance to the next mode.
 Run The Run Mode cycles through the flippers automatically. The display shows the name
 and number of the flipper coil currently being pulsed. Either press the Escape button to
 return to the Test Menu, or the Enter button to advance to the next mode.
 T. 13 Ordered Lamp Test The number assigned to each lamp indicates the lamp's position in the
 matrix. The number on the left indicates the column. The number on the right indicates the row.
 Example Lamp 23 means 2nd column, 3rd row.
 -
 This test checks each lamp circuit individually. Press the Up or Down button to cycle through the
 lamps. Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of the
 playfield. Direction depends on which button, Up or Down, is pressed. For each name and
 number that is shown in the display the corresponding lamp should light. Any other results
 indicates the system has detected a problem.
 T.14 Lamp Row-Col Test This test allows individual rows and columns in the lamp matrix
 to be operated. This is useful for trouble-shooting wiring and driver problems.
 Press the UP or DOWN buttons to cycle trough the different rows and columns.
 T. 15 Dip Switch Test This test is used to show the positions of the dip switches on the CPU
 board (U27).
 1-19
```

## PDF page 36

```
 T. 16 Wheel Test This test is used to determine if both optos the Wheel working and
 on are to see
 if they are wired correctly to the two inputs. By turning the Wheel, the display shows whether the
 switches are seen and which direction it believes the Wheel is turning.
 T.17 Vari Target Test This test is used to exercise the Vari Target and monitor the switches
 on
 the assembly. The "ENTER" button is used to reset the Vari Target, and the state of the three
 switches is shown on the display.
 T. 18 Token Tube Test This test is used to exercise the Token Tube solenoids and
 to check the
 state of the switches in the mechanism. The "UP" and "DOWN" buttons change the mode of the
 test, and the "ENTER" button is used to release a token. Possible Modes: LEFT TUBE, RIGHT
 TUBE, ALTERNATE.
 The LEFT TUBE mode will fire only the left solenoid.
 The RIGHT TUBE mode will fire only the right tube's solenoid.
 The SEQUENTIAL mode will alternately fire the left and right solenoids.
 During this test, the state of the switches in the mechanism is displayed.
 T.19 Light Rope Test This test is used to turn the Light Rope segments. The 'UP"
 on and
 "DOWN" buttons change which segment(s) will be exercised. Possible combinations LIGHT
 are:
 ROPE 1, LIGHT ROPE 2, and BOTH. Pressing the "ENTER" key will start flashing the selected
 rope segments.
 T .20 3-Bank Drop Target Test This test is used to exercise each of the 3-Bank
 sets and show
 the state of their switches. The "UP" and UDOWN" switches select the bank to test, and the
 "ENTER" switch fires the reset coil. The display shows the state of the switches for the selected
 drop bank.
 T.21 Top Trough Test This test is used to show the state of switches in the Underground
 Trough. Balls placed in the top popper will be popped into the Underground Trough. Any balls
 arriving at the "bank" will be kicked back out after a slight pause.
 The state of the underground switches is shown on the display.
 T .22 Empty Balls Test This test kicks out all balls loaded in troughs, lockups,
 poppers, and
 kickouts until no balls remain in those locations.
 Note: As the trough kicks out balls, they will stack up in the shooter groove, which may require
 manual clearing in order to allow further balls to be kicked out.
 1-20
```
