# The Simpsons Pinball Party (Stern, 2003)

Coverage: **partial - complete physical I/O inventory, Whitestar bindings, mechanism causality,
driver-variant boundary, and recreation behavior validated; wiring conflicted pending resolution
of two unresolved conflicts (opto polarity and the unreadable upper-flipper button) below, and
lamps 73-80 plus the driver's auxiliary lamp-column capacity have no spatial placement**

## Identity and evidence precedence

This is the Stern Whitestar physical product released 2003, IPDB 4674. It covers the eighteen-driver
`simpprty` clone tree (`simpprty` parent plus seventeen firmware/localization revisions: five each
of 2.04/3.00/4.00, four of 5.00, all sharing one static `simpprtyGameData` struct through
`CORE_CLONEDEFNV`). Identity is confirmed from the retained VPX table's own script
(`Const cGameName="simpprty"`) and from pinned `src/wpc/segames.c`'s
`CORE_GAMEDEFNV(simpprty, "Simpsons Pinball Party, The (5.00)", 2003, "Stern", de_mSES2, 0)`. The
unrelated Data East 1990 "The Simpsons" is a different physical machine; the Internet Archive item
`arcademanual_The_Simpsons_OPS` covers that machine and was not used.

Evidence precedence for this definition: the retained embedded VPX script is runtime and
mechanism-causality ground truth; the Stern operations manual controls physical construction, part
numbers, wiring, quantities, and device presence; pinned PinMAME controls controller generation,
public address topology, and mechanism-table position ranges; the retained VPX geometry supplies
normalized coordinates. The retained manual's `pdftotext` layer is unreliable for two independent
reasons -- most runs double every character, and the diagnostics chapter's own embedded font subset
additionally shifts character codes by a constant +29 with no ToUnicode correction -- so every table
used here was read from a rendered page and transcribed into
`external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/manual-transcription.md`; the OCR
text is a search index only and never an authority.

## First Whitestar machine in this project: platform notes that generalize

This is the first Stern Whitestar (Sega/Stern `GEN_WS`, `src/wpc/se.c`) machine curated in this
project, so several address-space and normalization facts were re-derived from pinned source rather
than carried over from the WPC games curated earlier, and should be reused by future Whitestar
curations:

1. **Whitestar's switch matrix is sequential-by-column, not WPC's column-times-ten notation.**
   `se_m2sw(col, row) = col*8+(7-row)+1` in the driver's own 0-indexed terms; in 1-indexed printed-
   manual terms this is `address = (column-1)*8 + row`. Confirmed against every cell of this
   manual's own 8x8 SWITCH MATRIX GRID table (column 1 row 1 = public 1, column 8 row 8 = public 64).
   Lamps use the *opposite* axis order: the manual's own LAMP MATRIX GRID table is unambiguously
   row-major (`address = (row-1)*8 + column`), confirmed the same way across all 80 printed cells --
   do not assume switches and lamps share one addressing convention on this platform.
