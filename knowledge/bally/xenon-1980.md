# Xenon (Bally 1980)

Coverage: **partial - controller and machine semantics curated; full physical GI inventory and spatial validation remain open.**

## Identity and public controller contract

Bally model 1196, November 1980, IPDB 2821, OPDB `G42Pk-MZe2e`. xenon, xenonf, xenona, xenonfa share init_xenon, GEN_BY35, dispBy7, lampCol = 8 and Sounds Plus/Vocalizer -56/-57 hardware. French speech and Oliver free-play firmware change no physical I/O; later firmware dates do not change the machine's 1980 release year. PinMAME source controls these emulator facts.

The five-column matrix is 1-40 with literal blank descriptions 12-15; 41-48 are unfitted. Diagnostics are -7/-6/-5. S1-S32 are four 8-position packages. Cabinet flipper buttons 84 left/82 right live outside the ROM-scanned matrix. Synthetic right 45/46 and left 47/48 are whole-flipper paired state gated by K1 relay 19; no independent EOS or winding timing is published. Consume public levels directly: the physical schematic draws normally-open contacts. The retained 2.5.2 sw29_UnHit erroneously clears 20 instead of 29; release 29 correctly in a recreation.

Momentary 1-15, continuous 17-20 and synthetic 45-48 all have a disposition. There is no public 16 because selector 15 is idle. Printed 18-entry self-test numbering is not public addressing; the fresh ROM test decoded every selector over repeated cycles. Public 17 is a fitted top-saucer coil, not a sixth-column strobe. Public 20's short power-up rise is reset initialization; its A3J2-15 load is N/U. Wiring-sheet misprints for the #1 trip/reset/outhole connectors are retained literally: A3's own schematic and plug chart agree on J1-2/3/5. K1 is an internal Q15/PB6 relay, not A3J2-6 NOTE 1.

## Mechanisms and ball paths

### Two-ball outhole / release stack

Two physical balls: outhole coil 7 transfers a drained ball into the two-position release stack; coil 8 ejects its leading ball to the manual shooter lane. Switch 2 is the leading position, 28 the second position; 8 is the separate outhole. Start with 2/28 active when both balls are home. Open 2 during an eject, open 28 as the trailing ball advances, then close 2 for the remaining ball. Never open/close 8 merely because coil 7 fired; the ball movement causes the switch changes. A jammed occupied position can cause retry pulses. VPX uses cvpmBallStack InitSw 8, 2, 28 and IsTrough=True; tuning and transfer delays are table-owned.

### Four individually tripped drop targets

One common reset coil 1 lifts all four targets and opens their held-down contacts 21-24. Trip coils 2/3/4/5 pull target #1/#2/#3/#4 down, closing 24/23/22/21. Top button #1/#2/#3/#4 at 20/19/18/17 requests the matching target only when its lamp is lit. A ball hit also drops a target. Hold each contact while its target stays down; bank completion awards the lit feature and resets. Startup/reset restores standing targets; never erase contacts before the physical reset. Individual trip or reset failure leaves the affected contact held and changes subsequent awards.

### Tube and Exit Chamber side saucer

Ball enters from the upper right over switch 27, traverses the raised clear tube to the left, trips end-of-tube-lane 1 and falls into the Exit Chamber saucer 33. Coil 9 ejects toward the right slingshot. The ROM can retain one ball there for multiball after three top-saucer X awards; represent 33 held while locked, and release it only after a real eject. The tube lamps are ten separate miniature bulbs in five pairs, never a motor or ten independent flashers. A switch stuck closed or an eject/ball-path jam changes lock/serve behavior; no fabricated fixed flight time is asserted.

### Top saucer

Top saucer 34 retains a ball until continuous driver 17 ejects it toward the right side of the middle bumper, as the factory vector drawing states. Each entry scores/advances according to S15/S16 and advances the three X awards. First complete X sequence qualifies the tube lock; second releases the captive ball for two-ball play. Third sequence during multiball qualifies outlane specials; further completion awards the configured special. Do not treat 17 as an unfitted sixth-column strobe: the game has five switch columns and a fitted saucer coil on 17.

### Right Slingshot

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Left Slingshot

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Lower Thumper Bumper

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Middle Thumper Bumper

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Right Thumper Bumper

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Left Thumper Bumper

