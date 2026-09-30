# Stern World Poker Tour (2006) — reviewed manual address excerpts

Status: **curator-checked against rendered factory pages 6, 8, 10, and 125; additional transcription remains candidate where stated.** This document is a literal manual transcription for high-tier curation. It makes no machine, source-authority, runtime, topology, or spatial-coordinate decision.

## Source and transcription envelope

| Field | Value |
| --- | --- |
| Source | *World Poker Tour Manual*, Stern Pinball |
| Original PDF | `World_Poker_Tour_Manual.pdf` |
| PDF SHA-256 | `4cf31702805e75d37aef1c0c1624426000fec6cabf71a47e27691f5d5f8b6d01` |
| Manufacturer URL | https://sternpinball.com/wp-content/uploads/2018/11/World_Poker_Tour_Manual.pdf |
| Discovery URL / downloaded | https://sternpinball.com/manuals/ / 2026-09-30 UTC |
| Attribution / license | Stern Pinball / NOASSERTION |
| Method | Visual transcription from derived renders made with `tools/render_excerpt_image.py`; existing PDF text layer used only as a secondary check. |
| Transcriber / model | GPT Terra manual-research worker (Codex session 2026-09-30); Sol curator corrected selected cells against factory renders |
| Review distinction | Sol curator visually checked the switch, lamp, coil and GI source pages. Table transcription remains secondary to the retained factory PDF. |
| Blank-cell convention | `— (printed blank)` means the source cell was visibly blank. It is never filled from a neighboring/repeated row. |

## Switch matrix grid (01–64)

The separate switch-location drawing on PDF page **7** marks SW15 Tournament Start with **“Optional Tournament Kit Required.”** Its matrix address is present regardless of kit fitment; the physical button is optional.

Evidence: PDF one-based page **6**, printed locator **DR. 4**, heading **“SWITCH MATRIX GRID (01-64)”**. Derived full-page crop: `terra-renders/wpt-p006-switch-and-dedicated-table-upright.webp`, SHA-256 `e984a247602ff1b9320f0dbf49d8836636fe3f32e57e41637e3104d083aa644f`; vector type-size-derived 132 dpi, color, rotated 90° CCW, 1452×1122. A focused lower/right crop is also present as `wpt-p006-switch-49-64.webp` (SHA-256 `8f43d7…`; table range actually includes 33–64). Method/transcriber/attribution/license/status are the envelope above; **candidate / reviewed false**.

The source presents row-drive fields as merged ranges, not as newly printed text in every switch row:

| Switch range | Printed drive transistor | Wire color | Connector pin |
| --- | --- | --- | --- |
| 01–16 | Q1 | GRN-BRN | J1-P1 |
| 17–32 | Q2 | GRN-RED | J1-P3 |
| 33–48 | Q3 | GRN-ORG | J1-P4 |
| 49–64 | Q4 | GRN-YEL | J1-P5 |

| Return | Printed IC | Wire color | Connector pin |
| --- | --- | --- | --- |
| 1 | IC-U22A | WHT-BRN | J6-P9 |
| 2 | IC-U22B | WHT-RED | J6-P8 |
| 3 | IC-U22C | WHT-ORG | J6-P7 |
| 4 | IC-U22D | WHT-YEL | J6-P6 |
| 5 | IC-U15A | WHT-GRN | J6-P5 |
| 6 | IC-U15B | WHT-BLU | J6-P3 |
| 7 | IC-U15C | WHT-VIO | J6-P2 |
| 8 | IC-U15D | WHT-GRY | J6-P1 |
| 9 | IC-U35A | TAN-BLK | J12-P9 |
| 10 | IC-U35B | TAN-RED | J12-P8 |
| 11 | IC-U35C | TAN-ORG | J12-P7 |
| 12 | IC-U35D | TAN-YEL | J12-P6 |
| 13 | IC-U40A | TAN-GRN | J12-P4 |
| 14 | IC-U40B | TAN-BLU | J12-P3 |
| 15 | IC-U40C | TAN-VIO | J12-P2 |
| 16 | IC-U40D | TAN-WHT | J12-P1 |