2. **No Whitestar game in the pinned source ever populates `wpc.invSw`.** `simpprtyGameData`'s
   positional aggregate initializer (`{GEN_WS, dispSPP, {flippers, swCol, lampCol, custSol,
   soundBoard, display}}`) only sets the fields present in the literal; the trailing `wpc`/`simData`/
   `sxx` struct members are left at their C zero-initialization default. `core.c:2455`
   (`memcpy(coreGlobals.invSw, core_gameData->wpc.invSw, ...)`) then copies those zeros straight into
   the live switch-inversion mask. A `grep -rn invSw src/wpc/segames.c` across the whole ~3600-line
   Whitestar game-table file returns no assignment at all -- this is a platform-wide fact, not
   specific to this game, and should be checked (not assumed) on every future Whitestar curation.
   `controllers/pinmame/whitestar.json` still declares `inversion_applied_by_emulator: true` as a
   platform *capability* claim (matching the WPC profiles' shape); this record documents the
   per-driver reality as `conflict.whitestar-invsw-never-populated` rather than editing the shared
   profile, since the capability genuinely exists on the platform even though this driver never
   exercises it.
3. **The dedicated-switch byte packs Left/Right flipper button-and-EOS pairs plus one dead
   upper-flipper bit, confirmed bit-for-bit from `se.c`'s own `dedswitch_r` comment.** `// D0 - DED
   #1 - Left Flipper` through `// D7 - DED #8 - Begin Test (Black Button)`, with `fls =
   core_revnyb(fls & 0x0f) | ((fls & 0x80)>>3)` read against `core.h`'s
   `CORE_SWLRFLIPEOSBIT=0x01`/`CORE_SWLRFLIPBUTBIT=0x02`/`CORE_SWLLFLIPEOSBIT=0x04`/
   `CORE_SWLLFLIPBUTBIT=0x08`/`CORE_SWULFLIPBUTBIT=0x80` yields DS-1->public 84 (LL button), DS-2->83
   (LL EOS), DS-3->82 (LR button), DS-4->81 (LR EOS), DS-5->88 (UL button bit -- see below). DS-6/7/8
   are the ordinary Red/Green/Black service buttons at `SE_SWRED=-2`/`SE_SWGREEN=-1`/`SE_SWBLACK=0`.
4. **A driver can declare an upper-flipper cabinet button in `hw.flippers` bit space that is never
   actually wired up, and the emulator's own dedicated-switch byte can name the dead bit directly.**
   `core.c`'s `locals.flipMask` construction unconditionally includes only the two lower-flipper
   button bits; it includes the four EOS bits and the two upper-flipper button bits *only* if the
   matching `FLIP_EOS(...)`/`FLIP_SW(FLIP_Ux)` bit is set in `core_gameData->hw.flippers`.
   `simpprtyGameData.hw.flippers = FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)` sets only the lower-flipper
   bits, so `flipMask = 0x0F` (both lower buttons, both lower EOS, no upper bits at all), and public
   switch 88 is never written by `core_updateSw` for this driver -- not merely unobserved, but
   structurally unreachable. See "Three flipper coils with no dedicated button" below.
5. **The flipper-coil address remap is confirmed directly from the driver's own comment.**
   `se.c`'s `se_solenoid_w`: `/* move flipper power solenoids (L=15,R=16) to (R=45,L=47) */`. Raw
   solenoid addresses 15/16 are masked out of the public 9-16 group (`sols &= 0xffff3fff`) and
   instead drive `selocals.flipsol`; physical Q16 (RIGHT FLIPPER) surfaces at public power-phase 45
   and canonical callback 46, physical Q15 (LEFT FLIPPER) at public power-phase 47 and canonical
   callback 48 -- matching `controllers/pinmame/whitestar.json`'s own note exactly, now verified
   against source rather than assumed from the profile text.
6. **`coreGlobals.nGI = 1` is set directly in `se.c`** (both the `MACHINE_INIT`/`MACHINE_RESET`
   paths), so Whitestar publishes exactly one aggregate GI channel regardless of how many separately
   fused physical illumination branches a machine's own wiring diagram shows. This manual's General
   Illumination Circuit Detailed Wiring Diagram (PDF 121, printed 103) shows one relay closing four
   fused branches simultaneously, which is the same single-relay design PinMAME models -- unlike the
   WPC-95 GI conflicts already documented for Tales of the Arabian Nights and Theatre of Magic in
   this project, there is no script-vs-manual disagreement here at all.

## Address topology for this game specifically

- Switches: matrix 1-64 (two "NOT USED" gray-shaded positions, 27 and 28), dedicated -3/-2/-1/0 and
  81-84/88, CPU DIP 1-8 (5-bit country selector, bits 6-8 unused padding).
- Solenoids: physical drivers 1-14 and 17-32 retain their printed numbers; 15/16 are always-masked
  raw addresses for the two lower flipper coils, which surface instead at 45-48; the Solenoid
  Expander Auxiliary board (`SE_BOARDID_520_5068_01`) publishes three UK-only up/down-post outputs at
  33-35 and leaves 36 unused; 37-44 are reserved WPC-family compatibility holes; 49 is the
  simulator-only shooter channel and 50 is reserved. Ten of the thirty-two main-board positions are
  flashers (21-23, 25-29, 31, 32, confirmed by the manual's own "In Test Flash Lamps Menu... This
  Game: Q21-Q23, Q25-Q29, Q31-Q32" note); position 24 ("Optional Coil") is explicitly optional
  factory-fit hardware for a coin meter, token dispenser, or knocker.
- Lamps: 8x10 matrix 1-80 (two "NOT USED" positions, 71-72); lamp 32 (Tournament Button) is optional,
  gated behind the Optional Tournament Kit, and has no `l32` object anywhere in the retained script's
  own lamp-fade sequence at all.
- GI: one aggregate channel, public address 0.
- `simpprtyGameData.hw.lampCol = 4` declares up to four auxiliary lamp columns (public 81-112 by the
  platform's own addressing convention if populated), but this capacity is not identified by any
  available primary source -- see "Unresolved: auxiliary lamp columns" below.

## Ball path: trough, saucers, and VUKs

Five balls rest on trough switches 10-13 (5-Ball Trough #1 nearest the release kicker through #4 at
the drain entrance) plus opto 14 (5-Ball Trough VUK Opto). The retained script's
`bsTrough.InitSw 0,14,13,12,11,10,0,0` reads all five through the shared `cvpmBallStack` helper
class, which manages ball position internally rather than exposing five separate playfield trigger
objects, so all five (plus the related stacking opto, switch 15) are documented projections onto the
trough's own release kicker (`BallRelease`). `SolRelease` (solenoid 1) fires `bsTrough.ExitSol_On`
and also pulses switch 15 in the same event. Switches 14 and 15 share one Transmitter/Receiver opto
PC-board part pair per the manual's own "Sw. 14 & 15 Part Note" -- the only two switches this manual
identifies as opto construction anywhere in the document; there is no shaded-cell opto legend on this
manual's switch-matrix page at all, unlike the Williams WPC-95 manuals used earlier in this project.

Three simple saucer/VUK mechanisms round out the ball-management inventory: the Itchy & Scratchy
Eject VUK (switch 20, solenoid 5), the Upper Right saucer (switch 24, solenoid 19), and the Upper
Left VUK (switch 55, solenoid 6), each confirmed by the matching `cvpmBallStack.InitSaucer`/`InitSw`
call in the retained script.

## Drop-target bank, Couch lock, TV lock post, and Garage door

Three drop targets (#1 Top/switch 17, #2 Mid/switch 18, #3 Bot/switch 19) share one reset solenoid
(4, Drops Reset Up) and one trip solenoid (30, Drop Bank Trips); `dtDrop.InitDrop
Array(sw17, sw18, sw19), Array(17, 18, 19)` wires them directly. Neither reset-related solenoid has
a separate reset-bar mesh in the retained table, so both are documented projections onto the bank's
own middle target.

A ball enters the Couch lock through the Couch Enter gate (switch 36) and stacks on up to three lock
positions (38 Bot, 39 Mid, 40 Top); solenoid 3 (Couch Release, script sub `CouchExit`) opens a drop
gate (`CouchDrop`) to release the stack. Solenoid 7 (TV Release) raises and lowers a post (`TopPost`)
that holds a ball at the TV Lockup switch (37); there is no separate lock-position sensor beyond
switch 37 itself. Solenoid 20 (Garage Door (Eject)) drives an *incremental* open/close motion rather
than a single pulse: the retained script's `GdoorT_Timer` steps `Gdoor.RotX` by 4 degrees per tick
across a 0-60 degree range, and switch 48 (Garage Door) is set or cleared only once the door reaches
its open or closed limit, not continuously during the sweep.

## Homer Head toy

Solenoid 8 (Homer Head) actuates a moving figure (`HHead`); `HomerOn_Timer`/`HomerOff_Timer` animate
its rotation while `HomerActive` is set. Ball position relative to the figure is tracked by four
internal VPX trigger objects (`Homer`, `Homer2`, `Homer3`, `homer4`) that contain no
`Controller.Switch` call anywhere in the retained script -- they drive only the figure's own
animation state, never a public switch address.

## Three flipper coils with no dedicated button, and a documented conflict

The lower flipper pair (printed coils #15 Left, #16 Right) is the only flipper hardware PinMAME's
synthesized flipper subsystem knows about, remapped to public 45-48 as described above and read from
dedicated switches DS-1..DS-4 (public 84/83/82/81). Three *additional*, ordinary numbered solenoids
exist purely as ball-playfield coils with no PinMAME flipper-subsystem involvement at all:

- 12, "UPF Left Flipper" -- the upper mini-playfield's left flipper.
- 13, "UPF Right Flipper" -- the upper mini-playfield's right flipper.
- 14, "Top Right Flipper" -- a third main-playfield flipper, distinct from both the lower-right
  flipper (15/16) and the upper mini-playfield pair.

None of the three has a dedicated public-switch button input, because `simpprtyGameData.hw.flippers`
declares no `FLIP_UL`/`FLIP_UR` bits at all. The manual nonetheless documents a real, populated
cabinet button for the third of these -- DS-5, "Upper Rt. Flipper Button", part 180-5164-00 Doubled,
the identical doubled-button part used for DS-3 (Right Flipper Button) -- wired GRY-GRN to CN6-P7.
Pinned `se.c`'s own `dedswitch_r` comment marks that exact bit `"D4 - DED #5 - Not Used (Upper
Flipper on some games!)"`, and `core.c`'s `locals.flipMask` construction confirms it structurally:
the bit is never written by `core_updateSw` for this driver, so public switch 88 always reads
inactive regardless of the physical button.

