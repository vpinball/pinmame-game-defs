# Bally Elvira and the Party Monsters (1989) — Solenoids & Flashers table, switched A/C bank

Source: Bally Midway *Elvira and the Party Monsters* Operations and Parts Information Manual
16-2011-101, IPDB machine 782 file `Elvira_and_the_Partymonsters_OCR_searchable.pdf`, PDF page 66,
printed page 2-14, upper half of the table. Read from the native 300 dpi render. The same table is
printed again on PDF page 2 (the ROM summary sheet) and PDF page 43 (printed 1-37, inside the
Solenoid Test text); the continuation is in `solenoid-table-controlled-special.md`.

Column headings as printed: `Sol. No.`, `Function`, `Solenoid Type`, `Wire Color`,
`Connections: CPU Board`, `Connections: Playfield/Cabinet`, `Driver Trnstr`,
`Solenoid Part No. / Flashlamp Type / i = Insert Bd ; p = Playfield`.

Each A/C pair shares one driver transistor and one CPU-board pin. The table prints the pair's A-side
wire in the first row and the C-side wire in the second, joined by a brace; the CPU Board cell prints
the pin in the first row and the grey control wire in parentheses in the second. Cells printed blank
are marked *(blank)*.

| Sol. No. | Function | Type | Wire | CPU Board | Playfield/Cabinet | Driver | Part No. / Flashlamp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01A³ | Outhole Kicker | Switched | Vio-Brn | 1P11-1 | 5J1-9: 5J4-9 (A) | Q33 | AE-23-800 |
| 01C³ | Jets (p)/Bats (i) | Switched | Blk-Brn | (Gry-Brn) | 5J5-9 (C) | Q33 | #906/#89 flashlamps 1p,1i |
| 02A³ | Ball Eject (Shtr Lane Feeder) | Switched | Vio-Red | 1P11-3 | 5J1-7: 5J4-8 (A) | Q25 | AE-23-800 |
| 02C³ | Organ Flasher | Switched | Blk-Red | (Gry-Red) | 5J5-8 (C) | Q25 | #906 flashlamp 1p |
| 03A³ | Drop Target Bank | Switched | Vio-Orn | 1P11-4 | 5J1-6: 5J4-7 (A) | Q32 | AE-26-1200 |
| 03C³ | Right Ramp (p)/Punch (i) | Switched | Blk-Orn | (Gry-Orn) | 5J5-7 (C) | Q32 | #906/#89 flashlamps 1p,1i |
| 04A³ | *(blank)* | Switched | Vio-Yel | 1P11-5 | 5J1-5: 5J4-6 (A) | Q24 | *(blank)* |
| 04C³ | Left Ramp (p)/Drac (i) | Switched | Blk-Yel | (Gry-Yel) | 5J5-6 (C) | Q24 | #906/#89 flashlamps 1p,1i |
| 05A³ | Eject Hole | Switched | Vio-Grn | 1P11-6 | 5J1-4: 5J4-5 (A) | Q31 | AE-23-800 |
| 05C³ | Moon (p)/ Wolfman (i) | Switched | Blk-Grn | (Gry-Grn) | 5J4-5 (C) | Q31 | #906/#89 flashlamps 2p,1i |
| 06A³ | Ball Popper | Switched | Vio-Blu | 1P11-7 | 5J1-3: 5J4-4 (A) | Q23 | AE-23-800 |
| 06C³ | Right Return (p)/ Hot Dog,BBQ,Bun (i) | Switched | Blk-Blu | (Gry-Blu) | 5J5-4 (C) | Q23 | #906/#89 flashlamps 1p,3i |
| 07A³ | Knocker | Switched | Vio-Blk | 1P11-8 | 5J1-2: 5J4-3 (A) | Q30 | AE-23-800 |
| 07C³ | Left Return (p)/Letters (i) | Switched | Blk-Vio | (Gry-Vio) | 5J5-3 (C) | Q30 | #906/#89 flashlamps 1p,3i |
| 08A³ | Ball Lock Release | Switched | Vio-Gry | 1P11-9 | 5J1-1: 5J4-2 (A) | Q22 | AE-23-800 |
| 08C³ | Skull (p)/ House (i) | Switched | Blk-Gry | (Gry-Blk) | 5J5-2 (C) | Q22 | #906/#89 flashlamps 1p,1i |

Literal details kept as printed:

- 04A³ prints no Function and no part number, but does print its wire, CPU pin, board connection
  and driver transistor. Those are Aux Power Driver Board terminals that every A/C pair has.
- 05C³ prints its C-side connection as `5J4-5 (C)`. Every other C-side row prints a `5J5-` pin, and
  `5J4-5` is also the 05A³ A-side pin. The cell is transcribed as printed, not corrected.
- The superscript 3 on every Sol. No. refers to note [3] under the table: *"A" circuits are pulsed,
  when Sol. 12 is de-energized; "C" circuits are pulsed, with Sol. 12 energized. Wire colors in
  brackets are those from respective "A" and "C" terminals corresponding to the J1-terminal
  connection listed for the Aux Power Driver Bd, which controls the device pulsing by Sol. 12.*

Printed page 1-38 (PDF page 44), the text under Figure 4, describes the same relay: in its
de-energized state it connects "circuit A power" to the controlled and switched solenoids, and when
energized it connects "circuit C power" to the eight group C solenoids 01C through 08C. Its worked
example calls sol. 01C "the Transporter Flashers circuit", which is a leftover from another machine's
manual; on this machine 01C is Jets (p)/Bats (i).
