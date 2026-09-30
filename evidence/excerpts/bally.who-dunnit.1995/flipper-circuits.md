# WHO dunnit lower-flipper windings and inputs

Source: Bally *WHO dunnit* manual, PDF pages 98–99 (printed 2-16–2-17) assembly parts, PDF page 126 (printed 2-44) input matrix, PDF page 128 (printed 2-46) circuit table, PDF page 129 (printed 2-47) fitted assembly list, duplicate PDF page 137 (printed 3-5), and PDF page 157 (printed 3-25) Fliptronic II A-15472-1 connector schematic. Independently read from the original embedded rasters at native dimensions on 2026-09-30. Manual circuit numbers are **not** PinMAME public output numbers.

| Side / winding | Manual circuit | Public output | PDF 128 coil | PDF 137 coil | PDF 129 assembly | Power feed | Driver | Return | Return wire |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| Lower right power | 29 | 45 | FL-15411 | FL-11541 | A-14876-R-5 | J907-1 Red-Grn | Q4 | J902-13 | Yel-Grn |
| Lower right hold | 30 | 46 | FL-15411 | FL-11541 | A-14876-R-5 | J907-1 Red-Grn | Q11 | J902-11 | Org-Grn |
| Lower left power | 31 | 47 | FL-15411 | FL-11541 | A-15849-L-4 | J907-4 Red-Blu | Q3 | J902-9 | Yel-Blu |
| Lower left hold | 32 | 48 | FL-15411 | FL-11541 | A-15849-L-4 | J907-4 Red-Blu | Q9 | J902-7 | Org-Blu |
| Upper right power | 33 | unused physical winding | NOT USED | NOT USED | not listed | J907-6 Red-Vio | Q2 | J902-6 | Yel-Vio |
| Upper right hold | 34 | unused physical winding | NOT USED | NOT USED | not listed | J907-6 Red-Vio | Q7 | J902-4 | Org-Vio |
| Upper left power | 35 | unused physical winding | SEE | SEE | not listed | J907-8 Red-Gry | Q1 | J902-3 | Yel-Gry |
| Upper left hold | 36 | 36, repurposed Up Down Post | SEE | SEE | A-17932, post | J907-8 Red-Gry | Q5 | J902-1 | Org-Gry |

The table transcribes both original circuit regions, including unused/repurposed rows. PDF 157 supplies +50 V for the lower-flipper feeds. Both circuit pages print ORANGE for the lower coils, NOT USED for the upper right and ABOVE in the upper-left Coil Color column; SEE/ABOVE spans the two columns. PDF 128/129 and the assembly tables below print FL-15411, whereas PDF 137 prints FL-11541. This is `conflict.lower-flipper-coil-part`, within one document family. The assembly readings corroborate FL-15411 but do not explicitly correct PDF 137; no fitted coil part number is selected. Resolution requires an applicable factory correction or documented original coil/assembly inspection. Winding wiring and ROM-facing remaps are separately supported.

## Complete assembly parts regions

Native PDF 98 A-14876-R-5 and PDF 99 A-15849-L-4 list the following parts, compacted where the two sides share identical descriptions. `not listed` means no part cell is printed in that page's table; it does not assert absent hardware. Subitems belong to the preceding numbered assembly.

| Item | PDF 98 right part | PDF 99 left part | Printed description |
| --- | --- | --- | --- |
| 1 | A-14877-R | B-13104-L | Flipper Base Assembly, Right / Left |
| 2 | SW-1A-194 | SW-1A-194 | Switch Assembly |
| 3 | 4701-00002-00 | 4701-00002-00 | Lockwasher #6 Split |
| 4 | 4105-0119-10 | 4105-0119-10 | Sht. Metal Screw, #5 x 5/8 inch |
| 5 | 4008-01079-05 | 4008-01079-05 | Mach. Screw, 8-32 x 5/16 inch |
| 6 | 4701-00003-00 | 4701-00003-00 | Lockwasher #8 Split |
| 7 | 01-9375 | 01-9375 | Switch Mounting Bracket |
| 8 | 20-6516 | 20-6516 | Speednut, Tinnerman |
| 9 | 4010-01066-06 | 4010-01066-06 | Cap Screw, 10-32 x 3/8 inch |
| 10 | 4701-00004-00 | 4701-00004-00 | Lockwasher #10 Split |
| 11 | A-12390 | A-12360 | Flipper Stop Assembly |
| 12 | FL-15411 | FL-15411 | Flipper Coil, Orange |
| 12a | not listed | 03-7066-5 | Coil Tubing |
| 13 | 01-7695 | 01-7695-1 | Solenoid Bracket |
| 14 | 4006-01017-04 | 4006-01017-04 | Mach. Screw, 6-32 x 1/4 inch |
| 15 | 10-364 | 10-364 | Spring |
| 16 | 4006-01005-06 | 4006-01005-06 | Mach. Screw, 6-32 x 3/8 inch |
| 17 | 4406-01117-00 | 4406-01117-00 | Nut 6-32 Hex. |
| 18 | A-15848-R | A-15848-L | Crank Link Assembly, Right / Left |
| 18a | A-17050-R | A-17050-L | Flipper Crank Assembly, Right / Left |
| 18b | A-15847 | A-15847 | Flipper Link Assembly |
| 18c | 02-4676 | 02-4676 | Link Spacer Bushing |
| 18d | 4010-01086-14 | 4010-01086-14 | Cap Screw, 10-32 x 7/8 inch |
| 18e | 4700-00023-00 | 4700-00023-00 | Flat Washer, 5/8 x 13/64 x 16ga. |
| 18f | 4701-00004-00 | 4701-00004-00 | Lockwasher #10 Split |
| 18g | 4401-01132-00 | 4401-01132-00 | Nut 10-32 ESN |
| 19 | 23-6577 | 23-6577 | Bumper Plug, 5/8 inch |
| 20 | 03-7568 | 03-7568 | Flipper Bushing |
| 21, associated | 23-6519-4 | 23-6519-4 | Flipper Rubber Ring, Red |
| 22, associated | 20-10110-5 | 20-10110-5 | Flipper Bat w/Shaft (PDF 99 adds White) |

## Input connector and runtime scope

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
