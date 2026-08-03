# Iron Man Pro Vault Edition (Stern, 2014)

Coverage: **author-ready - complete physical I/O inventory, PinMAME bindings, wiring, custom mechanisms, edition construction, and recreation behavior validated**

## Identity and evidence precedence

This is the June/July 2014 Iron Man Pro Vault Edition reissue, IPDB 6154, model I-00B0 and Stern product 500-55B0-01. It covers only `im_183ve`, `im_185ve`, and `im_186ve`; the non-`ve` drivers belong to the original 2010 physical product even though PinMAME's clone graph shares one root. The exact `im_185ve` VPW script is runtime ground truth, the 2014 native-text service manual governs physical inventory/wiring, the original parts book documents inherited geometry, and PinMAME governs transport/display metadata.

## Vault Edition construction boundary

The logical game and mechanism map is shared with the original. The reissue adds LED playfield lighting, a modern metal/wood backbox with red T-molding, brushed-aluminum cabinet decals and new speaker-panel art, strengthened one-piece molded Iron Monger/War Machine/Whiplash toys, and Stern's then-current one-piece auto launcher. Preserve those physical differences when recreating this product. The service matrix uses LED module 112-5033-08 for most inserts but explicitly calls for clear #555-form-factor lamps at 54, 56, 73, 79, and 80; the three row-10 lamps are unlabeled load/test positions absent from the playfield location map.

## Ball path and custom devices

Four balls occupy switches 18-21; jam opto 22 and trough up-kicker 1 serve shooter switch 23, which supports manual and automatic launch through output 2. War Machine opto 10 holds a ball until kick-back output 5 ejects it. Orbit and center-lane posts are outputs 6 and 12 and have no sensors. Whiplash magnet 4 acts near targets 47/48. Spinners are 11/13/14, ramp entrance/exits 12/43/37/49, orbit rollovers 7/9, and the four drone targets 44-46/50. Never create a physical trough-release switch at address 15; the manual proves it is Tournament Start despite an old VPX bookkeeping pulse.

## Motorized Iron Monger

Output 19 toggles the Iron Monger lift between endpoint switch 1 down and switch 3 up. Target faces 4-6 and the toy's collision/flash geometry move with it; targets must become unavailable below the playfield. Output 3 is the strong non-centering magnet in the assembly. The proven table's 240-unit travel over 62 update steps is useful initial tuning, but its early endpoint-switch mutation is an animation shortcut. A recreation must report endpoints when physical travel reaches them and must apply magnetic force without teleporting the ball.

## Standard devices, lamps, and capacity

Flippers are outputs 15/16 with button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops pair 9/30, 10/31, 11/32, and slings 17/26, 18/27. Output 8 is an optional 16 VAC shaker on RED-WHT/J17-P7; the manual's Q8 table says 50 VDC but its transformer/I/O schematics prove the 16 VAC feed. Q7/Q13/Q14 are unused. Q24 is the manual's optional 5 V coin-meter/device channel even though the proven VPW table includes it in the SetLampMod flasher block; the physical service table wins and no stock Q24 playfield flasher should be created. Q20-23/Q25-32 are LED flashers with exact module parts in the JSON; Q31 drives the two lower-left-ramp emitters shown in the location map and called x2 by the exact script. Lamp 1-63 and 73/79/80 are populated; address 55 drives two physical Mark VI emitters, 64-72 and 74-78 are unused, and the hidden row-10 bulbs are non-playfield electrical loads. Bind GI 0, synthetic game-on 33, explicit unused SAM auxiliary capacity 51-66, and the 128x32 four-bit DMD; never turn legacy aliases 34-36 or auxiliary capacity into playfield hardware.

## Spatial construction and multiplicity

Player-view positions use x=0 left, x=1 right, y=0 rear/backglass, and y=1 apron. Exact coordinates come from the organized 245,182,464-byte VPW table after semantic reconciliation against the official switch, lamp, coil, and GI maps. The controller script is runtime ground truth, but VLM light-map callbacks, reflections, transmission layers, and room/VR effects are renderer helpers rather than physical devices. Jam opto 22 has no table object; its disclosed approximate anchor is a least-squares continuation of the exact consecutive sw18-sw21 centers, with about plus or minus 0.02 normalized x/y uncertainty.