| # | Literal switch name | Printed switch/type note | Part number / printed component | Printed location |
| ---: | --- | --- | --- | --- |
| 1 | NOT USED | — (printed blank) | 180-0000-00 | On Assembly |
| 2 | NOT USED | — (printed blank) | 180-0000-00 | On Assembly |
| 3 | SHOOTER LANE VUK | D.O.T.S. | 180-5209-00 | On Assembly |
| 4 | RIGHT DROP #1 (BOT) | OPTO 'U' | 520-5252-04 | On Assembly |
| 5 | RIGHT DROP #2 | OPTO 'U' | 520-5252-04 | On Assembly |
| 6 | RIGHT DROP #3 | OPTO 'U' | 520-5252-04 | On Assembly |
| 7 | RIGHT DROP #4 (TOP) | OPTO 'U' | 520-5252-04 | On Assembly |
| 8 | RIGHT ORBIT SPINNER | D.O.T.S. | 180-5010-04 | Above P/F |
| 9 | RIGHT RAMP ENTER | GATE SW. | 180-5010-01 | Above P/F |
| 10 | MIDDLE DROP #1 | OPTO 'U' | 520-5252-04 | On Assembly |
| 11 | MIDDLE DROP #2 | OPTO 'U' | 520-5252-04 | On Assembly |
| 12 | MIDDLE DROP #3 | OPTO 'U' | 520-5252-04 | On Assembly |
| 13 | MIDDLE DROP #4 | OPTO 'U' | 520-5252-04 | On Assembly |
| 14 | LOWER RIGHT 10 PT | D.O.T.S. | 180-5054-00 | Below P/F |
| 15 | TOURNAMENT START | CABINET | 180-5119-03 | Front Molding |
| 16 | START BUTTON | CABINET | 180-5174-00 | In Cabinet |
| 17 | NOT USED | — (printed blank) | 180-5119-02 | Below P/F |
| 18 | 4-BALL TROUGH #4 (L) | — (printed blank) | 180-5119-02 | On Assembly |
| 19 | 4-BALL TROUGH #3 | — (printed blank) | 180-5119-02 | On Assembly |
| 20 | 4-BALL TROUGH #2 | — (printed blank) | 180-5119-02 | On Assembly |
| 21 | 4-BALL TROUGH #1 (R) | OPTO PAIR | TX 515-0173-00; RX 515-0174-00 | On Assembly |
| 22 | 4-BALL STACKING OPTO | OPTO PAIR | TX 515-0173-00; RX 515-0174-00 | On Assembly |
| 23 | SHOOTER LANE | — (printed blank) | 180-5157-00 | Below P/F |
| 24 | LEFT OUTLANE | — (printed blank) | 500-6227-04 | Below P/F |
| 25 | LEFT RETURN LANE | — (printed blank) | 500-6227-04 | Below P/F |
| 26 | LEFT SLING-SHOT | — (printed blank) | 180-5054-00 | 2 per Asm. |
| 27 | RIGHT SLING-SHOT | — (printed blank) | 180-5054-00 | 2 per Asm. |
| 28 | RIGHT RETURN LANE | — (printed blank) | 500-6227-04 | Below P/F |
| 29 | RIGHT OUTLANE | — (printed blank) | 500-6227-04 | Below P/F |
| 30 | LEFT BUMPER | — (printed blank) | 180-5015-04 | On Assembly |
| 31 | RIGHT BUMPER | — (printed blank) | 180-5015-04 | On Assembly |
| 32 | BOTTOM BUMPER | — (printed blank) | 180-5015-04 | On Assembly |
| 33 | LEFT DROP #1 (BOT) | OPTO 'U' | 520-5252-04 | On Assembly |
| 34 | LEFT DROP #2 | OPTO 'U' | 520-5252-04 | On Assembly |
| 35 | LEFT DROP #3 | OPTO 'U' | 520-5252-04 | On Assembly |
| 36 | LEFT DROP #4 | OPTO 'U' | 520-5252-04 | On Assembly |
| 37 | LEFT DROP #5 | OPTO 'U' | 520-5252-04 | On Assembly |
| 38 | LEFT DROP #6 | OPTO 'U' | 520-5252-04 | On Assembly |
| 39 | LEFT DROP #7 | OPTO 'U' | 520-5252-04 | On Assembly |
| 40 | LEFT DROP #8 (TOP) | OPTO 'U' | 520-5252-04 | On Assembly |
| 41 | LOWER LEFT 10 PT | — (printed blank) | 180-5054-00 | Below P/F |
| 42 | LOWER LEFT TARGET | — (printed blank) | 500-5232-08 | Below P/F |
| 43 | LEFT ORBIT SPINNER | — (printed blank) | 180-5010-04 | Above P/F |
| 44 | LEFT ORBIT HI | GATE SW. | 180-5087-00 | Above P/F |
| 45 | POP STANDUP #1 (L) | RED SQ. | 500-6983-02 | Below P/F |
| 46 | POP STANDUP #2 | RED SQ. | 500-6983-02 | Below P/F |
| 47 | POP STANDUP #3 | RED SQ. | 500-6983-02 | Below P/F |
| 48 | POP STANDUP #4 (R) | RED SQ. | 500-6983-02 | Below P/F |
| 49 | POP EJECT | D.O.T.S. | 180-5209-00 | On Assembly |
| 50 | RIGHT ORBIT HI | GATE SW. | 180-5087-00 | Above P/F |
| 51 | SHOOTER VUK EXIT | GATE SW. | 180-5010-01 | Above P/F |
| 52 | RIGHT RAMP MADE | OPTO PAIR | 500-6775-00 | On Assembly |
| 53 | UPF EXIT | GATE SW. | 180-5010-01 | Above P/F |
| 54 | LEFT RAMP MADE | OPTO PAIR | 500-6775-00 | On Assembly |
| 55 | LEFT VUK | D.O.T.S. | 180-5209-00 | On Back Panel |
| 56 | UPF ABOVE LEFT VUK | OPTO PAIR | 500-6775-00 | On Assembly |
| 57 | JAIL BARS BASH | TRANS. / REC. | TX 520-5247-00; RX 520-5248-00 | — (printed blank) |
| 58 | JAIL BARS REST | TRANS. / REC. | TX 520-5247-00; RX 520-5248-00 | — (printed blank) |
| 59 | TRANSFER TUBE #1 (L) | OPTO PAIR | 515-7498-08-01 | on Back Panel |
| 60 | UPF STANDUP #1 (L) | WHITE SQ. | 515-7497-08-01 | on Back Panel |
| 61 | UPF STANDUP #2 | WHITE SQ. | 515-7497-08-01 | on Back Panel |
| 62 | UPF STANDUP #3 | WHITE SQ. | 515-7497-08-01 | on Back Panel |
| 63 | JAIL BARS UP | OPTO 'U' | 520-5251-00 | On Assembly |
| 64 | NOT USED | — (printed blank) | — (printed blank) | — (printed blank) |

