# Pin-Bot — Solenoid Table (printed page 27)

Source: `PinBot Instruction Manual & Schematics 600 dpi scan.pdf` (72 pages, SHA-256
`b20e98516ec75d5af42f2dff5304221d7eaea0e6bc7734898c64d98305d22e53`), PDF page 33 (printed
"PIN-BOT 27", Test/Diagnostic Procedures (Continued), Solenoid Test). Read from a rendered page image
of the 600 dpi scan, which has no text layer. Every row is transcribed. Superscript note markers are
written as `^n`.

Printed text above the table: "SOLENOID TEST. 1. (From Lamp Test) Using AUTO-UP, press ADVANCE.
Observe that the player 1 and 2 displays show the message, COIL TEST, the Credit display shows 04
(Solenoid Test identifier). Next, the BALL IN PLAY/ MATCH display shows a series of test steps from
01 through 22, while the player 1 and 2 displays show the name of the solenoid. During each of these
steps, pulsing of the respective solenoid occurs. The test cycles repeatedly, unless halted via the
MANUAL-DOWN switch. Refer to the Solenoid Table for solenoid numbers and wiring information. CPU
Board connections at 1P11, 1P12, and 1P19 are also listed in the table. To continuously pulse a
single solenoid, use MANUAL-DOWN. Press ADVANCE to sequence through the switched, controlled, and
special solenoids. Use AUTO-UP to resume test cycling, and to proceed to the next test."

## PIN-BOT Solenoid Table

Column headers: Sol. No. | Function | Solenoid Type | Wire Color ^1 | Connections: CPU Bd. and
Playfield/ Cabinet | Driver Trans. | Solenoid Part No.

| Sol. No. | Function | Solenoid Type | Wire Color ^1 | CPU Bd. | Playfield/Cabinet | Driver Trans. | Solenoid Part No. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01A^3 | Outhole | Switched | Vio-Brn | 1P11-1 | 8P3-1 (to B1 on Diode Sw. Bd.) | Q33 | AE-23-800-01 |
| 01C^3 | Knocker | Switched | Blk-Brn | (Gry-Brn) | 8P3-1 (to B1 on Diode Sw. Bd.) | Q33 | AE-23-800-02 |
| 02A^3 | Ball Trough Feeder | Switched | Vio-Red | 1P11-3 | 8P3-2 (to B2 on Diode Sw. Bd.) | Q25 | AE-23-800-03 |
| 02C^3 | Upper P'fld & "Top" Flashers (2) | Switched | Blk-Red | (Gry-Red) | 8P3-2 (to B2 on Diode Sw. Bd.) | Q25 | #89 flashlamps |
| 03A^3 | Single Eject Hole | Switched | Vio-Orn | 1P11-4 | 8P3-3 (to B3 on Diode Sw. Bd.) | Q32 | AE-23-800-03 |
| 03C^3 | Left Insert Bd. Flasher | Switched | Blk-Orn | (Gry-Orn) | 8P3-3 (to B3 on Diode Sw. Bd.) | Q32 | #89 flashlamps |
| 04A^3 | Drop Target (3-Bank) | Switched | Vio- Yel | 1P11-5 | 8P3-4 (to B4 on Diode Sw. Bd.) | Q24 | AE-23-800-04 |
| 04C^3 | Right Insert Bd. Flasher | Switched | Blk-Yel | (Gry-Yel) | 8P3-4 (to B4 on Diode Sw. Bd.) | Q24 | #89 flashlamps |
| 05A^3 | Ramp Raise | Switched | Vio-Grn | 1P11-6 | 8P3-5 (to B5 on Diode Sw. Bd.) | Q31 | AE-24-900-02 |
| 05C^3 | Lower P'fld & "Top" Flashers (1) | Switched | Blk-Grn | (Gry-Grn) | 8P3-5 (to B5 on Diode Sw. Bd.) | Q31 | #89 flashlamps |
| 06A^3 | Ramp Lower (Outer) | Switched | Vio-Blu | 1P11-7 | 8P3-6 (to B6 on Diode Sw. Bd.) | Q23 | SM-26-600-DC |
| 06C^3 | Energy Flashers | Switched | Blk-Blu | (Gry-Blu) | 8P3-6 (to B6 on Diode Sw. Bd.) | Q23 | #89 flashlamps |
| 07A^3 | Left Eject Hole (Visor) | Switched | Vio-Vio | 1P11-8 | 8P3-7 (to B7 on Diode Sw. Bd.) | Q30 | AE-23-800-03 |
| 07C^3 | Left Playfield Flasher | Switched | Blk-Vio | (Gry-Vio) | 8P3-7 (to B7 on Diode Sw. Bd.) | Q30 | #89 flashlamps |
| 08A^3 | Right Eject Hole (Visor) | Switched | Vio-Gry | 1P11-9 | 8P3-8 (to B8 on Diode Sw. Bd.) | Q22 | AE-23-800-03 |
| 08C^3 | Sun Flasher | Switched | Blk-Gry | (Gry-Blk) | 8P3-8 (to B8 on Diode Sw. Bd.) | Q22 | #89 flashlamps |
| 09 | Robot Face - Insert Bd. | Controlled | Brn-Blk | 1P12-1 | 8P3-9 | Q17 | #1251 flashlamps |
| 10 | Right Visor - Gen. Illumin. | Controlled | Brn-Red | 1P12-2 | 8P3-10 | Q9 | #1251 flashlamps |
| 11 | General Illumin. - Insert Bd. | Controlled | Brn-Orn | 1P12-4 | 8P3-12 | Q16 | 5580-09555-01 ^4 |
| 12 | General Illumin. - Playfield | Controlled | Brn-Yel | 1P12-5 | 3P7-1 | Q8 | 5580-09555-01 ^4 |
| 13 | Visor Motor | Controlled | Brn-Grn | 1P12-6 | 8P3-13 | Q15 | 5580-09555-01 ^4 |
| 14 | Solenoid Select Relay | Controlled | Brn-Blu | 1P12-7 | 8P3-14 | Q7 | 5580-09555-01 ^4 |
| 15 | "Top" Flashers (3) | Controlled | Brn-Vio | 1P12-8 | 8P3-15 | Q14 | #89 flashlamps |
| 16 | "Top" Flashers (4, center) | Controlled | Brn-Gry | 1P12-9 | 8P3-16 | Q6 | #89 flashlamps |
| 17 | Lower Jet Bumper | Special #1 | Blu-Brn | 1P19-7 | 8P3-17 | Q75 | AE-23-800-03 |
| 18 | Left Visor Gen. Illumin. | Special #2 | Blu-Red | 1P19-4 | 8P3-18 | Q71 | #1251 flashlamps |
| 19 | Left Jet Bumper | Special #3 | Blu-Orn | 1P19-3 | 8P3-19 | Q73 | AE-23-800-03 |
| 20 | Left Kicker | Special #4 | Blu-Yel | 1P19-6 | 8P3-20 | Q69 | AE-23-800-03 |
| 21 | Right Kicker | Special #5 | Blu-Grn | 1P19-8 | 8P3-21 | Q77 | AE-23-800-03 |
| 22 | Upper Jet Bumper | Special #6 | Blu-Blk | 1P19-9 | 8P3-22 | Q79 | AE-23-800-03 |
| - | Right Flipper | - | Orn-Vio [Blu-Vio] | 1P19-1 | 7P1-20 [7J1-21,8P3-34] ^2 | - | FL23/600-30/2600-50VDC |
| - | Left Flipper | - | Orn-Gry [Blu-Gry] | 1P19-2 | 7P1-23 [7J1-24,8P3-32] ^2 | - | FL23/600-30/2600-50VDC |

