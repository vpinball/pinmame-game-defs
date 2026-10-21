# Joker Poker technical chart: complete factual tables

Source: inkochnito, hosted by Pinball Rebel,
`Gottlieb_Joker_Poker_Tech_Chart.pdf`, one page, SHA-256
`7a5391c0dc0e373da1fc6252750a76aad7fe0490f1f25f7b879da9503f2601b0`.
Transcribed by GPT Sol by reading the rendered page, 2026-10-21; reviewed against
that render. This is a secondary chart, not a retained Gottlieb factory schematic.
Connector/wire claims remain candidates until its overlapping columns can be
compared with the primary. Quotes and wire spelling below follow the page;
whitespace and curly/straight quote typography are normalized. `[blank]` denotes
a printed empty cell. Merged header cells are repeated explicitly in this linear
transcription; repeated values in the switch rows are not independently printed.

## Fuse List (all rows)

| Wire in | Value | Wire out | description | location |
| --- | --- | --- | --- | --- |
| Orn | 5 Amp Slo-Blo | Blu | 115V Primary Fuse | Bottom Board |
| [blank; preceding merged Orn cell] | 2½ Amp Slo-Blo | [blank; preceding merged Blu cell] | 230V Primary Fuse | Bottom Board |
| Wht-Yel | ¼ Amp Slo-Blo | Blu-Wht-Red | Displays 69VAC | Bottom Board |
| Yel | 5 Amp Slo-Blo | Red-Wht | Coils 25VAC | Bottom Board |
| Blu-Blk | 5 Amp Slo-Blo | Orn-Blk | Controlled lamps 8VAC | Bottom Board |
| Yel-Red | 7½ Amp | Brn-Red | G.I. Playfield (via Tilt Relay) & Coin Chute 6VAC | Bottom Board |
| Yel-Red | 7½ Amp | Wht-Red | G.I. Name & Scene Lights 6VAC | Bottom Board |
| [blank] | [blank] | [blank] | [blank] | [blank] |
| Red | 2 Amp Slo-Blo | Wht-Blk | "A" Target Bank Reset | Playfield |
| Red | 1 Amp Slo-Blo | Orn-Blk | "Q" Target Bank Reset | Playfield |
| Red | 1 Amp Slo-Blo | Brn-Red | "10-J" Target Bank Reset | Playfield |
| Red | ½ Amp Slo-Blo | Blu-Orn | Out Hole | Playfield |
| Brn-Blk | 2 Amp Slo-Blo | Grn-Yel | "K" Target Bank Reset | Playfield |

## Switch Matrix (all 40 cells, all row/column headers)

| Return header | Connector | Wire |
| --- | --- | --- |
| RETURN 0 | A1J7-12 & A1J6-3 | Yellow |
| RETURN 1 | A1J7-13 | Blue-White |
| RETURN 2 | A1J7-14 | Orange-White |
| RETURN 3 | A1J7-17 | Brown-White |
| RETURN 4 | A1J7-16 | Green-White |
| RETURN 5 | A1J7-15 | Purple-White |
| RETURN 6 | A1J7-11 | Yellow-White |
| RETURN 7 | A1J7-10 | Yellow-Black |

| Strobe header | Connector(s) | Wire |
| --- | --- | --- |
| STROBE 0 | A1J7-2; A1J6-8 | Blue |
| STROBE 1 | A1J7-3; A1J6-4 | Orange |
| STROBE 2 | A1J7-4; A1J6-5 | Brown |
| STROBE 3 | A1J7-7; A1J6-6 | Green |
| STROBE 4 | A1J7-6; [blank] | Purple |