PDF page 7 / printed DR.5 **Switch Part Notes** footnote, checked on the full vector render and a four-times zoom crop: “¥ Yen Coin Switch is 180-5091-00. Part Numbers which start with 515- or 500- include the bracket, target, and/or housing. Sw. 56 Part Note: The Switch is comprised of a Hanger Bracket (535-5319-00) and Contact Wire (535-7563-01) located in the Cabinet. Some Switch Diodes may be located under the playfield, in the Cabinet or Backbox on Terminal Strips or Diode Boards and not on the assemblies.” The same page prints “DOTS: Diode On Terminal Strip, see Sec. 5, Chp.2, Playfield Wiring.” The SW56 statement conflicts with the page-6 grid's `OPTO PAIR` and the page-7 backpanel drawing's paired SW56 locations. The footer's generic Section 4/Chapter 1/page 63 reference does not identify this particular switch assembly.

PDF page 126 / printed Sec.5 Ch.2 p.100 **Playfield Switch Wiring**, visually checked on the full vector render, independently labels switch 54 `LEFT RAMP MADE` in the switch matrix. This supports the page-6 chart and page-7 left-ramp location, while the distinct transfer-trough assembly on PDF p.119 also prints `SW.54` beside its paired optical transmitter/receiver boards. Each transmitter/receiver pair is one beam; neither drawing proves that the two installed beams are independent public switch addresses. The discrepancy stays open pending harness continuity or a discriminating installed-machine ROM switch test.

## Dedicated switches (D1–D24) and CPU/Sound SW1

Evidence: same PDF page **6**, printed **DR. 4**, heading **“Dedicated Switches (D1-D24)”** and **“CPU/Snd. SW1 Dip Switches (1-8)”**. Same crop, SHA/method/transcriber/attribution/license/status as the preceding table; **candidate / reviewed false**.

| Range / IC | Dedicated drive | Wire color | Connector pin | Printed ground |
| --- | --- | --- | --- | --- |
| D1–D8 / IC-U2 | D1 | PNK-BRN | J2-P2 | J2-P1/11 & J3-P1 |
|  | D2 | PNK-RED | J2-P3 | *(merged as above)* |
|  | D3 | PNK-ORG | J2-P4 | *(merged as above)* |
|  | D4 | PNK-YEL | J2-P6 | *(merged as above)* |
|  | D5 | PNK-GRN | J2-P7 | *(merged as above)* |
|  | D6 | PNK-BLU | J2-P8 | *(merged as above)* |
|  | D7 | PNK-VIO | J2-P9 | *(merged as above)* |
|  | D8 | PNK-GRY | J2-P10 | *(merged as above)* |
| D9–D16 / IC-U4 | D9 | GRY-BRN | J3-P1 | J3-P10 |
|  | D10 | GRY-RED | J3-P2 | *(merged as above)* |
|  | D11 | GRY-ORG | J3-P4 | *(merged as above)* |
|  | D12 | GRY-YEL | J3-P5 | *(merged as above)* |
|  | D13 | GRY-GRN | J3-P6 | *(merged as above)* |
|  | D14 | GRY-BLU | J3-P7 | *(merged as above)* |
|  | D15 | GRY-VIO | J3-P8 | *(merged as above)* |
|  | D16 | GRY-BLK | J3-P9 | *(merged as above)* |
| D17–D24 / IC-41 | D17 | LGN-BRN | J13-P1 | J13-P10 |
|  | D18 | LGN-RED | J13-P3 | *(merged as above)* |
|  | D19 | LGN-ORG | J13-P4 | *(merged as above)* |
|  | D20 | LGN-YEL | J13-P5 | *(merged as above)* |
|  | D21 | LGN-BLK | J13-P6 | *(merged as above)* |
|  | D22 | LGN-BLU | J13-P7 | *(merged as above)* |
|  | D23 | LGN-VIO | J13-P8 | *(merged as above)* |
|  | D24 | LGN-GRY | J13-P9 | *(merged as above)* |

