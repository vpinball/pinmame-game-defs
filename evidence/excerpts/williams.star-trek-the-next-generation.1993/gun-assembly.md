# Star Trek: The Next Generation — Gun Assembly construction and circuit

Transcribed from `Star_Trek_TNG_OPS.pdf`, PDF page 121 (printed 3-23, Gun Circuit Diagram) and PDF
page 51 (printed 1-41, Removing the Gun Assembly). This scan carries a searchable OCR text layer, but
it was visually confirmed against the rendered pages. These two pages establish that the gun/cannon
mechanism is a single rotating assembly and settle the construction of switches 92/95/96/97.

## Gun Circuit Diagram (printed 3-23)

Left and right gun position sensing is drawn as two plain switch-contact symbols in series on the
CPU board wiring, with no LED/phototransistor symbol and no connection to the 16-Opto PCB or
Proximity Sensor II boards — confirming items 92/95/96/97 are ordinary leaf switches (matching the
Switch-Matrix un-shaded cells and the Switch-Locations single-part-number signature; three
independent sources agree, so `conflicts` records nothing here).

- Left: 8-driver Board `J5-1` (Violet-White, "sw. col. 9") + CPU `J209-2` (White-Red, "sw. row 2") →
  sw. 92, Left Gun Mark; CPU `J209-8` (White-Violet, "sw. row 7") → sw. 97, Left Gun Home.
- Right: 8-driver Board `J5-1` (Violet-White, "sw. col. 9") + CPU `J209-7` (White-Blue, "sw. row 6")
  → sw. 96, Right Gun Mark; CPU `J209-5` (White-Green, "sw. row 5") → sw. 95, Right Gun Home.
- Left Gun Kicker (sol 1) via Power Driver Board `J130-1` (Violet-Brown) / `J107-3` (+50V); Right Gun
  Kicker (sol 2) via `J130-2` (Violet-Red).
- Left/Right Gun Motor (sol 17/18) via Motor EMI Board, 8-driver Board `J1-3`
  (Black-Brown/Black-Red)/CPU `J211`, +12V from Power Driver Board `J118-2`.

## Removing the Gun Assembly (printed 1-41)

Service procedure for the Gun (cannon) mechanism: plastic gun cover → kicker bracket (4 hex screws)
→ playfield plastic → three plugs disconnect at a branch in the black tubing under the playfield →
motor bracket assembly (two switches — Home/Mark — plus the motor, unplugged from the EMI board) →
three hex screws release the U-Gun Motor Bracket Assembly. Confirms the gun/cannon is a single
rotating assembly carrying the kicker, popper, and motor+position switches together, matching the
retained script's `CannonBaseL`/`CannonBaseR` single rotating primitive.