A closed leaf contact requests its own ROM-driven impulse coil. The retained isolated-input gameplay run confirms this switch-to-output pairing. Ball rebound and animation timing remain table-owned; the coil does not keep the contact closed.

### Left flipper

Cabinet button mechanically powers the two-winding flipper through K1 relay 19. Physical EOS transfers power to hold; PinMAME exposes whole-flipper synthetic state and a duplicate, not an independently timed EOS/power/hold model. The button is outside the ROM-scanned matrix. Relay-off disables the winding. Return spring restores the bat on release; wear/EOS failure and coil heating are physical failure modes, not extra public outputs.

### Right flipper

Cabinet button mechanically powers the two-winding flipper through K1 relay 19. Physical EOS transfers power to hold; PinMAME exposes whole-flipper synthetic state and a duplicate, not an independently timed EOS/power/hold model. The button is outside the ROM-scanned matrix. Relay-off disables the winding. Return spring restores the bat on release; wear/EOS failure and coil heating are physical failure modes, not extra public outputs.

### Manual spring plunger

Passive manual plunger launches from the right shooter lane. Switch 25 senses the passing ball; it is not a launch-button command and has no launch coil.

## Rules and operator choices

Factory feature description PDF 7-8 (printed 4/4A): a tube traversal ends in the Exit Chamber side saucer, awards/advances its lit Exit Value, and ejects toward the right sling. S21 selects special repetition, S22 exit-value memory, S23 one/two advances, S24 the 50K/90K limit. Top-saucer S15/S16 choose 5K/no advance, 10K/one or 10K/two. Completing three center Xs qualifies capture; the next sequence releases two balls. Further sequences in multiball qualify outlane specials then an award. S30 controls X-light memory. A drain during multiball returns to tube qualification.

Lit top buttons request matching individual target trips. Completing four drops scores 10K and the current 2X/4X/25K/extra-ball/special award; S6/S7/S8 control initial 2X, tube advance and repeated special. XENON bonus begins 2K, advances to 58K and retains 20K/40K super-bonus milestones; tilt forfeits it. Spinner scores 10 normally and 1000 lit in multiball; each bumper scores 100. S14 chooses both/alternating lane arrows; S29 controls game-over voice. Self-test 16/17 select replay/extra-ball/novelty, 18 sound/background, 19 high-score-to-date awards. These adjustments are distinct from physical DIPs. Host-clock traces are not factory timing specifications.

## Lamps, bulbs and source disagreements

A5 publishes 60 decodable cells; only 1 is unwired. Complete connector excerpts preserve every pin, blank wire cell, key, N/U and SCR. A spare branch does not erase a fitted branch. Backbox-only indicators:13 BALL IN PLAY, 27 MATCH, 29 HIGH SCORE, 43 SHOOT AGAIN, 45 GAME OVER, 61 TILT. Credit 59 is under the apron. Main 11 is the playfield Shoot Again, separate from 43. Drop awards 15/31/47/63 each fit one backbox and one playfield socket. Target/top pairs 5/21/37/53 each fit two sockets; three table render objects do not mean three bulbs. Main 26 has tube-entrance/end bulbs; 52 has 40K/special inserts.

Tube strip AS-2518-60 has DS1-DS10 miniature lamps E-125-71 in five parallel pairs: public 14 group 1, 30 group 2, 62 group 3, 46 group 4, 10 group 5. They are lamps, not high-voltage flashers. Primitive1/84-92 are actual glass-bulb meshes; Diode1-10 are displaced glow planes. The board drawing and IPDB 43255 corroborate ten bulbs. Exact world-mesh centers are supplied, but DS orientation/full spatial reconciliation remain observed.

A9 AS-2518-52 has four seven-SCR groups, with 26 fitted circuits: sixteen frame pairs(32 bulbs), seven ring pairs(14 bulbs), SIDE SAUCER 69, END OF TUBE 85, BALL SHOOTER 101(two bulbs each per owner repair observations; the manual draws one branch per load without socket quantities). Frame/ring lights belong to the backbox insert, not playfield bonus circles. Q7/public 71 and Q26/public 117 are N/U. Decoder output 7(72/88/104/120) has no SCR; generic upper-half selectors have no independent physical load. Lamp-test activity proves neither fitment nor an omitted socket. Plug Table B's A9J2-25 is impossible; the A9 and playfield sheets agree on ball-shooter A9J3-10 wire 25. This is a wiring-detail note, not a physical conflict.