| # | Literal dedicated switch name | Printed note | Part number / printed component | Printed location |
| ---: | --- | --- | --- | --- |
| D1 | LEFT COIN SLOT | — (printed blank) | 180-5204-00 | Coin Door |
| D2 | CENTER COIN SLOT | — (printed blank) | 180-5204-00 | Coin Door |
| D3 | RIGHT COIN SLOT | — (printed blank) | 180-5204-00 | Coin Door |
| D4 | 4TH COIN SLOT | — (printed blank) | 180-5204-00 | Coin Door |
| D5 | 5TH COIN SLOT | IF USED | 180-5204-00 | Coin Door |
| D6 | NOT USED | — (printed blank) | 180-0000-00 | — (printed blank) |
| D7 | LT POST SAVE (UK ONLY) | — (printed blank) | 180-5160-01 | Cabinet Side |
| D8 | RT POST SAVE (UK ONLY) | — (printed blank) | 180-5160-01 | Cabinet Side |
| D9 | LEFT FLIPPER BUTTON | — (printed blank) | 180-5160-01 | Cabinet Side |
| D10 | LEFT FLIPPER E.O.S. | — (printed blank) | 180-5149-00 | Flipper Asm. |
| D11 | RIGHT FLIPPER BUTTON | — (printed blank) | 180-5160-01 | Cabinet Side |
| D12 | RIGHT FLIPPER E.O.S. | — (printed blank) | 180-5149-00 | Flipper Asm. |
| D13 | UPR. LT. FLIPPER BUTTON | — (printed blank) | 180-5160-01 | Cabinet Side |
| D14 | UPR. LT. FLIPPER E.O.S. | — (printed blank) | 180-5149-00 | Flipper Asm. |
| D15 | UPR. RT. FLIPPER BUTTON | — (printed blank) | 180-5160-01 | Cabinet Side |
| D16 | UPR. RT. FLIPPER E.O.S. | — (printed blank) | 180-5149-00 | Flipper Asm. |
| D17 | TILT PENDULUM (PLUMB BOB) | See Sec. 4 Chp. 1, Pg. 63 for cab. parts | — (printed blank) | — (printed blank) |
| D18 | SLAM TILT (OPT.) | Optional Kit | 502-5032-00 | — (printed blank) |
| D19 | TICKET NOTCH IF USED | — (printed blank) | 180-5119-02 | Below P/F |
| D20 | NOT USED | — (printed blank) | 180-0000-00 | — (printed blank) |
| D21 | BACK BUTTON (GREEN) | — (printed blank) | 180-5192-04 | Coin Door |
| D22 | < / - BUTTON (RED) | — (printed blank) | 180-5192-02 | Coin Door |
| D23 | + / > BUTTON (RED) | — (printed blank) | 180-5192-02 | Coin Door |
| D24 | SELECT BUTTON (BLACK) | — (printed blank) | 180-5192-00 | Coin Door |

The eight printed CPU/Sound SW1 entries are, literally, “DIP SWITCH POSITION #1” through “DIP SWITCH POSITION #8”; each has printed states **ON** and **OFF**. Printed location: “Between Connectors J3 / J13”, “D-IP SW1 CPU/SOUND BD.”

## Lamp matrix (01–80)

Evidence: PDF one-based page **8**, printed locator **DR. 6**, heading **“LAMP MATRIX (01-80)”**. Derived full-page crop: `terra-renders/wpt-p008-lamp-table-upright.webp`, SHA-256 `010f9137a37e3217f823e086d83abcf1e43536bef10951849de426e457e55721`; vector type-size-derived 113 dpi, color, rotated 90° CCW, 1245×962. Focus crop: `wpt-p008-lamp-57-80.webp`, SHA-256 `e6458bc78a0f826a454c988e372918fa651866bd76c48a484cf3937a5086d8f5`. **Candidate / reviewed false.**

The source's electrical header has these explicitly printed lamp-column feeds. The Q41/Q42 groups do not print a new IC/feed group; this is a merged/repeated matrix header, so no missing value is inferred.

