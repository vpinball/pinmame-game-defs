# Last Action Hero (Data East 1993) - Digital Display, Crane, Magnet and Laser Kick tests

Transcribed by hand from a native-resolution (300 dpi) render of printed page 27 (PDF 31) of the IPDB scan `Data_East_1993_Last_Action_Hero_Manual.pdf`, footer `Game Diagnostics`. The scan has no text layer. Spelling, spacing and doubled words are the print's.

## DIGITAL DISPLAY TEST

`The Digital display utilizes a Dot Matrix Display Control board mounted in piggyback fashion to the display driver Board. The purpose behind this board is to provide more information (32 X 128 Dots) to the operator as well as displaying graphics to the player.`

`The board is controlled by a 68B09E microprocessor and it's personality ROMs (Unique to the Game) . It receives Data, Reset & Clock information from the CPU Board via the ribbon cable and sends back multiple Status and Busy signals to the CPU . This is to insure syncronized communication between the CPU and the Display Controller board.`

The Automatic Test paragraph says the display tests are entered with the `STEP` push-button from the Sound Manual test and cycle column, row, inverted-column, inverted-row and checkerboard patterns `until advanced to the next test or until the power is removed`.

## Crane Test

`This test shows the status of the two limit switches for the crane mechanism, and provides motor control to actuate these switches. To move the crane left and right, operate the start button. As long as the button is depressed the motor will continue to rotate. The motor only rotates in one direction, but the cam on the motor, allows the crane arm to sweep an arc of 145 degrees and then return. During this process the the display indicates the status of both limit switches.(i.e. LEFT CRANE SW. ON - RIGHT CRANE SW. OFF)`

`Operating the trigger switch should pulse the ball release coil on the crane mechanism.`

## Magnet Test

`This test rapidly cycles the 3 magnets located in the center of the playfield as long as the start button is operated. In addition, the display indicates the current status of the test. It is recomended that this test not be operated for more than a few seconds due to the high current required to operate these magnets.`

## Laser Kick Test

`This test provided to insure proper interaction between certain switches and their associated solenoids without entering game play. For example, by rolling the ball over the left outlane switch the Laser Kick should fire. If it kicks too early or too late, the switch actuator should be adjusted to compensate for this error. If it fails to fire, use the switch test or coil test to help determine the the cause of failure. Note: During this function, similar tests may be performed on Vertical Up Kickers or Saucers in the game.`

The Laser Kick paragraph names a left-outlane laser kick that this machine's own coil and switch tables do not list (its kickback is `22 Ripper Kickback (See Schematic)`, switch 48 `Ripper Kickback`); the paragraph reads as text shared with other Data East manuals of the period.
