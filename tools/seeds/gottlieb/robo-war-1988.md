# Robo-War (Gottlieb/Premier, 1988)

Coverage: **partial**. Identity, the four driver variants, the complete controller address inventory with wiring, both display rows, the mechanisms and their relay gating, and runtime observations of the production ROM are retained. Only spatial placement is open: the trough switch, the playboard tilt contact, the playboard illumination and the six #67 flashers that share coil outputs have no position, every lamp is projected onto the centre of its insert or pop bumper because the table models no bulb, and a few table placements stay observed. These are authoring gaps, not a promotion checklist that has passed.

The factory instruction manual for game #714, scanned in two parts (part 1 SHA256 `c887ba2af6229371753d6a062a7a94eb5fd51cafdaed4c6ae49fabe1a5af2fef`, part 2 `f96ce0b20bebce7fdd085809e00c2eef6cc044957ec3942353f48fd053debb83`), is the physical authority. The retained community table `2fad113d9980585d74083d5010878ef061d57128b3ad694e75535954f5207f83` supplies the runtime bindings and the geometry; it was not launched, so its script is static evidence and the ROM's behaviour comes from the harness runs. The load-bearing excerpts live under [the game evidence directory](../../evidence/excerpts/gottlieb.robo-war.1988/).

## Physical identity and firmware

IPDB 1975 identifies Robo-War, April 1988, Premier Technology (trade name Gottlieb), model 714, System 80B, 2,130 units, designed by John Trudeau and Jon Norris with software by John Buras; the manual's title blocks print GAME #714. It has two lower flippers and two-ball multiball.

The pinned catalog has four drivers, all declaring the same System 80B game (`GEN_GTS80B`, `FLIP_SWNO(6,16)`, two 20-character alphanumeric rows, the System 80B sound board, inversion mask 0): `robowars` (production PROMs), `robowarf` (French PROMs, a language change), and the Flipprojets free-play builds `robowrfp` and `robowffp`, which replace PROM 1 and change credit handling only. All four run on the same machine. Only `robowars` is in the authorized ROM library, so only it was runtime-tested. A German version is known, but PinMAME has no driver for it.

## Controller contract

Use the [System 80B profile](../../controllers/pinmame/gts80b.json) at PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Switch numbers are strobe digit then return digit, `00-77`. The playboard uses strobes 3-7 only: the switch matrix sheet E-25886 prints strobes 0-2 with empty wire boxes and bare contacts, and the cabinet sheet's only contacts on them are the advance buttons (06, 16), Play/Test (07) and the left and right coins (17, 27). The other cells of strobes 0-2, the two `(SPARE)` cells 32 and 34, `(SPARE)` 67 and `(NOT USED)` 77 are recorded unused. Cell 37 is the center coin and 47 the replay (start) button, both cabinet contacts; the playboard matrix leaves 37 blank and prints 47 NOT USED for that reason. Every playboard and cabinet contact is drawn normally open; public `1` means closed. The slam switch (`-1`) is the one normally closed contact: public `0` is its closed, normal state.

Drive the lower flippers with `114` (left) and `112` (right). PinMAME copies them to 06 and 16 every update, where the cabinet sheet wires the left and right ADVANCE BUTTON contacts, and overwrites any direct write there. Physically the advance buttons are separate cabinet contacts: folio 49 lists two black pushbuttons with their own switches (item 26) apart from the flipper switch assemblies (item 9), so only the emulator ties them to the flipper buttons. The synthetic outputs `47/48` follow the left button and `45/46` the right while the game is on; the real flippers are not CPU-controlled (see below). Playboard switch `46` is a separate contact at the right flipper (part 25434): the rules call it the RIGHT FLIPPER SWITCH, it rotates the R-O-B-O top-lane lamps, and held in it shows the multi-bonus and replay level. A recreation should close 46 whenever the right flipper is raised; the table does so from its right flipper key.

Solenoids `1-9` are real drivers; `10` is PinMAME's game-on state from lamp 0 and `11` mirrors lamp 1 (relay T). Lamps `0-47` are the A3 board's latched lamp drivers. Lamps `48-51` carry the complement of `44-47`, as the A3 board's Z12 inverted outputs to Q49-Q52 do; nothing is wired to them on this game (E-25887 and the folio 48 list stop at L47). Lamps `52-60` mirror solenoids 1-9 in PinMAME's physical output mode only, and `61-63` have no writer. GI `0` is PinMAME's model of the tilt relay's playboard illumination. DIP settings `1-32` are the control board's switches S1-S32 (the ROM's own DIP display confirms the numbering); `33-42` feed only the sound board's Y-CPU port, which this game's sound ROM never reads and whose board has no switches.

Lamp 4 is not a lamp: it is bit 16 of the sound command, wired from A3J2 pin 2 to the sound board.

## Relays and the S multiplex

Four 16890 relays on the playboard are driven by lamp drivers, each with a diode across its coil:

