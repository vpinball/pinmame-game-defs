# Dedicated Switches (D-1 - D-24) and CPU/Sound Bd. SW1 DIP Switch (1-8)

Transcribed from `Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf`,
PDF page 6, printed "DR. 4", the two blocks below the Switch Matrix Grid on the same page.
Headers read `Dedicated Switches (D-1 - D-24) {Ded. Sw. Locations on the next page}` and
`CPU/SOUND BD. SW1 DIP SWITCH (located between Connectors J3/J13)`.

The whole region is transcribed, including every `NOT USED` row.

## D-1 - D-8 (CPU/SND Board IC-U02, PNK-xxx, J2)

| Switch | Wire | Connector | Annotation | Label | Part number | Location |
| --- | --- | --- | --- | --- | --- | --- |
| SW. D-1 | PNK-BRN | J2-P2 | | LEFT COIN SLOT | 180-5204-00 | Coin Door |
| SW. D-2 | PNK-RED | J2-P3 | | CENTER COIN SLOT/DBA | 180-5204-00 | Coin Door |
| SW. D-3 | PNK-ORG | J2-P4 | | RIGHT COIN SLOT | 180-5204-00 | Coin Door |
| SW. D-4 | PNK-YEL | J2-P6 | | FOURTH COIN SLOT | 180-5204-00 | Coin Door |
| SW. D-5 | PNK-GRN | J2-P7 | IF USED | FIFTH COIN SLOT | | |
| SW. D-6 | PNK-BLU | J2-P8 | | NOT USED | | |
| SW. D-7 | PNK-VIO | J2-P9 | | L. POST SAVE (UK ONLY) | 180-5160-01 | Cabinet Side |
| SW. D-8 | PNK-GRY | J2-P10 | | R. POST SAVE (UK ONLY) | 180-5160-01 | Cabinet Side |

## D-9 - D-16 (CPU/SND Board IC-U04, GRY-xxx, J3)

| Switch | Wire | Connector | Label | Part number | Location |
| --- | --- | --- | --- | --- | --- |
| SW. D-9 | GRY-BRN | J3-P1 | LEFT FLIPPER BUTTON | 180-5160-01 | Cabinet Side |
| SW. D-10 | GRY-RED | J3-P2 | LEFT FLIPPER E.O.S. | 180-5149-00 | Flipper Asm. |
| SW. D-11 | GRY-ORG | J3-P4 | R. FLIPPER BUTTON | 180-5160-01 | Cabinet Side |
| SW. D-12 | GRY-YEL | J3-P5 | RIGHT FLIPPER E.O.S. | 180-5149-00 | Flipper Asm. |
| SW. D-13 | GRY-GRN | J3-P6 | NOT USED | | |
| SW. D-14 | GRY-BLU | J3-P7 | NOT USED | | |
| SW. D-15 | GRY-VIO | J3-P8 | NOT USED | | |
| SW. D-16 | GRY-BLK | J3-P9 | NOT USED | | |

## D-17 - D-24 (CPU/SND Board IC-41, LGN-xxx, J13)

| Switch | Wire | Connector | Annotation | Label | Part number / note |
| --- | --- | --- | --- | --- | --- |
| SW. D-17 | LGN-BRN | J13-P1 | | TILT PENDULUM (PLUMB BOB) | *See Sec. 4, Chp. 1, Pg. 47 for cab. parts* |
| SW. D-18 | LGN-RED | J13-P3 | OPTIONAL | SLAM TILT | 502-5032-00 Optional Kit |
| SW. D-19 | LGN-ORG | J13-P4 | IF USED | TICKET NOTCH | 180-5119-02 Below P/F |
| SW. D-20 | LGN-YEL | J13-P5 | | NOT USED | |
| SW. D-21 | LGN-BLK | J13-P6 | | BACK (GREEN BUTTON) | 180-5192-04 Coin Door |
| SW. D-22 | LGN-BLU | J13-P7 | | MINUS (< / - RED BUTTON) | 180-5192-02 Coin Door |
| SW. D-23 | LGN-VIO | J13-P8 | | PLUS (+ / > RED BUTTON) | 180-5192-02 Coin Door |
| SW. D-24 | LGN-GRY | J13-P9 | | SELECT (BLACK BUTTON) | 180-5192-00 Coin Door |

## D-25 - D-32: CPU/Sound Bd. SW1 DIP Switch (1-8)

The same page continues the dedicated-switch numbering into the CPU/Sound board's own SW1
DIP bank. Every cell reads identically apart from the position number:

| Switch | Label | Setting |
| --- | --- | --- |
| SW. D-25 | DIP SWITCH POSITION #1 | ON / OFF |
| SW. D-26 | DIP SWITCH POSITION #2 | ON / OFF |
| SW. D-27 | DIP SWITCH POSITION #3 | ON / OFF |
| SW. D-28 | DIP SWITCH POSITION #4 | ON / OFF |
| SW. D-29 | DIP SWITCH POSITION #5 | ON / OFF |
| SW. D-30 | DIP SWITCH POSITION #6 | ON / OFF |
| SW. D-31 | DIP SWITCH POSITION #7 | ON / OFF |
| SW. D-32 | DIP SWITCH POSITION #8 | ON / OFF |

## Ground rows printed alongside the same blocks

| Board | Wire | Connector |
| --- | --- | --- |
| CPU/SND Board | GROUND (BLK) | J2-P1/11 & J3-P10 |
| CPU/SND Board | GROUND (BLK) | J13-P10 |

## Wire colour abbreviations printed on the same page

`BLK Black`, `BLU Blue`, `BRN Brown`, `GRY Gray`, `GRN Green`, `LGN Light Grn.`,
`ORG Orange`, `PNK Pink`, `RED Red`, `TAN Tan`, `VIO Violet`, `WHT White`, `YEL Yellow`.

## Notes on this page's own conventions

- The `Dedicated Switch Schematic` inset on the following page shows
  `Dedicated Switch Inputs (G??-XXX)` and `Ground (BLACK)` with `N.O.` and `COM.` terminals
  labelled `Normally Open Switch` and `Common`. No individual dedicated switch is
  identified as normally closed anywhere on either page.
- The manual's own D-numbering runs 1-32 and covers the eight DIP positions as D-25 to
  D-32; it is a board-input numbering, not a PinMAME public switch address.
