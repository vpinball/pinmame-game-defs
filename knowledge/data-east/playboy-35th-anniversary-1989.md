# Data East Playboy 35th Anniversary (1989)

Machine definition: `machines/partial/data-east/playboy-35th-anniversary-1989.json`

## Identity and controller contract

Pinned PinMAME publishes one driver only: `play_a24`, from `CORE_GAMEDEF(play,a24,...)`. An exhaustive search found no `CORE_CLONEDEF` and no second catalog driver for the title. The single-driver record is deliberate, not an overlooked clone family.

`INITGAMES11(play, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, S11_MUXDELAY)` must be decoded against `core_tGameData`, not guessed from local argument names. It sets generation `GEN_DE` (`0x1000`), display layout `de_dispAlpha2`, `hw.flippers=FLIP1516`, zero switch/lamp/custom-solenoid offsets, `hw.soundBoard=SNDBRD_DE1S`, `hw.display=0`, `hw.gameSpecific1=S11_MUXDELAY`, and `sxx.muxSol=10`. The display layout supplies two seven-character alphanumeric and two seven-character numeric displays; all are controlled backbox devices with `not_applicable` playfield spatial records.

`S11_MUXDELAY` is bit `0x10`, documented as “delay mux solenoid by one IRQ.” In `pia0b_w`, Playboy retains the current PIA port-B byte and publishes the previous byte. `updsol` then uses solenoid 10/K1 to expose the common eight drivers as A-side public outputs 1-8 or C-side 25-32. This compensates for the ROM's relay timing so the decoded public states land in the correct bank. A VPX-style recreation consuming PinMAME outputs 1-8 and 25-32 must not add another delay or rebuild the raw mux. A raw PIA/board emulator must reproduce the one-IRQ latch; a physical recreation may still model K1 relay construction and sound.

Pinned `s11.c` types output 9 as a bulb, 11 as GI, 12-15 as bulbs, and 25-32 as eight muxed #89 bulbs under K1 at output 10. The manual instead fits physical coils at 25-30 and 32, with branch 31 unfitted. The core type is output/PWM metadata, not physical-fitment authority, so the disagreement stays a conflict.

## Address coverage

- Inputs enumerate service switches -7/-6, DIP/jumper 0, and matrix addresses 1-64.
- Outputs enumerate lamps 1-64 and System 11 public solenoids 1-50.
- Solenoid 23 is Game On; 24 is unused; 33-44 are inert; 45-48 are synthetic lower-flipper winding states; 49 is a simulation-only shooter state; 50 is reserved.
- Solenoid 10 is K1, which selects the C-bank block at public outputs 25-32.

The controller id is `pinmame.dataeast`, not `pinmame.system-11`: sharing PinMAME's `s11.c` implementation does not turn the physical Data East CPU/driver board into Williams System 11 hardware. The reviewed shared profile now supplies the platform address contract. The machine-level `inversion_applied_by_emulator` flag is true because consumers receive normalized public states and must not invert them again. Independently, `INITGAMES11` leaves Playboy's per-game `wpc.invSw` array all zeroes.

The manual prints physical flipper EOS contacts at matrix 15/16, but `FLIP1516` makes the non-fliptronic core overwrite those public addresses with left/right cabinet-button state. This is a PinMAME public-address behavior rather than a description of the physical EOS wiring. A recreation should use public 15/16 as cabinet-button state and must not infer physical EOS state from them.

## Lamp mapping and object accounting

The active table uses `SetLamp`: 16 active occurrences, with no `Lampz.MassAssign` and no `vpmMapLights`. Mapping claims therefore remain specific to this retained implementation.

Only 55 numeric `L*` Light objects exist for 64 addresses. The nine absent names are 26, 32, and 57-63. They are not missing outputs: `UpdateLamps` explicitly routes all nine to same-number Flasher objects, and the manual location drawing puts those exact addresses in a separate backbox/back-panel box. They therefore have controlled `not_applicable` playfield-spatial records. The drawing does not locate PINBALL-letter lamps 41, 49, 53-56, or 64 in either its backbox box or playfield plan. Their same-number table objects are presentation proxies flagged as backglass; those centers are withheld without turning the manual's silence into a false playfield claim.

