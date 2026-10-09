# NBA Fastbreak — Test Menu and Mechanism Tests

Text layer of `Bally_1997_NBA_Fastbreak_Operations_Manual_Final_no_schematics.pdf` (the March 1997 edition, an ABBYY FineReader OCR layer), extracted with `pdftotext -layout` and reproduced as extracted: OCR character errors are left in place, unreadable characters are shown as `?`, and runs of blank lines are collapsed. It is unreviewed OCR; every device fact the definition takes from these pages was read against the rendered page or confirmed by the ROM's own service tests. PDF pages 40-44, printed 1-18 to 1-22: the Test menu and the T.1-T.18 descriptions, including T.16 MOTOR TEST and T.17 BACKBOX TEST.

## PDF page 40

```
Press the Up or Down buttons to scroll through the Test menu. Press the Enter button to access a test.
Press the Escape button to return to the Test menu. During any test, press the Start button to obtain the
wire color, driver number, connector number and fuse location.

                                           T. TEST MENU
        T.1 Switch Edges Test                       T.10 Lamps And Flasher Test
        T.2 Switch Levels Test                      T.11 Display Test
        T.3 Single Switch Test                      T.12 Flipper Coil Test
        T.4 Solenoid Test                           T.13 Ordered Lamps Test
        T.5 Flasher Test                            T.14 Lamp Row-Col.
        T.6 General Illumination Test               T.15 DIP Switch Test
        T.7 Sound & Music Test                      T.16 Motor Test
        T.8 Single Lamps Test                       T.17 Backbox Test
        T.9 All Lamps Test                          T.18 Empty Balls Test

  Note: In order to operate the tests that use the +50 V or +20 V circuits, pull the
  top interlock switch button out. The interlock switches are located on a bracket
  in the coin door opening.

  The switch matrix, on the left side of the display, shows the state of all switches. A dot indicates the
  switch is open, a square indicates the switch is closed. The numbers assigned to each switch indicate
  where the switch is located in the matrix. The number on the left indicates the column, the number on
  the right indicates the row. Example - Switch 23 is 2nd column, 3rd row.

  A short to ground - on either the row or column wire - appears as a shorted row(s). However, a column
  wire shorted to ground disappears when all of the indicated row switches are open. A row wire shorted
  to ground does not disappear.

  A shorted diode in the switch matrix can cause other switches to appear closed. These “phantom"
  switches (though not actually closed), complete a rectangle in the switch matrix. Therefore, if two
  switches in the same column are closed (example; #22 and #24), and a third switch is pressed in
  another column but in the same row as one of the first two (example; #32), the "phantom" switch #34 is
  falsely indicated as closed. The switch with the shorted diode is diagonally opposite the "phantom"
  switch (in this case #22).

T.1     SWITCH EDGES TEST
        Press each of the switches one at a time. The name and number of the switch is shown in the
        display. If a switch other than the one pressed, or no switch at all is indicated, the system has
        detected a problem with the switch circuit. To return the Test menu, press the Escape button.

T.2     SWITCH LEVELS TEST
        This test automatically cycles through all switches that are detected closed. The name and
        number of each switch that is detected is shown in the display. A filled square indicates the
        switch’s position in the matrix. To return the Test menu, press the Escape button.

T.3     SINGLE SWITCHES TEST
        The Single Switch test isolates a particular switch by blocking signals from all other switches.
        Use the Up or Down buttons to select the switch to be tested. To return the Test menu, press the
        Escape button.

                                                  1-18
```

## PDF page 41

