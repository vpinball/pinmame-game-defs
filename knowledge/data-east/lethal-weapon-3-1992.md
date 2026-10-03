# Lethal Weapon 3 (Data East, 1992)

Coverage: **partial - manual-verified I/O for the full 8x8 switch and lamp matrices with connector, wire-colour and drive-transistor wiring, all 22 printed coil-driver slots including the Left/Right relay pair, and nine source-reconciled mechanisms; the retained table provides normalized positions for all fitted playfield switches, 63 of 64 lamp addresses, fourteen playfield coil mechanisms, the modelled flasher effects, and 35 in-bounds GI emitters; held below author-ready because drive 3's left-side fitment, physical flasher sockets, the knocker location, spatial validation, switch polarity, and two source conflicts are not yet complete**

## Identity

Data East Lethal Weapon 3, 1992, `GEN_DEDMD32` - the 128x32 DMD generation, sound board DE2S. PinMAME roots the family at `lw3_208` with 9 drivers, every one sharing `init_lw3` and therefore one `lw3GameData`, so all nine present identical playfield hardware. Three of the nine are later software rather than factory firmware - a 2013 voices mod and two 2020 community rulesets - which run on this same cabinet and so remain driver variants rather than new games. The voices mod is also the one set whose sound ROMs differ, swapping two of three for `_vm` variants; the other eight are uniform.

## The addendum corrects the manual about the display

The manual as printed says, on printed page 23, that the display is **32 x 64** dots. It is wrong. The factory addendum of 2 July 1992 states "The display is made up of 32 X 128 Dots not 32 X 64 Dots", and that is what pinned PinMAME independently declares through `de_128x32DMD` and `SNDBRD_DEDMD32`. Without the addendum the manual and the emulator would appear to disagree about the display and the manual would have been the wrong side to believe. It is recorded as its own source, not folded into the manual's, because it is a primary factory correction.

## The address model, and where it differs from WPC and Whitestar

Data East runs on the shared Williams System 11 core (`s11.c`); there is no `de.c`. `s11.c` installs no switch or lamp conversion of its own, so it inherits PinMAME's sequential defaults. **Both printed matrices are column-major**: address = (column - 1) x 8 + row. Column 1 of the switch matrix is the cabinet/coin column.

- **There is no GI channel at all.** General illumination is **public solenoid 11**, printed "GENERAL ILLUM. RELAY" (K-1) and commented `// GI output` in `s11.c`'s own `lw3_` typing block. The retained script agrees, naming its callback `SolRelayGI`. This is the second Data East machine in the project to confirm it, from a different manual.
- **Public solenoid 10 is the Left/Right relay**, printed "L/R COIL RELAY", which re-publishes outputs 1-8 at 25-32. The retained script binds all eight right-side addresses to Flash1R through Flash8R, so the pairing is confirmed on both sides. The superseded legacy record omits address 10 entirely.
- **64 lamps, and every one is populated** - the printed chart carries no "Not Used" cell.
- **Solenoids 33-44 are permanently zero on this machine.** That conclusion is scoped to `lw3GameData`: other Data East/System 11-derived configurations can populate part of the range through `S11_PRINTERLINE` or `S11_SNDOVERLAY`.

## Public switches 15 and 16 are cabinet flipper buttons despite the matrix labels

The manual contradicts itself. Its switch-matrix chart names addresses 15 and 16 Left EOS and Right EOS, but the adjacent Switch Part Numbers table lists `15* Left Flip. Cab` and `16* Right Flip. Cab.` with part number `180-5048-01`, and its legend says `* Indicates Cabinet Switches`. The parts table is the more specific physical identification and agrees with both PinMAME and the known-working script, so the canonical labels are Left/Right Flipper Cabinet Button while the printed EOS aliases remain documented.

`core.c:1740-1741` writes the flipper **button** state into the addresses `FLIP_SWNO(15,16)` names, and because this game declares no `FLIP_SOL` the end-of-stroke simulation at `core.c:1756-1775` never runs, so no end-of-stroke state is modelled.

**The mirroring is mode-dependent, and an unqualified rule here would be wrong.** Those two `core_setSw` calls sit inside `#ifdef PROC_SUPPORT` / `if (!coreGlobals.p_rocEn)` at `core.c:1733`, under the comment "Only handle flipper switches if we're not in a real game, otherwise they will get physically activated anyway". In an ordinary emulation build the addresses are rewritten from the flipper button bits on every `core_updateSw` pass, so a recreation cannot publish an end-of-stroke reading on them. In a P-ROC build driving real hardware the writes are skipped, because physical switches supply the state instead.

The mirrored state comes from PinMAME's flipper column, `CORE_FLIPPERSWCOL` (internal column 11), which `core_swSeq2m(n) = n + 7` publishes at switches 81-88. With keyboard handling off (the LibPinMAME default) `core_updateSw` copies the right button (82) into 16 and the left button (84) into 15, and fabricates 45/46 from 82 and 47/48 from 84, so **a consumer drives 82/84, never 15/16**. The other six column positions are end-of-stroke and upper-button bits this driver does not use and the ROM cannot read, and are recorded unused.

The retained known-working VPW 2.0 script writes both addresses directly from the cabinet flipper key, at `script.vbs:928-929` on key down and `960-961` on key up. In an emulation build those writes are overwritten on the next update and have no effect; that is a defect of the table, not a fact about the machine. The table still works because the same keys reach `DE.VBS` `vpmKeyDown`/`vpmKeyUp`, which write `swLRFlip = 82` and `swLLFlip = 84`. An earlier revision of this note read the direct writes as what a P-ROC-mode consumer would need. In a P-ROC build `core_updateSw` skips the copy and the state comes from the physical switches, so the table's writes are not what a P-ROC consumer needs either.

The superseded legacy record labels them "Left/Right Flipper Button", which describes what the emulator publishes rather than what the manual prints; both are recorded here.

## Lamps bind through `vpmMapLights`, not `Lampz`

The retained table uses the older idiom: each light's own `TimerInterval` field IS its ROM lamp index, and the lights sit in an `AllLamps` collection. A resolver written for the newer `Lampz.MassAssign` convention finds **zero** lamps here and reports a clean-looking result, which is how it was nearly missed. Four addresses - 7, 9, 18 and 27 - drive two bulbs at genuinely different playfield positions; lamp 18's pair sits at opposite sides of the table. Each is placed individually rather than averaged, because a centroid between two real inserts is a coordinate with no bulb in it.

## Evidence and its limits

The contributor-supplied manual has **no text layer whatsoever** - 93 pages, 0 characters - so every table here was read from 400 dpi renders and transcribed by hand. Four excerpts are committed beside this definition and digest-checked.

Spatial placement rests on one canonical VPW 2.0 extraction whose playfield is 952 x 2162. Fourteen playfield coils are placed at the retained Kicker, Bumper, Plunger, target-bank or slingshot mechanism they actuate, with the manual location drawing independently confirming the physical feature; these are mechanism locations, not invented winding centers. The knocker remains unplaced because the printed drawing has no readable 8L callout and the script's `KnockerPosition` is only a sound-placement helper. Driver 3 also remains unplaced and has unknown fitment: the drive table prints no coil while the same manual's location drawing clearly prints `3L` in the lower-right shooter-housing/cabinet extension without naming the device. The retained script also binds direct flashers 9 and 16, muxed flashers 25-32, and the solenoid-11 GI relay to exact Light objects; all in-bounds visual effects are retained individually, while the `GI_BG` object is excluded because its negative raw y coordinate makes it an off-playfield proxy.

Flasher Light objects are presentation effects rather than a physical socket survey. Their counts are lower than the manual bulb quantities at addresses 9, 16, 25-27, 29, 31 and 32; address 30 is the opposite mismatch, with four retained effects for three printed bulbs, and is preserved as `conflict.drive-6-flasher-effect-count`. Address 28 happens to match three-to-three, but count agreement alone still does not prove socket identity. Three additional local tables were inspected during maintainer review, but their credits establish a Javier to 32Assassin to VPW derivative chain, so they are not independent corroboration. Every coordinate therefore remains `observed` until an independent recreation or a complete original-machine location/socket survey agrees.

The drive-6 label is reconciled by the manual's own location drawing. Its drive table says `LEFT 3 BANK`, but printed page 28 places callout 6L beside the center drop-target bank, agreeing with the switch chart and the known-working script's `dtM` binding. The definition therefore calls the device Center Drop-Target Bank Reset while preserving `Left 3 Bank` as the manual wording; the relay-half name alone does not establish left-versus-center placement, as drive 7 appears in the same printed Left coil column but is named `RIGHT 3 BANK`.

## ROM-internal game state and operator settings

Everything in this section and the next is **contributor-reported candidate/observed firmware evidence**, gathered for a Total Recall re-theme of this table between 5 September and 3 October 2026 and listed under "ROM-level sources" at the end of this note. It asserts nothing about physical devices, wiring, polarity or placement, and none of it is promoted into the definition. Each fact names its proof:

