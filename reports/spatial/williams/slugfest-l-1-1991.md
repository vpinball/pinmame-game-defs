# SlugFest first-model spatial blockers

Status: **partial**. Coordinates use x left 0/right 1 and y rear 0/front 1.

Exact retained VPX SHA-256: `c75825c0c39fcd89cc9d6c7c60d18fe3257e2c0a07a6321f43306c6d8e244424`. Embedded script: `162f1067a1c0c1f72509b69cde2dc9381f26ccb425f56830e1c8792041fa1f25`.
Factory operations manual: `94d1bce9eaca3dd1b8df72d66050edba3310afdffd86a2a8927ceffb86b9820a`. Extraction manifest: `3e31614714de9b6d84f5817b5188c73ae1536f4165015f98329f12eda0c91730` (3636 files, 741886310 bytes).

The manifest is reproducible with tools/build_external_evidence_manifest.py. It sorts every POSIX relative filename case-sensitively, records byte size and SHA-256, and hashes compact sorted-key UTF-8 JSON with a final LF. Only its own manifest pair is excluded.

Normalization is x=raw_x/1100, y=raw_y/2000, rounded to six places. The committed spatial seed names every exact object and raw point. Cabinet/backbox objects outside the rectangle are classified from the factory physical evidence; they are never clamped into the playfield.

- 53 insert Light centers are report-only reference candidates. They are invisible non-bulb insert overlays; no canonical emitter placement is asserted without physical socket reconciliation.
- Three ramp-flasher Light centers are report-only candidates; canonical physical #912 socket positions are omitted until reconciled.
- GI strings 0/3/4 have no physical bulb inventory or coordinates. Backbox/control-panel devices use not_applicable; no clamping of out-of-range cabinet Light coordinates.
- No registration anchor, baked-mesh primitive origin, Flasher sprite or lightmap receiver is used as a physical placement.
- Model 60001 original dispenser is the physical baseline; later dispenser/cosmetic models and ticket conversion are documented but not fully recreated.

