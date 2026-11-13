# Breakshot — ROM service tests (bsv103)

Read from the ROM's own service menu, run on LibPinMAME by the four retained harness runs the seed
`tools/seeds/capcom/breakshot-1996-service-readings.json` names. Each row pairs the public address the
step drove or that changed with the 128x32 DMD frame shown at that step. The text is literal, with ` / `
between display lines; `Frame` is the first 16 hex digits of the frame's pixel SHA-256 (the seed and
`evidence/runtime/capcom/breakshot-service-diagnostics.json` carry the full digests). The curator read each cited 128x32 DMD frame on an 8x nearest-neighbour render of the retained frame; text is literal, with ' / ' separating the display's lines.

## Switch Test

Each public switch held at 1 on its own while the test was showing. `unchanged` means the frame equals the
previous step's; `name panel unchanged` means only the switch grid changed and the test named nothing.

| Public | Display | Frame |
| ---: | --- | --- |
| 1 | COIN 1 / 01) GRN-BRN | `2d0b5f04af5342a0` |
| 2 | COIN 2 / 02) GRN-RED | `72d9012b1efa4993` |
| 3 | COIN 3 / 03) GRN-ORG | `700cbbb7710350c3` |
| 4 | COIN 4 / 04) GRN-YEL | `3897162dadf2a1fd` |
| 9 | unchanged | `f63b26dc39d64840` |
| 10 | unchanged | `f63b26dc39d64840` |
| 11 | unchanged | `f63b26dc39d64840` |
| 12 | unchanged | `f63b26dc39d64840` |
| 13 | unchanged | `f63b26dc39d64840` |
| 14 | unchanged | `f63b26dc39d64840` |
| 15 | unchanged | `f63b26dc39d64840` |
| 16 | unchanged | `f63b26dc39d64840` |
| 17 | UNUSED / 17)ROW WHT-BRN COL RED-BRN | `66d89add3e509db6` |
| 18 | UNUSED / 18)ROW WHT-RED COL RED-BRN | `1cd24d5a2a274995` |
| 19 | UNUSED / 19)ROW WHT-ORG COL RED-BRN | `d617335709a8444a` |
| 20 | UNUSED / 20)ROW WHT-YEL COL RED-BRN | `24cb2a852cc389e1` |
| 21 | name panel unchanged | `5773261731fd32a0` |
| 22 | name panel unchanged | `ddc6c8c29804f628` |
| 23 | UNUSED / 23)ROW WHT-VIO COL RED-BRN | `684800c0a57b5df9` |
| 24 | unchanged | `7a4082ee91cbac5a` |
| 25 | UNUSED / 25)ROW WHT-BRN COL RED-BLK | `39d6445ed7a8d203` |
| 26 | UNUSED / 26)ROW WHT-RED COL RED-BLK | `d8cce62cc4487e83` |
| 27 | UNUSED / 27)ROW WHT-ORG COL RED-BLK | `e93ea65eb8616b9c` |
| 28 | UNUSED / 28)ROW WHT-YEL COL RED-BLK | `ab67466a29725b5b` |
| 29 | SLAM TILT / 29)ROW WHT-GRN COL RED-BLK | `d03c0365615787c3` |
| 30 | TILT BOB / 30)ROW WHT-BLU COL RED-BLK | `2823d5d9ae156c86` |
| 31 | OPTIONAL BUY IN / 31)ROW WHT-VIO COL RED-BLK | `8823a62bc143be65` |
| 32 | DISPENSER NOTCH / 16) WHT-GRY | `1b0809489bdb62ce` |
| 33 | L. FLIPPER EOS / 33)ROW WHT-BRN COL RED-ORG | `07245066121fd64a` |
| 34 | R. FLIPPER EOS / 34)ROW WHT-RED COL RED-ORG | `f63146462e4c0ba1` |
| 35 | OUTHOLE / 35)ROW WHT-ORG COL RED-ORG | `10b4817434fd4b67` |
| 36 | TROUGH OPTO 1 / 36)ROW WHT-YEL COL RED-ORG | `e96986628213c9b6` |
| 37 | TROUGH OPTO 2 / 37)ROW WHT-GRN COL RED-ORG | `1aa57c7a70d70114` |
| 38 | TROUGH OPTO 3 / 38)ROW WHT-BLU COL RED-ORG | `81fd477a8308be2d` |
| 39 | UNUSED / 39)ROW WHT-VIO COL RED-ORG | `56a87c49e52913e9` |
| 40 | DISPENSER NOTCH / 16) WHT-GRY | `f336f1b45f9d36ac` |
| 41 | L. SLINGSHOT / 41)ROW WHT-BRN COL RED-YEL | `81ec925e999f8a94` |
| 42 | R. SLINGSHOT / 42)ROW WHT-RED COL RED-YEL | `d5c0cc1b3557b3b4` |
| 43 | SHOOTER LANE / 43)ROW WHT-ORG COL RED-YEL | `05ccdcb9a895a576` |
| 44 | L. INLANE / 44)ROW WHT-YEL COL RED-YEL | `1224e25bb3b7a920` |
| 45 | R. INLANE / 45)ROW WHT-GRN COL RED-YEL | `6bc1d217a943b634` |
| 46 | L. OUTLANE / 46)ROW WHT-BLU COL RED-YEL | `7640d0e347b9494f` |
| 47 | R. OUTLANE / 47)ROW WHT-VIO COL RED-YEL | `4fadf9b5c346dc86` |
| 48 | unchanged | `7a7a9e31b9300fe9` |
| 49 | R. DROP L. / 49)ROW WHT-BRN COL RED-GRN | `06adadad55788f88` |
| 50 | R. DROP C. / 50)ROW WHT-RED COL RED-GRN | `98a0495a99809ada` |
| 51 | R. DROP R. / 51)ROW WHT-ORG COL RED-GRN | `c53b71f5a164fe93` |
| 52 | R. DROP STANDUP / 52)ROW WHT-YEL COL RED-GRN | `62dc452cbf2d1129` |
| 53 | L. ORBIT OPTO / 53)ROW WHT-GRN COL RED-GRN | `b6355b9ba08db643` |
| 54 | R. ORBIT OPTO / 54)ROW WHT-BLU COL RED-GRN | `d5bc2b8601fd1b20` |
| 55 | CAPTIVE STANDUP / 55)ROW WHT-VIO COL RED-GRN | `81d455c7ed6d5e59` |
| 56 | unchanged | `7d9891dce392a610` |
| 57 | L. STAR BMPR / 57)ROW WHT-BRN COL RED-BLU | `4178dd907fa6565f` |
| 58 | C. STAR BMPR / 58)ROW WHT-RED COL RED-BLU | `81230105355cce7f` |
| 59 | R. STAR BMPR / 59)ROW WHT-ORG COL RED-BLU | `e0f92c3cedeb93f1` |
| 60 | L. TOPLANE / 60)ROW WHT-YEL COL RED-BLU | `29b1ad8556769d03` |
| 61 | C. TOPLANE / 61)ROW WHT-GRN COL RED-BLU | `7cb257e7e210e7eb` |
| 62 | R. TOPLANE / 62)ROW WHT-BLU COL RED-BLU | `a3d9ba7f58703a8f` |
| 63 | BANKSHOT LANE / 63)ROW WHT-VIO COL RED-BLU | `33a225b12a1156fc` |
| 64 | DISPENSER NOTCH / 16) WHT-GRY | `7e68ed084e49a5e1` |
| 65 | CNTR PKT OPTO / 65)ROW WHT-BRN COL RED-VIO | `0201fa21a2c72dfc` |
| 66 | CENTER POST / 66)ROW WHT-RED COL RED-VIO | `ae2786454435e28e` |
| 67 | BONUS SAUCER / 67)ROW WHT-ORG COL RED-VIO | `3089608d3d6bb4b1` |
| 68 | CNTR PKT L / 68)ROW WHT-YEL COL RED-VIO | `7f249f531d647d1a` |
| 69 | CNTR PKT C / 69)ROW WHT-GRN COL RED-VIO | `f22556cb3c5073fe` |
| 70 | CNTR PKT R / 70)ROW WHT-BLU COL RED-VIO | `e8740441cbca5234` |
| 71 | UR. FLIPPER EOS / 71)ROW WHT-VIO COL RED-VIO | `4c9c1097e9b8cdd7` |
| 72 | DISPENSER NOTCH / 16) WHT-GRY | `7db3506bf9a9c3aa` |
| 73 | L. DROP L. / 73)ROW WHT-BRN COL RED-GRY | `d2f0a3ce0e47cdc1` |
| 74 | L. DROP C. / 74)ROW WHT-RED COL RED-GRY | `f87400ecefdfc764` |
| 75 | L. DROP R. / 75)ROW WHT-ORG COL RED-GRY | `f0bc17e8dcd4f761` |
| 76 | L. DROP STANDUP / 76)ROW WHT-YEL COL RED-GRY | `87ff6d03bf82afc7` |
| 77 | L LITE SUPER Q. / 77)ROW WHT-GRN COL RED-GRY | `0e1e58034ade707f` |
| 78 | R LITE SUPER Q. / 78)ROW WHT-BLU COL RED-GRY | `d3310cd2ee6a7442` |
| 79 | CAPTIVE ROLLOVR / 79)ROW WHT-VIO COL RED-GRY | `38b5ba3884528438` |
| 80 | unchanged | `053358e4d702a340` |

