# Joker Poker (Gottlieb 1978, solid state)

Coverage: **partial**. Identity, the sole supported ROM, System 1 routing, the
display layout, target-bank implementation, and observed switch interaction
locations are documented. The factory schematic/manual is unavailable; physical
wiring and contact construction, complete GI/bulb inventories, reset linkages,
unresolved address fitment and complete physical placements remain open.

## Identity and evidence

This is Gottlieb model **417 SS**, IPDB 1306, the June 1978 solid-state Joker Poker,
not the same-titled electromechanical version. The sole pinned PinMAME game driver
is `jokrpokr`, under the non-game `gts1` system root. It uses `417.cpu`, `GEN_GTS1`,
the `GTS1C` chime module and `sys1_disp`. The source comment retains an August date;
IPDB reports that Gottlieb documentation corrected that month to June. No new
physical variant is inferred from that difference.

Source links and full factual excerpts are carried in the definition. The exact
user-supplied `Joker Poker (Gottlieb 1978) 1.1.vpx` by Goldchicco, 32assassin and
BorgDogs is retained externally with an extraction manifest. Its embedded script
declares `jokrpokr`; it has not been independently launched and play-verified in
this contribution. Runtime claims therefore describe the retained implementation,
not observed successful play. The older corpus script is superseded by these exact
table bytes for this curation, without editing that upstream evidence.

Fresh-state harness startup failed before ready: the exact emulator diagnostic
reports missing inherited `A1752CF.bin` and `A1753CE.bin`. No gameplay or service
injection ran, so the retained failures provide no positive runtime evidence.
See source `runtime.joker-poker.boot-blocker` and its diagnostic excerpt. Supply
the authorized common System 1 ROM pair before repeating these probes.

The one-page inkochnito technical chart reproduces switch, lamp, solenoid and fuse
tables and is transcribed in full. It is **secondary evidence**. Without the game's
factory schematic its wire, connector, transistor, part-number and Not Used cells
remain candidates. It does not supply switch contact construction, DIP meanings,
the sixth CPU-scanned strobe or all special inputs. The L17 transistor type differs
between two of its own tables; both readings are preserved in the excerpt.
Even a printed Not Used cell cannot settle fitment without primary wiring, so
those read-capable switches and lamp-driver bits retain unknown availability.
Only source-proven unreadable or constant-zero addresses are marked unused.

IPDB's real-machine photographs corroborate topology. Photo 32830 by Jim Palson
also exposes Gottlieb instruction card B-18450. Copyrighted table files, photographs,
ROMs and the complete chart remain external to Git.

Backglass photo 12959 by Bill Dempski separately corroborates four player-score
windows and one central auxiliary window in the backbox. This establishes their
physical location without claiming its restored display parts are factory original.

## Controller contract

`pinmame.gts1` documents the pinned source, including the non-sequential factory
switch numbering. CPU matrix reads reach public `x0` through `x5`, for x=0..7.
The chart prints only strobes 0..4. Special GPIO reads reach 46/56/66/76; the table
uses 66 for the outhole, the library writes 56 for audits reset and 76 for slam.
All read-capable but undocumented positions remain unresolved. Their omission from
the chart and failure to appear in a script do not prove them unused.

The CPU does not read the flipper-button column. Host inputs 82 and 84 drive right
and left synthetic flipper output pairs 45/46 and 47/48 while game-on is true.
The right button moves both the lower-right and upper-right flippers in the table.
Synthetic outputs are virtual signals, not four fitted solenoid drivers or four
independently timed winding states. Other flipper-column positions and unselected
special/matrix returns are explicitly enumerated.

Solenoids 1..12 are writable CPU routes; 17 is derived game enable (lamp 1 on while
lamp 2 is off). Only 1..8 are identified by the chart and script. Solenoids 9..12
stay unknown. Other ordinary solenoid addresses are constant zero in the driver.
Lamp callbacks use the default sequential numbering from 1. `lamp_w` reaches
44 bits even though the secondary physical table ends at L36; 37..44 stay unknown.
The remaining default 8x8 callback matrix tail is never written. Twenty-four CPU
DIP bits are inventoried; the physical S-number order is not the public bit order
for S1..S8, and game-specific meanings require a manual.

Use the public state as delivered. The matrix read path complements its bit into
the PPS/4 input, but no blanket application of another inversion is allowed. This
does not prove each physical contact's normally-open/normally-closed construction;
that field is deliberately withheld, especially on the mixed-level slam input.

The six segment callbacks are player 1 start 12 width 6, player 2 start 18 width 6,
player 3 start 0 width 6, player 4 start 6 width 6, Ball in Play start 40 width 2 and Credits
start 32 width 2. The last two callback regions describe parts of the auxiliary
display assembly rather than two additional four-digit panels.

## Drop targets and ball paths

- The isolated Ten at mid-left and two adjacent Jacks at center-left have switches
  21/22/23 and one reset solenoid, 6. Do not turn their shared reset group into three
  adjacent physical targets.
