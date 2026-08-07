# Cactus Canyon — Opto Theory and Opto Board Assemblies

Transcribed from `Cactus_Canyon_Manual.pdf`, PDF page 55 (printed 1-45, "Opto Theory") and PDF pages
68-71 (printed 2-10 through 2-13, board and assembly parts pages that fix device construction). The
retained PDF carries an OCR text layer, but it is garbled on dense tabular pages, so this is
confirmed against the rendered pages, which are the source of record. This is the primary
opto-identification source for the machine, used together with the two cues (matrix shading and
parts-list construction) checked in `switch-locations.md` and `switch-matrix.md`.

## Opto Theory (printed 1-45)

"The opto receiver (Photo Transistor) should be approximately 0.1-0.7 volts when the opto beam is
unblocked and approximately 11-13 volts when the opto beam is blocked. The opto transmitter (LED)
should always be approximately 1.4 volts." Confirms the general LED/phototransistor interrupter
theory; it does not itself state which printed switch addresses are opto.

## Opto board assemblies (printed 2-10 through 2-13) — definitive opto inventory

| Assembly | Title | Channels | Switches served |
| --- | --- | --- | --- |
| A-18617-1 / A-18618-1 | Trough IR LED PCB / Trough IR Photo Transistor PCB | 5 (LED1-5 / Q1-Q5) | Trough optos (feeds the 10-Opto board below) |
| A-22407 | Train Single Opto | 1 (single Schmitt-integrated opto, IC Opto Integ Schmitt) | 71 Train Encoder |
| A-17316 | Flipper Opto PCB Assembly | 2 (OPTO1, OPTO2, "Interrupter Flip-Opto") | 112 Lower Right Flipper Opto, 114 Lower Left Flipper Opto |
| A-20246 (A-18159.1) | 10-Opto PCB Assembly w/Bracket | 10 positions (LM339 quad comparators U1-U3) | 31-35 (trough), 36-37 (loop bottoms), 41-42 (poppers) = 9 used, 1 spare |
| A-22443 | Mine Dual Opto PCB | 2 (U1, U2, IC Opto Integ Schmitt) | 77 Mine Home, 78 Mine Encoder |

Printed page content behind each row: 2-10 (PDF 68) carries A-18617-1 Trough IR LED PCB / A-18618-1
Trough IR Photo Transistor PCB / A-22407 Train Single Opto; 2-11 (PDF 69) carries A-20580 Coin
Interface PCB / A-17316 Flipper Opto PCB Assembly; 2-12 (PDF 70) carries A-20246 10-Opto PCB Assembly
w/Bracket / A-16120 D.C. Motor Control Board; 2-13 (PDF 71) carries 04-12330 Motor EMI w/Brake &
Resistors / A-22443 Mine Dual Opto PCB.
