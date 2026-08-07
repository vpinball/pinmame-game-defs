# Star Trek: The Next Generation — Opto and proximity-sensor board assemblies

Transcribed from `Star_Trek_TNG_OPS.pdf`, printed pages 3-14/3-15 (Flipper Opto PCB / LED & Photo
Transistor PCB, PDF 112-113), 3-20/3-21/3-22 (Proximity Sensor II, Eddy Sensor, Motor EMI, PDF
118-120), and 3-26/3-27 (16-Opto PCB Assembly A-16998, PDF 124-125) — the board/assembly pages that
fix construction for the switches identified as opto or eddy-sensor devices. This scan carries a
searchable OCR text layer, but it was visually confirmed against the rendered pages.

## Flipper Opto PCB / LED & Photo Transistor PCB (printed 3-14/3-15)

`A-17316 Flipper Opto PCB Assembly` (F2/F4/F6, the three fitted cabinet flipper-button optos).
`A-16908 LED PCB Assembly` (green board) / `A-16909 Photo Transistor PCB Assembly` (blue board) — the
generic small opto pair used throughout the 16-Opto PCB (switches 31-38, 41-48) and the Borg Bracket
Assembly (switch 31).

## 16-Opto PCB Assembly, A-16998 (printed 3-26/3-27)

Connector table confirms every column-3/column-4 opto switch's harness pin (J1/J2 → switches 41-48,
J3/J4 → switches 31-38) and the shared J5 CPU-board feed (row 1-8 from J209-1..9, column 3/4 from
J207-3/4, +12V and ground from Power Driver Board J118-2/J118-3). Note: "Photo Transistor assemblies
have blue boards. LED assemblies have green boards."

## Proximity Sensor II, Eddy Sensor, Motor EMI (printed 3-20/3-21/3-22)

`A-16922 Proximity Sensor II PCB Assembly` (TDA0161 eddy-current IC): Left board `J1-3` Green-Brown
"sw. col. 1 from CPU J207-1", `J1-4` White-Blue "sw. row 6 from CPU J209-7" → public switch 16
(column 1, row 6, Left Return Lane); Right board `J1-4` White-Violet "sw. row 7 from CPU J209-8" →
public switch 17 (Right Return Lane). `A-17064 Eddy Sensor Assembly` wires directly into each
Proximity Sensor II board's `J2` (Red/Black). This confirms switches 16/17 ("Left/Right Return Lane")
are eddy-current proximity sensors, not leaf switches or optos, physically — and because column 1
carries no shading on the switch matrix and PinMAME's `invSw[1]` is `0x00`, there is no polarity
conflict to record.

`A-15542 Motor EMI PCB Assembly` (one per gun): suppresses motor noise between the Power Driver
Board and each U-Gun Motor Bracket Assembly (`A-17220-L`/`A-17220-R`).
