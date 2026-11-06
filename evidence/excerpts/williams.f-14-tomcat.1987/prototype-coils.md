# Preliminary prototype manual coil table

Factory document 16-549-101 P, dated 18 March 1987. Original SHA-256 eefef0ea864ac8b9a613e05b0b59a8143c083081392a9a41bb447564a0edccb7. Primary GPT Sol visually read all six pages at native scan resolution. Method: mixed, reviewed: true. This complete solenoid-table region is PDF page 2, printed 1; normalized row headers/merged cells follow the transcription conventions in manual-tables.md. The table prints four FL11630 flipper coils, before the upper-coil change documented by SS41. It still leaves special 19 Spare (Not Used), rather than fitting an extra upper sling. Its footnote 3 prints Sol. 12 as the A/C selector while the table itself lists 14; this is a printed inconsistency settled for the production emulator contract by the own row 14, final manual and retained script. No exact P-3/P-4/P-5 ROM-to-hardware association is stated here.


Columns: Sol. No.; Function; Solenoid Type; Wire Color¹; Connections: CPU Bd., Playfield/Cabinet; Driver Trans.; Solenoid Part Number / Flashlamp Type (b = Backbox, p = Playfield). A/C connection text spans each pair; repeated in both normalized rows. The printed parenthesized CPU wire on each C row is preserved; wire bracket membership is recorded in JSON. Footnote markers are in the last column.

