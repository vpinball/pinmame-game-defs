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

The retained known-working VPW 2.0 script does drive both addresses from the cabinet flipper key, at `script.vbs:928-929` on key down and `960-961` on key up. That agrees with what the emulator mirrors, so it is redundant in an ordinary build rather than authoritative - and it is what a P-ROC-mode consumer would need. An earlier revision of this note asserted flatly that a recreation "must not drive 15 or 16" while the working recreation does exactly that; the rule was both unqualified and contradicted by the evidence.

The superseded legacy record labels them "Left/Right Flipper Button", which describes what the emulator publishes rather than what the manual prints; both are recorded here.

## Lamps bind through `vpmMapLights`, not `Lampz`

The retained table uses the older idiom: each light's own `TimerInterval` field IS its ROM lamp index, and the lights sit in an `AllLamps` collection. A resolver written for the newer `Lampz.MassAssign` convention finds **zero** lamps here and reports a clean-looking result, which is how it was nearly missed. Four addresses - 7, 9, 18 and 27 - drive two bulbs at genuinely different playfield positions; lamp 18's pair sits at opposite sides of the table. Each is placed individually rather than averaged, because a centroid between two real inserts is a coordinate with no bulb in it.

## Evidence and its limits

The contributor-supplied manual has **no text layer whatsoever** - 93 pages, 0 characters - so every table here was read from 400 dpi renders and transcribed by hand. Four excerpts are committed beside this definition and digest-checked.

Spatial placement rests on one canonical VPW 2.0 extraction whose playfield is 952 x 2162. Fourteen playfield coils are placed at the retained Kicker, Bumper, Plunger, target-bank or slingshot mechanism they actuate, with the manual location drawing independently confirming the physical feature; these are mechanism locations, not invented winding centers. The knocker remains unplaced because the printed drawing has no readable 8L callout and the script's `KnockerPosition` is only a sound-placement helper. Driver 3 also remains unplaced and has unknown fitment: the drive table prints no coil while the same manual's location drawing clearly prints `3L` in the lower-right shooter-housing/cabinet extension without naming the device. The retained script also binds direct flashers 9 and 16, muxed flashers 25-32, and the solenoid-11 GI relay to exact Light objects; all in-bounds visual effects are retained individually, while the `GI_BG` object is excluded because its negative raw y coordinate makes it an off-playfield proxy.

Flasher Light objects are presentation effects rather than a physical socket survey. Their counts are lower than the manual bulb quantities at addresses 9, 16, 25-27, 29, 31 and 32; address 30 is the opposite mismatch, with four retained effects for three printed bulbs, and is preserved as `conflict.drive-6-flasher-effect-count`. Address 28 happens to match three-to-three, but count agreement alone still does not prove socket identity. Three additional local tables were inspected during maintainer review, but their credits establish a Javier to 32Assassin to VPW derivative chain, so they are not independent corroboration. Every coordinate therefore remains `observed` until an independent recreation or a complete original-machine location/socket survey agrees.

The drive-6 label is reconciled by the manual's own location drawing. Its drive table says `LEFT 3 BANK`, but printed page 28 places callout 6L beside the center drop-target bank, agreeing with the switch chart and the known-working script's `dtM` binding. The definition therefore calls the device Center Drop-Target Bank Reset while preserving `Left 3 Bank` as the manual wording; the relay-half name alone does not establish left-versus-center placement, as drive 7 appears in the same printed Left coil column but is named `RIGHT 3 BANK`.
