# Catacomb physical wiring regions

Source: Stern Electronics Catacomb schematics, SHA-256 `45fd3691ca719eab243553b98967aef4fb7cbe6c1ce7340e3342ecf0a1d24294`. Method: curator visual reading of native scans; OCR used only to find pages. PDF page numbers are one-based.

## PDF 3: PLAYFIELD CATACOMB -147-

The switch drawing is a five-strobe/eight-return circuit. Strobes ST0-ST4 are A4J2 pins 1-5, with wires W-R, BRN-W, W-BLU, W-Y, Y-R. Returns I0-I7 are A4J2 pins 8-15, with BRN, GREY, W-O, W-B, W-G, W-BRN, BRN-Y, O. The coin/credit/tilt cabinet branches use the cabinet connector, as the game's switch-identification table separately shows. A drawn open contact is not a software inversion mask.

The physical general-illumination branch is labelled `A2J1-8 (W)`, `6 VAC`, `GEN. ILLUM`, `A2J1-1 (R)`, `RETURN`. Its one generic lamp symbol represents a circuit; it does not count sockets. The accompanying crop preserves the branch, rather than a source-owned whole sheet.

The coil branch explicitly fits two main flippers, right/left kickout holes, four drop-bank reset coils, three slingshots, two thumper bumpers, an outhole turnstyle, an outhole reflex and BACKBOX PLAYFIELD. The return wires are listed literally in the manual-table excerpt. The BACKBOX PLAYFIELD branch is A3J2-15 (R-W). No GI relay is drawn on this machine-specific playfield sheet.

## PDF 9: SDU-100 solenoid-driver drawing 340-432-S rev C

The momentary 74LS154 code is distinct from the printed physical transistor number. Decoding the drawn lines gives public outputs: 1 Q2 top thumper; 2 Q1 bottom thumper; 3 Q5 top sling; 4 Q6 left sling; 5 Q7 right sling; 6 Q3 knocker; 7 Q4 left kickout; 8 Q8 right kickout; 9 Q13 outhole reflex; 10 Q14 outhole turnstyle; 11 Q9 reset A; 12 Q10 reset B; 13 Q12 reset C; 14 Q11 reset D; 15 Q16 unnamed. Code 1111 is N/U and the emulator suppresses it.

Continuous outputs reach Q17, Q19, Q15, Q18 at public 17,18,19,20 respectively. Q15 operates the on-board K1 FLIPPER ENABLE RELAY. Its coil drive is an internal board circuit; no external relay-coil connector is established here. Q18 reaches J2-15 BACKBOX PLAYFIELD (R-W). The machine's own p21 manual table marks Q16, Q17 and Q19 N/U; service-test pulses on their public outputs are a diagnostic sweep, not evidence of fitted loads. The independently retained coil test displays each physical Q number as its public callback fires and confirms this entire permutation repeatedly.

The cabinet sheet p2 prints the knocker wire B-Y, whereas this SDU sheet and the manual coil table print G-B at J2-5. Both refer to the same knocker and address; preserve the wiring-detail disagreement as a note, not an unresolved machine conflict.

## PDF 1,2,10: common boards and harnesses

P1 is titled WIRING DIAGRAM FOR SOLID STATE, 12B-STD-110-2. It is generic board/harness evidence. Its A1 insert drawing shows two generic GEN ILL LAMPS branches from A2J3-11/2 and A2J3-10/1; these symbols do not prove two physical bulbs. Its connector table is not a Catacomb socket inventory.

P2 CABINET AND FRONT DOOR WIRING draws FRONT DOOR LITES between A2J2-1 (Y-B) and A2J2-5 (G-R); plural wording and one circuit symbol do not establish a quantity. Its separate door memory-clear contact connects A4J3-5 (W) to A3J2-7 (Y-R), as preserved in the [door service excerpt](door-service.md). The [MPU drawing](mpu-nmi.md) on PDF7 separately shows the on-board S33 NMI button. P2 also draws test, slam and both flipper-button circuits.

P10 transformer TA-100 drawing 340-464-S rev E labels J1 PLAYFIELD GI buses at pins 5,8 and returns at 1,2; J2 CABINET bus 1 and return 5; J3 BACK BOX buses 10,11 and returns 1,2. The secondary is labelled 7.3 VAC with F5 20 AMP. P3's game wiring literally labels its GI branch 6 VAC. These are retained readings, not a measured operating voltage. Neither sheet maps every physical socket.

## Reproduction of the crop

The original PDF is rotated 90 degrees. Its p3 raster is 2596 pixels across a rotated placed width of 1178.640015 points, giving 158.59 dpi. The Poppler helper's integer argument is 159 dpi, derived from that raster, not a fixed assumed resolution. Command: `tools/make_excerpt.py --page 3 --box 0.17,0.66,0.36,0.85 --dpi 159 --width 500`, grayscale quality 75. Crop SHA-256: `52f73010f4e4887413dfb96266d4f674da8e24519851c7e9db2ec969bb7494de`.
