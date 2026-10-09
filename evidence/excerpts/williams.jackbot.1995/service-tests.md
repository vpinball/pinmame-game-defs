# Jack*Bot — Test Menu and Menu System Operation

Transcribed by the curator, read from the rendered pages of `Williams_1995_Jack_Bot_English_Manual.pdf` (SHA-256 `8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94`, a scan with no text layer; 300 dpi renders). A first pass of Windows OCR was corrected word by word against the page images. Spelling, capitalization and punctuation are as printed, including the manual's own typos (`then` for `than`, `until press the Up or Down button is pressed`, and so on). Italic and bold type is not marked. PDF page 37 (printed 1-8) is the Menu System Operation diagram; PDF pages 45-49 (printed 1-16 to 1-20) are the Test menu and the T.1-T.18 descriptions. The page images are the authority; this transcription is unreviewed by a second reader.

## PDF page 37 (printed 1-8): Menu System Operation

The page is a diagram: three groups of boxed lists hang off the Main Menu bracket, with a key printed at the right of the Bookkeeping and Printouts lists. The text, left to right and top to bottom:

```
MENU SYSTEM OPERATION

The Main Menu allows you to choose from several categories, which in turn lead to other menus to choose from.  To
access the Main Menu, open the coin door and press the Begin Test button, then press the Enter button.  Press the
Up or Down buttons to cycle through the Main Menu.  Press the Enter button to access a menu.  Press the Escape
button to return to the Main Menu.  Press the Start button for HELP at any time.

MAIN MENU

B.  BOOKKEEPING MENU            P.  PRINTOUTS MENU               T.  TEST MENU
  B.1 Main Audits                 P.1 Earnings Data                T.1 Switch Edges Test
  B.2 Earning Audits              P.2 Main Audits                  T.2 Switch Levels Test
  B.3 Standard Audits             P.3 Standard Audits              T.3 Single Switches Test
  B.4 Feature Audits              P.4 Feature Audits               T.4 Solenoid Test
  B.5 Histograms                  P.5 Score Histograms             T.5 Flasher Test
  B.6 Time-Stamps                 P.6 Time Histograms              T.6 General Illumination Test
                                  P.7 Time-Stamps                  T.7 Sound and Music Test
                                  P.8 All Data                     T.8 Single Lamp Test
                                                                   T.9 All Lamps Test
                                                                   T.10 Lamp and Flasher Test
                                                                   T.11 Display Test
                                                                   T.12 Flipper Coil Test
                                                                   T.13 Ordered Lamps Test
                                                                   T.14 Lamp Row-Col
                                                                   T.15 DIP Switch Test
                                                                   T.16 Ramp Test
                                                                   T.17 Visor Test
                                                                   T.18 Empty Balls

U.  UTILITIES MENU              A.  ADJUSTMENT MENU
  U.1 Clear Audits                A.1 Standard Adjustments
  U.2 Clear Coins                 A.2 Feature Adjustments
  U.3 Reset H.S.T.D.              A.3 Pricing Adjustments
  U.4 Set Time and Date           A.4 H.S.T.D. Adjustments
  U.5 Custom Message              A.5 Printer Adjustments
  U.6 Set Game I.D.
  U.7 Factory Adjustments
  U.8 Factory Resets
  U.9 Presets
  U.10 Clear Credits
  U.11 Auto Burn-in

Key, printed beside the Bookkeeping and Printouts lists:
  Press Escape
  To move out of a menu selection.

  Press Enter
  To get into a menu selection.

  Press Up
  Increases sequence;  Example A.1, A.2, A.3, A.4.

  Press Down
  Decreases sequence;  Example A.4, A.3, A.2, A.1.

  Use Up or Down to cycle through the
  selections in a menu.

  Use Escape and Enter to move into and out of the
  selected menu.

1-8
```