Numeric Light objects 41, 49, 53, 54, 55, 56, and 64 are executable consumers but are flagged `is_backglass=true` in the retained table. The manual location drawing does not locate these PINBALL-letter lamps in either its backbox box or playfield plan. Their names prove consumption, not a physical socket plane, so their coordinates are withheld as unresolved placement evidence rather than classified as a source conflict. All remaining Light centers are only candidate placement evidence.

## Mechanism topology

Script causality plus manual construction establishes a serial three-ball trough and eject, outhole feeder, VUK, Champagne saucer, two-sensor Grotto path with kickout, three-face resetting drop bank, Laser Kick outlane kickback, two flippers, two slingshots, three pop bumpers, seven fixed PLAYBOY standups, three fixed center standups, manual shooter, and passive lanes/ramps/spinner. The fixed target banks are not drop banks: their drawings show independent leaf-switch stations and no reset coil.

The printed coil/flash location page adds a separate backbox inset to the playfield plan. It proves that outputs 3, 4, 8, 9, 12, 14 and 15 include backbox bulbs even though every retained VPX effect for those outputs sits in playfield space; output 12's four clear inset symbols already equal its complete schematic quantity. Three 5/6-like and two 13/16-like inset glyphs remain deliberately unassigned. The certain per-address minima are retained in the output notes. The diagram supports physical-plane classification and broad feature locations, but its grouped bubbles, unresolved small digits and lack of a registered coordinate frame do not support normalized socket centers.

The Laser Kick uses candidate Kicker001 geometry because `Kicker001_Hit` explicitly publishes switch 17. The off-bounds sw17 helper and unbound visible sw17a are excluded. Pinned `s11.c` PIA comments identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4; applying `setSSSol`'s Data East offsets `(3, 4, 5, 1, 0, 2)` derives printed SP1, SP3, SP4, SP6, SP5 and SP2 at public addresses 17-22. This is not inferred by treating printed SP numbers as handler indices. The manual, retained table geometry, and working script agree on the pop switches: Bumper2 is the center pop at switch 47 and Bumper3 is the right pop at switch 48; their SP1/SP2 coils are public outputs 17/22 respectively. Hidden Grotto transfer construction and special-solenoid pulse timing remain unresolved.

## Literal transcription and reconciliation

The 76-page manual has SHA-256 `0c4be366c30942919b7101c69acfb6563ac8bc6cd5aaaac0bad24ae5b9b1afa7` and a 76,678-character text layer. That layer was not trusted for multi-column tables: all decisive switch, lamp, coil and construction cells were read from 300/400 dpi renders. Excerpts preserve printed capitalization, abbreviations and typos such as `Ctr 3 Bank-Mid`, `DropTar. 50K`, `pinbAll`, `mansIon`, schematic `23-1200`, and chart `12-1200`. Normalized semantic labels appear only in the machine record, while disagreements remain in its reconciliation conflicts.

## Retained table and geometry

The table SHA-256 is `3b32aeacee1c5beb1c723e6e1bba79ae269deb36cc56101201b5d171a7a8336b`, contains 1,748 gameitems, and binds `Const cGameName = "play_a24"`. Its exact bounds are right 952 and bottom 1974. Both values are asserted before normalization, and no other machine's geometry is reused.

## Coverage and blockers

Status remains `partial`; `coverage.missing` is [`output_semantics`, `mechanism_behavior`, `polarity`, `spatial_placement`, `unresolved_conflicts`].

- `output_semantics`: callback group aliases/comments and core C-bank bulb typing disagree with printed physical functions.
- `mechanism_behavior`: hidden Grotto transfer geometry and hardware-triggered special-coil pulse behavior are absent.
- `polarity`: no original-machine trace reconciles cabinet button/EOS, K1 relay, and raw versus decoded output states.
- `spatial_placement`: table objects are presentation candidates, flash groups lack socket surveys, and seven routed PINBALL lamps are not located by the manual's drawing at all.
- `unresolved_conflicts`: ten source disagreements remain first-class.

## Recreation boundary

Consume PinMAME's decoded public mux outputs without adding another IRQ delay. Treat public 15/16 as flipper buttons rather than physical EOS contacts. Do not convert presentation proxies into extra hardware, infer socket locations from names, or erase the manual/core and manual/table disagreements.