| Device | Object | Raw x,y | Normalized x,y | Evidence role |
| --- | --- | --- | --- | --- |
| pinmame.output.lamp 12 | L12 | 128.34807,411.8434 | 0.11668,0.205922 | candidate insert reference (not bulb) |
| pinmame.output.lamp 13 | L13 | 268.36258,377.8383 | 0.243966,0.188919 | candidate insert reference (not bulb) |
| pinmame.output.lamp 14 | L14 | 408.84988,361.83655 | 0.371682,0.180918 | candidate insert reference (not bulb) |
| pinmame.output.lamp 15 | L15 | 549.84064,347.3418 | 0.499855,0.173671 | candidate insert reference (not bulb) |
| pinmame.output.lamp 16 | L16 | 689.36066,361.8449 | 0.626692,0.180922 | candidate insert reference (not bulb) |
| pinmame.output.lamp 17 | L17 | 829.8746,386.33853 | 0.754431,0.193169 | candidate insert reference (not bulb) |
| pinmame.output.lamp 18 | L18 | 970.35,416.836 | 0.882136,0.208418 | candidate insert reference (not bulb) |
| pinmame.output.lamp 22 | L22 | 129.05472,490.32263 | 0.117322,0.245161 | candidate insert reference (not bulb) |
| pinmame.output.lamp 23 | L23 | 268.6066,464.914 | 0.244188,0.232457 | candidate insert reference (not bulb) |
| pinmame.output.lamp 24 | L24 | 409.56232,438.8287 | 0.372329,0.219414 | candidate insert reference (not bulb) |
| pinmame.output.lamp 25 | L25 | 549.8379,423.11588 | 0.499853,0.211558 | candidate insert reference (not bulb) |
| pinmame.output.lamp 26 | L26 | 690.0738,438.8332 | 0.62734,0.219417 | candidate insert reference (not bulb) |
| pinmame.output.lamp 27 | L27 | 830.10614,464.92065 | 0.754642,0.23246 | candidate insert reference (not bulb) |
| pinmame.output.lamp 28 | L28 | 971.06354,490.33072 | 0.882785,0.245165 | candidate insert reference (not bulb) |
| pinmame.output.lamp 32 | L32 | 128.60995,569.4217 | 0.116918,0.284711 | candidate insert reference (not bulb) |
| pinmame.output.lamp 33 | L33 | 270.05002,541.8272 | 0.2455,0.270914 | candidate insert reference (not bulb) |
| pinmame.output.lamp 34 | L34 | 409.1689,515.1429 | 0.371972,0.257571 | candidate insert reference (not bulb) |
| pinmame.output.lamp 35 | L35 | 549.84467,505.6144 | 0.499859,0.252807 | candidate insert reference (not bulb) |
| pinmame.output.lamp 36 | L36 | 689.6662,515.14307 | 0.626969,0.257572 | candidate insert reference (not bulb) |
| pinmame.output.lamp 37 | L37 | 830.55945,541.8229 | 0.755054,0.270911 | candidate insert reference (not bulb) |
| pinmame.output.lamp 38 | L38 | 970.10944,569.41815 | 0.881918,0.284709 | candidate insert reference (not bulb) |
| pinmame.output.lamp 41 | L41 | 397.75,1614 | 0.361591,0.807 | candidate insert reference (not bulb) |
| pinmame.output.lamp 42 | L42 | 357.9,1540 | 0.325364,0.77 | candidate insert reference (not bulb) |
| pinmame.output.lamp 43 | L43 | 304.775,1481.25 | 0.277068,0.740625 | candidate insert reference (not bulb) |
| pinmame.output.lamp 44 | L44 | 261.375,1429.75 | 0.237614,0.714875 | candidate insert reference (not bulb) |
| pinmame.output.lamp 45 | L45 | 236.42499,1390.5 | 0.214932,0.69525 | candidate insert reference (not bulb) |
| pinmame.output.lamp 46 | L46 | 194.75,1338 | 0.177045,0.669 | candidate insert reference (not bulb) |
| pinmame.output.lamp 47 | L47 | 164.075,1293 | 0.149159,0.6465 | candidate insert reference (not bulb) |
| pinmame.output.lamp 48 | L48 | 103.175,1236.5 | 0.093795,0.61825 | candidate insert reference (not bulb) |
| pinmame.output.lamp 51 | L51 | 162.325,1163.5 | 0.147568,0.58175 | candidate insert reference (not bulb) |
| pinmame.output.lamp 52 | L52 | 190.625,1112.75 | 0.173295,0.556375 | candidate insert reference (not bulb) |
| pinmame.output.lamp 53 | L53 | 238.875,1084.75 | 0.217159,0.542375 | candidate insert reference (not bulb) |
| pinmame.output.lamp 54 | L54 | 285.7,1050 | 0.259727,0.525 | candidate insert reference (not bulb) |
| pinmame.output.lamp 55 | L55 | 350.025,1001 | 0.318205,0.5005 | candidate insert reference (not bulb) |
| pinmame.output.lamp 56 | L56 | 403.375,989.75 | 0.366705,0.494875 | candidate insert reference (not bulb) |
| pinmame.output.lamp 57 | L57 | 456.875,967 | 0.415341,0.4835 | candidate insert reference (not bulb) |
| pinmame.output.lamp 58 | L58 | 551.475,975 | 0.501341,0.4875 | candidate insert reference (not bulb) |
| pinmame.output.lamp 61 | L61 | 641.25,973.25 | 0.582955,0.486625 | candidate insert reference (not bulb) |
| pinmame.output.lamp 62 | L62 | 712.825,985.5 | 0.648023,0.49275 | candidate insert reference (not bulb) |
| pinmame.output.lamp 63 | L63 | 754.175,1007.5 | 0.685614,0.50375 | candidate insert reference (not bulb) |
| pinmame.output.lamp 64 | L64 | 817.10004,1026 | 0.742818,0.513 | candidate insert reference (not bulb) |
| pinmame.output.lamp 65 | L65 | 853.025,1069.75 | 0.775477,0.534875 | candidate insert reference (not bulb) |
| pinmame.output.lamp 66 | L66 | 904.275,1115.5 | 0.822068,0.55775 | candidate insert reference (not bulb) |
| pinmame.output.lamp 67 | L67 | 947.025,1167 | 0.860932,0.5835 | candidate insert reference (not bulb) |
| pinmame.output.lamp 68 | L68 | 549.675,1762.25 | 0.499705,0.881125 | candidate insert reference (not bulb) |
| pinmame.output.lamp 71 | L71 | 946.47504,1308 | 0.860432,0.654 | candidate insert reference (not bulb) |
| pinmame.output.lamp 72 | L72 | 895.97504,1343 | 0.814523,0.6715 | candidate insert reference (not bulb) |
| pinmame.output.lamp 73 | L73 | 861.47504,1395 | 0.783159,0.6975 | candidate insert reference (not bulb) |
| pinmame.output.lamp 74 | L74 | 817.97504,1447.5 | 0.743614,0.72375 | candidate insert reference (not bulb) |
| pinmame.output.lamp 75 | L75 | 783.75,1489.75 | 0.7125,0.744875 | candidate insert reference (not bulb) |
| pinmame.output.lamp 76 | L76 | 747.875,1531.5 | 0.679886,0.76575 | candidate insert reference (not bulb) |
| pinmame.output.lamp 77 | L77 | 701.75,1591.25 | 0.637955,0.795625 | candidate insert reference (not bulb) |
| pinmame.output.lamp 78 | L78 | 994.55,1236.75 | 0.904136,0.618375 | candidate insert reference (not bulb) |
| pinmame.input.switch 41 | CardFaceContact1 | 128.817,318.8519 | 0.117106,0.159426 | target-face projection |
| pinmame.input.switch 42 | CardFaceContact2 | 269.05,311.06952 | 0.244591,0.155535 | target-face projection |
| pinmame.input.switch 43 | CardFaceContact3 | 409.525,308.28525 | 0.372295,0.154143 | target-face projection |
| pinmame.input.switch 44 | CardFaceContact4 | 550,307.5 | 0.5,0.15375 | target-face projection |
| pinmame.input.switch 45 | CardFaceContact5 | 690.475,308.28525 | 0.627705,0.154143 | target-face projection |
| pinmame.input.switch 46 | CardFaceContact6 | 830.95,311.06952 | 0.755409,0.155535 | target-face projection |
| pinmame.input.switch 47 | CardFaceContact7 | 971.183,322.3519 | 0.882894,0.161176 | target-face projection |
| pinmame.output.solenoid 20 | Flasher20 | 346,798 | 0.314545,0.399 | candidate flasher Light center |
| pinmame.output.solenoid 25 | Flasher25 | 551,634 | 0.500909,0.317 | candidate flasher Light center |
| pinmame.output.solenoid 26 | Flasher26 | 761,798 | 0.691818,0.399 | candidate flasher Light center |

