# Alien Poker (Williams 1980)

Coverage: **partial — complete production controller inventory and recreation contract; physical
socket/contact placement, service-contact construction and factory lane-change contact 43 remain incomplete.** The spatial
report lists unplaced devices, the unresolved physical counterpart of virtual switch 43 and all observed projections. The six production drivers are separated from Oliver Kaegi's physical
multiball conversion. No completion score overrides these gaps.

## Identity, variants and source roles

The October 1980 Williams booklet 16P-501-103 identifies model 501. Verified IPDB 48 and OPDB
G4yen-MD12Y identify the same production game. Pinned PinMAME 46e1a01a declares GEN_S6,
System 6A seven-digit displays and a common init for L-2/L-6, French speech and the free-play fixes.
French sets replace speech ROMs; the ff patch restores the knocker when Adjustment 18 selects
free play. These changes do not add hardware. The 2006 catalog date on alpok_b6 is a firmware
date and does not establish a second factory manufacture year.

The retained JPSalas 1.0.1 table (metadata date 29.12.2017) supplies runtime bindings and exact geometry;
its embedded script runs alpok_l6. The pinned vpxtable_scripts sidecar has matching parsed I/O
signatures but different bytes. The standalone sidecar is a later/different script and is not
substituted into the extraction. Manuals govern physical fitment/wiring, PinMAME source governs
transport, and actual ROM display responses settle diagnostic roles. Production photographs
corroborate count, side and order. Original manuals, images, table and ROM bytes remain external.

## Switches, polarity and service controls

All 64 matrix positions, five negative service inputs, eight synthetic flipper positions and
18 published DIP positions have explicit dispositions. Factory 44–64 are unused; a stale ROM
display is not evidence of non-fitment. Numeric and zero-padded switch aliases remain available.
The matrix is sequential, column-major; it is not column-times-ten notation.

The System 6 read path returns the raw row byte and alpok has zero invSw. In the retained Test 03,
each fitted contact 1–42 is independently closed at public 1 and the ROM displays its own number.
That read path plus active-level proof establishes normally-open construction for contacts 1–42. The original
drop-target contacts are mechanical sliders over horseshoe PCBs, not optos or ordinary leaf
contacts. They remain closed while the target is fully down. Cabinet tilts include the plumb bob,
ball-roll and slam inputs; playfield tilt 31 is a separate assembly.

Right cabinet input 82 is copied into matrix 43 on every core update; a consumer drives 82.
A single-write held probe proves the copy and synthetic 45/46 pair. Left 84 drives 47/48 without 43.
The factory matrix names contact 43 and Figure 4 draws it beside the upper right flipper, but its
mounting and construction are unresolved. Its virtual public record has no physical location or
normally-closed claim. The emulator's cabinet-button copy proves neither physical fact.
The other flipper-column positions have no fitted function in this driver. The table redundantly
writes 43 before s6.vbs writes 82; that is a table defect with no separate effect, not a conflict
about the physical machine. Hardware EOS switches act locally on the cabinet-wired flipper coils;
the synthetic pairs do not measure winding current or EOS timing.

The coin-door controls are Advance(-7), Auto-Up/Manual-Down(-6) and High Score Reset 8.
CPU diagnostic(-5), sound diagnostic(-4) and Master Command Enter(-3) are board controls.
Manual-Down/Advance enters diagnostics; Auto-Up advances tests, Manual-Down steps within a test.
The manual's Master Command 8/7/6 are public DIP 17/18/19: zero audits, restore defaults, auto-cycle.
The lower CPU function bank is explicitly unused; unassigned positions gain no invented function.
Sound options 1/2 are the two modeled sound-board command bits. The booklet does not name their
game-specific settings, so none is invented. Exact coin-door/board service-contact construction
is not established by the retained game booklet and stays within the polarity blocker alongside
factory contact 43; ROM
behavior for the ordinary fitted matrix contacts is established separately.

## Outputs and display roles

All 23 standard/special/game-on outputs, synthetic 45–48 and 64 lamp cells are enumerated.
Sound lines 9–13 are meaningful command lines. Output 16 is the cabinet coin-lockout
coil; output 23 enables the flipper relay and special circuits. Lamp 49 is explicitly unused. No separate
System 6 public GI group is fabricated for the table's local illumination effects.

Figure 3 reverses left/right jets 18/19; Table 3, the driver's switch slots and isolated gameplay
agree on 18=right and 19=left. The literal print is preserved. Full connection/part-number columns
are transcribed; no connector pin is borrowed from a generic/sister-game chart. The booklet calls
the sound board's ROM “Sound ROM 2,” while the selected driver loads sound3.716; the filename is
recorded without assuming the printed board label and dump name use the same numbering.

