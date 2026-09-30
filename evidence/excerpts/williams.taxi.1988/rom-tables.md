# Taxi legal U27 service tables

Four locally supplied ROM archives were inspected read-only. ROM bytes remain outside Git. Fixed16-byte label entries from U27; high attribute bit expands period, o/p are ROM-font hyphen/slash codes. z quote glyphs are retained as z unless runtime independently establishes their meaning. The complete58-entry switch and30-entry coil table regions follow; subsequent MUSIC OFF / MAIN THEME entries are music, not coils.

## taxi_l4

Archive SHA256 30f21e3aa2ed62e93d38953e410b0c92679f264b7252d0408aad1d3eb991c03c; member taxi_u27.l4 SHA256 b1271c2410a67388da397ffee860926fea43d1cda1cc8a498b0b1483ceb8512a (32768 bytes).

| Switch | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x1f8c | PLUMB  TILT |
| 2 | 0x1f9c | BALL  TILT |
| 3 | 0x1fac | CREDIT BUTTON |
| 4 | 0x1fbc | RIGHT COIN |
| 5 | 0x1fcc | CENTER COIN |
| 6 | 0x1fdc | LEFT COIN |
| 7 | 0x1fec | SLAM  TILT |
| 8 | 0x1ffc | HI.  SCORE RESET |
| 9 | 0x200c | PLAYFIELD TILT |
| 10 | 0x201c | OUTHOLE |
| 11 | 0x202c | TROUGH   1 |
| 12 | 0x203c | TROUGH   2 |
| 13 | 0x204c | JOYRIDE EJECT |
| 14 | 0x205c | "C"    LANE |
| 15 | 0x206c | "A"    LANE |
| 16 | 0x207c | "B"    LANE |
| 17 | 0x208c | LEFT  BUMPER |
| 18 | 0x209c | LEFT  KICKER |
| 19 | 0x20ac | RIGHT BUMPER |
| 20 | 0x20bc | RIGHT KICKER |
| 21 | 0x20cc | LOWER BUMPER |
| 22 | 0x20dc | SHOOTER LANE |
| 23 | 0x20ec | UPPER LANE ENTRY |
| 24 | 0x20fc | CARRY PASSENGERS |
| 25 | 0x210c | LEFT RAMP ENTRY |
| 26 | 0x211c | RIGHT RAMP ENTRY |
| 27 | 0x212c | LOLA  LEFT |
| 28 | 0x213c | LOLA  MIDDLE |
| 29 | 0x214c | LOLA  RIGHT |
| 30 | 0x215c | PINBOT TOP |
| 31 | 0x216c | PINBOT MIDDLE |
| 32 | 0x217c | PINBOT BOTTOM |
| 33 | 0x218c | RIGHT RAMP EXIT |
| 34 | 0x219c | LEFT RAMP EXIT |
| 35 | 0x21ac | CATAPULT |
| 36 | 0x21bc | RIGHT LOCK |
| 37 | 0x21cc | LEFT  OUTLANE |
| 38 | 0x21dc | LEFT RETURN LANE |
| 39 | 0x21ec | RIGHT OUTLANE |
| 40 | 0x21fc | RGHT RETURN LANE |
| 41 | 0x220c | NOT    USED |
| 42 | 0x221c | NOT    USED |
| 43 | 0x222c | SPINOUT KICKER |
| 44 | 0x223c | SPINOUT SWITCH |
| 45 | 0x224c | NOT    USED |
| 46 | 0x225c | NOT    USED |
| 47 | 0x226c | NOT    USED |
| 48 | 0x227c | NOT    USED |
| 49 | 0x228c | NOT    USED |
| 50 | 0x229c | NOT    USED |
| 51 | 0x22ac | NOT    USED |
| 52 | 0x22bc | NOT    USED |
| 53 | 0x22cc | NOT    USED |
| 54 | 0x22dc | NOT    USED |
| 55 | 0x22ec | NOT    USED |
| 56 | 0x22fc | NOT    USED |
| 57 | 0x230c | LANE CHANGE RGHT |
| 58 | 0x231c | LANE CHANGE LEFT |