| Lamps | Drive | Ground / J12 | Printed IC / 18VDC feed / J13 |
| --- | --- | --- | --- |
| 01–08 | Q33 | RED-BRN / J12-P1 | IC-U17 / YEL-BRN / J13-P9 |
| 09–16 | Q34 | RED-BLK / J12-P2 | IC-U16 / YEL-RED / J13-P8 |
| 17–24 | Q35 | RED-ORG / J12-P3 | IC-U15 / YEL-ORG / J13-P7 |
| 25–32 | Q36 | RED-YEL / J12-P4 | IC-U14 / YEL-BLK / J13-P6 |
| 33–40 | Q37 | RED-GRN / J12-P5 | IC-U13 / YEL-GRN / J13-P5 |
| 41–48 | Q38 | RED-BLU / J12-P6 | IC-U12 / YEL-BLU / J13-P4 |
| 49–56 | Q39 | RED-VIO / J12-P7 | IC-U11 / YEL-VIO / J13-P3 |
| 57–64 | Q40 | RED-GRY / J12-P9 | IC-U10 / YEL-GRY / J13-P1 |
| 65–72 | Q41 | RED-WHT / J12-P10 | — (merged/repeated header; no new value printed) |
| 73–80 | Q42 | RED / J12-P11 | — (merged/repeated header; no new value printed) |

| # | Printed bulb type | Literal lamp name | Part number |
| ---: | --- | --- | --- |
| 1 | #555 Clear | START BUTTON | 165-5002-00 |
| 2 | #CM86 Clr. | TOURNAMENT BUTTON | 165-5103-00 |
| 3 | #555 Clear | DEAL AGAIN | 165-5002-00 |
| 4 | #555 Clear | LEFT SPECIAL | 165-5002-00 |
| 5 | #555 Clear | L. TRIPLE SCORE | 165-5002-00 |
| 6 | #555 Clear | R. TRIPLE SCORE | 165-5002-00 |
| 7 | #555 Clear | RIGHT SPECIAL | 165-5002-00 |
| 8 | #555 Clear | LIGHT LOCK | 165-5002-00 |
| 9 | #555 Clear | ONE PAIR | 165-5002-00 |
| 10 | #555 Clear | TWO PAIR | 165-5002-00 |
| 11 | #555 Clear | THREE OF A KIND | 165-5002-00 |
| 12 | #555 Clear | SKILL FLIP | 165-5002-00 |
| 13 | #44 Clear | LEFT RAMP ARROW | 165-5000-44-HF |
| 14 | #44 Clear | LEFT RAMP RIVER | 165-5000-44-HF |
| 15 | #44 Clear | RIGHT RAMP ARROW | 165-5000-44-HF |
| 16 | #44 Clear | RIGHT RAMP RIVER | 165-5000-44-HF |
| 17 | #555 Clear | STRAIGHT | 165-5002-00 |
| 18 | #555 Clear | FLUSH | 165-5002-00 |
| 19 | #555 Clear | FULL HOUSE | 165-5002-00 |
| 20 | #555 Clear | MYSTERY | 165-5002-00 |
| 21 | #44 Clear | LEFT RAMP TURN | 165-5000-44-HF |
| 22 | #44 Clear | LEFT RAMP FLOP | 165-5000-44-HF |
| 23 | #44 Clear | RIGHT RAMP TURN | 165-5000-44-HF |
| 24 | #44 Clear | RIGHT RAMP FLOP | 165-5000-44-HF |
| 25 | #555 Clear | FOUR OF A KIND | 165-5002-00 |
| 26 | #555 Clear | STRAIGHT FLUSH | 165-5002-00 |
| 27 | #555 Clear | ROYAL FLUSH | 165-5002-00 |
| 28 | #555 Clear | ADVANCE HOLD EM | 165-5002-00 |
| 29 | #555 Clear | LEFT RAMP CHIP TRICK | 165-5002-00 |
| 30 | #555 Clear | EJECT ARROW | 165-5002-00 |
| 31 | #555 Clear | WPT CHAMPIONSHIP | 165-5002-00 |
| 32 | #555 Clear | RIGHT RAMP CHIP TRICK | 165-5002-00 |
| 33 | #44 Clear | ACE OF SPADES | 165-5000-44-HF |
| 34 | #44 Clear | QUEEN OF HEARTS | 165-5000-44-HF |
| 35 | #44 Clear | TEN OF SPADES | 165-5000-44-HF |
| 36 | #44 Clear | JACK OF DIAMONDS | 165-5000-44-HF |
| 37 | #555 Clear | POKER CORNER | 165-5002-00 |
| 38 | #555 Clear | EJECT LOCK | 165-5002-00 |
| 39 | #555 Clear | ARUBA | 165-5002-00 |
| 40 | #555 Clear | LOS ANGELES | 165-5002-00 |
| 41 | #44 Clear | EIGHT OF SPADES | 165-5000-44-HF |
| 42 | #44 Clear | QUEEN OF SPADES | 165-5000-44-HF |
| 43 | #44 Clear | TEN OF CLUBS | 165-5000-44-HF |
| 44 | #44 Clear | KING OF CLUBS | 165-5000-44-HF |
| 45 | #555 Clear | SPIN A CARD | 165-5002-00 |
| 46 | #555 Clear | EJECT CHIP TRICK | 165-5002-00 |
| 47 | #555 Clear | BAHAMAS | 165-5002-00 |
| 48 | #555 Clear | PARIS | 165-5002-00 |
| 49 | #44 Clear | NINE OF SPADES | 165-5000-44-HF |
| 50 | #44 Clear | KING OF HEARTS | 165-5000-44-HF |
| 51 | #44 Clear | NINE OF DIAMONDS | 165-5000-44-HF |
| 52 | #44 Clear | JACK OF SPADES | 165-5000-44-HF |
| 53 | #555 Clear | LEFT ORBIT ARROW | 165-5002-00 |
| 54 | #555 Clear | LEFT ORBIT CHIP TRICK | 165-5002-00 |
| 55 | #555 Clear | ATLANTIC CITY | 165-5002-00 |
| 56 | #555 Clear | LAS VEGAS | 165-5002-00 |
| 57 | #44 Clear | KING OF DIAMONDS | 165-5000-44-HF |
| 58 | #44 Clear | SEVEN OF SPADES | 165-5000-44-HF |
| 59 | #44 Clear | QUEEN OF CLUBS | 165-5000-44-HF |
| 60 | #44 Clear | KING OF SPADES | 165-5000-44-HF |
| 61 | #555 Clear | RIGHT ORBIT ARROW | 165-5002-00 |
| 62 | Lamp Note 1 | LEFT BUMPER / « D.O.T.S. » | 112-5024-08 |
| 63 | #555 Clear | STEAL THE BLIND | 165-5002-00 |
| 64 | #555 Clear | A CHIP AND A CHAIR | 165-5002-00 |
| 65 | #555 Clear | LEFT VUK ARROW | 165-5002-00 |
| 66 | #555 Clear | CUT THE CARDS | 165-5002-00 |
| 67 | #44 Blue | POP STANDUP #1 (L) | 165-503-05-HF |
| 68 | #44 Blue | POP STANDUP #2 | 165-503-05-HF |
| 69 | #555 Clear | RIGHT ORBIT CHIP TRICK | 165-5002-00 |
| 70 | Lamp Note 1 | RIGHT BUMPER / « D.O.T.S. » | 112-5024-08 |
| 71 | #555 Clear | PLAY THE BUTTON | 165-5002-00 |
| 72 | #555 Clear | SPOT THE TELL | 165-5002-00 |
| 73 | #555 Clear | LEFT VUK LOCK | 165-5002-00 |
| 74 | #555 Clear | EXTRA BALL | 165-5002-00 |
| 75 | #44 Blue | POP STANDUP #3 | 165-503-05-HF |
| 76 | #44 Blue | POP STANDUP #4 (R) | 165-503-05-HF |
| 77 | LP. #77 | NOT USED | — (printed blank) |
| 78 | Lamp Note 1 | BOTTOM BUMPER / « D.O.T.S. » | 112-5024-08 |
| 79 | #555 Clear | KNOW YOUR OUTS | 165-5002-00 |
| 80 | #555 Clear | CHANGE GEARS | 165-5002-00 |