## Solenoid Test

Each coil selected with the right flipper button and fired with Start. `Fired` lists the public solenoid
addresses that went active on the fire step.

| Public | Display | Fired | Frame |
| ---: | --- | --- | --- |
| 1 | S01 - OUTHOLE / BRN-BLK J17/18.1 / VIO PWR 50V | 1 | `08845844b7f19648` |
| 2 | S02 - TROUGH / BRN-RED J17/18.2 / VIO PWR 50V | 2 | `d81459ca6d80096f` |
| 3 | S03 - KNOCKER / BRN-ORG J17/18.3 / VIO PWR 50V | 3 | `632bce706f2916a1` |
| 4 | S04 - L. SLINGSHOT / BRN-YEL J17/18.4 / VIO PWR 50V | 4 | `1cdefcfbcceedaea` |
| 5 | S05 - R. SLINGSHOT / BRN-GRN J17/18.5 / VIO PWR 50V | 5 | `0a46e49503edb888` |
| 6 | S06 - KICKER / BRN-BLU J17/18.6 / VIO PWR 50V | 6 | `0abc022c3389f5a9` |
| 7 | S07 - R. DROP RESET / BRN-VIO J17/18.7 / VIO PWR 50V | 7 | `d30698418106ad0c` |
| 8 | S08 - BONUS SAUCER / BRN-GRY J17/18.9 / VIO PWR 50V | 8 | `d55ba00c5e28613d` |
| 9 | S09 - L. FLIPPER / GRN-BRN J21/22.1 / VIO PWR 50V | 9, 47, 48 | `2c81a5485fe2e66f` |
| 10 | S10 - R. FLIPPER / GRN-RED J21/22.2 / VIO PWR 50V | 10, 45, 46 | `83781aff50d8b265` |
| 11 | S11 - UR. FLIPPER / GRN-ORG J21/22.3 / VIO PWR 50V | 11, 33, 34 | `c9791ed6236dcb55` |
| 12 | S12 - CENTER POST UP / GRN-YEL J21/22.4 / VIO PWR 50V | 12 | `06e3255d67b12dc9` |
| 13 | S13 - L. DROP RESET / GRN-BLK J21/22.5 / VIO PWR 50V | 13 | `bd924826cf742b4d` |
| 14 | S14 - CENTER POST DOWN / GRN-BLU J21/22.7 / VIO PWR 50V | 14 | `268688fa48565ce3` |
| 15 | S15 - RIGHT TOPGATE / GRN-VIO J21/22.8 / RED PWR 20V | 15 | `b7105a6814380720` |
| 16 | S16 - LEFT TOPGATE / GRN-GRY J21/22.9 / RED PWR 20V | 16 | `e6ff5af29e8166ad` |
| 17 | S17 - UNUSED | 17 | `60eacc13aa77f0a3` |
| 18 | S18 - UNUSED | 18 | `3fe76964d22f620c` |
| 19 | S19 - UNUSED | 19 | `22e7dc4154d4ac36` |
| 20 | S20 - UNUSED | 20 | `660f0c1b90daef6a` |
| 21 | S21 - UNUSED | 21 | `477b8c97e6195c77` |
| 22 | S22 - UNUSED | 22 | `93b5706921e9e6d8` |
| 23 | S23 - UNUSED | 23 | `ebe63b3165e92edb` |
| 24 | S24 - UNUSED | 24 | `b13ccff7811389aa` |
| 25 | S25 - CNTR POCKET L / GRY-BRN J26/27.1 / VIO PWR 50V | 25 | `06a26a1e4429a367` |
| 26 | S26 - CNTR POCKET C / GRY-RED J26/27.2 / VIO PWR 50V | 26 | `392a9b96d509801f` |
| 27 | S27 - UNUSED / GRY-ORG J26/27.3 | 27 | `c8d97fe0741870d3` |
| 28 | S28 - CNTR POCKET FLASH / GRY-YEL J26/27.5 / RED PWR 20V | 28 | `a96f19a8645046cc` |
| 29 | S29 - R STAR BUMPER / GRY-GRN J26/27.6 / VIO PWR 50V | 29 | `b7edb3baed01105c` |
| 30 | S30 - C STAR BUMPER / GRY-BLU J26/27.7 / VIO PWR 50V | 30 | `0c34db429421b75e` |
| 31 | S31 - L STAR BUMPER / GRY-VIO J26/27.8 / VIO PWR 50V | 31 | `58e26328640aa4c8` |
| 32 | S32 - CNTR POCKET R / GRY-BLK J26/27.9 / VIO PWR 50V | 32 | `762337d7b3eb977b` |