Note on the names: the diagram prints T.3 as `Single Switches Test`, T.7 as `Sound and Music Test`, T.8 as `Single Lamp Test`, T.10 as `Lamp and Flasher Test` and T.18 as `Empty Balls`. The T. TEST MENU list on PDF page 45 prints T.3 as `Single Switch Test`, T.7 as `Sound & Music Test`, T.8 as `Single Lamps Test`, T.10 as `Lamps And Flasher Test` and T.18 as `Empty Balls Test`; the T.3, T.7, T.8, T.10 and T.18 headings on PDF pages 45-49 read `Single Switches Test`, `Sound and Music Test`, `Single Lamp Test`, `Lamp and Flasher Test` and `Empty Balls`. Each printing is reproduced as printed. The numbers T.1-T.18 and the names of the other tests, including T.16 `Ramp Test` and T.17 `Visor Test`, agree on every page.

## PDF page 45 (printed 1-16): Test Menu list, switch matrix text, T.1-T.3

```
Use the Service Switch Actuator to hold in the top interlock switch located in the bottom left
corner of the coin door opening.  The actuator must be in place in order to activate the solenoids
and flashlamps.

Press the Up or Down buttons to cycle through the menu.  Press the Enter button to access a test.  Press
the Escape button to return to the Test menu.  Note:  During any test, press the Start button to obtain the
wire color, driver number, connector number and fuse location.

                          T. TEST MENU
         T.1     Switch Edges Test
         T.2     Switch Levels Test
         T.3     Single Switch Test
         T.4     Solenoid Test
         T.5     Flasher Test
         T.6     General Illumination Test
         T.7     Sound & Music Test
         T.8     Single Lamps Test
         T.9     All Lamps Test
         T.10    Lamps And Flasher Test
         T.11    Display Test
         T.12    Flipper Coil Test
         T.13    Ordered Lamps Test
         T.14    Lamp Row-Col
         T.15    DIP Switch Test
         T.16    Ramp Test
         T.17    Visor Test
         T.18    Empty Balls Test

    The switch matrix, on the left side of the display, shows the state of all switches.  A dot indicates
the switch is open, a square indicates the switch is closed. The numbers assigned to each switch indicate
where the switch is located in the matrix.  The number on the left indicates the column, the number on
the right indicates the row.  Example - Switch 23 is 2nd column, 3rd row.
    A short to ground - on either the row or column wire - appears as a shorted row(s).  However, a
column wire shorted to ground disappears when all of the indicated row switches are open.  A row wire
shorted to ground does not disappear.
    A shorted diode in the switch matrix can cause other switches to appear closed.  These
"phantom" switches (though not actually closed), complete a rectangle in the switch matrix.  Therefore, if
two switches in the same column are closed (example; #22 and #24), and a third switch is pressed in
another column but in the same row as one of the first two (example; #32), the "phantom" switch #34 is
falsely indicated as closed.  The switch with the shorted diode is diagonally opposite the "phantom"
switch (in this case #22).

T.1     Switch Edges Test
        Press each switch one at a time.  The name and number of the switch is shown in the display.  If
        a switch other then the one pressed, or no switch at all is indicated, the system has detected a
        problem with the switch circuit.

T.2     Switch Levels Test
        This test automatically cycles through all switches that are detected closed.  The name and
        number of each switch that is detected is shown in the display.  A filled square indicates the
        switch's position in the matrix.

T.3     Single Switches Test
        The Single Switch test isolates a particular switch by blocking signals from all other switches.
        Use the Up or Down buttons to select the switch to be tested.

1-16
```

## PDF page 46 (printed 1-17): T.4-T.6