```
T.4   SOLENOID TEST
      The Solenoid test has three modes -- Repeat, Stop, and Run. Only one solenoid should pulse at
      a time. The system has detected a problem if more than one solenoid pulses, a solenoid comes
      on and stays on, or no solenoids pulse during the Repeat and Run modes.

              Repeat: The Repeat mode pulses a single solenoid. Press the Enter button to start this
              test. The name of the first solenoid shows in the display and the corresponding coil
              pulses. Press the Up or Down buttons to cycle through the solenoids, one at a time. The
              same solenoid pulses until you press the Up or Down buttons to advance to the next one.
              To return the Test menu, press the Escape button. To advance to the next test mode,
              press the Enter button.

              Stop: The Stop mode halts the Solenoid test. No solenoids should be active. To return
              the Test menu, press the Escape button. To advance to the next test mode, press the
              Enter button.

              Run: The Run mode cycles through the solenoids automatically. The display shows the
              name and number of the solenoid currently being pulsed. To return the Test menu, press
              the Escape button. To return to the Repeat mode, press the Enter button.

T.5   FLASHER TEST
      This tests the flashlamp part of the solenoid circuit. There are three modes - Repeat, Stop, and
      Run. During this test the flashlamp circuit named in the display should blink. The system has
      detected a problem if more than one flashlamp circuit blinks, the lamps stays on, or no lamps
      blink during the Repeat and Run modes.

              Repeat: The Repeat mode pulses a single flashlamp. Press the Enter button to start
              this test. The name and number of the first flashlamp is displayed and the corresponding
              bulb(s) blinks. The same bulb(s) blinks until you press the Up or Down buttons to
              advance to the next one. To return to the Test menu, press the Escape button. To
              advance to the next test mode, press the Enter button.

              Stop: The Stop mode halts the Flasher test. There should not be any flashlamps lit
              during this mode. To return to the Test menu, press the Escape button. To advance to
              the next test mode, press the Enter button.

              Run: The Run mode cycles through the flashlamps automatically. The display shows
              the name and number of the flashlamp circuit currently being pulsed as the
              corresponding bulb(s) flashes. To return to the Test menu, press the Escape button. To
              return to the Repeat mode, press the Enter button.

T.6   GENERAL ILLUMINATION TEST
      This test checks all of the General Illumination circuits. There are two modes of operation -- Stop
      and Run.

      Note: General Illumination strings four & five do not brighten or dim, they are always ON.

              Stop: The Stop mode allows you to cycle through the General Illumination test manually.
              Press the Up or Down buttons to advance through the test. All illumination is tested first,
              followed by an individual circuit test. The circuit name and number shows in the display
              while the corresponding bulbs light. If any other results occur the system has detected
              an error. To return to the Test menu, press the Escape button. To advance to the next
              test mode, press the Enter button.

                                                1-19
```

## PDF page 42

```
T.6 GENERAL ILLUMINATION TEST CONTINUED...
             Run: The Run mode cycles through the General Illumination test automatically. For
             each circuit shown in the display the corresponding bulbs should light. If any other
             results occur, the system has detected a problem. To return to the Test menu, press the
             Escape button. To return to the Stop mode, press the Enter button.

T.7    SOUND AND MUSIC TEST
       The Sound and Music test checks the audio circuits. This test has three modes for testing the
       sound and music circuits - Run, Repeat, and Stop.

               Run: The Run mode steps through a sequence of sounds and music. Press the Up or
               Down buttons to advance to a particular sound or tune. A sound or tune should be heard
               for each name and number that appears in the display. Any other results indicate the
               system has detected a problem. To return to the Test menu, press the Escape button.
               To advance to the next test mode, press the Enter button.

               Repeat: The Repeat mode causes the program to stop and repeat a particular
               sound/tune. The same sound repeats continuously until you press the Up or Down
               buttons to advance to the next one. Any other results indicates the system has detected
               a problem. To return to the Test menu, press the Escape button. To advance to the next
               test mode, press the Enter button.

               Stop: The Stop mode stops this test altogether. Nothing should be heard. Any other
               results indicate the system has detected a problem. To return to the Test menu, press
               the Escape button. To return to the Run mode, press the Enter button.

T.8    SINGLE LAMP TEST
       The number assigned to each lamp indicates the lamp’s position in the matrix. The number on
       the left indicates the column. The number on the right indicates the row. Example - Lamp 23
       means 2nd column, 3rd row.

       The Single Lamp test checks each lamp circuit individually. Press the Up or Down buttons to
       scroll through this test. A lamp should light for each name and number that is displayed. Any
       other results indicate the system has detected a problem. To return to the Test menu, press the
       Escape button.

T.9    ALL LAMPS TEST
       This test causes all the controlled lamps to flash at the same time. Every controlled lamp should
       flash. Any other results indicate the system has detected a problem. To return to the Test menu,
       press the Escape button.

T.10   LAMP AND FLASHER TEST
       This test causes all the flashlamps and the controlled lamps to flash at the same time. The
       controlled lamps blink, while the flashlamps cycle from highest to lowest. Any other results
       indicate the system has detected a problem. To return to the Test menu, press the Escape
       button.

T.11   DISPLAY TEST
       This test automatically checks every dot in the Dot Matrix Display board. A series of patterns
       appear in sequence. Each pattern turns on and off a section of dots. Every dot on the matrix
       display should be turned on and off during this test. To return to the Test menu, press the
       Escape button.

                                                 1-20
```