| Printed switch | Description | Cell wire |
| --- | --- | --- |
| SW.00 | Test Button | Blue-White |
| SW.10 | Pop Bumper Switches (2) | Blue-Black |
| SW.20 | Extra Ball Target | Yellow-Green |
| SW.30 | Special Rollover | Blue-White-Red |
| SW.40 | 10 Point Contacts (11) | Slate-White-Red |
| SW.50 | "A" Drop Target | Orange-Black |
| SW.60 | Not Used | [blank] |
| SW.70 | Not Used | [blank] |
| SW.01 | #1 Coin Chute | Orange-White |
| SW.11 | "A" Rollover (2) | Yellow-Black |
| SW.21 | "10" Drop Target | Orange-Green |
| SW.31 | "Q" Drop Target | White-Blue |
| SW.41 | "K" Drop Target | Maroon |
| SW.51 | "A" Drop Target | Brown-Black |
| SW.61 | Not Used | [blank] |
| SW.71 | Not Used | [blank] |
| SW.02 | #2 Coin Chute | Brown-White |
| SW.12 | "B" Rollover (3) | Orange-White |
| SW.22 | "J" Drop Target | Slate-Green |
| SW.32 | "Q" Drop Target | White-Orange |
| SW.42 | "K" Drop Target | Maroon-White |
| SW.52 | Joker Drop Target | Green-Black |
| SW.62 | Not Used | [blank] |
| SW.72 | Not Used | [blank] |
| SW.03 | Replay Button | Green-White |
| SW.13 | "C" Rollover (2) | Slate-White |
| SW.23 | "J" Drop Target | Slate-Green |
| SW.33 | "Q" Drop Target | White-Slate |
| SW.43 | "K" Drop Target | Maroon-Green |
| SW.53 | "A" Drop Target | Slate-Black |
| SW.63 | Not Used | [blank] |
| SW.73 | Not Used | [blank] |
| SW.04 | Tilt | Purple-White |
| SW.14 | Not Used | [blank] |
| SW.24 | Not Used | [blank] |
| SW.34 | Not Used | [blank] |
| SW.44 | "K" Drop Target | Maroon-Yellow |
| SW.54 | "A" Drop Target | Yellow-Black |
| SW.64 | Not Used | [blank] |
| SW.74 | Not Used | [blank] |

No STROBE 5 region, special-input row, DIP descriptions or switch construction
symbols are printed. Omission is not a printed Not Used claim.

## Lamps and solenoids (complete table)

