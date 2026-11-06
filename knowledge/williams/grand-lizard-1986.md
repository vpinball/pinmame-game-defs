# Williams Grand Lizard (1986)

Williams model 523, IPDB 1070, April 1986. The three production drivers grand_l1,
grand_l3 and grand_l4 share physical hardware. The L-4 root retains U26 L-3
and U27 L-4; L-3 changes U27 and L-1 uses its own game pair. All share the same
CPU/sound topology and physical playfield. OPDB identity is G4XPZ-M7Zob.

This definition remains **partial**. Complete flasher, backglass matrix-lamp
and controlled GI bulb counts are not established. Emitter/socket coordinates,
some mechanism sensor projections and the unswitched playfield GI inventory
remain incomplete.
Observed VPX geometry is useful authoring evidence but is not automatically
validated by matching object names or by a second table of shared ancestry.

## Controller and physical construction

The pinned emulator is 46e1a01a0f73dc5ce163d98db1ae435883ecc450.
GEN_S11X chooses the System 11 controller contract, eight matrix columns,
64 lamp channels and no custom outputs. There is no A/C multiplexer, printer
or sound-overlay expansion. Every public switch/solenoid/lamp address has an
explicit disposition, including unused ranges. Switches are ordinary contact
circuits; s11's uninverted read with no invSw mask presents a closure at 1.
Factory switch parts identify leafs/buttons/tilts and drop-target microswitches;
normally_closed is never inferred from a table object's initial occupancy.

Cabinet buttons 82 (right) / 84 (left) drive the synthetic flipper states.
FLIP_SWNO(0,48) copies only right 82 to lane-change 48; zero means no left copy.
Matrix 47 is factory Not Used despite the table's gratuitous left-key write.
Both upper/lower flippers on one side move together. 45/46 and 47/48 are virtual
paired states, not independent CPU coils or measured winding timing.
Physical EOS and lane-change contacts are separate parts. The preliminary
power sheet omits upper-left and draws EOS contacts incorrectly; final
production tables/assembly distinguish all four coils and closed-rest EOS.

The standard display layout has four seven-character player rows and four
separate one-digit controller callbacks. Ball In Play/Match uses starts 0/8
(indices 4/5), Credits 20/28 (indices 6/7). Player starts are 1,9,21,29.
These are backbox devices.

## Ball handling and mechanisms

Playfield Tilt switch 9 (SW-1A-117) is fitted, but its precise contact center
remains unplaced. The retained evidence does not establish a cabinet/service
location, so it is not exempted from spatial coverage by its numeric range.

Three balls begin in the trough. Outhole 10 and kicker 1 collect the drain;
positions 12 (feed end lower-right), 13 (center), 14 (rear upper-left) advance as
balls roll; feed 8 serves shooter 11 for the mechanical plunger. The parts list
reverses Left/Right words for 12/14 against the explicit matrix positions;
the list and its spelling remain transcribed, not silently overwritten.

The four-target flash bank D-10883 has two independent pair resets 3/4 for
20/21 and 22/23. The rear three-bank D-9355 has one reset 2 for 25-27. Targets
latch down and keep their switches closed until physically raised. Reset
plungers/plates, guides, retract springs and microswitch adjustment determine
actual recovery; no electrical coil-to-sensor relationship is invented.

The A-ramp lock under the left ramp holds up to three balls at 32/33/34.
Output 5 drives the release-end C-8492 eject cam. Three locked balls, or one/two
plus top release target 24, starts multiball. The ROM supplies retries/rules;
the recreation must move balls and update serial occupancy realistically.
The script's sw34 kick direction/speed and magnet strength 12 are tuning,
not physical factory measurements. Held sensors may trigger retries or startup
switch reports; the game can compensate scoring after 60 balls without a switch.

Slingshots 17/18 have physical trigger contacts separate from scoring 43/44.
PinMAME's ssSw map deliberately uses the scoring bits to emulate the triggers
when enable 23 is on. Output 19 is a right flasher, not a third bumper: this
machine has no pop bumpers. Contacts, kick arms and rubber tension return the
ball and open the switch after impact; exact motion is table-owned.