| Coil service index | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x2daa | OUTHOLE |
| 2 | 0x2dba | PINBOT FLASHER |
| 3 | 0x2dca | BALL SERVE |
| 4 | 0x2dda | DRAC FLASHER |
| 5 | 0x2dea | CATAPULT |
| 6 | 0x2dfa | LOLA  FLASHER |
| 7 | 0x2e0a | LOLA  3 BANK |
| 8 | 0x2e1a | SANTA FLASHER |
| 9 | 0x2e2a | JOYRIDE EJECT |
| 10 | 0x2e3a | GORBIE FLASHER |
| 11 | 0x2e4a | PINBOT 3 BANK |
| 12 | 0x2e5a | LEFT RAMP FLASH |
| 13 | 0x2e6a | SPINOUT KICKER |
| 14 | 0x2e7a | RIGHT RAMP FLASH |
| 15 | 0x2e8a | RIGHT LOCK |
| 16 | 0x2e9a | SPINOUT FLASHER |
| 17 | 0x2eaa | BALL GATE |
| 18 | 0x2eba | INSERT G.I. |
| 19 | 0x2eca | PLAYFLD  G.I. |
| 20 | 0x2eda | A/C   SELECT |
| 21 | 0x2eea | CABINET BELL |
| 22 | 0x2efa | KNOCKER |
| 23 | 0x2f0a | JACKPOT FLASHER |
| 24 | 0x2f1a | JOYRIDE FLASHER |
| 25 | 0x2f2a | LEFT  BUMPER |
| 26 | 0x2f3a | LEFT  KICKER |
| 27 | 0x2f4a | RIGHT BUMPER |
| 28 | 0x2f5a | RIGHT KICKER |
| 29 | 0x2f6a | LOWER BUMPER |
| 30 | 0x2f7a | NOT   USED |

## taxi_l3

Archive SHA256 e1e62914dd2d49e58cedeba6971af12c615338de866e3f904b2bdfca0ef43e74; member taxi_u27.l3 SHA256 47377bfd02b3a8b00f9a2d0e1b777ed0b47b3c85e02d91a126b2b9d2aadf88f0 (32768 bytes).

| Switch | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x1f8c | PLUMB  TILT |
| 2 | 0x1f9c | BALL  TILT |
| 3 | 0x1fac | CREDIT BUTTON |
| 4 | 0x1fbc | RIGHT COIN |
| 5 | 0x1fcc | CENTER COIN |
| 6 | 0x1fdc | LEFT COIN |
| 7 | 0x1fec | SLAM  TILT |
| 8 | 0x1ffc | HI.  SCORE RESET |
| 9 | 0x200c | PLAYFIELD TILT |
| 10 | 0x201c | OUTHOLE |
| 11 | 0x202c | TROUGH   1 |
| 12 | 0x203c | TROUGH   2 |
| 13 | 0x204c | JOYRIDE EJECT |
| 14 | 0x205c | "C"    LANE |
| 15 | 0x206c | "A"    LANE |
| 16 | 0x207c | "B"    LANE |
| 17 | 0x208c | LEFT  BUMPER |
| 18 | 0x209c | LEFT  KICKER |
| 19 | 0x20ac | RIGHT BUMPER |
| 20 | 0x20bc | RIGHT KICKER |
| 21 | 0x20cc | LOWER BUMPER |
| 22 | 0x20dc | SHOOTER LANE |
| 23 | 0x20ec | UPPER LANE ENTRY |
| 24 | 0x20fc | CARRY PASSENGERS |
| 25 | 0x210c | LEFT RAMP ENTRY |
| 26 | 0x211c | RIGHT RAMP ENTRY |
| 27 | 0x212c | MARILYN LEFT |
| 28 | 0x213c | MARILYN MIDDLE |
| 29 | 0x214c | MARILYN RIGHT |
| 30 | 0x215c | PINBOT TOP |
| 31 | 0x216c | PINBOT MIDDLE |
| 32 | 0x217c | PINBOT BOTTOM |
| 33 | 0x218c | RIGHT RAMP EXIT |
| 34 | 0x219c | LEFT RAMP EXIT |
| 35 | 0x21ac | CATAPULT |
| 36 | 0x21bc | RIGHT LOCK |
| 37 | 0x21cc | LEFT  OUTLANE |
| 38 | 0x21dc | LEFT RETURN LANE |
| 39 | 0x21ec | RIGHT OUTLANE |
| 40 | 0x21fc | RGHT RETURN LANE |
| 41 | 0x220c | NOT    USED |
| 42 | 0x221c | NOT    USED |
| 43 | 0x222c | SPINOUT KICKER |
| 44 | 0x223c | SPINOUT SWITCH |
| 45 | 0x224c | NOT    USED |
| 46 | 0x225c | NOT    USED |
| 47 | 0x226c | NOT    USED |
| 48 | 0x227c | NOT    USED |
| 49 | 0x228c | NOT    USED |
| 50 | 0x229c | NOT    USED |
| 51 | 0x22ac | NOT    USED |
| 52 | 0x22bc | NOT    USED |
| 53 | 0x22cc | NOT    USED |
| 54 | 0x22dc | NOT    USED |
| 55 | 0x22ec | NOT    USED |
| 56 | 0x22fc | NOT    USED |
| 57 | 0x230c | LANE CHANGE RGHT |
| 58 | 0x231c | LANE CHANGE LEFT |