## PDF page 43

```
T.12   FLIPPER COIL TEST
       The Flipper Coil test has three modes -- Repeat, Stop, and Run. Only one flipper should pulse at
       a time. The system has detected a problem if more than one flipper pulses, a flipper comes on
       and stays on, or no flippers pulse during the Repeat and Run modes.

               Repeat: The Repeat mode pulses a single flipper. Press the Enter button to begin the
               test. Press the Up or Down buttons to cycle through the flipper coils one at a time. To
               return to the Test menu, press the Escape button. To advance to the next test mode,
               press the Enter button.

               Stop: The Stop mode halts the Flipper Coil test. No coils should pulse while the test is
               stopped. To return to the Test menu, press the Escape button. To advance to the next
               test mode, press the Enter button.

               Run: The Run mode cycles through the flippers automatically. The display shows the
               name and number of the flipper coil currently being pulsed. To return to the Test menu,
               press the Escape button. To return to the Repeat mode, press the Enter button.

T.13   ORDERED LAMPS TEST
       The number assigned to each lamp indicates the lamp’s position in the matrix. The number on
       the left indicates the column. The number on the right indicates the row. Example - Lamp 23
       means 2nd column, 3rd row.

       This test checks each lamp circuit individually. Press the Up or Down buttons to cycle through
       the lamps. Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of
       the playfield. The direction depends on which button, Up or Down, is pressed. For each name
       and number that is shown in the display, the corresponding lamp should light. Any other results
       indicate the system has detected a problem. To return to the Test menu, press the Escape
       button.

T.14   LAMP ROW-COL.
       This test allows individual rows and columns in the lamp matrix to be operated. This is useful for
       troubleshooting wiring and driver problems.

       Press the Up and Down buttons to cycles through the different rows and columns.

       To return to the Test menu, press the Escape button.

T.15   DIP SWITCH TEST
       This test is used to show the positions of the DIP switches on the CPU board (U27).

       To return to the Test menu, press the Escape button.

T.16   MOTOR TEST
       Select T.16 from the Test Menu and press the Enter button to begin the Motor Mechanism Test.
       Once the self-test completes successfully, the Up and Down buttons can be used to select the
       following tests. Use the Enter button to start the selected test, and the Escape button to abort the
       selected test.

       The status of the POS. 1, 2, LOCK, 3, 4 optical position switches are displayed on the dot matrix
       display during most of the tests.

       Additionally, while this test is running, the Shot Clock L.E.D. display continuously counts down
       from 24 to 0.

                                                  1-21
```

## PDF page 44

```
T.16 MOTOR TEST CONTINUED...
       SELF-TEST - This test verifies that the mechanism is fully operational. This test is run
       automatically upon entry to the Motor Test. It can also be started manually by pressing the Enter
       button when selected.

       MOVE LEFT - This test moves the defender motor one position to the left of the current position.

       MOVE RIGHT - This test moves the defender motor one position to the right of the current
       position.

       AUTO RUN - This test runs the motor in a repetitive cycle, from left to right and back again, one
       position at a time. During this test, the following data is kept:

                CYCLES: The number of cycles performed.

       This test will run until either the Escape button is pressed, or five consecutive errors occur.

       CLEAR AUTO RUN DATA - This test clears the CYCLES count maintained by the AUTO RUN
       test.

T.17    BACKBO XTEST
        Select T.17 from the Test Menu and press the Enter button to begin the Backbox test.

       This test allows the backbox flipper to be flipped when the Shoot button (located on the front
       molding) is pressed. This in turn causes the backbox basketball to be flipped through the
       backbox basket/switch.

       The status of the Shoot button and backbox basket switches is displayed on the dot matrix
       display during this test.

        N.B. The coin door, (or the solenoid power safety interlock switch) must be closed in order to
        provide power to the backbox flipper solenoid.

T.18    EMPTY BALLS TEST
        Select T.18 from the Test Menu and press Enter button to begin the Empty Balls test.

        This test kicks out all balls loaded in troughs, lockups, poppers, and kick-outs until no balls
        remain in those locations.

        Note: As the trough kicks out balls, they will stack up in the shooter groove, which may require
        manual clearing in order to allow further balls to be kicked out.

                                                   1-22
```
