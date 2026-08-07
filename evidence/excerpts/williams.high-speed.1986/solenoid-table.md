# High Speed — Solenoid Table

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 33 (printed page 25, inside the
Test/Diagnostic Procedures section, under SOLENOID TEST), read from a 300 dpi `pdftoppm` render. A
second identical copy of this table is bound at PDF page 59 alongside the ROM Summary in this
rebound copy; both were compared and agree cell for cell.

This is the wiring table of record for outputs. The "Sol. No." column is the public PinMAME solenoid
address on this platform — see the SOLENOID TEST text quoted below, which cycles test steps 01
through 22 and matches the table one-for-one.

## Column headings, verbatim

`Sol. No. | Function | Solenoid Type | Wire Color | Connections: CPU Bd. | Connections: Playfield/Cabinet | Driver Trans. | Solenoid Part No.`

## The table, verbatim

| Sol. No. | Function | Solenoid Type | Wire Color | CPU Bd. | Playfield/Cabinet | Driver Trans. | Solenoid Part No. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Outhole | Controlled | Gry-Brn | 1P11-1 | 8P3-1 | Q33 | AE-23-800-01 |
| 02 | Ball Release | Controlled | Gry-Red | 1P11-3 | 8P3-2 | Q25 | AE-23-800-03 |
| 03 | Eject Hole | Controlled | Gry-Orn | 1P11-4 | 8P3-3 | Q32 | AE-23-800-03 |
| 04 | Police Light Relay | Controlled | Gry-Yel | 1P11-5 | Backbox | Q24 | 5580-10883-00 |
| 05 | Flasher No. 2 (Left Blue) | Controlled | Gry-Grn | 1P11-6 | 8P3-5 | Q31 | #63 flashlamps |
| 06 | Flasher No. 3 (Right Blue) | Controlled | Gry-Blu | 1P11-7 | 8P3-6 | Q23 | #63 flashlamps |
| 07 | Left Hideout Relay | Controlled | Gry-Vio | 1P11-8 | 8P3-7 | Q30 | AE-24-900-02 |
| 08 | Right Hideout Relay | Controlled | Gry-Blk | 1P11-9 | 8P3-8 | Q22 | AE-24-900-02 |
| 09 | Flasher No. 1 (Left Red) | Controlled | Brn-Blk | 1P12-1 | 8P3-9 | Q17 | #63 flashlamps |
| 10 | Insert Board Flashers | Controlled | Brn-Red | 1P12-2 | 9P1-7 | Q9 | #63 flashlamps |
| 11 | General Illumination Relay | Controlled | Brn-Orn | 1P12-4 | 3P7-1 | Q16 | 5580-09555-00 |
| 12 | Flasher No. 4 (Right Red) | Controlled | Brn-Yel | 1P12-5 | 8P3-12 | Q8 | #63 flashlamps |
| 13 | Ramp Gates | Controlled | Brn-Grn | 1P12-6 | 8P3-13 | Q15 | AL-23-800-01 |
| 14 | Kickback (Left Outlane) | Controlled | Brn-Blu | 1P12-7 | 8P3-14 | Q7 | AE-24-900-01 & Relay |
| 15 | Knocker | Controlled | Brn-Vio | 1P12-8 | Backbox | Q14 | AE-23-800-02 |
| 16 | Coin-Lockout Relay | Controlled | Brn-Gry | 1P12-9 | 7P1-7, 7P2-4 | Q6 | 404603-22 (note 2) |
| 17 | Left Kicker | Special #1 | Blu-Brn | 1P19-7 | 8P3-17 | Q75 | AE-23-800-03 |
| 18 | Right Kicker | Special #2 | Blu-Red | 1P19-4 | 8P3-18 | Q71 | AE-23-800-03 |
| 19 | Right Jet Bumper | Special #3 | Blu-Orn | 1P19-3 | 8P3-19 | Q73 | AE-23-800-03 |
| 20 | Lower Left Jet Bumper | Special #4 | Blu-Yel | 1P19-6 | 8P3-20 | Q69 | AE-23-800-03 |
| 21 | Upper Left Jet Bumper | Special #5 | Blu-Grn | 1P19-8 | 8P3-21 | Q77 | AE-23-800-03 |
| 22 | Top Playfield Flashers | Special #6 | Blu-Blk | 1P19-9 | 8P3-22 | Q79 | #63 flashlamps |
| — | Upper Flipper | — | (Blk-Yel) | — | (7J1-19, 8P3-33) | — | FL 23/600-30/2600-50VDC |
| — | Right Flipper | — | Orn-Vio (Blu-Vio) | 1P19-1 | 7P1-20 (7J1-21, 8P3-34) | — | FL 23/600-30/2600-50VDC |
| — | Left Flipper | — | Orn-Gry (Blu-Gry) | 1P19-2 | 7P1-23 (7J1-24, 8P3-32) | — | FL 23/600-30/2600-50VDC |

