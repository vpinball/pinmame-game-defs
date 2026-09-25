# Earthshaker — ROM switch and coil name tables

Decoded by `tools/s11_rom_name_tables.py` from the user-authorized local ROM archives; no ROM
bytes are reproduced. Each table is a run of fixed 16-byte entries in the U26 program ROM. A byte
with bit 7 set is the character in its low seven bits followed by the display's period segment,
and the ROM font codes `o` and `p` for `-` and `/`. Entries are shown trimmed of padding.

| Driver | ROM member | Member SHA-256 | Switch table | Coil table |
| --- | --- | --- | --- | --- |
| esha_la3 | eshk_u26.l3 | `72371df80fc8b097a0694f3a3512e1cd7ca99e8804769ddd216c9d97dd794c62` | 0x12ec | 0x0fe3 |
| esha_la1 | u26-la1.rom | `4010722ee77bc60fca9ac27b748c4f126085c76adefd6d97aa406c5ce7e4b176` | 0x0f18 | 0x1af5 |
| esha_lg1 | u26-lg1.rom | `6c471f004eb12398579e9d531aa9b56714fe6bc89a2912271279a7317d871f5a` | 0x1791 | 0x0b19 |
| esha_lg2 | u26-lg2.rom | `3068bfc02ed450932df55c6a0f568bae4e5f9577cf9255ff3b29acbdf2267a60` | 0x167f | 0x1a6d |
| esha_ma3 | eshk_u26.l3 | `2b696581b3119a46d65300439f72a6580238fd1ac4298ab13d1d42981ce8bf2c` | 0x12ec | 0x0fe3 |
| esha_pa1 | u26-pa1.rom | `7ea4d98d94012ef76b2c13156b6f6093cd5f48426b70e2a0ead59e463a200a00` | 0x1616 | 0x13ee |
| esha_pr4 | eshk_u26.f1 | `d16fa0e39ea574f3344aac2ac770c222a52841b327cbaa52bd7881415d46f5f3` | 0x12ec | 0x0fe3 |

The local `esha_ma3.zip` stores its U26 program ROM under the member name `eshk_u26.l3`; its
SHA-1 (`8c1d5e4e0b4217055ad9e1490ff3dba52ef013f4`) is the one pinned `s11games.c` gives for
`eshk_u26.ma3`, so the bytes are the Metallica MOD ROM despite the member name. All seven member
SHA-1s match pinned `s11games.c`.

## esha_la3 switch table (public switch address = entry number)

| Switch | ROM text |
| --- | --- |
| 1 | PLUMB  TILT |
| 2 | A/C RELAY |
| 3 | CREDIT BUTTON |
| 4 | RIGHT COIN |
| 5 | CENTER COIN |
| 6 | LEFT COIN |
| 7 | SLAM  TILT |
| 8 | HIGH SCORE RESET |
| 9 | PLAYFIELD TILT |
| 10 | OUTHOLE |
| 11 | TROUGH   1 |
| 12 | TROUGH   2 |
| 13 | TROUGH   3 |
| 14 | R. INNER RETLANE |
| 15 | R. OUTER RETLANE |
| 16 | RIGHT OUTLANE |
| 17 | LEFT OUTLANE |
| 18 | LEFT RETURN LANE |
| 19 | LEFT STANDUP |
| 20 | EJECT HOLE |
| 21 | RIGHT STANDUP 1 |
| 22 | RIGHT STANDUP 2 |
| 23 | CAPTIVE BALL |
| 24 | BOTM. RT. STANDUP |
| 25 | BLDNG. 1 UNUSED |
| 26 | BLDNG. 2 UNUSED |
| 27 | LEFT DROP TARGET |
| 28 | CENTER DROP TARG. |
| 29 | RIGHT DROP TARGT. |
| 30 | CENTER STANDUP |
| 31 | RIGHT LOOP |
| 32 | LEFT LOOP |
| 33 | ON-RAMP 50K |
| 34 | ON-RAMP 25K |
| 35 | ON-RAMP 100K |
| 36 | ON-RAMP BYPASS |
| 37 | TOP BALL POPPER |
| 38 | DROP HOLE 1 |
| 39 | DROP HOLE 2 |
| 40 | BOTM. BALL POPPER |
| 41 | SPINNER |
| 42 | FAULT OPEN |
| 43 | RIGHT RAMP ENTRY |
| 44 | CENTR. RAMP ENTRY |
| 45 | CNTR. RAMP MIDDLE |
| 46 | CENTER RAMP END |
| 47 | UNUSED |
| 48 | UNUSED |
| 49 | UNUSED |
| 50 | SHOOTER LANE |
| 51 | UNUSED |
| 52 | LEFT JET BUMPER |
| 53 | RIGHT JET BUMPER |
| 54 | TOP JET BUMPER |
| 55 | LEFT SLINGSHOT |
| 56 | RIGHT SLINGSHOT |
| 57 | RIGHT FLIPPER |
| 58 | LEFT FLIPPER |

