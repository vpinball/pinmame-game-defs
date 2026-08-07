# Creature from the Black Lagoon (Bally, 1992)

Coverage: **partial - physical I/O inventory, WPC-Fliptronic bindings, mechanism causality, driver-variant boundary, and recreation behavior are validated; spatial placement and physical wiring are conflicted pending several genuinely unresolved gaps documented below**

## Identity and evidence precedence

This is the Bally WPC-Fliptronic physical product released 1992/93, IPDB 588. It covers the eight-driver
`cftbl_*` clone tree: `cftbl_l4` (parent, production L-4), `cftbl_l4c` (2020 community "L-4C Competition +
LED Ghost MOD"), `cftbl_d4`/`cftbl_d3`/`cftbl_d2` (LED Ghost Fix revisions), `cftbl_l3`/`cftbl_l2` (earlier
firmware), and `cftbl_p3` (P-3 Prototype, SP-1, 1992, with an early sound ROM). Every one of these is a
ROM revision for the same physical machine.

Evidence precedence for this definition: the retained known-working script is runtime and
mechanism-causality ground truth; the Bally operations manual controls physical construction, part
numbers, wiring, polarity, quantities, and device presence; pinned PinMAME controls controller
generation, public address topology, and driver-declared hardware options; the retained VPX geometry
supplies normalized coordinates. The retained manual PDF carries a real (Adobe Paper Capture) OCR text
layer, but it garbles every multi-column table used here, so every printed table was read from 300 dpi
renders and transcribed into `evidence/excerpts/bally.creature-from-the-black-lagoon.1992/`, indexed by
`external:pinmame-review-artifacts/creature/manual-transcription.md`; the OCR text is a search index
only and never an authority.

**This retained extraction is the smallest curated in the project to date (856 files).** Several
documented devices have no matching VPX object at all; this record stays honestly `partial` rather than
reaching for projections that would misrepresent the table's actual fidelity.

## Controller platform and address topology

