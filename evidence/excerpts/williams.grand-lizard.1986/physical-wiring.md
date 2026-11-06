# Grand Lizard physical power wiring

Preliminary manual PDF 14-16 (printed 12-13), Cabinet Wiring Diagram and Power
Wiring Diagram. Curator visually read the native renders; crops retain the
load-bearing GI and flipper branches. This is drawing transcription, not a new
complete circuit specification. Plug labels, wire names and topology are literal.

## General illumination: PDF 16

Power supply 3J8/3P8 has four returns 1 BRN, 2 YEL, 3 GRN, 4 VIO and four fused
outputs 6 WHT-BRN, 7 WHT-YEL, 8 WHT-GRN, 9 WHT-VIO, all fuses 5ASB. Relay contacts
are in the two supply branches feeding 6 and 7. The two branches feeding 8 and 9
do not pass through those contacts.

The BRN/WHT-BRN pair reaches backbox 9P2/9J2 pins 1/2; GRN/WHT-YEL reaches
9P2/9J2 pins 3/4. The YEL/WHT-YEL pair also reaches cabinet 7P6/7J6 pins 2/3,
then 7P4/7J4 pins 1/2. On PDF 14, 7J4 feeds the coin-door GENERAL ILLUMINATION
lamp symbols. Playfield 8P4/8J4 pins 3/4 carry GRN/WHT-GRN and pins 6/5 carry
WHT-VIO/VIO. Their source branches 8/9 are unswitched by this relay.

Thus the solenoid 11 relay (production solenoid table: CPU 1P12-4 to 3P7-1)
interrupts backbox/cabinet GI, while the depicted playfield GI branches stay on.
The retained VPX's `PFGI` dims playfield lights and render materials from 11;
that is a table lighting shortcut. The PinMAME `grand_` brightness-type block
itself calls 11 Backbox GI. No playfield-emitter coordinate is assigned to 11.
The repeated schematic lamp symbols are illustrative branches, not a counted
socket inventory. No bulb quantity is inferred from their drawing repetition.

## Flipper contacts: PDF 14-15

The cabinet sheet calls 7SW72 RIGHT FLIPPER and 7SW73 LEFT FLIPPER, drawing
normally-open cabinet contacts; the right button has a second ganged contact
feeding the upper-right coil. The power sheet labels the right feed ORG-VIO
from 1P19-1 and left feed ORG-GRY from 1P19-2; the returns to the coils include
BLK-YEL upper-right, BLU-VIO lower-right and BLU-GRY lower-left.

This preliminary sheet draws only three flippers although the final production
table lists four, including upper-left FL24/600-30/2600-50VDC. Its EOS symbols
are drawn open; the production flipper assembly notes instead say the contacts
fully open with the flipper actuated, so their rest construction is closed.
These schematic omissions/misprints do not change the two open cabinet buttons
or PinMAME's synthetic 45-48 contract. No emulator matrix EOS is synthesized.

The production assembly PDF 43 distinguishes item 2a, 03-7811 End of Stroke (EOS)
Switch, and 2b, SW-1A-150 Lane Change Switch. The parts list PDF 48 assigns only
the latter to matrix 48. The left lower assembly uses unique parts B-10655-L
and C-9957-L; the right assembly is C-9952-R.

## Relay-controlled magnet loads

Production PDF 50 explicitly calls 9/10 Left/Right Magnet Relay, with relay part
5580-09613-00. PDF 43 separately identifies A-8447 Magna-Save. A controller
output therefore energizes a relay whose contacts power its magnetic assembly;
the normalized effect coordinate, when present, locates the magnet acting on
the ball and is not a measured relay-coil center.