## Lamp Test

The single-lamp walk; at each step only the listed public lamp was lit.

| Public | Display | Frame |
| ---: | --- | --- |
| 1 | 11B - START BUTTON / COL-SM1B J5/6.1 BLU-BRN / ROW-M1B J7/8.1 ORG-BRN | `8b88a5d9eee7b2be` |
| 2 | 12B - OPTIONAL BUY IN / COL-SM1B J5/6.1 BLU-BRN / ROW-M2B J7/8.2 ORG-RED | `1e1508e0baeb505f` |
| 3 | 13B - CAPTIVE BALL 1 / COL-SM1B J5/6.1 BLU-BRN / ROW-M3B J7/8.4 ORG-BLK | `0a9957da42749df6` |
| 4 | 14B - CAPTIVE BALL 2 / COL-SM1B J5/6.1 BLU-BRN / ROW-M4B J7/8.5 ORG-YEL | `3e9894bce18d3a21` |
| 5 | 15B - CAPTIVE BALL 3 / COL-SM1B J5/6.1 BLU-BRN / ROW-M5B J7/8.6 ORG-GRN | `63c26c54b365d7ec` |
| 6 | 16B - SHOOT AGAIN / COL-SM1B J5/6.1 BLU-BRN / ROW-M6B J7/8.7 ORG-BLU | `ef0c24788b41a96e` |
| 7 | 17B - R SUPER CUE / COL-SM1B J5/6.1 BLU-BRN / ROW-M7B J7/8.8 ORG-VIO | `215e218140a04351` |
| 8 | 18B - CAPTIVE BALL EB / COL-SM1B J5/6.1 BLU-BRN / ROW-M8B J7/8.9 ORG-GRY | `9f075b5b327c8898` |
| 9 | 21B - 1 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M1B J7/8.1 ORG-BRN | `fc0e16ced598e433` |
| 10 | 22B - 2 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M2B J7/8.2 ORG-RED | `3b51e164f38a9a3b` |
| 11 | 23B - JACKPOT / COL-SM2B J5/6.2 BLU-RED / ROW-M3B J7/8.4 ORG-BLK | `fec6768ad3b5b39d` |
| 12 | 24B - L SUPER CUE / COL-SM2B J5/6.2 BLU-RED / ROW-M4B J7/8.5 ORG-YEL | `df2dbe4962e183f4` |
| 13 | 25B - 3 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M5B J7/8.6 ORG-GRN | `f9d2766bbceb2f6f` |
| 14 | 26B - 9 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M6B J7/8.7 ORG-BLU | `d1bde9cf8f445278` |
| 15 | 27B - 10 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M7B J7/8.8 ORG-VIO | `8d85747cf301f1b8` |
| 16 | 28B - 11 BALL / COL-SM2B J5/6.2 BLU-RED / ROW-M8B J7/8.9 ORG-GRY | `2a29eea19a9122f6` |
| 17 | 31B - 6 BALL / COL-SM3B J5/6.3 BLU-ORG / ROW-M1B J7/8.1 ORG-BRN | `698e02131d500297` |
| 18 | 32B - 14 BALL / COL-SM3B J5/6.3 BLU-ORG / ROW-M2B J7/8.2 ORG-RED | `cf6758cb99b7e1ab` |
| 19 | 33B - L DROP SPOT BALL / COL-SM3B J5/6.3 BLU-ORG / ROW-M3B J7/8.4 ORG-BLK | `e5795c8e6cb06e93` |
| 20 | 34B - 9 BALL POINTS / COL-SM3B J5/6.3 BLU-ORG / ROW-M4B J7/8.5 ORG-YEL | `ed1e5f6516ee1ed8` |
| 21 | 35B - ROTATION OPTION / COL-SM3B J5/6.3 BLU-ORG / ROW-M5B J7/8.6 ORG-GRN | `a3640b5cf810487d` |
| 22 | 36B - 9 BALL XBALL / COL-SM3B J5/6.3 BLU-ORG / ROW-M6B J7/8.7 ORG-BLU | `c3e72b331ae05038` |
| 23 | 37B - 8 BALL OPTION / COL-SM3B J5/6.3 BLU-ORG / ROW-M7B J7/8.8 ORG-VIO | `04ab33facbbe2594` |
| 24 | 38B - 9 BALL SPCL / COL-SM3B J5/6.3 BLU-ORG / ROW-M8B J7/8.9 ORG-GRY | `03547d215d2322f9` |
| 25 | 41B - L CNTR PKT GI / COL-SM4B J5/6.4 BLU-YEL / ROW-M1B J7/8.1 ORG-BRN | `194af821f44d8d07` |
| 26 | 42B - R CNTR PKT GI / COL-SM4B J5/6.4 BLU-YEL / ROW-M2B J7/8.2 ORG-RED | `0ae03b16a620d8f4` |
| 27 | 43B - RIGHT TOPLANE / COL-SM4B J5/6.4 BLU-YEL / ROW-M3B J7/8.4 ORG-BLK | `4ee912739fa9bdd9` |
| 28 | 44B - KICKER / COL-SM4B J5/6.4 BLU-YEL / ROW-M4B J7/8.5 ORG-YEL | `5ab2e38d8829eb49` |
| 29 | 45B - 4 BALL / COL-SM4B J5/6.4 BLU-YEL / ROW-M5B J7/8.6 ORG-GRN | `c6ae0122f2a43719` |
| 30 | 46B - LITE SUPER CUE L / COL-SM4B J5/6.4 BLU-YEL / ROW-M6B J7/8.7 ORG-BLU | `5a7860f6762ac700` |
| 31 | 47B - 12 BALL / COL-SM4B J5/6.4 BLU-YEL / ROW-M7B J7/8.8 ORG-VIO | `09a42ac7cb0e267f` |
| 32 | 48B - CENTER TOPLANE / COL-SM4B J5/6.4 BLU-YEL / ROW-M8B J7/8.9 ORG-GRY | `6d35dc9454a12ef3` |
| 33 | 51B - ORBIT SPOT BALL / COL-SM5B J5/6.5 BLU-GRN / ROW-M1B J7/8.1 ORG-BRN | `aab3f58ab9c09225` |
| 34 | 52B - CALL YOUR SHOT / COL-SM5B J5/6.5 BLU-GRN / ROW-M2B J7/8.2 ORG-RED | `8fee6b1cde266c16` |
| 35 | 53B - COLLECT BONUS / COL-SM5B J5/6.5 BLU-GRN / ROW-M3B J7/8.4 ORG-BLK | `df9d29bd4f232f1a` |
| 36 | 54B - 8 BALL / COL-SM5B J5/6.5 BLU-GRN / ROW-M4B J7/8.5 ORG-YEL | `cb471a48b45687d8` |
| 37 | 55B - 13 BALL / COL-SM5B J5/6.5 BLU-GRN / ROW-M5B J7/8.6 ORG-GRN | `c820af3539d24a8b` |
| 38 | 56B - LITE SUPER CUE R / COL-SM5B J5/6.5 BLU-GRN / ROW-M6B J7/8.7 ORG-BLU | `8a9b5de3dd11c32c` |
| 39 | 57B - 5 BALL / COL-SM5B J5/6.5 BLU-GRN / ROW-M7B J7/8.8 ORG-VIO | `b920be5b61606c2d` |
| 40 | 58B - BALLORAMA / COL-SM5B J5/6.5 BLU-GRN / ROW-M8B J7/8.9 ORG-GRY | `66154e546849dacc` |
| 41 | 61B - 9 BALL OPTION / COL-SM6B J5/6.6 BLU-BLK / ROW-M1B J7/8.1 ORG-BRN | `a00450a7e17510f6` |
| 42 | 62B - CNTR POCKET L / COL-SM6B J5/6.6 BLU-BLK / ROW-M2B J7/8.2 ORG-RED | `b3983a011f0a7181` |
| 43 | 63B - CNTR POCKET C / COL-SM6B J5/6.6 BLU-BLK / ROW-M3B J7/8.4 ORG-BLK | `e1e92dedad12f9fd` |
| 44 | 64B - CNTR POCKET R / COL-SM6B J5/6.6 BLU-BLK / ROW-M4B J7/8.5 ORG-YEL | `0aa71ed3ce7035b8` |
| 45 | 65B - LEFT TOPLANE / COL-SM6B J5/6.6 BLU-BLK / ROW-M5B J7/8.6 ORG-GRN | `4a3083dd253a547f` |
| 46 | 66B - R DROP SPOT BALL / COL-SM6B J5/6.6 BLU-BLK / ROW-M6B J7/8.7 ORG-BLU | `7c769e72cd4acd45` |
| 47 | 67B - 15 BALL / COL-SM6B J5/6.6 BLU-BLK / ROW-M7B J7/8.8 ORG-VIO | `daacc7f1f4861dcf` |
| 48 | 68B - 7 BALL / COL-SM6B J5/6.6 BLU-BLK / ROW-M8B J7/8.9 ORG-GRY | `7ebc04d5f5ec6030` |
| 49 | 71B - BANK SHOT / COL-SM7B J5/6.8 BLU-VIO / ROW-M1B J7/8.1 ORG-BRN | `042b695b84b03eb5` |
| 50 | 72B - BONUS RACK 1 / COL-SM7B J5/6.8 BLU-VIO / ROW-M2B J7/8.2 ORG-RED | `0a363e59a0e6ffe2` |
| 51 | 73B - BONUS RACK 2 / COL-SM7B J5/6.8 BLU-VIO / ROW-M3B J7/8.4 ORG-BLK | `24900ff98ddc10a2` |
| 52 | 74B - BONUS RACK 3 / COL-SM7B J5/6.8 BLU-VIO / ROW-M4B J7/8.5 ORG-YEL | `30e55f2a12cfa233` |
| 53 | 75B - BONUS RACK 4 / COL-SM7B J5/6.8 BLU-VIO / ROW-M5B J7/8.6 ORG-GRN | `e8fd6a179caf4983` |
| 54 | 76B - BONUS RACK 5 / COL-SM7B J5/6.8 BLU-VIO / ROW-M6B J7/8.7 ORG-BLU | `45687179ecebd147` |
| 55 | 77B - BONUS RACK 6 / COL-SM7B J5/6.8 BLU-VIO / ROW-M7B J7/8.8 ORG-VIO | `a5214c685b4cc227` |
| 56 | 78B - BONUS RACK 7 / COL-SM7B J5/6.8 BLU-VIO / ROW-M8B J7/8.9 ORG-GRY | `cbaca87ed0c4df80` |
| 57 | 81B - BONUS RACK 8 / COL-SM8B J5/6.9 BLU-GRY / ROW-M1B J7/8.1 ORG-BRN | `24778f674f0dd024` |
| 58 | 82B - BONUS RACK 9 / COL-SM8B J5/6.9 BLU-GRY / ROW-M2B J7/8.2 ORG-RED | `509a68a32d4b54fe` |
| 59 | 83B - BONUS RACK 10 / COL-SM8B J5/6.9 BLU-GRY / ROW-M3B J7/8.4 ORG-BLK | `0110ed8c4ae24ac9` |
| 60 | 84B - BONUS RACK 11 / COL-SM8B J5/6.9 BLU-GRY / ROW-M4B J7/8.5 ORG-YEL | `442851937e56a573` |
| 61 | 85B - BONUS RACK 12 / COL-SM8B J5/6.9 BLU-GRY / ROW-M5B J7/8.6 ORG-GRN | `a7d98cf136f1f814` |
| 62 | 86B - BONUS RACK 13 / COL-SM8B J5/6.9 BLU-GRY / ROW-M6B J7/8.7 ORG-BLU | `c823b23d0ba873c0` |
| 63 | 87B - BONUS RACK 14 / COL-SM8B J5/6.9 BLU-GRY / ROW-M7B J7/8.8 ORG-VIO | `6b7c995d8d5c532b` |
| 64 | 88B - BONUS RACK 15 / COL-SM8B J5/6.9 BLU-GRY / ROW-M8B J7/8.9 ORG-GRY | `ab53023b2acb6183` |