An attributable successful owner repair ties SIDE SAUCER J2-9 to a two-bulb pair around the left capture hole. The same owner describes two beneath the tube exit and two beneath the shooter cover; those quantities remain observed because that post does not trace their wires. Both retained tables drive only two distant bulb meshes from 69 and omit 85/101; the GI loop also writes l26a/l69a. Two runtime meshes do not reconcile all six physical bulbs across three circuits. The table mesh count is not itself a defect; the omitted callbacks and GI overwrite are disclosed implementation limitations. Photos and this prose do not trace the exact sockets, so spatial mapping remains open. The exact v600 geometry supplements its related 2.5.2 table and is not independent measurement.

GI is bare AC, with playfield, insert and cabinet branches recorded in the matrix-parts-gi excerpt and spatial report. No CPU path or PinMAME GI group exists, so no fictitious binding is added. The report retains actual modeled bulb candidates and excludes halos/glow planes/DOF helpers and controlled-load candidates. Candidate count does not establish the physical total or circuit split. Cabinet/backbox GI has not-applicable spatial disposition and unknown quantity; playfield candidates remain observed. This gap explicitly belongs to output_semantics/spatial_placement.

## Provenance and promotion

- `manual.xenon`: https://web.archive.org/web/20251203114903id_/https://www.ipdb.org/files/2821/Bally_1980_Xenon_Manual_And_Schematics.pdf; SHA256 `1eca010c9761e73339e04f7316d04c189d3d5ad8a7f051d9cad820c39810df9c`. IPDB 2821 Xenon model 1196/1980 verified on https://www.ipdb.org/machine.cgi?id=2821; original https://www.ipdb.org/files/2821/Bally_1980_Xenon_Manual_And_Schematics.pdf; retained manuals/by-machine/bally.xenon.1980/Bally_1980_Xenon_Manual_And_Schematics.pdf; all 54 pages Windows.Media.Ocr and native renders; decisive pages checked visually; exact excerpt locators below
- `pinmame.games.xenon`: https://github.com/vpinball/pinmame/blob/46e1a01a0f73dc5ce163d98db1ae435883ecc450/src/wpc/by35games.c; SHA256 `1c00fca170c7549a399a89fb0f76d4318fce08a6620becd4558fe8cb803bf00d`. dispBy7 lines 23-27, INITGAME 2 macro, Xenon lines 949-1009
- `pinmame.core.xenon`: https://github.com/vpinball/pinmame/blob/46e1a01a0f73dc5ce163d98db1ae435883ecc450/src/wpc/by35.c; SHA256 `91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2`. by35_lampStrobe, pia 0b_r, pia 1b_w, vblank, SWITCH_UPDATE
- `pinmame.core-common.xenon`: https://github.com/vpinball/pinmame/blob/46e1a01a0f73dc5ce163d98db1ae435883ecc450/src/wpc/core.c; SHA256 `38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00`. core_updateSw/core_getSol synthetic flipper column and paired outputs
- `vpx-script.xenon-2-5-2`: external:pinmame-vpx-sources/bally/xenon-1980/extracted-v2.5.2/script.vbs; SHA256 `3a8e128c1c43ffbccb5f93ba6d8a4f8445e6ff360e1ddcccf6cd2576345ebc1c`. Embedded VPU 6313 v2.5.2; retained release page credits physical measurements/photos by wrd1972 and tube-entrance fix. Exact script ranges below.
- `vpx-table.xenon-2-5-2`: external:pinmame-vpx-sources/bally/xenon-1980/Xenon (Bally 1980) v2.5.2.vpx; SHA256 `f2a9b5f78d9fc736b6c0054bcf22412d356785743a3d5eb02a38d030b2fcba1b`. https://vpuniverse.com/files/file/6313-xenon-bally-1980/ v2.5.2; bounds 0, 0, 952, 1974; source-owned original retained
- `vpx-extraction.xenon-2-5-2`: external:pinmame-vpx-sources/bally/xenon-1980/extracted-v2.5.2; SHA256 `23c6e20722da373a95a7e0a6599dd94577f711610dd659cff262d3289aa66b31`. vpxtool git:v0.33.3; 1532 files, 106093787 bytes. Manifest: every relative POSIX path, size, SHA256 in case-sensitive path order; sort_keys canonical compact JSON UTF-8 plus LF, excluding root manifest.json/manifest.sha256. Raw objects and world-mesh locators in spatial report.
- `vpm-library.bally`: external:pinmame-vpx-sources/shared/vpinmame-20261106/Bally.vbs; SHA256 `d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c`. Machine-neutral Bally.vbs v3.61 copied from installed authorized scripts, with core.vbs and VPMKeys.vbs retained beside it.
- `runtime.xenon`: evidence/runtime/by35/xenon-1980.json; SHA256 `59dd3c83be5677c5a069ceae0921a0e069a08bc94d0843d26170a83ec47d1c67`. Fresh-state service test and isolated gameplay, complete external traces/scenarios hash-pinned; authorized ROM member SHA1s matched pinned Xenon source.
- `photos.xenon`: external:pinmame-review-artifacts/bally.xenon.1980/photos/provenance.json; SHA256 `501c09ffda4195d36a6ab09b13f9a15df0b4de973bc1dc3a7df0293ca4a83fea`. IPDB 2821 model 1196/year 1980 verified; image/page/resource/acquisition/credits/hashes in physical-photo-observations. Pinside sources supplement topology, not wiring authority.
- `repair.xenon-auxiliary`: https://www.flipperfrance.com/threads/eclairage-auxiliaire-sur-xenon.21618/; SHA256 `a3db6ad2b52ac44e16cc6478e1e57f57de5a28e0d57699b4aebebbcab4db6723`. Attributable first-person repair: post 3 J2-9 SIDE SAUCER pair restored by MCR 106-1 replacement; post 5 tube-exit and shooter pairs observed. Complements, rather than replaces, factory wiring; no socket coordinates.
- `vpx-script.xenon-6-0-0`: external:pinmame-vpx-sources/bally/xenon-1980/extracted-v600/script.vbs; SHA256 `1f67d3023ff7c36cbe732bd38750aa0da8f81557b46b86ac40e8415c9de477c9`. https://www.vpforums.org/index.php?app=downloads&showfile=12098 JPsalas 6.0.0, same bounds 952x1974; related factory-layout table supplements the primary, not an independent measurement.