| transistor | connector | code | description | wire color | transistor type |
| --- | --- | --- | --- | --- | --- |
| Q01 | J5-18 | L01 | Game Over Relay | Wht-Blu | MPS-U45 |
| Q Relay | [blank] | [blank] | Match / Game Over Light | Yel-Blk | [blank] |
| Q Relay | [blank] | [blank] | Ball in Play | Pur-Red | [blank] |
| Q02 | J5-19 | L02 | Tilt Relay | Wht-Orn | MPS-U45 |
| T Relay | [blank] | [blank] | Tilt Light | Wht-Brn-Blk | [blank] |
| Q03 | J5-17 | L03 | High Game to Date | Wht-Brn | MPS-U45 |
| Q04 | J5-15 | L04 | Same Player Shoot Again | Wht-Grn | MPS-U45 |
| Q05 | J5-13 | L05 | Not Used | Wht-Pur | MPS-A13 |
| Q06 | J5-14 | L06 | Not Used | Wht-Yel | MPS-A13 |
| Q07 | J5-12 | L07 | Not Used | Blu-Wht-Red | MPS-A13 |
| Q08 | J5-11 | L08 | Aces Bonus | Orn-Wht-Red | MPS-A13 |
| Q09 | J5-9 | L09 | Queens Bonus | Brn-Wht-Red | MPS-A13 |
| Q10 | J5-10 | L10 | Kings Bonus | Grn-Wht-Red | MPS-A13 |
| Q11 | J5-8 | L11 | Jacks Bonus | Pur-Wht-Red | MPS-A13 |
| Q12 | J5-7 | L12 | Tens Bonus | Yel-Wht-Red | MPS-A13 |
| Q13 | J5-5 | L13 | 4,000 Bonus | Blu-Wht-Blk | MPS-A13 |
| Q14 | J5-6 | L14 | 5,000 Bonus | Orn-Wht-Blk | MPS-A13 |
| Q15 | J5-4 | L15 | 3,000 Bonus | Brn-Wht-Blk | MPS-A13 |
| Q16 | J5-3 | L16 | 2,000 Bonus | Grn-Wht-Blk | MPS-A13 |
| Q17 | J5-1 | L17 | "K" Drop Target Bank Reset | Pur-Wht-Blk | MPS-A13 |
| Q18 | J5-2 | L18 | 1000 Bonus | Yel-Wht-Blk | MPS-A13 |
| Q19 | J3-20 | L19 | Special Rollover | Wht-Blu-Red | MPS-A13 |
| Q20 | J3-18 | L20 | Extra Ball Target | Wht-Orn-Red | MPS-A13 |
| Q21 | J3-16 | L21 | Top "B" Rollover | Wht-Brn-Red | MPS-A13 |
| Q22 | J3-17 | L22 | Top "C" Rollover | Wht-Grn-Red | MPS-A13 |
| Q23 | J3-15 | L23 | Top "A" Rollover | Wht-Pur-Red | MPS-A13 |
| Q24 | J3-14 | L24 | Bottom "C" Rollover | Wht-Yel-Red | MPS-A13 |
| Q33 | J3-12 | L25 | Left Bottom "B" Rollover | Wht-Blu-Blk | MPS-A13 |
| Q34 | J3-13 | L26 | Right Bottom "B" Rollover | Wht-Orn-Blk | MPS-A13 |
| Q35 | J3-11 | L27 | Bottom "A" Rollover | Wht-Brn-Blk | MPS-A13 |
| Q36 | J3-9 | L28 | 5x Bonus | Wht-Grn-Blk | MPS-A13 |
| Q37 | J3-7 | L29 | Not Used | Wht-Pur-Blk | MPS-A13 |
| Q38 | J3-8 | L30 | Not Used | Wht-Yel-Blk | MPS-A13 |
| Q39 | J3-6 | L31 | Not Used | Blu-Wht-Wht | MPS-A13 |
| Q40 | J3-5 | L32 | Not Used | Orn-Wht-Wht | MPS-A13 |
| Q41 | J3-4 | L33 | Not Used | Brn-Wht-Wht | MPS-A13 |
| Q42 | J3-3 | L34 | Not Used | Grn-Wht-Wht | MPS-A13 |
| Q43 | J3-2 | L35 | Not Used | Pur-Wht-Wht | MPS-A13 |
| Q44 | J3-1 | L36 | Not Used | Yel-Wht-Wht | MPS-A13 |
| Q32 | J4-6 | Solenoid 1 | Outhole | Blu-Red | 2N6043 |
| Q25 | J2-1 | Solenoid 2 | Knocker | Orn-Red | 2N6043 |
| Q26 | J2-2 | Solenoid 3 | 10's chime | Orn-Blk | 2N6043 |
| Q27 | J2-3 | Solenoid 4 | 100's chime | Grn-Red | 2N6043 |
| Q28 | J2-4 | Solenoid 5 | 1000's chime | Pur-Red | 2N6043 |
| Q31 | J4-5 | Solenoid 6 | "10-J" Drop Target Bank Reset | Yel-Red | 2N6043 |
| Q30 | J4-4 | Solenoid 7 | "Q" Drop Target Bank Reset | Blu-Blk | 2N6043 |
| Q29 - Q45 | J4-2 | Solenoid 8 | "A" Drop Target Bank Reset | Orn-Blk | MPS-U45 - 2N3055 |

## Solenoids (complete table)

