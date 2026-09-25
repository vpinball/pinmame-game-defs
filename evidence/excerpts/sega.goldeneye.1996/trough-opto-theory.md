# Sega GoldenEye (1996) — Trough Up-Kicker OPTO Theory of Operation & Schematic

Source: Sega Pinball *GoldenEye* operations manual (`Sega_1996_Goldeneye_Manual.pdf`), PDF page 88,
printed page 94 (Section 5, Chapter 2, Playfield Wiring), **Trough Up-Kicker OPTO — Theory of
Operation & Schematic**. Read from the native 300 dpi render. The schematic is a drawing, so the crop is
the evidence for it; the transcription records the labels and the operative text.

## Theory of Operation (paraphrased; operative terms quoted)

Light from the transmitter falling on the receiver LED biases the gate of Q1 off; with Q1 off no base
current flows in Q2, which acts as an "OPEN SWITCH". When the light is interrupted ("BLOCKED"), R1 bleeds
the gate voltage off Q1, Q1 conducts and switches Q2 on, which acts as a "CLOSED SWITCH".

## Fig. 1 labels

- Transmitter board `520-5124-00`: `+5v` pin 2, `GND` pin 1, `LED MT5000UR (See Note)`, `R1 180`.
- Receiver board `520-5125-00`: `LED MT5000UR`, `R1 1M`, `R2 5.6K`, `R3 10K`, `Q1 2N5460` (gate G,
  drain D, source S), `Q2 2N3906`, test points `A` and `B`; pin 1 `SWITCH ROW / RETURN WHT/XXX WIRE`, pin 2
  `SWITCH COL / DRIVE GRN/XXX WIRE`.
- Legend: double arrow `= Light`. Note: "The RADIO SHACK part number for the LED MT5000UR is 276-087."

## Troubleshooting (The following tests indicate normal operating conditions)

1. Volt Meter Test:
   - A. `OPEN OPTO (Light Falling on LED) = SWITCH OPEN.` Meter across points A and B reads approximately
     0.8 - 1.2v DC.
   - B. `CLOSED OPTO (Light Blocked) = SWITCH CLOSED.` Meter across points A and B reads approximately
     0.0 - 0.1v DC.

The next page (PDF 89, printed 95) repeats the rule for the oscilloscope and bench tests, and PDF 90
(printed 96, Single Trough OPTO Alignment/Test) says that in Switch Test mode lifting the trough plunger
with a fingertip should block the beam and trigger the switch position.
