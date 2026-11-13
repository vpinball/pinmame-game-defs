# Breakshot — redemption mode and the optional dispensers

Read from `Capcom_1996_Breakshot_Manual.pdf` (Capcom PM00147, issue 05/02/96). PDF page = printed page + 4,
except the wiring sheets at the back, which carry no printed page number. The menu and test pages have a text
layer, checked against 300 dpi renders; the prose is summarized here rather than copied, and the adjustment
names, ranges, models and connector labels are literal. PDF page 145 has no text layer; its labels were read
from a 300 dpi render.

## What the manual says the machine can carry

- PDF 24, printed 20 (menu overview): menu `F. REDEMPTION` configures the game as a redemption game, dispensing tickets or
  tokens when a preset score is reached, and is not available in every software version.
- PDF 55, printed 51 (`F. REDEMPTION`, headed `(NOT AVAILABLE IN ALL VERSIONS OF SOFTWARE)`): the menu applies
  when the game is equipped with an optional ticket or token dispenser. Five scoring levels each set a score,
  a payout, a mechanism (`TOKEN, TICKET, CREDIT, XBALL`) and a percentage (F1-01 to F1-01L for the first three);
  prizes are paid as each level is reached within a time limit, after which the game continues with the
  dispenser disabled.
- PDF 29, printed 25, adjustment `B1-16+ TICKET DISPENSER`, range `NONE` / `STANDARD TICKET`, factory `NONE`:
  selects the ticket dispenser type if one is installed. `TICKET DISPENSERS CURRENTLY SUPPORTED: 1) DELTRONICS,
  MODEL 1275; 2) COIN CONTROLS, MODEL CTD10.` Entering a dispenser increments audit `A3:27` and pulses the ticket
  motor drive. `B1-16A TICKETS / CREDIT`, range `0, 1 - 99`, factory `0`: tickets per free credit; 0 for a game
  without a ticket dispenser.
- PDF 30, printed 26, adjustment `B1-17+ TOKEN DISPENSER`, factory `NONE`, range `NONE`, `BALLYWULFF DISPENSER`,
  `COIN CONTROLS DISPENSER` and four `COIN CONTROLS COMPACT HOPPER` settings, `(RED DISC)`, `(PURPLE OR GREEN
  DISCS)`, `(GRAY, BLACK, BROWN, OR BLUE DISCS)` and `(5 AWP DISC USED IN ITALY)`: the token dispenser type if one
  is installed. Entering one increments audit `A3:28` and pulses the token meter drive. `B1-17A TOKENS / CREDIT`,
  range `0, 1 - 99`, factory `0`.
- PDF 42, printed 38, test `C1-09 : TICKET DISPENSER TEST`: exercises the ticket dispenser's motor, notch switch
  and meter; it dispenses one ticket, increments the ticket meter and reports `DISPENSED` or `ERROR`.
- PDF 42-43, printed 38-39, test `C1-10 : TOKEN DISPENSER TEST`: activates the dispenser solenoid and pulses the
  ticket meter, one token per test. The manual notes that most token dispensers have no feedback switch, so the
  test normally reports success; one with switch feedback can report `ERROR`.
- PDF 57, printed 53, `F5 : COUNT TOKENS`: empties a token dispenser that has a token switch, counting each token.

The switch table (PDF 82) and the solenoid table (PDF 84) list no dispenser device, and the location drawings
show none.

## PDF 145: `DIAGRAM, PRINTER INTERFACE, WIRING`

Title block: Capcom Coin-Op, Inc.; part no. `PB-6 WIRING`; drawn `B.ZIEGLER`; date `2/27/96`; sheet `10 OF 10`.
The sheet draws one `RS232/ COIN METER PCB` on its own (right half) and, inside a dashed box headed
`GERMAN CONFIGURATION` (left half), the same board with a `TOKEN DRIVER PCB`.

RS232/Coin Meter PCB connectors, as printed on the right-hand drawing (pin 1 first where the drawing marks it):

| Connector | Printed signals and wire colours | Printed destination |
| --- | --- | --- |
| J9 | GND BLK, BUSY BRN/BLK, RTS BRN/RED, TXD BRN/ORG, RXD BRN/YEL, OP3/DTR BRN/GRN, PA0/RI BRN/BLU, PA1/DSR BRN/VIO, PA2/DCD BRN/GRY, KEY, COINMETER 5 BLU/ORG, TICKETMETER 1 BLU/RED, MOTOR_DRV BLU/BRN, VCC GRY | `TO CPU J3` |
| J1 | RI GRY/WHT, KEY (no wire), CTS GRY/BLK, RTS GRY/VIO, DSR GRY/BLU, GND GRY/GRN, DTR GRY/YEL, TXD GRY/ORG, RXD GRY/RED, DCD GRY/BRN | `TO PRINTER CONNECTOR` |
| J10 | GND, MOTOR_EN, NC, NC, NC (pin 1 at GND); no wire colours printed | none printed |
| J8 | GND, GND, KEY, + 12V | none printed |
| J2 | 12-pin, `FEMALE CONN. TO COIN DOOR (SEE 12 PIN CONFIG.)` | coin door |
| P1 | 12-pin, `MALE CONN. TO CABINET (SEE 12 PIN CONFIG.)` | cabinet |
| J3-J7 | three-pin headers, no signals printed | `TO COIN METERS` |
| J11 | three-pin header, nothing printed | none |

`12 PIN CONFIGURATION`: 1 BLK/GRN, 2 GRN/BRN, 3 GRN/RED, 4 GRN/ORG, 5 GRN/YEL, 6 BLK/WHT, 7 WHT/BRN, 8 YEL/BRN,
9 RED/BRN, 10 NC, 11 YEL, 12 BLK.

German configuration, where it differs:

| Board, connector | Printed signals and wire colours | Printed destination |
| --- | --- | --- |
| RS232/Coin Meter J10 | BLK, VIO/RED, NC, NC, NC (the GND and MOTOR_EN positions) | `TO TOKEN DRIVER BOARD J2` |
| RS232/Coin Meter J1 | only GND GRY/GRN, TXD GRY/ORG and RXD GRY/RED wired | `TO PRINTER CONNECTOR` |
| RS232/Coin Meter J9 | as above; its BUSY line BRN/BLK also branches `TO PRINTER CONNECTOR` | `TO CPU J3` |
| RS232/Coin Meter J8 | + 12V branches `TO PRINTER CONNECTOR` | printer |
| Token Driver J2 | DRV_EN VIO/RED, KEY, GND, GND BLK | `TO COIN METER BOARD J10` |
| Token Driver J3 | +50VDC VIO, PGND BLK, KEY, PGND BLK | `TO POWER BOARD` |
| Token Driver J1 | + 50VDC VIO, KEY, DRIVER VIO/BRN | `TO TOKEN DISPENSER` |

The sheet does not show where the ticket dispenser plugs in, nor which line carries its notch switch.

## What the ROM and PinMAME show

- The bsv103 ROM's own Switch Test names a `DISPENSER NOTCH` as its switch `16) WHT-GRY`, and shows that text
  while public 32, 40, 64 or 72 is held (`service-tests.md`). Public 16 is in the cabinet column PinMAME never
  reads on Breakshot, so no public input carries the notch.
- Pinned `src/wpc/capcom.c` comments the CPU's J3 lines as the `Token/Coin Meter/Printer Interface Board` (port A
  PA0-PA2, port B PB2, PB3 and PB6, each marked of unknown purpose) and maps none of them to a public switch,
  solenoid or lamp, so PinMAME publishes no dispenser motor, solenoid or meter.
