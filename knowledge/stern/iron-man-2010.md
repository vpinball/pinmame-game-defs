# Iron Man (Stern, 2010)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical I/O inventory, PinMAME bindings, wiring, mechanism causality, original-versus-Vault boundary, and recreation behavior validated**

## Identity and evidence precedence

This is the original 2010 Iron Man physical product, IPDB 5550, model I-00B3. It covers `im_100`, `im_110`, `im_120`, `im_140`, `im_160`, `im_181`, `im_182`, `im_183`, `im_185`, and `im_186`; firmware catalog years through 2020 do not change the playfield's 2010 construction. PinMAME roots the family under the Vault driver for software lineage, but that does not turn these ROMs into the 2014 reissue. The proven VPW script is runtime ground truth, the official service/parts manuals control physical construction and wiring, and PinMAME controls transport/display metadata.

## Original versus 2014 Pro Vault Edition

Both products use the same logical switch, Q-output, lamp, GI, DMD, and custom-mechanism map, and Stern states code 1.86 applies to both. The original uses its 2010 wood/cabinet/backbox treatment, incandescent insert/GI/flasher construction, earlier multi-piece auto-launch and toy assemblies, and original cabinet/speaker art. Do not project the Vault Edition's LED modules, strengthened one-piece Iron Monger/War Machine/Whiplash toys, brushed-aluminum cabinet art, red T-molding, modern metal/wood backbox, or current one-piece auto launcher backward. PinMAME's prefix-wide LED output typing is emulator metadata and is not evidence that the 2010 machine shipped with LEDs.

## Ball path, trough, and shooter

Four balls initialize on trough switches 18-21. Jam opto 22 sees an ejecting ball and output 1 serves it toward shooter-lane switch 23. The shooter supports the manual plunger and output 2 auto launch. Switch 10 is the War Machine capture opto; output 5 kicks that ball back into play. Main route sensors are orbit rollovers 7/9, spinners 11/13/14, ramp entrance/exits 12/43/37/49, top lanes 38/39, returns/outlanes 24/25/28/29, and the seven fixed Iron Man targets 33-36 and 40-42. The VPX trough routine's pulse of switch 15 is only a table workaround: physical switch 15 is Tournament Start.

## Iron Monger and magnets

Iron Monger is a moving collision assembly, not a cosmetic animation. Output 19 toggles travel between switch 1 down and switch 3 up; shoulder/legs targets 4-6 move with it and become unavailable below the playfield. The proven table uses a 240-unit range over 62 update steps, which is useful initial tuning. Output 3 is the strong non-centering Iron Monger magnet. Output 4 is the separate Whiplash magnet by targets 47/48. Apply real force to a steel ball and retain moving target/collision geometry; do not teleport the ball or set endpoint switches before travel completes.

## Posts and standard devices

Output 6 commands the orbit up-post and output 12 the center-lane up-post; both are unsensed and must change physical collision state. Flippers use outputs 15/16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops pair 9/30, 10/31, and 11/32. Slings pair 17/26 and 18/27. Output 8 is an optional 16 VAC shaker on RED-WHT/J17-P7: the manual's Q8 table prints 50 VDC, but its transformer/I/O schematics prove the 16 VAC secondary. Q7, Q13, and Q14 are unpopulated. Q24 is the manual's optional 5 V device/coin-meter channel even though the proven VPW table includes address 24 in its SetLampMod flasher block; physical service construction governs, so do not add a stock Q24 playfield flasher.

## Lamps, flashers, and controller capacity

Lamp addresses 1-63 are populated, 64-72 are unused, 73/79/80 are hidden clear #555 row-10 bulbs, and 74-78 are unused. Address 55 has quantity two and Q20-23/Q25-32 carry explicit physical quantities, including the two Q31 lower-left-ramp emitters. Those multiplicities are documented cross-edition inferences from the same logical/playfield layout: the numbered callouts are in the 2014 Vault location maps and the exact working table is the Vault VPW, while the 2010 parts book does not number lamp or coil addresses. The original parts drawing shows unnumbered twist-lock sockets over the playfield underside; population of 73/79/80 is likewise a documented cross-edition inference from that construction, Stern's shared-code compatibility, and the later service grid rather than a numbered 2010 callout. Preserve original incandescent construction for every shared emitter, and bind lamp matrix 1-80, GI 0, synthetic game-on 33, explicit unused auxiliary compatibility addresses 51-66, and the 128x32 four-bit DMD. Public solenoids 34-36 are legacy aliases of game-on 33 and are not physical outputs.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, War Machine capture/kickback, motorized Iron Monger with moving collision targets and both endpoints, both non-centering magnets, two unsensed up-posts, two ramps, orbit/spinner network, fixed target banks, flippers, pops, slings, and optional shaker.
- Initialize trough switches 18-21 and Iron Monger down switch 1. Preserve EOS polarity, actual motor endpoint timing, ball occupancy, and collision gating.
- Bind every explicit matrix/dedicated/DIP input, Q1-Q32, game-on 33, unused auxiliary capacity 51-66, lamp 1-80, GI 0, and DMD. Keep unused and optional channels explicit.
- Use the proven VPX script when runtime behavior is ambiguous, but use the 2010 parts book for original construction and the 2014 manual only for the shared logical/wiring map.

## Sources

- `manual.iron-man-original-parts.2010`: official scanned 2010 parts book SHA-256 `0948d154156860d351daa943ab3b5882ef4c86bb42cde630bcd04067ab85ed1a`; organized under the external manual cache.
- `manual.iron-man-vault-edition.2014`: official native-text service manual SHA-256 `20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990`; shared logical tables and wiring are on PDF pages 16-21 and 48-58.
- `vpx.iron-man-vault-vpw-1.0.1`: exact known-working `im_185ve` script SHA-256 `d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea` at pinned revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`.
- `runtime.iron-man-vault.boot-start`: exact-ROM compatible-code trace SHA-256 `2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9`; ROM bytes remain external.