- **code**: read from a 6800 disassembly of the CPU ROM;
- **rig**: observed in VPinMAME driven headlessly through its COM controller, with switches closed in the order a ball would trip them and no VPX, physics or ball, at about 10.7x real time unless stated;
- **prediction**: a value stated before the run and then produced by the ROM in the rig;
- **map**: `lw3_208.map.json` from tomlogic's Pinball Memory Maps project, whose ROM list includes both `lw3_208` and `lw3_301`.

**ROM scope.** The work ran on `lw3_301`, the unofficial 3.01 fan patch (CPU 3.01 and display 3.00 over the unchanged 2.08 sound ROMs), not on factory firmware. For addresses and routines, only two things were checked on `lw3_208`: the tomlogic base fields, which that map was written for, and the music-selection window below; every other address and routine here is verified on `lw3_301` only. The sound-command evidence spans both: captures before 5 September 2026 are `lw3_208`, later ones `lw3_301`, and the two share their sound ROMs. The patch's own code occupies 0xFD00-0xFFFF, so anything routed through it - the start-of-ball save, Leo award 20, the 0xFD43 award-0 hook - does not exist in this form on 2.08. The operator strings were read from the 3.00 display ROM `lw3drom1.300`, not from 2.08's `lw3drom1.a26`.

**Address space.** The main CPU is a 6808 with 8 KB of RAM at 0x0000-0x1FFF, and reset clears everything below 0x1600, so 0x1600-0x1FFF is the battery-backed part (code). `Controller.NVRAM` returns 8238 bytes on this driver, and every RAM address below is a raw index into it: tomlogic's offsets read correctly unshifted and wrong when shifted by the 46-byte difference (rig). Data East's `ChangedNVRAM` returns no array, so a table polls and diffs the full image. 0x2C00 and 0x3402 are I/O ports, not RAM.

### Game state

| Address | Meaning | Encoding | Proof |
| --- | --- | --- | --- |
| 0x01A2 | current player; 0 means no game is running | int | map; rig |
| 0x01A3 | current ball | int | map; rig |
| 0x01A5 | players in the game | int | map; rig |
| 0x01C1 + i, then 0x01B1 + 4i to 0x01B4 + 4i | player i+1 score (i = 0-3), five BCD bytes, the most significant held apart from the other four | bcd | map |
| 0x16CE | credits | bcd | map; rig |
| 0x0024 bit 7 | EXTRA BALL lit: lamp 40's blink-plane bit, the ROM's own lit state; light shows do not touch it | bit | code + rig |
| 0x01C5 | extra balls pending (shoot again) | int | code |
| 0x01C6 | start-of-ball save: 0x01 armed, 0x09 expired, bit 7 set once the save is spent; cleared at the next ball | flags | code + rig, 3.01 only |
| 0x0810-0x0813 | ball time, four BCD bytes of seconds, ticked once a second and paused while a ball is held in a saucer | bcd | code + rig, 3.01 only |
| 0x04D6 | match number, written at 0xDA78 from the high nibble of 0x03E3 | bcd | code + one rig sighting |
| 0x0183 | byte the CPU stages for the display board; see "Display and attract" | raw | rig; meanings retracted |
| 0x0184 / 0x0185 | next sound command / last command sent | raw | code |

Lamp state lives in two planes: lamp n is bit `(n-1) & 7` of byte `0x18 + ((n-1) >> 3)` (on) and of `0x20 + ((n-1) >> 3)` (blink), and 0x0000-0x0007 hold the masks 0x01-0x80 (code). That is why 0x001B, the on-plane byte for lamps 25-32, steps 0/8/24/56/120 with the bonus-multiplier lamps 28-31; it is lamp output, not game state.

### Rule state

| Address | Meaning | Proof |
| --- | --- | --- |
| 0x140F | stunt rung. Between stunts it is the number completed this ball (0-5) and the next stunt is value + 1, wrapping 6 to 1; during a stunt it already holds the current rung, because the ROM increments it before dispatching | prediction: 9 of 9 over 10 cycles, all six rungs and the wrap; the cycle that started no stunt left it unchanged |
| 0x1406 / 0x1407 / 0x1408 | Lethal Weapon 1 / 2 / 3 collect latches: 0x80 this one is next, 0x01 collected, 0x00 idle. Completing the set resets 0x1406 to 0x80 and steps 0x140F; the LW1 collect arms 0x1407 at 0x8F82 and the LW2 (VUK) collect arms 0x1408 at 0x8FB7, so 0x1408 is armed only by the LW2 collect | code + rig |
| 0x1400-0x1405 | drop-bank completions, any bank in any order: the first sets 0x1400 and 0x1403, the second 0x1401 and 0x1404, the third 0x1402 and 0x1405 together with the pending-multiball byte 0x1019 | rig, 30 Sep re-run superseding a per-bank reading |
| 0x1018 / 0x1019 | multiball gate (0x81 while it runs) / multiball pending. Entry 0x7A8F requires 0x1018 = 0 and 0x1019 non-zero; the body at 0x7A9A clears 0x1019 | code + rig |
| 0x1420 | multiball status: incremented by the multiball body and read as a gate at 0x73B5, 0x7635, 0x779C, 0x8D38 and 0x8D4E; 0 outside multiball, 1 throughout every scripted multiball | code + rig |
| 0x1421 | jackpots collected this multiball, incremented in the collect routine | code + rig |
| 0x1422 | replays scored this game | code |
| 0x1423 | specials (free games) awarded this game | code |
| 0x1424 | extra balls earned this game | code |
| 0x1426 | Freeway ramps made, BCD, incremented at 0x781A | code + rig |
| 0x1429 | bonus multiplier: 0 means 1X, otherwise the literal 2, 4, 6 or 8 | rig |
| 0x142B | end-of-ball bonus, BCD in units of 10,000: paid = BCD x 10,000 x multiplier; zeroed the moment it is paid | prediction: 3 of 3 |
| 0x142E | 3 during a game and 0 outside; balls per game, or a balls-remaining count that never decremented in single-ball runs | rig, medium |
| 0x1409 | music track 0-2; it keeps its value across games | code + rig |
| 0x140A-0x140D | the selected track's four cue bytes, copied by 0xAD5F from the table at 0xAD84: select cue, play cue, 0x04, 0x05 | code |
| 0x10FA / 0x10FB | music-selection countdown, BCD | code + rig |
| 0x10FD / 0x10FE | ramp count at which the next ramp award comes / that award's code, from the table at 0xB0F5: 3, 7, 13, 21, 31, 43, 57, 73, 91 | code; no award at a listed count was checked in the rig. Every entry is odd, which fits the changelog's "awards on ODD ramp shots", but the changelog also lists 2.08's climbing ramp values as 3, 7, 14, 21, 31, 43, 57, 73, 91, 99 million, so counts against values is a reading of the code alone |
| 0x16F1 | ramps needed for EXTRA BALL LIT, 0 when the limit or lamp 40 forbids it | code; see the discrepancy below |
| 0x109D | Leo Getz award index, 0-20 | code + rig |
| 0x10A4 | Leo award in progress | rig |
| 0x10A1 / 0x10A2 / 0x10A3 | super-wheel choice window (80 at open, held one second, then one tick per about 66 ms) / left-flipper award / right-flipper award | rig |
| 0x109E | pointer to the active Leo wheel table | rig |
| 0x1C84 / 0x1C85 | the machine's lifetime extra-ball percentage, computed at 0xBFF8 from the counters at 0x1C24 and 0x1C04 | code |

**Readings corrected by later evidence.** The 5 September map read 0x1422 as "double jackpot armed" and 0x1426 as "jackpot value level", both at medium confidence from two scripted multiballs. The 3 October code reading makes them replays this game and Freeway ramps made. Multiball jackpots are collected on the Freeway ramp, so a ramp counter steps once per jackpot and once more on the two-ramp double, which accounts for the earlier 0x1426 correlation; a replay scored during the high-scoring double would account for 0x1422, but that was not checked against the recording. A 6 September note that 0x142B counts sinkhole visits is superseded by the 8 September bonus prediction.

**Unresolved.** The same source names the Freeway extra-ball target both 0x16F1 and 0x16F2 (the latter "starts at 17 on 3.01 and is re-derived from the lifetime percentage at ball start", 0xB036), and the rig image holds 0x23 at 0x16F1 against the changelog's 17; neither is explained. 0x105C follows the stunt ladder with the values 5, 16, 21, 32, 37 and 80 and is not decoded. Freeway ramps are cleared at ball start unless 0x1E82 is non-zero (0xB0A0), a save flag whose menu entry is not tied. The Uzi clip count, the Million Plus count and the Getaway hurry-up value produced no RAM candidate under any label tried; the contributor's reading, not demonstrated, is that the ROM keeps them as locals of tasks suspended in the coroutine sleep at 0x58D9, which an NVRAM image cannot show. The three-second Lethal Weapon 1 save and the five-second Tri-Ball save likewise have no countdown byte.

### Rules read from code