| Coil service index | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x2d06 | OUTHOLE |
| 2 | 0x2d16 | PINBOT FLASHER |
| 3 | 0x2d26 | BALL SERVE |
| 4 | 0x2d36 | DRAC FLASHER |
| 5 | 0x2d46 | CATAPULT |
| 6 | 0x2d56 | MARILYN FLASHER |
| 7 | 0x2d66 | MARILYN 3 BANK |
| 8 | 0x2d76 | SANTA FLASHER |
| 9 | 0x2d86 | JOYRIDE EJECT |
| 10 | 0x2d96 | GORBIE FLASHER |
| 11 | 0x2da6 | PINBOT 3 BANK |
| 12 | 0x2db6 | LEFT RAMP FLASH |
| 13 | 0x2dc6 | SPINOUT KICKER |
| 14 | 0x2dd6 | RIGHT RAMP FLASH |
| 15 | 0x2de6 | RIGHT LOCK |
| 16 | 0x2df6 | SPINOUT FLASHER |
| 17 | 0x2e06 | BALL GATE |
| 18 | 0x2e16 | INSERT G.I. |
| 19 | 0x2e26 | PLAYFLD  G.I. |
| 20 | 0x2e36 | A/C   SELECT |
| 21 | 0x2e46 | CABINET BELL |
| 22 | 0x2e56 | KNOCKER |
| 23 | 0x2e66 | JACKPOT FLASHER |
| 24 | 0x2e76 | JOYRIDE FLASHER |
| 25 | 0x2e86 | LEFT  BUMPER |
| 26 | 0x2e96 | LEFT  KICKER |
| 27 | 0x2ea6 | RIGHT BUMPER |
| 28 | 0x2eb6 | RIGHT KICKER |
| 29 | 0x2ec6 | LOWER BUMPER |
| 30 | 0x2ed6 | NOT   USED |

## taxi_lg1

Archive SHA256 c1eb1fd3b26d4cf243d6c794f80ccd3c2291c066e097aa5627e5ff92e2ebb8ba; member u27-lg1m.rom SHA256 8ead41ba89c92d95fd639a73c4be05a14a30c9f511fdc386261579663244109d (32768 bytes).

| Switch | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x201a | PLUMB  TILT |
| 2 | 0x202a | BALL  TILT |
| 3 | 0x203a | CREDIT BUTTON |
| 4 | 0x204a | RIGHT COIN |
| 5 | 0x205a | CENTER COIN |
| 6 | 0x206a | LEFT COIN |
| 7 | 0x207a | SLAM  TILT |
| 8 | 0x208a | HI.  SCORE RESET |
| 9 | 0x209a | PLAYFIELD TILT |
| 10 | 0x20aa | OUTHOLE |
| 11 | 0x20ba | TROUGH   1 |
| 12 | 0x20ca | TROUGH   2 |
| 13 | 0x20da | JOYRIDE EJECT |
| 14 | 0x20ea | "C"    LANE |
| 15 | 0x20fa | "A"    LANE |
| 16 | 0x210a | "B"    LANE |
| 17 | 0x211a | LEFT  BUMPER |
| 18 | 0x212a | LEFT  KICKER |
| 19 | 0x213a | RIGHT BUMPER |
| 20 | 0x214a | RIGHT KICKER |
| 21 | 0x215a | LOWER BUMPER |
| 22 | 0x216a | SHOOTER LANE |
| 23 | 0x217a | UPPER LANE ENTRY |
| 24 | 0x218a | CARRY PASSENGERS |
| 25 | 0x219a | LEFT RAMP ENTRY |
| 26 | 0x21aa | RIGHT RAMP ENTRY |
| 27 | 0x21ba | MARILYN LEFT |
| 28 | 0x21ca | MARILYN MIDDLE |
| 29 | 0x21da | MARILYN RIGHT |
| 30 | 0x21ea | PINBOT TOP |
| 31 | 0x21fa | PINBOT MIDDLE |
| 32 | 0x220a | PINBOT BOTTOM |
| 33 | 0x221a | RIGHT RAMP EXIT |
| 34 | 0x222a | LEFT RAMP EXIT |
| 35 | 0x223a | CATAPULT |
| 36 | 0x224a | RIGHT LOCK |
| 37 | 0x225a | LEFT  OUTLANE |
| 38 | 0x226a | LEFT RETURN LANE |
| 39 | 0x227a | RIGHT OUTLANE |
| 40 | 0x228a | RGHT RETURN LANE |
| 41 | 0x229a | NOT    USED |
| 42 | 0x22aa | NOT    USED |
| 43 | 0x22ba | SPINOUT KICKER |
| 44 | 0x22ca | SPINOUT SWITCH |
| 45 | 0x22da | NOT    USED |
| 46 | 0x22ea | NOT    USED |
| 47 | 0x22fa | NOT    USED |
| 48 | 0x230a | NOT    USED |
| 49 | 0x231a | NOT    USED |
| 50 | 0x232a | NOT    USED |
| 51 | 0x233a | NOT    USED |
| 52 | 0x234a | NOT    USED |
| 53 | 0x235a | NOT    USED |
| 54 | 0x236a | NOT    USED |
| 55 | 0x237a | NOT    USED |
| 56 | 0x238a | NOT    USED |
| 57 | 0x239a | LANE CHANGE RGHT |
| 58 | 0x23aa | LANE CHANGE LEFT |