| Sol. No. | Function | Solenoid Type | Wire Color | CPU Bd. | Playfield/Cabinet | Driver Trans. | Solenoid Part Number / Flashlamp Type | Qty | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01A | Outhole | Switched | Vio-Brn | 1P11-1 | 8P3-1 (to B1 on Diode Sw. Bd.) | Q33 | AE-23-800-01 | — [blank] | 3 |
| 01C | Flasher 1 | Switched | Blk-Brn | (Gry-Brn) | 8P3-1 (to B1 on Diode Sw. Bd.) | Q33 | #89 flashlamps | 2p | 3 |
| 02A | Ball Trough Feeder | Switched | Vio-Red | 1P11-3 | 8P3-2 (to B2 on Diode Sw. Bd.) | Q25 | AE-23-800-03 | — [blank] | 3 |
| 02C | Flasher 2 | Switched | Blk-Red | (Gry-Red) | 8P3-2 (to B2 on Diode Sw. Bd.) | Q25 | #89 flashlamps | 2p | 3 |
| 03A | Ball Popper (Launch) | Switched | Vio-Orn | 1P11-4 | 8P3-3 (to B3 on Diode Sw. Bd.) | Q32 | AE-23-800-12 | — [blank] | 3, 4 |
| 03C | Flasher 3 | Switched | Blk-Orn | (Gry-Orn) | 8P3-3 (to B3 on Diode Sw. Bd.) | Q32 | #89 flashlamps | 2p | 3 |
| 04A | Spare (Not Used) | Switched | Vio-Yel | 1P11-5 | 8P3-4 (to B4 on Diode Sw. Bd.) | Q24 | — [blank] | — [blank] | 3 |
| 04C | Flasher 4 | Switched | Blk-Yel | (Gry-Yel) | 8P3-4 (to B4 on Diode Sw. Bd.) | Q24 | #89 flashlamps | 2p | 3 |
| 05A | Center Right Eject | Switched | Vio-Grn | 1P11-6 | 8P3-5 (to B5 on Diode Sw. Bd.) | Q31 | AE-23-800-11 | — [blank] | 3, 4 |
| 05C | Flasher 5 | Switched | Blk-Grn | (Gry-Grn) | 8P3-5 (to B5 on Diode Sw. Bd.) | Q31 | #89 flashlamps | 2p | 3 |
| 06A | Knocker | Switched | Vio-Blu | 1P11-7 | 8P3-6 (to B6 on Diode Sw. Bd.) | Q23 | AE-23-800-02 | — [blank] | 3 |
| 06C | Flasher 6 | Switched | Blk-Blu | (Gry-Blu) | 8P3-6 (to B6 on Diode Sw. Bd.) | Q23 | #89 flashlamps | 2p | 3 |
| 07A | Right Eject | Switched | Vio-Blk | 1P11-8 | 8P3-7 (to B7 on Diode Sw. Bd.) | Q30 | AE-23-800-11 | — [blank] | 3, 4 |
| 07C | Flasher 7 | Switched | Blk-Vio | (Gry-Vio) | 8P3-7 (to B7 on Diode Sw. Bd.) | Q30 | #89 flashlamps | 2p | 3 |
| 08A | Spare (Not Used) | Switched | Vio-Gry | 1P11-9 | 8P3-8 (to B8 on Diode Sw. Bd.) | Q22 | — [blank] | — [blank] | 3 |
| 08C | Flasher 8 | Switched | Blk-Gry | (Gry-Blk) | 8P3-8 (to B8 on Diode Sw. Bd.) | Q22 | #89 flashlamps | 3p | 3 |
| 09 | Flasher 9 | Controlled | Brn-Blk | 1P12-1 | 8P3-9 | Q17 | #89 flashlamps | 2b, 1p | — |
| 10 | Center Left Eject | Controlled | Brn-Red | 1P12-2 | 8P3-10 | Q9 | AE-23-800-11 | — [blank] | 4 |
| 11 | General Illumination Relay | Controlled | Brn-Orn | 1P12-4 | 3P7-1 | Q16 | 5580-09555-01 | — [blank] | 5 |
| 12 | Line Of Death Kickback | Controlled | Brn-Yel | 1P12-5 | 8P3-12 | Q8 | AE-23-800-11 | — [blank] | 4 |
| 13 | Rescue Kickback (left outlane) | Controlled | Brn-Grn | 1P12-6 | 8P3-13 | Q15 | AE-23-800-11 | — [blank] | 4 |
| 14 | Solenoid A/C Select Relay | Controlled | Brn-Blu | 1P12-7 | 8P3-14 | Q7 | 5580-09555-01 | — [blank] | 4 |
| 15 | Flasher 10 | Controlled | Brn-Vio | 1P12-8 | 8P3-15 | Q14 | #89 flashlamps | 2b, 1p | — |
| 16 | Rotating Beacons (backbox) | Controlled | Brn-Gry | 1P12-9 | 8P3-16 | Q6 | #1683 & mtr14-7946 | — [blank] | 4 |
| 17 | Left Kicker | Special #1 | Blu-Brn | 1P19-7 | 8P3-17 | Q75 | AE-23-800-03 | — [blank] | — |
| 18 | Right Kicker | Special #2 | Blu-Red | 1P19-4 | 8P3-18 | Q71 | AE-23-800-03 | — [blank] | — |
| 19 | Spare (Not Used) | Special #3 | Blu-Orn | 1P19-3 | 8P3-19 | Q73 | — [blank] | — [blank] | — |
| 20 | Jet Bumper | Special #4 | Blu-Yel | 1P19-6 | 8P3-20 | Q69 | AE-23-800-03 | — [blank] | — |
| 21 | Upper Diverter - Launch Ramp | Special #5 | Blu-Grn | 1P19-8 | 8P3-21 | Q77 | AE-26-1500-02 | — [blank] | — |
| 22 | Lower Diverter - Launch Ramp | Special #6 | Blu-Blk | 1P19-9 | 8P3-22 | Q79 | AE-26-1500-02 | — [blank] | — |
| - | Upper Right Flipper | - | [Blk-Yel] | — [blank] | [7P1-14, 8P3-33] | - | FL11630-50VDC | — [blank] | — |
| - | Right Flipper | - | Orn-Vio; [Blu-Vio] | 1P19-1 | 7P1-15; [7P1-16,8P3-34]² | - | FL11630-50VDC | — [blank] | 2 |
| - | Upper Left Flipper | - | [Blk-Blu] | — [blank] | [7P1-17, 8P3-31] | - | FL11630-50VDC | — [blank] | — |
| - | Left Flipper | - | Orn-Gry; [Blu-Gry] | 1P19-2 | 7P1-18; [7P1-19,8P3-32]² | - | FL11630-50VDC | — [blank] | 2 |

Notes (printed):

1. Wire colors, except flipper Orn-Vio and Orn-Gry, are ground connections (to coil terminal with unbanded end of diode). Flipper Orn-Vio and Orn-Gry wires connect from CPU Board to flipper switch.
2. Flipper connections shown in braces are from flipper switch to flipper coil.
3. "A" coils are pulsed, when Sol. 12 is de-energized; "C" coils are pulsed, with Sol. 12 energized. Wire colors in brackets are those from respective A and C terminals corresponding to the B terminal connection listed for the Diode Switching Board, which controls the device pulsing by Sol. 12.
4. Relay (p/n 5580-09555-01) is mounted on Relay Snubber Bd. p/n C-11232 or C-11232-2, or Relay Bd. p/n C-11232-1.
5. Relay is mounted on Power Supply Bd. D-8345 in the backbox.
