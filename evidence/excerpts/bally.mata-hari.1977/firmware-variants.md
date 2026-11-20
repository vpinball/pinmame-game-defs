# Mata Hari variant documentation and read paths

## Oliver Kaegi

[Oliver's software page](https://pinball4you.ch/okaegi/pro_soft.html) documents the 2732 replacement U6 credit-floor patch (revision 2, 19 September 2004) and separately the PCK-Bally build (revision 7, 1 February 2005). The former uses S17–19 together, displays 02 at power-up and maintains credit 01 after a coin. `mataharb.zip` contains the readme (`info.txt`, SHA-256 `0eaa1a58ec17117f420e1e0757daa068ff786ebcbab889ceff62598ee973ad0c`), with the exact `72132fn.u6` CRC-32 `dad6fdf1` in its footer under the name `7-2132fN.U6`. Its reference to `720-3132.U6` in the introduction and `720-2132.U6` in the Mata Hari row are retained as printed. The program digests identify the actual pair. In the native control, S19 off allowed the machine to spend its sole credit and denied a second player. With S17–19 on it kept 01 and added a second player.

The stand-alone `matatest` program uses the revision-7 `infomata.txt` operator chart supplied with Oliver's release. The original text is retained as `okaegi-infomata.txt`, SHA-256 `63358c72adbe3f8164c689d7b2fa3c3d8f273bd5c1b757bf7db2e0b1e09e18b6`. The publisher archive manifest independently identifies ROM SHA-1s `ced5fcd18009106ac3c7b42e36cdc10ce410eeeb` and `8defbe8e11a75d26daf1351f439dd409f1efc608`, matching the authorized local ROMs and pinned driver. Oliver identifies player displays 1 and 2 as the game and PCK version indicators at boot. His web page also specifies the last-ball high-score display.

| Revision-7 operator setting | Meaning |
| --- | --- |
| S32/S31 | `00` gives 3 balls, `01` gives 5, `10` gives 4 and `11` gives 2 |
| S28 | Match on |
| S27 | Display credits |
| S26 | Author's maximum-credit assignment. Both S25 and S26 on enable the verified one-credit floor. |
| S25 | Author's maximum-credit and free-play assignment. See the program and native results below. |
| S23 | Saucer on first visit starts at 3,000 when off or 3,000 plus 2X when on |

The chart's saucer progression gives 3,000 on each visit. Award steps are 2X, 3X and 5X, followed by bonus countdown and return to the S23 starting point. The A/B ladder lights the left and right lower bumpers at 1K and 2K, then progresses through 3K, 4K, 5K, extra ball and two Special steps. Making A+B for the skill shot advances twice. Drops score 500 plus one bonus, with 50K on the first completion of all eight and Special on the second. The outlanes score 1,000, or 50,000 lit at 3X on the right and 2X on the left. The readme prints “light outlane” in that second row.

At `$598c`–`$59ad` the ROM reads the DIP banks into RAM `$0d`–`$10` and stores their nibbles at `$0264`–`$026b` from `$59c2`. `$1ad6`–`$1afb` reconstructs the final bank and checks mask `$03` before writing one credit to initialized zero bytes at `$02ad–$02ae`. `$1b1d`–`$1b35` uses mask `$04` to display credits. The erased-memory native probe required a first coin even with S25/S26 on. In a separate initialized-memory run, S25/S26 on replenished 00 to 01 and issued solenoid 19 on Start without a coin. The other three settings showed 00 and issued no serve.

The credit-limit routine at `$1ab7` reconstructs the DIP byte in A, then masks and indexes with the incoming B register at `$1ac6`. The pointer at `$1ab1` leads to BCD `10, 15, 25, 40` at `$1ab3–$1ab6`. The one-credit floor has a separate guard in `$1ad6`. Read these paths in `matatest-disassembly.txt`, replayed with the same MC6800 reader as the [stock listing](stock-rom-read-path.md).

The `matatest-initialized-credits` manifest pins all raw captures. Each run starts with the same previously initialized revision-7 CMOS, with the balance set to 00 for the Start test or 09 for the coin test. The first three DIP banks are zero and S27 is on. Each coin test pulses one factory chute switch 37 times. This fixes the pricing inputs while varying S25/S26. The author chart labels them as maximum-credit settings. The three coin paths in this matrix stop at 25 for every setting.

| S26/S25 | Initialized-zero Start result | Coin I (switch 10) | Coin II (switch 11) | Coin III (switch 9) |
| --- | --- | ---: | ---: | ---: |
| `00` | 00, no serve | 25 | 25 | 25 |
| `01` | 00, no serve | 25 | 25 | 25 |
| `10` | 00, no serve | 25 | 25 | 25 |
| `11` | 01, serve | 25 | 25 | 25 |

For each row use the corresponding binary index 0–3 under `zero-`, `cap-`, `centre-` and `right-coin-`. Each directory includes its scenario, initial and saved state, full trace and input hashes. The retained `right-` directories are exploratory switch-12 runs. `probe-matatest-credits.py` replays the four confirmed groups into a fresh external output directory.

The native game showed 3,000 on the first top A closure. Oliver describes the skill shot itself as an A+B sequence.

## Quench Free Play+ (February 2019)

[Quench's author post](https://pinside.com/pinball/forum/topic/nvram-memory-structure-of-early-bally-games), topic 316891 post 8, describes his Bally MPU-17 Free Play+ family and the credit display's blank state at zero. The exact `mataharc.zip` includes `MataHari_Update.txt` dated February 12, 2019 (SHA-256 `5bd2fc8d261b99b97cd229064a2403d27e3b6b26b6d4d01810edcca3d447b8b9`). U2 CRC-32 `5794ecfb` and U6 CRC-32 `7171d600` match the pinned driver. The readme covers 2716/2816 devices with the correct jumpers, a closed-switch test that cycles every closed input, zero in the ball-in-play field at game over with Match disabled, and a drop target that awards once while down. In free play, boot supplies nine credits when the prior balance was zero. Credit lamp 59 is available at zero and the unlit credit display does not prevent join-in.

| S19 | S18 | S17 | Maximum credits | Starting behavior |
| --- | --- | --- | ---: | --- |
| Off | Off | Off | 5 | Paid |
| Off | Off | On | 10 | Paid |
| Off | On | Off | 15 | Paid |
| Off | On | On | 20 | Paid |
| On | Off | Off | 25 | Paid |
| On | Off | On | 30 | Paid |
| On | On | Off | 99 | Free play, count down on a start or join |
| On | On | On | 99 | Free play, clear balance at new game |

PinMAME's [original introduction](https://github.com/vpinball/pinmame/commit/b16f9c4a8c16c1e13ad83c23b1beb53116086995) added the family. The Mata Hari U2 CRC progressed from `e60ee602` to `508b968b` in [the February variant update](https://github.com/vpinball/pinmame/commit/211ea3fd7cc320709848d91361feb25a3c67077e) and to `5794ecfb` in [the February replacement](https://github.com/vpinball/pinmame/commit/75d195ebe43c89a3fc6d9611f47e2825aef9d2b7). U6 stayed the same. Those commit messages describe groups of changes across multiple games. The February 12 Mata Hari-specific readme and native tests establish this game's behavior.

## Quench V22 (April 2025)

The [V22 author readme](https://nvram.weebly.com/uploads/5/4/2/5/54255141/matahari.v22.2025.04.13.txt) matches the text in both authorized V22 archives, with U2 CRC-32 `20e71aec` and U6 CRC-32 `995b3454`. It supersedes the V21 Pinheadz page for this driver. Fit two 2532/2732 EPROMs with the MPU provisioned for the chips and the BY35 addressing used by the driver. The six- and seven-digit sets load the same program. S19 off uses virtual millions. For S19 on, the millions strobe runs from MPU J1-7 to each player module's Bally J1-12 or Stern J1-11. The credit and ball/match windows retain two digits each. Both modes crossed one million in the retained traces.

| S18 | S17 | Maximum credits |
| --- | --- | ---: |
| Off | Off | 5 |
| Off | On | 10 |
| On | Off | 20 |
| On | On | 99, free play |

| S29 | S31 | S30 | Special | Extra ball award |
| --- | --- | --- | --- | --- |
| Off | Off | Off | 50,000 | 50,000 |
| Off | Off | On | 50,000 | Extra ball (c) |
| Off | On | Off | Extra ball (a) | Extra ball (b) |
| Off | On | On | Replay | Extra ball (b) |
| On | Off | Off | 50,000 | 25,000 |
| On | Off | On | Extra ball (a) | 25,000 |
| On | On | Off | Extra ball (a) | Extra ball (c) |
| On | On | On | Replay | Extra ball (c) |

An extra ball already lit changes the awards marked (a), (b) and (c) to 50,000, 5,000 and 25,000 respectively.

| Software setting | 0 | 1 |
| --- | --- | --- |
| 13:1 | Tilt forfeits the ball | Tilt-through protection repeats an unscored ball |
| 13:2 | No extra-ball sound | Extra-ball sound |
| 13:3 | Start clears balance | Start and join count down |
| 13:4 | One bonus countdown per multiplier unit | One premultiplied countdown |
| 14:1 | Multipliers through 5X | Adds 7X, 8X and 10X |
| 14:2 | A/B advances saucer potential | Saucer visit advances potential |
| 14:3 | Single lit outlane alternates on 500-point scores | Left-only before both qualify |
| 14:4 | First outlane award qualifies at 3X | First outlane award qualifies at 2X |
| 15:1 | A/B value tops at 5,000 | Extends to 15,000 |
| 15:2 | When extended, Special at 15,000 | Also at 9,000, 12,000 and 14,000 |
| 15:3 | 15,000 Special once per ball | Open-ended 15,000 Special |
| 15:4 | Awards 10,000 and above in 1,000 steps | 10,000 step plus 1,000 steps |

Setting 16 is the 0–15 power-up free-play balance when the saved balance was zero. In free play the indicator stays lit and players can start or join at zero. The knocker can fire at the 99-credit cap.

Other documented changes include scoring every simultaneous drop, awarding 500 for the last target and remembering a fallen target to suppress re-scoring. Firmware cycles every closed switch in test and speeds threshold adjustments and repeated service presses. Hold Start and tap Self Test to jump from tests to switch test, from switch test to Audit 13, clear audits 1–12 or load defaults in settings 13–16. V22 displays the version in the ball/match field, restores the previous scores after power-up, shows the high score at last ball, blanks unused player fields, flashes the current score at serve until scoring, clears the final Player Up lamp at game over, clears ball-in-play to 0 when Match is disabled, tunes both tilt and slam, lights Shoot Again on an unscored drain, and processes pending points before handling the outhole. The older [V21 page](https://www.pinheadz.net/mata-hari-new-rules) describes the predecessor, without V22's separate tilt tune.

### V22 Audit 12

The author readme's Audit 12 paragraph prints `13:3=1` next to Credit Reset. The readme's setting table, the exact ROM and the native controls establish that Credit Reset uses `13:3=0`.

- **Record.** With S17 and S18 on and Credit Reset selected, `$1aea` keeps the higher of the saved Audit 12 value and the ordinary credit balance at the end of the game. The ROM samples the balance after high-score checks and before Match. Coin-added credits count, and the game score may stay below High Game to Date. The record uses CMOS `$02fe–$02ff`.
- **High Game to Date.** `$1b4a` substitutes the saved record in the credit field when S17, S18 and S20 are on and Credit Reset is selected. The same path can run between balls. S20 controls this display independently of the record write.
- **Service.** The sequential walker at `$5ae3` includes Audit 12 in paid play and both free-play modes regardless of S20. The player displays show the saved value and the ball-in-play display shows page 12.

The retained `audit12-v22-focused.txt` lists the exact code from the authorized six-digit V22 ROMs, which have the same program bytes as the seven-digit set. `audit12-verify.py` checks the decoded instructions and the five native captures under `audit12-native-final/`. Each case used a fresh state with synthetic CMOS for 15 starting credits, a 432,100 high score and the stated prior record. Each finished at 9,500 points with Match disabled. The paid condition limited the initial credit balance to ten.

| Audit 12 native run | End balance | High Game to Date credits pre-game / between balls / post-game | Prior record → saved / service | Trace SHA-256 |
| --- | ---: | --- | --- | --- |
| `freeplay-reset` | 9 | 02 / 02 / 09 | 2 → 9 / 9 | `439d7179ff5738aa18a9c1127ab93cd56173b60bbc39693c0eb08b3c5a0237b3` |
| `freeplay-count` | 23 | 15 / 23 / 23 | 2 → 2 / 2 | `0fddd3b0c98f99b9a8ac0587858f2b86f34b6f2f3af084ac19731917ed84d9f9` |
| `paid` | 10 | 10 / 10 / 10 | 2 → 2 / 2 | `4e899b08a0f7214c674704b55639b0f4de1d8c73606e8a9263e29c2889591905` |
| `freeplay-reset-higher-record` | 9 | 20 / 20 / 20 | 20 → 20 / 20 | `ad943ebdca3ab56da3dacc75c6dc68063a3d951753fa923e4bfd60fa8d571c0d` |
| `freeplay-reset-hidden` | 9 | blank / blank / blank | 2 → 9 / 9 | `ce3772743e0f41ae3ab5d32eeacbb9dfe8d010112673216491c4a9e1457f1b9d` |
