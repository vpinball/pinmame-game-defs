# Dirty Harry (Williams, 1995)

Coverage: **partial**. The production inventory, firmware family, address disposition,
physical switch construction, mechanisms and available geometry are curated. The remaining
requirement is `spatial_placement` (incomplete physical GI socket inventory and observed geometry).
No author-ready promotion is claimed.

## Identity and physical scope

This is Williams model **50030**, released in March 1995, IPDB **684**, OPDB
`GrJ2Z-M61Xd`. The manual's own title, model and board inventory agree with that identity.
It has WPC Security, separate DCS sound, a 128x32 backbox DMD, three flippers and three
jet bumpers. The pinned drivers `dh_lx2`, French `dh_lf2` and LED Ghost Fix `dh_dx2`
share `init_dh`, display, sound-ROM set, generation and routing. They are firmware
variants of this physical machine.

Sample hardware belongs to this game's history. It does not create a separate machine
group or an invented prototype driver. The January 11, 1995 insert-label amendment
16-10007 removes drop-target-down coil 6, drop-reset coil 25, left-loop gate 36,
switch 53 and test switch 88, and removes coil 25's tieback diode. It also changes
top-right popper 4 from AE-24-900 to **AE-23-800**. The retained production tables
already contain these corrections, but the switch-location drawing retains a stale
53 balloon and the unique-parts list retains a drop-target assembly. The explicit
amendment controls production fitment.

LX-2 still names and drives 6, 25 and 36 in its solenoid test, and pulses 6 during
startup. Those are retained sample-control paths with no production load. Runtime
activity is recorded without converting it into physical fitment. The historical
sample mechanism references the unused production addresses so a reader can account
for them. No undocumented sample target travel or geometry is invented.

## Controller contract and exhaustive address disposition

The definition enumerates dedicated inputs 1-8, every matrix cell 11-88, the
unfitted PIC-selectable columns 91-98/101-108, all Fliptronic inputs 111-118 and the
eight-bit CPU option byte. It enumerates public solenoids 1-50, all 64 lamp-matrix
positions and GI 0-4. `dhGameData` declares no custom switch/lamp columns or custom
solenoid handler; the profile's broad optional namespaces are not extra fitted devices.

Each unused production matrix/lamp cell is explicitly printed unused by this game's
table. The absence of a VPX binding or a runtime transition is never used as proof.
The PIC can select internal columns 9/10, but the CPU harness and matrix have only
eight drive columns. They are retained as unfitted address space. Output 37-44 is
constant zero in `core_getSol` on this generation; it is not a WPC-95 LPDC range.

Printed flipper circuits **29-32 map to public 45-48**. Printed 33/34 remain the
upper-right power/hold pair. Public 35 is the **right-loop magnet**, repurposing the
upper-left power output; 36 is the removed sample left-loop gate. The flipper diagram
draws the starred upper-left circuit but calls it upper RIGHT in its footnote. The
solenoid table, separate solenoid wiring, three-flipper inventory and script callback
35 settle that wording error. It is a device note, not an unresolved physical conflict.

PinMAME's power callbacks 33, 45 and 47 aggregate the power and hold bits. Their state
is useful for moving the flipper, but does not measure the power winding alone.
Hold outputs 34, 46 and 48 remain separately published. The retained old table moves
the upper-right flipper from the lower-right routine; a recreation can use the
independent ROM upper-flipper outputs documented here.

Outputs 29 and 31 carry observed virtual WPC_GILAMPS/J111 states. This driver installs
no fast-flip RAM address, so 31 is the legacy bit-7 mirror rather than a physical
game-on relay. Output 32 is a statically proven zero bit. Output 49 is the built-in
simulator's shooter-release state, and 50 is constant zero. Public 30 exposes J111
GPIO bit 6 under the same unconditional state-channel contract as bit 5 at 29.
No higher-level game function is assigned to either GPIO bit. No transition at 30
was observed in the retained probes; this does not make its published state unused.
It must not be mistaken for printed lower-right hold circuit 30.

## Switch polarity and initialization

At pinned PinMAME revision `97aa922bf8e4b6970126192ec1ac1fb0305a4f62`, WPC Security
reads matrix rows through `wpc_pic_r` directly from `swMatrix`. The per-game mask is
`00 00 00 ff 7f 00 00 00 00 00 00 00`: public 31-38 and 41-47 are inverted,
although unused masked 36/37 remain unfitted. The clean-state T.1 sweep confirms that
fitted matrix switches are ROM-active at public **1**. A masked contact therefore
rests physically closed; an unmasked one rests open. The mask is not inferred from
the appearance of an opto beam, and consumers must not invert the delivered state again.

