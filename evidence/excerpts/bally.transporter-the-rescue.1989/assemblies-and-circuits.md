# Assemblies and circuits

Method: manual visual reading by the primary curator from native-resolution retained renders; reviewed against the original page image on 2026-11-06. Source line breaks are joined; spelling and part numbers are retained.

Original manual SHA-256: `d1e29962c3bc53733ba61a62d8d814d2a1adbf508f78dfe10c01cd4fb95f2ce9`.

## PDF 51, printed 2-2: Major Assemblies (complete table region)

| Item | Description | Part number |
| --- | --- | --- |
| 1 | Post | 02-3905 |
| 2 | Lower Left Flipper Assy | C-11626-L-3 |
| 2a | Ball Flipper (Yellow) | 20-9592-6 |
| 3 | Bottom Arch Assembly | D-12861 |
| 4 | Bottom Arch Kicker Assy | B-11873-1 |
| 5 | 3-Bank Drop Target | C-11223-1 |
| 6 | Ball Gate Assembly | A-12915 |
| 7 | Standup Target, Tr Orn | B-12912-12 |
| 8 | Jet Bumper Assembly | C-12872 |
| 9 | Ball Gate Assembly | A-8244-1 |
| 10 | Ball Gate Assembly | A-12910 |
| 11 | Left Lockup (Kicker) | B-12871-1 |
| 12 | Right Lockup (Kicker) | B-12871 |
| 13 | Deflector Assembly | B-12878 |
| 14 | Spin Target Assembly | B-12164 |
| 15 | Lt & Rt Slingshot Assy | C-12873 |
| 16 | Lower Rt Flipper Assy | C-11626-R-3 |
| 16a | Ball Flipper (Yellow) | 20-9592-6 |
| 17 | Ball Shooter Lane Feeder | C-9638 |
| 17a | Coil & Bracket Assembly | B-9362-L-1 |
| 18 | Outhole Kicker Assembly | B-8039-2 |
| 19 | Ball Popper Assembly | D-11335-2 |
| 20 | Ball Trough Assy: Lwr Guide | C-8235 |
| 20 | Ball Trough Assy: Upr Guide | B-8623 |
| 21 | Space Ship Assembly | D-12896 |
| 22 | Ball Gate Actuator | B-12942 |
| 23 | Upper Right Flipper | C-11626-R-3 |
| 23a | Lg Bally Flipper (Yellow) | 20-9669-6 |

## PDF 61: 3-Bank Drop Target Board & Schematic

The board outline identifies part C-12559 with OPTO 1, OPTO 2 and OPTO 3. The schematic identifies three optical emitter/receiver pairs and LM339/4 comparator outputs to J1 row 1 (pin 4), row 2 (pin 5), row 3 (pin 7), with J1 pin 1 column. J1 pin 6 is Key; J1 pins 2 and 3 have no printed signal label. J2 pin 1 is +12V Power Input, pin 2 Key, pin 3 Circuitry Ground and pin 4 N.C. This is construction evidence for the bank switches, independently of the unshaded matrix cells. It does not by itself call a clear or blocked beam an active matrix closure.

## PDF 6, printed 1-3, and PDF 7, printed 1-4

The underside board/mechanism diagram shows two three-bank drop target mechanisms, three thumper bumpers, the ball popper, top flipper gate, lower left/right and upper right flippers, left/right slingshots, kickback, outhole, ball trough and shooter-lane feeder. The insert board carries a relay board; the playfield carries a separate relay board. The board names are Power Supply D-12246, Aux Power Driver D-12247-2008 and Master Interconnect D-12313-2008. The control-locations text puts Advance, Auto-Up/Manual-Down and High-Score Reset inside the coin door; Credit is a button beside the door. CPU and sound diagnostic switches are on the CPU board in the backbox. The memory-protect interlock is on the coin-door frame and opens with the door.

## PDF 78, Controlled, Special & Switched Solenoids

The circuit drawing labels controlled output 9 PLAYFIELD GEN. ILLUM. RELAY (Q17), output 12 A/C SELECT RELAY (AUX PWR DRVR) (Q8), output 13 Not Used (Q15), output 10 TOP FLIPPER GATE (Q9), output 11 TURN 1 FLASHER (Q16), output 15 TURN 2 FLASHER (Q14), and output 16 TURN 3 FLASHER (Q6). Its special branch labels 17 LEFT THUMPER BUMPER (Q75), 19 RIGHT THUMPER BUMPER (Q73), 21 LOWER THUMPER BUMPER (Q77), 22 INSERT BD. GEN. ILLUM. RELAY (Q79), 14 KICKBACK (L Outlane) (Q7), 18 LEFT KICKER ("sling") (Q71), and 20 RIGHT KICKER ("sling") (Q69). The switched branch pairs each 01A-08A load and 01C-08C flasher through the A/C select circuitry. This page establishes circuit identity and separate playfield/insert GI control; it does not enumerate GI sockets or their locations.