## Gameplay check

A short game on fresh state: boot, coins, Start, the shooter lane, both drop banks, the tilt bob and the
slam tilt. `Fired` lists the public solenoid addresses that went active during the step and `Released`
those whose only change was back to off; a dash means none.

| Step | Display | Fired | Released | Frame |
| --- | --- | --- | --- | --- |
| boot into attract with a full trough (the power-on coil pulses happen in this window) | attract: high-score entry 5,000,000 / 3) JRP | 28 | - | `52a9163a9a79e7f8` |
| coin chute 1 (first coin) | Credits 1/2 | - | - | `8828cba1b727d305` |
| coin chute 1 (second coin) | Credits 1 | - | - | `dda6e5aac02c4c55` |
| Start with a credit and a full trough: the ROM resets both drop banks and serves a ball | ball-rack animation | 2, 7, 13 | - | `c9f7171294b86968` |
| the served ball leaves the trough eject position (36 clears) |  | - | 2 | `0ec24a1f373e5a3b` |
| the ball reaches the shooter lane (43) | COMPLETE 3 MORE POOL GAMES FOR CUTTHROAT COUNTDOWN | - | - | `f1a9e8e696b67dc3` |
| the ball leaves the shooter lane | BALL IN PLAY 1, score 0 | - | - | `099af323df7b67b7` |
| play with every target standing: control window | unchanged: BALL IN PLAY 1, score 0 | - | - | `dd5617fdbfd2583f` |
| hold the left flipper button bit (84) |  | 9, 47, 48 | - | `15374cfb275479fc` |
| release the left flipper button bit |  | - | 9, 47, 48 | `87d0f468bac253a3` |
| hold the right flipper button bit (82) |  | 10, 45, 46 | - | `9cdc0ba27d69bd58` |
| release the right flipper button bit |  | - | 10, 45, 46 | `87d0f468bac253a3` |
| hold public 21 (the ROM's UR. FLIPPER switch) |  | 11, 33, 34 | - | `7bf4121a88125d8f` |
| release public 21 |  | - | 11, 33, 34 | `8fcf285986a1f5a9` |
| hold public 81 (the flipper column's lower-right end-of-stroke bit, which CAPCOM.VBS writes for a staged right flipper key) |  | - | - | `dd5617fdbfd2583f` |
| release public 81 |  | - | - | `69c30326115dedcb` |
| right bank control: public 48 alone to 1 (the address both community tables give the right bank's first target) | unchanged: BALL IN PLAY 1, score 0 | - | - | `87d0f468bac253a3` |
| public 48 back to 0 |  | - | - | `dd5617fdbfd2583f` |
| right bank: 49 down | drop-target animation | - | - | `f5f303daa67c49d3` |
| right bank: 50 down | drop-target animation | - | - | `30284fee691ba719` |
| right bank: 51 down, 49-51 all at 1 | PLAYER 1 BALL IN PLAY 1, score 0,009,000 | - | - | `8b9a898ec758549a` |
| right bank: 49 back up |  | - | - | `8b9a898ec758549a` |
| right bank: 50 back up |  | - | - | `8b9a898ec758549a` |
| right bank: 51 back up |  | - | - | `8b9a898ec758549a` |
| right bank as the community tables number it: 48 down |  | - | - | `8b9a898ec758549a` |
| 49 down |  | - | - | `8b9a898ec758549a` |
| 50 down, 48-50 all at 1 |  | - | - | `8b9a898ec758549a` |
| 48 back up |  | - | - | `8b9a898ec758549a` |
| 49 back up |  | - | - | `8b9a898ec758549a` |
| 50 back up |  | - | - | `8b9a898ec758549a` |
| left bank: 73 down | drop-target animation | - | - | `9bd9f1fd067891c9` |
| left bank: 74 down | drop-target animation | - | - | `30284fee691ba719` |
| left bank: 75 down, 73-75 all at 1 | PLAYER 1 BALL IN PLAY 1, score 0,018,000 | - | - | `062b4c8f0f4b139f` |
| left bank: 73 back up |  | - | - | `062b4c8f0f4b139f` |
| left bank: 74 back up |  | - | - | `062b4c8f0f4b139f` |
| left bank: 75 back up |  | - | - | `062b4c8f0f4b139f` |
| tilt bob (30), first touch |  | - | - | `062b4c8f0f4b139f` |
| tilt bob (30), second touch |  | - | - | `062b4c8f0f4b139f` |
| tilt bob (30), third touch | TILT | - | - | `98bdc6143424df68` |
| slam tilt (29) | Credits 0 | - | - | `b05478368dc7edc4` |
