Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 34-35: the transformer schematic 12B-16B-6. Transcribed from page renders at their native resolution; the `Uncertain readings` lists say where a digit or word could not be read.

# Meteor (Stern 1979) - Transformer / power / general illumination (PDF page 34, PDF page 35)

Pages: PDF page 34 (left: transformer, P.C. board TA-100, rectifiers) and PDF page 35 (right: connectors J1, J2, J3 with wire colours and functions). Drawing no. 12B-16B-6; title block (PDF page 35): "STERN ELECTRONICS INC. 1725 DIVERSEY BLVD. CHICAGO 60614 - TRANSFORMER SCHEMATIC - FOR GENERAL USE - DATE 8-24-79".

## Transformer 16B-6 windings (as printed)
| Winding terminals | Printed voltage | Board terminals | Fuse (printed) | Goes to |
| --- | --- | --- | --- | --- |
| 1 / 9 / 5 / 3 / 12 / 11 / 7 (primary taps) | "120 VAC" arrows | E1, E2 | F6 3A (SB) on E1 | AC line |
| 2, 4, 6 | (no voltage printed) | E3 (2) , E4 (6) | F4 (5A.) on E3; VR1 V100ZA15 across E3/E4 | BR3 bridge (VJ248 with R1 600 ohm) -> "43 VDC" (TP5) |
| 17, 18 | 7.3 VAC | E7, E8 | F5 20A. on E7 | "7.3 VAC" line (GEN. ILL.); E8 to ground bus |
| 13, 14 | 7.8 VAC | E9, E10 | F1 10A. on E9 | BR1 bridge (VJ248, R2 25 ohm) -> TP1 -> "5.4 VDC" thick line |
| 15, 16 | 12 VAC | E11, E12 | F3 4 AMP on E11 | BR2 bridge (VJ248) -> TP3 "11.9 VDC" |
| 8, 10 | 173 VAC | E5 (8), E6 (10) | F2 3/4A. (S.B.) on E5 | CR1-CR4 1N4004 (TYP.) bridge, TP2 with R3 100K -> "230 VDC" |

"T1 is NOT LOCATED ON P.C. BOARD." (flag "2" note). Board outline: "TA-100 P.C. BOARD". Test points: TP5 (43 VDC), TP4, TP1, TP3 (11.9 VDC), TP2 (230 VDC via R3 100K).

Printed Notes (verbatim):
1. POWER LINE CONNECTIONS:
| AC LINE VOLTAGE | STRAP TERMINALS | APPLY POWER TO TERM'S. |
| --- | --- | --- |
| 115 | 1 TO 3 & 9 TO 11 | 1 & 9 |
| 120 | 1 TO 3 & 5 TO 7 | 1 & 5 |
| 220 | 3 TO 5 | 1 & 12 |
| 240 | 3 TO 5 | 1 & 7 |

## Connector table (PDF page 35). Wire colour as printed with leading/trailing dashes.
J2 (CABINET):
| Pin | Colour | Function (printed) |
| --- | --- | --- |
| 6 | -Y- | A.C. POWER |
| 7 | -W- | A.C. RETURN |
| 2 | -G- | COIN LOCK-OUT & KNOCKER BUS |
| 1 | Y-B | GEN. ILL. BUS |
| 5 | G-R | GEN. ILL. RETURN |
| 9 | (blank) | (blank, thick ground-bus line drawn to it) |
| 10 | -G- | A.C. POWER GRD. |
| 3 | (blank) | (blank) |
| 4 | (blank) | (blank) |
| 8 | (blank) | KEY |

