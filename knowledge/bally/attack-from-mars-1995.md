# Attack From Mars (Bally, 1995)

Coverage: **author_ready - manual-verified semantic I/O with full connector, wire-colour and driver-transistor wiring, mechanism inventory and behaviour, ball paths, normalized spatial placement for every playfield device, and pinned-harness runtime observation**

## Identity and evidence precedence

WPC-95 machine, IPDB 3781. The PinMAME family roots at `afm_113` with clones including `afm_113b` (1.13b, the common home-ROM revision), earlier `afm_03`/`afm_10`/`afm_11`, the Pinball FX and Ultrapin derivatives, and three FreeWPC community firmware revisions. The IPDB identity comes from the pinned OPDB snapshot and ROM crosswalk recorded in `reports/opdb-identity.json`; no model number is asserted.

Physical inventory authority is the **Bally/Midway Operators Handbook 16-10206**, retained in this repository's evidence roots at SHA-256 `5900c779f3bfb14251ada18d25a4dde84dd608b6ddd988ece8c92ea20fd0114b`: lamp matrix and lamp locations on printed pages 2-3, switch matrix and switch locations on 4-5, solenoid/flasher table and locations on 6-7, upper playfield parts on 8-9. Every table was read from rendered pages, not OCR, and transcribed into the retained review artifact.

Two further sources shaped the earlier partial revision of this note but are **not retained in this repository's evidence roots** and are therefore not authority for any promoted claim: a 176-page Bally/Midway operations manual scan (contributor-held; its page numbering 2-42 through 2-47 is cited in the sections below only to show where the contributor read a value) and a community altsound package used for the DCS opcode table. Where a claim rests only on one of those, it is prose reference material rather than a validated assertion in the definition.

Runtime authority is the pinned LibPinMAME harness recorded in `evidence/runtime/wpc-95/attack-from-mars-boot-attract-and-ball-start.json`. The earlier contributor switch/solenoid/lamp/sound-command logging on `afm_113b` under VPinMAME 3.6 retained no content-addressed traces, so claims backed only by that source remain candidate-grade prose here and were not promoted to validated assertions.

## Corrections to the legacy import

The legacy VPE-derived definition carried several verifiable errors, all corrected against the manual tables:

