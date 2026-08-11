# Laser War technical-chart special-solenoid evidence

Human transcription checked cell-by-cell against a retained 300 dpi render of the 2021 Inkochnito community technical chart. Blank printed cells are recorded as `[blank]`; capitalization and abbreviated wire colors follow the chart.

## Switched, CPU Controlled Auxiliary & Constant Power Solenoids - printed rows 17-22

| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil or Flash Type |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | Blue Pop Bumper | Q8 | CPU | Blu-Orn | CN19-3 | Red | PS CN3-6 | 32V | 23-800 |
| 18 | Yellow Pop Bumper | Q9 | CPU | Blu-Red | CN19-4 | Red | PS CN3-6 | 32V | 23-800 |
| 19 | Left Slingshot | Q10 | CPU | Blu-Yel | CN19-6 | Red | PS CN3-6 | 32V | 23-800 |
| 20 | Red Pop Bumper | Q11 | CPU | Blu-Brn | CN19-7 | Red | PS CN3-6 | 32V | 23-800 |
| 21 | Right Slingshot | Q12 | CPU | Blu-Grn | CN19-8 | Red | PS CN3-6 | 32V | 23-800 |
| 22 | Not Used | Q13 | CPU | Blu-Blk | CN19-9 | [blank] | [blank] | [blank] | [blank] |

This is a literal physical-circuit transcription. The chart explicitly labels the first column `Coil No.` and numbers the six circuits 17-22, so the definition uses those numbers as its conflicted working public addresses. The chart does not print SP1-SP6 identities. Interpreting pinned `s11.c`'s shared PIA handler comments and applying Data East's `ssSolNo` permutation produces a different physical-device order at public 17-22. That disagreement remains unresolved until a LibPinMAME trace observes the public pulses.

Source document SHA-256: `30a1def10178a2cf7e753046ed44f07d01075a6333791669e4fe0c4e165ddfe7`