- **Start-of-ball save (3.01 only).** The once-a-second task at 0x43A8 calls 0xFCE1, which sets 0x01C6 from 0x0813 unless it is already 0x10 or above or has bit 7 set: 0 gives 0x00, 1-9 gives 0x01 (armed), 10 or more, or 0x0812 non-zero, gives 0x09 (expired). The drain path at 0xFE28 / 0xFE6E saves when 0x01C6 is 1-4: audit 0x1D44 FREEZE USED + 1, sound script 0x9E (heard as 0x51), 0x01C6 bit 7 set. While armed, seconds left = 10 - BCD(0x0813), and the window opens at the first playfield switch rather than at the serve. Rig: a drain at ball time 06 was saved; a drain at 20 was not. The 3.01 changelog gives 10 s at ball start (2.08: "4 switches"), 3 s after the LW1 eject outside Tri-Ball and 5 s at Tri-Ball start, and the contributor found no ball-save entry in the manual's adjustment table.
- **Extra ball.** One routine, 0x9694, lights it: lamp 40 to blink, display script 0xFC4C, light show 0xB0, sound script 0x98 (heard as 0x4F then 0xA6). It has two callers: Leo award 0 (0x968E via the patch hook 0xFD43), which bumps audit 0x1D24 EXBALL LIT FROM LEO about three seconds before the callout, and the ramp count at 0x783A, which bumps 0x1D20 EXBALL LIT FROM RAMP when 0x1426 reaches the target and lamp 40 is not lit. Collecting it (0x9275, then 0x5661) adds 1 to 0x1424 and 0x01C5, lights lamp 17 Shoot Again and bumps 0x1C24 while 0x1424 is under Ad 06; at the limit it pays 5,000,000 instead (0x56A1, a 3.01 rule).
- **Leo Getz wheel.** Each award has a predicate in the 21-entry table at 0x956B, and the wheel redraws until one passes, before any animation; the 1.3 s spin on the display is presentation only. Award 0's predicate (0x9662) refuses when Ad 06 is 0, an extra ball is pending, 0x1424 has reached Ad 06, the lifetime percentage has reached E Ad 42, or lamp 40 is already lit; award 19 (0x9637) adds a 50 % draw. The wheel tables are per ball at 0x94D0, 0x94E0 and 0x94F0, and ball 1's holds no award 0. Tournament mode skips the random number in the picker (0x6FE4). Rig: 0x109D is final about 50 ms after 0x10A4 rises, so read it at least two polls later; a 0 there is real only together with the 0x1D24 step.
- **Replay and special.** The score is compared with the replay levels at 0xDF65. The award follows Ad 04 (0x1E17): 1 gives an extra ball (0x1424 + 1 while under Ad 06); otherwise a credit, with 0x1422 + 1, while 0x1422 + 0x1423 is under Ad 05 (0x563B, knocker 0x47D3, display script 0xFC84). Leo award 1, SPECIAL, runs 0x56A7: Ad 04 = 0 pays nothing, 1 an extra ball, otherwise 0x1423 + 1; its predicate 0x96AE needs 0x1423 = 0 and a random draw. Code only; no rig run.
- **Stunts.** Completing the Lethal Weapon 1-2-3 set starts the next rung of High Fall, Car Crash, Toilet Bomb, Explosion, Helicopter and Super Stunt Spectacular, awarding 5, 10, 15, 20, 25 and 50 million in BCD with lamps 49-53 (code), then resets. The 3.00 display ROM's lamp test names lamps 49-53 5, 10, 15, 20 and 25 MILLION, matching the code, while the manual's lamp chart names them 3, 6, 9, 12 and 15 Million; whether 2.08 awards the manual's values was not checked. The same lamp test calls lamp 44, the manual's Silent Alarm, M.BALL READY. The three holes are the left saucer (switch 40, solenoid 4), the VUK (switch 31, solenoid 15) and the right saucer (switch 32, solenoid 5) (rig).
- **Tri-Ball.** Three drop-bank completions in any order arm it, the third sending the Tri-Ball ready cue, and a VUK shot then starts it (rig, 30 Sep; an earlier reading of two passes is superseded). The 3.01 changelog gives a 20,000,000 initial jackpot, which the first scripted collection paid (+20,260,010 with incidental scoring). Whether the jackpot must be re-lit between collections is unresolved: the run that suggested it could not hold a multiball without real balls.
- **Shoot-out.** Verdict code 0x88EC-0x8932: the loop at 0x891B waits while 0x108C = 6; a trigger inside the window bumps audit 0x1DBC SHOOTOUT VICTORYS, increments 0x1410 and pays the award loop at 0x8932, and two expired windows bump 0x1DC0 SHOOTOUT DEFEATS with no award. Rig: the trigger wins when it lands 0.15-0.5 s after cue 0x00D5, and the counters, not the callouts, are the reliable verdict.
- **Music selection.** The selector task at 0xB450 opens once per game at the start press, on ball 1 only. Right flipper steps the track up, left steps it down, both end the selection; 0xB529 commits it and the expiry bumps MUSIC 1, 2 or 3. On `lw3_301` the USE FLIPPERS TO SELECT MUSIC screen showed for about 0.36 s after the start press in two real-time runs; on `lw3_208` it held for about 7.3 s with 0x005D ticking every 0.5 s. The patch therefore leaves the selector effectively unusable in VPinMAME.
- **Bonus multiplier.** A flipper press rotates the lit top lanes, and completing the three advances the multiplier; cue 0x00DC is sent on that advance only (rig, one advance in 27 hits).
- **Ball search** starts 15.3 s after the last switch and repeats every 17-18 s (rig); there is no adjustment for it.

### Operator adjustments

The adjustment block occupies 0x1E00-0x1E59 on the rig's image, and 0x1E5A onward reads 0xFF. The bytes tied to a menu entry so far, with the menu numbers as the contributor read them from the operations manual's adjustment table (Ad 01 to E Ad 56, not re-checked here):

| Address | Adjustment | Rig value | Tied by |
| --- | --- | --- | --- |
| 0x1E04 | Free play | - | map |
| 0x1E0D | E Ad 15 Balls per game | 03 | code (0x4ED0, 0x81CC); map gives BCD |
| 0x1E0E | E Ad 16 Tilt warnings | 02 | code: Tournament ON writes 02 at 0x9D24 |
| 0x1E0F | Maximum credits | - | map, BCD |
| 0x1E16 | Ad 03 Replay levels | 01 | code: Tournament ON writes 00 (none), OFF writes 01 |
| 0x1E17 | Ad 04 Game awards: 0 none, 1 extra ball, otherwise credit | 02 | code (0x56A7) |
| 0x1E18 | Ad 05 Limit freegame | 03 | code (0x5641) |
| 0x1E19 | Ad 06 Limit extra balls | 03 | code (0x5664) |
| 0x1E1A | E Ad 42 Extra ball percentage | 0x25 (25 %) | code (0x9650, 0x967C, 0xABCE, 0xB04D) |
| 0x1E53 | Ad 39 Tournament mode (on 2.08 this entry is Next Game Promo) | 00 | code (0x6FE4, 0x9D11) |

0x1E01 is carried to the sound board in the three-byte control message 0x0024; its menu entry is not tied. Turning Tournament mode on (0x9D11) also writes 0x1E0E = 02, 0x1E16 = 00, 0x1E17 = 00 and 0x1E19 = 00, so with it on neither the Leo wheel nor the ramp can light an extra ball. A scripted game run twice, tournament off and on, unlocked no unheard sound command and still played the match. The service buttons are not in the switch matrix, so the rig changes adjustments by writing these bytes.

The display ROM holds the operator text as NUL-separated ASCII: 336 switch, coil and test strings at 0x04000-0x06000, 153 player-facing strings at 0x15C00-0x163E9, the audit names at 0x163E9-0x16A30, and 198 adjustment and menu strings at 0x16A30-0x17600. The 198 mix adjustment names, setting words, design credits, instruction-card lines and German translations. The adjustment names, in ROM order, are: EXPAND ADJUSTS, MATCH PERCENT, BALLS PER GAME, TILT WARNINGS, REPLAY BOOST, CREDITS LIMIT, HISCORES ALLOWED, HISCORE 1-4 AWARDS, BACKUP WORLD RECORD, BACKUP HISCORE 1-5, RESET H.S.T.D. EVERY, VIDEO MODES, FREE PLAY, CUSTOM MESSAGE, ATTRACT MUSIC, FLASH LAMPS, COILS PULSE, LEVEL ADJUST BY, INSTALL COUNTRY, TOURNAMENT MODE, BUYIN ALLOWED, RESTART GAME, EXTRA BALL PERCENT, VOLUME CONTROL, BILL VALIDATOR, POLICE LIGHT, GUN ENABLED, SAVE 3 BANKS, SAVE UZI, SAVE RAMP EX. BALLS, L.W. 1-2-3 STYLE, SAVE STUNTS, 3 BANK STYLE, SPOT 3 BANK STYLE, RERACE STYLE, SAVE LW 1,2,3 and CUSTOM PRICING; the audit-name block ends with REPLAY/MANUAL, START REPLAY, REPLAY LEVELS, GAME AWARDS, LIMIT FREEGAME, LIMIT EX BALLS, GAME RULES and GAME PRICE. Only the bytes in the table above are tied to a name. The 3.01 changelog adds two numbered entries: it changes the default of Adjustment 50, "Earning LW 1,2,3", from 02 (FACTORY) to 00 (EXHARD) so that the three holes must be collected in order, and it lets Victory Lap run when Adjustment 4, Game Awards, is set to Extra Ball.