- **Solenoid 19 is 'Right Side High (2)'**, the two-bulb right-side flasher circuit (J133-6/J134-5, transistor Q27, #906 bulbs). The legacy 'ROM Started'/`c_game_on` label is wrong for this machine; the definition's open conflict on item 19 is resolved by the manual and the g5k script, which drives 19 as an ordinary flasher.
- **Solenoids 11/12/13 are Left Jet / Bottom Jet / Right Jet** (all A-9415-2). The legacy import duplicated 'Right Slingshot' onto 11 and shifted the jets up by one, losing the Right Jet entirely.
- **Lamp rows 6-8 (61-88) were largely Medieval Madness names** ('Castle Lock', 'Howard Hurtz', 'Sir Psycho', 'Duke of Bourbon', etc.). The manual matrix gives the true AFM names: 61/62/68/76/77/78 are the remaining MARTIAN letter-target lamps, 63-65 Atomic Blaster 1-3, 66/74 Right/Left Loop Jackpot, 67 Extra Ball, 71-73 Capture 1-3, 75 Left Loop Arrow, 81 Shoot Again, 82-85 outlane/return lamps, 86 Launch Button, 87 not used, 88 Start Button.
- **Solenoids 25-28 are flasher circuits** ('Left Ramp Left (2)', 'Left Ramp Right (2)', 'Left Side High (2)', 'Left Side Low'; general-purpose drives into #906/#89 flashlamps), not coils.
- **Output 24 'Motor Bank' is the bank motor** (part 14-8023) on a flasher-class drive circuit, not a flasher.
- Switch label fixes: 14 'Plumb Bob Tilt', 16 'Left Outlane', 71/72 'Right Loop High'/'Right Loop Low' (legacy said 'Right Bank').
- **Solenoid 43 is PinMAME's mirror of LPDC output 39, not a separate circuit.** `core_getSol` duplicates the WPC-95 LPDC outputs 37-40 at public addresses 41-44, so 43 reports the same physical output as 39 (Strobe Light). That is why 43 is absent from the manual table and why the contributor's runtime logging saw it toggle. The known-working script binds `SolModCallback(39)` and `SolModCallback(43)` to two different visual lamps, which is a table convenience rather than two physical circuits. The definition records 43 as a virtual duplicate of 39.

## Addresses that duplicate an already-declared circuit

Attack From Mars publishes the same physical outputs on more than one PinMAME address, so a recreation must bind each device once and accept either address:

- Public solenoid 43 mirrors LPDC output 39 (WPC-95 duplicates 37-40 at 41-44). Output 39 is the printed **Strobe Light**, assembly A-20718 on J110-4, cabled through H-20705 - not a second saucer-dome circuit. The retained JPSalas script settles it by binding the strobe on the mirror address with `SolCallback(43) = "SetLamp 130,"` where lamp 130 is the table's `Strobe` object, so a recreation must accept the strobe on either 39 or 43. Outputs 37 and 38 are mirrored the same way at 41 and 42.
- `afmGameData` declares `custSol=3`, so PinMAME also publishes game-specific solenoids 51-53. `afm_getSol` returns WPC_FLIPPERCOIL95 bit 0x20 for 51, bit 0x10 for 52, and bits 0xc0 for 53 - the same bits `core_getSol` reports on public solenoids 34, 33, and 35/36 respectively.
- The two ball-gate addresses carry a naming disagreement, now resolved. Every physical source agrees that public solenoid 33 is the **right** gate and 34 the **left**: the printed solenoid/flasher table (33 RIGHT GATE High Power Q84 J120-6, 34 LEFT GATE Low Power Q86 J120-4), the upper-playfield parts list (actuator coil A-17796 with A-17797-2 Right Ball Gate on item 24 and A-17797-1 Left Ball Gate on item 25), and both retained known-working scripts. Pinned PinMAME disagrees and is also internally inconsistent: `wpc.c` writes `WPC_FLIPPERCOIL95` bits 4-7 to public solenoids 33-36, so bit 0x10 is public 33 and bit 0x20 is public 34, yet `afm.c` reads bit 0x10 for `sLGate` and bit 0x20 for `sRGate` while its own comments annotate `sRGate` as `/* 33 */` and `sLGate` as `/* 34 */`. The manual owns physical identity and the known-working script owns runtime binding, so both entries are `validated` on that basis, the emulator defect is recorded in the device notes, and no conflict record is carried because the disagreement is between sources of unequal authority rather than unresolved.
- `afmGameData` also declares `lampCol=2`, so PinMAME exposes two auxiliary lamp columns above the standard 8x8 matrix for the 16-LED saucer board. They are now enumerated: the sixteen L.E.D.s appear at public lamp addresses **91-98 and 101-108**. `afm_wpc_w` shifts a sixteen-bit word into `tmpLampMatrix[8]` and `[9]` using `WPC_SOLENOID1` bit 4 as the clock and bit 5 as the data, and `wpc.c` documents that register's bits 4-7 as the J122/J123/J124 GPIO that "appear as LPDC outputs 37..40 in manuals", so the clock is public solenoid 37 and the data public solenoid 38 - exactly the printed L.E.D. Clock and L.E.D. Data entries on saucer board A-20670. The pinned harness confirmed it: in attract mode exactly eight of the sixteen addresses are lit at a time and the set rotates through four phases that between them cover all sixteen, while solenoids 37, 38 and their LPDC mirrors 41 and 42 are active; at ball start the ring and all four solenoids go quiet together.

## Displays

One dot-matrix display, 128x32, WPC-95 standard. No segment or alphanumeric displays.

## Custom mechanisms

- **UFO saucer with subway return.** Every saucer entry closes switch 78 'Center Trough' - attack-wave hits and the final destruction alike. The ball exits through a subway to the left popper (switch 36) and is ejected up a vertical tube by solenoid 3. The saucer-shake motor (solenoid 15) wobbles the UFO in short pulse bursts on hits; the destruction sequence runs roughly 5-7 pulses about 0.25 s apart, and the ROM raises the 3-bank wall at roughly pulse 5 - before the burst ends - so a recreation ejecting the left popper during this window must mind the moving bank geometry.
- **Three-target motor bank.** Standups 45-47 ride a motorized wall (output 24) between limit switches 66 (down) and 67 (up).
- **Pop-up aliens.** Four alien mech assemblies cover the seven MARTIAN standups, one per target group, each an A-20579 (item 15 is printed A-20479-2, see below) with figurine 23-6768 on its own support bracket. Reading the printed switch names letter by letter, MARTIAN is spelt 56 "M", 57 M"A", 58 MA"R", 43 MAR"T", 44 MART"I", 41 MARTI"A", 42 MARTIA"N". Solenoid 5 (Left Alien Low) covers the left bank M-A-R on switches 56-58, solenoid 6 (Left Alien High) covers the T on switch 43, solenoid 8 (Right Alien High) covers the I on switch 44, and solenoid 14 (Right Alien Low) covers the right bank A-N on switches 41-42. The retained table corroborates the grouping geometrically: alien primitives sit at (0.137, 0.535), (0.369, 0.271), (0.622, 0.270) and (0.826, 0.541), each beside its target group, and each group's lamp inserts sit directly below its targets.
- **Right popper scoop (Stroke of Luck)**: capture switch 37, eject solenoid 4.
- **Single center drop target**: switch 77, reset solenoid 16.
- **Loop gates** (33 right, high power; 34 left, low power) and the **center-ramp diverter** on a power/hold pair (35/36), opened when a lock is lit.
- **Strobe light**: backpanel strobe tube (output 39) plus a 16-LED chase chain clocked serially via outputs 37 'L.E.D. Clock' and 38 'L.E.D. Data'; featured in Strobe Multiball.
- Standard complement: two flippers (outputs 29-32), two slingshots (9/10, switches 51/52), three jet bumpers (11-13, switches 53-55), four-ball trough (switches 31-35, eject solenoid 2, auto plunger solenoid 1), knocker (7).

## Ball-state transitions

All observed on `afm_113b`:

- **Serve:** trough eject (solenoid 2) to shooter lane (switch 18), then player plunge or auto plunger (solenoid 1).
- **Lock / saucer capture:** lock shots and saucer balls end at switch 78, transit the subway, and land in the left popper (switch 36). For locks 1 and 2 the ROM keeps the ball in the popper and serves a replacement from the trough; lock 3 releases for multiball. Popper eject is solenoid 3.
- **Ball saver:** indicated by **lamp 15 'Return To Battle (2)' flashing** - not lamp 81, which is the extra-ball 'Shoot Again' indicator. The saver re-serve fires within roughly 100 ms of the drain.
- **End of ball:** with a trivial bonus count the next player's serve can follow the drain in as little as 1.6 s. Recreation logic that distinguishes ball-saver serves from next-player serves purely by timing will misclassify (measured failure at a 2 s threshold).
- **Stroke of Luck:** switch 37 capture, award, solenoid 4 eject.

## Lamp semantics

Behavioral notes beyond the matrix names, observed at runtime:

| Lamp | Name | Behavior |
|---|---|---|
| 13 | Martian Attack Multi-ball | trophy - permanently lit once attained this game; not a mode-active indicator |
| 14 | Annihilation | trophy - same semantics as 13 |
| 15 | Return To Battle (2) | the ball-saver indicator; flashes during the saver window |
| 36 | Martian Attack | flashing = available; off on the qualifying scoop hit and while the mode runs |
| 37 | Rule Universe | flashing = available; off on scoop hit |
| 38 | Stroke Of Luck | flashing = available; off on scoop hit |
| 54 / 55 / 26 / 27 | Light Lock / Lock 1 / Lock 2 / Lock 3 | 54 flashing = lock can be lit, 54 solid = lock lit (diverter opens); 55/26/27 track lock positions, flashing = ready to accept |
| 67 | Extra Ball | flashing = available at the scoop |
| 81 | Shoot Again | lit = extra ball in play; not the ball-saver lamp |

Availability indicators blink in roughly 200-300 ms phases; solid versus flashing distinguishes owned versus offered throughout the rule set.

## General illumination

Five GI strings per the manual solenoid/flasher table: 01 Bottom Playfield, 02 Middle Playfield, 03 Top Playfield (#44/#555 bulbs, dimmable) plus 04 Top Insert and 05 Bottom Insert (#555 bulbs; these two strings do not brighten or dim - they are always on). All five strings are modelled as machine outputs on `pinmame.output.gi` addresses 0-4. Strings 01-03 carry playfield placements taken from the retained table's `aGiLLights`, `aGiMLights` and `aGiTLights` arrays, deduplicated from 50 light objects to 29 physical sockets because the table pairs every bulb with a co-located halo. The manual publishes no per-string bulb count, so the quantity comes from those arrays and is not presented as a printed figure. Strings 04 and 05 are backbox insert-panel circuits and take a controlled `cabinet_or_service` spatial record with no asserted count. String 01 is the one string that spans both: the printed table gives it a playfield harness on J105-1/J105-7 with #44 bulbs and a separate backbox harness on J106-1/J106-7 with #555 bulbs, and only the playfield sockets are placed.

## Dedicated and flipper switches

The manual's dedicated grounded switches include the four coin chutes (D1-D4), service credits/volume/begin-test controls (D5-D8), and the Fliptronic flipper block: F1 Lower Right Flipper EOS, F2 Lower Right Flipper cabinet button (opto), F3 Lower Left Flipper EOS, F4 Lower Left Flipper cabinet button (opto), F5-F8 not used (no upper flippers on this game). The manual's F-numbers map onto the emulator's dedicated switch addresses in order, F1 through F8 to public 111 through 118, which the definition now records with a `manual.address` alias on each. F1-F4 are used; F5-F8 print `---` and "Not Used" in both the switch matrix and the switch-locations parts list, and the switch-locations playfield map draws F6 and F8 floating outside the playfield outline with no leader line, so public switches 115-118 are marked unused. Note that `afmGameData` still declares `FLIP_SW(FLIP_L|FLIP_U)`; that is emulator scaffolding for the generation and is not evidence of upper flippers on this machine. The matching upper Fliptronic *outputs* are genuinely in use - they drive the two loop gates and the ramp diverter.

## Timing and tuning observations

- Saucer destruction: solenoid-15 shake burst of ~5-7 pulses at ~0.25 s spacing; the 3-bank rises at roughly pulse 5, before the burst ends.
- The ROM re-asserts the current background-music command about twice per second (relevant for alt-sound implementations).
- Ball-saver re-serve within ~100 ms of drain; next-player serve possible within ~1.6 s of drain.

## Controller interactions - DCS sound commands

Commands to the DCS sound board arrive as 16-bit big-endian pairs in the PinMAME sound-command stream. Protocol notes, runtime-verified on `afm_113b`:

- Parse against the known-id list below; naive byte splitting desynchronizes on the `0x03D2`/`0x03D3` heartbeat pair.
- The current background-music command is re-asserted roughly twice per second during play.
- Rows marked *(loop)* are looping music tracks; everything else is one-shot.
- Many voice/SFX commands exist as even/odd duplicate-id pairs; both trigger the same sample.

Selected stable mappings, each observed dozens of times: `0x01A5` ball saved ('Return to battle!'), `0x0128`/`0x0129` skill-shot award (held-flipper super skill shot and top-lane skill shot both fire these), `0x0346`/`0x0347` saucer destroyed (wave completion), `0x0122`/`0x0123` extra ball awarded, `0x000F` game-over music.

### Opcode reference (586 ids)

Sample names are from the contributor-held community altsound package for `afm_113b`, which is not retained in this repository's evidence roots, (`altsound.afm-113b.community-package`, SHA-256 `bc139099b58ed94240d86f4fcc8e06ba37dafa5a14d9d5417917b5f225eac830`); annotations are contributor runtime observations. Note: the package itself writes `0x006A` on two rows (`martian_target_mid` and `martian_target_mid2`, both mapping `0x006a-laser_shot.ogg`) and has no `0x006B` row; the table below lists the second row as `0x006B` as a contributor-inferred correction per the even/odd pairing convention, flagged in its annotation.

| Opcode | Sample name (altsound transcription) | Runtime annotation | Group |
|---|---|---|---|
| 0x0001 | pre_launch *(loop)* | pre-launch music (ball in shooter lane) | Music (looping background tracks) |
| 0x0002 | mus_defaultmusic *(loop)* | default/main-play music (re-asserted ~2x/s during play) | Music (looping background tracks) |
| 0x0003 | main_play *(loop)* | main-play music group (interchangeable with 0x0002) | Music (looping background tracks) |
| 0x0004 | mus_attackwave *(loop)* | attack-wave music | Music (looping background tracks) |
| 0x0005 | mus_hurryup *(loop)* | hurry-up music | Music (looping background tracks) |
| 0x0006 | main_theme *(loop)* |  | Music (looping background tracks) |
| 0x0007 | main_theme *(loop)* |  | Music (looping background tracks) |
| 0x0008 | mus_totalannihilation *(loop)* | multiball music | Music (looping background tracks) |
| 0x0009 | martian_attack *(loop)* | Martian Attack music intro (number-paired with 0x000A loop: intro N hands over to loop N) | Music (looping background tracks) |
| 0x000A | martian_attack *(loop)* | Martian Attack music loop (pair of 0x0009) | Music (looping background tracks) |
| 0x000B | multiball *(loop)* |  | Music (looping background tracks) |
| 0x000C | strobe_multiball *(loop)* |  | Music (looping background tracks) |
| 0x000D | waiting *(loop)* |  | Music (looping background tracks) |
| 0x000E | mus_stroke_of_luck *(loop)* |  | Music (looping background tracks) |
| 0x000F | freaky *(loop)* | game-over music — reliable end-of-game signal | Music (looping background tracks) |
| 0x0010 | mus_martian_multiball *(loop)* |  | Music (looping background tracks) |
| 0x0011 | never_heard_this *(loop)* |  | Music (looping background tracks) |
| 0x0012 | attack_mars *(loop)* |  | Music (looping background tracks) |
| 0x0013 | bip |  | SFX & speech (general) |
| 0x0014 | big_drums *(loop)* |  | Music (looping background tracks) |
| 0x0050 | music_regular *(loop)* |  | Music (looping background tracks) |
| 0x0051 | music_regular_2 *(loop)* |  | Music (looping background tracks) |
| 0x0052 | rulethuniverse music |  | SFX & speech (general) |
| 0x0055 | (unnamed) |  | SFX & speech (general) |
| 0x0064 | martian_voc_martiangrowling |  | Martians: voices, taunts, Martian Attack |
| 0x0065 | martian_voc_martiangrowling2 |  | Martians: voices, taunts, Martian Attack |
| 0x0068 | martianattack_voc_martiangrowling |  | Martians: voices, taunts, Martian Attack |
| 0x0069 | martianattack_voc_martiangrowling2 |  | Martians: voices, taunts, Martian Attack |
| 0x006A | martian_target_mid |  | Martians: voices, taunts, Martian Attack |
| 0x006B | martian_target_mid2 | contributor-inferred id: the package writes 0x006A on both rows | Martians: voices, taunts, Martian Attack |
| 0x006C | martian_target_high |  | Martians: voices, taunts, Martian Attack |
| 0x006D | martian_target_high_2 |  | Martians: voices, taunts, Martian Attack |
| 0x006E | martian_target_low |  | Martians: voices, taunts, Martian Attack |
| 0x006F | martian_target_low_2 |  | Martians: voices, taunts, Martian Attack |
| 0x0070 | plunger_ball_launch |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0071 | plunger_ball_launch_2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0072 | short_gun_detonation |  | SFX & speech (general) |
| 0x0073 | sameas-000114-short_gun_detonation |  | SFX & speech (general) |
| 0x0074 | medium_bomb |  | SFX & speech (general) |
| 0x0075 | sameas-000116-medium_bomb |  | SFX & speech (general) |
| 0x0076 | toplane_enter |  | SFX & speech (general) |
| 0x0077 | toplane_enter_2 |  | SFX & speech (general) |
| 0x0078 | totalannihilation_exitorbit |  | SFX & speech (general) |
| 0x0079 | totalannihilation_exitorbit2 |  | SFX & speech (general) |
| 0x007A | rightorbit_enter_lowerswitchhit |  | SFX & speech (general) |
| 0x007B | rightorbit_enter_lowerswitchhit2 |  | SFX & speech (general) |
| 0x007C | toplane_entering |  | SFX & speech (general) |
| 0x007D | toplane_entering2 |  | SFX & speech (general) |
| 0x007E | tractorbeam_pullinghouseup |  | SFX & speech (general) |
| 0x007F | tractorbeam_pullinghouseup2 |  | SFX & speech (general) |
| 0x0080 | slingshot |  | SFX & speech (general) |
| 0x0081 | slingshot2 |  | SFX & speech (general) |
| 0x0082 | tractorbeam_enterramp_beamfiring |  | SFX & speech (general) |
| 0x0083 | tractorbeam_enterramp_beamfiring2 |  | SFX & speech (general) |
| 0x0084 | saucershield_canthitduringmultiball |  | Locks, multiball, jackpots, extra ball |
| 0x0085 | saucershield_canthitduringmultiball2 |  | Locks, multiball, jackpots, extra ball |
| 0x0088 | big_o_beam |  | SFX & speech (general) |
| 0x0089 | sameas-000136-big_o_beam |  | SFX & speech (general) |
| 0x008A | marsian_are_coming |  | SFX & speech (general) |
| 0x008B | sameas-000138-marsian_are_coming |  | SFX & speech (general) |
| 0x008C | bomb_delay_effect |  | SFX & speech (general) |
| 0x008D | sameas-000140-bomb_delay_effect |  | SFX & speech (general) |
| 0x008E | lock_lockislit_fanfare | Stroke-of-Luck award reveal (19-variant pool) | Locks, multiball, jackpots, extra ball |
| 0x008F | lock_lockislit_fanfare2 | Stroke-of-Luck award reveal (dup) | Locks, multiball, jackpots, extra ball |
| 0x0090 | lock3_missilelaunched |  | Locks, multiball, jackpots, extra ball |
| 0x0091 | lock3_missilelaunched2 |  | Locks, multiball, jackpots, extra ball |
| 0x0092 | lock3_saucerhitbymissile |  | Locks, multiball, jackpots, extra ball |
| 0x0093 | lock3_saucerhitbymissile2 |  | Locks, multiball, jackpots, extra ball |
| 0x0094 | lock_balllocked_fanfare | ball locked jingle (lock 1/2) | Locks, multiball, jackpots, extra ball |
| 0x0095 | lock_balllocked_fanfare2 | ball locked jingle (duplicate id, rarely seen) | Locks, multiball, jackpots, extra ball |
| 0x0098 | lock3_jetsound | lock 3 / multiball start transition (music stops) | Locks, multiball, jackpots, extra ball |
| 0x0099 | lock3_jetsound2 | lock 3 (duplicate id) | Locks, multiball, jackpots, extra ball |
| 0x009A | inlanes_complete_strokeofluck_lit |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x009B | inlanes_complete_strokeofluck_lit2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x009C | bumper |  | SFX & speech (general) |
| 0x009D | bumper_2 |  | SFX & speech (general) |
| 0x009E | outlane_ball_lost |  | SFX & speech (general) |
| 0x009F | outlane_ball_lost_2 |  | SFX & speech (general) |
| 0x00A0 | impact_on_the_ground |  | SFX & speech (general) |
| 0x00A1 | sameas-000160-impact_on_the_ground |  | SFX & speech (general) |
| 0x00A2 | saucer_shield_impact |  | Saucer / attack waves |
| 0x00A3 | saucer_shield_impact2 |  | Saucer / attack waves |
| 0x00A4 | multiball_rampshot_artilleryshots |  | Locks, multiball, jackpots, extra ball |
| 0x00A5 | multiball_rampshot_artilleryshots2 |  | Locks, multiball, jackpots, extra ball |
| 0x00AE | marsian_upset |  | SFX & speech (general) |
| 0x00AF | sameas-000174-marsian_upset |  | SFX & speech (general) |
| 0x00B2 | marsian_unhappy |  | SFX & speech (general) |
| 0x00B3 | sameas-000178-marsian_unhappy |  | SFX & speech (general) |
| 0x00B4 | marsian_trying_to_be_scary |  | SFX & speech (general) |
| 0x00B5 | sameas-000180-marsian_trying_to_be_scary |  | SFX & speech (general) |
| 0x00B8 | atomicblaster_2ndpartinstalled |  | SFX & speech (general) |
| 0x00B9 | atomicblaster_2ndpartinstalled2 |  | SFX & speech (general) |
| 0x00BA | lock1_tanksrolling | lock-related callout | Locks, multiball, jackpots, extra ball |
| 0x00BB | lock1_tanksrolling2 | lock-related callout (dup) | Locks, multiball, jackpots, extra ball |
| 0x00C0 | tractorbeam_beamingup |  | SFX & speech (general) |
| 0x00C1 | tractorbeam_beamingup2 |  | SFX & speech (general) |
| 0x00C4 | lock2_missilesraising |  | Locks, multiball, jackpots, extra ball |
| 0x00C5 | lock2_missilesraising2 |  | Locks, multiball, jackpots, extra ball |
| 0x00C8 | orbit_ramp_2waycombo |  | SFX & speech (general) |
| 0x00C9 | orbit_ramp_2waycombo2 |  | SFX & speech (general) |
| 0x00CC | inlane |  | SFX & speech (general) |
| 0x00CD | inlane_2 |  | SFX & speech (general) |
| 0x00D0 | videomode_basedestroyed |  | Saucer / attack waves |
| 0x00D1 | videomode_basedestroyed2 |  | Saucer / attack waves |
| 0x00D2 | totalannihilation_award_beamexplosion |  | Saucer / attack waves |
| 0x00D3 | totalannihilation_award_beamexplosion2 |  | Saucer / attack waves |
| 0x00D4 | funny_sound |  | SFX & speech (general) |
| 0x00D5 | sameas-000212-funny_sound |  | SFX & speech (general) |
| 0x00D6 | superjets_shoot |  | SFX & speech (general) |
| 0x00D7 | superjets_shoot2 |  | SFX & speech (general) |
| 0x00E4 | marsian_talking_to_us |  | SFX & speech (general) |
| 0x00E5 | sameas-000228-marsian_talking_to_us |  | SFX & speech (general) |
| 0x00E6 | bigobeam_cow |  | SFX & speech (general) |
| 0x00E7 | bigobeam_cow2 |  | SFX & speech (general) |
| 0x00E8 | hurryup_award_received |  | Saucer / attack waves |
| 0x00E9 | hurryup_award_received2 |  | Saucer / attack waves |
| 0x00EA | martian_attacklit_stab |  | Martians: voices, taunts, Martian Attack |
| 0x00EB | martian_attacklit_stab2 |  | Martians: voices, taunts, Martian Attack |
| 0x00EC | extraball_lit_fanfare |  | SFX & speech (general) |
| 0x00ED | extraball_lit_fanfare2 |  | SFX & speech (general) |
| 0x00F0 | opening_doors |  | SFX & speech (general) |
| 0x00F1 | sameas-000240-opening_doors |  | SFX & speech (general) |
| 0x00F2 | videomode_saucersound |  | Saucer / attack waves |
| 0x00F3 | videomode_saucersound2 |  | Saucer / attack waves |
| 0x00F4 | marsian_are_going_away |  | SFX & speech (general) |
| 0x00F5 | sameas-000244-marsian_are_going_away |  | SFX & speech (general) |
| 0x00F6 | leftramp_enter_shot |  | SFX & speech (general) |
| 0x00F7 | leftramp_enter_shot2 |  | SFX & speech (general) |
| 0x00FC | bigobeam_duck_high |  | SFX & speech (general) |
| 0x00FD | bigobeam_duck_high2 |  | SFX & speech (general) |
| 0x00FE | bigobeam_duck_mid |  | SFX & speech (general) |
| 0x00FF | bigobeam_duck_mid2 |  | SFX & speech (general) |
| 0x0100 | bigobeam_duck_low |  | SFX & speech (general) |
| 0x0101 | bigobeam_duck_low2 |  | SFX & speech (general) |
| 0x0102 | multiball_rampshot_missilesfizzing |  | Locks, multiball, jackpots, extra ball |
| 0x0103 | multiball_rampshot_missilesfizzing2 |  | Locks, multiball, jackpots, extra ball |
| 0x0104 | multiball_rampshot_missileexplosion |  | Locks, multiball, jackpots, extra ball |
| 0x0105 | multiball_rampshot_missileexplosion2 |  | Locks, multiball, jackpots, extra ball |
| 0x010C | bigobeam_voc_chicken_high |  | SFX & speech (general) |
| 0x010D | bigobeam_voc_chicken_high2 |  | SFX & speech (general) |
| 0x010E | bigobeam_voc_chicken_mid |  | SFX & speech (general) |
| 0x010F | bigobeam_voc_chicken_mid2 |  | SFX & speech (general) |
| 0x0110 | bigobeam_voc_chicken_low |  | SFX & speech (general) |
| 0x0111 | bigobeam_voc_chicken_low2 |  | SFX & speech (general) |
| 0x0112 | rightorbit_atomicblaster_upperswitch |  | SFX & speech (general) |
| 0x0113 | rightorbit_atomicblaster_upperswitch2 |  | SFX & speech (general) |
| 0x0114 | video_mode_options_shoot |  | SFX & speech (general) |
| 0x0115 | video_mode_options_shoot2 |  | SFX & speech (general) |
| 0x0116 | martianattack_hitmartian |  | Martians: voices, taunts, Martian Attack |
| 0x0117 | martianattack_hitmartian2 |  | Martians: voices, taunts, Martian Attack |
| 0x0118 | ramp_bigobeam_firing |  | SFX & speech (general) |
| 0x0119 | ramp_bigobeam_firing2 |  | SFX & speech (general) |
| 0x011C | leftorbit_shot |  | SFX & speech (general) |
| 0x011D | leftorbit_shot2 |  | SFX & speech (general) |
| 0x011E | unlocking_door |  | Locks, multiball, jackpots, extra ball |
| 0x011F | sameas-000286-unlocking_door |  | Locks, multiball, jackpots, extra ball |
| 0x0120 | enterinitial_confirmletter |  | SFX & speech (general) |
| 0x0121 | enterinitial_confirmletter2 |  | SFX & speech (general) |
| 0x0122 | extraball_fanfare | EXTRA BALL awarded (jingle; music stops until scoop eject) | Locks, multiball, jackpots, extra ball |
| 0x0123 | extraball_fanfare2 | extra ball awarded (duplicate id, rarely seen) | Locks, multiball, jackpots, extra ball |
| 0x0124 | bigobeam_spider |  | SFX & speech (general) |
| 0x0125 | bigobeam_spider2 |  | SFX & speech (general) |
| 0x0126 | atomicblaster_exitorbit_shotsound |  | SFX & speech (general) |
| 0x0127 | atomicblaster_exitorbit_shotsound2 |  | SFX & speech (general) |
| 0x0128 | top_lane_skillshot | skill shot award — fires for BOTH the super skill shot and the top-lane skill shot | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0129 | top_lane_skillshot2 | skill shot award (duplicate id) | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x012A | tractorbeam_saucerdoorclosing |  | Saucer / attack waves |
| 0x012B | tractorbeam_saucerdoorclosing2 |  | Saucer / attack waves |
| 0x012C | balllost_bonuscalc |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x012D | balllost_bonuscalc2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x012E | balllost_bonus_counting_low |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x012F | balllost_bonus_counting_low2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0130 | balllost_bonus_counting_mid |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0131 | balllost_bonus_counting_mid2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0132 | balllost_bonus_counting_high |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0133 | balllost_bonus_counting_high2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0134 | balllost_bonus_counting_higher |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0135 | balllost_bonus_counting_higher2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0136 | balllost_bonus_counting_highest |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0137 | balllost_bonus_counting_highest2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0138 | extraball_martianhitbyball |  | Martians: voices, taunts, Martian Attack |
| 0x0139 | extraball_martianhitbyball2 |  | Martians: voices, taunts, Martian Attack |
| 0x013A | martian_all_letters_hit |  | Martians: voices, taunts, Martian Attack |
| 0x013B | martian_all_letters_hit2 |  | Martians: voices, taunts, Martian Attack |
| 0x013C | strokeofluck_options_saucer_appearing |  | Saucer / attack waves |
| 0x013D | strokeofluck_options_saucer_appearing_2 |  | Saucer / attack waves |
| 0x013E | videomode_saucerexplosion |  | Saucer / attack waves |
| 0x013F | videomode_saucerexplosion2 |  | Saucer / attack waves |
| 0x0142 | superjets_activated_explosion |  | Saucer / attack waves |
| 0x0143 | superjets_activated_explosion2 |  | Saucer / attack waves |
| 0x0146 | bigobeam_lobster_clicking |  | SFX & speech (general) |
| 0x0147 | bigobeam_lobster_clicking2 |  | SFX & speech (general) |
| 0x0148 | extraball_fanfare_secondpart |  | SFX & speech (general) |
| 0x0149 | extraball_fanfare_secondpart2 |  | SFX & speech (general) |
| 0x014A | bigobeam_fly |  | SFX & speech (general) |
| 0x014B | bigobeam_fly2 |  | SFX & speech (general) |
| 0x014E | strokeofluck_selectedoption |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x014F | strokeofluck_selectedoption2 |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0150 | sonar_ping |  | SFX & speech (general) |
| 0x0151 | sonar_ping2 |  | SFX & speech (general) |
| 0x0152 | half_coin_in |  | Attract, coins, match, tilt, service |
| 0x0153 | half_coin_in_2 |  | Attract, coins, match, tilt, service |
| 0x0154 | tilt | tilt | Attract, coins, match, tilt, service |
| 0x0155 | sameas-000340-tilt | tilt (dup) | Attract, coins, match, tilt, service |
| 0x0156 | crowds_clapping |  | SFX & speech (general) |
| 0x0157 | sameas-000342-crowds_clapping |  | SFX & speech (general) |
| 0x0158 | orbit_fleeingbonus_saucer |  | Saucer / attack waves |
| 0x0159 | orbit_fleeingbonus_saucer2 |  | Saucer / attack waves |
| 0x015A | ramp_fleeingbonus_groundmartians |  | Martians: voices, taunts, Martian Attack |
| 0x015B | ramp_fleeingbonus_groundmartians2 |  | Martians: voices, taunts, Martian Attack |
| 0x015C | coin_in_game_ready_to_start |  | Attract, coins, match, tilt, service |
| 0x015D | coin_in_game_ready_to_start_2 |  | Attract, coins, match, tilt, service |
| 0x015E | tilt_warning | tilt warning | Attract, coins, match, tilt, service |
| 0x015F | sameas-000350-tilt_warning | tilt warning (dup) | Attract, coins, match, tilt, service |
| 0x0160 | bouing |  | SFX & speech (general) |
| 0x0161 | sameas-000352-bouing |  | SFX & speech (general) |
| 0x0162 | matchsequence_saucersound |  | Saucer / attack waves |
| 0x0163 | matchsequence_saucersound2 |  | Saucer / attack waves |
| 0x0164 | start_of_attack_mars *(loop)* | Martian Multiball start (empty looping row = silences music) | Music (looping background tracks) |
| 0x0165 | sameas-000356-start_of_attack_mars *(loop)* | Martian Multiball start (dup) | Music (looping background tracks) |
| 0x0166 | replay_saucerlaunchingsound |  | Saucer / attack waves |
| 0x0167 | replay_saucerlaunchingsound2 |  | Saucer / attack waves |
| 0x0168 | no_coins_insert_coins |  | Attract, coins, match, tilt, service |
| 0x0169 | no_coins_insert_coins |  | Attract, coins, match, tilt, service |
| 0x0176 | rafle_shot |  | SFX & speech (general) |
| 0x0177 | sameas-000374-rafle_shot |  | SFX & speech (general) |
| 0x0178 | appluase_when_defeating_mars |  | SFX & speech (general) |
| 0x0179 | sameas-000376-appluase_when_defeating_mars |  | SFX & speech (general) |
| 0x017A | ruletheuniverse_success_cheering |  | SFX & speech (general) |
| 0x017B | ruletheuniverse_success_cheering2 |  | SFX & speech (general) |
| 0x017C | ruletheuniverse_success_cheering_short |  | SFX & speech (general) |
| 0x017D | ruletheuniverse_success_cheering_short2 |  | SFX & speech (general) |
| 0x017E | applause_when_ruling_universe |  | SFX & speech (general) |
| 0x017F | sameas-000382-applause_when_ruling_universe |  | SFX & speech (general) |
| 0x0180 | bouing |  | SFX & speech (general) |
| 0x0181 | sameas-000384-bouing |  | SFX & speech (general) |
| 0x0186 | boumboumboum | Rule-the-Universe completion ("you rule the universe") | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0192 | bigobeam_hurryup_voc_watch_out_man_they_ve_got_a_big_o_beam |  | Saucer / attack waves |
| 0x0193 | atomicblaster_hurryup_voc_use_the_atomic_blaster_now |  | Saucer / attack waves |
| 0x0194 | the_fate_of_the_world_is_in_your_hands |  | SFX & speech (general) |
| 0x0196 | lock1_voc_get_every_available_man |  | Locks, multiball, jackpots, extra ball |
| 0x0197 | lock2_voc_get_the_troops_ready |  | Locks, multiball, jackpots, extra ball |
| 0x019B | i_hate_martians | Martian Attack end | Martians: voices, taunts, Martian Attack |
| 0x019C | martianattack_voc_look_out_martians |  | Martians: voices, taunts, Martian Attack |
| 0x019D | martianmultiball_voc_look_out_more_martians |  | Martians: voices, taunts, Martian Attack |
| 0x019E | lock2_voc_missile_locked_on_target |  | Locks, multiball, jackpots, extra ball |
| 0x019F | lock2_voc_missiles_on_standby |  | Locks, multiball, jackpots, extra ball |
| 0x01A0 | totalannihilation_voc_take_that_muffin_head |  | SFX & speech (general) |
| 0x01A1 | totalannihilation_voc_take_that_ripple_head |  | SFX & speech (general) |
| 0x01A5 | ballsave_voc_return_to_battle_soldier | BALL SAVED — the ball-saver callout; fires only on a genuine save | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x01A6 | don_t_shoot_until_you_seem_them_jump |  | SFX & speech (general) |
| 0x01A7 | somebody_shoot_one_of_those_things |  | SFX & speech (general) |
| 0x01A8 | stop_them |  | SFX & speech (general) |
| 0x01A9 | totalannihilation_voc_start_total_annihilation_uh_uh |  | SFX & speech (general) |
| 0x01AB | hurryup_award_voc_excellent |  | Saucer / attack waves |
| 0x01AE | hurryup_award_voc_great_shot |  | Saucer / attack waves |
| 0x01B1 | hurryup_award_voc_well_done_soldier |  | Saucer / attack waves |
| 0x01B2 | hurryup_award_voc_wohoo |  | Saucer / attack waves |
| 0x01B3 | martianmultiball_voc_oh_darn_you_re_some_ugly_martians | Martian Attack end variant | Martians: voices, taunts, Martian Attack |
| 0x01B4 | martianmultiball_voc_you_re_some_ugly_martians | Martian Attack end variant | Martians: voices, taunts, Martian Attack |
| 0x01B5 | extraball_voc_extraball | extra ball voice line | SFX & speech (general) |
| 0x01B6 | multiball_rampshot_voc_soldier_jackpot |  | Locks, multiball, jackpots, extra ball |
| 0x01B8 | lock3_voc_start_multiball |  | Locks, multiball, jackpots, extra ball |
| 0x01BA | wave6_voc_start_let_s_take_their_ship_and_attack_mars |  | Martians: voices, taunts, Martian Attack |
| 0x01BC | atomicblaster_voc_we_must_build_an_atomic_blaster |  | SFX & speech (general) |
| 0x01BD | wave6_voc_start_we_must_finish_them_off | wave 6 (final wave) start | Saucer / attack waves |
| 0x01BE | shootagain_voc_shoot_again | keep shooting encouragement | SFX & speech (general) |
| 0x01BF | superjets_voc_superjets | Super Jets awarded | SFX & speech (general) |
| 0x01C0 | ruletheunivese_voc_success_five_billion |  | SFX & speech (general) |
| 0x01F9 | capture_voc_martian_ah_ah_ah_ah_ah |  | Martians: voices, taunts, Martian Attack |
| 0x01FA | martian_hit |  | Martians: voices, taunts, Martian Attack |
| 0x01FB | oh_no |  | SFX & speech (general) |
| 0x01FD | martian_hit |  | Martians: voices, taunts, Martian Attack |
| 0x01FE | martian_hit |  | Martians: voices, taunts, Martian Attack |
| 0x0214 | martianattack_voc_attack |  | Martians: voices, taunts, Martian Attack |
| 0x0215 | atomicblaster_voc_shootcenter_run_away |  | SFX & speech (general) |
| 0x0216 | greetings_earthlings_ah_ah |  | SFX & speech (general) |
| 0x0217 | aaaah_women |  | SFX & speech (general) |
| 0x0219 | saucer_shielddestroyed_voc_your_city_will_be_destroyed |  | Saucer / attack waves |
| 0x021A | earth_will_be_ours |  | SFX & speech (general) |
| 0x021C | saucer_shieldhit_voc_you_cannot_defeat_our_force_field |  | Saucer / attack waves |
| 0x021D | wave6_voc_success_2_can_t_we_just_be_friends_ | wave-6-end music stop | Saucer / attack waves |
| 0x021E | got_enough_ |  | SFX & speech (general) |
| 0x021F | saucer_shielddestroyed_voc_we_are_invincible |  | Saucer / attack waves |
| 0x0220 | ah_ah_ah_aaaah |  | SFX & speech (general) |
| 0x0222 | nothing_can_defeat_us |  | SFX & speech (general) |
| 0x0223 | atomicblaster_voc_it_will_never_work |  | SFX & speech (general) |
| 0x0224 | ouch |  | SFX & speech (general) |
| 0x0225 | ouch |  | SFX & speech (general) |
| 0x0226 | hey_look_your_shoe_in_untied_ah_ah_ah |  | SFX & speech (general) |
| 0x0227 | come_here_tasty_human |  | SFX & speech (general) |
| 0x0228 | wave6_voc_success_no_no_nooo | wave-6-end music stop | Saucer / attack waves |
| 0x0229 | multiball_rampshot_voc_jackpot |  | Locks, multiball, jackpots, extra ball |
| 0x022A | multiball_rampshot_voc_super_jackpot | super jackpot | Locks, multiball, jackpots, extra ball |
| 0x022B | greetings_earthling |  | SFX & speech (general) |
| 0x022D | ah_ah_ah |  | SFX & speech (general) |
| 0x022F | martianattack_voc_martianangry_aaaarrrgh_startmartianattack |  | Martians: voices, taunts, Martian Attack |
| 0x0230 | ha_ha_ha_by_martian |  | Martians: voices, taunts, Martian Attack |
| 0x0231 | more_women |  | SFX & speech (general) |
| 0x0232 | oh_yes |  | SFX & speech (general) |
| 0x0233 | startgame_voc_you_again |  | SFX & speech (general) |
| 0x0234 | martianattack_voc_not_you_again |  | Martians: voices, taunts, Martian Attack |
| 0x0237 | ugh_i_m_so_scared |  | SFX & speech (general) |
| 0x0238 | miss_me_ahah |  | SFX & speech (general) |
| 0x0239 | nanana_pfrrrr |  | SFX & speech (general) |
| 0x023A | wave6_voc_puny_humans_we_have_four_arms |  | Saucer / attack waves |
| 0x023B | martianmultiball_voc_again |  | Martians: voices, taunts, Martian Attack |
| 0x023C | multiball_rampshot_voc_oh_baby |  | Locks, multiball, jackpots, extra ball |
| 0x0242 | wave6_voc_haaah |  | Saucer / attack waves |
| 0x0243 | wave6_voc_martians_superior_humans_pathetic_aaah |  | Martians: voices, taunts, Martian Attack |
| 0x0244 | i_hate_humans |  | SFX & speech (general) |
| 0x0245 | oh_no |  | SFX & speech (general) |
| 0x0246 | martianmultiball_voc_start_oh_no_multiball |  | Martians: voices, taunts, Martian Attack |
| 0x0247 | wave6_voc_ah_we_won_t_be_defeated_so_easily |  | Saucer / attack waves |
| 0x0248 | multiball |  | Locks, multiball, jackpots, extra ball |
| 0x0249 | ruletheuniverse_voc_succes_you_rule_the_universe |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x024A | wave6_success_3_but_we_ll_be_back | wave 6 end | Saucer / attack waves |
| 0x024B | it_won_t_be_that_easy |  | SFX & speech (general) |
| 0x024C | not_so_fast | villain "not so fast" taunt | SFX & speech (general) |
| 0x024D | wave6_voc_not_so_fast_human |  | Saucer / attack waves |
| 0x024E | voc_replay | replay award | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x024F | ruletheuniverse_voc_start_so_you_want_to_rule_the_universe | Rule-the-Universe start | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0250 | ruletheuniverse_voc_start2_you_don_t_stand_a_chance |  | SFX & speech (general) |
| 0x0251 | surprise |  | SFX & speech (general) |
| 0x0258 | capture_voc_get_your_hands_off_me |  | SFX & speech (general) |
| 0x0259 | capture_voc_get_your_hands_off_me_all_four_of_them |  | SFX & speech (general) |
| 0x025A | capture_voc_help_oh_no_aaah |  | SFX & speech (general) |
| 0x025B | capture_voc_femaleaaah |  | SFX & speech (general) |
| 0x025C | capture_voc_put_me_down |  | SFX & speech (general) |
| 0x025D | capture_voc_femaleaaaah |  | SFX & speech (general) |
| 0x025E | capture_voc_hurryup_award_you_re_my_hero |  | Saucer / attack waves |
| 0x025F | capture_voc_hurryup_award_oh_thank_you_thank_you |  | Saucer / attack waves |
| 0x0260 | you_re_the_best |  | SFX & speech (general) |
| 0x0261 | look_out_martians |  | Martians: voices, taunts, Martian Attack |
| 0x0262 | get_them |  | SFX & speech (general) |
| 0x0263 | martianmultiball_voc_you_know_i_enjoy_killing_these_martians |  | Martians: voices, taunts, Martian Attack |
| 0x0269 | tractorbeam_voc_oh_they_ve_got_our_life_stock_and_treasured_historical_monuments |  | SFX & speech (general) |
| 0x026A | bigobeam_voc_female_would_you_look_at_the_size_of_that_cow |  | SFX & speech (general) |
| 0x026B | bigobeam_voc_female_it_s_hideous |  | SFX & speech (general) |
| 0x026D | bigobeam_voc_female_it_s_it_s_so_big |  | SFX & speech (general) |
| 0x0271 | bigobeam_voc_female_aaah |  | SFX & speech (general) |
| 0x0272 | extraball_lit_go_for_the_extra_ball | "go for the extra ball" (EB lit) | SFX & speech (general) |
| 0x0273 | multiball_shoot_for_the_super_jackpot | shoot-for-super-jackpot hint | Locks, multiball, jackpots, extra ball |
| 0x0274 | capture_voc_hurryup_save_me_save_me |  | Saucer / attack waves |
| 0x0276 | tractorbeam-voc_hurryup_get_them |  | Saucer / attack waves |
| 0x0277 | tractorbeam_voc_hey_they_ve_got_our_stuff |  | SFX & speech (general) |
| 0x0278 | tractorbeam_voc_stop_them |  | SFX & speech (general) |
| 0x0279 | tractorbeam_voc_hey_that_s_my_car |  | SFX & speech (general) |
| 0x027A | tractorbeam_voc_no_not_our_hotdogs |  | SFX & speech (general) |
| 0x02BC | wave1_voc_we_must_destroy_the_stinking_martians |  | Martians: voices, taunts, Martian Attack |
| 0x02BD | wave1_voc_you_martians_will_never_take_france |  | Martians: voices, taunts, Martian Attack |
| 0x02BE | you_will_remove_that_saucer_from_the_sky |  | Saucer / attack waves |
| 0x02BF | wave1_voc_start_sacre_bleu_the_martians_are_destroying_the_eiffel_tower |  | Martians: voices, taunts, Martian Attack |
| 0x02C0 | wave1_voc_healthzero_destroy_the_saucer |  | Saucer / attack waves |
| 0x02C1 | wave1_voc_healthzero_blow_the_saucer_out_of_the_sky |  | Saucer / attack waves |
| 0x02C2 | go_away_from_france_you_martians_from_another_planet |  | Martians: voices, taunts, Martian Attack |
| 0x02C3 | vive_la_france |  | SFX & speech (general) |
| 0x02C6 | wave3_voc_start_mamamia_save_the_tower_of_pisa |  | Saucer / attack waves |
| 0x02C7 | you_martians_are_no_good |  | Martians: voices, taunts, Martian Attack |
| 0x02CA | take_that_you_pasta_head |  | SFX & speech (general) |
| 0x02CB | wave3_voc_what_s_the_matter_you_you_ugly_martian |  | Martians: voices, taunts, Martian Attack |
| 0x02CC | wave3_voc_i_bust_you_face_you_ugly_martian |  | Martians: voices, taunts, Martian Attack |
| 0x02CD | wave3_voc_success_italia_italia |  | Saucer / attack waves |
| 0x02CE | wave3_voc_excellent |  | Saucer / attack waves |
| 0x02CF | well_done |  | SFX & speech (general) |
| 0x02D0 | achtung_martians |  | Martians: voices, taunts, Martian Attack |
| 0x02D1 | we_will_fight_for_germany |  | SFX & speech (general) |
| 0x02D2 | wave2_voc_take_that_you_ugly_green_martian |  | Martians: voices, taunts, Martian Attack |
| 0x02D3 | wave2_voc_germany_will_kick_your_martian_butt_to_the_moon |  | Martians: voices, taunts, Martian Attack |
| 0x02D4 | wave2_voc_start_the_brandenburg_tour_is_in_danger |  | Saucer / attack waves |
| 0x02D5 | destroy_the_martians |  | Martians: voices, taunts, Martian Attack |
| 0x02D6 | look_out_martians_germany_coming_through |  | Martians: voices, taunts, Martian Attack |
| 0x02D7 | wave2_voc_healthzero_destroy_the_saucer |  | Saucer / attack waves |
| 0x02D8 | wave2_voc_success_germany_is_victorious |  | Saucer / attack waves |
| 0x02D9 | wave2_voc_the_martians_they_ll_never_take_germany |  | Martians: voices, taunts, Martian Attack |
| 0x02DA | wave2_voc_start_we_must_save_the_brandenburg_tour |  | Saucer / attack waves |
| 0x02DB | wave4_voc_start_no_time_for_tea_blast_those_martians |  | Martians: voices, taunts, Martian Attack |
| 0x02DC | wave4_voc_start_blimey_london_bridge_is_falling_down_isn_t_it |  | Saucer / attack waves |
| 0x02DD | wave4_voc_healthzero_blow_the_saucer_out_of_the_sky |  | Saucer / attack waves |
| 0x02DE | destroy_bleeding_saucer |  | Saucer / attack waves |
| 0x02DF | wave4_voc_destroy_tho_lily_livered_martians_star_of_london_england_mode |  | Martians: voices, taunts, Martian Attack |
| 0x02E5 | wave4_voc_take_that_you_horrible_green_martian |  | Martians: voices, taunts, Martian Attack |
| 0x02E6 | wave4_voc_success_that_s_all_for_now |  | Saucer / attack waves |
| 0x02EA | i_say_good_shot |  | SFX & speech (general) |
| 0x02EB | wave4_voc_super_shot |  | Saucer / attack waves |
| 0x02ED | wave4_voc_success_well_done |  | Saucer / attack waves |
| 0x02F9 | bigobeam_voc_hideyalobsters |  | SFX & speech (general) |
| 0x02FA | gamestart_newsticker1 |  | SFX & speech (general) |
| 0x02FB | gamestart_newsticker2 |  | SFX & speech (general) |
| 0x02FC | oh_no_sparky_ |  | SFX & speech (general) |
| 0x02FF | dog_bark |  | SFX & speech (general) |
| 0x0304 | take_that_you_ugly_green_stinking_disgusting_martian_ |  | Martians: voices, taunts, Martian Attack |
| 0x0307 | you_are_very_skillful_wow |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0308 | wave1_voc_saucerdestroyed_oulala |  | Saucer / attack waves |
| 0x0309 | outrageous |  | SFX & speech (general) |
| 0x030D | wave3_voc_healthzero_blow_the_saucer_out_of_the_sky |  | Saucer / attack waves |
| 0x030F | wave3_voc_start_mamamia_the_martians_are_straightening_the_tower_of_pisa |  | Martians: voices, taunts, Martian Attack |
| 0x0311 | wave5_voc_saucerhit_take_that_martian |  | Martians: voices, taunts, Martian Attack |
| 0x0312 | wave5_voc_saucerhit_and_that |  | Saucer / attack waves |
| 0x0313 | wave5_voc_blast_the_saucers |  | Saucer / attack waves |
| 0x0314 | wave5_voc_healthzero_blow_the_saucer_out_of_the_sky |  | Saucer / attack waves |
| 0x0315 | will_blow_the_snot_out_of_you_martians |  | Martians: voices, taunts, Martian Attack |
| 0x0316 | destroy_the_saucer |  | Saucer / attack waves |
| 0x0317 | wave5_voc_we_ll_fight_for_our_freedom |  | Saucer / attack waves |
| 0x0318 | get_em |  | SFX & speech (general) |
| 0x0319 | look_out_martians |  | Martians: voices, taunts, Martian Attack |
| 0x031A | wave5_voc_saucerdestroyed_nobody_messes_with_the_usa |  | Saucer / attack waves |
| 0x031B | wave5_voc_start_we_gotta_save_the_statue_of_liberty |  | Saucer / attack waves |
| 0x0320 | ball_lock |  | Locks, multiball, jackpots, extra ball |
| 0x0321 | sameas-000800-ball_lock |  | Locks, multiball, jackpots, extra ball |
| 0x0322 | wouiii |  | SFX & speech (general) |
| 0x0323 | wouiii |  | SFX & speech (general) |
| 0x0328 | ramp |  | SFX & speech (general) |
| 0x0329 | sameas-000808-ramp |  | SFX & speech (general) |
| 0x032A | cow_ramp |  | SFX & speech (general) |
| 0x032B | sameas-000810-cow_ramp |  | SFX & speech (general) |
| 0x0330 | lock2_missileslocked |  | Locks, multiball, jackpots, extra ball |
| 0x0331 | lock2_missileslocked2 |  | Locks, multiball, jackpots, extra ball |
| 0x0332 | ramp |  | SFX & speech (general) |
| 0x0333 | sameas-000818-ramp |  | SFX & speech (general) |
| 0x0334 | ramp_while_pressing_launh_button |  | SFX & speech (general) |
| 0x0335 | sameas-000820-ramp_while_pressing_launh_button |  | SFX & speech (general) |
| 0x0336 | burp |  | SFX & speech (general) |
| 0x0337 | sameas-000822-burp |  | SFX & speech (general) |
| 0x0338 | saucer_wireramp_kickout |  | Saucer / attack waves |
| 0x0339 | saucer_wireramp_kickout2 |  | Saucer / attack waves |
| 0x033A | saucer_wireramp_kickout_after_destroy |  | Saucer / attack waves |
| 0x033B | saucer_wireramp_kickout_after_destroy2 |  | Saucer / attack waves |
| 0x033C | scoop_out |  | SFX & speech (general) |
| 0x033D | scoop_out_2 |  | SFX & speech (general) |
| 0x033E | scoop_out_kickout |  | SFX & speech (general) |
| 0x033F | scoop_out_kickout_2 |  | SFX & speech (general) |
| 0x0340 | rooster |  | SFX & speech (general) |
| 0x0341 | sameas-000832-rooster |  | SFX & speech (general) |
| 0x0342 | rooster_2 |  | SFX & speech (general) |
| 0x0343 | sameas-000834-rooster_2 |  | SFX & speech (general) |
| 0x0344 | big_rooster |  | SFX & speech (general) |
| 0x0345 | sameas-000836-big_rooster |  | SFX & speech (general) |
| 0x0346 | saucerdestroyed_saucerexplosion | SAUCER DESTROYED (wave completion) — unambiguous kill signal | Saucer / attack waves |
| 0x0347 | saucerdestroyed_saucerexplosion2 | saucer destroyed (duplicate id) | Saucer / attack waves |
| 0x0348 | saucerdestroyed_shipsound | explosion — fires on NON-final explosions too, NOT a completion signal | Saucer / attack waves |
| 0x0349 | saucerdestroyed_shipsound2 | explosion (dup) — same caveat | Saucer / attack waves |
| 0x034A | saucerdestroyed_shipwhirringup |  | Saucer / attack waves |
| 0x034B | saucerdestroyed_shipwhirringup2 |  | Saucer / attack waves |
| 0x0352 | saucer_targetbankhit |  | Saucer / attack waves |
| 0x0353 | saucer_targetbankhit2 |  | Saucer / attack waves |
| 0x0354 | replay |  | SFX & speech (general) |
| 0x0355 | sameas-000852-replay |  | SFX & speech (general) |
| 0x0356 | big_o_meam_loading |  | SFX & speech (general) |
| 0x0357 | sameas-000854-big_o_meam_loading |  | SFX & speech (general) |
| 0x0358 | saucershield_destroyed_banklowering_attackwavestarting |  | Saucer / attack waves |
| 0x0359 | saucershield_destroyed_banklowering_attackwavestarting2 |  | Saucer / attack waves |
| 0x035A | flying_saucer_take_off |  | Saucer / attack waves |
| 0x035B | flying_saucer_take_off_2 |  | Saucer / attack waves |
| 0x035C | saucer_explosion_and_video_mode_option_remove_explosion |  | Saucer / attack waves |
| 0x035D | saucer_explosion_and_video_mode_option_remove_explosion2 |  | Saucer / attack waves |
| 0x0362 | ha_ha_ha_martian_voice |  | Martians: voices, taunts, Martian Attack |
| 0x0363 | sameas-000866-ha_ha_ha_martian_voice |  | Martians: voices, taunts, Martian Attack |
| 0x0364 | martianmultiball_voc_martianscreaminguuh |  | Martians: voices, taunts, Martian Attack |
| 0x0365 | martianmultiball_voc_martianscreaminguuh2 |  | Martians: voices, taunts, Martian Attack |
| 0x0366 | martianattack_voc_lastmartian_ohno | "oh no" — last martian remaining | Martians: voices, taunts, Martian Attack |
| 0x0367 | martianattack_voc_lastmartian_ohno2 | "oh no" (dup) | Martians: voices, taunts, Martian Attack |
| 0x0368 | martianmultiball_voc_martianscreamingoww |  | Martians: voices, taunts, Martian Attack |
| 0x0369 | martianmultiball_voc_martianscreamingoww2 |  | Martians: voices, taunts, Martian Attack |
| 0x036A | martianattack_voc_martianscreamingoow |  | Martians: voices, taunts, Martian Attack |
| 0x036B | martianattack_voc_martianscreamingoow2 |  | Martians: voices, taunts, Martian Attack |
| 0x036E | martianattack_voc_attack2 |  | Martians: voices, taunts, Martian Attack |
| 0x036F | martianattack_voc_attack3 |  | Martians: voices, taunts, Martian Attack |
| 0x0370 | run_away |  | SFX & speech (general) |
| 0x0371 | sameas-000880-run_away |  | SFX & speech (general) |
| 0x0372 | greetings_earthling_ah_ah_ah_urgh |  | SFX & speech (general) |
| 0x0373 | sameas-000882-greetings_earthling_ah_ah_ah_urgh |  | SFX & speech (general) |
| 0x0374 | aaaah_women |  | SFX & speech (general) |
| 0x0375 | sameas-000884-aaaah_women |  | SFX & speech (general) |
| 0x0378 | your_cities_will_be_destroyed_ |  | Saucer / attack waves |
| 0x0379 | sameas-000888-your_cities_will_be_destroyed_ |  | Saucer / attack waves |
| 0x037A | earth_will_be_ours |  | SFX & speech (general) |
| 0x037B | sameas-000890-earth_will_be_ours |  | SFX & speech (general) |
| 0x037E | you_cannot_defeat_our_force_field |  | SFX & speech (general) |
| 0x037F | sameas-000894-you_cannot_defeat_our_force_field |  | SFX & speech (general) |
| 0x0380 | can_t_we_just_be_friends_ |  | SFX & speech (general) |
| 0x0381 | sameas-000896-can_t_we_just_be_friends_ |  | SFX & speech (general) |
| 0x0382 | got_enough_ |  | SFX & speech (general) |
| 0x0383 | sameas-000898-got_enough_ |  | SFX & speech (general) |
| 0x0384 | we_are_invincible |  | SFX & speech (general) |
| 0x0385 | sameas-000900-we_are_invincible |  | SFX & speech (general) |
| 0x0386 | ha_ha_ha_martian_voice |  | Martians: voices, taunts, Martian Attack |
| 0x0387 | sameas-000902-ha_ha_ha_martian_voice |  | Martians: voices, taunts, Martian Attack |
| 0x038A | nothing_can_defeat_us |  | SFX & speech (general) |
| 0x038B | sameas-000906-nothing_can_defeat_us |  | SFX & speech (general) |
| 0x038C | it_will_never_work |  | SFX & speech (general) |
| 0x038D | sameas-000908-it_will_never_work |  | SFX & speech (general) |
| 0x038E | ouch |  | SFX & speech (general) |
| 0x038F | sameas-000910-ouch |  | SFX & speech (general) |
| 0x0390 | ouch_2 |  | SFX & speech (general) |
| 0x0391 | sameas-000912-ouch_2 |  | SFX & speech (general) |
| 0x0392 | sneakattack_voc_hey_look_your_shoe_is_untied | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x0393 | sneakattack_voc_hey_look_your_shoe_is_untied2 | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x0394 | sneakattack_voc_come_here_tasty_human | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x0395 | sneakattack_voc_come_here_tasty_human2 | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x0396 | no_no_nooo |  | Martians: voices, taunts, Martian Attack |
| 0x0397 | sameas-000918-no_no_nooo |  | Martians: voices, taunts, Martian Attack |
| 0x0398 | laser |  | Martians: voices, taunts, Martian Attack |
| 0x0399 | sameas-000920-laser |  | Martians: voices, taunts, Martian Attack |
| 0x039A | laser |  | Martians: voices, taunts, Martian Attack |
| 0x039B | sameas-000922-laser |  | Martians: voices, taunts, Martian Attack |
| 0x039C | greetings_earthling |  | Martians: voices, taunts, Martian Attack |
| 0x039D | sameas-000924-greetings_earthling |  | Martians: voices, taunts, Martian Attack |
| 0x03A0 | sneakattack_voc_hahaha | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x03A1 | sneakattack_voc_hahaha2 | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x03A4 | martian_growl |  | Martians: voices, taunts, Martian Attack |
| 0x03A5 | sameas-000932-martian_growl |  | Martians: voices, taunts, Martian Attack |
| 0x03A6 | sneakattack_voc_martian_laugh | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x03A7 | sneakattack_voc_martian_laugh2 | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x03A8 | more_women |  | Martians: voices, taunts, Martian Attack |
| 0x03A9 | sameas-000936-more_women |  | Martians: voices, taunts, Martian Attack |
| 0x03AA | oooh_yes |  | Martians: voices, taunts, Martian Attack |
| 0x03AB | sameas-000938-oooh_yes |  | Martians: voices, taunts, Martian Attack |
| 0x03AC | you_again |  | Martians: voices, taunts, Martian Attack |
| 0x03AD | sameas-000940-you_again |  | Martians: voices, taunts, Martian Attack |
| 0x03AE | not_you_again |  | Martians: voices, taunts, Martian Attack |
| 0x03AF | sameas-000942-not_you_again |  | Martians: voices, taunts, Martian Attack |
| 0x03B4 | ugh_i_m_so_scared |  | Martians: voices, taunts, Martian Attack |
| 0x03B5 | sameas-000948-ugh_i_m_so_scared |  | Martians: voices, taunts, Martian Attack |
| 0x03B6 | missed_me_ahah |  | Martians: voices, taunts, Martian Attack |
| 0x03B7 | sameas-000950-missed_me_ahah |  | Martians: voices, taunts, Martian Attack |
| 0x03B8 | nananana_pffff |  | Martians: voices, taunts, Martian Attack |
| 0x03B9 | sameas-000952-nananana_pffff |  | Martians: voices, taunts, Martian Attack |
| 0x03BA | saucerdestroyed_applause |  | Martians: voices, taunts, Martian Attack |
| 0x03BB | saucerdestroyed_applause2 |  | Martians: voices, taunts, Martian Attack |
| 0x03BC | game_start_ball_in |  | Martians: voices, taunts, Martian Attack |
| 0x03BD | game_start_ball_in_2 |  | Martians: voices, taunts, Martian Attack |
| 0x03BE | bigobeam_cow_triggeredwithlaunchbutton |  | Martians: voices, taunts, Martian Attack |
| 0x03BF | bigobeam_cow_triggeredwithlaunchbutton2 |  | Martians: voices, taunts, Martian Attack |
| 0x03C0 | tractorbeam_cow_triggeredwithlaunchbutton |  | Martians: voices, taunts, Martian Attack |
| 0x03C1 | tractorbeam_cow_triggeredwithlaunchbutton2 |  | Martians: voices, taunts, Martian Attack |
| 0x03C2 | sneakattack_voc_surprise | Sneak Attack (single martian pop-up) | Martians: voices, taunts, Martian Attack |
| 0x03C3 | sneakattack_voc_surprise2 |  | Martians: voices, taunts, Martian Attack |
| 0x03C4 | replay |  | Martians: voices, taunts, Martian Attack |
| 0x03C5 | sameas-000964-replay |  | Martians: voices, taunts, Martian Attack |
| 0x03D4 | menu_sound |  | SFX & speech (general) |
| 0x03D5 | sameas-000980-menu_sound |  | SFX & speech (general) |
| 0x03D6 | menu_back |  | SFX & speech (general) |
| 0x03D7 | menu_sound_enter |  | SFX & speech (general) |
| 0x03D8 | menu_coin_door_open |  | Attract, coins, match, tilt, service |
| 0x03D9 | menu_sound |  | SFX & speech (general) |
| 0x03DA | sameas-000985-menu_sound |  | SFX & speech (general) |
| 0x03DB | menu_reverse |  | SFX & speech (general) |
| 0x03DC | menu_enter |  | SFX & speech (general) |
| 0x03DD | menu |  | SFX & speech (general) |
| 0x03E3 | gamestart |  | SFX & speech (general) |
| 0x03E5 | endvideomode |  | SFX & speech (general) |
| 0x03E6 | martianattack start |  | Martians: voices, taunts, Martian Attack |
| 0x044C | puny_humans_we_have_four_arms |  | SFX & speech (general) |
| 0x044D | sameas-001100-puny_humans_we_have_four_arms |  | SFX & speech (general) |
| 0x044E | martianmultiball_voc_again |  | Martians: voices, taunts, Martian Attack |
| 0x044F | martianmultiball_voc_again2 |  | Martians: voices, taunts, Martian Attack |
| 0x0450 | oh_baby |  | SFX & speech (general) |
| 0x0451 | sameas-001104-oh_baby |  | SFX & speech (general) |
| 0x0452 | sneakattack_voc__haaa |  | Martians: voices, taunts, Martian Attack |
| 0x0453 | sneakattack_voc__haaa2 |  | Martians: voices, taunts, Martian Attack |
| 0x0454 | martians_superior_humans_pathetic_aaah |  | Martians: voices, taunts, Martian Attack |
| 0x0455 | sameas-001108-martians_superior_humans_pathetic_aaah |  | Martians: voices, taunts, Martian Attack |
| 0x0456 | i_hate_humans |  | SFX & speech (general) |
| 0x0457 | sameas-001110-i_hate_humans |  | SFX & speech (general) |
| 0x0458 | oh_no |  | SFX & speech (general) |
| 0x0459 | sameas-001112-oh_no |  | SFX & speech (general) |
| 0x045A | ah_we_won_t_be_defeated_so_easily |  | SFX & speech (general) |
| 0x045B | sameas-001114-ah_we_won_t_be_defeated_so_easily |  | SFX & speech (general) |
| 0x045C | multiball |  | Locks, multiball, jackpots, extra ball |
| 0x045D | sameas-001116-multiball |  | Locks, multiball, jackpots, extra ball |
| 0x045E | you_rule_the_universe |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x045F | sameas-001118-you_rule_the_universe |  | Awards & flow (skill shot, ball save, replay, RTU, SOL) |
| 0x0460 | but_we_ll_be_back |  | SFX & speech (general) |
| 0x0461 | sameas-001120-but_we_ll_be_back |  | SFX & speech (general) |
| 0x0462 | it_won_t_that_easy |  | SFX & speech (general) |
| 0x0463 | sameas-001122-it_won_t_that_easy |  | SFX & speech (general) |
| 0x0464 | not_so_fast |  | SFX & speech (general) |
| 0x0465 | sameas-001124-not_so_fast |  | SFX & speech (general) |
| 0x0466 | not_so_fast_human |  | SFX & speech (general) |
| 0x0467 | sameas-001126-not_so_fast_human |  | SFX & speech (general) |
| 0x0468 | replay |  | SFX & speech (general) |
| 0x0469 | sameas-001128-replay |  | SFX & speech (general) |
| 0x55AA | (unnamed) | special/system command observed in stream | Protocol / system |
| 0x55AB | (unnamed) | special/system command | Protocol / system |
| 0xAAFF | shootagain | special/system command | Protocol / system |

## Service and setup documentation

The contributor-held operations manual, which is not retained in this repository's evidence roots, is the 'Bally Attack From Mars Full Operations Manual (Final)' scan, 176 pages, SHA-256 `12c36ce8e1e0997a03016d76589df4fe2a6ad66cd5592d2a6f8dd75e49f6b1e5` (image-only scan; matrix pages were rendered and read visually, not OCR-trusted). Game adjustments, error codes, and unit disassembly (flying saucer mechanism 1-57, back panel 1-63) are in Section 1; parts and assemblies in Section 2; wiring diagrams and schematics in Section 3.

## One open question that is deliberately not asserted

The retained table carries three bulb lights `gi31`, `gi32` and `gi33` sitting exactly at the three
jet-bumper centres. They are absent from the `aGiTLights` collection that the script modulates,
which proves only that this table does not drive them through that collection - it does not prove
the physical sockets are missing, and the script's own comment says general-illumination string 03
also covers the bumpers. The manual itemizes no general-illumination string, so no printed count
exists either way.

The definition therefore asserts **no** physical socket count for string 03, and its fourteen
placements are documented as the emitters the string is observed to drive rather than a complete
socket inventory. Strings 01 and 02 keep their table-derived counts because no comparable ambiguity
exists for them. An author recreating the machine gets fourteen correct emitter positions plus this
note, and nothing uncertain is presented as settled.

## Resolved since the partial state

Every question this note previously left open has been answered, and the definition is now
`author_ready`:

- **Spatial placement.** All 187 placements are normalized against the retained JPSalas 3.0.2 table
  at bounds `left=0 top=0 right=964 bottom=2162`. See
  `reports/spatial/bally/attack-from-mars-1995.md` for the projection list and the excluded
  render-helper classes.
- **Wiring.** Every switch, solenoid, lamp and GI address now carries its printed connector, wire
  colour and driver transistor from the handbook's switch matrix, lamp matrix and solenoid/flasher
  table.
- **GI strings.** All five are modelled. Strings 01-03 are playfield circuits with placements taken
  from the table's deduplicated emitter arrays; strings 04 and 05 are backbox insert-panel circuits
  and take a controlled `cabinet_or_service` record with no asserted bulb count, because the manual
  publishes none.
- **Solenoid 43.** Resolved as the LPDC mirror of the Strobe Light on output 39, not a second
  saucer-dome circuit.
- **F1-F8.** Mapped to public addresses 111-118. F1-F4 are the two lower flippers' EOS leaves and
  cabinet button optos; F5-F8 are printed "Not Used" in both the switch matrix and the parts list and
  are marked unused, because Attack From Mars has no upper flippers. The matching upper Fliptronic
  *outputs* are still in use - they drive the two loop gates and the ramp diverter.
- **Variants.** All ten drivers now carry a `physical_compatibility` and `variant_notes` entry. The
  five factory revisions are `identical`; the Zen Studios and Global VR re-releases and the three
  FreeWPC builds are `compatible` and run on the unmodified physical machine.

## The motor bank gates the shots behind it

The three-bank moving target is the machine's central geometric mechanism and a recreation gets it
wrong without this: the bank does not merely present targets, it physically blocks the shots behind
it. Pinned PinMAME encodes the causality in its keyboard conditions - the three moving targets
45-47 are only reachable while switch 67 Motor Bank Up is closed, and the left and right saucer
targets 75/76, the drop target 77 and the centre trough 78 are only reachable while switch 66 Motor
Bank Down is closed. `afm_keyCond` says it plainly in a comment: "The drop target and hole behind can
only be reached if the bank is down."

The two retained models number the travel differently and neither is a physical measurement. The
JPSalas script's `cvpmMech` is linear, reversed and single-solenoid over 55 steps with switch 67 at
one end and 66 at the other; PinMAME's `afm_handleMech` steps an internal `bankPos` counter while
solenoid 24 is energized and asserts 66 near the start of the cycle and 67 near its midpoint. Both
agree the two leaf switches mark opposite ends of one continuous motor travel, which is the fact an
author needs. Solenoid 24 is wired through the flasher driver group on transistor Q29, but its load
is motor 14-8023 in assembly A-20572, not a flashlamp.

## The ramp diverter chooses the centre-ramp destination

Ramp diverter A-17241 with shaft and blade A-20556 rides the Fliptronic upper-left flipper circuit,
solenoid 35 power and 36 hold, which PinMAME reads together as its `sDiverter` custom solenoid from
`WPC_FLIPPERCOIL95` bits `0xc0`. With the blade at rest a centre-ramp shot entering at switch 62
continues to the right ramp exit at switch 65; with the diverter energized the same shot is delivered
into the left popper at opto 36. The retained script drives the blade with `SolDiv`, which rotates
the actuator and swaps which of the two ramp walls is dropped.

## One printed part number disagrees with itself

The upper-playfield parts list prints item 15's alien mech assembly as **A-20479-2** while the
solenoid-locations list prints the same mech as **A-20579-2**. The two differ by one digit and the
other three alien mechs are all A-20579-1, so A-20579-2 is the more likely reading, but the
disagreement is recorded rather than silently corrected. It has no behavioural consequence.

Two further printed details are worth carrying into a recreation. The flasher "assembly" numbers are
ramp assemblies, not flasher brackets: A-20621 is the middle plastic ramp (solenoids 17 and 18),
A-20549 the right wire ramp (19), A-20553 the left plastic ramp (25 and 26) and A-20546 the left wire
ramp (27). That is what puts solenoid 19 on the right side of the playfield and 27 on the left. And
solenoid 23 Saucer Dome shares assembly A-20670 with solenoids 37 and 38 - all three are on the one
saucer L.E.D. board inside saucer assembly A-20608.

## Sources

- `manual.attack-from-mars.1995`: contributor-held Bally/Midway operations manual scan, SHA-256 `12c36ce8e1e0997a03016d76589df4fe2a6ad66cd5592d2a6f8dd75e49f6b1e5`; lamp matrix 2-42/2-43, switch matrix 2-44, solenoid/flasher table 2-46, assemblies Section 2. **Not retained in this repository's evidence roots**, so it is corroboration for the retained handbook rather than an independent authority for any promoted assertion.
- `vpx.attack-from-mars-g5k-1.3.11`: known-working script at corpus revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `21fb64898f5a1a564e70ba2d40afed5fb54b8c49b0707530f0e24b7ca6cdf50c`; runs `afm_113b`; controller-address and callback authority.
- `runtime.afm-113b.contributor-logging`: contributor instrumentation on VPinMAME 3.6, `afm_113b.zip` SHA-256 `378102edfd80d650bf6810d5e521fd08cfd972f8732f3c2204f5929d2266358d`; no retained traces, candidate/observed authority only.
- `altsound.afm-113b.community-package`: contributor-held community altsound.csv for `afm_113b`, SHA-256 `bc139099b58ed94240d86f4fcc8e06ba37dafa5a14d9d5417917b5f225eac830`; sample-name reference for the DCS opcode table below. **Not retained in this repository's evidence roots**, and the opcode table is reference prose that no promoted assertion depends on.
- `legacy.game.afm` / `legacy.platform.wpc`: legacy VPE-derived import, corrected as documented above.
- `pinmame.catalog.4ec52ff0ac13`: pinned driver family and display topology.
- `manual.bally.attack-from-mars.1995`: retained Bally/Midway Operators Handbook 16-10206, SHA-256
  `5900c779f3bfb14251ada18d25a4dde84dd608b6ddd988ece8c92ea20fd0114b`; 16 image-only pages carrying the
  lamp matrix, switch matrix, solenoid/flasher table, all three location maps, the five
  general-illumination circuits, the flipper coils and the upper-playfield parts list.
- `manual-support.bally.attack-from-mars.1995`: human transcription of every printed table read from
  the rendered pages, SHA-256 `eecef9b72e309e581c07fd5ecc8c5b4f9d3808f5bf4a4a3fdf53891e10296733`.
- `vpx-table.afm-jpsalas-3-0-2` / `vpx-script.afm-jpsalas-3-0-2`: retained known-working JPSalas 3.0.2
  table, SHA-256 `f4bd2ae0e456030d14ea2f6f8fcd45e0e4f72ff22235a908d17424f1e9441cbd`, and its embedded
  script, SHA-256 `46992cf7854853bac592ab9b2b5f65d641727accec8405b7aff84fbc8e2aa139`; geometry for all
  187 placements and the runtime binding authority. It binds `afm_113b`.
- `runtime.attack-from-mars.boot-attract-and-ball-start`: pinned LibPinMAME harness runs that boot
  `afm_113b` from empty NVRAM, reach attract and start a ball; they observe all five GI strings, sixty
  matrix lamps, every one of the sixteen saucer-L.E.D. addresses, and solenoids 29, 31, 37, 38, 41
  and 42.