The Fliptronic register reads the complement of column 11. The manual's maintenance
page 1-48 independently states that the physical EOS contacts are normally open.
PinMAME synthesizes EOS 111/113/115 from its declared flipper outputs, so a recreation
drives cabinet buttons 112/114/116/118 and lets the emulator supply EOS. The sweep
shows 112 firing 45/46, 114 firing 47/48, 116 firing 33/34 and 118 firing 47/48.
The latter is the second opto of the left cabinet button, not a fourth flipper.
Position 117 is retained as unfitted. Its generic manual listing is not fitment proof.

Set the four occupied trough positions 32-35 active for a normal four-ball start.
Keep always-closed 24 at public 1 and establish the intended coin-door state at 22.
The ROM names ALWAYS CLOSED on the **release** of 24; that is not an ordinary
ball contact. Chamber 44, popper 45 and mini-trough lockup 77 should follow balls,
and position 76 follows the gun crank. Do not permanently tie an opto active merely
because its clear beam has a particular electrical level.

## Ball routes and mechanisms

The two A-17811 slingshots pair switches61/62 with coils9/10. Their plungers and
links move the kicker cranks; spring10-128 returns each arm after a pulse. The three
B-9414-3 jet bodies pair switches63/64/65 with coils11/12/13 and A-9415-2 coil
assemblies. The wafer/leaf senses the ball; the linked ring rebounds it and the
springs restore it. All five contacts rest open. The retained T.1 probe confirms
each switch-to-coil pulse, without claiming a measured physical stroke time.
Stuck leaves or binding rubber/wafer/ring parts are faults, not home sensors.

The cabinet B-10686-1 knocker has AE-23-800 coil7 and A-5387 plunger, without a
feedback switch or ball route. A-15361 is the passive plumb-bob tilt14: its pendulum,
wire and bob move into the contact bracket and settle clear at rest. Cabinet slam
tilt21 is a separate contact. Neither uses a software-driven physical reset. The
standard assembly tables are retained in `standard-assemblies.md`.

The four-ball outhole trough A-19963 has optos 32-35 and separate jam/exit opto 31.
Coil 1 feeds shooter lane 15; coil 2 launches it. The script derives trough states
from a ball count and pulses jam 31 only when releasing from a full trough. That
simplification is documented, not a claim about the physical jam switch's geometry.

The motorized .44 Magnum comprises gun A-19112, mounting/crank assembly A-18581,
12V motor 20 and mechanical position switch 76. A-19947 and the drive plate turn
continuous motor rotation into an oscillating gun. Position 76 closes near the
backbox-facing end and opens before counter-clockwise travel. There is no separate
direction output. The script's -98/-2 degree limits, -4 degree mark and timer rate
are recreation tuning, not physical calibration or a measured travel range.

The front cabinet gun handle A-16113-1 operates trigger 11. Trapdoor high-power 8
and hold 16 are windings of one A-14701 coil on A-19282, operating flap A-19132.
When the door admits a ball, it enters the under-playfield mini-trough. Mechanical
lockup switch 77 and opto 45 report the ball path to popper 5, which loads the tube
into the gun. Chamber opto 44 confirms a loaded ball; gun-launch coil 3 drives the
spring-return bell armature and fires it. A chambered ball, a gun position mark and
a ball in the mini-trough are distinct states.

At startup the ROM homes the gun. T.17 GUN TEST runs motor 20 on Up, stops it on Down
or after its timeout, shows the position switch and gently ejects a ball placed
in the chamber. T.18 TRAP DOOR checks the trigger/serve/door/autoplunger/mini-trough/
gun path. Failed or stuck 45/77/44 feedback can leave a ball unloaded or repeatedly
ejected; missing/misadjusted 76 prevents reliable homing. The service test provides
observable checkpoints without asserting a measured mechanical speed.

The manual calls the automatic stop "about 20 seconds". Two fresh LX-2 probes,
one with 76 held closed and one with thirty periodic synthetic marks, both stopped
motor 20 after approximately **24.600 elapsed harness seconds**. The earlier
22-second static-open probe ended before that limit. This demonstrates a timeout
independent of the tested marker patterns; it does not measure physical speed or
the real cam's mark duration.

The retained script writes 77 equal to motor enable and computes 76 from its own
angle. The first is a mini-trough feedback substitution, not physical motor-to-77
causality. It also clears coin switch 3 instead of chamber 44 on the enabled launch
branch, clearing 44 on the disabled branch. These are consumed-table defects. The
definition preserves the factory sensors and records only the motor/crank-to-76
physical relationship.

Warehouse entrance feeds under-playfield opto 46 and top-right popper 4, then the
ramp outlet. Its script-only anti-double-ball wall is not the removed sample drop
target. HQHole drops a ball into opto 47 and coil 14 ejects it from a separate hidden
outlet. Safehouse switch 73 and coil 26 form the left saucer/pop-up path. Do not
collapse receiving holes and ejector positions or claim their coils directly actuate
ball-presence switches.

