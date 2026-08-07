# White Water — Switch/Lamp addressing convention and Bigfoot Test

Source: `Williams_1993_White_Water_English_Manual.pdf`, PDF pages 33 and 36,
printed pages 1-13/1-16 (Section 1, "T. TEST MENU"). Transcribed from the
retained text layer (this section's layout is single-column and OCRs
cleanly), cross-checked against a 200 dpi render.

## Addressing convention (PDF page 33, printed 1-13)

> The switch matrix, on the left side of the display, shows the state of
> all switches. ... The number on the left indicates the column, the number
> on the right indicates the row. Example - Switch 23 is 2nd column, 3rd
> row.

This is the primary-source statement that fixes `address = column*10 + row`
for this manual, used throughout the curator to align the Switch Matrix and
Lamp Matrix wiring tables with the printed parts lists.

## T.14 Bigfoot Test (PDF page 36, printed 1-16)

> T.14 Bigfoot Test — The Bigfoot Test has three options: 1) Head Motor
> Test; 2) Head Opto Test; 3) Head Position Test. Press the Up or Down
> button to select an option, (an option flashes when it is selected).
> Press the Enter button to begin. Press the Escape button to stop the
> option and return to the Bigfoot Test Menu.
>
> 1) Head Motor Test — The head rotates continuously. The direction CW
> (clock-wise) or CCW (counter clock-wise) shows on the display. Press the
> Up or Down button to change the direction of the head rotation.
>
> 2) Head Opto Test — The head rotates continuously. The display shows two
> boxes, one for Opto 1 and the other for Opto 2. When the switch makes, an
> "X" appears in the appropriate box. When the switch breaks the "X"
> disappears.
>
> 3) Head Position Test — The head turns intermittently. The display shows
> the position of the head.

This confirms the physical Bigfoot mechanism has exactly two position
sensors (named "Opto 1"/"Opto 2" by the diagnostic menu itself, matching
switch matrix addresses 86/87 "Bigfoot Opto 1"/"Bigfoot Opto 2"), a single
reversible drive motor (Head Motor Test drives it continuously in a
selectable direction — matching solenoid 26 "Bigfoot Enable" as the
direction control and solenoid 25 "Bigfoot Drive" as the step/run pulse),
and a small number of named head positions (Head Position Test just reports
"the position", not a numeric step count, consistent with the retained
script's four named positions Left/Diverter, Up, Right/Unknown,
Down/Player derived from the same two-bit opto code).