Layout notes:

- The table has 32 rows: 16 Switched (eight A/C pairs, 01A-08C), 8 Controlled (09-16), 6 Special
  (17-22) and 2 flipper rows.
- The Wire Color column prints each A/C pair inside one brace (for example "Vio-Brn" / "Blk-Brn"),
  so the pair is joined, but each of the two wire colours is printed on its own line; both are written
  here on their own row. The Vio-Yel cell on row 04A prints a space after the hyphen ("Vio- Yel").
- The CPU Bd. value is printed on the A row only (for example 1P11-1); the C row prints a
  parenthesised grey-wire colour ("(Gry-Brn)" and so on) in the same column. The small type in the
  scan reads like "Gry-Bm" / "Gry-Gm" at rows 01C and 05C, written here as Gry-Brn and Gry-Grn.
- The Playfield/Cabinet value ("8P3-n (to Bn on Diode Sw. Bd.)") is printed once for each A/C pair,
  split over two lines ("... (to B1 on" / "Diode Sw. Bd.)"); it is repeated here on both rows.
- The Driver Trans. and Solenoid Part No. columns print a separate value on each A and C row.
- Row 06A prints "Ramp Lower" with "(Outer)" right-aligned in the Function column; the other
  Function cells print only their name.
- The two flipper rows print "-" in Sol. No., Solenoid Type and Driver Trans. The bracketed values
  ([Blu-Vio], [Blu-Gry], [7J1-21,8P3-34], [7J1-24,8P3-32]) are printed on a second line under the
  CPU-board wire colour and connection; the connection brackets carry note marker 2.
- Row 12 prints "3P7-1" in the Playfield/Cabinet column; every other Controlled and Special row
  prints an "8P3-n" connection.
- The Controlled rows skip connection 8P3-11 and CPU pin 1P12-3 (11 prints 8P3-12 / 1P12-4).

## Notes (verbatim)

"Notes: 1. Wire colors, except flipper Orn-Vio and Orn-Gry, are ground connections (to coil terminal
with unbanded end of diode). Flipper Orn-Vio and Orn-Gry wires connect from CPU Board to flipper
switch. 2. Flipper connections shown in braces are from flipper switch to flipper coil. 3. "A" coils
are pulsed, when Sol. 14 is de-energized; "C" coils are pulsed, with Sol. 14 energized. Wire colors in
brackets are those from respective A and C terminals corresponding to the B terminal connection listed
for the Diode Switching Board, which controls the device pulsing by Sol. 14. 4. Relay (p/n
5580-09555-01) is mounted on Relay Snubber Ckt. Bd. p/n C-11232-1."

(The text says "braces" for note 2 and "brackets" for the wire colours; the flipper rows print square
brackets "[ ]" in both places.)

## Comparison with the copy on PDF page 2

PDF page 2 prints the same PIN-BOT Solenoid Table (below the PIN-BOT ROM and Jumper Table) in a
smaller printing. Read row by row against this page: Sol. No., Function, Solenoid Type, Wire Color,
CPU Bd., Playfield/Cabinet, Driver Trans., Solenoid Part No. and the four notes all agree. No
differences. The page 2 copy carries hand-drawn pen marks (underlines/strike lines across the
01A-03A rows, the "Q33", "Q25" and "Q32" cells and a stub at the left margin) which change no printed
text.

Normalization: none, apart from writing the A/C braces as repeated values per row, the superscripts as
`^n`, and the grey-wire colours as printed in parentheses.