## Notes printed under the table, verbatim

> 1. Wire colors, except flipper Orn-Vio and Orn-Gry, are ground connections (to coil terminal with
>    unbanded end of diode). Flipper Orn-Vio and Orn-Gry wires connect from CPU Board to flipper
>    switch.
> 2. Solenoid 16 has a Coinco part number.
> 3. Connections shown in parentheses are from flipper switch to flipper coil.

## What the table establishes

- **Addresses 1-16 are all printed "Controlled" and 17-22 "Special #1" through "Special #6".** This
  manual uses no "Switched"/"A-side"/"C-side" wording at all, unlike the later System 11B manuals: the
  game has no A/C multiplex relay, so addresses 1-8 have no "C" partner and the platform's 25-32 alias
  bank is never populated.
- **The Special # ordering is sequential against the public address**: Special #1 is 17, #6 is 22.
- **There is no solenoid number for any flipper coil.** The three flipper rows print `—` in the Sol.
  No. and Driver Trans. columns. Notes 1 and 3 together say the CPU board line (Orn-Vio, Orn-Gry, at
  1P19-1 and 1P19-2 on the *special-solenoid* connector) runs to the flipper switch, and a separate
  wire runs from the flipper switch to the coil: the coils are fired by the cabinet button through the
  switched-solenoid supply, not by a CPU driver transistor.
- **Only one General Illumination circuit exists** (address 11) and its part is a relay, not a coil.
- **Addresses 4 and 15 are the only two whose Playfield/Cabinet connection reads "Backbox"**, and
  address 10 is the only one that lands on connector 9 (the backbox Insert Board — see
  `diagnostics-and-amendments.md` for the board-number list). Address 16 is the only one on connector 7
  (the cabinet).
- **There is no drop-target reset coil anywhere in this table**, and no coil for any of the three
  "Stoplight Bank" target groups: those are standup targets, not drop targets.

## SOLENOID TEST text on the same page, verbatim excerpt

> 1. (From Lamp Test) Using AUTO-UP, press ADVANCE. Observe that the SPEEDER 1 and 2 displays show the
>    message, COIL TEST, the Credit display shows 04 (Solenoid Test identifier). Next, the BALL IN
>    PLAY/MATCH display shows a series of test steps from 01 through 22, while the SPEEDER 1 and 2
>    displays show the name of the solenoid. During each of these steps, pulsing of the respective
>    solenoid occurs. The test cycles repeatedly, unless halted via the MANUAL-DOWN switch. Refer to
>    the Solenoid Table for solenoid numbers and wiring information. CPU Board connections at 1P11,
>    1P12, and 1P19 are also listed in the table.
>
>    To continuously pulse a single solenoid, use MANUAL-DOWN. Press ADVANCE to sequence through the
>    controlled and special solenoids. Use AUTO-UP to resume test cycling, and to proceed to the next
>    test.

The test range 01-22 with no gaps is the manual's own confirmation that the Sol. No. column is a
contiguous public numbering rather than a test-order column.
