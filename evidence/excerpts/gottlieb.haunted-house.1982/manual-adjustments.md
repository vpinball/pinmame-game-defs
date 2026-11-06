# Haunted House: adjustments and service tests

Original manual SHA-256 `168a1bc2e2198b03154835d45471eb5b3910f1619930c5c3fd48f9b86ad8c21f`. Complete adjustment regions from PDF 13/printed 9, visually transcribed and checked by primary curator. ON/OFF are physical DIP positions, not controller input inversions. Line wrapping and dotted leaders are normalized; handwritten check marks are not defaults.

## V. SOUND/SPEECH BOARD (A6)

The installed Sound/Speech Board is programmed for sounds only. Voice chip U14 is not used; its socket is vacant.

## VI. GAME ADJUSTMENTS — A. CONTROL BOARD SWITCH ADJUSTMENTS

There are 32 switches, in four eight-switch packages S1–S8, S9–S16, S17–S24, S25–S32. Settings are recognized on normal power-up and at the first player's new-game start, not when adding players.

| SWITCHES | COIN CHUTE ADJUSTMENTS |
| --- | --- |
| S1 S2 S3 S4 | Left Chute |
| S5 S6 S7 S8 | Right Chute |
| S9 S10 S11 S12 | Center Chute |

For German games S5–S8 adjust the center chute and S9–S12 the right chute.

| first | second | third | fourth | COINS/CREDITS |
| --- | --- | --- | --- | --- |
| OFF | OFF | OFF | OFF | 1/1 |
| OFF | OFF | OFF | ON | 1/2 |
| OFF | OFF | ON | OFF | 1/3 |
| OFF | OFF | ON | ON | 1/4 |
| OFF | ON | OFF | OFF | 1/5 |
| OFF | ON | OFF | ON | 1/6 |
| OFF | ON | ON | OFF | 1/7 |
| OFF | ON | ON | ON | 1/8 |
| ON | OFF | OFF | OFF | 1/9 |
| ON | OFF | OFF | ON | 2/1* |
| ON | OFF | ON | OFF | 2/2* |
| ON | OFF | ON | ON | 2/3* |
| ON | ON | OFF | OFF | 2/4* |
| ON | ON | OFF | ON | 2/5* |
| ON | ON | ON | OFF | 1/1 AND 2/3 |
| ON | ON | ON | ON | 3/1* |

*NO CREDITS UNTIL LAST COIN IS INSERTED.

| SWITCH | NAME | ON | OFF |
| --- | --- | --- | --- |
| 13 | EXTRA CREDITS | Adds 9 credits to center coin chute setting | No effect |
| 14 | COIN CHUTE CONTROL | Left and Right Chutes Same | Left and Right Chutes Separate |
| 17 | BALLS PER GAME | 3 | 5 |
| 18 | MATCH FEATURE | ON | OFF |
| 19 | REPLAY LIMIT | Limits each player to one replay per game | No replay limit |
| 20 | NOVELTY MODE | Playfield SPECIAL and EXTRA BALL award 50,000 points and 5 knocks; high score, high game to date and match disabled | Normal game mode |
| 21 | GAME MODE | Extra Ball | Replay |
| 22 | PLAYFIELD SPECIAL | Awards Extra Ball | Awards Special |
| 25 | MUST REMAIN ON | ON required | — |
| 26 | MUST REMAIN ON | ON required | — |
| 27 | COIN SWITCH TUNE? | Yes | No |
| 28 | CREDITS DISPLAYED? | Yes | No |
| 29 | TILT PENALTY | Ball in play only | Game over |
| 30 | ATTRACT FEATURES | ON | OFF |
| 31 | MUST REMAIN OFF | — | OFF required |
| 32 | BACKGROUND TONE | ON | OFF |

German games: S13 adds nine credits to the RIGHT chute; S14 controls left and CENTER chutes. S20 overrides S21. With S21 ON, high game to date and match awards are disabled. Dashes in the two fixed-setting rows represent absent descriptions, not printed words.

| 15 | 16 | MAXIMUM CREDITS |
| --- | --- | --- |
| OFF | OFF | 8 |
| OFF | ON | 10 |
| ON | OFF | 15 |
| ON | ON | 25 |

| 23 | 24 | HIGH GAME TO DATE |
| --- | --- | --- |
| OFF | OFF | Not displayed—no award |
| OFF | ON | Displayed—no award |
| ON | OFF | Displayed—awards 2 replays |
| ON | ON | Displayed—awards 3 replays |

## PDF 18/printed 14, self-test flowchart and all notes

PDF 14/printed 10 SOUND ADJUSTMENTS, complete switch-bank region: SB1-1 USED IN SELF-TEST ONLY; SB1-2 NOT USED; SB1-3/SB1-4 attract mode OFF/OFF Disabled, ON/OFF Every 10 Seconds, OFF/ON Every 2 Minutes, ON/ON Every 4 Minutes; SB1-5 ON Background Sound enabled / OFF disabled; SB1-6 NOT USED; SB1-7 NOT USED; SB1-8 NOT USED. The game is programmed for sound only. The cabinet volume potentiometer is accessible through the front door; clockwise increases volume. Board potentiometers are factory calibration controls.

Self/Test enters bookkeeping, credit display 00, player score displays blank. Credit starts Step 16. Self/Test advances between tests. Bookkeeping Steps 1–15: coins left chute; coins right chute/Note 1; coins center chute/Note 2; total plays; total replays; game percentage/Note 3; extra balls; total tilts; total slams; times high game to date beaten; first high score level; second high score level; third high score level; high game to date score; average playing time/Note 4.

Step 16 LAMP DRIVER TEST: Q, T, U relays and coin lockout coil pulse. Controlled lamps plus ball gate and ball release turn on sequentially. This is the literal generic wording; this game's actual lamp-driven loads are enumerated on printed 38.

Step 17 SOLENOID TEST: controlled solenoids pulse while their assigned number appears in status display. Note A assignments: 1 Top Hole; 2 Up Kicker; 5 Drop Target Bank (4), Upper Playfield; 6 Lower Playfield; 8 Knocker; 9 Outhole. Note B: optional mechanical coin counters are not pulsed.

Step 18 SWITCH TEST: matrix switches inspected; 99 if all open, otherwise closed matrix numbers appear. Step 19 DISPLAY TEST: every display digit turned on individually, then numbers 0–9 sequenced. Step 20 MEMORY TEST: defective device part number on Player 1; 99 in status if all OK. Exit: wait 60 seconds, power cycle, open slam switch, or close tilt switch.

Note 1: S14 ON adds Steps 01 and 02 into Step 01. Note 2: German games swap center/right Steps 02/03. Note 3: when Step 06 is reset, Steps 04 and 05 must also be reset. Note 4: when Step 15 is reset, Step 04 must also be reset. Note C: James Bond and later System 80 games display 7641-1 for a bad 2716 game PROM. Note D: German games assign solenoid 4 to center coin chute and solenoid 7 to right coin chute.
