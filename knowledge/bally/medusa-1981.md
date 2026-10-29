# Medusa (Bally, 1981) recreation knowledge

Coverage: **partial**. The controller address space and physical mechanisms are
enumerated. Extra auxiliary lamp-state semantics and physical socket placement
remain open; this is not an author-ready definition.

## Identity and physical edition

Bally game 1245, FO713, IPDB 1565, September 1981 manufacture. February 4 was the
project date, not the manufacture date. IPDB's live record was verified against
its title, manufacturer and model; its resources and physical photographs are
retained outside Git. The reviewed OPDB identity is G4xXQ-MDWW1. Sources:
[IPDB](https://www.ipdb.org/machine.cgi?id=1565), the own-game manual cover and
the [1981 Bally parts catalog](https://www.pinwiki.com/wiki/images/d/d6/Bally-Parts-Catalog-1981.pdf),
Medusa printed pages 46–49. Factual transcriptions and immutable artifact hashes are
under `evidence/excerpts/bally.medusa.1981/`.

The public catalog has production `medusa` and Oliver's 2004 free-play
`medusaa`. The latter aliases the production initializer, inputs and display
layout and retains its sound ROMs. It is compatible firmware on the same
physical machine, not a 2004 edition. Debug-only `medusaf` is not a public
catalog member. No new driver or physical-family grouping is invented.

## Controller contract

Pinned PinMAME 46e1a01a declares GEN_BY35, Squawk & Talk BY61B, eight auxiliary
lamp columns, FLIP_SW(FLIP_L), and hw.display 0x10. Read INITGAME2's own macro:
the final 0x10 is a display bit, not BY35GD_ALPHA or another game's flag.
Public switches 1–48 are sequential matrix positions; 5 and 7 are explicitly
unused. Direct diagnostics are -7, -6 and -5. The matrix's own normally open contact
symbols and the unmasked read path establish construction and public closure
separately. Consume public PinMAME state as delivered; do not reinvert it.

The physical flipper buttons are cabinet-wired. Bally.vbs writes 82 (right)
and 84 (left), and the enabled core synthesizes 45/46 and 47/48 respectively.
Both members of a pair are meaningful state; neither measures winding timing.
The ROM reads no flipper column, and other81-88 positions add no controls.
The matrix's printed MOVABLE FLIPPER END OF STROKE41 is used as zipper-open
feedback by the retained script, and the schematic says it closes when the
movable flippers are open. The evidence does not identify which assembly leaf
stack supplies it; do not invent an extra contact or a separate winding-EOS
address. Preserve the position feedback without treating where the mechanism
parks as contact construction.

Momentary outputs1-15 are decoded driver selectors plus1. Printed self-test
01-15 agrees on Medusa, established by the ROM display rather than assumed
from another Bally. Continuous18 is coin lockout and19 is K1 flipper enable.
20 mirrors the sixth switch strobe.17 mirrors PB4, the extra playfield-display
data strobe: W-1255-1 wires feature-display6A1J1-15 to A4J4-5, and pia1b_w
loads the sixth BCD latch on the selected0x10 edge. N/U Q17 load wiring does
not make that display state dead. The complete trace is in `pinmame.md`.

## Solenoid expander and memory bank

AS-2518-66 routes seven driver lines through relay-selected alternatives.
Lamp34/Q38/A5J3-25 drives its relay/optocoupler and internal indicator.
At lamp34=0, public1 is knocker,2 right-bank reset,3 top-bank reset,4/5/6
drop top targets2/4/6,8 outhole. At lamp34=1, the same addresses select
zipper open,zipper close,top targets1/3/5/7,and saucer. The retained script
adds24 before its local callback dispatch. Local callbacks25-30/32 are never
public controller addresses. The emitted definition represents the shared
loads at their real public binding and explicitly records the relay relation.
Shared actuator ownership is recorded once under `mechanism.expander`; each
physical mechanism describes its selected load.

Seven Olympus targets run left-to-right switches48..42. They mechanically
stay down until reset. The ROM can re-drop remembered targets individually;
a recreation with only a bank-reset coil loses that behavior. The right bank
has four targets A(top) through D(bottom), switches4..1 and a shared reset.
The parts catalog's generic memory drawing illustrates four targets with a
blank suffix; use Medusa's own ASE-3038-4 panel row for the seven-target build.
Its pictured coil count is not transplanted. A held target in the exploratory
run provoked repeated resets; model physical release after a successful reset,
and treat persistent closure as a failure condition rather than a second hit.

The retained table orders its top target bank sw48, sw47, …, sw42 but reverses
the knockdown callbacks against the factory A3 wiring and printed identities.
For example public 3 with lamp 34 on selects target 1, while local callback 27
calls SolHit 7. Canonical effects follow the factory drawing and ROM self-test
mapping; the callback reversal is a table defect.

## Zipper, Shield post, ball path and displays

The upper flippers rotate for the normal left/right buttons and translate as
one linked assembly. Separate reset and latch coils open and close the zipper;
the exploded ASE-2397-4 assembly shows the springs, latch, sliding links and
two flipper bases. A top target closes the zipper. It opens when the timer
expires or the ball leaves the upper area. DIP8 selects accumulating ten-second
awards versus resetting the interval. The script uses alternate open/closed
flipper objects and writes41 itself; these are a model of four total physical
flippers, not six fitted flippers. Exact movement speed and contact-center
measurements remain table-owned/unvalidated.

Shield of the Gods is one rubbered post between the lower flippers, assembly
ASE-2593-7, requested by cabinet button17 and pulsed by public7. Each game
starts with five post credits; lane shots add credits and unused credits score
10000 each at bonus. The script's plunger plus two alternate walls model one
post impulse and return. Do not turn these three helper objects into three
physical posts or wire the cabinet button directly to a permanently raised post.

The one-ball outhole sends the drain to the manual shooter. Saucer19 at the
upper left holds its ball until the gated public8 pulse ejects it. The table's
ball-stack eject and collection points are routing aids, with angle/speed
constants chosen by its author. No extra ball trough or factory timing is
inferred from them. A ball remaining on the outhole or saucer contact can
provoke another ROM kick; a recreation should clear its contact as the ball
physically leaves and retain failed-eject/jam behavior.

Four seven-digit player score regions and two two-digit credit/ball regions
are in the backbox. The playfield six-digit feature module has three two-digit
windows: Extended Play Time Units, Like Numbers and Shield of the Gods Bonus.
medusaDisp publishes those at indices6/7/8, segment starts42/44/46. The trace's
extra rendered DMD callback is a display convenience, not a physical DMD.
Three left targets in sequence stop the left like-number digit; four right
targets stop the right. Equal stopped numbers award an extra ball. Last-ball
extended play delays final bonus until its time units run out. The own manual
awards10 units for left1-2-3,5 for the right bank,1 for saucer and lit A/B.

## Physical wiring and table defects

The own-game Figure V and isolated ROM responses pair bumper37->coil12
(upper right),38->11(upper left),39->10(lower right),40->9(lower left).
The retained table places37 on its upper-left object,38 lower-left,40
upper-right. That is a table handler defect; the definition follows the
physical drawing and independently observed response. Its slings map
34->15,35->14,36->13. Cabinet17->7 and tilt15 disabling19 were also observed.
Host switch readback is stimulus, never a claimed ROM observation.

The operations table calls12 a KICKER, but the matrix, target object and
Medusa's own parts row identify a left-side top standup. No extra kicker coil
is added. A5J2's broad TO BACK BOX bracket includes circuits the playfield
wiring actually fits on the playfield. Follow the per-pin own-game harness,
not that blanket bracket, for location. All60 main channels and28 physical
auxiliary circuits are transcribed with connector and SCR details.

## Lamps, GI and remaining evidence

All legal main and auxiliary public slots are enumerated, including unused
or unresolved slots absent from the script. Main lamp34 is an internal relay
gate,50 has an explicitly N/U sole branch. Auxiliary S7 is unconnected on
each decoder. A9 latches three address bits and has28 SCRs; the emulator
nevertheless exports60 auxiliary bits. Twenty-eight high-selector slots lack
independent physical SCRs and have no settled normal-operation runtime
meaning. They stay conspicuously unknown, without guessed bulb fitment.

The A9 board drawing duplicates #4 at J2-18; the own playfield sheet explicitly
calls that wire #14, settling it. Both sheets duplicate #3 at A9J3-11, where
the table puts Olympus bar position15. Its physical identity stays candidate
pending a real harness/socket trace. The table drives three visual top-target
sites from main47; the wiring names TOP MIDDLE BACK TARGET, so the physical
bulb count and branch fitment are not assumed. Main59's credit indicator has
an apron proxy; no physical socket position is asserted from it.

Normalized coordinates use the retained 952×1974 table, x=0 left, x=1 right,
y=0 rear/backglass, y=1 front/apron, at most six decimals. The exact table has
21 separate rear-bar bulb primitives. Their world-space bounds, checked against
four independently positioned bumper-cap controls, supply observed bulb
placements; the duplicated-label position remains candidate. Insert/target
Lights and GI/flipperlight helpers establish no sockets, so their coordinates
remain in the extraction artifact. Display and mechanism locations remain
observed projections. A coarse Figure V outhole fit puts the mouth above the
table's Shield post, contradicting their physical order; the failed measurement
is retained and its coordinate withheld. The spatial report lists every
projection, missing position, rejected measurement and unresolved output.

The own-game GI diagram supplies5.9VAC and shows upper-flipper NC contacts
switching the translucent lower-flipper lighting. The table instead toggles GI
from game-on/ball count and dims flipperlight helpers with lower callbacks.
Those visual effects do not prove wiring, emitters or physical GI quantities.
The29 GI helpers and eight flipperlight objects have not been promoted to
sockets. IPDB's full/upper/lower, display, zipper-underside and NOS images and
all42 Pinside gallery thumbnails were retained and inspected; the available
underside-looking Pinside view is the coin door, not a playfield socket survey.

A clear factory playfield underside/socket survey, Olympus bar A9J3-11 trace,
credit-indicator/target-lamp fitment and a reconciled outhole position are still needed. These are
concrete physical evidence gaps. Current sources are enough for the recorded
behavior and bindings, while those remaining gaps keep coverage partial.