| Coil service index | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x3126 | OUTHOLE |
| 2 | 0x3136 | PINBOT FLASHER |
| 3 | 0x3146 | BALL SERVE |
| 4 | 0x3156 | DRACULA FLASHER |
| 5 | 0x3166 | CATAPULT |
| 6 | 0x3176 | MARILYN FLASHER |
| 7 | 0x3186 | MARILYN 3 BANK |
| 8 | 0x3196 | SANTA FLASHER |
| 9 | 0x31a6 | JOYRIDE EJECT |
| 10 | 0x31b6 | GORBIE FLASHER |
| 11 | 0x31c6 | PINBOT 3 BANK |
| 12 | 0x31d6 | LEFT RAMP FLASH |
| 13 | 0x31e6 | SPINOUT KICKER |
| 14 | 0x31f6 | RIGHT RAMP FLASH |
| 15 | 0x3206 | RIGHT LOCK |
| 16 | 0x3216 | SPINOUT FLASHER |
| 17 | 0x3226 | BALL GATE |
| 18 | 0x3236 | INSERT G.I. |
| 19 | 0x3246 | PLAYFLD  G.I. |
| 20 | 0x3256 | A/C   SELECT |
| 21 | 0x3266 | CABINET BELL |
| 22 | 0x3276 | KNOCKER |
| 23 | 0x3286 | JACKPOT FLASHER |
| 24 | 0x3296 | JOYRIDE FLASHER |
| 25 | 0x32a6 | LEFT  BUMPER |
| 26 | 0x32b6 | LEFT  KICKER |
| 27 | 0x32c6 | RIGHT BUMPER |
| 28 | 0x32d6 | RIGHT KICKER |
| 29 | 0x32e6 | LOWER BUMPER |
| 30 | 0x32f6 | NOT   USED |

## taxi_p5

Archive SHA256 285ae1298b958e97714703cbcc7aedd88d6c05dfe231e62c29a8d94ca7eed296; member taxi_u27.p5 SHA256 31f5dc1570a84324f1f8475596ca37f8f55ffe14ba6cedc1d19d3b48bf332852 (32768 bytes).

