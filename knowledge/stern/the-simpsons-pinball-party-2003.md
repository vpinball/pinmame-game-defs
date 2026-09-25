# The Simpsons Pinball Party (Stern, 2003)

Coverage: **partial - complete physical I/O inventory, Whitestar bindings, opto polarity, flipper
inputs, mechanism causality, driver-variant boundary, and recreation behavior validated; held below
author-ready because lamp 80's second LED has no coordinate and public lamps 81-96, which PinMAME
publishes for this driver, have unknown availability**

## Identity and evidence precedence

This is the Stern Whitestar physical product released 2003, IPDB 4674. It covers the eighteen-driver
`simpprty` clone tree (`simpprty` parent plus seventeen firmware/localization revisions: five of
4.00 and four each of 5.00, 3.00 and 2.04, all sharing one static `simpprtyGameData` struct through
`CORE_CLONEDEFNV`). Identity is confirmed from the retained VPX table's own script
(`Const cGameName="simpprty"`) and from pinned `src/wpc/segames.c`'s
`CORE_GAMEDEFNV(simpprty, "Simpsons Pinball Party, The (5.00)", 2003, "Stern", de_mSES2, 0)`. The
unrelated Data East 1990 "The Simpsons" is a different physical machine; the Internet Archive item
`arcademanual_The_Simpsons_OPS` covers that machine and was not used.

Evidence precedence for this definition: the retained embedded VPX script is runtime and
mechanism-causality ground truth; the Stern operations manual controls physical construction, part
numbers, wiring, quantities, and device presence; pinned PinMAME controls controller generation,
public address topology, and mechanism-table position ranges; hash-pinned LibPinMAME harness runs of
the `simpprty` ROM settle the runtime facts no script binds; the retained VPX geometry supplies
normalized coordinates. The retained manual's `pdftotext` layer is unreliable for two independent
reasons -- most runs double every character, and the diagnostics chapter's own embedded font subset
additionally shifts character codes by a constant +29 with no ToUnicode correction -- so every table
used here was read from a rendered page and transcribed into
`external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/manual-transcription.md` and the
committed excerpts; the OCR text is a search index only and never an authority.

## Whitestar platform notes that generalize

This was the first Stern Whitestar (Sega/Stern `GEN_WS`, `src/wpc/se.c`) machine curated in this
project, so several address-space and normalization facts were re-derived from pinned source rather
than carried over from the WPC games curated earlier:

1. **Whitestar's switch matrix is sequential-by-column, not WPC's column-times-ten notation.**
   `se_m2sw(col, row) = col*8+(7-row)+1` in the driver's own 0-indexed terms; in 1-indexed printed-
   manual terms this is `address = (column-1)*8 + row`. Confirmed against every cell of this
   manual's own 8x8 SWITCH MATRIX GRID table (column 1 row 1 = public 1, column 8 row 8 = public 64).
   Lamps use the *opposite* axis order: the manual's own LAMP MATRIX GRID table is unambiguously
   row-major (`address = (row-1)*8 + column`), confirmed the same way across all 80 printed cells --
   do not assume switches and lamps share one addressing convention on this platform.
2. **No Whitestar game in the pinned source ever populates `wpc.invSw`, and `se.c` reads the
   switch matrix inverted.** `simpprtyGameData`'s positional aggregate initializer only sets the
   fields present in the literal; the trailing `wpc`/`simData`/`sxx` members stay zero, and `core.c`
   copies those zeros straight into the live switch-inversion mask. `se.c`'s `switch_r` returns
   `~core_getSwCol`, so public 1 is what the CPU reads as a closed matrix contact. A public opto that
   the script or the ROM treats as active at 1 therefore has a matrix-facing contact that rests
   open, whatever its beam does; see "Opto polarity" below.
