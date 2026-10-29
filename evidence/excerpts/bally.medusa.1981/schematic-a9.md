# Medusa auxiliary lamp board and playfield harness

Source: `Bally_1981_Medusa_Schematics_paginated.pdf`, SHA256
`a4a8d3c6717cde7afc8015e556400ddec19c420bc1f3990977c8514a872b93b6`,
PDF7 W-1207-10 and PDF3 W-1255-1. Transcription by GPT Terra, all28 output
rows visually checked by primary GPT Sol against native PDF7 render. Entire
output table follows. Table values with duplicate panel numbers are literal.

## A9 auxiliary lamp driver

The following rows were visually checked against page 07. Public addresses are **derived candidates** from `by35_lampStrobe` and the drawn decoder input wiring; the source’s printed labels, pin numbers and wire codes are transcribed separately. `S7` is printed `N/U` for each decoder. Do not infer physical lamp quantities from these rows.

| Public candidate | Decoder output | SCR | Connector | Printed wire code | Printed function |
| ---: | --- | --- | --- | ---: | --- |
| 65 | U2 S0 | Q1 | J2-7 | 10 | #1 LEFT TOP OF PANEL |
| 66 | U2 S1 | Q2 | J2-4 | 15 | #5 TOP OF PANEL |
| 67 | U2 S2 | Q3 | J2-8 | 51 | #9 TOP OF PANEL |
| 68 | U2 S3 | Q4 | J2-10 | 80 | #13 TOP OF PANEL |
| 69 | U2 S4 | Q5 | J2-9 | 54 | #17 TOP OF PANEL |
| 70 | U2 S5 | Q6 | J2-6 | 45 | #1 SHOOTER LANE ROLLOVER BUTTON & GORGON BONUS |
| 71 | U2 S6 | Q7 | J2-5 | 60 | #5 SHOOTER LANE ROLLOVER BUTTON & GORGON BONUS |
| 81 | U3 S0 | Q8 | J2-14 | 12 | #2 TOP OF PANEL |
| 82 | U3 S1 | Q9 | J2-11 | 18 | #6 TOP OF PANEL |
| 83 | U3 S2 | Q10 | J2-15 | 52 | #10 TOP OF PANEL |
| 84 | U3 S3 | Q11 | J2-18 | 57 | **#4 TOP OF PANEL**, as printed |
| 85 | U3 S4 | Q12 | J2-17 | 43 | #18 TOP OF PANEL |
| 86 | U3 S5 | Q13 | J2-13 | 40 | #2 SHOOTER LANE ROLLOVER BUTTON & GORGON BONUS |
| 87 | U3 S6 | Q14 | J2-12 | 62 | READY SHOOTER LANE |
| 97 | U4 S0 | Q15 | J3-8 | 13 | #3 TOP OF PANEL |
| 98 | U4 S1 | Q16 | J3-3 | 20 | #7 TOP OF PANEL |
| 99 | U4 S2 | Q17 | J3-9 | 53 | #11 TOP OF PANEL |
| 100 | U4 S3 | Q18 | J3-11 | 70 | **#3 TOP OF PANEL**, as printed |
| 101 | U4 S4 | Q19 | J3-10 | 25 | #19 TOP OF PANEL |
| 102 | U4 S5 | Q20 | J3-7 | 82 | #3 SHOOTER LANE ROLLOVER BUTTON & GORGON BONUS |
| 103 | U4 S6 | Q21 | J3-4 | 95 | AIM SHOOTER LANE |
| 113 | U5 S0 | Q22 | J3-15 | 14 | #4 TOP OF PANEL |
| 114 | U5 S1 | Q23 | J3-12 | 21 | #8 TOP OF PANEL |
| 115 | U5 S2 | Q24 | J3-16 | 56 | #12 TOP OF PANEL |
| 116 | U5 S3 | Q25 | J3-18 | 72 | #16 TOP OF PANEL |
| 117 | U5 S4 | Q26 | J3-17 | 23 | #20 RIGHT TOP OF PANEL |
| 118 | U5 S5 | Q27 | J3-14 | 27 | #4 SHOOTER LANE ROLLOVER BUTTON & GORGON BONUS |
| 119 | U5 S6 | Q28 | J3-13 | 96 | FIRE SHOOTER LANE |

Other printed entries: J2-1 and J2-2 `N/U`, J2-3 `KEY`, J2-16 `N/U`; J3-1 `N/U`, J3-2 `KEY`. On the board drawing J3-5, -6, -19 and -20 are `GND`; the separate harness drawing marks those four positions `N/U`. Preserve both contexts.

**Unresolved:** Q11 duplicates Q22’s printed `#4` panel label, and Q18 duplicates Q15’s printed `#3` label. The sheet does not by itself establish corrected identities. The A9 circuit draws only AD0–AD2 into the address latch; the treatment of addresses with the fourth address bit set needs separate analysis before declaring those public positions unused or aliases.

## Primary checks and input connector

On the actual A9 drawing U1 D3 is tied to ground and only AD0-AD2 are latched;
each MC14028B has its D input driven by PD0-PD3 and S7 unconnected. This
establishes28 physical SCR circuits and four unloaded decoder outputs; it does
not establish meaningful emulator state for the extra public slots.

| J1 pin | Literal function |
| --- | --- |
| 1 | AD1 |
| 2 | AD0 |
| 3 | LAMP STROBE |
| 4 | AD2 |
| 5 | N/U |
| 6 | KEY |
| 7 | PD1 |
| 8 | PD0 |
| 9 | PD2 |
| 10 | PD3 |
| 11 | +5 |
| 12 | N/U |
| 13 | GND |
| 14 | GND |
| 15 | GND |

The complete PDF3 harness agrees with the28 output connector/wire rows above,
except A9J2-18 explicitly reads `#14 TOP OF PANEL`, settling PDF7's `#4`.
A9J3-11 still reads `#3 TOP OF PANEL` on PDF3, duplicating A9J3-8. The retained
script places public100 at Olympus bar position15, but that runtime assignment
does not independently prove which physical socket the duplicated label denotes.
PDF3 draws paired lamp symbols on the five SHOOTER LANE ROLLOVER BUTTON &
GORGON BONUS circuits. Do not conflate their two emitters. It draws one symbol
for each of the20 top-panel channels and each READY/AIM/FIRE circuit.
The top bar's21st channel is separately driven by A5J3-14 (public60).
