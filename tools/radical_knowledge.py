"""Deterministic recreation notes for the two physical Radical editions."""
from __future__ import annotations


def _paragraphs(text: str) -> str:
	"""Keep one Markdown paragraph per line; source wrapping is editorial only."""
	return "\n\n".join(" ".join(block.splitlines()) for block in text.strip().split("\n\n")) + "\n"


def render_knowledge(prototype: bool = False) -> str:
	title = "Radical! — P-3 physical prototype" if prototype else "Radical! — production"
	identity = (
		"This record contains only `radcl_p3`. The prototype adds a ball popper and upper sling; it is a physical edition, "
		"not merely a production ROM label. The same IPDB title page 1904 covers the family, but the retained OPDB snapshot "
		"has no separately verified prototype identity, so `identity` stays missing. The exact production OPDB ID is not copied here."
		if prototype else
		"Production Bally Radical! is model 2015, released 1990, on System 11C. IPDB 1904 and OPDB `G59ZY-MD8p7` refer to this title. "
		"This record contains `radcl_l1`, German `radcl_g1` and competition `radcl_l1c`; `radcl_p3` belongs to the separate physical prototype record."
	)
	edition = (
		"P-3 calls switch 16 BALL POPPER, switch 28 ADV BONUS X, switch 49 TOP SLING, output 3 BALL POPPER and output 15 TOP SLING. "
		"The April handbook still depicts this hardware. IPDB photos 31926/31927 visibly corroborate the extra sling and popper. "
		"The VPW and later JPSalas tables supply both receiver and remote return geometry. Their default production ROM and table "
		"options do not prove prototype firmware timing; use the P-3 driver with the fitted mechanisms."
		if prototype else
		"L-1 and German LG-1 name switch 16 SNAKE RUN, switch 28 SPOT LETTER, switch 49 NOT USED, and outputs 3/15 NOT USED. "
		"The production standup target replaces the prototype ball receiver and the top sling is absent. Its exact target contact "
		"part/construction has not been established by a production assembly sheet; the public closure and its runtime meaning are known. "
		"The retained manual's prototype parts are preserved literally rather than assigned to the production target."
	)
	return _paragraphs(f"""# {title}

Coverage: **partial**. Spatial observations are usable research, not an author-ready socket survey.

## Identity and variants

{identity}

{edition}

The root/clone relationships and exact ROM member identities come from pinned PinMAME
`46e1a01a0f73dc5ce163d98db1ae435883ecc450`, not a ROM zip's filename. All four drivers share
`radclGameData`: `GEN_S11C`, `disp16oneline`, `FLIP_SWNO(58,57)`, mux relay 12 and `S11_MUXSW2`.
Prototype U4/U20 sound ROMs differ; the display/CPU/audio board generation remains System 11C.
The 2018 competition year is firmware provenance, not a new physical release. German and
competition firmware have `identical` physical compatibility with production: language and
software fixes do not alter fitted hardware, controller generation, sound system or displays.

The competition driver's loaded program is patch **aa9e**, not the earlier commented 8351 patch.
Compatibility is inferred from the firmware author's later software-only update, an owner's
earlier physical installation and unchanged pinned routing. `competition-author.md` preserves
the exact posts and change categories. The exact patched archive was unavailable for a service
replay; no trace of it is claimed.

## Controller contract and contacts

The definition enumerates all public switches **-7..-4, 1..64, 81..88**, the country jumper at DIP 0,
all solenoid addresses **1..64**, and lamps **1..64**. The normalizer is sequential column-major,
not WPC column-times-ten numbering. System 11C reads the matrix uninverted and this game has no
`invSw` mask. Working script closures and the ROM's named Switch Levels responses establish
public 1 as active for these inputs. The six target-bank optos are therefore normally open at the
matrix contact; this conclusion is not inferred from whether a beam is clear or blocked.

Switch 2 is **virtual A/C relay feedback**: PinMAME overwrites it from relay 12 even though the
manual prints Not Used. Switch 20 is a **physical bowtie microswitch**, part of B-13629/C-13809;
the old legacy note that called it nonphysical was wrong. Cabinet flipper buttons are 82/84.
PinMAME copies them into 57/58 on each update, so drive 82/84. A repeated host pulse on 57/58 can
race that copy and is not an appropriate consumer interface. Positions 81/83/85..88 are enumerated
but the game's read path cannot consume them. Cabinet service inputs are Advance (-7), maintained
Auto-Up/Manual-Down (-6), CPU diagnostic (-5) and sound diagnostic (-4); hold Auto-Up during normal
play probes. The country jumper selects the USA/Germany configuration; it is not a playfield DIP bank.
The center coin provision is optional because the handbook depicts both two- and three-slot doors.

The score contact for a sling is SW-1A-120. The inventory also names a separate SW-1A-114 kick
contact on the same assembly; it is not another matrix address. The physical leaf pairs belong
to the mechanism topology. No host-addressable EOS input is invented for cabinet-wired flippers.

## Trough, outhole and ball supply

Normal operation uses **two balls**. Switch 10 is the outhole, 11 the right/first trough position,
12 the left/second trough position and 14 the shooter lane. `InitSw 10,11,12,0,0,0,0,0` has an
entry/outhole argument followed by two trough positions; it does not describe three trough sensors.
Coil 1 transfers a drained ball into the trough; coil 2 feeds the shooter. These coils move balls,
not the sensor actuators directly. The manual warns that a missing-ball report can result from
trough 11/12 or shooter 14 and directs the operator to return a found ball through the outhole.

The virtual table starts with two balls in the trough and an empty lock. A recreation must keep
ball occupation distinct from the contact's normal electrical state and answer the ROM with
the positions the balls actually occupy. Its `Drain` kicker is a disposal helper near the apron,
not the physical outhole's coordinate. Outhole/trough locations remain unmeasured rather than
being copied from that helper. `BallRelease` is an observed feed-effect projection only.

## Visible lock

Lane 38 leads to the two-position lock: 40 is the front position and 39 is behind it.
The script's `cvpmVLock` order is `[40,39]`; its `sw40k`/`sw39k` objects model ball routing.
One physical actuator, coil 8, operates the B-11395-1 locker. It is a **release-all** mechanism;
the firmware author says it cannot pace the held balls independently, including with unmodified
firmware. Do not reconstruct two separately controlled eject coils from the two VPX kicker objects.

Ball possession and re-locking depend on occupancy/timing. A ghost closure, a ball jumping a
switch, a jam or a double release can disturb the game's ball count. The competition patch
specifically changes lock accounting and recovery from such states. The library's exit force 21
and direction 0 are table tuning, not factory measurements or a guaranteed physical kickout
direction. The two sensor placements are observed projections onto their own ball locations.

## Targets, diverters and kickback

Two C-11223-4 banks each have three retracting targets, a shared reset plate and AE-26-1200 coil.
Top switches 30/31/32 pair with reset 4; lower switches 22/23/24 pair with reset 6. Each switch stays
active while its target is down; a reset raises the bank. C-13205-1 carries three interrupters and
an LM339 comparator; the full assembly and board tables are retained. The unshaded switch matrix
does not turn them into leaf switches. Do not reset a drop switch merely because a sound or
single collision ended; a stuck blade and a failed shared reset are distinct failure modes.

Coil 7 pulses the **bowtie diverter** through its flat cam and springs. The working script toggles
the two walls and switch 20 only on an enabled edge, so one pulse changes the latched position;
the falling edge does not automatically return it. Its initial wall pose is a table choice, not
a measured factory home. Preserve physical pose across a power cycle or initialize the contact
from the chosen pose; do not apply a blind controller-wide inversion. A stuck microswitch can
misreport the selected branch. The right ball gate, B-13496-1, has coil 13, a drive arm, shaft and
paddle; its wall selection follows the driven state. It has no separately proved position input.
Kickback 14 acts on left outlane 51. The table's impulse power 42 and 0.3 s charge are tuning values.
Spinners 17/29 are ball-driven and coast by inertia; neither has a motor output.

The prototype's popper uses input 16 and coil 3. The retained newer tables catch a ball at `sw16a`
and return it through the remote `sw16` outlet. VPW additionally forces an eject after 2500 ms to
make prototype geometry work with the default production firmware. That forced timer is a table
convenience, not a factory delay. Its extra top sling has score 49 and drive 15; VPW's default
`DisableUpperSling=1` suppresses its hit response, while JP6 explicitly selects prototype walls,
receiver and rubber or the production `sw16b` standup. The option does not change the ROM automatically.

## Flippers, bumpers and slings

There are four physical flippers, two on each cabinet button chain, with FL-11630 coils and
mechanical EOS behavior. The CPU does not independently power an upper-flipper output here.
PinMAME fabricates 45/46 together from right button 82 and 47/48 together from left 84 while enable 23
is on. These are virtual states, not four measured windings or EOS transitions. Upper generic
slots 33..36, sound-overlay 37..44, simulator 49/50 and custom 51..64 are explicitly disposed of from
this game's routing and empty handlers; lack of a trace transition is not their proof of nonuse.

The six special drivers are 17 left jet, 18 left sling, 19 right jet, 20 right sling, 21 bottom jet,
22 top jet. The own ROM's Switch Levels sweep paired score 52→17, 55→18, 53→19, 56→20, 54→21 and 50→22;
P-3 additionally paired 49→15. Those are isolated host stimuli followed by real ROM output pulses,
not immediate switch readback. The physical scoring and kick contacts must still be modeled in
the assembly; no service-trace interval is claimed as measured mechanical response time.

## Lamps, flashers, GI and displays

The 64 matrix lamps include playfield inserts 1..56/63/64 and backbox award lamps 57..62.
Lamp 42's matrix and all three service sets identify the 25K loop-ramp award; the inventory's 50K
reading is retained as printed. The matrix prints 6 where position 60 belongs. Backbox award lamps
remain outside playfield coordinates. The parts bill's six-lamp snake PCB lists #555 lamps where
the general inventory prints #44; both construction readings are disclosed on the affected devices.

The A/C relay 12 selects A-side drives 1..8 when released and C-side flashers 25..32 when energized;
they are paired loads, not sixteen independent transistors. Other flashers are 9 and 16. Hardware
has separate reverse-acting playfield GI 10 and insert/backbox GI 11; energized means dark.
The table's single GI collection/callback is a presentation simplification, not evidence that
the cabinet has only one circuit. No separate `pinmame.output.gi` group is invented.

Historical fake lamp 116 aliases are retained on the real left curl ramp flasher at solenoid 16.
The script's `SolCallback(16)` calls `SetLamp 116` as an animation key; 116 is not a controller
lamp-matrix address. Bind the flasher to solenoid 16; no lamp 116 binding is introduced.

Printed 08C/public 32 drives **two playfield emitters**. The table's `1p1b` marks disagree with
the two photographed right-side domes, the working callback's two bases and the full parts bill:
two playfield ramps have the same black/gray H-13745 cable. The insert-panel BOM's seven #89
backbox flashlamps are allocated to outputs 9, 28, 29, 30 (three) and 31, leaving no extra 32
backbox bulb. The top-center label on PDF 84 is blurred (6C/8C) and remote from the second
output-32 dome; the drawing is not used to establish two 08C locations. Preserve the literal
marks and correction. Other flasher circuits retain their separately documented backbox loads.
Source bulb quantities never come from render helpers.

Production outputs 3/15 have no fitted popper/top-sling loads. Their Coil Test steps are named
NOT USED. Output 15's power-up pulse is part of a whole controlled-byte 9..16 rise/clear, checked
in all retained initialization runs; service sweep and this common transient explain the public
state without implying a fitted actuator. `unused` here does not mean constant zero.

Physical displays are two 16-character alphanumeric modules, DSPL1 on D-12706 and D-12502-1.
PinMAME layout indices 0/1 start at segment-memory 0/20. Its extra 128×32 rendering is a virtual
presentation, not a fitted DMD. The sound board is D-11581-2015; unused CPU-board sound ROM slots
do not imply that the machine lacks audio.

## Spatial evidence and remaining work

The exact retained JPSalas 1 table was re-extracted byte-for-byte with vpxtool `git:v0.33.3`.
VPW 1.0.1 and JPSalas 6.0.0 were subsequently retained with source URLs, acquisition times, full
case-sensitive file manifests and hashes. They share ancestry, so agreement is supplementary,
not independent validation. All use 952×1974 VPX bounds. Normalization is left 0/right 1,
backglass 0/apron 1 through the shared helper.

The 58 lamp coordinates are manually read **insert-center projections** from the game's own
native-resolution location drawing. Six independently read bumper centers/flipper pivots
reconcile it to the table; maximum leave-one-out error is 0.014408 normalized. Coordinates round
to 0.001; extrapolated points stay observed. They are not a survey of sockets below the inserts.
GI has 39 distinct modeled bulb centers after exact-center render doubles are collapsed, but the
machine-side wiring/count is not established. VPW supplies ten dome-base placements for nine
flasher circuits and the prototype mechanisms. Flasher 16 is a bulbless glow in all retained
tables, so its coordinate instead comes from the factory's own round symbol beside 16 on PDF 84.
A separate six-control fit has maximum leave-one-out error 0.008251; its symbol projection is
slightly outside the control convex hull, explicitly extrapolated and observed. Switch 27 has
a handler but no matching table object; its observed projection instead marks the midpoint of
the distinct horizontal actuator blade beside 27 on PDF 82, separate from the diagonal sling
beside 49. That page has its own six-control fit and the point is extrapolated; the function
remains Middle Man and no ramp-entry function or precise microswitch body is inferred. Outhole/trough locations lack
defensible physical coordinates. These gaps, the GI membership/count and independent placement
validation keep both editions partial. The production target contact construction and prototype
OPDB identity remain explicitly unresolved in their respective coverage lists.

Sources and exact locators are in each definition. Whole printed tables, assembly tables,
script/core fragments, original photo observations and firmware-author evidence are under
`evidence/excerpts/bally.radical.1990/`. Compact service observations pin raw display segment
digests, successful run/scenario hashes, ROM identities and retained initialization state. The
failed original German sweep is retained as failure evidence; the corrected fresh sweep is the
one cited. ROM bytes, manuals, photos and community tables remain outside Git.
""")
