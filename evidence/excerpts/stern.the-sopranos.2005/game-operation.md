# The Sopranos — contents, game operation, switch test and trough opto boards

Transcribed from `Stern_2005_The_Sopranos_Service_Manual.pdf` from the PDF text layer, with the cited sentences checked
against the rendered pages. Section headings in this manual use an obfuscated font whose text layer is unreadable; they
are given here as read from the render.

## General table of contents (PDF 13-14, printed i-ii)

`For Proper Operation..., four (4) Pinballs must be installed!`; `Switch Matrix Grid, Dedicated Switches & Locations ... DR.
4`; `Lamp Matrix Grid & Locations ... DR. 5`; `Coils Detailed Chart Table ... DR. 6`; `Coil & Flash Lamp Locations ... DR. 7`.
Chapter 2 lists among the major assemblies `4-Ball Trough Assembly, 500-6318-14`, `30° Eject (under Fish & under Safe)
Assemblies, 500-6511-01 (Qty. 2)`, `Up/Down Post (Spinner Lane Ball Lock) Assembly, 500-5867-02`, `1-Bank Drop Target Assembly,
500-6893-01`, `Fish Head & Body, Fish Jaw & Lever Support Bracket & Fish Jaw (Coil) Actuator`, `Safe Front (Above Playfield)
Assembly, 515-7493-00`, `Safe Bottom (Below Playfield) Assembly, 500-6865-00`, `Up/Down Post (Right Boat Ramp Ball Lock & Bada
Bing! Ball Lock) Asm., 500-5867-09 (Qty. 2)` and `Bada Bing! (behind Left Wire Ramp)`.

## Game operation (PDF 19, printed 5)

Start: `Insert coin(s) ... Press the Start Button ... Subsequent players can be added (up to 4 can play!) by pressing the Start
Button before the end of ball 1 ... a ball is served to the Shooter Lane.` Tournament: `the Tournament Game is started by
depressing the Tournament Start Button (located on the Front Molding, if installed).` Tilt: `Closure of the Plumb Bob Tilt
Switch according to the number of tilts set ... will end the current Ball-In-Play. Closure of the Slam Tilt Switch on the Coin
Door ends the current game(s).`

## Switch test (PDF 27, printed 13)

`As each switch is closed, the respective Switch Matrix Grid Position (1-64) will be lit.` `While in Switch Test or Active Switch
Test, the Flipper & Start Buttons are deactivated (because they can be part of these tests).`

## Troubleshooting table (PDF 28, printed 14)

`In ADJUSTMENTS MENU, with the Coin Door CLOSED, adjustments are not getting changed as desired ... This is normal. The Memory
Protect Switch is enabled when the Coin Door is CLOSED. Changes can be made with the Coin Door OPEN only.` `In COIL TEST MENU, the
coils and flashlamps do not fire after activating the "RUN" Icon. Ensure the POWER INTERLOCK SWITCH is pulled out`.

## Trough Up-Kicker Dual OPTO Boards (PDF 132, printed Section 5, Chapter 4)

`As light from the Transmitter LED1 falls on the Receiver LED1, it generates a Positive Bias Voltage (0.7v to 1.5v) which is
applied to the Gate (G) of Q1 (Fet 2N5460) turning Q1 off. When Q1 is held off, no current flows through Q2's (2N3906) Base (B).
With no base current, Q2 is off and acts as an OPEN SWITCH. When the light is interrupted (BLOCKED) R1 (Rec. Bd.) bleeds the gate
voltage off of Q1 allowing it to conduct, switching Q2 on, which acts as a CLOSED SWITCH. The LED2 (Trans/Rec) Circuit operates
identical as the LED1 Circuit.` Boards `520-5173-00 Transmitter` and `520-5174-00 Receiver`; receiver connector CN1 pins `1
WHT/XXX (Switch Row/Return +)`, `3 WHT/XXX (Switch Row/Return +)`, `2 GRN/XXX (Switch Col/Drive -)`.
