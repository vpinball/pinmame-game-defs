# Data East Time Machine (1988)

Machine definition: `machines/partial/data-east/time-machine-1988.json`

## Identity and controller contract

Pinned PinMAME defines `tmac_a24` as the clone-tree parent, with `tmac_a18` and `tmac_g18` cloning it. All three catalog rows are dated 12/88. The physical declaration is `INITGAMES11(tmac, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, 0)`. The parent is the highest revision because that is what the macro says; no revision-order rule was inferred.

`de_dispAlpha2` supplies two seven-character alphanumeric and two seven-character numeric displays. They are controlled backbox devices and have explicit `not_applicable` playfield-spatial records. The machine is correctly bound to `pinmame.dataeast`; no Data East controller profile is authored, so `controller_platform` remains a concrete coverage blocker rather than borrowing the System 11 profile. `INITGAMES11` leaves Time Machine's `wpc.invSw` array zero-initialized, and `core.c` copies that zero mask into `coreGlobals.invSw`, so the emulator applies no per-game switch inversion for any of the three drivers.

## Address coverage

- Inputs: service switches -7/-6, DIP/jumper address 0, and every matrix address 1-64.
- Outputs: every lamp address 1-64 and every Data East public solenoid address 1-50.
- Solenoid 23 is the Game On/control signal; 24 is unused; 33-44 are inert; 45-48 are synthetic lower-flipper winding states; 49 is a simulation-only shooter state; 50 is reserved.
- Solenoid 10 is the left/right mux relay. Its public right bank is 25-32. The manual says the complete left/right arrangement effectively provides 23 regular coils, while its device chart names only SIDE R 01-04. Manual and script resolve mechanisms only at 25-28; pinned source configures four distinct emulator-published mux states at 29-32, but no retained runtime trace proves their per-address activity and no retained source identifies fitted physical circuits for SIDE R 05-08.

## Lamp mapping and the 65th object

The active script calls `vpmMapLights AllLamps`. Shared VPM uses each Light's `TimerInterval` as its ROM lamp index. The collection contains 134 Light members and covers TimerInterval 1-65. Addresses 1-64 are the complete hardware matrix. The sole TimerInterval-65 member is `l65`, an `is_backglass=true` presentation helper on `hSpacewarpLights`; the controller never publishes lamp 65, so it is deliberately excluded rather than counted as an output.

Lamp 25 remains conflicted: the manual explicitly prints `2X All Scores Cntr Plyfld`, but the collection's sole TimerInterval-25 object is marked backglass. No coordinate is selected. Backbox/back-panel lamps are also kept off the playfield coordinate plane even when the retained table uses in-bounds presentation proxies.

## Mechanism topology

The script supplies causality and the manual supplies construction. Together they establish a serial three-ball trough, an outhole feeder, a three-position visible lock released by one cam/coil assembly, a separate super VUK reached from an under-playfield path, the Laser Kick outlane kickback, two flippers, two slingshots, three pop bumpers, three independent fixed three-target standup banks, a manual shooter, and fixed ramp/wireform paths. The standup banks are not drop-target banks: the manual assembly shows switch/bracket targets and no reset coil.

The special-solenoid table and location drawing swap SP1/SP2 between the right and center pop bumpers. Pinned `s11.c` PIA comments identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4; applying `setSSSol`'s Data East offsets `(3, 4, 5, 1, 0, 2)` derives SP1, SP3, SP4, SP6, SP5 and SP2 at public addresses 17-22. This is not inferred by treating printed SP numbers as handler indices. The right/center mechanisms keep empty actuator lists until an original-machine capture settles the disagreement; SP3, SP4, and SP5 agree as left sling, left pop, and right sling, while SP6 is unfitted.

## Manual transcription policy

The retained Archive.org manual is a 78-page, 4,542,921-byte scan with SHA-256 `f232f8114ea31776a9d49e274b5ebed32cb3805acb4e719785fe48d43ddd719c`. Only visible rendered-page content is used: PDF 26-27 = printed 22-23 (switches), 28-29 = printed 24-25 (lamps), 30-31 = printed 26-27 (coils), 67 = printed 47 (parts list), 74 = printed 54 (three-bank standups), 76 = printed 56 (lock bracket), and 77 = printed 57 (super VUK). PDF 78 is blank.

## Retained table and geometry

The retained table SHA-256 is `b6c4b39bc7a672c1914b25e19192ec4cde8432aae00f9a5cd913c9b2f3c3c4f4` and binds the correct parent with `Const cGameName = "tmac_a24"`. Its exact bounds are 1000 by 1910. Both values are asserted before normalization. Whole-line VBScript comments are removed before any callback or mapping claim; inline executable code remains.

## Coverage and blockers

Status remains `partial`. `coverage.missing` is [`controller_platform`, `output_semantics`, `mechanism_behavior`, `polarity`, `spatial_placement`, `unresolved_conflicts`].

- `controller_platform`: the Data East platform has no authored controller profile.
- `output_semantics`: public 29-32 are distinct emulator-published mux states whose runtime activity, physical quantity, and circuit identity are untraced.
- `mechanism_behavior`: hardware-triggered special-coil timing is not exposed, and SP1/SP2 assignment conflicts.
- `polarity`: FLIP1516 publishes cabinet-button state where the manual prints physical EOS contacts; no bench capture reconciles rest/end-of-stroke state.
- `spatial_placement`: lamp coordinates are table candidates, flash groups lack socket surveys, and the conflicted outputs have no selected position.
- `unresolved_conflicts`: five source disagreements remain recorded in the definition and spatial report.

## Recreation boundary

Recreate only the explicitly mapped addresses and topologies. Do not invent activity, physical quantities, or feature names for public mux states 29-32. Also do not treat presentation helpers as extra hardware, convert the fixed target banks into drop targets, or infer physical switch/coil polarity from controller-normalized public state.
