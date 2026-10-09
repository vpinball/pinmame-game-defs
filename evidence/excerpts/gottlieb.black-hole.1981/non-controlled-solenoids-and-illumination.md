# Black Hole — Playfields "non-controlled" solenoids and illumination (printed page 45)

Source: the Scribd copy of the Gottlieb *Black Hole Instruction Manual* (document 223467608), viewer page 47 (printed
page 45), headed "PLAYFIELDS "NON-CONTROLLED" SOLENOIDS AND ILLUMINATION", title block "PLAYFIELDS SOLENOIDS AND
ILLUMINA[TION], SYSTEM 80, GAME #668", dated 7-27-81, drawing number cut off after "E-21". Pages 44 and 45 are one
fold-out sheet: the left strip of this page carries the line ends of page 44's lamp list (which completes the words page
44 cuts off), all returning to +6V DC through wire 088. Read from the 904 x 1158 page image, enlarged in four crops.
Contacts are drawn with their relay letter: Q (game over), T (tilt), U (upper) and L (lower); a contact drawn with a
slash is normally closed.

## Lamps not driven by the controller (left strip)

+6V DC (wire 255) through a T contact feeds an "ON GATE SW." changeover: one side (wire 400) lights the lamp labelled
RETURN, the other (wire 411) the lamp labelled OUTLANE.

## Upper playfield coils and flippers (from transformer panel A12J8 / A12P8)

| Feed | Path | Load |
| --- | --- | --- |
| A12P8-3, +24V DC (SOURCE), wire 222 | T contact (wire 888), Q contact, "SWITCHED +24V DC (SOURCE)" wire 388, A9J8-13 | two KICKING RUBBER COILs, each fired by two KICKING RUBBER SW. contacts in parallel; return wire 266 |
| A12P8-5, +38V DC (SOURCE), wire 366 | T contact (wire 488), Q contact, "SWITCHED +38V DC (SOURCE)", A9J8-6/-5 | flipper power |
| A12P8-8, LEFT FLIPPERS SW., wire 055 | U contact (slashed, normally closed), wire 077 | two LEFT FLIPPER COILs, one through TOP LEFT FLIPPER SW., one through BOTTOM LEFT FLIPPER SW. |
| A12P8-7, RIGHT FLIPPERS SW., wire 044 | U contact (slashed), wire 033 | two RIGHT FLIPPER COILs, one through TOP RIGHT FLIPPER SW., one through BOTTOM RIGHT FLIPPER SW. |
| A12P8-11 / -12, FLIPPER SW. RETURN (LEFT) / (RIGHT), wire 388 | | flipper button returns |
| A12P8-4, +6V DC (SOURCE), wire 255 | | lamp supply |

LOWER PLAYFIELD ILLUMINATION: #313 lamps, "(9)", wire 888 through A9J8-9, returned to A12P1 GND.

## Upper playfield general illumination

A12P8-2 6.3V AC (wire 066) and A12P8-1 6.3V AC RETURN (wire 000). Through a T contact and wire 788 (A9J8-14/-10) and a
U contact: POP BUMPERS (4), HOLE (1) and UPPER PLAYFIELD ILLUMINATION ( ) (quantity left blank). A second T contact
switches wire 022 "TO LIGHTBOX TILT LAMP".

## Upper pop bumpers (driver boards A8)

| Board | Switch (wire) | Output to coil (wire) | Fuse |
| --- | --- | --- | --- |
| 1A8J1 | UPPER CENTER POP BUMPER SW. (077) | 188 | F12 2 1/2 AMP SLO-BLO (244/266) |
| 2A8J1 | LOWER CENTER POP BUMPER SW. (011) | 488 | F13 2 1/2 AMP SLO-BLO (255/266) |
| 3A8J1 | RIGHT POP BUMPER SW. (022) | 888 | F10 2 1/2 AMP SLO-BLO (277/266) |
| 4A8J1 | BOTTOM POP BUMPER SW. (033) | 266 | F11 2 1/2 AMP SLO-BLO (288/266) |

Each board takes DC GROUND (wire 9), INPUT +5V DC (wire 688) and GROUND BUS on J1 pins 6, 5 and 2, the switch on pin
4 and the coil output on pin 1; the fuses feed the coils from "SWITCHED +38V DC". The +5V DC (SOURCE) and DC GROUND come
from A1J6-18 and A1J6-9 of the control board.

## Dashed block "LOCATED ON LOWER PLAYFIELD"

| Board or feed | Detail |
| --- | --- |
| 5A8J1 | RIGHT POP BUMPER SW. (011); output wire 188 to the POP BUMPER COIL (wire 133), F21 2 AMP SLO-BLO |
| 6A8J1 | CENTER POP BUMPER SW. (022); output wire 166 to the POP BUMPER COIL (wire 144), F22 2 AMP SLO-BLO |
| A9P8-13, SWITCHED +24V DC (wire 388) | KICKING RUBBER COIL fired by two KICKING RUBBER SW. contacts; KICKING TARGET COIL fired by KICKING TARGET SW. |
| A9P8-6 (wire 055) | L contact (normally open), wire 111, LEFT FLIPPER COIL through LEFT FLIPPER SW. |
| A9P8-5 (wire 044) | L contact (normally open), wire 333, RIGHT FLIPPER COIL through RIGHT FLIPPER SW. |
| A9P8-14 (wire 788) | L contact, wire 077: 6.3V AC PLAYFIELD ILLUMINATION ( ) and POP BUMPERS (2), 6.3V AC RETURN on A9P8-10 (wire 000) |
| A9P8-9 (wire 888) | L contact: SWITCHED +24V DC |
| A9P8-15 | GROUND |

The lower block's +5V DC and ground reach the boards through A9J7/A9P7 9-12.