### Replay levels and high scores

Replay levels sit at 0x1668 + 5i as five-byte BCD (code: 0xDF60 computes 5i, 0xDF65 compares). The audits name four replay levels, which end at 0x167B where the high-score table begins. The high-score table (map) holds six entries: the low four score bytes at 0x167C + 4i, the most significant at 0x1694 + i, and three initials at 0x16BA + 3i. The display ROM's rank titles are CHIEF OF POLICE, DEPUTY CHIEF, COMMANDER, LIEUTENANT, SERGEANT and PATROLMAN.

### Audits

Audits are four-byte BCD counters bumped by `LDX #address / JSR $604A` (code), and the display ROM lists 111 audit names. Their addresses are derived: address = 0x1D4C + 4 x (index - 58), skipping a three-letter fragment at raw index 79 that would otherwise shift every name above 0x1DA0 by one. The formula is validated over 0x1D14-0x1DE0 only. It is anchored on the multiball routine, which bumps TRI-BALL AWARD and, on a restart, RERACE AWARD; four routines that each bump two counters produce names that belong together (0x7AB8, 0x92D6, 0xA130, 0xA192); 0x1DB4 stepped 30 times for 30 left orbits in the rig; and audit steps coincide with independently bound sound cues. Below 0x1D14 the formula is wrong: no counter it places there moves on a coin insert in 64 recordings, while 0x16A5, 0x16AD, 0x16B1 and 0x16B5-0x16B7 do. 0x1C04 and 0x1C24 are read as the ball and extra-ball totals by the percentage code at 0xBFF8.

| Index | Address | Name | | Index | Address | Name |
| --- | --- | --- | --- | --- | --- | --- |
| 44 | 0x1D14 | DRAINS LEFT | | 70 | 0x1D7C | STUNT 3 |
| 45 | 0x1D18 | DRAINS CENTER | | 71 | 0x1D80 | STUNT 4 |
| 46 | 0x1D1C | DRAINS RIGHT | | 72 | 0x1D84 | STUNT 5 |
| 47 | 0x1D20 | EXBALL LIT FROM RAMP | | 73 | 0x1D88 | SUPER STUNT |
| 48 | 0x1D24 | EXBALL LIT FROM LEO | | 74 | 0x1D8C | SUPER SPINNER READY |
| 49 | 0x1D28 | # OF 2X MADE | | 75 | 0x1D90 | CRAZY RIGGS |
| 50 | 0x1D2C | # OF 4X MADE | | 76 | 0x1D94 | LEO GETZ AWARD |
| 51 | 0x1D30 | # OF 6X MADE | | 77 | 0x1D98 | SUPER LEO GETZ |
| 52 | 0x1D34 | # OF 8X MADE | | 78 | 0x1D9C | GETAWAY AWARD |
| 53 | 0x1D38 | # OF BONUS HOLDS | | 79 | 0x1DA0 | LOOPING AWARD |
| 54 | 0x1D3C | LASER KICK USED | | 80 | 0x1DA4 | MAX # OF RAMPS |
| 55 | 0x1D40 | # SUPER LEO EXBALL | | 81 | 0x1DA8 | SUPER LETHAL WEAPON |
| 56 | 0x1D44 | FREEZE USED | | 82 | 0x1DAC | MPLUS TO 5M AWARD |
| 57 | 0x1D48 | TRI-BALL LIT | | 83 | 0x1DB0 | START FIGHT |
| 58 | 0x1D4C | TRI-BALL AWARD | | 84 | 0x1DB4 | LEFT ORBITS |
| 59 | 0x1D50 | RERACE AWARD | | 85 | 0x1DB8 | RIGHT ORBITS |
| 60 | 0x1D54 | JACKPOT LIT | | 86 | 0x1DBC | SHOOTOUT VICTORYS |
| 61 | 0x1D58 | 1 JACKPOT AWARD | | 87 | 0x1DC0 | SHOOTOUT DEFEATS |
| 62 | 0x1D5C | 2 JACKPOT AWARDS | | 88 | 0x1DC4 | SHOOTOUT BONUS |
| 63 | 0x1D60 | 3 JACKPOT AWARDS | | 89 | 0x1DC8 | VIDEO MODE |
| 64 | 0x1D64 | 4 OR MORE JACKPOTS | | 90 | 0x1DCC | VICTORY RAMPS AWARDED |
| 65 | 0x1D68 | RAMP DOUBLE JACKPOT | | 91 | 0x1DD0 | MUSIC 1 |
| 66 | 0x1D6C | TIMER DOUBLE JACKPOT | | 92 | 0x1DD4 | MUSIC 2 |
| 67 | 0x1D70 | QUAD JACKPOT | | 93 | 0x1DD8 | MUSIC 3 |
| 68 | 0x1D74 | STUNT 1 | | 94 | 0x1DDC | WON FIGHT |
| 69 | 0x1D78 | STUNT 2 | | 95 | 0x1DE0 | PROPRIETARY |

The Freeway code writes its ramp record to 0x1DA7, the lowest byte of MAX # OF RAMPS. Indices 0-43 are bookkeeping (coins, replays, score bands, averages) and 97-110 operator actions; their names are the ROM's, but no address is established for them.

### Leo Getz awards

Every award was fired in the rig and the display captured (17 September 2026). "Prints" is the handler's own screen; a dash means the award never reached the super-wheel choice screen.

| # | Handler | Prints | Choice-screen words | Note |
| --- | --- | --- | --- | --- |
| 0 | 0x968E | EXTRA BALL LIT! / LETHAL WEAPON 1 | (blank) | cues 0x4F, 0xA6 |
| 1 | 0x96D7 | SPECIAL! | SPECIAL | credit + 1 |
| 2 | 0x96FF | LETHAL WEAPON 3 / HIGH FALL / 5 MILLION | - | starts the next stunt |
| 3 | 0x8B7F | SUPER SPINNER | (blank) | lamp 27 Subway on |
| 4 | 0x7E2C | nothing | - | code: lamp 57 Karate Kick on, lamp 25 off, 0x100B = 8 |
| 5 | 0x742E | TRI-BALL READY | TRI-BALL READY | cue 0x04 |
| 6 | 0x9790 | LOOPING READY! | LITE LOOPING | cue 0x5A |
| 7 | 0x97AF | VIDEO MODE READY | (blank) | |
| 8 | 0x97C6 | 8X | (blank) | cue 0xDC, audit # OF 8X MADE |
| 9 | 0x8DE5 | CRAZY RIGGS 2,500,000 | CRAZY RIGGS | +250,000 steps, 15 s clock |
| 10 | 0x7BFC | nothing | (blank) | inferred Super Pops: fills the timer block award 20 uses |
| 11 | 0x9837 | nothing; score + 5,000,000 | (blank) | |
| 12 | 0x989D | nothing | (blank) | lamp 18 Murtaugh's Retirement on |
| 13 | 0x8B6A | BONUS | (blank) | lamp 32 on: hold bonus |
| 14 | 0x8B65 | nothing | (blank) | lamp 9 Start Getaway on |
| 15 | 0x98C0 | armored-truck scene, + 5,000,000 | BANK HEIST | cue 0x6F |
| 16 | 0x962E | SUPER LETHAL WEAPON 10,000,000 | SUPER LETHAL WEAPON | cues 0x3C, 0x73; 30 s clock |
| 17 | 0x95E9 | HIT BOTH FLIPPERS TO FIGHT | FIGHT 20M | fight mode |
| 18 | 0x9847 | 10 MILLION | 10 MILLION | cue 0x74 |
| 19 | 0x95D9 | EXTRA BALL! | - | cue 0x71 |
| 20 | 0xFD20 | nothing | SUPER DUPER POPS | patch code; 0x101B = 0x81, 0x101D = 0x17 |

### Display and attract

