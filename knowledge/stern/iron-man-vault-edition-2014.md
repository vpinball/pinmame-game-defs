# Iron Man Pro Vault Edition (Stern, 2014)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical I/O inventory, PinMAME bindings, wiring, custom mechanisms, edition construction, and recreation behavior validated**

## Identity and evidence precedence

This is the June/July 2014 Iron Man Pro Vault Edition reissue, IPDB 6154, model I-00B0 and Stern product 500-55B0-01. It covers only `im_183ve`, `im_185ve`, and `im_186ve`; the non-`ve` drivers belong to the original 2010 physical product even though PinMAME's clone graph shares one root. The exact `im_185ve` VPW script is runtime ground truth, the 2014 native-text service manual governs physical inventory/wiring, the original parts book documents inherited geometry, and PinMAME governs transport/display metadata.

## Vault Edition construction boundary

The logical game and mechanism map is shared with the original. The reissue adds LED playfield lighting, a modern metal/wood backbox with red T-molding, brushed-aluminum cabinet decals and new speaker-panel art, strengthened one-piece molded Iron Monger/War Machine/Whiplash toys, and Stern's then-current one-piece auto launcher. Preserve those physical differences when recreating this product. The service matrix uses LED module 112-5033-08 for most inserts but explicitly calls for clear #555-form-factor lamps at 54, 56, 73, 79, and 80; the three row-10 lamps are unlabeled load/test positions absent from the playfield location map.

## Ball path and custom devices

Four balls occupy switches 18-21; jam opto 22 and trough up-kicker 1 serve shooter switch 23, which supports manual and automatic launch through output 2. War Machine opto 10 holds a ball until kick-back output 5 ejects it. Orbit and center-lane posts are outputs 6 and 12 and have no sensors. Whiplash magnet 4 acts near targets 47/48. Spinners are 11/13/14, ramp entrance/exits 12/43/37/49, orbit rollovers 7/9, and the four drone targets 44-46/50. Never create a physical trough-release switch at address 15; the manual proves it is Tournament Start despite an old VPX bookkeeping pulse.

## Motorized Iron Monger

Output 19 toggles the Iron Monger lift between endpoint switch 1 down and switch 3 up. Target faces 4-6 and the toy's collision/flash geometry move with it; targets must become unavailable below the playfield. Output 3 is the strong non-centering magnet in the assembly. The proven table's 240-unit travel over 62 update steps is useful initial tuning, but its early endpoint-switch mutation is an animation shortcut. A recreation must report endpoints when physical travel reaches them and must apply magnetic force without teleporting the ball.

## Standard devices, lamps, and capacity

Flippers are outputs 15/16 with button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops pair 9/30, 10/31, 11/32, and slings 17/26, 18/27. Output 8 is an optional 16 VAC shaker on RED-WHT/J17-P7; the manual's Q8 table says 50 VDC but its transformer/I/O schematics prove the 16 VAC feed. Q7/Q13/Q14 are unused. Q24 is the manual's optional 5 V coin-meter/device channel even though the proven VPW table includes it in the SetLampMod flasher block; the physical service table wins and no stock Q24 playfield flasher should be created. Q20-23/Q25-32 are LED flashers with exact module parts in the JSON. Lamp 1-63 and 73/79/80 are populated; 64-72 and 74-78 are unused. Bind GI 0, synthetic game-on 33, explicit unused SAM auxiliary capacity 51-66, and the 128x32 four-bit DMD; never turn legacy aliases 34-36 or auxiliary capacity into playfield hardware.

## Author construction checklist

- Build the typed four-ball trough, one-piece manual/auto launch, War Machine capture/kickback, strengthened moving Iron Monger with endpoints/targets/magnet, Whiplash target/magnet, both unsensed up-posts, ramps/orbits/spinners, fixed target banks, flippers, pops, slings, and optional shaker.
- Initialize switches 18-21 and Iron Monger down switch 1. Preserve ball occupancy, normally-closed EOS contacts, moving collision geometry, and real endpoint timing.
- Bind every matrix/dedicated/DIP input, Q1-Q32, game-on 33, unused auxiliary 51-66, lamp 1-80, GI 0, and DMD, including the three unlabeled clear matrix bulbs.
- Use the exact VPW behavior as the runtime tie-breaker and the official 2014 service manual for construction, wiring, parts, and lamp technology.

## Sources

- `manual.iron-man-vault-edition.2014`: official manual SHA-256 `20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990`; organized under the external manual cache.
- `vpx.iron-man-vault-vpw-1.0.1`: pinned known-working exact-ROM script SHA-256 `d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea`.
- `rom.iron-man-vault.im-185ve`: exact external archive SHA-256 `e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f`; contained binary SHA-256 `c827da1c3f5305b27e9e504d7553bcd9c39547f357dd3827122adcc4c173c257`.
- `runtime.iron-man-vault.boot-start`: exact boot/start trace SHA-256 `2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9` with game-on 33, DMD, lamps, and GI observed.