The seven target contacts are explicit target-face projections, not surveyed switch-wire coordinates. The insert positions follow script bindings (AllLamps plus TimerInterval), not names alone. Flasher candidates use script-driven Light centers; their physical #912 socket positions still require reconciliation.

## Physical devices without placements

- switch.51: Back Row Trough. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.52: Strike Trough. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.54: Pitch Home. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.55: Ramp Timing Opto. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.56: Playfield Tilt 1. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.57: Playfield Tilt 2. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.61: Left Grandstand Return. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.62: Middle Grandstand Return. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- switch.63: Right Grandstand Return. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.1: Baseball Bat. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.2: Pitch Magnet. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.20: Left Ramp Flasher. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.21: Center Ramp Motor. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.22: Pitch Motor Fast Drive. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.23: Pitch Motor Medium Drive. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.24: Pitch Motor Slow Drive. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.25: Center Ramp Flasher. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- solenoid.26: Right Ramp Flasher. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.12: Out Top Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.13: Out Top 2 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.14: Out Top 3 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.15: Out Top Center. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.16: Out Top 3 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.17: Out Top 2 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.18: Out Top Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.22: Single Middle Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.23: Double Middle 2 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.24: Single Middle 3 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.25: Sacrifice Middle Center. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.26: Single Middle 2 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.27: Double Middle 1 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.28: Single Middle Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.32: Double Bottom Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.33: Single Bottom 2 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.34: Triple Bottom 3 Left. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.35: Home Run Bottom Center. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.36: Triple Bottom 2 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.37: Single Bottom 1 Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.38: Double Bottom Right. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.41: Runner #32. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.42: Runner #31. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.43: Runner #30. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.44: Runner #29. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.45: Runner #28. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.46: Runner #27. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.47: Runner #26. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.48: Runner #25 (Third Base). Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.51: Runner #24. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.52: Runner #23. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.53: Runner #22. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.54: Runner #21. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.55: Runner #20. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.56: Runner #19. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.57: Runner #18. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.58: Runner #17 (Second Base). Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.61: Runner #16. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.62: Runner #15. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.63: Runner #14. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.64: Runner #13. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.65: Runner #12. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.66: Runner #11. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.67: Runner #10. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.68: Runner #1 (Home). Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.71: Runner #8. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.72: Runner #7. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.73: Runner #6. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.74: Runner #5. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.75: Runner #4. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.76: Runner #3. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.77: Runner #2. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- lamp.78: Runner #9 (First Base). Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- gi.0: GI Infield Top. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- gi.3: GI Outfield. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
- gi.4: GI Infield Bottom. Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate.