The display board runs its own 68B09E and plays the attract loop itself; the main CPU marks it only through sound commands. One capture of the loop on `lw3_301` gave 190 s, from four logo-to-logo intervals of 187-195 s, and 43 numbered screens before it repeats. Most of that capture ran fast, with real time reconstructed from the ROM clock, and only its last 53.5 s ran at 1x. The screens are: the DATA EAST logo build, the title, STARRING and three cast cards, Silver Pictures and Warner Bros. cards, CREDITS / PUSH START / BEST VALUE groups, the 3.01 patch's own VISIT PINBALLCODE.COM card, drug and drink-driving cards, a chunk of the design-credit roll (a different chunk each loop), a Tales from the Crypt "Coming Soon" promotion, REPLAY AT with the first replay level, two high-score blocks in which each entry slides in beside a police badge carrying its initials (1.78 s hold, 0.15 s black, 0.33 s slide), BSMT2000 and DIGITAL STEREO cards, DATA EAST PIONEER IN DOT MATRIX TECHNOLOGY, HELP MURTAUGH MAKE BURGERS, and ten instruction cards. Timing came from the ROM's own RAM clock (0x014E centiseconds, 0x014F seconds); the measured spec is retained with the sources. A survey of eleven Data East titles' attract loops found the badge layout unique to this game among them.

In one 262 s real-time capture from power-up, the sound stream carried 0x0020 at 1.8, 32.3, 43.8, 90.7, 127.9 and 235.5 s, each preceded by 0x0000, and paired once each with 0x000F (power-up track, 1.8 s), 0x0011 (43.8 s), 0x0064 (90.7 s) and 0x005F (128.0 s). 0x0064 is the 10.9 s promotion audio and 0x005F its 3.2 s closing sting. Which attract card each cue lines up with is the contributor's alignment and is not re-derived here.

0x0183 holds a byte the CPU stages for the display board. A lift correlation against the sound stream over 90 recordings first gave its values meanings; watching play then showed it cycling 144, 92, 68, 64, 16, 80, 8, 24, 56 several times a second, so those meanings were retracted. Values with bit 7 set are the ones the display board's dispatch at 0x8D25 accepts as messages. What the byte means remains open.

## Controller interactions - sound commands

The sound board takes single-byte commands. Protocol facts, code-level on `lw3_301`:

- The sound latch is **0x3402**, written at 0x46AD from 0x0184 and strobed through 0x3403. A byte equal to the last one sent (0x0185) or equal to 0xFF is suppressed. 0x2C00 is the display board's latch; twenty early injection attempts went to it by mistake.
- A routine plays a sound by posting a four-byte display record `[count, id -> 0x0183, parameter -> 0x0184, duration -> 0x0186]` through 0x4BEA, so the command is the parameter of a display record. A record can carry a tail of up to two further `[sound, duration]` pairs, walked at 0x4C5E (count 1-3 over the 113 records reached by an explicit load). The music and mode band, 35 commands, goes through a direct single-byte send via 0x0182 and 0x4BD1 and never appears in a record. Pools are tables of record addresses, picked at random by five pickers (0x53C6, 0x7FC2, 0x9A1F, 0x9A31, and 0x91CF, which indexes by the stunt step).
- The script table at 0xD316 has a real script for 110 of the 256 indices; an entry pointing at 0xD554 is empty, so that number drives lamps only. 0xD516 refuses a send whose number is below the running priority in 0x0596.
- 133 commands have an immediate send site in the code. The final record map ties 179 commands to the routine that posts them and leaves one, 0x001B, unexplained. 0x0024 (a three-byte configuration message carrying 0x1E01), 0x0026 (a single control byte) and 0x002E (the sound-board reset handshake) are written to the queue directly and are control, not samples. 0x0028 has a sound script but no sample in the community altsound package, and 0x002A is carried in the ROM with no path to it.
- Writing 0x00 to 0x0185 and then a command to 0x0184 makes the ROM send that command (rig, 15 of 15 previously unheard commands). This is playback and says nothing about what triggers the command in play.
- The 3.01 patch changes when some commands are sent - gun clicks replace the skill-shot chimes, "Now!" at fight start, no explosion on a fight win, the machine gun on every trigger, a shorter ramp-entrance sound, "Step on it" at Getaway start, a sound for 10 and 20 million awards, "They got away" only after a failed video mode - while the sound ROMs are unchanged. Captures before 5 September 2026 are `lw3_208`; later ones are `lw3_301`.

Commonly cited cues; the evidence grade of each is its row in the table below, where several are `RE-DERIVED (unverified)` and the operator test tones were never heard in play: power-up 0x000F; game start 0x0018 then the track's select cue; no credit 0x00A5 three times; music select cues 0x000C, 0x0009, 0x0006 and play cues 0x000F, 0x0001, 0x0002 for tracks 1-3; sinkhole collects 0x00AE, 0x00AF, 0x00B0; Leo saucer award 0x00A7; stunt start 0x0068 with 0x00EF and 0x00D5, then the rung's animation and callout (High Fall 0x00D4 / 0x0014, Car Crash 0x00D1 / 0x0015, Toilet Bomb 0x00D2 / 0x0016, Explosion 0x00D3 / 0x0017, Helicopter 0x00D0 / 0x0003, Super Stunt Spectacular 0x0066 / 0x00E6); drop bank complete 0x004D; Tri-Ball ready 0x0004; multiball 0x0005 with 0x005C and the auto-plunger 0x0087; ramp jackpot 0x0008 with 0x0070; ramp entrance 0x0083; gun armed 0x00BB and gun ready 0x00D5; ball saved 0x0051; extra ball lit 0x004F then 0x00A6; extra ball awarded 0x0071; bonus multiplier advance 0x00DC; tilt warning 0x0061; game over 0x0011; operator sound test 0x00F0-0x00F2. 0x00F4-0x00FE repeat the mode-music band (0x001A, 0x001C, 0x001E, 0x003E, 0x0030, 0x0032, 0x0034, 0x0036, 0x0038, 0x003A, 0x003C) with the same audio.

### Command reference (244 commands)

Labels are the Total Recall project's names, not the ROM's or the altsound package author's: `mus_`, `sfx_`, `voc_` and `ctl_` give the class, `sys_` is the operator test bank, `unk_` marks audio never heard in play whose trigger is unknown, and `_dup` marks a command whose audio duplicates another. The evidence status and confidence are the contributor's own grades for that row.