```
T.4     Solenoid Test
        The Solenoid test has three modes - Repeat, Stop, and Run.  Only one solenoid should  pulse at
        a time.  The system has detected a problem if more then one solenoid pulses, a solenoid comes
        on and stays on, or no solenoids pulse during the Repeat or Run modes.

                Repeat:   The Repeat mode pulses a single solenoid.  After entering this test, solenoid
                one shows in the display and the corresponding solenoid activates.  Press the Up or
                Down button to cycle through the solenoids, one at a time.  The same  solenoid pulses
                until the Up or Down button is pressed.  Either press the Escape button to return to the
                Test menu, or press the Enter button to move to the next mode.

                Stop: The Stop mode halts the Solenoid test. Press Enter during the Repeat mode and
                the Solenoid test stops.  No solenoids should be activated while the test is stopped.
                Either press the Escape button to return to the Test menu, or the Enter button to move to
                the next mode.

                Run:  The Run mode cycles through the solenoids automatically.  The display shows the
                name and  number of the solenoid currently being  pulsed.

T.5     Flasher Test
        This tests the flashlamp part of the solenoid circuit exclusively.  This, like the Solenoid test, has
        three modes - Repeat, Stop, and Run. During this test only one flashlamp circuit should pulse at
        a time.  The system has detected a problem if more then one circuit pulses, a circuit stays on, or
        no circuits pulse during the Repeat or Run modes.

                Repeat: The Repeat mode pulses a single flashlamp. After entering this test the name
                and number of the first flashlamp circuit shows in the display and the corresponding
                bulb(s) flash.  Press the Up or Down buttons to cycle through all of the flashlamps circuits
                one at a time. The same circuit pulses until press the Up or Down button is pressed.
                Either press the Escape button to return to the Test menu, or press the Enter button to
                advance to the next mode.

                Stop:  The Stop mode halts the Flasher test.  No flashlamp circuit should be active
                during this mode.  Either press the Escape button to return to the Test menu, or press
                the Enter button to advance to the next mode.

                Run:  The Run mode cycles through the flashlamps automatically.  The display shows
                the name and number of the flashlamp circuit currently being pulsed as the
                corresponding bulb(s) flashes.

T.6     General Illumination Test
        This test checks all of the General Illumination circuits.  There are two modes of operation - Stop
        and Run.

                Stop:  Press the Up or Down buttons to cycle through the General Illumination test
                manually.  All illumination is tested first, followed by an individual circuit test.  The circuit
                name and number shows in the display while the corresponding lamps lights.  If any other
                results occur the system has detected an error.

                Run:  Press the Enter button any time during Stop mode and the General Illumination
                test cycles through automatically.  For each circuit shown in the display the
                corresponding bulbs should light.  If any other results occurs the system has detected a
                problem.

1-17
```

## PDF page 47 (printed 1-18): T.7-T.11

```
T.7     Sound and Music Test
        The Sound and Music test checks the audio circuits.  This test has three modes for testing the
        sound and music circuits - Run, Repeat, and Stop.

                Run:  The Run mode steps through a sequence of sounds and music.  Press the Up or
                Down buttons during this portion of the Sound and Music test to advance to a particular
                sound or tune without having to wait for the program to play all the sounds available in
                the test.  A sound or tune should be heard for each name and number that appears in the
                display.  Any other results indicates the system has detected a problem.

                Repeat:  Press the Enter button at any time during the Run mode to cause the program
                to stop and repeat a particular sound/tune.  The same sound should repeat continuously
                until the Up or Down button is pressed.  Any other results indicates the system has
                detected a problem.

                Stop:  Press the Enter button at any time during the Repeat mode to stop this test
                altogether.  Nothing should be heard.  Any other results indicates the system has
                detected a problem.

T.8     Single Lamp Test
        The number assigned to each lamp indicates the lamp's position in the matrix.  The number on
        the left indicates the column.  The number on the right indicates the row.  Example - Lamp 23
        means 2nd column, 3rd row.

        This test checks each lamp circuit individually.  Press the Up or Down button to cycle through this
        test.  For each name and number that is shown in the display the corresponding lamp should
        light.  Any other results indicates the system has detected a problem.

T.9     All Lamps Test
        This test causes all the controlled lamps to flash at the same time.  Every controlled lamp should
        flash.  Any other results indicates the system has detected a problem.

T.10    Lamp and Flasher Test
        This test causes all the flashlamps and the controlled lamps to flash at the same time.  The
        controlled lamps blink, while the flashlamps cycle from highest to lowest.  Any other results
        indicates the system has detected a problem.

T.11    Display Test
        This test automatically checks every dot in the Dot Matrix Display board.  A series of patterns
        appear in sequence.  Each pattern turns on and off a section of dots.  Every dot on the matrix
        display should be turned on and off during this test.

1-18
```