- **Q** (lamp 0), the game-over relay: its normally open contact switches +24 V onto the flipper and kicking-rubber circuits, so flippers and slingshots are dead outside a game and after a tilt.
- **T** (lamp 1), the tilt relay: its normally closed contact passes the 6.3 V AC playboard illumination, so the playboard goes dark while T is energized. The ROM energizes it on tilt and also in short bursts during play as a lighting effect.
- **S** (lamp 12), the switching relay: its changeover contact moves solenoids 1, 2, 3, 5 and 6 between two loads each, through steering diodes on the A19 board and resistors on the A13 board.
- **A** (lamp 13), the auxiliary lamp relay: its normally open contact completes the common of the Playboard Light Show and the Glass Stop lamps.

The S table printed on folio 48:

| Solenoid | S released (lamp 12 = 0) | S energized (lamp 12 = 1) |
| --- | --- | --- |
| 1 | 1 Bank Reset (Alpha I, coil 5195) | Left Top Dome #67 |
| 2 | 2 Bank Reset (Alpha II, coil 19300) | Left Center Dome #67 |
| 3 | Hole kicker (coil 5195) | Stargate #67 (2) |
| 5 | 3 Bank Reset (Alpha III, coil 19300) | Left Bottom Dome #67 |
| 6 | 4 Bank Reset (top B-E-T-A, coil 5194) | Right Top Dome #67 |

Solenoids 4 and 7 are plain flashers: one #67 under the right side plastics and one under the left, each through a 1A16 transistor. Solenoid 8 is the knocker in the cabinet and 9 the outhole kicker. The ball release (coil 16570) and the Stargate ramp (coil 17875) are not on solenoid drivers at all: lamp drivers 2 and 14 switch them through the 2A16 transistor board. A recreation must therefore read lamps 2 and 14 as coils and route solenoids 1, 2, 3, 5 and 6 by the state of lamp 12 at the moment they fire. The ROM sets S before it pulses. In the gameplay probe every pulse of solenoids 1, 2, 3, 5 or 6 with lamp 12 off is a bank reset (at power-up, at game start, twice for each completed bank and at the next ball) or the hole kick, and every other pulse of them comes with lamp 12 on, in flasher bursts.

## Ball transport and mechanisms

- **Trough and shooter.** Two balls. A drained ball closes the outhole switch 66 and solenoid 9 kicks it into the trough. Trough switch 56 (`#2 TROUGH`) is closed only while both balls rest there. Lamp driver 2 pulses the ball-release coil to feed one ball to the shooter lane, where it crosses rollover 36 (no score) and is plunged by hand. Start with 56 closed. The ROM counts the end of a ball when 56 closes again; with one ball still out it waits.
- **Hole and multiball.** The kick-out hole at the upper right (switch 76) captures the ball when not in multiball: the ROM keeps it, raises the Stargate ramp (lamp 14 on) and releases the second ball. Hitting the Stargate spot target 72 then releases the captured ball (S released, solenoid 3 kicks) and lowers the ramp; the display shows the multi-bonus. In multiball the hole scores and restores the multi-bonus and kicks straight back out.
- **Stargate ramp.** A lifting ramp at the upper left. Lamp 14 holds coil 17875 energized; a normally closed ON RAMP SW. opens at the end of the stroke and leaves the coil on its hold winding. The assembly drawing (folio 52) shows the levers upright and the free end level with the bracket when activated, and the end about a bracket height lower when deactivated. Lowered, the ball rides the ramp up to the Stargate rollunder 71; raised, it passes underneath to the Stargate spot target 72. A second, normally open ON RAMP SW. lights the uncontrolled Stargate LAUNCH ATTACK lamp while the ramp is up. At game start the ROM raises the ramp for under a second and lowers it again, so play starts with it down; the probe also saw it rise at tilt.
- **Drop targets.** Four banks, each reset by one coil only while S is released: Alpha I is a single left target (43); Alpha II two center targets (42, 52); Alpha III three right targets (41, 51, 61); the top bank four targets B-E-T-A (40, 50, 60, 70) along the left lane. Each target holds its switch closed while down. The rules chain them: completing Alpha III while flashing resets and flashes Alpha II, completing Alpha II while flashing flashes Alpha I, and Alpha I while flashing lights an extra ball, resets Alpha III and adds a letter to R-O-B-O-W-A-R.
- **Pop bumpers and kicking rubbers.** Three pop bumpers (53 top left, 63 top right, 73 bottom) fire from their own skirt switches through driver boards 1A8-3A8; two kicking rubbers fire coils 1496 from their own pairs of contacts on the Q-switched +24 V. The CPU only reads their scoring switches; both kicking rubbers share switch 33.
- **Flippers.** Two 20095 flippers, each fed from Q's switched +24 V through its cabinet button, with a normally closed end-of-stroke switch at the coil's centre tap. There is no flipper drive from the CPU.
- **Spinner.** Switch 30 on the left orbit pulses once per revolution; lamp 44 lights it.

The right lanes are named the factory's way: the inner right lane (65, under the Special insert of lamp 38) is the RIGHT OUT ROLLOVER and the outer right lane (75, under the ADV X insert of lamp 41) the RIGHT RETURN ROLLOVER. The table names the objects at those positions RightInlane and RightOutlane; its bindings and geometry agree with the factory, only its names differ. Folio 7 describes post adjustments: the left outlane post sets a liberal or conservative outlane and the lower right post sets the return lane's share.