3. **The dedicated-switch byte packs the Left/Right flipper button-and-EOS pairs plus a fifth
   button input, confirmed bit-for-bit from `se.c`'s own `dedswitch_r`.** `fls =
   core_revnyb(fls & 0x0f) | ((fls & 0x80)>>3)` read against `core.h`'s bit names yields DS-1->public
   84 (LL button), DS-2->83 (LL EOS), DS-3->82 (LR button), DS-4->81 (LR EOS), DS-5->88 (bit 0x80,
   which `core.h` names `CORE_SWULFLIPBUTBIT`). DS-6/7/8 are the ordinary Red/Green/Black service
   buttons at `SE_SWRED=-2`/`SE_SWGREEN=-1`/`SE_SWBLACK=0`. Flipper-column bits 0x10-0x40 (public
   85-87) are never read.
4. **An input PinMAME never synthesizes is not thereby unreachable.** `core.c`'s `locals.flipMask`
   includes the upper-flipper button bits only when `hw.flippers` sets `FLIP_SW(FLIP_Ux)`, and
   `simpprtyGameData.hw.flippers = FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)` does not, so PinMAME's own
   keyboard handling never writes public 88 (and `se.c`'s comment calls the bit "Not Used (Upper
   Flipper on some games!)"). But `core_updateSw` rewrites only the bits inside `flipMask` and keeps
   the rest, so a host that writes public 88 reaches the ROM unchanged -- and this ROM uses it. An
   earlier pass of this note claimed the ROM could never see 88; a harness run disproved it (see
   "Flipper buttons" below).
5. **The flipper-coil address remap is confirmed directly from the driver's own comment.**
   `se.c`'s `se_solenoid_w`: `/* move flipper power solenoids (L=15,R=16) to (R=45,L=47) */`. Raw
   solenoid addresses 15/16 are masked out of the public 9-16 group (`sols &= 0xffff3fff`);
   physical Q16 (RIGHT FLIPPER) surfaces at public power-phase 45 and canonical callback 46, physical
   Q15 (LEFT FLIPPER) at public power-phase 47 and canonical callback 48. Public 15 is then reused
   for PinMAME's synthetic fast-flip/game-on state, read from ROM RAM byte 0x04 -- but only for the
   `simpprty` driver itself: `se.c` matches the running driver's own name against `"simpprty"` in
   its first eight characters, so the seventeen clones leave public 15 at zero. A harness run of
   `simpprty` shows 15 rising to 1 when a game starts.
6. **`coreGlobals.nGI = 1` is set directly in `se.c`**, so Whitestar publishes exactly one aggregate
   GI channel regardless of how many separately fused physical illumination branches a machine's own
   wiring diagram shows. This manual's General Illumination Circuit Detailed Wiring Diagram (PDF 121,
   printed 103) shows one relay closing four fused branches simultaneously, which is the same
   single-relay design PinMAME models.
7. **`hw.lampCol` counts every lamp column beyond the eighth, including printed ones.** PinMAME
   publishes `64 + lampCol*8` lamps. This driver's `lampCol = 4` covers the printed rows 9-10
   (public 65-80, the aux lamp strobe) *and* two more columns, public 81-96, which only `se.c`'s
   `gilamp_w` fills from CPU ports `$3406`/`$3407`. An earlier pass counted the four columns as
   81-112; the range is 81-96.

## Address topology for this game specifically

- Switches: matrix 1-64 (two "NOT USED" gray-shaded positions, 27 and 28), dedicated -3/-2/-1/0,
  81-84 and 88, unused flipper-column holes 85-87, CPU DIP 1-8 (5-bit country selector, bits 6-8
  unused padding).
- Solenoids: physical drivers 1-14 and 17-32 retain their printed numbers; raw 15/16 carry no coil
  (the two lower flipper coils surface at 45-48), public 15 is the fast-flip/game-on state on the
  `simpprty` driver and 16 is unused; the Solenoid Expander Auxiliary board
  (`SE_BOARDID_520_5068_01`) publishes three UK-only up/down-post outputs at 33-35 and leaves 36
  unused; 37-44 are reserved WPC-family compatibility holes; 49 is the simulator-only shooter channel
  and 50 is reserved. Ten of the thirty-two main-board positions are flashers (21-23, 25-29, 31, 32,
  confirmed by the manual's own "In Test Flash Lamps Menu... This Game: Q21-Q23, Q25-Q29, Q31-Q32"
  note); position 24 ("Optional Coil") is explicitly optional factory-fit hardware for a coin meter,
  token dispenser, or knocker, and the ROM pulses it once per inserted coin.
- Lamps: 8x10 matrix 1-80 (two "NOT USED" positions, 71-72); lamp 32 (Tournament Button) is optional,
  gated behind the Optional Tournament Kit, and has no `l32` object anywhere in the retained script's
  own lamp-fade sequence at all. Public 81-96 are enumerated as virtual outputs with unknown
  availability; see "Unresolved: lamps 81-96" below.
- GI: one aggregate channel, public address 0.

## Ball path: trough, saucers, and VUKs

The manual's switch-location drawing shows the trough rising from left to right: 5-Ball Trough #1
(switch 10) at the far left end, then 11, 12 and 13, and a single stamp `14:15` at the right-hand exit
end beside the shooter lane (16). Switch 14, the 5-Ball Trough VUK Opto, sees the ball waiting at the
up-kicker; switch 15, the 5-Ball Stacking Opto, sits at the same exit location above it. The retained
script's `bsTrough.InitSw 0,14,13,12,11,10,0,0` agrees: 14 is the exit position the kicker empties
and 10 the last to fill. The shared `cvpmBallStack` helper class manages ball positions internally
rather than exposing five playfield trigger objects, so all five (plus the stacking opto) are
documented projections onto the trough's own release kicker (`BallRelease`). `SolRelease`
(solenoid 1) fires `bsTrough.ExitSol_On` and also pulses switch 15 as the kicked ball passes the
stacking beam. Switches 14 and 15 share one Transmitter/Receiver opto PC-board part pair per the
manual's own "Sw. 14 & 15 Part Note" -- the only two switches this manual identifies as opto
construction anywhere in the document.

Three simple saucer/VUK mechanisms round out the ball-management inventory: the Itchy & Scratchy
Eject VUK (switch 20, solenoid 5), the Upper Right saucer (switch 24, solenoid 19), and the Upper
Left VUK (switch 55, solenoid 6), each confirmed by the matching `cvpmBallStack.InitSaucer`/`InitSw`
call in the retained script.

## Opto polarity: settled by the script and the ROM

PinMAME normalizes nothing on this driver (point 2 above), so the public state of 14 and 15 is
exactly what a recreation asserts. Both are settled by observation rather than by argument.

- **Switch 14** is the exit position of `bsTrough`. `core.vbs` 3.61's `cvpmBallStack.SetSw` writes
  `Controller.Switch(14) = True` whenever a ball occupies that position and `KickOut` clears it
  when the ball leaves, so the known-working table holds 14 at 1 while a ball waits at the
  up-kicker. That library copy is retained under the review artifacts with its SHA-256.
- **Switch 15** is asserted by the script only as a pulse on each up-kicker firing, so its sense was
  asked of the ROM directly. Hash-pinned LibPinMAME runs of `simpprty`
  (`evidence/runtime/whitestar/simpsons-pinball-party-stacking-opto.json`) with five balls held on
  10-14 show the ROM acting on public 1 and quiet at 0: held at 1 from power-up, or raised to 1 in
  attract mode, it fires the trough up-kicker (public 1) -- six times, because the harness never lets
  a ball move -- and then the auto launch (public 2) once; 0 at boot and a fall back to 0 draw no coil
  at all. That 1 means a ball blocking the stacking beam is an inference, corroborated by switch 14
  on the same board pair.

`normally_closed` is false on both: the opto boards' matrix-facing contact rests open and closes while
a ball blocks the beam, exactly like the mechanical switches. Hold 14 and 15 at 0 at rest, drive each
to 1 only while a ball blocks its beam, and never invert them. This settled
`conflict.whitestar-invsw-never-populated`, which was removed.

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

## Flipper buttons: five flipper coils from two cabinet buttons

The lower flipper pair (printed coils #15 Left, #16 Right) is the only flipper hardware PinMAME's
synthesized flipper subsystem knows about, remapped to public 45-48 and read from dedicated switches
DS-1..DS-4 (public 84/83/82/81). Three more flipper coils are ordinary numbered solenoids: 12 "UPF
Left Flipper" and 13 "UPF Right Flipper" on the upper mini-playfield, and 14 "Top Right Flipper" on
the main playfield.

The right cabinet button is a doubled switch. The manual prints part 180-5164-00 *Doubled* for both
DS-3 (Right Flipper Button) and DS-5 (Upper Rt. Flipper Button, GRY-GRN to CN6-P7), and its
switch-location drawing stamps DS-3 and DS-5 on the same right button; the left button carries DS-1
alone. So one press of the right button closes both 82 and 88.

A hash-pinned harness run with a game in progress
(`evidence/runtime/whitestar/simpsons-pinball-party-flipper-buttons.json`, keyboard handling off, so
every input is a host write) shows what the ROM does with each input:

| Input held alone | Solenoids the ROM energises |
| --- | --- |
| DS-1, public 84 (left button) | 47/48 (lower left) and 12 (UPF left) |
| DS-3, public 82 (right button, first contact) | 45/46 (lower right) only |
| DS-5, public 88 (right button, second contact) | 13 (UPF right) and 14 (top right) only |
| 82 and 88 together | 13, 14, 45 and 46 |

**A recreation must drive 82 and 88 together from its right flipper button.** Driving 82 alone, as
PinMAME's own keyboard path does, leaves both upper-right flippers dead. The retained table works
around exactly that: its `SolRFlipper` (the lower-right callback on public 46) also rotates solenoid
14's object (`RightFlipper2`) and solenoid 13's (`TopRightFlipper`) beside their own callbacks.

This removed `conflict.upper-flipper-button-not-read`. It never described incompatible claims about
the machine: the manual's fitted input and an emulator that does not synthesize it are two compatible
facts, and the second was also mis-stated -- PinMAME delivers a host write to 88. Both facts now live
on switch 88 and solenoids 12-14.

## Jet bumpers: object names do not match printed sides

Three jet bumpers, and the retained script's own object names are a trap: `Bumper1_Hit` pulses
switch 50 (Right Bumper) and fires solenoid 10; `Bumper2_Hit` pulses switch 51 (Bottom Bumper) and
fires solenoid 11; `Bumper3_Hit` pulses switch 49 (Left Bumper) and fires solenoid 9 -- i.e. object
number order (1, 2, 3) does **not** match printed side order (Left, Right, Bottom) or address order
(49, 50, 51) at all. This was confirmed two ways: directly from the script's own
`Controller.Switch`/`vpmTimer.PulseSw` calls, and geometrically -- `Bumper3` sits at the lowest x
(leftmost), `Bumper1` at the highest x (rightmost), and `Bumper2` at the highest y (frontmost, i.e.
"bottom" of the nest) -- both independently agreeing with the printed Left/Right/Bottom identity.

## Lamps 73-80: the LED mode sign

Lamps 73-80 (Duffman, Homer's Day, Willie's Woes, Wiggum vs Snake, Bart's Day, Krusty's Last Stand,
Stop The Monorail, Alien Invasion) are the LEDs of the mode sign: LED PCB (Mode Signifier)
520-5225-00, bolted through bracket 535-9232-00 to the back panel next to the TV and read through the
screened mode plastic (manual PDF 82, 114 and 170, excerpted in
`evidence/excerpts/stern.the-simpsons-pinball-party.2003/led-mode-sign.md`). The lamp-location page
stamps them in one column "on Sign" at the rear of the playfield, above it, and the manual's LED test
note (PDF 42) calls them lamps 73-80. They are ordinary lamp-matrix positions on row 10 (J12-P11,
Q42), green LEDs L1-L7 for 73-79 and two red LEDs, L8 at the bottom-left and L9 at the bottom-right,
for 80.

Two earlier readings were wrong and are corrected here. The lamp page's footnote names board
520-5219-00, but the same manual gives that number to the TV's Color Dot Display; the three specific
pages agree on 520-5225-00, so the footnote is a typo rather than a second device. And these lamps
are not the TV's 14x10 dot matrix, which pinned PinMAME publishes as the separate mini-DMD display;
the retained script's `UpdateLeds` reads that display from `Controller.ChangedLEDs`, and the empty
`LEDY`/`LEDG`/`LEDR` collections it hides at start-up were never bound to lamps 73-80. The script
drives 73-80 with `NFadeObj` onto eight primitives `l73`-`l80` (its own name for them is "Moes Sign").

**Placement.** The sign is vertical and faces the player, so L1-L7 stack in one column and project
onto one playfield point. Each of lamps 73-79 is placed at its own primitive's x/y (about 0.5763,
0.0345); the primitives differ only in height, from z 305 for lamp 73 down in 20-unit steps, which
matches the manual's top-to-bottom order. That is one position per LED, not an average. Lamp 80 is
two LEDs and every retained table models one object, so it carries no spatial key: L9's position is
the one spatial gap left on this machine. Two further local tables were copied, extracted and checked
(`Simpsons Pinball Party, The (Stern 2003).vpx` and `The Simpsons Pinball Party (Stern 2003).vpx`,
hashes in the spatial report); both share the retained table's script base and place `l73`-`l80`
identically, so they add no independent geometry.

## General illumination

One aggregate PinMAME GI channel (public address 0). The manual's wiring diagram shows one relay
closing four separately-fused branches (F24 backpanel/10 bulbs, F25 left playfield plus right return
lane/11 #44 + 1 #555, F26 upper mini-playfield plus spotlights plus coin door/7 #44 + 5 #555 plus
coin-door bulbs, F27 right playfield/12 #44), all switched together -- matching PinMAME's
single-channel model with no script-vs-manual disagreement. The manual's own bulb counts are printed
"may change during production", so the retained table's own `GI` collection (37 `GI_N` Light objects
plus 5 `spotlightright*` objects, 42 members total, toggled together by the script's `UpdateGI`) is
used as the placement set rather than a hand count from the diagram.

## Unresolved: lamps 81-96

`simpprtyGameData.hw.lampCol = 4` makes PinMAME publish public lamps 1-96: `se.c` sets `nLamps = 64 +
4*8`, and `vp_getChangedLamps` scans eight plus four columns. The printed 8x10 matrix fills 1-80.
Public 81-88 and 89-96 are `coreGlobals.lampMatrix[10]` and `[11]`, which only `se.c`'s `gilamp_w`
writes, copying whatever the CPU stores at ports `$3406`/`$3407` (the memory map's own comment: "GI
lamps on Simpsons?"). In LibPinMAME's physical-output mode nothing writes those outputs for this
driver. No lamp circuit exists for them: the manual's lamp matrix has exactly eight drive columns and
ten return rows, all accounted for by 1-80.

Whether the ROM ever writes those ports is not settled. Three hash-pinned harness runs (boot, attract
mode, and a started game with every flipper input exercised, about 210 s in all) never saw 81-96
change. That does not prove the ROM never writes them, so the sixteen addresses are enumerated as virtual outputs with
`availability: unknown` and `output_semantics` stays in `coverage.missing`. Resolution path: static
analysis of the `simpprty` CPU ROM for every write that can reach `$3406-$3407`, or a harness run of
the ROM's own lamp tests watching 81-96.

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

- Build the five-ball trough with its release kicker (14 is the exit ball, 10 the far end, 15 the
  stacking beam above 14), the three-target drop bank with its reset and trip solenoids, the Couch
  lock (three stacked positions plus entry gate), the TV lock post, the incrementally-animated Garage
  door, the Homer Head toy, three saucer/VUK kickers, two slingshots, three jet bumpers (mind the
  non-matching object-to-address numbering above), and five flipper coils.
- Drive switches 14 and 15 at 1 only while a ball blocks their beam; never invert them.
- Never drive public 81 or 83: PinMAME's end-of-stroke simulation rewrites them every frame from
  the lower flipper coils.
- Wire the right flipper button to both public 82 and public 88. The ROM fires the lower right flipper
  from 82 and the upper-mini-playfield right flipper (13) and top right flipper (14) from 88; the left
  button (84) fires the lower left flipper and the upper-mini-playfield left flipper (12).
- Treat solenoids 15/16 as non-coils; bind the two lower flipper coils at 45/46 (right) and 47/48
  (left) only, one physical coil per side. On the `simpprty` driver, public 15 is the fast-flip
  game-on state.
- Place the mode-sign LEDs 73-79 on the vertical sign on the back panel next to the TV, top to
  bottom in address order, and lamp 80 as two red LEDs at the sign's bottom corners. Do not model
  them as the TV's dot matrix.
- Do not invent lamps for public 81-96; nothing physical is wired there.

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
- `vpm-script-library.core-vbs-3-61`: the VPinMAME `core.vbs` 3.61 script library that defines
  `cvpmBallStack`, SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.
- `runtime.simpsons-pinball-party.stacking-opto` and `runtime.simpsons-pinball-party.flipper-buttons`:
  hash-pinned LibPinMAME harness runs of `simpprty` with the pinned `pinmame64.dll` (SHA-256
  `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c`, built from `8371478`).
- `pinmame.core.4ec52ff0ac13`: `src/wpc/segames.c`, `src/wpc/se.c`, `src/wpc/se.h`, and the shared
  `src/wpc/core.c`/`core.h` flipper/switch/lamp handling at the revision the record was first
  curated against.
- `pinmame.core.8371478a7640`: the same files plus `src/wpc/vpintf.c` at the operational pinned
  baseline, for the switch read path, the flipper-column mask, the fast-flip state and the 1-96 lamp
  range.
