# Judge Dredd — General Illumination Circuit

Transcribed from `Bally_1993_Judge_Dredd_Manual.pdf`, PDF page 124, printed page 3-10, the General
Illumination Circuit schematic and its Block Diagram, read together with the GI rows already
transcribed from printed 2-44 (`solenoid-flasher-table.md`) and printed 2-45
(`solenoid-flasher-locations.md`). Produced by rendering the retained PDF at 300 dpi with `pdftoppm`
and reading the page directly.

## Circuit (printed 3-10, upper drawing)

One representative string is drawn, and it is the generic WPC arrangement rather than anything
Judge-Dredd-specific:

```
Power Driver Board
  J113 -x-> LS374 --A--> 560 ohm --+--> 2N5401 base
                                   |
                          10K ohm to VCC
       2N5401 --B--> 51 ohm --C--> opto-triac driver + triac --> J120 -x-> G.I. Lights
       J115 -x-> ground (triac cathode return)
       J115 -x-> S.B. (slo-blo fuse) --> J120 -x-> G.I. Lights (power side)
```

Printed caption: `When point "A" toggles low, then points "B" and "C" are high. This turns On the
triac and the desired General Illumination string lights.`

## Block diagram (printed 3-10, lower drawing)

```
6.3 volt secondary --> Power Driver Board (fuse) --> Playfield or Backbox, "Up to 18 bulbs."
                                                 --> Power Driver Board: Triac Drivers <- LS374 Latch
5 volt secondary  --> Zero Cross Detection Circuit (Power Driver Board) --> Microprocessor CPU Board
                                                                        --> LS374 Latch
```

The only quantitative fact this page adds is the printed bound `Up to 18 bulbs` per string, and it is
a board capability limit rather than a count for any particular string on this machine.

## What this page does not settle

The schematic is drawn for a single unnumbered representative string. It does **not** show which
latch bit or triac corresponds to printed String 1 through String 5, so it cannot be used to check
the order in which the five strings are published to a controller. The only per-string identity this
manual carries anywhere is the printed String 1-5 numbering with its wire colours and connector pins
on 2-44:

| Printed string | Wire | Playfield drive | Backbox drive | Playfield bulb | Backbox bulb |
| --- | --- | --- | --- | --- | --- |
| String 1 | Wht-Brn | J-120-7 | J-121-6 | `#44` | `#555` |
| String 2 | Wht-Org | J-120-8 | J-121-8 | `#555` | `#555` |
| String 3 | Wht-Yel | J-120-9 | J-121-7 | `#44` | `#555` |
| String 4 | Wht-Grn | J-120-10 | J-121-10 | `#555` | `#555` |
| String 5 | Wht-Vio | J-120-11 | --- | `#555` | --- |

That wire-colour column is the only handle available for checking a claim about which physical string
a given public GI address drives.