## Lighting

- **Controlled inserts.** Lamps 3, 5-11 and 15-47 are #44 bulbs on the A3 board's MPS-A13 or MPS-U45 drivers (folio 41 note 2), one bulb each except the bonus multipliers 15-18, which light two bulbs in parallel under one oval insert each. E-25887 prints lamp 37 as LEFT OUT ROLLOVER, SPECIAL; the folio 48 list, the rules and the location drawing put it over the left return lane, so the device carries the list's name.
- **Flashers.** Six #67 bulbs are reached through relay S (above). The location drawing prints the four domes as caps along the top: SOL.1, SOL.2 and SOL.5 at the upper left (about x 0.08, y 0.07; x 0.07, y 0.11; x 0.05, y 0.14) and SOL.6 at the upper right (about x 0.89, y 0.07). It prints the two Stargate SOL.3 #67 callouts near the top of the Stargate ramp, with leaders the drawing does not resolve (labels about x 0.21-0.22, y 0.09-0.14). SOL.7 #67 is printed without a leader at the left side (about x 0.04, y 0.29) and SOL.4 #67 likewise at the right (about x 0.88, y 0.51); the table's LPF and RPF lights lie on the same sides, but a leader-less label marks no part, so those placements stay observed. These positions come from the folio 48 control fit and are approximate; the table's dome objects LF61-LF63 and RTF and its SGP lights are render helpers that sit 0.1-0.15 away from the drawn domes and are not sockets.
- **Light show and glass stop.** The auxiliary lamp driver 1A11 (MA-866) runs on its own clock and steps ten outputs while relay A completes their common. Each output lights one row of two triangle inserts in the PLAYBOARD LIGHT SHOW (twenty bulbs, numbered `#1-#10` on the location drawing in two V-shaped arrays in the centre of the playfield) and one GLASS STOP bulb (ten bulbs on A9P8/J8). The script runs its own chaser on the same lamp 13. No controller address reaches these bulbs.
- **Playboard illumination.** 6.3 V AC through T's normally closed contact. The manual does not list the sockets.

## Game rules a recreation needs

The rules on folios 4 and 5 are transcribed in [manual-rules.md](../../evidence/excerpts/gottlieb.robo-war.1988/manual-rules.md). Their physical consequences are already described above: the hole captures outside multiball and the Stargate spot target releases the ball and lowers the ramp; the right flipper switch rotates the top-lane lamps; the drop-target banks reset only through the S-released coils. Three- or five-ball play is DIP 25; the five-ball scores differ.

## Spatial evidence and limits

The retained table's script-bound objects give every placement, a pop-bumper lamp taking its bumper's; the [spatial mapping excerpt](../../evidence/excerpts/gottlieb.robo-war.1988/spatial-mapping.txt) lists each object, its raw point and the normalization by the table bounds 1024 x 2240. Bank reset coils are anchored at the mean of their targets, the hole, outhole and ball-release coils at their kickers, and the Stargate ramp coil at the ramp's drag-point centroid; none of these is a measured coil.

{CALLOUT_CHECK}

The factory drawing prints SW 42 twice, at the center bank and at the single left target, and no SW 43; the matrix, assignment list and script put 43 at the left target, so the second SW 42 is a drawing slip and that placement is not checked. The drawing's SOL.1, SOL.2, SOL.3, SOL.5 and SOL.6 callouts mark the flashers on those outputs, not the coils, so the coil anchors are not checked against them. SOL.4 and SOL.7 have no leaders, so the flashers on those outputs are not checked either.

No light in the table shows a bulb, so no lamp socket is measured and no lamp is checked against the drawing. Each insert lamp's script-bound light is a textured overlay of its insert, and its placement is the insert's centre, projected; each multiplier oval L15-L18 holds both bulbs of its lamp, so both placements are projected onto the oval's centre. The bulb-mode lights the script also fades with lamps 5-11 and 19-22 (`l5a`-`l11a`, `l19x`-`l22x`) only paint glow 27-42 units beside their inserts, and `l32sc`, `l35sc`, `l37sc` and `L38sc` are reflections on the side walls. Each pop-bumper lamp is projected onto its bumper's centre, since the light there shows no bulb either.

## Remaining authoring requirements

- Place trough switch 56: the table has no object for it and the drawing prints its label without a leader.
- Place the playboard tilt contact on switch 57 (part 9141): the table has no object for it and the drawing prints SW 57 without a leader in the drain area.
- Place the playboard illumination sockets, which the manual does not list.
- Measure the lamp sockets: every insert lamp is projected onto its insert's centre (both bulbs of each bonus-multiplier lamp 15-18 onto its one oval) and every pop-bumper lamp onto its bumper's centre.
- Give the six #67 flashers on solenoids 1, 2, 3, 5 and 6 positions a consumer can use; the schema allows only effect placements on a coil output, so they are described here.
- Measure the shooter-lane rollover, the outhole and right flipper switches, the left drop target's switch 43, the flashers on solenoids 4 and 7 and the coil anchors, which stay observed.