| Opcode | Label (Total Recall project) | Class | Evidence status | Confidence |
| --- | --- | --- | --- | --- |
| 0x0000 | ctl_cmd_prefix_a | control | RE-DERIVED (unverified) | medium |
| 0x0001 | mus_track2_play | music | RE-DERIVED (unverified) | medium |
| 0x0002 | mus_track3_play | music | RE-DERIVED (unverified) | medium |
| 0x0003 | voc_stunt5_helicopter | voice | BOUND | high |
| 0x0004 | mus_triball_ready | music | VERIFIED | high |
| 0x0005 | mus_multiball | music | BOUND | high |
| 0x0006 | mus_track3_select | music | VERIFIED | high |
| 0x0007 | mus_track3_select_dup | music | DUPLICATE of a firing sample | high |
| 0x0008 | mus_jackpot | music | BOUND | high |
| 0x0009 | mus_track2_select | music | VERIFIED | high |
| 0x000A | mus_ball_start_alt | music | VERIFIED | high |
| 0x000B | ctl_rom_only_0b | control | ROM HAS A SOUND SCRIPT - no sample in the package | low |
| 0x000C | mus_track1_select | music | VERIFIED | high |
| 0x000D | dup_mus_default | music | DUPLICATE audio - but it HAS its own send site | medium |
| 0x000E | mus_ball_end | music | RE-DERIVED (unverified) | medium |
| 0x000F | mus_default | music | RE-DERIVED (unverified) | medium |
| 0x0010 | unk_quadrupl | music | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0011 | mus_gameover | music | BOUND | high |
| 0x0012 | unk_zz_top_music | voice | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0013 | mus_cc_factory_fadeout | music | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0014 | voc_stunt1_highfall | voice | BOUND | high |
| 0x0015 | voc_stunt2_carcrash | voice | BOUND | high |
| 0x0016 | voc_stunt3_toiletbomb | voice | BOUND | high |
| 0x0017 | voc_stunt4_explosion | voice | BOUND | high |
| 0x0018 | mus_stop | sfx | BOUND | high |
| 0x0019 | ctl_bonus_tally | control | BOUND - audit-witnessed | high |
| 0x001A | mus_videomode | music | VERIFIED | high |
| 0x001B | sfx_videomode_end | control | SILENT MARKER (band rule) | high |
| 0x001C | mus_crazy_riggs | music | VERIFIED | high |
| 0x001D | sfx_crazy_riggs_end | control | SILENT MARKER (band rule) | high |
| 0x001E | mus_fight | music | VERIFIED | high |
| 0x001F | voc_fight_win | control | SILENT MARKER (band rule) | high |
| 0x0020 | ctl_cmd_prefix_b | control | RE-DERIVED (unverified) | medium |
| 0x0021 | ctl_rom_only_21 | control | SILENT (odd band marker, no sample by design) | high |
| 0x0022 | ctl_rom_only_22 | control | LIGHT SHOW ONLY - no sound by design | high |
| 0x0023 | ctl_rom_only_23 | control | SILENT (odd band marker, no sample by design) | high |
| 0x0024 | ctl_rom_only_24 | control | SOUND BOARD CONTROL - 3-byte config command | high |
| 0x0025 | ctl_rom_only_25 | control | SILENT (odd band marker, no sample by design) | high |
| 0x0026 | ctl_rom_only_26 | control | SOUND BOARD CONTROL - single-byte command | high |
| 0x0028 | ctl_rom_only_28 | control | ROM HAS A SOUND SCRIPT - no sample in the package | low |
| 0x002A | ctl_rom_only_2a | control | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x002E | ctl_rom_only_2e | control | SOUND BOARD CONTROL - reset handshake | high |
| 0x002F | ctl_rom_only_2f | control | SILENT (odd band marker, no sample by design) | high |
| 0x0030 | unk_hurry_up_2 | music | DUPLICATE (unheard) | medium |
| 0x0031 | ctl_rom_only_31 | control | SILENT (odd band marker, no sample by design) | high |
| 0x0032 | mus_multiball_saucer | music | RE-DERIVED (unverified) | medium |
| 0x0033 | ctl_jackpot_modifier | control | VERIFIED | high |
| 0x0034 | mus_ramp_loop | music | VERIFIED | high |
| 0x0035 | sfx_ramp_loop_end | control | SILENT MARKER (band rule) | high |
| 0x0036 | mus_multiball_end | music | VERIFIED | high |
| 0x0037 | sfx_triball_transition | control | SILENT MARKER (band rule) | high |
| 0x0038 | mus_getaway | music | RE-DERIVED (unverified) | medium |
| 0x0039 | sfx_getaway_end | control | SILENT MARKER (band rule) | high |
| 0x003A | mus_award_lightshow | music | VERIFIED | high |
| 0x003B | sfx_ramp_award | control | SILENT MARKER (band rule) | high |
| 0x003C | mus_shootout_end | music | VERIFIED | high |
| 0x003D | sfx_extraball_collected_03 | control | SILENT MARKER (band rule) | high |
| 0x003E | mus_super_spinners | music | BOUND | high |
| 0x003F | sfx_super_spinners_end | control | SILENT MARKER (band rule) | high |
| 0x0040 | sfx_sling_01 | sfx | RE-DERIVED (unverified) | medium |
| 0x0041 | sfx_spinner | sfx | BOUND (corrected) | high |
| 0x0042 | sfx_bumper_04 | sfx | POOL (membership certain, member state not separable) | high |
| 0x0043 | sfx_trigger_shot | sfx | RE-DERIVED (unverified) | medium |
| 0x0044 | unk_machine_gun_a | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0045 | sfx_stunt_trigger_hit | sfx | RE-DERIVED (unverified) | medium |
| 0x0046 | unk_machine_gun | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0047 | sfx_stunt1_gunfire | sfx | OBSERVED IN PLAY - stunt 1 sequence | medium |
| 0x0048 | sfx_videomode_intro | sfx | VERIFIED | high |
| 0x0049 | sfx_saucer_bell | sfx | OBSERVED IN PLAY - after a saucer kickout, with a countdown running | medium |
| 0x004A | sfx_laser_kick_step | sfx | BOUND - not a duplicate after all | high |
| 0x004B | sfx_ramp_jackpot_step | sfx | BOUND | high |
| 0x004C | unk_bells | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x004D | sfx_drop_clear | sfx | BOUND | high |
| 0x004E | sfx_lane | sfx | BOUND | high |
| 0x004F | sfx_extraball_lit | sfx | VERIFIED | high |
| 0x0050 | unk_bell_3 | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0051 | voc_freeze | voice | BOUND - freeze / ball save, audit-proved | high |
| 0x0052 | sfx_sequence_end | sfx | VERIFIED | high |
| 0x0053 | sfx_kickback_dup | sfx | DUPLICATE of a firing sample | high |
| 0x0054 | sfx_kickback | sfx | VERIFIED | high |
| 0x0055 | sfx_bank_hit_1 | sfx | RE-DERIVED (unverified) | medium |
| 0x0056 | unk_echo_bells | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0057 | unk_bells_up_2 | sfx | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0058 | sfx_bank_hit_2 | sfx | BOUND | high |
| 0x0059 | sfx_gun_fire | sfx | VERIFIED | high |
| 0x005A | sfx_saucer_right_kickout_follow | sfx | VERIFIED | high |
| 0x005B | sfx_skillshot_made | sfx | VERIFIED | high |
| 0x005C | sfx_multiball_start | sfx | BOUND | high |
| 0x005D | sfx_ball_ready | sfx | BOUND | high |
| 0x005E | sfx_skillshot_miss | sfx | VERIFIED | high |
| 0x005F | mus_attract_promo_end | music | BOUND | high |
| 0x0060 | sfx_tilt | sfx | BOUND | high |
| 0x0061 | sfx_tilt_warning | sfx | BOUND | high |
| 0x0062 | sfx_gameover_credits | control | SILENT MARKER | high |
| 0x0064 | mus_attract_promo | music | BOUND | high |
| 0x0065 | sfx_shootout_end_miss | sfx | VERIFIED | high |
| 0x0066 | sfx_stunt6_superstunt | sfx | BOUND | high |
| 0x0067 | voc_pre_match | voice | PROVISIONAL (context only) | low |
| 0x0068 | sfx_stunt_start | sfx | VERIFIED | high |
| 0x006C | seq_shootout_arm | sequence | BOUND - a COMPOSITE: the whole shoot-out arming sequence | high |
| 0x006D | voc_shot | voice | BOUND | high |
| 0x006E | sfx_engine_down | sfx | BOUND - audit-witnessed | high |
| 0x006F | sfx_super_leo_select | sfx | VERIFIED | high |
| 0x0070 | voc_jackpot_01 | voice | VERIFIED | high |
| 0x0071 | voc_extraball_award | sfx | VERIFIED | high |
| 0x0072 | sfx_award_lightshow | sfx | VERIFIED | high |
| 0x0073 | voc_super_lw_10m | voice | VERIFIED | high |
| 0x0074 | voc_award_explosion | voice | BOUND - shared award cue | high |
| 0x0075 | sfx_million_plus | sfx | BOUND | high |
| 0x0076 | voc_ramp_award_03 | sfx | VERIFIED | high |
| 0x0077 | sfx_award_7m_ramp | sfx | VERIFIED (shared with the shoot-out result) | high |
| 0x0078 | voc_double_jackpot | voice | BOUND - the double jackpot callout | high |
| 0x0079 | voc_quad_jackpot | voice | BOUND - the quad jackpot callout | high |
| 0x007A | ctl_rom_only_7a | control | ROM HAS A SOUND SCRIPT - no sample in the package | low |
| 0x007B | sfx_bumper_01 | sfx | POOL member PLACED - shootout bonus | high |
| 0x007C | sfx_score_tick | sfx | RE-DERIVED (unverified) | medium |
| 0x007D | sfx_super_pops | sfx | RE-DERIVED (unverified) | medium |
| 0x007E | sfx_drop_tally | sfx | VERIFIED | high |
| 0x007F | ctl_rom_only_7f | control | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x0080 | unk_loud_machine_gun | sfx | DUPLICATE (unheard) | medium |
| 0x0082 | sfx_gun_reload | sfx | VERIFIED (shared, reload cue) | high |
| 0x0083 | sfx_ramp_enter | sfx | BOUND | high |
| 0x0084 | unk_burning_car | sfx | LIGHT SHOW ONLY - no sound by design | high |
| 0x0085 | sfx_player_added | sfx | BOUND | high |
| 0x0086 | sfx_helicopter_clean | sfx | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x0087 | sfx_autolaunch | sfx | BOUND | high |
| 0x0088 | unk_machine_noise | sfx | DUPLICATE (unheard) | medium |
| 0x0089 | sfx_ramp_timeout | sfx | VERIFIED | high |
| 0x008A | sfx_orbit_whoosh_1 | sfx | POOL (membership certain, member state not separable) | high |
| 0x008B | sfx_orbit_whoosh_3 | sfx | POOL (membership certain, member state not separable) | high |
| 0x008C | sfx_orbit_whoosh_2 | sfx | POOL (membership certain, member state not separable) | high |
| 0x008D | sfx_orbit_whoosh_4 | sfx | POOL (membership certain, member state not separable) | high |
| 0x008E | sfx_orbit_whoosh_5 | sfx | BOUND | high |
| 0x008F | sfx_bumper_02 | sfx | POOL (membership certain, member state not separable) | high |
| 0x0090 | unk_loaded | voice | DUPLICATE (unheard) | medium |
| 0x0091 | sfx_canon_fire_clean | voice | CLEAN TAKE - dry version of 0x00AB | medium |
| 0x0092 | unk_they_go_away | voice | LIGHT SHOW ONLY - no sound by design | high |
| 0x0093 | voc_playfield_05 | voice | POOL member PLACED - won fight | high |
| 0x0094 | voc_outlane_right_02 | voice | BOUND | high |
| 0x0095 | voc_playfield_04 | voice | POOL (membership certain, member state not separable) | high |
| 0x0096 | voc_freeze_single | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x0097 | voc_multiball_feed | voice | VERIFIED | high |
| 0x0098 | voc_playfield_03 | voice | POOL (membership certain, member state not separable) | high |
| 0x0099 | dup_voc_playfield_02 | voice | DUPLICATE (package copy) - the ROM sends 0x00AC | high |
| 0x009B | voc_freeze_single_02 | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x009C | ctl_rom_only_9c | control | ROM HAS A SOUND SCRIPT - no sample in the package | low |
| 0x009D | voc_jackpot_clean | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x009E | sfx_canon_clean | sfx | CLEAN TAKE - dry version of 0x00AB | medium |
| 0x009F | sfx_canon_alt | sfx | BOUND - the cannon's 50/50 alternate | high |
| 0x00A0 | voc_extraball | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x00A1 | unk_loaded_2 | voice | DUPLICATE (unheard) | medium |
| 0x00A2 | voc_outlane_right | voice | RE-DERIVED (unverified) | medium |
| 0x00A3 | voc_playfield_01 | voice | POOL (membership certain, member state not separable) | high |
| 0x00A4 | voc_back_in_action | voice | BOUND | high |
| 0x00A5 | voc_no_credit | voice | BOUND (shared: rebuff + playfield pool) | high |
| 0x00A6 | voc_extraball_lit | voice | BOUND | high |
| 0x00A7 | voc_leo_saucer_award | voice | BOUND - audit-witnessed | high |
| 0x00A8 | voc_leo_getz | voice | RE-DERIVED (unverified) | medium |
| 0x00A9 | voc_bumper_03 | voice | POOL (membership certain, member state not separable) | high |
| 0x00AA | ctl_rom_only_aa | control | ROM HAS A SOUND SCRIPT - no sample in the package | low |
| 0x00AB | sfx_canon_fire | sfx | BOUND - the cannon, posted by 0x87E3 | high |
| 0x00AC | voc_playfield_02 | voice | POOL (membership certain, member state not separable) | high |
| 0x00AD | voc_playfield_06 | voice | POOL (membership certain, member state not separable) | high |
| 0x00AE | sfx_lw_collect_1 | sfx | BOUND | high |
| 0x00AF | sfx_lw_collect_2 | sfx | BOUND | high |
| 0x00B0 | sfx_lw_collect_3 | sfx | BOUND | high |
| 0x00B1 | voc_drop_mid_hit | voice | RE-DERIVED (unverified) | medium |
| 0x00B2 | voc_match_no | voice | BOUND | high |
| 0x00B3 | voc_drop_bank_complete | voice | VERIFIED | high |
| 0x00B4 | voc_im_driving | voice | OBSERVED IN PLAY - playfield callout pool | medium |
| 0x00B5 | sfx_fight_clean | voice | CLEAN TAKE - the dry fight sample, mixed inside 0x00EB | medium |
| 0x00B6 | voc_attract_callout | voice | BOUND | high |
| 0x00B7 | voc_double_jackpot_clean | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x00B8 | sfx_saucer_left | sfx | BOUND | high |
| 0x00B9 | sfx_saucer_vuk | sfx | RE-DERIVED (unverified) | medium |
| 0x00BA | sfx_saucer_right | sfx | RE-DERIVED (unverified) | medium |
| 0x00BB | sfx_bells_short | sfx | BOUND - precedes the NOW cue in every one of its fires | high |
| 0x00BC | voc_im_driving_2 | sfx | OBSERVED IN PLAY - isolated, with 0x10CD stepping | medium |
| 0x00BD | voc_shootout_result | voice | BOUND | high |
| 0x00BE | sfx_shared_launch_crazy_riggs_switch | sfx | RE-DERIVED (unverified) | medium |
| 0x00BF | sfx_crazy_riggs_switch | sfx | RE-DERIVED (unverified) | medium |
| 0x00C0 | sfx_ramp_shot | sfx | BOUND | high |
| 0x00C1 | sfx_ramp_award_03 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00C2 | voc_ramp_award_02 | sfx | VERIFIED | high |
| 0x00C3 | voc_fight_punch_01 | voice | POOL (membership certain, member state not separable) | high |
| 0x00C4 | sfx_fight_punch_02 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00C5 | voc_fight_punch_04 | voice | POOL (membership certain, member state not separable) | high |
| 0x00C6 | voc_fight_punch_03 | voice | POOL (membership certain, member state not separable) | high |
| 0x00C7 | sfx_impact_02 | voice | POOL (membership certain, member state not separable) | high |
| 0x00C8 | sfx_impact_03 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00C9 | sfx_impact_04 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00CA | sfx_impact_01 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00CB | voc_ramp_award_01 | voice | VERIFIED | high |
| 0x00CC | voc_ramp_complete | voice | VERIFIED | high |
| 0x00CD | sfx_ramp_award_02 | sfx | POOL (membership certain, member state not separable) | high |
| 0x00CE | sfx_videomode_target | sfx | VERIFIED | high |
| 0x00CF | sfx_crazy_riggs_finish | sfx | BOUND (never captured - video paused) | high |
| 0x00D0 | sfx_stunt5_helicopter | sfx | BOUND | high |
| 0x00D1 | sfx_stunt2_carcrash | sfx | BOUND | high |
| 0x00D2 | sfx_stunt3_toiletbomb | sfx | BOUND | high |
| 0x00D3 | sfx_stunt4_explosion | sfx | BOUND | high |
| 0x00D4 | sfx_stunt1_highfall | sfx | BOUND | high |
| 0x00D5 | voc_now | voice | RE-DERIVED (unverified) | medium |
| 0x00D6 | voc_millions_clean | voice | CLEAN TAKE - dry version of a callout the package carries mixed | medium |
| 0x00D7 | sfx_super_jackpot | sfx | VERIFIED | high |
| 0x00D8 | sfx_saucer_kickout | sfx | BOUND | high |
| 0x00D9 | sfx_videomode_hit | sfx | BOUND | high |
| 0x00DA | sfx_fight_won | sfx | BOUND - won fight, audit-proved | high |
| 0x00DB | sfx_multiball_lost | sfx | BOUND | high |
| 0x00DC | sfx_top_lane_completed | sfx | VERIFIED | high |
| 0x00DD | sfx_bonus_step | sfx | BOUND | high |
| 0x00DE | sfx_orbit_right | sfx | RE-DERIVED (unverified) | medium |
| 0x00DF | sfx_orbit_left | sfx | RE-DERIVED (unverified) | medium |
| 0x00E0 | sfx_attract_beat | sfx | BOUND | high |
| 0x00E1 | sfx_menu_exit | sfx | VERIFIED | high |
| 0x00E2 | sfx_bomb_tail | sfx | BOUND - not a duplicate after all | high |
| 0x00E3 | sfx_video_cow | sfx | BOUND - the rare target appearing in the crime simulator | high |
| 0x00E4 | unk_million | sfx | BOUND - part of the quad jackpot award | high |
| 0x00E5 | sfx_bomb | sfx | BOUND - display script 0xF6 posts it | high |
| 0x00E6 | voc_stunt6_superstunt | voice | BOUND | high |
| 0x00E7 | voc_saucer_right_02 | voice | VERIFIED | high |
| 0x00E8 | voc_left_bank_reset_dup | voice | DUPLICATE of a firing sample | high |
| 0x00E9 | voc_left_bank_reset | voice | VERIFIED | high |
| 0x00EA | voc_murtaugh_retirement | voice | VERIFIED | high |
| 0x00EB | seq_fight_start | sequence | VERIFIED | high |
| 0x00EC | voc_shootout_end | voice | BOUND | high |
| 0x00ED | sfx_click | sfx | BOUND (shared: credit button + gun trigger) | high |
| 0x00EE | unk_owh_owh_owh | voice | ORPHANED - the ROM carries the sound with no path to it | low |
| 0x00EF | sfx_saucer_stage_arm | sfx | RE-DERIVED (unverified) | medium |
| 0x00F0 | sys_test_tone_left | system | SYSTEM (operator sound test) | high |
| 0x00F1 | sys_test_tone_right | system | SYSTEM (operator sound test) | high |
| 0x00F2 | sys_test_tone | system | SYSTEM (operator sound test) | high |
| 0x00F4 | mus_videomode_dup | music | DUPLICATE of a firing sample | high |
| 0x00F5 | mus_crazy_riggs_dup | music | DUPLICATE of a firing sample | high |
| 0x00F6 | mus_laser_kick | music | BOUND - not a duplicate after all | high |
| 0x00F7 | mus_super_spinners_dup | music | DUPLICATE of a firing sample | high |
| 0x00F8 | unk_hurry_up_sirens_3 | music | DUPLICATE (unheard) | medium |
| 0x00F9 | mus_multiball_saucer_dup | music | DUPLICATE of a firing sample | high |
| 0x00FA | mus_ramp_loop_dup | music | DUPLICATE of a firing sample | high |
| 0x00FB | mus_multiball_end_dup | music | DUPLICATE of a firing sample | high |
| 0x00FC | mus_getaway_dup | music | DUPLICATE of a firing sample | high |
| 0x00FD | mus_award_lightshow_dup | music | DUPLICATE of a firing sample | high |
| 0x00FE | mus_shootout_end_dup | music | DUPLICATE of a firing sample | high |
| 0x00FF | ctl_shared_marker | control | RE-DERIVED (unverified) | medium |

