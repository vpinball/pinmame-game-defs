# WHO dunnit lower-flipper windings and inputs

Source: Bally *WHO dunnit* manual, PDF page 128 (printed 2-46) circuit table, PDF page 129 (printed 2-47) fitted assembly list, and PDF page 157 (printed 3-25) Fliptronic II A-15472-1 connector schematic. Independently read at native resolution on 2026-09-30. Manual circuit numbers are **not** PinMAME public output numbers.

| Side / winding | Manual circuit | Public output | Coil | Assembly | Power feed | Driver | Return | Return wire |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| Lower right power | 29 | 45 | FL-15411 | A-14876-R-5 | J907-1 Red-Grn +50 V | Q4 | J902-13 | Yel-Grn |
| Lower right hold | 30 | 46 | FL-15411 | A-14876-R-5 | J907-1 Red-Grn +50 V | Q11 | J902-11 | Org-Grn |
| Lower left power | 31 | 47 | FL-15411 | A-15849-L-4 | J907-4 Red-Blu +50 V | Q3 | J902-9 | Yel-Blu |
| Lower left hold | 32 | 48 | FL-15411 | A-15849-L-4 | J907-4 Red-Blu +50 V | Q9 | J902-7 | Org-Blu |

The same schematic labels J906-1 lower-right E.O.S. and J906-3 lower-left E.O.S., with J906-6 switch ground. These are F1/public 111 and F3/public 113. Cabinet opto input pairs are J905-1/J905-3 right and J905-2/J905-5 left, with J905-6 switch ground: F2/public 112 and F4/public 114. The schematic names physical E.O.S. switches but does not establish their contact construction or rest state. PinMAME's timed `FLIP_SOL` E.O.S. display is emulator synthesis, not a physical contact measurement.

The hash-pinned fresh `wd_12` T.1 service trace asserts public cabinet input 112 and observes 45/46, then asserts 114 and observes 47/48; it shows release transitions too. This proves the ROM-facing binding under isolated diagnostic input, not a measured flipper stroke, coil current, or physical E.O.S. transition.