Magna-Save outputs 9/10 drive relay 5580-09613-00, which powers A-8447 magnetic
assemblies near the left/right outlanes. 45/46 are cabinet request buttons.
L-I-Z earns left units; A-R-D earns right units. Isolated ROM depletion runs
settle left lamps 42-44 and right 45-47: three requests exhaust one group and
the next two no longer energize its relay. The manual drawing and retained
table visual bindings place those number groups on the wrong sides; physical
side/order follow the matrix, rule descriptions, separate relay responses and
the corrected lamp map. Do not reproduce the mirrored visual shortcut.

The retained table also swaps A/D target callbacks 38/40. Both factory matrix
and parts/drawing agree 38=A and 40=D; the physical mesh anchors follow those
letters. This is a table defect, not unresolved machine identity.

## Lamps, flashers and general illumination

Lamps 1-6 are backglass indicators and 51 is unfitted. Their individual circuit
bulb quantities are unspecified in the retained lists, so no quantity defaults
to one. The table comments out
five backglass assignments and 51; commented code does not establish absence.
Lamp row/column connectors, transistor identifiers and all 64 literal matrix
labels are preserved in the excerpts. Light overlays and copied LightNb glow
helpers are not observed bulb sockets and do not establish physical quantity.

The factory flasher map shows two sockets on 6 (lock), one symbol for 12 (three-bank), and
one identifiable 7 symbol. Other 7/19 leaders end on plastic outlines and cannot
be counted as sockets. 13 spans the head and backbox:
B-10823 head mounting shows two head sockets, but the backbox count remains
unknown. The single 12 symbol also fails to establish its complete circuit
count: the owner describes series-paired flashers without mapping each pair.
These count gaps prevent full output-semantics completion. Clear wiring or
continuity evidence for outputs 7/12/19 and the original eye-flasher panel
can settle the remaining counts.
The retained Jeff-Z owner repair photograph corroborates two head lamps and
the disconnected left auxiliary flipper contact. It does not show complete
original flasher circuits; repair/replacement parts are disclosed in its source.

GI 11 interrupts backbox/cabinet lighting through power-supply relay contacts
and 3J8-6/7. The playfield GI branches 3J8-8/9 to 8J4 bypass that relay. The
table's PFGI dims the playfield rendering as an artistic shortcut; no
playfield lamp coordinate is attributed to GI 11. Its complete backbox/cabinet
socket inventory and quantity also remain unquantified. Unswitched playfield GI has
no PinMAME callback to bind; its physical socket inventory/positions still
need complete underside evidence and are an explicit spatial blocker.

Coin-lockout output 16 remains a fitted Coinco 404603-2 relay circuit.
Preliminary PDF 14 draws two parallel coil/diode branches under 7L16 at
7J4 pins 3/4. This establishes two windings, but not their mechanical unit
identities. The production table has no quantity column; its one channel
row does not establish one assembly. Physical unit quantity remains
unspecified and is an output-semantics blocker. A complete coin-door
assembly drawing or original, traced photograph can settle the actuator count.

## Evidence and readiness

The production 52-page manual and preliminary 34-page schematic manual are
retained with immutable hashes under the external manuals root. Full matrix
and parts tables, source-contract excerpts and tightly cropped wiring regions
travel with this contribution. The two retained local VPX builds share the
3rdaxis/Slydog43 ancestry. Neither exact build was launched or independently
verified playable in this contribution. Their script mappings were checked
against the manual and independent ROM runs; geometry remains observed.
Exact extraction manifests record every relative path, size and SHA256 in
case-sensitive path order, using canonical UTF8 JSON bytes plus
newline; vpxtool reported a malformed scratched-glass PNG dimension warning.
That warning is retained and does not change successful object extraction.

The spatial report inventories every located, unplaced and not-applicable
record, raw geometry/drawing evidence, projections and remaining dimensions.
Curator generation is independent of external paths; evidence-enabled checks
recompute exact sources, manifests and geometry. Runtime traces use fresh
state directories and legal existing ROMs; host-written switch readback is
not presented as ROM evidence. Full source locators and trace hashes are in
the definition and compact runtime evidence. Author-ready promotion is refused.