- The three Queens use switches 31/32/33 and reset solenoid 7.
- The right-side four Kings use 41/42/43/44. Their reset coil is **lamp driver 17**;
  the table's LampCallback detects its rising edge and calls `dtkk.DropSol_On`.
  It must not be rendered as a seventeenth lamp.
- The upper-left five-target Aces/Joker bank uses switches 50/51/52/53/54 and
  solenoid 8. Switch 52 is the center Joker.

Every drop handler calls the ordered cvpmDropTarget Hit method. A struck target
stays down, with its switch state held by that library, until the corresponding
reset output raises the group. Bank index order and script-controlled resetting
are known; factory linkage, reset-pulse requirements, travel/timing, jam behavior
and actual power-on physical state remain unverified. No arbitrary animation
speed or VPX launch value is elevated into a machine specification.

The retained script models a single-ball outhole with `InitNoTrough`, switch 66
and solenoid 1. Drain_Hit passes the ball to the stack; the BallRelease kicker is
the virtual serve point. A collected ball closes the occupancy state, and serving
removes it. A coil does not electrically actuate its occupancy switch. The exact
physical eject path/sensor position requires a drawing; BallRelease coordinates
are not claimed as outhole geometry. The right shooter lane and manual plunger
are separate passive mechanisms.

Two pop bumper scoring contacts share input 10. Eleven ten-point contact regions
share40: ten passive rubber regions plus the single left kicking rubber. The
secondary chart lists the pops, kicking rubber and three flippers as directly
switched coils, and the coin-lockout relay as directly grounded. These loads must
not acquire invented numbered CPU outputs. Their circuits, contacts, EOS switches,
power-enabling relationships and exact physical inventory still need primary
wiring. Passive gates near the top and at the serve path are visible in the VPX;
their real-machine mounting, one-way behavior and resting geometry are not yet
established sufficiently for a complete mechanism inventory.

## Scoring and lamps

The factory three-ball card spots Ten bonus on ball 1, Queen bonus on ball 2 and Ace
bonus on ball 3; completing the spotted sequence lights 5X. Completing target
groups lights their bonuses; completing the Ten/J sequence or another group
scores 5,000 and resets. Drops score 500 or5,000 when the matching bonus is lit.
Completing the A group or A-B-C lanes lights the Extra Ball/Special features. Pops
score 1,000. Bonus is scored and features reset after each ball. The card says tilt
does not disqualify the player. Operator-specific tilt penalties and three/five
ball settings require the manual; the photographed card is not a complete DIP guide.

Lamp1 is Q/game-over relay, lamp 2 is T/tilt relay, and lamp 3 is High Game to Date.
Lamps4 and8..16,18..28 map to the table's corresponding insert lights. The source
chart gives the complete candidate names, which include Aces/Queens/Kings/Jacks/
Tens bonus, the numeric 1,000..5,000 bonus ladder, Special, Extra Ball, A/B/C lanes,
Shoot Again and 5X. The Q/T relay contact-controlled backbox legends are recorded
in the excerpt, not silently counted as extra independent callbacks.

The three production chime outputs are3/4/5. The VPX defaults ChimeSound to0 and
uses alternate audio samples; this is a recreation preference, not evidence for
a production electronic sound variant.

The VPX forces its GI collection on and has UseGI=0. The secondary fuse list
describes a playfield/coin-chute circuit via the tilt relay and a separate name/
scene-light circuit. This does not establish socket count, complete routing or
exact physical positions. No synthetic GI callback address or consumer-specific
DOF/B2S mapping enters the canonical machine.

## Spatial audit and remaining work

The exact extraction bounds are 952x1927 VPX units, with x left-to-right and y
rear-to-apron. The official spatial helper produces six-decimal positions.
Bound target and rollover centers are observed interaction locations. Scoring-
rubber wall centroids remain candidate interaction-region projections; they do
not measure individual leaf contacts. The adjacent spatial JSON records every
source hash, the 1,031-file / 67,599,557-byte extraction manifest, object coordinates,
projection class and unresolved device.

The 21 script-bound lamp objects are insert/glow regions without shown bulb meshes.
Their object names are retained in the report for future reconciliation, but no
physical bulb position or quantity is inferred from them. There is no independent
factory drawing fit. Reset coils, outhole hardware and GI still lack adequate
physical coordinates. Cabinet/backbox controls use explicit not-applicable spatial
records; the diagram does not assign invented playfield coordinates to them.

To promote this record, obtain the factory manual/schematics for 417 SS; compare
the complete secondary tables and resolve all read-capable undocumented addresses;
establish contact construction, direct coil/EOS and GI topology, and all DIP
meanings; verify actual gameplay and mechanism sequences with the legal ROM/table;
then inventory every physical bulb/load and reconcile positions with exact table
geometry and a factory layout or independently measured physical source. No
source presently makes an incompatible physical claim that needs a conflict:
missing evidence is recorded as unknown/candidate rather than manufactured disputes.
