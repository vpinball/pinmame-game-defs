# World Poker Tour script and PinMAME source excerpt

Retained known-working script: `World Poker Tour (Stern 2006) v.2.3.1.vbs`, pinned `vpxtable_scripts` revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d44738c5fa4693a8b096f226399f3ea2f81c985a1e780c33d012acf7d2bc390a`. Extracted 2018 table script SHA-256 `1b5b833d6dd2657a52eeed69ad556a7bfa066171cabf2526f1e1aa33daa77f0c`. The alternate retained `World Poker Tour (Stern 2006).vpx` SHA-256 is `92a9720af51c825c9603d9dc78acc2423b7f86c907e1c4a6e92393156a22d9b8`, embedded script SHA-256 `ad1b982910737127e2ed47c7ad50f2a3390b212ae1ca780f8045aa7d8f60a99c`. Its Q13/Q14 upper callbacks are deliberately disabled for SAM fastflips, while `SolLFlipper`/`SolRFlipper` rotate both lower and upper flippers. The known-working and 2018 scripts instead enable separate upper callbacks. Both implementations model four upper/lower physical flippers; disabled callbacks alone do not prove missing hardware. Both tables use the `wpt_140a` ROM and 952×2250 bounds. These are external retained inputs, attributed to their table authors, license NOASSERTION.

| Locator in pinned script | Source assertion, condensed |
| --- | --- |
| 304–307 | Four starting balls are created at `sw18` through `sw21`. |
| 539–546 | Q1 release, Q2 auto-fire, Q3 shooter VUK, Q4 left VUK, Q5/Q6 left half-bank resets, Q7 middle bank reset, Q8 right bank reset. |
| 550–562 | Q12 jail-up; Q13/Q14 upper flippers active; Q15/Q16 lower flippers; Q17/Q18 slings; Q19 jail latch; Q20 left-ramp post; Q21 scoop eject; Q32 right-ramp down-post. |
| 566–574 | Q22/Q23 and Q25–Q31 are flasher callbacks; Q26–Q30 are five separate backpanel calls. |
| 735–767 | Trough SW18–SW21 hold occupancy and release bookkeeping moves balls between seats. |
| 910–911, 1094 | `ScoopTrigger` asserts/relinquishes SW54; a separate `sw54` handler also asserts SW54 and is commented "left ramp opto". This is a script conflict, not proof of two factory sensors on one wire. |
| 2649–2664 | Individual drop target objects map SW4–7, SW10–13, SW33–40. |

Pinned PinMAME source: revision `8371478a7640f1896dcdf565aed340dc5df989ba`; `src/wpc/sam.c` lines 2351–2353 select SAM game data, line 2448 registers WPT with `sammini1_dmd128x32`, two extra lamp columns, and `SAM_GAME_WPT`. Lines 1373–1377 initialise fourteen 7×5 mini DMD blocks. Lines 1388–1398 set GI count one, lamp count `64 + lampcol*8` (80 for WPT), physical solenoid 1–32 and a synthetic game-on 33, with auxiliary capacity 51–66. WPT's game-specific flag activates the mini LED matrix board, not an auxiliary solenoid board. `src/wpc/core.c` lines 2117–2163 apply the switch inversion mask inside the controller read/write path.

Curator review: GPT-6-Sol, 2026-09-30. These locators were checked against the retained files. Public I/O activity and script handlers do not by themselves establish installed sockets, sensor polarity, or the two SW54 physical sites.