The table ends at entry 58; addresses 59-64 have no entry.

## esha_la3 coil table (table order)

The Auto Burn-in coil test (runtime evidence `evidence/runtime/system-11/earthshaker-la3-service-and-mechanisms.json`,
run `burnin-coil-test`) fires one public address per entry in this order; the address column is
that run's pulse, not a value stored beside the text.

| Entry | ROM text | Address pulsed at that step |
| --- | --- | --- |
| 1 | OUTHOLE | 1 |
| 2 | CAPTV. BALL FLASH | 25 |
| 3 | BALL RELEASE | 2 |
| 4 | CNTR. RMP. FLASH 1 | 26 |
| 5 | DROP TARGT. RESET | 3 |
| 6 | CNTR. RMP. FLASH 2 | 27 |
| 7 | CALIFORNIA FAULT | 4 |
| 8 | CNTR. RMP. FLASH 3 | 28 |
| 9 | EJECT HOLE | 5 |
| 10 | CNTR. RMP. FLASH 4 | 29 |
| 11 | BOTM. BALL POPPER | 6 |
| 12 | RGHT. RMP. FLASH 1 | 30 |
| 13 | KNOCKER | 7 |
| 14 | RGHT. RMP. FLASH 2 | 31 |
| 15 | UNUSED | 8 |
| 16 | RGHT. RMP. FLASH 3 | 32 |
| 17 | UNUSED | 9 |
| 18 | UPPER PLAYFLD. G.I. | 10 |
| 19 | INSERT G.I. | 11 |
| 20 | A/C   SELECT | 12 |
| 21 | TOP BALL POPPER | 13 |
| 22 | JACKPT/SUN FLASH | 14 |
| 23 | LOWER PLAYFLD. G.I. | 15 |
| 24 | JET BUMPER FLASH | 16 |
| 25 | LEFT JET BUMPER | 17 |
| 26 | LEFT SLINGSHOT | 18 |
| 27 | RIGHT JET BUMPER | 19 |
| 28 | RIGHT SLINGSHOT | 20 |
| 29 | TOP JET BUMPER | 21 |
| 30 | QUAKE MOTOR | 22 |

## Entries that differ from esha_la3

| Driver | Table | Entry | esha_la3 | This driver |
| --- | --- | --- | --- | --- |
| esha_la1 | switch | 8 | HIGH SCORE RESET | HI.  SCORE RESET |
| esha_lg1 | both | - | (no difference) | (no difference) |
| esha_lg2 | both | - | (no difference) | (no difference) |
| esha_ma3 | switch | 25 | BLDNG. 1 UNUSED | AMP  1 UNUSED |
| esha_ma3 | switch | 26 | BLDNG. 2 UNUSED | AMP  2 UNUSED |
| esha_ma3 | switch | 33 | ON-RAMP 50K | LGTNING 50K |
| esha_ma3 | switch | 34 | ON-RAMP 25K | LGTNING 25K |
| esha_ma3 | switch | 35 | ON-RAMP 100K | LGTNING 100K |
| esha_ma3 | switch | 36 | ON-RAMP BYPASS | LGTNING BYPASS |
| esha_ma3 | switch | 42 | FAULT OPEN | FIGHT FIRE |
| esha_ma3 | coil | 7 | CALIFORNIA FAULT | FIGHT FIRE FIGHT |
| esha_ma3 | coil | 30 | QUAKE MOTOR | CROWD MOTOR |
| esha_pa1 | switch | 8 | HIGH SCORE RESET | HI.  SCORE RESET |
| esha_pa1 | switch | 25 | BLDNG. 1 UNUSED | BLDNG HEIGHT 1 |
| esha_pa1 | switch | 26 | BLDNG. 2 UNUSED | BLDNG HEIGHT 2 |
| esha_pa1 | coil | 17 | UNUSED | BUILDING MOTOR |
| esha_pr4 | both | - | (no difference) | (no difference) |

The esha_l4c and esha_pa4 archives are not in the local ROM corpus, so their tables were not read.