| Code | Solenoid description | Solenoid Type | Power Wire | Fuse | Transfer Wire 1 | Coil Wire Color | Transfer Wire 2 | Connector | Driver Transistor | Transistor Type | Coil Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L01 | Game Over Relay | Controlled | Red | [blank] | [blank] | Wht-Blu | [blank] | A3J5-18 | Q01 | MPS-U45 | A-16890 |
| L02 | Tilt Relay | Controlled | Red | [blank] | [blank] | Wht-Orn | [blank] | A3J5-19 | Q02 | MPS-U45 | A-16890 |
| L17 | "K" Drop Target Bank Reset | Controlled | Brn-Blk | 2 Amp Slo-Blo | Grn-Yel | Pur-Wht-Blk | [blank] | A3J5-1 | Q17 - UPT | MPS-U45 - 2N5875 | A-18318 |
| Sol. 1 | Outhole | Controlled | Red | ½ Amp Slo-Blo | ? | Blu-Red | [blank] | A3J4-6 | Q32 | 2N6043 | A-5195 |
| Sol. 2 | Knocker | Controlled | Red | [blank] | [blank] | Orn-Red | [blank] | A3J2-1 | Q25 | 2N6043 | A-5195 |
| Sol. 3 | 10's chime | Controlled | Red | [blank] | [blank] | Orn-Blk | [blank] | A3J2-2 | Q26 | 2N6043 | A-17876 |
| Sol. 4 | 100's chime | Controlled | Red | [blank] | [blank] | Grn-Red | [blank] | A3J2-3 | Q27 | 2N6043 | A-17876 |
| Sol. 5 | 1000's chime | Controlled | Red | [blank] | [blank] | Pur-Red | [blank] | A3J2-4 | Q28 | 2N6043 | A-17876 |
| Sol. 6 | "10-J" Drop Target Bank Reset | Controlled | Red | 1 Amp Slo-Blo | Brn-Red | Yel-Red | [blank] | A3J4-5 | Q31 | 2N6043 | A-18102 |
| Sol. 7 | "Q" Drop Target Bank Reset | Controlled | Red | 1 Amp Slo-Blo | Orn-Blk | Blu-Blk | [blank] | A3J4-4 | Q30 | 2N6043 | A-18102 |
| Sol. 8 | "A" Drop Target Bank Reset | Controlled | Red | 2 Amp Slo-Blo | Wht-Blk | Orn-Blk | [blank] | A3J4-2 | Q29 - Q45 | MPS-U45 - 2N3055 | A-17891 |
| [blank] | Left Pop Bumper | Directly | Brn-Blk | [blank] | [blank] | [blank] | [blank] | [blank] | Switch | [blank] | A-1496 |
| [blank] | Right Pop Bumper | Directly | Brn-Blk | [blank] | [blank] | [blank] | [blank] | [blank] | Switch | [blank] | A-1496 |
| [blank] | Kicking Rubber | Directly | Brn-Blk | [blank] | [blank] | [blank] | [blank] | [blank] | Switch | [blank] | A-5194 |
| [blank] | Coin Lockout | Directly | Red | [blank] | [blank] | [blank] | [blank] | A6J1-11 | Directly wired to ground | [blank] | A-16890 |
| [blank] | Left Flipper | Directly | Brn-Blk | [blank] | [blank] | Grn-Blk | [blank] | A6J5-4 | Button | [blank] | A-17875 |
| [blank] | Right Flipper | Directly | Brn-Blk | [blank] | [blank] | Pur-Blk | [blank] | A6J5-5 | Button | [blank] | A-17875 |
| [blank] | Top Flipper | Directly | Brn-Blk | [blank] | [blank] | Pur-Blk | [blank] | A6J5-5 | Button | [blank] | A-17875 |

Footnotes: 2N6043 can be replaced with a TIP 102. UPT = Under Playfield Transistor.
The L17 transistor type differs between the two printed tables (MPS-A13 versus
MPS-U45 - 2N5875); preserve both readings pending primary wiring.
