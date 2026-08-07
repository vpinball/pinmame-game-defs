# Judge Dredd — Dedicated Switches

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF page 117, printed page 3-3, the DEDICATED
SWITCHES wiring drawing and the DEDICATED SWITCH CIRCUIT below it. Produced by rendering the retained
PDF at 300 dpi with `pdftoppm` and reading the page directly. This page is the board-level source for
the coin-door input wiring that the Switch Matrix page on 2-42 summarises in its left-hand block.

## Wiring (CPU Board J205 -> Coin Door Interface Board J1/J3 -> switch)

| Printed | Wire | CPU J205 | CPU chip pin | Interface J1 | Interface J3 |
| --- | --- | --- | --- | --- | --- |
| D1 | Orange-Brown | 1 | U17-5 | 14 | 4 |
| D2 | Orange-Red | 2 | U17-7 | 13 | 5 |
| D3 | Orange-Black | 3 | U17-11 | 12 | 6 |
| D4 | Orange-Yellow | 4 | U17-9 | 17 | --- |
| D5 | Orange-Green | 6 | U16-9 | 11 | 7 |
| D6 | Orange-Blue | 7 | U16-11 | 10 | 8 |
| D7 | Orange-Violet | 8 | U16-7 | 9 | 9 |
| D8 | Orange-Gray | 9 | U16-5 (printed `(16-5)`) | 8 | 11 |
| — | Black (common ground) | 11 | — | 15 | 3 |

J205 pins 5 and 10 are not used. D8's chip pin is printed `(16-5)` without the `U`, transcribed
verbatim; every sibling row uses the `U16`/`U17` form.

## Function list printed beside the drawing

Coin Acceptor Switches:

- D1 Left Coin Chute
- D2 Center Coin Chute
- D3 Right Coin Chute
- D4 Forth Coin Chute (printed `Forth`, not `Fourth`)

Control Switches:

- D5 Normal Function: Service Credits / Test Function: Escape
- D6 Normal Function: Volume Down / Test Function: Down
- D7 Normal Function: Volume Up / Test Function: Up
- D8 Normal Function: Begin Test / Test Function: Enter

The drawing shows a switch symbol on J3 pins 4, 6, 7, 8, 9 and 11 only; D2 (J3-5) and D4 (no J3 pin)
have no switch symbol drawn, which is a drawing simplification of the coin-acceptor side rather than
a fitment statement — the function list names all four chutes.

## Dedicated switch circuit (lower drawing)

```
CPU Board: C --> inverter --> LM339 (+ input pulled to +5V through 10K)
           LM339 out --A--> 1K --> 1N4148 --> J205 -x- Orange-XXX --> J1 --> J3 --> switch
           switch other side --> J3-3 --> J1-15 --> J205-11 Black --> ground
           470 pF from A to ground; 1.2K pull-up to +12V
```

| Switch | A | B | C | |
| --- | --- | --- | --- | --- |
| Open | H | H | L | Off |
| Closed | L | L | H | On |

Printed explanation: `The dedicated switches operate similar to switches in the matrix except that
instead of a column circuit there is a direct tie to ground. Therefore, the column side is constantly
active (low).` and `When a switch closes the row side (dedicated input) of the circuit activates. The
"+" input to the LM339 drops below +5V causing its output to go low. Since the row circuit (dedicated
input) is tied directly to ground through the switch, the switch is considered closed by the
microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and
the row is inactive.`

These eight are ordinary normally-open contacts: closing one pulls the dedicated input low and the
board reports it closed. Nothing on this page is an opto or a normally-closed contact.