`GEN_WPCFLIPTRON` (`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`) with `wpc_dispDMD`. The controller profile
is `pinmame.wpc-fliptronic`, reused unchanged.

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row (40 used, 24 "Not
  Used"), Fliptronic 111-118. `cftblGameData`'s inverted-switch mask
  `{0x00,0x10,0x00,0xc8,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}` normalizes column 1 bit 4 (address 15)
  and column 3 bits 3/6/7 (addresses 34, 37, 38).
- Solenoids: physical drivers 1-28 with no LPDC board (this generation has no 37-44 duplication range;
  see the controller profile). No custom solenoids (`custSol = 0`).
- Lamps: 8x8 matrix 11-88, every position populated (no "Not Used" lamp address), **plus** a real
  auxiliary column at 91-98 that the manual never itemizes by individual bulb name (see the Sequential
  G.I. mechanism below). `cftblGameData` declares `lampCol = 1`.
- GI: five strings on public addresses 0-4, of which address 3 has no bound playfield emitter in this
  recreation.

## Opto polarity: two true optos, two mechanically inverted switches

Unlike every other WPC-Fliptronic/WPC-95 machine curated in this project so far, this manual's switch-
matrix wiring page (3-2) carries **no shaded-cell opto legend at all** -- every cell is plain text. Opto
construction instead comes from the Switch Locations parts list's two-row LED-plus-phototransistor
disclosure (A-14231 LED over A-14232 Trans.), which appears at exactly two addresses: **34** (Right
Popper) and **37** (Lower Right Popper). PinMAME's inverted-switch mask normalizes those two, **plus two
more that carry no opto-construction marker at all**: 15 (Top Left Rollover, printed part
`5647-12693-19`, an ordinary leaf switch) and 38 (Ramp Up/Down, printed part `5647-12693-11`, likewise
ordinary). Neither is a manual-vs-emulator conflict: the retained script's own `sw15_Hit`/`sw15_Unhit`
handlers invert the usual hit/unhit polarity (clearing the switch on Hit, setting it on UnHit -- the
opposite of every other rollover in the file), and switch 38 is a ramp-position microswitch whose public
state pinned `cftbl_handleMech` sets purely from the motor's own commanded direction
(`core_setSw(swRampUpDown, locals.creaturerampPos)`), never from a Hit event. Both are recorded
`normally_closed = true` on independent corroborating evidence, not because they carry the manual's opto
marker.

**Lesson for future WPC-Fliptronic/WPC-95 curation:** PinMAME's inverted-switch mask normalizes both true
optos and ordinary normally-closed mechanical switches identically. Do not assume every masked address is
an opto; check the manual's own LED/Trans (or shaded-cell) construction marker specifically, and use the
retained script's hit/unhit handling or a mechanism's own position-sensor logic to corroborate polarity
for masked addresses that carry no opto-construction evidence.

## Fliptronic block: an unresolved same-manual disagreement (`conflict.upper-flipper-switches-unconfirmed-fitment`)

`cftblGameData` declares `FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L)`: switch bits for both lower and
upper flippers, but solenoid bits for lower flippers only (no upper flipper coils fitted -- the
Solenoid/Flasher Locations and Table pages print exactly two flipper coils, FL-15411 Lower Left and
FL-11629 Lower Right, and nothing at printed addresses 33-36).

The Switch Locations parts list (printed 2-41) lists only F1-F4 (Right Flipper EOS/Opto Board, Left
Flipper EOS/Opto Board) with real part numbers, and simply omits F5-F8 -- not even as a "Not Used" row,
unlike every genuinely unfitted matrix range on the same page. But the Switch Matrix wiring page
(printed 3-2), a different page of the same manual, prints real, distinct wire colors and Fliptronic-II-
board connector pins for **all eight** F1-F8 positions, labeling F5-F8 "Upper Right/Left Flipper End of
Stroke/Opto" with no "Not Used" marking anywhere on that page -- the identical treatment given to the
fitted F1-F4 positions. The retained known-working script makes no `Controller.Switch` call anywhere for
addresses 111-118, so it supplies no corroborating runtime evidence either way.

Two pages of the same primary source disagree on whether this hardware is fitted, and this is not a case
where majority-evidence or the retained script settles it (unlike, for example, Twilight Zone's
slingshot-naming case). Switches 115-118 are recorded with **neither** a location **nor** a
`not_applicable` spatial record -- either would assert something not yet established -- and the coverage
gap is named explicitly rather than guessed at.

## Trough, outhole, and shooter lane

Three balls rest on plain leaf switches 56 (Right Trough, nearest the release), 57 (Center Trough), and
58 (Left Trough, drain entrance) -- a simpler three-position trough than the four/five-position optical
troughs on later WPC-Fliptronic and WPC-95 machines. The retained script's `UpdateTroughTimer` cascades
balls toward the release end whenever a downstream position empties, and solenoid 4 (`ReleaseBall`) kicks
the ball at 56 out to the shooter lane. A drained ball rests on outhole switch 55 and solenoid 12
(`SolOuthole`) kicks it into the trough. There is no auto-plunger: the retained extraction includes a
single manual pull-`Plunger` primitive, and switch 66 (Shooter) simply senses the ball resting in the
lane before the player plunges it.

## Three entry holes, one shared subway tunnel

Pinned `cftbl_stateDef` routes both "Left Subway" (switch 16, the driver's own key-help comment calls it
"K-I-S-S Hole") and "Center Subway" (switch 17, "Snackbar Hole") to the identical `stLowRPopper` ball
state -- both holes feed an internal tunnel that exits through the Lower Right Popper (switch 37,
solenoid 3). "Right Subway" (the F-I-L-M hole) is a separate, standalone kickback hole: it exits through
the Top Right Popper (switch 34, solenoid 1) directly, the same physical hole the ball entered.

## Creature Ramp: motorized up/down ramp

A DC gearmotor (assembly A-16042) raises and lowers the curly "Creature Ramp" between an Up position (the
ball climbs it) and a Down position (the ball instead takes the ordinary left ramp). Solenoid 23 drives it
up, solenoid 26 drives it down, and switch 38 senses the commanded position (see the polarity note above).
Pinned `cftbl_stateDef`'s `stLRamp` hook state reads `core_getSw(swRampUpDown)` to decide which path a
ball entering the left-ramp mouth (switch 36) takes. Switches 35 (Right Ramp Enter), 61 (Right Ramp
Exit), 62 (Left Ramp Exit), and 64 (Upper Ramp) sense the remaining entry/exit points around the two ramp
paths.

## Sequential G.I.: the curly-ramp chase lights (`WPC_CFTBL` custom hardware)

This is the standout feature unique to this driver. Pinned `wpc.h` defines `WPC_CFTBL = 0x01`,
documented as "chase light 2 bit decoder from solenoid #3 output, wired through triacs to 2 GI outputs,
leading to 8 additional PWM controlled GI", and `cftblGameData` sets this bit in `gameSpecific1`.

The mechanism has four parts, and the manual prints two pairs of them under the **same** name because
they share one physical board (A-15541):

- **Solenoids 20 and 24** are not coils. They are the board's own 2-bit decoder address-select lines,
  driven from an entirely different connector pair (`J118-2`/`Q36`/`J126-4` for 20, `Q32`/`J126-8` for
  24) than the GI power buses below, and neither drives a playfield bulb by itself. This curation
  overrides their `kind` to `control_signal` despite the manual's own inconsistent "Solenoid Type"
  column (printing "Flasher" for 20 but "Low Power" for 24, an internal disagreement for what is
  functionally the identical role).
- **GI addresses 0 and 3** ("Sequential G.I. #1"/"#2") are the true power buses, wired to a genuinely
  different connector pair (`J120-1`/`Q18`/`J120-7` for GI 0, `J120-5`/`Q15`/`J120-10` for GI 3).
- Pinned `wpc.c`'s `WPC_SOLENOID3`/`WPC_GILAMPS` handling computes `chase_2b` from solenoids 20/24's
  pulsed state and `chase_gi` from whether GI triacs 0 and 3 are conducting, then writes the selected
  8-bit pattern directly into `coreGlobals.lampMatrix[8]` -- the public lamp matrix's 9th row. **This
  means public lamp addresses 91-98 are real, individually addressable outputs for the 8 physical
  curly-ramp chase bulbs**, computed by the emulator's hardware model rather than driven through the
  ordinary lamp-strobe scan, and the manual never itemizes them by individual bulb name (it only names
  the assembly "Sequential G.I. #1/#2" as a whole).

The retained VPX table does not model this faithfully: it never reads `Controller.Lamp` for any of
91-98. Instead its own `chaselights` collection (32 `swirlramplight` Light objects -- four times the
true 8-bulb count) cycles through a self-contained internal timer (`swirlramplight1_Timer`) keyed only
to GI address 0's on/off state, approximating rather than reproducing the true decoder-selected pattern.
The table's own commented-out `SeqGI1`/`SeqGI2` handlers (bound to solenoids 20/24) carry the author's own
note: `'does not work properly with rom !!! so I did not use this, but for reference`. GI address 3 has
no bound emitter collection at all (`FadeGI 203` runs but no matching `UpdateGIObjects` call exists), so
it has no playfield placement in this recreation.

**Lesson for future curation:** a `lampCol` declaration does not always mean an ordinary auxiliary lamp
column with printed per-bulb names. Check the driver's `gameSpecific1`/`gameSpecific2` custom-hardware
bits (`WPC_CFTBL` here) before assuming a lamp-matrix column follows the standard strobe-scan
convention -- this one is entirely computed inside the core's own solenoid/GI handling.

## The hologram: cabinet-mounted illusion

A three-part cabinet-mounted mechanism creates the machine's signature effect -- a hologram of the
Creature that appears to float above the playfield. A 48VAC push motor (solenoid 21, "Hologram Push
Motor") positions a mechanism under the playfield; a #1156 lamp (solenoid 28, "Hologram Lamp")
illuminates a hidden image; and a 48VAC spinning mirror motor (solenoid 27, "Creature Mirror Motor")
reflects it up through the playfield glass. Solenoids 27 and 28 are both printed "Δ Located in cabinet
bottom" on the Solenoid/Flasher Locations page -- genuinely cabinet hardware, not playfield hardware,
even though the visible effect reads as a playfield feature. The retained script's `HoloLamp` handler
(bound to solenoid 28) sets a `holoState` flag and makes a `creature` Flasher object visible; a separate
`reflectionTrigger` disables ball-reflection rendering while the hologram is active so a mirrored ball
does not break the illusion. A distinct backbox-insert-only flasher (solenoid 11, "Creature Flasher")
lights a companion insert graphic and is not part of the hologram projection itself -- it is the only
solenoid-table item that prints an Insert connection with no Playfield connection at all.

## Other mechanisms

Three jet bumpers (Left 45/coil 13, Right 46/coil 14, Bottom 33/coil 15) and two slingshots (Left
47/coil 6, Right 48/coil 5) are standard WPC devices. The four-letter P-A-I-D rollover lane (25-28) and
four Snackbar standup targets (Cola 41, Hot Dog 42, Popcorn 43, Ice Cream 44) are simple award features
with no custom mechanism logic. The Creature Bowl orbit loop passes a single switch (65) up to four times
per lap; pinned `cftbl_stateDef` chains four "In Bowl Loop" states and a final "Creature Bowl" state, all
keyed on the same switch, counting passes rather than sensing four distinct physical positions. Switch 18
(Center Shot, feeding the "Move Your Car" lamp/feature) has a script handler (`Sub sw18_Hit`) but no
matching table object anywhere in the retained extraction -- unreachable and spatially unresolved in this
specific recreation.

## Lamps, flashers, and general illumination

All 64 lamp-matrix positions are populated; unlike the switch matrix, there is no "Not Used" lamp
address. Addresses 71-78 spell the backbox "CREATURE" header (printed "*Located on backbox insert"
individually on each letter); the retained table's matching `Light.L71`-`L78` objects independently
confirm this, sitting at normalized x outside [0,1] (behind the rear/backglass edge). Lamp 88 (Start
Button) is the cabinet pushbutton's own illumination.

Six solenoid-driven flashers (2 Left Subway Enter, 9 Back Flashers, 16 Right Popper Slide, 18 Right
Ramp, 19 Left Ramp, and, among the ones with a bound object, 8/10/11/17/22) are real fitted circuits per
the manual, but only five of them (8, 10, 11, 17, 22) have any matching VPX object at all
(`FlSol08`/`FlSol10`/`FlSol11`/`FlSol17`/`FlSol22`), and every one of those five sits at normalized y well
outside [0,1] -- reading as the table's backbox/insert-panel companion bulb rather than the playfield
dome the manual documents. None of the six is given a fabricated coordinate; all are left spatially
unresolved.

## Author construction checklist

- Build the three-position trough with the drain at Left Trough, the manual pull-plunger shooter lane,
  both slingshots, three jet bumpers, the shared KISS/Snackbar subway tunnel exiting at the Lower Right
  Popper, the standalone F-I-L-M top-right-popper kickback, the motorized up/down Creature Ramp, the
  P-A-I-D rollover lane, the four Snackbar standup targets, and the Creature Bowl orbit loop.
- Preserve opto/NC polarity for 15, 34, 37, and 38; 34/37 are true LED/Trans optos, 15/38 are mechanically
  normally-closed switches corroborated by script/mechanism logic rather than a printed opto marker.
- Build the Sequential G.I. chase-light mechanism as real emulator-computed hardware, not an ordinary lamp
  column: GI 0/3 are power buses, solenoids 20/24 are address-select lines, and lamps 91-98 are the eight
  individually addressable chase bulbs the true hardware exposes (even though no retained VPX table reads
  them yet).
- Build the three-part cabinet-mounted hologram mechanism (push motor, lamp, spinning mirror motor) as
  genuinely non-playfield hardware.
- Treat Fliptronic switches 115-118 as unconfirmed rather than either fitted or unfitted until better
  evidence resolves `conflict.upper-flipper-switches-unconfirmed-fitment`.
- Do not invent a playfield location for switch 18, GI address 3, lamps 91-98, or the six unbound
  flasher solenoids named above; the retained table's own evidence does not reach that far.

## Sources

- `manual.bally.creature-from-the-black-lagoon.1992`: Bally Creature from the Black Lagoon operations
  manual, SHA-256 `d84d28a807505339f57676e0222adc6cc6fe7bef7371d31f9a9076ec33021d97`.
- `manual-support.bally.creature-from-the-black-lagoon.1992`: retained human transcription index, SHA-256
  `5c30e18c830a9f2192d250bdc9ed178a4d7216a47cf637429776e098b5d5ec72`.
- `vpx-script.cftbl-source`: retained known-working embedded script, SHA-256
  `e6393a87a33c1e53e3b32c3cff2af19dc14b2b4c8764f71dbb57736cadb98df8`, binding `cftbl_l4`.
- `vpx-table.cftbl-source`: retained table, SHA-256
  `0527ebf5d66a6fa45d40a1ce2bdf1f395af7a3d77aed9bd4eb437399ee0bbb34`, bounds
  `left=0 top=0 right=964 bottom=2162`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/cftbl.c` and the WPC-Fliptronic/`WPC_CFTBL`
  handling in `src/wpc/wpc.c`/`src/wpc/wpc.h` at the pinned revision.
