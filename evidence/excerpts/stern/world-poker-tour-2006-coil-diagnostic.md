# World Poker Tour coil diagnostic and wiring reconciliation

Source: fresh-state `wpt_140a` (English V14.0) ROM Single Coil Test, committed scenario `tools/harness-scenarios/stern/world-poker-tour-2006-coil-sweep.json` SHA-256 `9d167f5bc664155d3caa3773faa1d37dafccd83f06dc6da01c049ceedb6a7d0c`; complete external trace `wpt-coil-diagnostic-final-v2-run.json` SHA-256 `f9b0b3b4899309d4ff2d30a704ee6c1663e283667e5fff6c8a732d5679b0ea82`. ROM archive `wpt_140a.zip` SHA-256 `b4f98abae8cecb80a603285357c39688182b90ef376c46c80de5facb4e302463`, LibPinMAME `pinmame64.dll` SHA-256 `ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d`, pinned revision `8371478a7640f1896dcdf565aed340dc5df989ba`. DMD frame images and fresh NVRAM state are retained beside the trace. No ROM or NVRAM bytes are committed.

The sweep was read from the actual DMD images. The menu path was first visually checked in a separate fresh-state run. The harness currently decodes segment text, not DMD text, so 31 in-test Plus actions advance the ROM's selector and the DMD frames identify the selected addresses; the earlier Plus action navigates to the Coil menu icon.

| ROM selector | ROM display name | Factory-chart comparison |
| --- | --- | --- |
| Q1–Q4 | Trough Up-Kicker; Auto Launch; Shooter Lane VUK; Left VUK | Same addresses and names. |
| Q5–Q8 | Lower Left; Upper Left; Middle; Right Drop Reset | Same four independent reset drivers. |
| Q9–Q12 | Left; Right; Bottom Bumper; Jail Up | Same addresses. |
| Q13–Q16 | Upper PF Left; Upper PF Right; Left; Right Flipper | Confirms four-flipper inventory and Q13/Q14 are real test positions. |
| Q17–Q20 | Left; Right Slingshot; Jail Latch; Left Ramp Up Post | Same addresses. |
| Q21 | Pop Bumper Eject | Factory chart says Bumper Eject. ROM prints `BRN / VIO-GRN` at the board; factory p.123 routes this through the separate 50 V step-up board to the pop-eject coil. The board label is not its actual high-side coil supply. |
| Q22–Q23 | Flash: Left; Right Slingshot | Same addresses. |
| Q24 | **Skipped by the ROM Single Coil Test** | Factory chart marks an optional 5 V coil. A separate exploratory coin-credit trace, SHA-256 `485d46110b429f9bd911e3a0216200e0557cd5317c482b0176848bb90987ab69`, observes public solenoid 24 toggle; that does not prove an installed playfield device. |
| Q25–Q31 | Flash: Left Spinner; Backpanel 1–5; Right VUK | Same seven positions and left/right order. |
| Q32 | Right Ramp Down Post | ROM display prints `ORG / BLK-GRY`. Factory board wiring diagram (PDF p.123) shows Q32 on J6-P8 with orange J6-P10 supply; the coil chart (PDF p.10) instead prints brown J7-P1 supply. The board diagram and independent ROM display agree on orange. |
| Next selector | AUX 1: Ticket Advance, #33 | Auxiliary diagnostic capacity, not a factory Q1–Q32 coil and not proof that LibPinMAME public solenoid 33 (synthetic game-on) is a ticket motor. |

Factory evidence reconciled visually: PDF p.10 (DR.8) coil chart, p.118 (Sec.4 Ch.2 p.92) down-post assembly, p.123 (Sec.5 Ch.1 p.97) power-driver wiring, p.129 (Sec.5 Ch.2 p.103) four-flipper circuit, and p.179 (S.A.M. coil selection chart). External p.123 render `wpt-p123-full.webp` SHA-256 `989a45a6d9a359ac3377bb479aaeba8b7135ff7f3c4ea83a277481feda09f0fa`; p.129 render `wpt-p129-full.webp` SHA-256 `d784f4ff7c80a3490e89cd2aa1ffd5d10a5c28229a0c4a454eb03244043243b0`. The p.179 game-specific row and p.129 diagram confirm lower Q15/Q16 use 22-1080 / 090-5032-ND and upper Q13/Q14 use 23-1100 / 090-5030-ND; p.123's generic drawing prints 23-1100 at all four. Page 129 explicitly labels D9/D11/D13/D15 normally open, D10/D12/D14/D16 normally closed, and describes the double-stacked cabinet buttons and 40 ms kick/1 ms per 12 ms hold. Q32's particular assembly sheet instead specifies 25-1240 / 090-5034-ND, while p.10 and p.123 print 26-1200 / 090-5044-ND. The installed Q32 coil remains an unresolved physical-part conflict.

Transcription: GPT-6-Sol curator, visually reviewed 2026-09-30. The diagnostic proves ROM selector labels and an output's displayed board-colour metadata. It cannot prove factory coil gauge, physical bulb count, or socket placement.