## ROM-level sources

- `rom.lw3-301`: `lw3_301.zip` from the contributor's VPinMAME ROM folder, SHA-256 `094935aa2f525c3bd46faab5c9de87a94c1bb13cde4238e5d62222d819ed8f13`, members `LW3CPUU.301` (CRC32 `e6a44d10`), `lw3drom0.300` (`af9c066b`), `lw3drom1.300` (`38f0ab03`), `Changelog-LW301.txt` and `ReadMe-LW301.txt`. It runs as the pinned PinMAME driver `lw3_301`, and its changelog is a primary source for the 3.01 rule changes. No ROM bytes, NVRAM images or disassembly byte columns are in this repository.
- `rom.lw3-208`: `lw3_208.zip` from the same folder, SHA-256 `3997903848a2cb0e5dc8cae3356e588f2797bbe0594155faae6baaafd33499ab`, used for the 2.08 music-selection run and the sound captures before 5 September 2026.
- `memory-map.tomlogic.lw3-208`: `maps/dataeast/version3/lw3_208.map.json` in tomlogic's Pinball Memory Maps repository, file version 9, "Copyright (C) 2026 by Tom Collins"; the file's own metadata gives the Open Data Commons Open Database License v1.0. The fields used here are its game state, credits, free play, maximum credits, ball count and high-score table. Local copy retained as `docs/lw3_208.map.json`, SHA-256 `e500263849de0ebf401213b2a728fea8ab982b0962e152469a88bf1bff3e20a1`.
- `rom-state.lw3-301.totalrecall-2026-10-03`: the Total Recall project's Lethal Weapon 3 ROM work, 5 September to 3 October 2026, copied unchanged into the working root at `review-artifacts/lethal-weapon-3-rom-state-2026-10-03/`: 192 files, 694 MB, listed in `MANIFEST.sha256` (SHA-256 `2c70ccd9801a1e0296d503b45cc3c1024b13735fbc335020476614b056599a56`). The rig drove VPinMAME through its COM controller; its version was not recorded in the retained metadata. The 6800 disassembler and rig scripts belong to that project and are not retained here, only their outputs. Documents relied on, under `docs/`:

  | File | SHA-256 | Holds |
  | --- | --- | --- |
  | `LW3_BLIND_SPOTS_ROM.md` | `13790c185e3e22ee0517e8869957f02eee195d2ef64bc3b1eeded036bfeaeac3` | 3 October code and rig findings: ball save, extra ball, Leo predicates, Freeway, replay, special, match, adjustment bytes, the tournament run |
  | `PAYLOAD_lw1_at_sw32.md` | `922ed1f33d299ca328c32ad4b82c91a038123b35680022d74651c136014c8a00` | the LW latch arming sites 0x8F82 and 0x8FB7 |
  | `lw3_blind_spots.md` | `1d7912e136781ab1fc4d148cf1cd05b508cca908494704063013664a7cc58854` | the 3 October blind-spot list and its corrections |
  | `project_knowledge.md` | `f9d84209418af56b0e2349d6196d82ec70d6606a84d3b8e426f71a833fcd2050` | sections 4d-4x: the rig method, the stunt counter, the 5 September state map, the disassembly, multiball, the LW latches, audits, the sound latch |
  | `lw3_301.map.json` | `8bf3137784fa6902196dcf9cdff5a29ed8a1dedd42b4a89dc2d118ed2b6c6629` | the 5 September mode-state map in tomlogic's file format |
  | `lw3_208.map.json` | `e500263849de0ebf401213b2a728fea8ab982b0962e152469a88bf1bff3e20a1` | local copy of tomlogic's map |
  | `AUDIT_NAMES.md` | `c2934ffb9eed415133c87e365273c34f317d20a912a8fe975e6c5e103d90a2ac` | the 111 audit names and derived addresses |
  | `AUDIT_MAPPING.md` | `351ae68ea317ce3d74ab6f06f796f46be9b1b3adb7f92a48c9addf0ba1cbc434` | the audit-address verification |
  | `LEO_AWARDS.md` | `7f0f185e80b76559bda47f39b7980eb1f98dbac2cbbab8eb41a44dbd2c18b079` | the 21 Leo awards fired in the rig |
  | `MUSIC_SELECT.md` | `0f3f61c48b83fb50c0ce4d1f13e6096f403509783e9bbad24dd5e9c9682eee27` | the music-selection code |
  | `SOUND_LATCH.md` | `889fced6d3e12a7512d5ae7e493350f7d239290c1de92d1f94a42ae7e50e5867` | the sound latch and record format |
  | `ROM_CRACK.md` | `cecc3bedcabc489ae840b04d34deb6fec16afd5c9cea1e0ba94dc24a3bb6f1d9` | the disassembly summary |
  | `EVENT_REGISTER.md` | `1facde9a4ba0cbe7007d45ded21425f642d44d0b116763e382e2f6979591bdf4` | the retracted 0x0183 correlation |
  | `display_text.md` | `b446bd20f32c0ac47cb853c22e24b8c8a303f6c2d425128f4cf299b833a69a49` | every plain-text string in `lw3drom1.300` |
  | `TR_SOUND_MAP.csv` | `50e0a9adc5f1a3adb56a85b4dae70a78de2f9932594bced71c3c047913af88ab` | the 244-row sound-command map behind the reference table |
  | `lw3_dmd_attract_spec.md` | `b7273e584a0f62a045cbaa2081d861e1cb47638c9b65d2e63411fd41dbd087db` | the measured attract loop |
  | `de_attract_survey.md` | `c8a7bfee52a228a3c44fed8098dc65309008c73a6036a4d4203ea0b8fb647b97` | the eleven-title Data East attract survey |
  | `dmd_log.md` | `870e42a9f132497b2fb862f2854e34f57d008f3133fe2e1a0d6d0d02a7aa16a3` | the 3 October attract-cue alignment |
  | `rom_mapping_effort.md` | `f9fca6b8f2ccf5fab8708ace55830031836602096f8e632cf6bad96de819715b` | the campaign's effort and platform notes |

  Rig recordings, under `rec/` (each holds `meta.json` with the sound stream and `nvram.npy` with the sampled RAM image):

  | Recording | `meta.json` SHA-256 | Shows |
  | --- | --- | --- |
  | `ballsave3` | `ce4102547432dff8794a35aa08d57ba2da1c53087d7b0c68c199b6ae5b352659` | ball save runs A-C |
  | `tourney_off` | `548553fa4ff56ba75bf7d93d08837dd51962866e95d30dc05646a0ed3863a86b` | tournament off |
  | `tourney_on` | `5dfaf978561d66eafbf39e9e5371c1905548119109ddfe703bfe321e9246b3b4` | tournament on |
  | `leo_dmd_award00` | `3d8ef155f87abfe03892fd04f85bfac3ba7c45b6bff49ee52ef7f71c8740845c` | Leo award 0 and the 0x1D24 / 0x0024 timing |
  | `av_attract_03oct_v3` | `aca9953f7cadd10e02f5fa0775dfa6c26f9b792fe3b60effeea6a89e88e2e2a3` | 262 s real-time attract with the sound stream |
  | `attract_1x` | `959686872a88ae83ef78f9ecc374a60d7cc812819001f0abf847b967cd74c388` | the attract-spec capture |
  | `musicsel_screen_lw3_208` | `cf828a3d6becd9e87bced302d64f5ec58a96e05e0b1e78fb6f0d0070c4e58111` | 2.08 music selection |
  | `musicsel_screen_lw3_301` | `ad3bd132bd146ef6c5479ecced0c5d24fd70e9bd3fefb46f81b419be152f0c67` | 3.01 music selection |
  | `stuntladder` | `f6d4492c7bb8c6376de643db09fe8ea0af52a639c849c1b2c86a0a928a9b591f` | the stunt ladder |
  | `l42` | `993f0683d6e0971c96f35d7d092edcabf23a5e8e31706ecc744cbc20e2a3c86e` | 0x140F during stunts |
  | `bonushunt` | `9b9943bfd3ee23a7da18eeae3329670342d67f5bccfa5bbb41955fd9e7a22bc5` | bonus byte |
  | `bonusmult` | `536003f61c185fc4bcd5bff80fa5673c0802f73d2c93344e8d27c57bc1bfc2c7` | bonus with the multiplier poked |
  | `jackpots2` | `e3abb5a4c197eb915a8fc8638c29e01d80ca3458483509ffd2a549b7985339eb` | jackpot scoring, flagged compromised for the re-lite question |
  | `av_play_03oct` | `f694106af304f4f0c4608b184667cf366625cd218728531c1a36086e70e6690a` | a full scripted game; Freeway count |
