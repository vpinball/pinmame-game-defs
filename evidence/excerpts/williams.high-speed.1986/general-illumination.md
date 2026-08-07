# High Speed — General illumination relay and lamp-string distribution

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 81 (printed page 47, Section 3), the
**Power Wiring Diagram**, read from 200 dpi and 400 dpi `pdftoppm` renders. The accompanying crop is
the POWER SUPPLY box's lower-right corner plus the 3P8 fan-out, because the fact here is a drawing —
which lamp strings the relay contacts sit in series with — and prose alone cannot carry it faithfully.

This page is the only source in the manual that says where High Speed's general illumination actually
goes. It is transcribed because two other sources restrict the GI to a smaller scope than it has:
pinned PinMAME's own per-game comment calls solenoid 11 a "Backbox GI output", and the retained
known-working VPX table's `PFGI` handler drives a playfield-only light collection.

## What the diagram shows, traced connection by connection

Inside the box labelled `POWER SUPPLY` (part `D-8345-541`, added by the Amendments sheet), at its lower
centre-right:

- Two **relay contact** symbols are drawn in series with two horizontal supply lines entering the box
  from the left. The Amendments sheet, Amendment Page 1, printed page 47 item (g), says of exactly this
  spot: *"Add the words, Relay Contacts, near the two sets of contacts in the lower center of the box
  labelled POWER SUPPLY box."* The relay itself is item 11 of the Solenoids/Flashers parts list,
  described there as `Pwr Sup Bd Relay` and in the Solenoid Table as `5580-09555-00`, driven from CPU
  connector 1P12-4 through Q16 with the Brn-Orn wire to 3P7-1.
- Both contacted lines run right into connector `3J6` and out through `3P8`. At this scan quality the
  two contacts cannot be attributed to individual `3J6` pins with certainty; what the drawing does show
  unambiguously is that they sit between the transformer secondary entering the box and the `3J6`/`3P8`
  pin groups below, i.e. upstream of every pin listed next.
- `3P8` pins **1, 2, 3, 4** carry `BRN`, `YEL`, `GRN`, `VIO`. The four pins are bracketed together on
  the 3J6 side with junction dots, i.e. they are one common leg split four ways.
- `3P8` pins **6, 7, 8, 9** carry `WHT-BRN`, `WHT-YEL`, `WHT-GRN`, `WHT-VIO`, each through its own fuse,
  annotated `ALL 5ASB`. These four pins are likewise bracketed together on the 3J6 side.
- From 3P8 the eight lines fan out to three destinations, each lamp string drawn as a row of bulb
  symbols wired across one pin from the 1-4 group and one pin from the 6-9 group:
  - `9P2` / `9J2` pins 1-4 — the backbox **Insert Board** (board 9), two rows of bulbs.
  - `7P6` / `7J6` pins 2-3 into `7P4` / `7J4` pins 1-2 — the **cabinet** (board 7), one row of bulbs,
    carrying the `YEL` and `WHT-YEL` pair.
  - `P/O 8P4` / `8J4` pins 3, 4, 5, 6 — the **playfield** (board 8), two rows of bulbs, carrying the
    `VIO` and `WHT-VIO` pairs.

Each lamp row is drawn across one pin from the 1-4 group and one pin from the 6-9 group, and both
groups sit downstream of the contacts, so every GI string has at least one switched leg. The strings
land on the playfield, in the cabinet, and on the backbox insert board. **Solenoid 11 switches the
whole game's general illumination, not the backbox alone.**

## What the diagram does not show

The bulb rows are drawn with three bulb symbols each and a dashed continuation, so the diagram states
neither the bulb count per string nor any bulb position. No page of this manual carries a GI bulb
inventory, a GI bulb type, or a GI location drawing. That is why this definition records solenoid 11 as
a playfield-and-backbox-and-cabinet GI device but omits its spatial record rather than adopting the
retained table's 68-object playfield `GI` light collection as if it were the manual's own set.

## Cross-reference: All Lamps Test text, printed page 23 (PDF page 31), verbatim

> …and that all feature lamps (playfield and backbox) blink on and off. (Note, however, that the
> General Illumination lamps remain lighted steadily.)

This distinguishes the strobed feature-lamp matrix from the relay-switched GI without restricting the
GI to either the playfield or the backbox, and so is consistent with the wiring above.

## Amendments affecting the GI circuit

From Amendment Page 1, printed page 50 item (c), concerning the `D-8345-541` Power Supply diagram:

> …terminal 1 of GEN. ILLUM. should have YEL-WHT as the wire color…

and from printed page 46:

> Change voltage from 6.3 to 5.9 VAC at input to 3J8.

The general illumination is therefore a nominal 6.3 VAC supply (5.9 VAC measured at the board input),
which is the ordinary `#44`/`#47` bayonet GI voltage for this era. The manual never states the GI bulb
type by number.
