# Revenge From Mars switch-contact polarity

Source: *Revenge From Mars Operations Manual*, February 1999, model 50070. Transcribed from PDF pages 37-38 (printed pages 1-27 through 1-28) and PDF page 87 (printed page 2-47), then visually checked against the rendered pages.

## Playfield and flipper contacts

Printed page 1-27 states: “Adjust the switch contacts to a 1/16-inch gap.” This establishes an open-at-rest gap for the blade contacts covered by that maintenance instruction.

Printed page 1-28 states: “The End-of-Stroke switches are NORMALLY OPEN. The switch should close when the flipper is energized.”

## Opto exceptions

The switch-matrix legend on printed page 2-47 states “=OPTO, TYPICALLY CLOSED.” Visual review found shading on exactly these stock positions: Trough Jam (41), Trough Ball 1-4 (42-45), Right Popper (46), Jet Exit (47), Right Lockup 1 (51), and Left Ramp Entrance (52). No other matrix cell is shaded.

## Direct grounded inputs

The same switch page presents the coin, diagnostic, end-of-stroke, and cabinet controls as dedicated inputs that close to their printed black ground returns. It identifies the lower-right and lower-left end-of-stroke inputs as D13-D14 and the cabinet inputs as D17-D24. These are active-high public inputs in the pinned P2K implementation; they are not part of the active-low per-game opto list.
