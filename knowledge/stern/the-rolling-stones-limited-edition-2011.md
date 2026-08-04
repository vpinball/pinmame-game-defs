# The Rolling Stones Limited Edition (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, recreation behavior, and normalized spatial placements validated**

## Identity and evidence precedence

This definition covers `rsn_100h` and `rsn_110h`, the PinMAME Limited Edition family, and IPDB machine 5708. The service charts label the fuller hardware “Premium”; the PinMAME descriptions and physical product record call it Limited Edition. They are treated as one physical I/O variant, not a third machine. The known-working `The Rolling Stones LE (Stern 2011) v1.0.6i.vbs` is ground truth for address callbacks and mechanism causality, with the official manual authoritative for installed wiring.

## Five-ball trough and ceramic ball

The LE trough holds five balls at switches 17-21. One is a white nonmagnetic ceramic ball. Dedicated D7 serializes as public 71 with an active-low/normally-closed controller sense: the proven table initializes 71 active, drives it inactive while the ceramic ball occupies trough switch 21, and restores it after the ball clears shooter switch 23. Drain handling preserves the ball's identity. Recreate a per-ball material/type flag; replacing every drain with a generic steel ball breaks detector and magnet behavior. Output 1 feeds through jam opto 22, output 2 auto-launches, and the LE adds top shooter switch 50 while retaining the manual plunger.

## Magnetized ball diverter and player controls

The LE adds left/right 50 V magnets on outputs 5/7 and left/center/right 20 V up/down posts on 17/30/32. In the proven table, an enabled post rises into the ball path and imparts an upward reaction on collision. Dedicated cabinet buttons D13/D15 serialize as public 88/86 for the left/right posts; the center post is ROM-driven and has no dedicated player button. The script also mirrors the ordinary flipper keys into public 87/85, but the service chart leaves physical D14/D16 unpopulated; those are explicit virtual compatibility states, not two extra cabinet switches. Model all five actuators, both real buttons, magnetic response by ball material, and the resulting routing/collision behavior.

## Moving Mick

Outputs 18/19 move Mick left/right across seven stops. Position sensors are 33 home/right, 34, 35, 36, 39 park, 37, and 38 away/left. The proven angular windows are +34..36, +24..26, +14..16, +3..5, -7..-6, -17..-15, and -27..-25 degrees. Every physical collision pulses the single dedicated target switch 72. Keep separate target-hit and carriage-position state, plus unsensed transit geometry. Position 5/park intentionally has no dedicated position lamp.

## Center lock, gate, and common mechanisms

Switches 53/46 sense the center/left lock path. Output 3 raises the lock and output 4 controls its latch; latch release drops both modeled barriers. Output 6 controls the left gate. Flippers use 15/16 with button/EOS pairs 84/83 and 82/81. Pops are 9/30, 10/31, and 11/32; slings 13/26 and 14/27. Ramps exit at 42/45, orbits at 44/48, spinner at 41, pop lane at 43, and top lanes at 6-9. Fixed standups are Mick bank 1-3, right bank 10-12, STAR 51/57/56, and ROCK STAR 54/55.

## Lamps, flashers, and optional devices

Lamps 1-53, 58, and 60-62 are used; 54-57, 59, and 63-80 are unused. Output 29 drives two LE bottom-arch flashers in addition to common flashers 20-23, 25-28, and 31. Q12 is unused. Output 8 is an optional 16 VAC shaker and output 24 an optional 5 V coin meter. The machine uses `SAM_NO_AUX`; no auxiliary-board output range should be invented.

## Author construction checklist

- Build the five-ball typed trough, detector behavior, manual/auto shooter with both switches, two magnets, three up/down posts and cabinet buttons, center lock/latch, moving Mick with all seven positions and shared hit switch, gate, flippers, pops, slings, spinner, ramps, orbits, lanes, and standups.
- Preserve ceramic-versus-steel magnetic response, individual ball identity through drain/trough cycling, raised-post collisions, lock occupancy, and moving-target collision geometry.
- Treat public 87/85 as proven VPX compatibility states with no physical D14/D16; do not turn them into extra cabinet controls. Treat service-manual “Premium” notes as this LE hardware variant.
- Bind the complete explicit I/O address spaces, including unused channels, synthetic game-on 33, GI 0, and the 128x32 DMD.

## Normalized spatial model and reconciliation

Coordinates use the global player-view playfield frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron. Exact VPX centers were normalized from its 1000 x 2000 bounds after reconciling the known-working script's callback names with the official manual's physical inventory. Named walls and moving primitives are represented by their main collision/assembly center. Paired render layers are never promoted as separate hardware.

Every used physical switch has a sensor placement, including the manual-ordered derived projection for SW22 and all seven positions of the one shared Moving Mick hit switch 72. Every used physical coil, magnet, relay, and post effect has an effect placement; moving endpoints remain explicit in the mechanism inventory. Matrix lamps, flashers, and all 40 individual GI collection emitters have emitter placements. Light20 is excluded from GI because it is the same physical/object center as matrix lamp 20. The two rear-panel flashers, cabinet lamps, shaker, coin meter, tilts/service controls, virtual compatibility states, unused channels, DIP switches, and internal magnetic detector are explicit controlled non-playfield N/A records. The aggregate DMD remains a display record without a playfield coordinate in the base schema. The exact VPX's F25/F25a/F25pf, F27/F27a/F27pf, and F28/F28a/F28pf objects are synchronized render layers collapsed to one physical socket per manual circuit; manual page 55 marks only F29 X2, while F25/F27/F28 have no multiplier; output 29 retains that manual-proven X2 multiplicity.

SW22 reuses the committed Standard sibling's `(0.727167, 0.982)` manual-ordered trough-region projection because the manual establishes the same downstream jam-opto arrangement for LE/Premium and the exact LE table supplies no competing SW22 object. This is a derived physical-equivalence marker with practical uncertainty of about plus or minus 0.02 normalized x and 0.02 normalized y, never an exact VPX coordinate.

The official manual remains authoritative for LE/Premium multiplicity and edition boundary. The exact table is authoritative for edition-matched geometry only after that semantic reconciliation. The Standard definition intentionally remains spatially fail-closed and receives none of these LE coordinates.

## Sources

- `manual.rolling-stones-standard-le.2011`: official Stern manual, SHA-256 `1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf`; Premium-only switch/output notes and magnetized-diverter wiring are on PDF pages 51, 55, and 95.
- `vpx.rolling-stones-le-1.0.6i`: known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`; semantic and causality ground truth.
- `vpuniverse.rolling-stones-balutito-mod-2-0-24384`: authenticated VPUniverse metadata page identifies ROM Name `rsn_110h`; identity evidence only, with no table artifact downloaded or hashed.
- `vpx-table.rolling-stones-le-archive-2020`: exact archive VPX, SHA-256 `da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10`; embedded `rsn_110h`, exact 1000x2000 geometry, and retained 176-point candidate extraction.
- `runtime.rolling-stones-limited-edition.boot-start`: exact `rsn_110h` harness, SHA-256 `81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, driver family, display, and no-aux configuration.
