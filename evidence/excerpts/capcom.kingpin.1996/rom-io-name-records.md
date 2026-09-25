# Transcription: Kingpin program-ROM I/O name records and cited strings

Source: `rom-static.kingpin.kpb105-io-records` -- the kpb105 program ROM `u1hu1l.bin` (1,048,576 bytes, SHA-1 `c731e0b5c9b211574dda8aecbad799bc180a59db`, matching pinned `src/wpc/capgames.c`), decoded by `tools/capcom_kingpin_rom_records.py`. ROM bytes are not committed; this table is the tool's output.

Each record is `type:u8 length:u8 number:u16 name_pointer:u32 payload`, big-endian, at the listed ROM offset. `Public` is the tool's conversion of the ROM's internal number to the PinMAME public address; the service-menu excerpts observe every one of those conversions at runtime. For switches, `Opto` is bit 1 of payload byte 14. The table holds no records for the two CPU-driven flipper coils (public 9/10), for switches 1-13, 15-16, 40, 56 and 64-80, or for lamps 1, 2 and 123-125.

| Offset | Type | ROM number | Public | Name | Opto | Payload |
| --- | --- | --- | --- | --- | --- | --- |
| 0x0b453a | lamp | 39 | 3 | START BUTTON |  | `03030240` |
| 0x0b4546 | lamp | 55 | 4 | AUTO PLUNGER |  | `03030240` |
| 0x0b4552 | lamp | 71 | 5 | L. YOU'RE COVERED |  | `02010260` |
| 0x0b455e | lamp | 87 | 6 | L. OPEN HIDEOUT |  | `02010260` |
| 0x0b456a | lamp | 103 | 7 | R. YOU'RE COVERED |  | `02010260` |
| 0x0b4576 | lamp | 119 | 8 | R. OPEN HIDEOUT |  | `02010260` |
| 0x0b4582 | lamp | 6 | 9 | 6X SHOTGUN |  | `02010260` |
| 0x0b458e | lamp | 22 | 10 | 8X MACHINE GUN |  | `02010260` |
| 0x0b459a | lamp | 38 | 11 | 4X .45 AUTOMATIC |  | `02010260` |
| 0x0b45a6 | lamp | 54 | 12 | 2X REVOLVER |  | `02010260` |
| 0x0b45b2 | lamp | 70 | 13 | TREASURE HUNT |  | `02010260` |
| 0x0b45be | lamp | 86 | 14 | KID GUN LEFT |  | `02010260` |
| 0x0b45ca | lamp | 102 | 15 | KID GUN RIGHT |  | `02010260` |
| 0x0b45d6 | lamp | 118 | 16 | LIVE AGAIN |  | `02010260` |
| 0x0b45e2 | lamp | 5 | 17 | POWERUP PAYOLA |  | `02010260` |
| 0x0b45ee | lamp | 21 | 18 | DOUBLE SPIN CITY |  | `02010260` |
| 0x0b45fa | lamp | 37 | 19 | BUMP & ROLL'EM |  | `02010260` |
| 0x0b4606 | lamp | 53 | 20 | ARMS RACE |  | `02010260` |
| 0x0b4612 | lamp | 69 | 21 | SPIN CITY |  | `02010260` |
| 0x0b461e | lamp | 85 | 22 | LOCK 1 |  | `02010260` |
| 0x0b462a | lamp | 101 | 23 | LOCK 2 |  | `02010260` |
| 0x0b4636 | lamp | 117 | 24 | LOCK 3 |  | `02010260` |
| 0x0b4642 | lamp | 4 | 25 | POWER BAR 1 |  | `02010260` |
| 0x0b464e | lamp | 20 | 26 | POWER BAR 2 |  | `02010260` |
| 0x0b465a | lamp | 36 | 27 | POWER BAR 3 |  | `02010260` |
| 0x0b4666 | lamp | 52 | 28 | POWER BAR 4 |  | `02010260` |
| 0x0b4672 | lamp | 68 | 29 | POWER BAR 5 |  | `02010260` |
| 0x0b467e | lamp | 84 | 30 | POWER BAR 6 |  | `02010260` |
| 0x0b468a | lamp | 100 | 31 | POWER BAR 7 |  | `02010260` |
| 0x0b4696 | lamp | 116 | 32 | POWER BAR 8 |  | `02010260` |
| 0x0b46a2 | lamp | 3 | 33 | POWER BAR 9 |  | `02010260` |
| 0x0b46ae | lamp | 19 | 34 | POWER BAR 10 |  | `02010260` |
| 0x0b46ba | lamp | 35 | 35 | BONUS 2X |  | `02010260` |
| 0x0b46c6 | lamp | 51 | 36 | BONUS 4X |  | `02010260` |
| 0x0b46d2 | lamp | 67 | 37 | BONUS 6X |  | `02010260` |
| 0x0b46de | lamp | 83 | 38 | BONUS 8X |  | `02010260` |
| 0x0b46ea | lamp | 99 | 39 | BONUS 10X |  | `02010260` |
| 0x0b46f6 | lamp | 115 | 40 | SLOT GI (2) |  | `02010260` |
| 0x0b4702 | lamp | 2 | 41 | L. RAMP POWERUP |  | `02010260` |
| 0x0b470e | lamp | 18 | 42 | L. RAMP POINTS |  | `02010260` |
| 0x0b471a | lamp | 34 | 43 | L. DROP KING |  | `02010260` |
| 0x0b4726 | lamp | 50 | 44 | R. DROP PIN |  | `02010260` |
| 0x0b4732 | lamp | 66 | 45 | L. RAMP LOCK |  | `02010260` |
| 0x0b473e | lamp | 82 | 46 | RAMP STANDUP |  | `02010260` |
| 0x0b474a | lamp | 98 | 47 | R. RAMP POWERUP |  | `02010260` |
| 0x0b4756 | lamp | 114 | 48 | R. RAMP POINTS |  | `02010260` |
| 0x0b4762 | lamp | 1 | 49 | R. ORBIT POWERUP |  | `02010260` |
| 0x0b476e | lamp | 17 | 50 | R. ORBIT POINTS |  | `02010260` |
| 0x0b477a | lamp | 33 | 51 | U.R. STANDUP PTS |  | `02010260` |
| 0x0b4786 | lamp | 49 | 52 | U.R. CHARMED LIFE |  | `02010260` |
| 0x0b4792 | lamp | 65 | 53 | BIG AL |  | `02010260` |
| 0x0b479e | lamp | 81 | 54 | CAPTIVE BALL |  | `02010260` |
| 0x0b47aa | lamp | 97 | 55 | U.R. 2 BALL FURY |  | `02010260` |
| 0x0b47b6 | lamp | 113 | 56 | U.R. STANDUP GUN |  | `02010260` |
| 0x0b47c2 | lamp | 0 | 57 | BOSS KILL |  | `02010260` |
| 0x0b47ce | lamp | 16 | 58 | GET THE GUNS |  | `02010260` |
| 0x0b47da | lamp | 32 | 59 | BIG HEIST |  | `02010260` |
| 0x0b47e6 | lamp | 48 | 60 | RAMBLE & GAMBLE |  | `02010260` |
| 0x0b47f2 | lamp | 64 | 61 | DELIVER THE GOODS |  | `02010260` |
| 0x0b47fe | lamp | 80 | 62 | PAYOFF PANIC |  | `02010260` |
| 0x0b480a | lamp | 96 | 63 | DOUBLE CROSS |  | `02010260` |
| 0x0b4816 | lamp | 112 | 64 | HIT THE KINGPIN |  | `02010260` |
| 0x0b4822 | lamp | 15 | 65 | L. ORBIT POWERUP |  | `02010260` |
| 0x0b482e | lamp | 31 | 66 | L. ORBIT POINTS |  | `02010260` |
| 0x0b483a | lamp | 47 | 67 | JACKPOT |  | `02010260` |
| 0x0b4846 | lamp | 63 | 68 | SUPER JACKPOT |  | `02010260` |
| 0x0b4852 | lamp | 79 | 69 | L. TOPLANE |  | `02010260` |
| 0x0b485e | lamp | 95 | 70 | C. TOPLANE |  | `02010260` |
| 0x0b486a | lamp | 111 | 71 | R. TOPLANE |  | `02010260` |
| 0x0b4876 | lamp | 127 | 72 | L. SLOT STANDUP |  | `02010260` |
| 0x0b4882 | lamp | 14 | 73 | R. SLOT STANDUP |  | `02010260` |
| 0x0b488e | lamp | 30 | 74 | JACKPOT JUMP 2X |  | `02020220` |
| 0x0b489a | lamp | 46 | 75 | JACKPOT JUMP 4X |  | `02020220` |
| 0x0b48a6 | lamp | 62 | 76 | JACKPOT JUMP 6X |  | `02020220` |
| 0x0b48b2 | lamp | 78 | 77 | JACKPOT JUMP 8X |  | `02020220` |
| 0x0b48be | lamp | 94 | 78 | JACKPOT JUMP 10X |  | `02020220` |
| 0x0b48ca | lamp | 110 | 79 | JACKPOT JUMP 12X |  | `02020220` |
| 0x0b48d6 | lamp | 126 | 80 | JACKPOT JUMP 14X |  | `02020220` |
| 0x0b48e2 | lamp | 13 | 81 | L. STAR BUMPER |  | `02010260` |
| 0x0b48ee | lamp | 29 | 82 | C. STAR BUMPER |  | `02010260` |
| 0x0b48fa | lamp | 45 | 83 | R. STAR BUMPER |  | `02010260` |
| 0x0b4906 | lamp | 61 | 84 | G.I. 1 |  | `02010260` |
| 0x0b4912 | lamp | 77 | 85 | G.I. 2 (2) |  | `01010240` |
| 0x0b491e | lamp | 93 | 86 | G.I. 3 (2) |  | `01010240` |
| 0x0b492a | lamp | 109 | 87 | G.I. 4 (RED) |  | `02010260` |
| 0x0b4936 | lamp | 125 | 88 | G.I. 5 |  | `02010260` |
| 0x0b4942 | lamp | 12 | 89 | G.I. 6 |  | `02010260` |
| 0x0b494e | lamp | 28 | 90 | G.I. 7 (RED) |  | `02010260` |
| 0x0b495a | lamp | 44 | 91 | G.I. 8 |  | `02010260` |
| 0x0b4966 | lamp | 60 | 92 | G.I. 9 (RED) |  | `02010260` |
| 0x0b4972 | lamp | 76 | 93 | G.I. 10 |  | `02010260` |
| 0x0b497e | lamp | 92 | 94 | G.I. 11 (RED) |  | `02010260` |
| 0x0b498a | lamp | 108 | 95 | G.I. 12 (2) |  | `01010240` |
| 0x0b4996 | lamp | 124 | 96 | G.I. 13 (2) |  | `01010240` |
| 0x0b49a2 | lamp | 11 | 97 | G.I. 14 (2) |  | `01010240` |
| 0x0b49ae | lamp | 27 | 98 | G.I. 15 (2) |  | `01010240` |
| 0x0b49ba | lamp | 43 | 99 | G.I. 16 |  | `02010260` |
| 0x0b49c6 | lamp | 59 | 100 | G.I. 17 (RED) |  | `02010260` |
| 0x0b49d2 | lamp | 75 | 101 | CAPTIVE STANDUP |  | `02010260` |
| 0x0b49de | lamp | 91 | 102 | G.I. 19 (RED) |  | `02010260` |
| 0x0b49ea | lamp | 107 | 103 | G.I. 20 |  | `02010260` |
| 0x0b49f6 | lamp | 123 | 104 | G.I. 21 (RED) |  | `02010260` |
| 0x0b4a02 | lamp | 10 | 105 | G.I. 22 |  | `02010260` |
| 0x0b4a0e | lamp | 26 | 106 | G.I. 23 (RED) |  | `02010260` |
| 0x0b4a1a | lamp | 42 | 107 | G.I. 24 |  | `02010260` |
| 0x0b4a26 | lamp | 58 | 108 | G.I. 25 (RED) |  | `02010260` |
| 0x0b4a32 | lamp | 74 | 109 | G.I. 26 |  | `02010260` |
| 0x0b4a3e | lamp | 90 | 110 | G.I. 27 (RED) |  | `02010260` |
| 0x0b4a4a | lamp | 106 | 111 | G.I. 28 |  | `02010260` |
| 0x0b4a56 | lamp | 122 | 112 | G.I. 29 (RED) |  | `02010260` |
| 0x0b4a62 | lamp | 9 | 113 | G.I. 30 |  | `02010260` |
| 0x0b4a6e | lamp | 25 | 114 | G.I. 31 (RED) |  | `02010260` |
| 0x0b4a7a | lamp | 41 | 115 | G.I. 36 (RED) |  | `02010260` |
| 0x0b4a86 | lamp | 57 | 116 | BACKPANEL, LEFT |  | `02010260` |
| 0x0b4a92 | lamp | 73 | 117 | G.I. 32 (2) |  | `02010260` |
| 0x0b4a9e | lamp | 89 | 118 | G.I. 33 (2,RED) |  | `02010260` |
| 0x0b4aaa | lamp | 105 | 119 | BACKPANEL, CENTER |  | `02010260` |
| 0x0b4ab6 | lamp | 121 | 120 | BACKPANEL, RIGHT |  | `02010260` |
| 0x0b4ac2 | lamp | 8 | 121 | LEFT SPINNER |  | `02010260` |
| 0x0b4ace | lamp | 24 | 122 | RIGHT SPINNER |  | `02010260` |
| 0x0b4ada | lamp | 88 | 126 | BACKBOX G.I.(2) |  | `01020200` |
| 0x0b4ae6 | lamp | 104 | 127 | G.I. 34 (2) |  | `02010260` |
| 0x0b4af2 | lamp | 120 | 128 | G.I. 35 (2,RED) |  | `02010260` |
| 0x0b4afe | switch | 5 | 14 | AUTO PLUNGER | no | `005a10054d04000000050000006400004b80` |
| 0x0b4b18 | switch | 24 | 17 | R. RAMP SPINNER | yes | `005a10075ab200000018000000000200a340` |
| 0x0b4b32 | switch | 25 | 18 | R. RAMP EXIT | no | `005a10075ba2000000190000003200004340` |
| 0x0b4b4c | switch | 26 | 19 | L. RETURN | no | `005a100548d00000001a0000003200004b40` |
| 0x0b4b66 | switch | 27 | 20 | R. RETURN | no | `005a100548d00000001b0000003200004b40` |
| 0x0b4b80 | switch | 28 | 21 | L. OUTLANE | no | `005a100549c40000001c0000003200004b40` |
| 0x0b4b9a | switch | 29 | 22 | R. OUTLANE | no | `005a100549c40000001d0000003200004b40` |
| 0x0b4bb4 | switch | 30 | 23 | LEFT ORBIT | no | `005a10074b740000001e0000003200004b40` |
| 0x0b4bce | switch | 31 | 24 | RIGHT ORBIT | no | `005a10074c580000001f0000003200004b40` |
| 0x0b4be8 | switch | 40 | 25 | DROP K | no | `005a1006613600000000000a003200004340` |
| 0x0b4c02 | switch | 41 | 26 | DROP I | no | `005a1006613600000001000a003200004340` |
| 0x0b4c1c | switch | 42 | 27 | DROP N | no | `005a1006613600000002000a003200004340` |
| 0x0b4c36 | switch | 43 | 28 | DROP G | no | `005a1006613600000003000a003200004340` |
| 0x0b4c50 | switch | 44 | 29 | DROP P | no | `005a1006635400000000000a003200004340` |
| 0x0b4c6a | switch | 45 | 30 | DROP I | no | `005a1006635400000001000a003200004340` |
| 0x0b4c84 | switch | 46 | 31 | DROP N | no | `005a1006635400000002000a003200004340` |
| 0x0b4c9e | switch | 47 | 32 | CAPTIVE BALL | no | `00fa1005a6360000002f0000003200004b40` |
| 0x0b4cb8 | switch | 56 | 33 | EOS L | no | `005a100928c8000000380000000800004b80` |
| 0x0b4cd2 | switch | 57 | 34 | EOS R | no | `005a100928c8000000390000000800004b80` |
| 0x0b4cec | switch | 58 | 35 | OUTHOLE | no | `005a100928c80000003a014d03e800006380` |
| 0x0b4d06 | switch | 59 | 36 | TROUGH 1 | yes | `0000100928c80000003b03e803e80200e380` |
| 0x0b4d20 | switch | 60 | 37 | TROUGH 2 | yes | `0000100928c80000003c03e803e80200e380` |
| 0x0b4d3a | switch | 61 | 38 | TROUGH 3 | yes | `0000100928c80000003d03e803e80200e380` |
| 0x0b4d54 | switch | 62 | 39 | TROUGH 4 | yes | `0000100928c80000003d03e803e80200e380` |
| 0x0b4d6e | switch | 72 | 41 | L. SLING | no | `005a100546d2000000480000001400004b40` |
| 0x0b4d88 | switch | 73 | 42 | R. SLING | no | `005a100546d2000000490000001400004b40` |
| 0x0b4da2 | switch | 74 | 43 | SHOOTER | no | `005a100928c80000004a000a003200004340` |
| 0x0b4dbc | switch | 75 | 44 | GUN LOCK 1 | yes | `005a100928c80000004b01f401f40200e380` |
| 0x0b4dd6 | switch | 76 | 45 | GUN LOCK 2 | no | `005a100928c80000004c01f401f400006380` |
| 0x0b4df0 | switch | 77 | 46 | GUN LOCK 3 | no | `005a100928c80000004d01f401f400006380` |
| 0x0b4e0a | switch | 78 | 47 | RAMP, DOWN | no | `005a1007a9b200003cda00640064000073c0` |
| 0x0b4e24 | switch | 79 | 48 | GUN TROUGH OPTO | yes | `005a10073c1a0000004f003200000200a380` |
| 0x0b4e3e | switch | 16 | 49 | L. SLOT STANDUP | no | `005a100544fa000000100000003200004b40` |
| 0x0b4e58 | switch | 17 | 50 | R. SLOT STANDUP | no | `005a1005456e000000110000003200004b40` |
| 0x0b4e72 | switch | 18 | 51 | SLOT SAUCER | no | `005a100928c800000012000001f400006380` |
| 0x0b4e8c | switch | 19 | 52 | SLOT OPTO | yes | `005a100928c800000013001400000200a340` |
| 0x0b4ea6 | switch | 20 | 53 | L. TOPLANE | no | `005a10079e32000000140000003200004b40` |
| 0x0b4ec0 | switch | 21 | 54 | C. TOPLANE | no | `005a10079e32000000150000003200004b40` |
| 0x0b4eda | switch | 22 | 55 | R. TOPLANE | no | `005a10079e32000000160000003200004b40` |
| 0x0b4ef4 | switch | 32 | 57 | L. STAR BUMPER | no | `005a1005472c000000200000000a00004b40` |
| 0x0b4f0e | switch | 33 | 58 | C. STAR BUMPER | no | `005a1005472c000000210000000a00004b40` |
| 0x0b4f28 | switch | 34 | 59 | R. STAR BUMPER | no | `005a1005472c000000220000000a00004b40` |
| 0x0b4f42 | switch | 35 | 60 | UR. BALL STANDUP | no | `005a10054452000000230000003200004b40` |
| 0x0b4f5c | switch | 36 | 61 | L. RAMP SPINNER | yes | `005a100758e200000024000000000200a340` |
| 0x0b4f76 | switch | 37 | 62 | L. RAMP EXIT | no | `005a100759ca000000250000003200004b40` |
| 0x0b4f90 | switch | 38 | 63 | RAMP STANDUP | no | `005a100545e2000000260000003200004b40` |
| 0x0b4faa | coil | 15 | 1 | OUTHOLE |  | `0104100cdb1c0000000f` |
| 0x0b4fbc | coil | 14 | 2 | TROUGH |  | `0104100cda580000000f` |
| 0x0b4fce | coil | 13 | 3 | KNOCKER |  | `0104000000000000000f` |
| 0x0b4fe0 | coil | 12 | 4 | LEFT SLINGSHOT |  | `0104100bd71e0000000f` |
| 0x0b4ff2 | coil | 11 | 5 | RIGHT SLINGSHOT |  | `0104100bd71e0000000f` |
| 0x0b5004 | coil | 10 | 6 | KING DROP RESET |  | `0104100bd6840000000f` |
| 0x0b5016 | coil | 9 | 7 | PIN DROP RESET |  | `0104100bd55e0000000f` |
| 0x0b5028 | coil | 8 | 8 | GUN EJECT |  | `0104100bc4440000000f` |
| 0x0b503a | coil | 29 | 11 | SLOT EJECT |  | `0104100bc7100000000f` |
| 0x0b504c | coil | 28 | 12 | SLOT MOTOR |  | `0a080000000000000000` |
| 0x0b505e | coil | 27 | 13 | TOPGATES |  | `0104100bc5ec0000000f` |
| 0x0b5070 | coil | 26 | 14 | RAMP |  | `0104100bc9080000000f` |
| 0x0b5082 | coil | 25 | 15 | C. STAR BUMPER |  | `0104100bd8360000000f` |
| 0x0b5094 | coil | 24 | 16 | R. STAR BUMPER |  | `0104100bd8360000000f` |
| 0x0b50a6 | coil | 7 | 17 | L. STAR BUMPER |  | `0104100bd8360000000f` |
| 0x0b50b8 | coil | 6 | 18 | L. RAMP FLASHERS |  | `08060000000008000000` |
| 0x0b50ca | coil | 5 | 19 | L. KID FLASHER |  | `08060000000008000000` |
| 0x0b50dc | coil | 4 | 20 | BIG AL FLASHERS |  | `08060000000008000000` |
| 0x0b50ee | coil | 3 | 21 | GUN TIP FLASHERS |  | `08060000000008000000` |
| 0x0b5100 | coil | 2 | 22 | R. RAMP FLASHER |  | `08060000000008000000` |
| 0x0b5112 | coil | 1 | 23 | BUILDING FLASHER |  | `08060000000008000000` |
| 0x0b5124 | coil | 0 | 24 | R. KID FLASHER |  | `08060000000008000000` |
| 0x0b5136 | coil | 23 | 25 | CAPTIVE FLASHER |  | `08060000000008000000` |
| 0x0b5148 | coil | 22 | 26 | BUMPERS FLASHER |  | `08060000000008000000` |
| 0x0b515a | coil | 21 | 27 | POWER FLASHERS |  | `08060000000008000000` |
| 0x0b516c | coil | 20 | 28 | LEX FLASHER |  | `08060000000008000000` |
| 0x0b517e | coil | 19 | 29 | L.ORBIT (EAST) FLASHER |  | `08060000000008000000` |
| 0x0b5190 | coil | 18 | 30 | KING FLASHERS |  | `08060000000008000000` |
| 0x0b51a2 | coil | 17 | 31 | PIN FLASHERS |  | `08060000000008000000` |
| 0x0b51b4 | coil | 16 | 32 | AUTO PLUNGER |  | `0104100bab400000000f` |