## PDF page 48 (printed 1-19): T.12-T.16

```
T.12    Flipper Coil Test
        The Flipper Coil test has three modes - Repeat, Stop, and Run.  Only one flipper should  pulse at
        a time.  The system has detected a problem if more then one flipper pulses, a flipper comes on
        and stays on, or no flippers pulse during the Repeat or Run modes.

                Repeat:  The Repeat mode pulses a single flipper.  After entering this test, flipper coil 01
                shows in the display and the corresponding coil activates.  Press the Up or Down button
                to cycle through the flipper coils, one at a time.  The same solenoid pulses until the Up or
                Down button is pressed.  Either press the Escape button to return to the Test menu, or
                press the Enter button to move to the next mode.

                Stop:  The Stop mode halts the Flipper Coil test.  Press Enter during the Repeat mode
                and the test stops.  No coils should be activated while the test is stopped.  Either press
                the Escape button to return to the Test menu, or the Enter button to move to the next
                mode.

                Run:  The Run mode  cycles through the flippers automatically.  The display shows the
                name and  number of the flipper coil currently being  pulsed.

T.13    Ordered Lamps Test
        The number assigned to each lamp indicates the lamp's position in the matrix.  The number on
        the left indicates the column.  The number on the right indicates the row.  Example - Lamp 23
        means 2nd column, 3rd row.

        This test checks each lamp circuit individually.  Press the Up or Down button to cycle through the
        lamps.  Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of the
        playfield.  Direction depends on which button, Up or Down, is pressed.  For each name and
        number that is shown in the display the corresponding lamp should light.  Any other results
        indicates the system has detected a problem.

T.14    Lamp Row-Col
        This test allows individual rows and columns in the lamp matrix to be operated.  This is useful for
        trouble-shooting wiring and driver problems.

        Press the Up and Down buttons to cycles through the different rows and columns.

T.15    DIP Switch Test
        This test is used to show the positions of the DIP switches on the CPU board (U27).

T.16    Ramp Test
        Once the test name is shown under the Test Menu, press the Enter button.  The bottom line of
        the display shows "RAMP DOWN SW." when the Ramp is down and the Ramp Down switch is
        activated.  This test has three modes of operation:

                Repeat:  The repeat test pulses a single coil, either the up or down coil, until the Up or
                Down button is pressed to move to the next coil.

                Stop:  Press the Enter button during the Repeat test and the Ramp stops activating.

                Run:  Press the Enter button during the Stop test and the Ramp cycles Up and Down
                automatically.

1-19
```

## PDF page 49 (printed 1-20): T.17-T.18

```
T.17    Visor Test
        Once the test name is shown under the Test Menu, press the Enter button.  The bottom line of
        the display will show the state of the Visor Open and Visor Closed switches.  An 'X' in the box
        indicates the switch is closed.

        This test has three modes of operation:

                Open   -   Open the Visor:  Run the visor motor until the Visor Open switch is closed.

                Close  -   Close the Visor:  Run the visor motor until the Visor Closed switch is closed.

                Cycle  -   Run the visor motor continuously.

        The Up and Down changes the test mode.  Pressing Enter changes the test between RUNNING
        and STOPPED.  When STOPPED, the motor will be turned off and the current test halted.

        Press Escape to return to the Test Menu at any time.

T.18    Empty Balls
        This test checks the poppers and kickers that are under the playfield.

        Press the enter button and all balls loaded into the poppers and troughs should be kicked out
        until no balls remain in these locations.  Any other result indicates a problem.

        Note:  As the trough kicks out balls, they will stack up in the shooter groove, which may require
        manual clearing in order to allow further balls to be kicked out.

1-20
```
