# Skateball — adjustments, switch construction and assembly parts

Source: Bally Game #1210 installation manual, PDF 9–12/23–24 (printed 5–8/19–20), SHA-256 `0758b23c3d33b28c06be006ba768151075b0f31ae9cddad6739e6c5ab7513a1a`. Primary curator visually checked the complete game-feature option table and parts list against rendered pages. Table punctuation and whitespace are normalized; source wording is retained in the function columns. Summarized prose is labelled separately. No setting is invented for an omitted switch.

PDF 9 prose: the MPU A4 in the backbox carries four eight-switch packages S1–8, S9–16, S17–24, S25–32. Coin chute 1/hinge side usesS1–S5; chute 3/right usesS9–S13; chute 2/center usesS17–S20, with all four OFF giving the chute 1 settings. The numerical coin-ratio tables are not used to assert any ratio in this definition.

PDF 10 complete maximum-credit/balls/match/credit-display tables:

| Maximum credits | S26 | S25 |
|---:|---|---|
|10|OFF|OFF|
|15|OFF|ON|
|25|ON|OFF|
|40|ON|ON|

| Balls/game | S32 | S31 |
|---:|---|---|
|5|OFF|ON|
|4|ON|OFF|
|3|OFF|OFF|
|2|ON|ON|

| Feature | Enabled/shown | Disabled/hidden |
|---|---|---|
|MATCH|S28 ON|S28 OFF|
|CREDITS DISPLAYED|S27 ON|S27 OFF|

PDF 11 complete GAME FEATURE OPTIONS table (ON rows are circled on this scan; a hand-drawn circle is not treated as an untouched factory default):

| Adjustment | Liberal | Liberal description | Conservative | Conservative description |
|---|---|---|---|---|
|Top drop targets X lite|SW.8 ON|Not making lit X will come on for next ball.|SW.8 OFF|Not making lit X will not come on for next ball.|
|Center drop targets arrow lite|SW.14 ON|Not making lit arrow will come on for next ball.|SW.14 OFF|Not making lit arrow will not come on for next ball.|
|Top drop targets arrow lite|SW.15 ON|Not making arrow will come on for next ball.|SW.15 OFF|Not making lit arrow will not come on for next ball.|
|50,000 and saucer extra ball lite|SW.16 ON|50,000 and extra ball lite together.|SW.16 OFF|50,000 then extra ball will lite.|
|Bonus2X thru5X lite|SW.23 ON|Any lite lit will come on for next ball.|SW.23 OFF|Any lite lit will not come on for next ball.|
|Saucer extra ball & right out special lite|SW.24 ON|Saucer extra ball and right out special lite together.|SW.24 OFF|Saucer extra ball then right special will lite.|
|Saucer extra ball lite|SW.30 ON|Liting A-B and S-K-A-T-E will lite saucer extra ball.|SW.30 OFF|Liting A-B and S-K-A-T-E will not lite saucer extra ball.|
|Drop targets bonus advance (both3 bank targets)|SW.7 ON|Hitting any drop target advances bonus1 step.|SW.7 OFF|Hitting drop targets does not advance bonus.|

PDF 9–12 assign no DIP function toS6, S21, S22, S29. PDF 12 describes self-test menu positions 16–19, selected with the replay/credit button; these are stored adjustments, not additional DIP switches. PDF 11 sound-option rows00 associated chimes with feature background;01 associated noises without background;02 most scoring chime effect;03 most scoring noise effect with background. PDF 10 high-score-to-date menu19 has00 no award,01 one credit,02 two credits,03 three credits. PDF 12 score thresholds01–03 can be set00 (off) or10,000–9,999,000 in10,000 steps, and high-score-to-date 04 uses00–9,990,000 with00 not disabling that feature.

PDF 23 construction prose: switch assemblies use leaf springs and contacts; normal adjustment is a1/16 inch open gap and.010 inch closed overtravel/wipe. This is contact-construction evidence, distinct from the emulator's public active-state convention.

PDF 24 complete miscellaneous and assembly-coil tables:

| Printed item | Part number |
|---|---|
|Transformer (Domestic or Export)|E-122-125|
|Bulbs,#44|E-125-22|
|Fuse,1 Amp.3AG Slow Blow (Playfield Solenoid Protection)|E-133-44|
|Coin Lockout|FO-36-7000|
|Flipper(4)|AQ-25-500/34-4500|
|Knocker|AR-26-1200|
|Outhole Kicker|AN-26-1200|
|Thumper-Bumper(3)|AN-26-1200|
|Sling-Shot(2)|AO-26-1200|
|Drop Target(3)|NO-26-1900|
|Saucer|AO-27-1300|
|Up Kicker|NO-26-1900|
|Down Kicker|AO-26-1200|

Complete module region: Lamp Driver A5 AS-2518-23; Display Driver A1 (1 Used) AS-2518-21; Display Driver A1 (4 Used) AS-2518-58; Solenoid Driver/Voltage Regulator A3 AS-2518-22; MPU A4 AS-2962-22; Transformer & Rectifier A2 AS-2877-1; Rectifier Board(part ofA2) AS-2518-18; Sound AS-3022-11. The generic Up Kicker/Down Kicker lines fit no additional branch on the game's own A3 or A6 wiring, and do not establish another mechanism.
