# The Machine: Bride of Pinbot — Helmet, Chase Light board, and helmet test (printed 2-27, 2-32, 3-6, 1-35)

Source: `the_machine_operations_manual.pdf`, PDF pages 95 (printed 2-27), 100 (printed 2-32),
120 (printed "PAGE 3-6 CHASE LIGHT"), and 55 (printed 1-35). Parts pages were read from 110 dpi
overview renders of the native 300 dpi scan; the test text from the OCR text layer, checked against
the rendered page.

## A-14007 Chase Light Assembly (printed 2-27)

| Item | Part Number | Ckt Designator | Description |
| --- | --- | --- | --- |
| 1 | 5768-12705-00 | | PCB Chase Light |
| 2 | 5162-08976-00 | Q1 - Q16 | Tras. 2N6427 NPN |
| 3 | 5010-08997-00 | R10 - R25 | Resistor, 2.7KΩ, 1/4w, 5% |
| 4 | 5010-09034-00 | R7 - R9 | Resistor, 10KΩ, 1/4w, 5% |
| 5 | 5010-09358-00 | R3, R4 | Resistor, 1KΩ, 1/4w, 5% |
| 6 | 5010-09162-00 | R5 | Resistor, 100KΩ, 1/4w, 5% |
| 7 | 5010-09113-00 | R6 | Resistor, 33KΩ, 1/4w, 5% |
| 8 | 5010-08930-00 | R1, R2 | Resistor, 470Ω, 1/4w, 5% |
| 9 | 5040-09365-00 | C2 | Capacitor, 1µfd, 63v (+50, -10%) |
| 10 | 5040-09421-00 | C1 | Capacitor, 100µfd, 25v (+50, -10%) |
| 11 | 5043-08980-00 | BYC1 - BYC4 | Capacitor, .01µfd, 50v, (+80, -20%) |
| 12 | 5281-09867-00 | U4, U5 | IC, 74LS244, Oct. Buff |
| 13 | 5281-10447-00 | U2, U3 | IC, 74LS164 |
| 14 | 5370-12272-00 | U1 | IC, LM339 Quad. Comp |
| 15 | 5250-09157-00 | U6 | Reg 7805, 1.0A. 5V |
| 16 | 5791-10862-05 | J1 | Connector, 5-pin Header |
| 17 | 5791-10862-10 | J2, J3 | Connector, 10-pin Header |
| 18 | 4004-01005-06 | | Mach. Screw, 4-40 x 3/8 |
| 20 | 4404-01119-00 | | Lockwasher Nut, 4-40 |

The board drawing labels J1 `DATA`, `CLK`, `GND`, `KEY`, `+12VDC`; J2 `L1`-`L8` plus `B+`; J3
`L9`-`L16` plus `B+`. Item 19 is not printed.

## Chase Light schematic (printed "PAGE 3-6 CHASE LIGHT", drawing A-14007, sheet 2 of 2)

J1 `DATA` and `CLOCK` enter through LM339 comparators (U1) into two cascaded 74LS164 serial-in
shift registers (U2, U3). Their sixteen outputs pass through two 74LS244 buffers (U4, U5) and
2.7 kΩ base resistors to sixteen 2N6427 transistors Q1-Q16, whose collectors are the lamp returns
on J2 and J3. A 7805 (U6) makes +5 V from J1's +12 VDC.

## A-14508 Helmet Assembly (printed 2-32)

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | 03-8548 | Helmet |
| 2 | 03-8149-9 | Mini Dome, Tr. Red |
| 3 | C-13337 | Single Flashlamp Assy. |
| 4 | 03-8022-4 | Spacer, 1/4" Lg. |
| 5 | 03-6047-1 | Spacer, 1/4" Lg. |
| 6 | 03-6047-3 | Spacer, 1/2" Lg. |
| 7 | 4106-01001-16 | Sh. Metal Screw, #6 x 1" |
| 8 | 4006-01003-12 | Mach. Screw, 6-32 x 3/4 |
| 9 | 4700-00070-00 | Flatwasher, 3/16 x 5/8 x 16ga. |
| 10 | 31-2-50002-1 | Decal |
| 11 | H-14425-7 | Helmet Cable |
| 12 | A-14410 | 8-Lamp Board |
| 13 | A-14412 | 8-Lamp Board |
| 14 | 4406-01128-00 | Nut, 6-32 KEPS |
| 15 | 03-7722-4 | Clip, 1/4" |
| 16 | 03-8063-6 | Yellow Light Bulb Sleeve |
| 17 | 03-8063-4 | Red Light Bulb Sleeve |

The drawing shows a U-shaped helmet open toward the bottom of the page with sixteen lamp sockets,
eight on each side on the two 8-lamp boards (item 12 leader to the right side, item 13 to the left
side), a mini dome with a single flashlamp assembly on one side, and the helmet cable.

## T.15 Helmet Light Test (printed 1-35)

> test the 16 lights on top of the helmet. Upon entering this test all lamps on the helmet should
> start blinking on and off. If they all are not, check for a burnt out bulb or socket contact not
> making a good connection or the power to the lights is lost (power is obtained through GI string
> #2). If this all checks out it may be the circuit that controls the lights. The Helmet Light Test
> has three modes: all lamps, single lamp, and cycle lamps.
>
> SINGLE LAMP - This will allow you to turn on each light on the helmet individually. The first
> light on will be in the lower left corner of the helmet. You may then use the the up button to
> move clockwise to the next light or the down button to move counter clockwise to the previous
> light.
>
> CYCLE LAMPS - This combines the above two tests into one self running test. Upon changing to this
> mode the helmet lights will all blink on and off a few times and a single light (starting in the
> lower left corner of the helmet) will turn each light on and off clockwise and then do the same
> counter clockwise.

The page numbers this test T.15; the bop_l7 ROM's own test menu places `HELMET LIGHT` at T.17.