Player displays are indices 0–3, seven digits at segment starts 1, 9, 21, 29. Ball-in-play tens/units
are indices 4/5 at starts 0/8; credits are 6/7 at 20/28. The s6.c layout comments reverse those names.
The ROM proves the roles: coin makes 6/7=03; Start makes 6/7=02 and 4/5=1 with a blank tens digit. Coil test shows selector
01–22 at 4/5 and test 02 at 6/7; switch test shows the contact number and test 03 respectively.
All eight exported layouts are backbox/service display subdivisions, not eight physical glass
assemblies: the two one-digit pairs together form the four-digit credit/ball window.

## Mechanisms, ball paths and failures

The production game uses one ball. It drains under the apron, closes switch 9 and is kicked by coil 1 into
the feed path to the shooter lane. The manual plunger launches it. BallRelease in the VPX is
the final shooter-lane proxy; Drain is a virtual ball-transfer object. Neither locates the physical
outhole coil or contact. Oliver's before-conversion photo confirms the original single coil.
Startup/new-game ROM activity releases/drops the bank and resets targets; held contacts after
an attempted reset can provoke retries. No measured mechanical timings are claimed.

Three saucers hold the ball on Spade 15, Club 22 or Heart 29 until coil 2, 15 or 3 ejects it back to
the open field. They advance P-O-K-E-R and other awards; production has no added multiball trough
or lock-release apparatus. A ball or stuck contact that remains after an ejection can be retried.
Kick angles, strength, physical travel and animation delays are table-owned tuning.

The five diamond targets run 10, J, Q, K, A, with contacts 42, 34, 26, 18, 10. Outputs 4, 5, 6, 7, 8 individually
raise the corresponding target; 21 releases/drops the whole bank. Each target slides through
guides, is retained upright and falls with spring bias; its full-down horseshoe contact remains
closed until raised. Original bank photographs show five separate coil/plunger mechanisms and
the perpendicular shared release. A generic D8362 common-lift bank from the parts catalog is
structurally different and must not be substituted. No unsupported assembly part number is assigned.

The factory rules reset an out-of-order drop individually, reduce its lit value and enable the
Spade saucer to increase it. In-order completion earns the lit Royal Flush value. Original owner
rebuild reports document friction/hanging just above playfield level, contact/PCB wear and weak
springs allowing rebound upright. These are attributed failure observations, not factory repair
procedures. Replacement NMP sensors in the same thread are outside factory construction.

Four jet assemblies pair 35→17(center), 37→18(right), 36→19(left), 38→20(bottom); left sling 13→22.
The scoring switch and dedicated special trigger belong to the same mechanism, with game-on 23
gating the response. The coil strikes the ball, and the mechanism returns mechanically. The
retained gameplay isolates these address pairs. Its first bumper step overlaps startup resets;
those extra resets are not attributed to the bumper.

Left button 84 operates the left flipper; right 82 operates both right flippers and lane change.
The spinner is passive and pulses 17; lamp 18 shares its spinner award with Royal Flush 3X.
Open-field returns, fixed rebound surfaces, the four King lanes and the manual shooter complete
the ball path. The recreation owns geometry, rubber response, spring strength and coil tuning.

## Lamps, GI and spatial limits

The eight-by-eight factory lamp matrix supplies all identities/wires. Lamp 37 explicitly feeds two
extra-ball arrows, at the upper Club and right Heart saucers. Lamp 18 feeds Royal Flush 3X and the
spinner. They retain two placements each. Bumper 29–32 have two light-render layers per assembly;
the report records one projected emitter on each physical bumper. Flash helpers, reflections,
GI glows and insert overlays never create additional sockets.

Backbox lamps 50–55/57–64 and cabinet/service devices are spatially not applicable to the playfield.
The physical playfield credit circuit 56 is fitted, but the table's l56 sits on bare wood outside
the painted field. Its socket remains unplaced. Switch 9, tilt 31 and coil 1 also lack defensible
physical positions. Factory dashed location bubbles are remote annotations, not sensor centres.
Other accepted insert/mechanism positions are observed feature projections from exact VPX
objects, checked for count/side/order against factory drawings and production photographs.
Hidden/raised socket centres and the uncontrolled GI socket inventory/wiring remain incomplete.
The printed lane-change contact 43 also lacks established mounting/construction despite its virtual
emulator representation. That is why the record remains partial even though the production runtime contract is documented.

See the machine's spatial JSON for exact hashes, object names, transformations, projections and
unplaced IDs; the committed compact runtime evidence is recomputed from retained raw traces by
tools/alien_poker_runtime.py. The original source and extraction manifests use distinct roots.
