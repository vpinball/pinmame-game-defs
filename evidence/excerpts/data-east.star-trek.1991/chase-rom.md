# Star Trek chase-light firmware and board evidence

Seven 65,536-byte CPU images were checked by `tools/verify_star_trek_chase.py` (SHA-256 `dc0daeceda23e5b24d474fe5305935b4adf3d565a5c58d8cc3dbdef72ffcdf89`). The source images stay outside Git. Images 110–201 are the sole CPU-named members of the corresponding authorized `trek_NNN.zip` archives; 300 and 301 are the retained patched `trekcpuu.300` and `trekcpuu.301` images in `review-artifacts/data-east-star-trek-1991/followup/`. All image SHA-1s match the respective definitions in pinned PinMAME `src/wpc/degames.c` revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. The verifier refuses a missing or ambiguous archive member, wrong image length or hash, changed dispatch/routine, invalid pointer, changed pattern, or changed extended-store context. Its derived output is retained as `followup/chase-verification.json` (SHA-256 `c529f2389cd95523622d77685ddab11feff227463e83b2fdd17f4051c283448d`). No ROM bytes are included in the output or this excerpt. CPU addresses below equal offsets within these 64 KiB images; only offsets at or above `4000` are searched.

| Revision | CPU image SHA-1 | Pattern routine | Pointer table |
| --- | --- | --- | --- |
| 110 | `989d70e067cd322351768550549a4e2c8923132c` | B953 | B970 |
| 117 | `96f343fcc7b0f39e0a8ec7df47cea433ad2c9119` | B9C5 | B9E2 |
| 120 | `abf68c358c50bdeb36714cca0a9848e398a6f9fc` | BC2F | BC4C |
| 200 | `0ebb16ab8b95f04a19fa4510e58c01493393d48c` | BCF2 | BD0F |
| 201 | `282c8181e60da6358ef320358575a538aa4abe8c` | BD2A | BD47 |
| 300 | `a453208a7640a39cb96947e8d3d3b2f71f85e613` | BD2A | BD47 |
| 301 | `f8dd222b5237cf4bd8bc00f32980d68d339032f9` | BD2A | BD47 |

The checked dispatch loads the pointer-table base, loads the selector from `$108F`, doubles it, calls a revision-specific helper, and loads an indexed pointer. The routine loads a count, advances, loads a pattern value, complements it, tests `$1091`, and conditionally stores the complemented value at `$2802`. Each table has eight big-endian pointers to a count followed by `(logical mask, delay)` pairs. Every image yields the same eight lists:

| Index | Logical masks | Delays |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 4, 2, 1 | 1, 1, 1 |
| 2 | 7, 0 | 1, 1 |
| 3 | 5, 2 | 1, 1 |
| 4 | 0, 1, 2, 3, 4, 5, 6, 7 | 1, 1, 1, 1, 1, 1, 1, 1 |
| 5 | 7, 0, 7, 0, 7, 0 | 4, 1, 2, 1, 2, 1 |
| 6 | 1, 2, 4, 4, 2, 1 | 1, 1, 1, 1, 1, 1 |
| 7 | 1, 2, 4 | 1, 1, 1 |

The maximum logical pattern mask is 7. The values are logical bits before the firmware's complement; delay units are not established here.

For each image, a raw scan for extended stores to `$2802` finds eleven potential sites. Their instruction contexts comprise three initialization B stores, five fixed `FF` A stores, one fixed `F8` A store, one indexed service-test A store, and the conditional pattern store. The service-test data sequence is `FE`, `FD`, `FB`, `FF`; the boot sequence writes `FF` to the direction register and then to the output latch. These facts support use of three low bits by the identified animation and service paths. **The raw scan is not a universal control-flow or indirect-address analysis**: a byte sequence may occur in data, and a computed or different addressing mode can be missed. It does not prove every possible program behavior.

The factory operations manual, PDF page 70, printed page 66, schematic 520-5054-00 revision A, shows the Light Chaser Board receiving IN 1, IN 2 and IN 3 at CN1 pins 5, 6 and 7. CN1 pins 1 and 3 are GND, pin 2 is KEY, pin 4 is +5V. Six outputs are paired: CN2 pin 7 OUT 1A, 6 OUT 1B, 4 OUT 2A, 3 OUT 2B, 2 OUT 3A, and 1 OUT 3B; CN2 pin 5 is KEY. The schematic draws one inverter and two driver channels per input. This establishes three board inputs, not six independently controlled channels or a bulb count. PinMAME's `s11.c` names generic printer CN3 outputs, a separate connector from the chaser board's CN1/CN2.

At the pinned PinMAME revision, `6821pia.c` resets the PIA through zeroed configuration and invokes the B output callback when the DDR changes, supplying the output latch masked by the DDR. `s11.c` inverts that output for `GEN_DEDMD16` printer-line games and publishes its bits as extended outputs. Setting the DDR while the latch is still zero can therefore briefly publish ones, including public outputs 40–44, before the subsequent `FF` latch write; this reset transient is not proof of five extra physical chase channels or game animation. The board schematic and identified three-bit firmware patterns provide the hardware and normal-path evidence; the scan's stated limits still apply.