| Switch | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x247f | PLUMB  TILT |
| 2 | 0x248f | BALL  TILT |
| 3 | 0x249f | CREDIT BUTTON |
| 4 | 0x24af | RIGHT COIN |
| 5 | 0x24bf | CENTER COIN |
| 6 | 0x24cf | LEFT COIN |
| 7 | 0x24df | SLAM  TILT |
| 8 | 0x24ef | HI.  SCORE RESET |
| 9 | 0x24ff | PLAYFIELD TILT |
| 10 | 0x250f | OUTHOLE |
| 11 | 0x251f | TROUGH   1 |
| 12 | 0x252f | TROUGH   2 |
| 13 | 0x253f | JOYRIDE EJECT |
| 14 | 0x254f | "C"   LANE |
| 15 | 0x255f | "A"   LANE |
| 16 | 0x256f | "B"   LANE |
| 17 | 0x257f | LEFT  BUMPER |
| 18 | 0x258f | LEFT  KICKER |
| 19 | 0x259f | RIGHT BUMPER |
| 20 | 0x25af | RIGHT KICKER |
| 21 | 0x25bf | LOWER BUMPER |
| 22 | 0x25cf | SHOOTER LANE |
| 23 | 0x25df | UPPER LANE ENTRY |
| 24 | 0x25ef | CARRY PASSENGERS |
| 25 | 0x25ff | LEFT RAMP ENTRY |
| 26 | 0x260f | RIGHT RAMP ENTRY |
| 27 | 0x261f | MARILYN LEFT |
| 28 | 0x262f | MARILYN MIDDLE |
| 29 | 0x263f | MARILYN RIGHT |
| 30 | 0x264f | PINBOT TOP |
| 31 | 0x265f | PINBOT MIDDLE |
| 32 | 0x266f | PINBOT BOTTOM |
| 33 | 0x267f | RIGHT RAMP EXIT |
| 34 | 0x268f | LEFT RAMP EXIT |
| 35 | 0x269f | CATAPULT |
| 36 | 0x26af | RIGHT LOCK |
| 37 | 0x26bf | LEFT  OUTLANE |
| 38 | 0x26cf | LEFT RETURN LANE |
| 39 | 0x26df | RIGHT OUTLANE |
| 40 | 0x26ef | RGHT RETURN LANE |
| 41 | 0x26ff | NOT    USED |
| 42 | 0x270f | NOT    USED |
| 43 | 0x271f | SPINOUT KICKER |
| 44 | 0x272f | SPINOUT SWITCH |
| 45 | 0x273f | NOT    USED |
| 46 | 0x274f | NOT    USED |
| 47 | 0x275f | NOT    USED |
| 48 | 0x276f | NOT    USED |
| 49 | 0x277f | NOT    USED |
| 50 | 0x278f | NOT    USED |
| 51 | 0x279f | NOT    USED |
| 52 | 0x27af | NOT    USED |
| 53 | 0x27bf | NOT    USED |
| 54 | 0x27cf | NOT    USED |
| 55 | 0x27df | NOT    USED |
| 56 | 0x27ef | NOT    USED |
| 57 | 0x27ff | LANE CHANGE RGHT |
| 58 | 0x280f | LANE CHANGE LEFT |

| Coil service index | U27 offset | ROM label |
| --- | --- | --- |
| 1 | 0x2e99 | OUTHOLE |
| 2 | 0x2ea9 | PINBOT FLASHER |
| 3 | 0x2eb9 | BALL SERVE |
| 4 | 0x2ec9 | DRACULA FLASHER |
| 5 | 0x2ed9 | CATAPULT |
| 6 | 0x2ee9 | MARILYN FLASHER |
| 7 | 0x2ef9 | MARILYN 3 BANK |
| 8 | 0x2f09 | SANTA FLASHER |
| 9 | 0x2f19 | JOYRIDE EJECT |
| 10 | 0x2f29 | GORBIE FLASHER |
| 11 | 0x2f39 | PINBOT 3 BANK |
| 12 | 0x2f49 | LEFT RAMP FLASH |
| 13 | 0x2f59 | SPINOUT KICKER |
| 14 | 0x2f69 | RIGHT RAMP FLASH |
| 15 | 0x2f79 | RIGHT LOCK |
| 16 | 0x2f89 | SPINOUT FLASHER |
| 17 | 0x2f99 | BALL GATE |
| 18 | 0x2fa9 | INSERT G.I. |
| 19 | 0x2fb9 | PLAYFLD  G.I. |
| 20 | 0x2fc9 | A/C   SELECT |
| 21 | 0x2fd9 | CABINET BELL |
| 22 | 0x2fe9 | KNOCKER |
| 23 | 0x2ff9 | JACKPOT FLASHER |
| 24 | 0x3009 | JOYRIDE FLASHER |
| 25 | 0x3019 | LEFT  BUMPER |
| 26 | 0x3029 | LEFT  KICKER |
| 27 | 0x3039 | RIGHT BUMPER |
| 28 | 0x3049 | RIGHT KICKER |
| 29 | 0x3059 | LOWER BUMPER |
| 30 | 0x3069 | NOT   USED |