Literal note: “Lamp Note 1 = White LED Module (Wedge Base #555 Style) 112-5024-08.” Page DR. 7 additionally prints: “#555 Wedge Base (W.B.) Bulb Clear = 165-5002-00”; “#44 Bayonet Base (B.B.) Clear Filament Clear = 165-5000-44-HF”; “#555 LED Wedge Base White = 112-5024-08”.

## Coils and flash lamps detailed chart

Evidence: PDF one-based page **10**, printed locator **DR. 8**, heading **“COILS DETAILED CHART TABLE”**. Crops: `terra-renders/wpt-p010-coils-1-24.webp`, SHA-256 `9b1e0bbd63cdae68c311cfaa756d1c118372602df51da24b03abefd0a55a0d5a`; `wpt-p010-coils-25-32.webp`, SHA-256 `4cf902bd02a62b75cc5db433cfca8b03cd5231cb11b290f6a028d0ef6e2d4cbb`. Both are color, vector type-size-derived 132 dpi. **Candidate / reviewed false.**

The printed headers are: Drive Transistor; Driver Output Board; Power Line Color; Power Line Connection; Power Voltage; Drive Transistor Control Line Color; D.T. Control Line Connect; Coil GA-Turn or Bulb Type. “I/O Power Driver” is a merged Driver Output Board cell over the table, not inserted as new independent text on every row.

| # | Literal coil / flash lamp | Drive | Power line color | Connection | Voltage | Control-line color | Control connection | Coil GA-Turn / bulb | Part number |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TROUGH UP-KICKER | Q1 | YEL-VIO | J10-P9/10 | 50v DC | BRN-BLK | J8-P1 | 26-1200 | 090-5044-ND |
| 2 | AUTO LAUNCH | Q2 | YEL-VIO | J10-P9/10 | 50v DC | BRN-RED | J8-P3 | 23-800 | 090-5001-ND |
| 3 | SHOOTER LANE VUK | Q3 | YEL-VIO | J10-P9/10 | 50v DC | BRN-ORG | J8-P4 | 26-1200 | 090-5044-ND |
| 4 | LEFT VUK | Q4 | YEL-VIO | J10-P9/10 | 50v DC | BRN-YEL | J8-P5 | 26-1200 | 090-5044-ND |
| 5 | LOWER LEFT DROP RESET | Q5 | YEL-VIO | J10-P9/10 | 50v DC | BRN-GRN | J8-P6 | 23-800 | 090-5001-ND |
| 6 | UPPER LEFT DROP RESET | Q6 | YEL-VIO | J10-P9/10 | 50v DC | BRN-BLU | J8-P7 | 23-800 | 090-5001-ND |
| 7 | MIDDLE DROP RESET | Q7 | YEL-VIO | J10-P9/10 | 50v DC | BRN-VIO | J8-P8 | 23-800 | 090-5001-ND |
| 8 | RIGHT DROP RESET | Q8 | YEL-VIO | J10-P9/10 | 50v DC | BRN-GRY | J8-P9 | 23-800 | 090-5001-ND |
| 9 | LEFT BUMPER | Q9 | YEL-VIO | J10-P9/10 | 50v DC | BLU-BRN | J9-P1 | 26-1200 | 090-5044-ND |
| 10 | RIGHT BUMPER | Q10 | YEL-VIO | J10-P9/10 | 50v DC | BLU-RED | J9-P2 | 26-1200 | 090-5044-ND |
| 11 | BOTTOM BUMPER | Q11 | YEL-VIO | J10-P9/10 | 50v DC | BLU-ORG | J9-P4 | 26-1200 | 090-5044-ND |
| 12 | JAIL UP | Q12 | YEL-VIO | J10-P9/10 | 50v DC | BLU-YEL | J9-P5 | 26-1200 | 090-5044-ND |
| 13 | UPPER PF LEFT FLIPPER | Q13 | GRY-YEL-3A Fuse-RED-YEL | J10-P6/7 | 50v DC | BLU-GRN | J9-P6 | 23-1100 | 090-5030-ND |
| 14 | UPPER PF RIGHT FLIPPER | Q14 | BLU-YEL-3A Fuse-RED-YEL | J10-P6/7 | 50v DC | BLU-BLK | J9-P7 | 23-1100 | 090-5030-ND |
| 15 | LEFT FLIPPER (50v RED/YEL) | Q15 | GRY-YEL-3A Fuse-RED-YEL | J10-P6/7 | 50v DC | ORG-GRY | J9-P8 | 22-1080 | 090-5032-ND |
| 16 | RIGHT FLIPPER (50v RED/YEL) | Q16 | BLU-YEL-3A Fuse-RED-YEL | J10-P6/7 | 50v DC | ORG-VIO | J9-P9 | 22-1080 | 090-5032-ND |
| 17 | LEFT SLINGSHOT | Q17 | BROWN | J7-P1 | 20v DC | VIO-BRN | J7-P2 | 23-800 | 090-5001-ND |
| 18 | RIGHT SLINGSHOT | Q18 | BROWN | J7-P1 | 20v DC | VIO-RED | J7-P3 | 23-800 | 090-5001-ND |
| 19 | JAIL LATCH [MINI-COIL] | Q19 | BROWN | J7-P1 | 20v DC | VIO-ORG | J7-P4 | 27-880 | 090-5072-05 |
| 20 | LEFT RAMP UP POST | Q20 | BROWN | J7-P1 | 20v DC | VIO-YEL | J7-P6 | 25-1240 | 090-5034-ND |
| 21 | BUMPER EJECT | Q21 | YEL-VIO | J10-P9/10 | 50v DC | WHITE [printed directional/slash glyph] VIO-GRN | J7-P7 | 26-1200 | 090-5044-ND |
| 22 | FLASH: LEFT SLINGSHOT | Q22 | ORANGE | J6-P10 | 20v DC | VIO-BLU | J7-P8 | #89 Bulb | 165-5000-89 |
| 23 | FLASH: RIGHT SLINGSHOT | Q23 | ORANGE | J6-P10 | 20v DC | VIO-BLK | J7-P9 | #89 Bulb | 165-5000-89 |
| 24 | OPTIONAL COIL | Q24 | RED | J16-P4>8 | 5v DC | VIO-GRY | J7-P10 | Opt. 5v | — (printed blank) |
| 25 | FLASH: LEFT SPINNER | Q25 | ORANGE | J6-P10 | 20v DC | BLK-BRN | J6-P1 | #89 Bulb | 165-5000-89 |
| 26 | FLASH: BACKPANEL #1 (L) | Q26 | ORANGE | J6-P10 | 20v DC | BLK-RED | J6-P2 | #89 Bulb | 165-5000-89 |
| 27 | FLASH: BACKPANEL #2 | Q27 | ORANGE | J6-P10 | 20v DC | BLK-ORG | J6-P3 | #89 Bulb | 165-5000-89 |
| 28 | FLASH: BACKPANEL #3 | Q28 | ORANGE | J6-P10 | 20v DC | BLK-YEL | J6-P4 | #89 Bulb | 165-5000-89 |
| 29 | FLASH: BACKPANEL #4 | Q29 | ORANGE | J6-P10 | 20v DC | BLK-GRN | J6-P5 | #89 Bulb | 165-5000-89 |
| 30 | FLASH: BACKPANEL #5 (R) | Q30 | ORANGE | J6-P10 | 20v DC | BLK-BLU | J6-P6 | #89 Bulb | 165-5000-89 |
| 31 | FLASH: RIGHT VUK | Q31 | ORANGE | J6-P10 | 20v DC | BLK-VIO | J6-P7 | #89 Bulb | 165-5000-89 |
| 32 | RIGHT RAMP DOWN POST | Q32 | BROWN | J7-P1 | 20v DC | BLK-GRY | J6-P8 | 26-1200 | 090-5044-ND |

Literal source note: “In Test Flash Lamps Menu (‘Flash’ Icon), Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q22-Q23 & Q25-Q31).”