Cabinet switch names, which the record table does not cover, are a separate NUL-terminated string list in the same ROM:

| Offset | String |
| --- | --- |
| 0x0d0cfc | COIN 1 |
| 0x0d0d03 | COIN 2 |
| 0x0d0d0a | COIN 3 |
| 0x0d0d11 | COIN 4 |
| 0x0d0d18 | LEFT FLIPPER |
| 0x0d0d25 | RIGHT FLIPPER |
| 0x0d0d33 | START BUTTON |
| 0x0d0d40 | COIN DOOR |
| 0x0d0d4a | SLAM |
| 0x0d0d4f | TILT |
| 0x0d0d54 | TOKEN EXTRA |
| 0x0d0d60 | TOKEN EXIT |
| 0x0d0d6b | TICKET NOTCH |
| 0x0d0d78 | LEFT FLIPPER |
| 0x0d0d85 | RIGHT FLIPPER |

Other program-ROM strings cited by the definition (NUL-terminated ASCII unless noted):

| Offset | Bytes / string | Use |
| --- | --- | --- |
| 0x0b85a2 | KING PIN | Title shown in the operator-menu header |
| 0x0b85ab | byte 0xE1 then "1.5" | Version shown in the header; the DMD font draws 0xE1 as a beta sign, giving "β1.5" (Krellan: "1.5β") |
| 0x0c3e24 | Disconnect the OPTO | C1.02 Opto Test prompt, line 1 |
| 0x0c3e88 | power connector J15 | C1.02 Opto Test prompt, line 2 |
| 0x0c3ed4 | from the Power Board | C1.02 Opto Test prompt, line 3 |
| 0x0c5836 | Check 50V Interlock SW. | 50 V coil-supply interlock message (English) |
| 0x0c584e | VERIFIE SW.PORTE 50V | Same message (French: check the 50 V door switch) |
| 0x0c5863 | PRUEFE 50V TUERSCHALTER | Same message (German: check the 50 V door switch) |