Right ramp diverter 15 (A-18585), left diverter 27 (A-19746), and right-loop gate 28
(A-17796) are separate route selectors without separate matrix position sensors.
The old table uses multiple collision walls for the left diverter; those walls are
one mechanism. Gate 28 opens while energized. Magnet 35 catches/releases a right-loop
ball to give a slow feed to the upper-right flipper. T.16 MAGNET TEST exercises it
from right-loop opto 42. Return springs and gravity restore the physical routes;
table-specific kick forces and velocities remain outside the canonical definition.

## Lamps, flashers and GI

The lamp matrix has 58 fitted addresses; 71-76 are explicitly unused. Cabinet lamps
87/88 are the Buy-in and Start buttons and have controlled non-playfield spatial
records even though the old table omits their Light bindings. Literal tables retain
source wire colors, connector pins, part numbers, blank cells and the duplicated
Q87 lamp-row transistor entry. The initial OCR normalization of row 5/6 was rejected
after checking the native scan. An unsettled wiring-detail reading does not create
a semantic physical-machine conflict.

Flasher 17 has two #906 bulbs, 18/19/21 one each, 22 one #89, and 23/24 two #906
bulbs each, including elevated rear-panel bulbs. Their multilight callbacks paint
reflections and broad illumination; they do not enumerate sockets. Shared GIWhite1
glow on 23/24 is a renderer helper. Special lamp 38 uses the Bankrobber sign, 47/48
the two warehouse bulb covers, and 84/85 the jet-area domes. Their world-space meshes
were checked instead of promoting the glow Light centers.

GI public 0-4 corresponds to printed strings 01-05: Right, Left, String 3, String 4,
Bottom. The old script binds 0/1/4 to three mixed collections and ignores 2/3. The
factory connector list places J120 on the insert panel, J121 on the playfield and
J119 on the coin door; the summary table has opposing location columns, and the
literal readings are retained. Strings 1/2 include additional insert-panel branches;
string 5 includes coin-door bulbs. No complete per-string bulb quantity is asserted.

Only Light objects explicitly showing a bulb mesh enter provisional GI placements.
The original table has eight such bottom-string and three left-string objects, and
none in its right-string collection. Broad Light halos and Flasher sprites are
excluded. The acquired IPDB playfield photographs corroborate the overall layout
but hide many sockets beneath ramps/plastics. Remaining socket attribution must stay
observed or absent until actual geometry/photos/wiring establish it.

The factory B-9414-3 jet body drawing independently specifies a 24-8776 wedge socket
and 24-8768 #555 bulb. It does not assign that socket's GI string or establish a
complete layout. Its one-used translucent-red cap note is retained literally;
the separate matrix dome lamps84/85 are not substituted for body sockets.

The additional acquired Pinside shop-out photographs confirm the two jet-area
domes, warehouse cover bulbs and elevated rear-panel flashers. Lit right-side
photographs show some under-plastic sources but cannot establish unique coordinates,
complete counts or electrical string membership. Their original resource hashes,
photographers and primary visual observations are retained in the definition and
`photo-reconciliation.md`; LED retrofits do not change the factory bulb specification.

## Spatial method and retained evidence

The retained Knorr v2.0 table has bounds `0,0,964,2162`. Table coordinates use
`x/964`, `y/2162`, rounded once to six decimals. Switch/coil positions follow the
actual script-bound collision object; trough, EOS, gun, trapdoor and hidden popper
anchors explicitly disclose projections. A point on a mechanism is not claimed to
be the exact coil or sensor body.

Insert lamps use independent coarse factory-symbol reads on PDF 113 rather than
treating Light overlays as observed sockets. Their seed records full-render size,
pixel centers and frame. Three independently read jet-bumper controls reconcile
the frame with exact retained-table objects; this is a coarse cross-check, not a
validated affine fit. Coordinates from these reads have three decimals. Crossing
leaders for 52/53 were followed to the two bullet inserts, not the nearby saucer.

Meshes were exported with `vpxtool export obj --units vpu`. Bankrobber's stored
origin is `(0,0,0)`, whereas its world-space bounds lie on the left playfield.
The gun mesh is offset from its stored primitive position. The rear-panel dome
origins have y=-16, but their actual exported centers are in bounds; no coordinate
was clamped. The spatial report gives each source role, raw measurement, mesh bounds,
projection, missing placement and immutable hash.

Original manuals, VPX, meshes, photographs, ROM archives and complete harness traces
remain outside Git under `pinmame-game-defs-working-dir`. Factual excerpts are under
`evidence/excerpts/williams.dirty-harry.1995`; exact source identities and the complete
case-sensitive path/size/SHA256 extraction-manifest algorithm are pinned in the
curator seeds. Recompute them through `tools/curate_dirty_harry.py --check`
with the applicable roots configured.