## General illumination circuit

Evidence: PDF one-based page **125**, printed locator **Section 5, Chapter 1, p. 99**, heading **“General Illumination Circuit”**. Render: `terra-renders/wpt-p125-full.webp`, SHA-256 `64382b0bae99ea71f19203463487e368be2cb9542e29c1a2125c765b403450c4`, derived by the supplied render tool; **candidate / reviewed false**. This is a full wiring/underside map—not coordinates.

| Circuit | Literal connection | Printed location | Printed quantity / bulb |
| --- | --- | --- | --- |
| 1 | J15-P6 to J15-P1 (Fuse F1) = BRN-WHT to WHT-BRN | Upper Playfield | 6 ea. #44 Bulb |
| 2 | J15-P7 to J15-P2 (Fuse F2) = YELLOW to WHT-YEL | Left Edge & Lwr. Rt. Flip | 12 ea. #44 Bulb |
| 3 | J15-P8 to J15-P3 (Fuse F3) = GREEN to WHT-GRN | Backpanel + US Coin Door X2 (Euro X3) | 9* #44 Bulb |
| 4 | J15-P9 to J15-P4 (Fuse F4) = VIOLET to WHT-VIO | Lower Right Playfield | 6 ea. #44 Bulb |

The J15 strip prints: P1 YEL; P2 WHT-YEL; P3 WHT-GRN; P4 WHT-VIO; P5 KEY; P6 BRN-WHT; P7 YELLOW; P8 GREEN; P9 VIOLET. The source footnote for the asterisk is “G.I. Bulb quantities may change during production.”