- Remaining spatial_placement: Factory fits SIDE SAUCER 69, END OF TUBE 85, BALL SHOOTER 101. Both related tables drive two far-separated bulb meshes from 69 and omit 85/101. Owner repair establishes the J2-9 pair and observes separate tube-exit/shooter pairs, but neither prose nor current photos locate and trace every socket. Need socket-to-A9J2-9/A9J2-17/A9J3-10 tracing or a numbered factory location drawing, plus a measured top view for the shooter socket. No helper or mirrored coordinate is promoted.
- Remaining output_semantics: Bare AC GI branches are proven, but no complete physical count/location map is printed. Modeled bulb candidates do not prove total quantity or string membership; cabinet/backbox quantities remain unknown. Need a complete annotated socket/branch survey.
- Remaining spatial_placement: Figure V validates 38 of 39 checked placements plus three explicitly justified flipper/bank projections. End-of-tube-lane 1 fails the fit (0.0904 control, 0.0783 callout); tube switch 27 and rebound 26 have leaderless labels inside broad outlines, while release-stack sensors 2/28 and coil 8 are only mechanism-region projections. Controlled lamps and tube bulbs lack numbered socket callouts; their exact retained coordinates remain observed. Need independent socket/leaf locations or an attainable measured physical survey for these specific placements.

All 54 pages of the manual-with-schematics and 41 pages of the operating scan were OCRed; decisive tables/drawings were checked visually. PinMAME supplies topology, the machine's own manual physical construction, known-working retained scripts runtime bindings, and exact geometry raw coordinates. Figure V now validates 38 of 39 checked placements plus three documented mechanism/flipper projections. Its eight independently read controls have 0.0224 RMS and 0.0665 maximum leave-one-out error; the callout fits have 0.0496/0.0591 maximum accepted leave-one-out errors. End-of-tube lane 1 fails and remains observed. Numbered switch/coil placements were checked; unnumbered emitters and explicitly excluded contacts/projections remain observed. No status edit or count agreement can grant author readiness. The primary Sol curator decision is partial.

Factory drawing check source: `drawing-callouts.xenon-1980`, `tools/seeds/bally/xenon-1980-callouts.json`, SHA256 `f89107573a2708eb32f24d230e5647f4c5ec31d3a245aeb19bf0c0dd168b44b1`. The report retains each measured pixel, fit and decision; the overlay manifest pins the independent reading artifacts.
