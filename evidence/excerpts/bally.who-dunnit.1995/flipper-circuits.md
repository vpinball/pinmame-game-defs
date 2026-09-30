# WHO dunnit lower-flipper windings and inputs

Source: Bally *WHO dunnit* manual, PDF page 126 (printed 2-44) input matrix, PDF page 128 (printed 2-46) circuit table, PDF page 129 (printed 2-47) fitted assembly list, and PDF page 157 (printed 3-25) Fliptronic II A-15472-1 connector schematic. Independently read at native resolution on 2026-09-30. Manual circuit numbers are **not** PinMAME public output numbers.

| Side / winding | Manual circuit | Public output | Coil | Assembly | Power feed | Driver | Return | Return wire |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| Lower right power | 29 | 45 | FL-15411 | A-14876-R-5 | J907-1 Red-Grn +50 V | Q4 | J902-13 | Yel-Grn |
| Lower right hold | 30 | 46 | FL-15411 | A-14876-R-5 | J907-1 Red-Grn +50 V | Q11 | J902-11 | Org-Grn |
| Lower left power | 31 | 47 | FL-15411 | A-15849-L-4 | J907-4 Red-Blu +50 V | Q3 | J902-9 | Yel-Blu |
| Lower left hold | 32 | 48 | FL-15411 | A-15849-L-4 | J907-4 Red-Blu +50 V | Q9 | J902-7 | Org-Blu |

The same schematic labels J906-1 lower-right E.O.S. and J906-3 lower-left E.O.S., with J906-6 switch ground. These are F1/public 111 and F3/public 113. The schematic names physical E.O.S. switches but does not establish their contact construction or rest state. PinMAME's timed `FLIP_SOL` E.O.S. display is emulator synthesis, not a physical contact measurement.

The native PDF 157 J905 connector list prints **four separate input pins**, mapped to public channels through the PDF 126 F2/F4/F6/F8 matrix headers:

| Connector | PDF 157 wire and destination | Public input / matrix address | PDF 126 fitment claim |
| --- | --- | --- | --- |
| J905-1 | Black-Violet, to right flipper opto | 112 / F2 | Lower right cabinet opto A-17316 |
| J905-2 | Blue-Gray, to left flipper opto | 114 / F4 | Lower left cabinet opto A-17316; matrix wire differs as noted below |
| J905-3 | Black-Yellow, to right flipper opto | 116 / F6 | Upper right flipper opto (NOT USED), part --- |
| J905-5 | Black-Blue, to left flipper opto | 118 / F8 | Upper left flipper opto (NOT USED), part --- |

J905-4 is Key; J905-6 Orange is Switch Ground. Pins J905-3/-5 are not folded into primary channels 112/114. PDF 126 versus PDF 157 leaves auxiliary contact fitment/usage unresolved (`conflict.auxiliary-flipper-opto-fitment`). A wired-pin claim does not establish a fitted contact or upper flipper coil. Upper-left E.O.S. F7/public 117 remains Not Used; PDF 157 calls J906-5 Not Used. Upper coils are separately absent/repurposed as recorded in the circuit table.

Pinned `wd.c:359` declares `FLIP_SW(FLIP_L|FLIP_U)`. In `core.c:1699–1731`, copying lower keyboard keys into upper button bits occurs only inside `if (g_fHandleKeyboard)`; enabling keyboard handling also enables this driver's simulator. With keyboard handling disabled, button bits are retained independently from the direct switch matrix. This is emulator input synthesis, not physical contact fitment, ROM-consumption proof, or an always-mirrored physical relationship. No retained direct-input proof settles 116/118 usage or polarity.

The PDF 157 connector list explicitly prints **J905-2 Blue-Gray to left flipper opto**. The PDF 126 (2-44) F4 matrix header instead prints **Black-Gray J905-2**. The connector and left cabinet opto binding agree, but the physical wire colour is unresolved (`conflict.left-flipper-opto-wire`); neither reading is selected as a structured control wire. The same PDF 157 page identifies **Fliptronic II Board A-15472-1** and prints **J902-1 Orange-Gray Sol 36 to playfield coil**, supporting the board identity of the up/down post output.

The hash-pinned fresh `wd_12` T.1 service trace asserts public cabinet input 112 and observes 45/46, then asserts 114 and observes 47/48; it shows release transitions too. This proves the ROM-facing binding under isolated diagnostic input, not a measured flipper stroke, coil current, or physical E.O.S. transition.