J1 (PLAYFIELD):
| Pin | Colour | Function |
| --- | --- | --- |
| 5 | (blank) | (blank; tied to pin 8 at a node on the 7.3 VAC line) |
| 8 | -W- | GEN. ILL. BUS |
| 6 | BLU-W | SOLENOID BUS |
| 4 | (blank) | KEY |
| 7 | -BLU- | FEATURE LAMP BUS |
| 1 | -R- | (no function text; = playfield GEN. ILL. return, A2J1-1 (R) on PDF page 36) |
| 2 | (blank) | (blank, thick ground bus) |
| 3 | (blank) | (blank; no line is drawn to this pin, the ground bus branches end at pins 1 and 2) |

J3 (BACK-BOX):
| Pin | Colour | Function |
| --- | --- | --- |
| 9 | -Y- | FLIPPER ENABLE RE. BUS |
| 12 | GREY | ZERO CROSSING INPUT (drawn joined to pins 9 and 13) |
| 13 | (blank) | (blank label; drawn joined to pins 9 and 12) |
| 10 | -O- | GEN. ILL. BUS |
| 11 | -R- | GEN. ILL. BUS |
| 6 | -BLU- | FEATURE LAMP BUS |
| 8 | -O- | 11.9 V.D.C. BUS |
| 5 | GREY | TO REG. 185 VDC INPUT |
| 1 | -G- | GEN. ILL. RETURN |
| 2 | -W- | GEN. ILL. RETURN |
| 3 | R-B | LDA BOARD RETURN |
| 4 | W-R | LDA BOARD RETURN |
| 14 | W-B | LDA BOARD RETURN |
| 15 | W-BLU | SDU BOARD RETURN (REG. SECTION) |
| 16 | B-BLU | SDU BOARD RETURN (REG. SECTION) |
| 17 | W-BRN | +5 FILTER RETURN |
| 18 | -W- | 175 V. FILTER RETURN |
| 19 | R-Y | SDU BOARD RETURN (SOL. DR. SECTION) |
| 20 | W-O | SDU BOARD RETURN (SOL. DR. SECTION) |
| 7 | (blank) | KEY |

Rail labels on PDF page 34/PDF page 35 as drawn: "43 VDC", "7.3 VAC", "5.4 VDC", "11.9 VDC", "230 VDC". Routing from these labelled rails to connector pins (best tracing, PDF page 35 overview): 43 VDC -> J1-6 (solenoid bus), J2-2 (coin lock-out & knocker bus; the vertical from the dot at the `43 VDC` label runs up to it) and J3-9 (flipper enable relay bus), with J3-12 and J3-13 drawn joined to J3-9 by a short vertical; 7.3 VAC -> J1-8 (and J1-5 tied) and also via a vertical to J2-1 and J3-10/J3-11 (general illumination busses); 5.4 VDC -> J1-7 and J3-6 (feature lamp buses); 11.9 VDC -> J3-8; 230 VDC -> J3-5 (to reg. 185 VDC input). Thick lines to J2-5, J2-9, J2-10, J1-1, J1-2, J3-1..J3-4, J3-14..J3-20 are the common return/ground bus from the bridges (E8/E10/E12, etc.).

General illumination, as drawn: bus (supply) pins J1-8 (W), J2-1 (Y-B), J3-10 (O), J3-11 (R); return pins J2-5 (G-R), J3-1 (G), J3-2 (W), J1-1 (R). No relay is drawn in any GI line. The only relay-labelled bus is J3-9 "FLIPPER ENABLE RE. BUS" (Y) which is the +43 VDC supply of the flipper enable relay.

## Uncertain readings
- which rail feeds which connector pin was inferred from line junction dots; the pin-level mapping of 7.3 VAC / 43 VDC to J1-8/J1-6/J2-1/J2-2/J3-10/J3-11/J3-9 is a best reading, the labels on the pins themselves are certain.
- J1-1 "-R-" has no function text; J1-5 has no colour and no text.
- J3-18 "-W-" printed next to "175 V." the leader text reads "175 V. FILTER RETURN" (the drawn rail is 230 VDC elsewhere).
- transformer pin numbers 2/4/6 and the dashed strap lines for 115/120 V are partly dashed; strap geometry not otherwise interpreted.
