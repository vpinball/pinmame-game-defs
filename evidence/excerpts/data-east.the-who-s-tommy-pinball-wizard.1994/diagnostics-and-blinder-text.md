# The Who's Tommy Pinball Wizard (Data East 1994) - Diagnostics text, Mirror and Arch Motor tests, and the Pinball Servo Controller

Transcribed from native-resolution (300 dpi) renders of printed pages 29, 30 and 31 (PDF 33, 34 and 35) and of the unnumbered blinder section at PDF pages 113, 115 and 116 and printed page 5 (PDF 9) of the IPDB-hosted scan `Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf`. The page text was drafted from an OCR pass over the renders and every quoted sentence below was then corrected against the render; obvious OCR noise (for example `rrmlnted`) is not reproduced. Quotations keep the print's own spelling (`erronious`, `its'`, `acheived`, `PROCEDE`).

## Instruction card and game rules (printed page 5)

The page reproduces the instruction card (`Part No. 755-5048-00`), styled as a theatre ticket:

| Feature | Card text |
| --- | --- |
| Skill Shot | Plunge the ball into the secret hole behind the parachute. |
| Multiball | Spell T-O-M-M-Y by shooting the mirror, then enter the mirror for 4-Ball Play. |
| Jackpot | Shoot ramps to collect Jackpots, then spell T-O-M-M-Y at Mirror to light Super Jackpots. |
| Union Jack | Orbit shot lights "Union Jack Collect"; Shoot "Union Jack Collect" to start flashing Feature. |
| Genius Hole | Shoot the "eject" to collect various Skill Level awards. |
| Mystery | Shoot the right ramp to light Mystery award at "eject." |
| Hint | You can become Tommy by holding in the Extra Ball Button when starting your game! |

The same page's text describes the Extra Ball (EB) Buyin Feature: `For the same credit, player may choose to continue the game at the same score and features active by depressing the E-Ball Button.`

## Game Diagnostics (printed page 29)

> Each feature may be tested manually or automatically using the STEP and FORWARD/REVERSE push-button switches inside the coin door and the Game Start push-button switch on the front of the cabinet.

> With the game in the game-over mode, open the coin door and make sure that the FORWARD/REVERSE push-button switch is set to REVERSE (down) and depress the STEP push-button switch.

The page's abbreviation list includes `PPB Playfield Power Board`, `SSFB Solid State Flipper Board`, `SMB Shaker Motor Board`, `G.I. General Illumination` and `N.C. Normally Closed`.

## Easy Trough Clear (printed page 30)

> Pressing the step button again displays the EASY TROUGH CLEAR message and instructs the player to operate either flipper button to easily remove the balls from the trough.

## Mirror Up & Down Test (printed page 31)

> This game has a feature which lowers a Target Switch (Mirror) to allow a shot to the Vertical Up Kicker (VUK) below the playfield. The motor on this mechanism is controlled by a relay driven by Q23 on the CPU and there are 2 Limit Switches (Mirror Motor Up & Mirror Motor Down) used by the CPU to determine the status of the Mirror Motor.

> After entering this test, press and hold the game's Start Button. This will cause the relay to energize as long as the Start Button is depressed. At the same time you will notice that the switch status (ON & OFF) will be indicated in the Dot Matrix Display (Mirror Up & Down). The appropriate switch should be closed just prior to the limit of the Mirror Motor Mechanism and both switches should not be closed (ON) at the same time.

> This test is located before the Switch Tests so the technician can move the mechanism until both switches read OFF. This will help eliminate erronious readings while trying to trace a problem during the Active Switch Test.

## Arch Motor Test (printed page 31)

> This game has a feature which covers the lower flippers, called the Blinder. The motor on this mechanism is controlled by the Servo Board, which receives its' data from the CPU Board.

> After entering this test, press and hold the game's Start Button which engages the Blinder Mechanism , releasing the Start Button will disengage the Blinder Mechanism. Refer to the Blinder Schematic/Troubleshooting Section for further information.

## Pinball Servo Controller Board - Theory of Operation (PDF page 113)

> The Pinball Servo Controller has been designed to interface between the microprocessor system and the servo operating the "Blinders." The servo used is a conventional radio control model servo and is a mechanical motor drive unit controlled by a servo amplifier that has electro-mechanical feedback positioning. The input signal to these servos is a positive pulse of at least 3.2 volts amplitude and is repeated at 12 to 20 milliseconds intervals. [...] The input controlling pulse varies its width to drive the servo output to a required position, and typically varies from 1.0 milliseconds to 2.0 milliseconds for 180 degrees of output rotation by the servo.

> The interface connector is a seven-pin unit and supplies +5 volts, +12 volts, common ground, clock, data and clear/not. It is keyed for correct insertion and has friction lock. The output connector is a three-pin which supplies +5 volt, common ground and a controlling pulse to the servo.

> All three digital control signals are fed to U4, which is a Hex D Flip-Flop (74HC174) [...]. Only one section of the IC is used, and the other five unused inputs are tied to ground. The DATA OUT is toggled by the input control signals, with the INPUT DATA level being strobed through on a CLOCK transition, and being reset by the CLEAR/NOT signal.

> U2 is a LM555 which is a timer and configured in a "free-running" mode. R4 (91K ohm) sets the cycle time which is nominally 18 milliseconds. [...] When the FET Switch is closed, this will short out R3, R5 and R6, leaving R1 (4.3K ohm) and R2 (5K ohm) to set the minimum pulse width by adjusting R2. When the FET Switch opens, it includes R3 (16K ohm), R5 (10K ohm) and R6 (4.7K ohm) in the timing network, and R5 is adjusted for maximum pulse width.

> The complete I/O sequence is that when the DATA is strobed in, the output pulse width is MINIMUM, and when the DATA is CLEARED, the output pulse width is MAXIMUM. These are individually set to each required servo output position due to the tolerances in each servo's components.

The drawing under the text is the board, labelled `DATA EAST INC 520-5078-0` (the last digit is cut off by the scan).

## Pinball Servo Controller Adjustment Procedure for Blinders (PDF pages 115-116)

> [Th]e Servo Interface (driver) Board has two (2) adjustment control pots. These adjustments are for the closure and [...]g movements.

The scan cuts off the left margin of this page, so the first letters of some lines are missing; they are marked `[...]`. Step 1 removes the servo motor after `REMOVE THE BOTTOM ARCH (See Figure 2 for location of the four (4) Bottom Arch Screws).` Step 3 (`ADJUST SERVO MOTOR VIA SERVO INTERFACE BOARD-- BLINDER CENTERING (OPEN) ALIGNMENT.`) reads in part:

> TURN ON POWER TO TEST. THE BLINDER ASS'Y WILL CYCLE AND OPEN OPEN THE BLINDERS, TO A SEMI-OPEN POSITION, ACCORDING TO THE PRESET SERVO INTERFACE BOARD. [...] START DIAGNOSTIC SERVO ARCH TEST. [...] ONCE IN PLAYFIELD RECHECK ALIGNMENT, USE DIAGNOSTIC ARCH TEST IN THE DIAGNOSTIC PROGRAM. PRESS START AND HOLD BUTTON TO OPEN BLINDER. ENSURE BLINDER STILL HOLDS OPEN ALIGNMENT. (ALSO ENSURE THE LEFT BLINDER BLADE DOES NOT HIT THE WIRE FORM UNDER THE ARCH (See Figure 2)). IF NOT ALIGNED CORRECTLY OR IT HITS THE WIRE FORM, ADJUST THE YELLOW POT R2 (See Figures 2 & 4).

> RELEASE START BUTTON. THE BLINDERS WILL CLOSE. AT THIS POINT, ENSURE BLINDER CLOSES AND DOES NOT PROTRUDE MORE THAN 3/16" BEYOND ARCH WALL (See Fig. 1)

Step 4B: `TURN RED POT (See Figure 4) TO ADJUST THE CLOSURE SO THE BOTTOM BLINDER DOES NOT EXTEND PAST THE RIGHT STEEL FLAT RAIL.` Figure 3 labels a `TOP BLADE` and a `BOTTOM BLADE`, a `LINK ARM`, a `SPRING` and the `SERVO MOTOR`.

Note on wording: page 31's test text says holding Start "engages" the blinder and releasing "disengages" it, while the adjustment procedure says holding Start in the same Arch test opens the blinders and releasing closes them. The two pages describe the same test; the procedure's open/close wording is the more specific.
