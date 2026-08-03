# TRON: Legacy Pro (Stern, 2011)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical inventory, PinMAME bindings, wiring, mechanisms, initial state, and edition boundary validated**

## Identity and evidence precedence

This definition covers non-`h` drivers `trn_110`, `trn_120`, `trn_140`, `trn_150`, `trn_160`, `trn_170`, `trn_174`, and `trn_17402`. PinMAME roots them under LE firmware for software lineage, but they run the physically different Pro playfield. The official Pro service charts govern installed hardware and wiring. The known-working LE script is ground truth only for shared callbacks, motion, ball routing, and controller behavior; no LE-only device is projected onto Pro. IPDB 5682 identifies this first-edition Pro product as model I-00B9.

## Initial balls, launcher, and eject

Four balls occupy trough switches 18-21. Output 1 ejects through jam opto 22 toward shooter switch 23; the proven table uses 90 degrees and force 8. Output 2 drives the auto launcher while retaining a manual plunger. Flynn's video-game eject holds on switch 11 and output 4 ejects at 200 degrees, force 24, Z 0.4, with variance 2.

## Pro TRON bank and Recognizer bank

Pro switches 1-4 are fixed TRON standups, not drop targets. Output 3 is therefore the disc-direction relay and must not reset or animate them. The common three-target Recognizer bank uses hit switches 49-51, output 6, down switch 52, and up switch 53. The proven 29-step recreation starts down, raises targets to Z -20, lowers them to -76, and removes target collisions near the lower endpoint. Pro has no separate moving Recognizer toy and switches 54-56/output 23 retain their Pro service-chart meanings instead of the LE motion system.

## Spinning disc and orbit post

The Rinzler identity disc is a real rotating ball-contact surface. Output 5 supplies disc power, output 3 selects direction, and output 30 is the physical motor relay. Switch 41 is the disc-area opto, not an index sensor. The proven recreation uses maximum turntable speed 8, direction steps ±40, a 10 ms motion timer, and 0.1-per-tick coast-down. Output 7 raises the orbit post while active and drops it while clear; there is no post endpoint sensor.

## Flippers and playfield routes

Output 12 drives the upper-left flipper used for the right ramp. The official Pro dedicated-switch chart on PDF page 49 identifies D13/D14 public 88/87 as its button and normally-closed EOS; the LE chart on PDF page 55 leaves both contacts blank. The proven script's commented output-34 compatibility hook is not another coil: local staged-flipper key handlers directly call `SolULFlipper`, while physical output 12 remains authoritative. Lower flippers are 15/16 with button/EOS pairs 84/83 and 82/81. Ramps use switches 34/35/37/38, right inner loop 39, orbits 43/46, and spinners 36/44. CLU lanes are 14/25/28, ZUSE targets 7/8/13/48, Zen rollover 12, and outlanes 24/29. Pops pair 9/30, 10/31, 11/32; slings pair 13/26 and 14/27.

## Lighting and edition boundary

The Pro lamp map is physically different from LE: 1-35, 37-45, 48-53, 55-64, and 66 are populated; 36, 46, 47, 54, and 65 are unused. Start/Tournament are 1/2. Bumper lamps 60-62 are factory LEDs; the other populated Pro matrix positions use #555 lamps. Public custom channels 101-106 exist through the common PinMAME TRON transport but the stock Pro lacks the LE tricolor ramp assembly, so they are explicit unpopulated channels. Do not import the LE four-drop reset, moving Recognizer/sensors, LED lamp numbering, dome mapping, or ramp-light hardware.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, Flynn eject, fixed TRON standups, two-position Recognizer target bank, rotating disc with physical ball interaction, orbit post, three flippers with all Pro button/EOS contacts, pops, slings, ramps, loops, orbits, spinners, CLU/ZUSE targets, Zen rollover, and every flasher group.
- Preserve target-bank collision enablement, disc friction/throw, held-ball states, unsensed post motion, and the upper-flipper shot geometry. Cosmetic animation is insufficient.
- Bind all 64 matrix inputs, dedicated/DIP spaces, physical outputs 1-32, synthetic game-on 33, explicit unused VPX compatibility address 34, lamps 1-80 plus explicit 101-106 compatibility channels, GI 0, and the 128x32 four-bit DMD.

## Sources

- `manual.tron-legacy-pro-le.2011`: official Stern manual, SHA-256 `1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84`; Pro switches/coils/lamps PDF pages 49/51/53 and location maps 50/52/54.
- `vpx.tron-legacy-le-vpm-1.1.4`: known-working shared-hardware reference at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc`.
- `runtime.tron-legacy-pro.boot-start`: exact `trn_174` harness with the shared target bank initialized down on switch 52, SHA-256 `51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM transport, driver family, DMD, GI, tricolor address allocation, and game-on output.
