# Tales from the Crypt (Data East 1993) - Game Diagnostics text for the Laser Kick and Gravestone tests

Transcribed by hand from a native-resolution render of printed page 27 (PDF 31) of the GameEx-hosted scan `Data_East_1993_Tales_from_the_Crypt_Manual.pdf`. The scan has no text layer, so the text was read from the render; OCR was used only to locate the page. Printed spelling, including `Switchs`, `the the` and `erronious`, is kept.

## Laser Kick Test

> This test provided to insure proper interaction between certain switches and their associated solenoids without entering game play. For example, by rolling the ball over the left outlane switch the Laser Kick should fire. If it kicks too early or too late, the switch actuator should be adjusted to compensate for this error. If it fails to fire, use the switch test or coil test to help determine the the cause of failure. Note: During this function, similar tests may be performed on Vertical Up Kickers or Saucers in the game.

## Gravestone Up & Down Test

> This game has a feature which lowers a Target Switch (Gravestone) to allow a shot to the Vertical Up Kicker (VUK) below the playfield. The motor on this mechanism is controlled by a relay driven by Q23 on the CPU and there are 2 Limit Switchs (Gravestone Motor Up & Gravestone Motor Down) used by the CPU to determine the status of the Gravestone Motor.
>
> After entering this test, press and hold the game's Start Button. This will cause the relay to pulse repeatedly as long as the Start Button is depressed. At the same time you will notice that the switch status (ON & OFF) will be indicated in the Dot Matrix Display (Gravestone Up & Down). The appropriate switch should be closed just prior to the limit of the Gravestone Motor Mechanism and both switches should not be closed (ON) at the same time.
>
> This test is located before the Switch Tests so the technician can move the mechanism until both switches read OFF. This will help eliminate erronious readings while trying to trace a problem during the Active Switch Test.

The printed text names `Q23` as the driver of the gravestone motor relay. The Special Coil Wiring Diagram on printed page 33 (see `coil-drivers.md`) draws Q23 on drive 16, which drives the shaker motor, and draws the relay with the 26 VAC contacts on drive 15, Q24.

## Digital Display Test (same page)

The page's first paragraph states that the display control board provides `more information (32 X 128 Dots) to the operator as well as displaying graphics to the player` and that it is controlled by a `68B09E` microprocessor and its personality ROMs.
