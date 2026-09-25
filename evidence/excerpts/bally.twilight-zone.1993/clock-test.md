# Twilight Zone — T.14 Clock Test (printed 1-18)

Transcribed from `Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf` (the complete IPDB copy of
operations manual 16-50020-101), PDF page 26, printed page 1-18. Read from the 300 dpi render; the PDF's OCR layer was
used only to find the page. The whole T.14 text block is transcribed; the display-panel drawing at the foot of the
page is described, not reproduced.

> **T.14 Clock Test** This test may be used to test the mechanical clock in the game.
> There are 8 opto sensors used to monitor the position of the clock hands. These 8 sensors are
> wired in as a 9th column in the switch matrix. The column drive is the Gray-White wire attached
> to pin J5-1 of the 8-Driver P.C.B. Assembly, pt #A-16100, (located on the left side-wall of the
> backbox). This column is driven by Q1 and Q12 of the 8-Driver Board. The switch matrix row
> connections are made to the normal white "row" switch matrix wires. This 9th column is shown
> on the far right of the switch matrix, in the clock test:

| Row | Column 9 (Gry-Wht) |
| --- | --- |
| Row 1 (Wht- Brn) | 15 minutes |
| Row 2 (Wht- Red) | 0 minutes |
| Row 3 (Wht- Org) | 45 minutes |
| Row 4 (Wht- Yel) | 30 minutes |
| Row 5 (Wht- Grn) | Hour 1 |
| Row 6 (Wht- Blu) | Hour 2 |
| Row 7 (Wht- Vio) | Hour 3 |
| Row 8 (Wht- Gry) | Hour 4 |

> The clock is operated through a D.C. Motor Control Board, pt #A-16120, (located UNDER the
> playfield at approximately the same position as the clock) and solenoid drives 42 and 43
> (located on the 8-Driver Board in the backbox). With only drive 43 turned ON, the clock moves
> forward. With only drive 42 turned ON, the clock moves in reverse. With both drives ON, or
> both drives OFF, the clock is stopped.
>
> **Using the clock test program:** The top line will show the current operation. Use the
> red "+" and "-" coin door buttons to select one of the following functions:
>
> Clock Forward Slow
> Clock Forward Fast
> Clock Reverse Slow
> Clock Reverse Fast
>
> Pressing the "Enter" button will "start" and "stop" the selected operation.
>
> The display will indicate the state of the switch matrix and the clock, as shown below:

Below the text the page draws the "DISPLAY PANEL VIEW": the switch matrix at the left (Dedicated Switch Column,
Switch Columns 1-8, Flipper Switch Column, Switch Column 9), and at the right the top line `CLOCK FWD SLOW`, four
minute-opto boxes labelled 00 15 30 45 with `0:00` "(Time at Last Quarter Hour)", and four HOUR OPTOS boxes labelled
Hour 4 (left) to Hour 1 (right) with `12 HOUR` "(Derived From Hour Optos, See Table Below)".

Drives 42 and 43 are the 8-Driver Board's own numbers (public PinMAME solenoids 56 and 57). The 9.2 ROM numbers this
test T.16, because it inserts T.14 LAMP ROW/COLUMN and T.15 DIP SW. TEST before it.