The retained (thin, non-VPW) table's own script is consistent with the button being unread: its
`SolRFlipper` (the ordinary lower-right flipper's canonical callback, public 46) redundantly rotates
solenoid 14's own table object (`RightFlipper2`) *alongside* solenoid 14's independent
`SolTopRightFlipper` callback, suggesting the real ROM fires the third flipper coil automatically off
the ordinary right-flipper button rather than reading a separate input. But a ~41 KB community
script cannot prove what the real ROM does with the physical DS-5 button, if anything -- this is
recorded as an unresolved conflict, `conflict.upper-flipper-button-not-read`, rather than assumed
either way. How solenoids 12/13 (the upper mini-playfield pair) are triggered cannot be confirmed
from this table's script at all; it contains no `Controller.Switch`/`vpmTimer.PulseSw` call anywhere
near `SolUPFLeftFlipper`/`SolUPFRightFlipper`.

## Jet bumpers: object names do not match printed sides

Three jet bumpers, and the retained script's own object names are a trap: `Bumper1_Hit` pulses
switch 50 (Right Bumper) and fires solenoid 10; `Bumper2_Hit` pulses switch 51 (Bottom Bumper) and
fires solenoid 11; `Bumper3_Hit` pulses switch 49 (Left Bumper) and fires solenoid 9 -- i.e. object
number order (1, 2, 3) does **not** match printed side order (Left, Right, Bottom) or address order
(49, 50, 51) at all. This was confirmed two ways: directly from the script's own
`Controller.Switch`/`vpmTimer.PulseSw` calls, and geometrically -- `Bumper3` sits at the lowest x
(leftmost), `Bumper1` at the highest x (rightmost), and `Bumper2` at the highest y (frontmost, i.e.
"bottom" of the nest) -- both independently agreeing with the printed Left/Right/Bottom identity.

## Lamps: the Mini-DMD sign panel has no per-bulb placement

Lamps 73-80 (Duffman, Homer's Day, Willie's Woes, Wiggum vs Snake, Bart's Day, Krusty's Last Stand,
Stop The Monorail, Alien Invasion) are Green/Red LEDs on "LED PC Bd., 520-5219-00" per the manual's
own lamp-locations footnote -- exactly the board `simpprtyGameData.hw.display` declares
(`SE_BOARDID_520_5219_00`, "The Simpson's Pinball Party Mini DMD"). The retained table's own
`LEDY`/`LEDG`/`LEDR` light collections, which the script's `UpdateLeds` `LampCallback` normally
drives for these eight addresses, are **empty** in this retained extraction. The `l73`-`l80` objects
that do exist are `Primitive` mesh stand-ins sharing one (x, y) location with only a stacked z offset
(165-305 in fixed 20-unit steps) -- a single physical sign panel rendered as an image swap, not eight
distinct playfield bulb positions. No spatial placement is claimed for these eight lamps; the
`spatial` key is omitted entirely rather than fabricating a coordinate or inventing a shared-local-
origin status the schema does not define (the same honest-omission pattern Star Trek: The Next
Generation's three unresolved Primitive-mesh lamps already established in this project).

## General illumination

One aggregate PinMAME GI channel (public address 0). The manual's wiring diagram shows one relay
closing four separately-fused branches (F24 backpanel/10 bulbs, F25 left playfield plus right return
lane/11 #44 + 1 #555, F26 upper mini-playfield plus spotlights plus coin door/7 #44 + 5 #555 plus
coin-door bulbs, F27 right playfield/12 #44), all switched together -- matching PinMAME's
single-channel model with no script-vs-manual disagreement, unlike the GI conflicts already
documented for Tales of the Arabian Nights and Theatre of Magic elsewhere in this project. The
manual's own bulb counts are printed "may change during production", so the retained table's own `GI`
collection (37 `GI_N` Light objects plus 5 `spotlightright*` objects, 42 members total, toggled
together by the script's `UpdateGI`) is used as the placement set rather than a hand count from the
diagram.

## Unresolved: auxiliary lamp columns

`simpprtyGameData.hw.lampCol = 4` reserves up to four auxiliary lamp columns beyond the base 80-lamp
matrix (internal array indices 10-13; public addresses 81-112 if populated, following the platform's
own row-major-across-columns convention). Pinned `se.c` wires only two of the four to any handler at
all (`gilamp_w`/`gilamp_r`, CPU addresses `0x3406-0x3407`, internal indices 10-11) -- and the
maintainer's own source comment on that handler, `// GI lamps on Simpsons?`, shows even upstream
PinMAME is unsure what hardware this drives. Neither this manual's 80-position Lamp Matrix Grid table
nor the retained script's own `Controller.ChangedLamps` consumption (the `UpdateLamps`/`NFadeL`
sequence stops at address 70, and the LED sequence separately covers 73-80 through the `UpdateLeds`
callback -- neither ever reads an address above 80) references anything in this range. No device is
enumerated for addresses 81-112 in this definition; the gap is named in `coverage.missing`
(`output_enumeration`) rather than guessed at.

## Manual identity and physical vs. UK-market variant hardware

Three regional-variant devices are enumerated but marked `optional` because their own manual
footnotes say so explicitly, not because of any absence in the retained table: cabinet-side switches
1/8 ("Left/Right Button (UK Only)"), the three AUX up/down-post solenoids 33-35 ("Auxiliary Coils
AUX 1 - AUX 3 are typically for UK Only"), and switch 53 / lamp 32 ("Tournament Button", "Optional
with Tournament Kit"). Coin-door matrix positions 3 and 7 print "Future Use" rather than "NOT USED"
in their Switch Part Number column -- the harness position is wired but no coin-slot hardware is
fitted by default -- and are recorded as `optional`, distinct from the two genuinely gray-shaded
"NOT USED" positions (27, 28).

## Author construction checklist

- Build the five-ball trough with its release kicker, the three-target drop bank with its reset and
  trip solenoids, the Couch lock (three stacked positions plus entry gate), the TV lock post, the
  incrementally-animated Garage door, the Homer Head toy, three saucer/VUK kickers, two slingshots,
  three jet bumpers (mind the non-matching object-to-address numbering above), and five flipper
  coils: the synthesized lower pair plus three independently-numbered upper/top-right coils with no
  dedicated button input of their own.
- Do not invert switches 14/15's public state without further evidence: pinned PinMAME applies none
  for this driver, and the manual states construction (opto) but not polarity for them
  (`conflict.whitestar-invsw-never-populated`, unresolved).
- Do not wire the physical Upper Rt. Flipper Button (DS-5) to anything the ROM reads; it has no
  reachable public address on this driver (`conflict.upper-flipper-button-not-read`, unresolved).
- Treat solenoids 15/16 as non-addresses; bind the two lower flipper coils at 45/46 (right) and
  47/48 (left) only, one physical coil per side.
- Do not invent lamp objects for 73-80 beyond a single sign-panel image swap, and do not invent
  devices for public lamp addresses above 80.

## Sources

- `manual.stern.the-simpsons-pinball-party.2003`: Stern Pinball The Simpsons Pinball Party
  operations manual, SHA-256 `412023c67f699d68c10c6a70120712d34d71417b7dd16f1662e252a66561c898`.
- `manual-support.stern.the-simpsons-pinball-party.2003`: retained human transcription, SHA-256
  `18a1d499a3525bd72340f0e5a98af98c3fb8b867f0f3b1b655242f5cc7ef37e8`.
- `vpx-script.simpsons-party-0-8-2`: retained known-working embedded script, SHA-256
  `5378f6baf3106ed013c6d1a787f4b6789bc1febe925903f05cb2eda9327b98ee`, binding `simpprty`.
- `vpx-table.simpsons-party-0-8-2`: retained table (v0.8.2), SHA-256
  `c7d14c512ae81eb0e26cddf9f74690818ae2259350cd334fc98be5e7ece79034`, bounds
  `left=0 top=0 right=952 bottom=2115`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/segames.c`, `src/wpc/se.c`, `src/wpc/se.h`, and the shared
  `src/wpc/core.c`/`core.h` flipper/switch/lamp handling at the pinned revision.
