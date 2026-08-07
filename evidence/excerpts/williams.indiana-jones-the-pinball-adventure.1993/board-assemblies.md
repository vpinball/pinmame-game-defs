# Indiana Jones — Board Identification (custom switch column and custom solenoids)

Transcribed from `Indiana_Jones_OPS.pdf`, PDF pages 136, 138-139, and 140, printed pages 3-20
(3-sw. Opto PCB Assembly for idol), 3-22/3-23 (8-Driver PCB Assembly/Schematic), and 3-24 (Motor Opto
Switch PCB Assembly for mini playfield) — the board/PCB identification pages that fix the custom
switch-column and custom-solenoid physical construction. Read from the rendered pages, not the OCR
text stream, which is scrambled on this scan.

- `A-13901-2`, "3-sw. Opto PCB Assembly (for idol)": three onboard opto pairs (`OPTO1/OPTO2/OPTO3`)
  feed Wheel Position 1/2/3 (printed 91/92/93, public 121/122/123) from CPU board rows 1-3 through
  switch column 9.
- `A-16657`, "Motor Opto Switch PCB Assembly (for mini playfield)": two onboard opto pairs feed Mini
  Playfield Right/Left Limit (printed 94/95, public 124/125 — see `switch-locations.md`'s Left/Right
  resolution) from CPU board rows 4-5 through the same switch column 9, and separately switches the
  mini-playfield tilt motor via the Bridge Driver Board on solenoids 22/23.
- `A-16100`, "8-Driver PCB Schematic": a `74ALS576` octal latch addressed at `3FEB`
  (`WPC_EXTBOARD1`) drives solenoids labelled `SOL.1`-`SOL.8` on this board — the physical
  realization of the public custom-solenoid range 51-58 documented in `solenoid-flasher-wiring.md`.
