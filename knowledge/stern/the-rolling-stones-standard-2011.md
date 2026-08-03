# The Rolling Stones Standard (Stern, 2011)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical inventory, PinMAME bindings, mechanism causality, wiring, and edition boundary validated**

## Identity and evidence precedence

This definition covers non-`h` drivers `rsn_103`, `rsn_105`, and `rsn_110`. PinMAME roots them under `rsn_110h` for software lineage, but they run the Standard physical playfield. IPDB identifies the Standard machine as 5668. The official Stern service chart governs physical inventory and wiring. The known-working LE VPX script is ground truth for public addresses and shared mechanism causality; its Premium-only devices are never projected onto Standard. Pinned PinMAME governs SAM serialization, `SAM_NO_AUX`, synthetic game-on 33, and the native 128x32 four-bit DMD.

## Edition boundary and initial state

The Standard trough contains four steel balls at switches 18-21. It omits matrix switch 17, top shooter switch 50, dedicated magnetic detector D7/public 71, cabinet post buttons D13/D15, both magnets, all three up/down posts, and Premium bottom-arch output 29. Accordingly outputs 5, 7, 17, 29, 30, and 32 are explicit unused Standard channels. The manual calls the fuller service-chart variant “Premium”; that hardware corresponds to PinMAME's Limited Edition `h` drivers. Standard still uses moving target D8/public 72 and common Mick position switches 33-39.

## Moving Mick

Moving Mick is a physical traversing target with seven discrete sensors, not seven hit targets. Output 18 moves left and 19 right. The proven script clamps travel from -27 to +36 degrees and asserts one sensor only at each narrow stop: 33 home/right, then 34, 35, 36, 39 park, 37, and 38 away/left. All seven positions share dedicated hit switch 72. The collision body must move with Mick across sensed and unsensed transit zones. Six inserts correspond to positions 1-4 and 6-7; position 5/park deliberately has no lamp.

## Locks, shooter, and ball paths

The center lock uses switch 53 at the bottom and switch 46 at the upper left-lock position. Output 3 raises the lock and output 4 holds/releases the latch barriers. Output 1 feeds the trough; output 2 auto-launches from switch 23 while retaining the manual plunger. Output 6 controls the left gate. Ramps exit at 42/45, orbits at 44/48, the passive left-orbit spinner pulses 41, pop lane is 43, and band-member top lanes are 6-9.

## Remaining playfield inventory

The two flippers are outputs 15/16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 13/26 and 14/27. Fixed target groups are Mick 1-3, right bank 10-12, STAR 51/57/56, and ROCK STAR 54/55. Q12 is physically unused, output 8 is the optional shaker, and output 24 is an optional 5 V coin meter. Lamps 1-53, 58, and 60-62 are used; 54-57, 59, and 63-80 are explicit unused addresses. Output flashers 20-23 and 25-28/31 are separate from matrix lamps.

## Author construction checklist

- Build the four-ball trough, manual plunger plus auto launcher, center lock/latch, moving target with seven position sensors and one shared hit switch, left control gate, two flippers, three pops, two slings, spinner, two ramps, two orbits, lanes, and fixed target groups.
- Bind every matrix and dedicated input, output 1-33, lamp 1-80, GI 0, and DMD from the JSON. Keep unused channels explicit and do not add Premium mechanisms to Standard.
- Preserve ball occupancy, lock barriers, moving collision geometry, Mick transit/endpoint causality, and the manual plunger path. Cosmetic animation is insufficient for the moving target or lock.
- Use the proven VPX motion ranges and callback causality as starting values while retaining the official service-manual physical boundary and wiring.

## Sources

- `manual.rolling-stones-standard-le.2011`: official Stern manual, SHA-256 `1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf`; switches PDF page 51, lamps 53, coils 55/78, assemblies 1-24, and wiring 85-95.
- `vpx.rolling-stones-le-1.0.6i`: known-working script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`; used only for shared hardware causality on Standard.
- `runtime.rolling-stones-standard.boot-start`: exact `rsn_110` harness, SHA-256 `56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and driver family.