## Related physical wiring sheets (not transcribed into invented address values)

All remain candidate/manual evidence: PDF p123 / printed Section 5 Chapter 1 p97 (I/O Power Driver detailed wiring); PDF p124 / p98 (board layout and connector pins); p126 / p100 (playfield switch wiring); p127 / p101 (playfield lamp wiring); p128 / p102 (terminal strips); p129 / p103 (four-flipper circuit); p132 / p106 (cabinet); p168 / Section 5 Chapter 4 p142 (Q21 50V Step-Up Driver PCB 520-5254-00). Corresponding visually inspected derived renders are under `terra-renders/`; hashes are recorded in `terra-proposed-manual-source-record.json`.

## Location / mechanism maps inspected (no coordinates created)

Each following render is Stern Pinball / NOASSERTION, derived by `render_excerpt_image.py`, visually checked by the transcriber, and **candidate / reviewed false**. The map legend uses white = above playfield, black = below playfield, gray = cabinet/back panel; those source categories were not converted to normalized x/y geometry.

| PDF one-based page / printed locator | Render / SHA-256 | Manual map scope |
| --- | --- | --- |
| 7 / DR. 5 | `wpt-p007-full.webp` / `760a837ad6d60a260b9524722bfaff9a805aac98ed68cb3b638c1d702d775d65` | Switch Locations; typical switch wiring and dedicated-switch diagram |
| 9 / DR. 7 | `wpt-p009-full.webp` / `da16d4302acbd2e5ae47fe2605399eaaab981c3dcdb38a5d3ae1bf6e1aabf1f4` | Lamp Locations |
| 11 / DR. 9 | `wpt-p011-full.webp` / `46010597a9d4d76c19c897e1818b04c552e3a7f1349741ac791fa6a056584d39` | Coil & Flash Lamp Locations |

These maps support manual candidates such as the source’s physical categories and displayed switch/device labels only. They do not establish script I/O semantics or emulator topology.