The official GI schematic fixes 27 playfield emitters on circuits B/Y/V (10/7/10), ten rear-panel emitters on circuit G, and two US or three European coin-door bulbs. Playfield construction is 25 under-playfield #44 bulbs plus one above-playfield #555 bulb on circuit Y and one on circuit V. The latter use exact `Lspot1`/`Lspot2` source centers: the VPW changelog says spotlight bulbs were separated and its ball-shadow code treats those objects as sources. Nearby `gi004`/`gi014` are the separated halo/render passes, not two more sockets; the other 25 physical playfield positions use exact `giNNN` centers. Objects `gi024`, `gi027`, `gi030`, and `gi031` are four rear-wall render pools introduced for backwall illumination, not physical sockets. The ten physical rear #44 sockets are represented by an explicit evenly spaced y=0 projection across the manual's single rear-panel row because the perspective sketch proves row and count but not ten independently measurable centers. The US coin-door branch has two #555 bulbs and the European branch three; cabinet bulbs intentionally have no playfield coordinate. The JSON uses US quantity 39 and documents European quantity 40.

Physical multiplicity follows the service maps even when VPW combines light output: Q22 has two modules at one War Machine-front cluster, Q27 has three War Machine modules, Q28 has three moving Iron Monger chest modules at one toy anchor, Q30 has two separately located Mark VI flashers around one combined table pool, and Q31 has two separately located lower-left-ramp emitters around one combined table pool. Lamp 55 likewise drives two separately mapped physical Mark VI emitters through one address while VPW exposes one central pool. Hidden row-10 lamps 73/79/80 are explicit internal nonvisual electrical loads with no invented playfield position; they are not cabinet devices. Cluster anchors preserve the correct construction region and quantity without misclassifying visual fanout as additional hardware.

Where the exact table collapses distinct modules, the individual Q27/Q30/Q31/lamp-55 construction anchors are calibrated from multiple official-map callouts against exact shared table points. Those manual projections have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y; they preserve proven physical region and separation without claiming unrecoverable table precision.

## Author construction checklist

- Build the typed four-ball trough, one-piece manual/auto launch, War Machine capture/kickback, strengthened moving Iron Monger with endpoints/targets/magnet, Whiplash target/magnet, both unsensed up-posts, ramps/orbits/spinners, fixed target banks, flippers, pops, slings, and optional shaker.
- Initialize switches 18-21 and Iron Monger down switch 1. Preserve ball occupancy, normally-closed EOS contacts, moving collision geometry, and real endpoint timing.
- Bind every matrix/dedicated/DIP input, Q1-Q32, game-on 33, unused auxiliary 51-66, lamp 1-80, GI 0, and DMD, including the three unlabeled clear matrix bulbs.
- Recreate all documented emitter multiplicities, ten rear-panel GI sockets, the applicable two- or three-bulb coin-door GI branch, and both address-55 Mark VI emitters; do not use the number of VPX render helpers as a parts count.
- Use the exact VPW behavior as the runtime tie-breaker and the official 2014 service manual for construction, wiring, parts, and lamp technology.

## Sources

- `manual.iron-man-vault-edition.2014`: official manual SHA-256 `20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990`; organized under the external manual cache.
- `vpx.iron-man-vault-vpw-1.0.1`: pinned known-working exact-ROM script SHA-256 `d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea`.
- `vpx-table.iron-man-vault-vpw-1.0-geometry`: organized exact table SHA-256 `c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b`; table bounds are 0..952 by 0..2215 and only semantically reconciled geometry is used.
- `rom.iron-man-vault.im-185ve`: exact external archive SHA-256 `e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f`; contained binary SHA-256 `c827da1c3f5305b27e9e504d7553bcd9c39547f357dd3827122adcc4c173c257`.
- `runtime.iron-man-vault.boot-start`: exact boot/start trace SHA-256 `2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9` with game-on 33, DMD, lamps, and GI observed.
