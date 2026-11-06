# Phantom of the Opera (Data East, 1990)

The definition remains **partial**. It now distinguishes the complete controller address space,
physical circuits, script workarounds and measured table candidates. Remaining requirements are
listed by dimension in the adjacent spatial report; observed geometry does not grant author readiness.

## Physical identity and firmware

IPDB 1777 identifies Data East model 500-5508-01, manufactured from January 1990. This agrees with the
PinMAME production title and OPDB `Grq1D-MQokp`. The pinned driver family is `poto_a32` (3.2), `poto_a31`
(3.1), `poto_a29` (2.9). All use the same poto initializer, `GEN_DE`, `FLIP1516`, `DE1S` sound, three identical
sound ROMs and two 16-character alphanumeric display rows. There is no physical-layout override.
The catalog's module name `de_mDEAS1` is not the generation: the actual generation is `GEN_DE`/0x1000.

IPDB describes an early promotional installation with external speaker/amplifier work and red
lamp boards. It does not identify a different supported playfield or driver. This definition does
not infer a separate physical edition from firmware dates or promotional audio equipment.

## Controller contract and physical wiring

The full game inventory covers switch matrix 1-64, negative service inputs -7/-6, flipper-column 81-88,
the inherited public DIP-style configuration bit 0, lamp matrix 1-64, public solenoids 1-50 and two display callbacks.
No custom solenoids or extra matrix columns are declared. Addresses 51-64 are a platform outer bound
without a game-specific custom device, rather than an omitted physical device inventory.

Sequential public addresses are column-major: col=(n-1)//8, row=(n-1)%8. The manual's printed
diagnostic wire codes and full source-literal tables are retained in
`evidence/excerpts/data-east.phantom-of-the-opera.1990/`. The game's open-contact matrix schematic,
zero inversion initializer and uninverted `pia4a_r` read establish normally-open contacts. The organ
service procedure independently says its two limit contacts are electrically open midway.
The cabinet service contacts are also drawn normally open. The maintained/toggled Green input
is a runtime convention, separate from physical contact construction. The CPU schematic shows
PIA11B PA7 pin 9 connected both to RA4, a 4.7K pull-up to +5V, and to jumper J8 to ground.
The CPU Board Assembly Drawing independently labels J8, and the complete CPU Jumper Table
documents it installed for Phantom CPU Ver 2, ROMs 5B,5C. The documented factory PA7 level is
therefore low; removing J8 lets RA4 pull it high. PinMAME configuration bit 0 supplies those raw
levels through `pia2a_r`: value 0 corresponds to grounded J8 and value 1 to the removed jumper.
This is a physical CPU jumper in the backbox, not a DIP-switch bank. Its firmware purpose remains
unresolved: the inherited Williams Country/W7 name does not establish Phantom's meaning.
The definition now includes `input_semantics` among its missing requirements and keeps this
device's semantic provenance candidate. Its documented factory installation is not a survey of
every surviving board. Use PinMAME's public state as delivered; never apply another platform-wide inversion.

Drive the left cabinet flipper at 84 and right at 82. `core_updateSw` copies these to matrix 15/16 on
every update; direct writes to 15/16 are overwritten. It also fabricates left 47/48 and right 45/46
while 23 enables the flippers. The table subscribes to hold callbacks 48/46. Its `de.vbs` library can
write upper staged bits 88/86, but the game has no upper flippers and cannot read that column through
its eight-bit matrix strobe. The two physical 23-900 coils and solid-state flipper board must not be
counted as four independently driven CPU outputs or modelled EOS inputs.

Public 10 energizes K1 on the PPB and selects the R branch of the eight shared transistors: L01-L08
publish 1-8; R01-R08 publish 25-32. The only populated R branches shown are outhole 25, trough 26,
left VUK 27, top super VUK 28 and right super VUK 29. Public 11 controls the power-supply GI relay.
The retained table switches its GI collection from both 10 and 11; that extra 10 handler is a table
simplification, not another physical GI circuit. No separate GI callback group exists here.

Special solenoids must not be numbered from the SP suffix. The own-game wiring and pinned PIA
permutation give SP1 right bumper 17, SP2 center bumper 22, SP3 left sling 18, SP4 left bumper 19,
SP5 right sling 21, SP6 unfitted 20. Alpha INITGAMES11 leaves ssSw empty: PinMAME does not synthesize
these switch-triggered hardware firings, and a quiet gameplay trace does not disprove the fitted
coil. The VPX collision objects supply bumper/sling recoil themselves. Their separate point and
trigger contacts are not duplicate public sensors. The own-game special schematic's CN16 trigger
header differs from the table/backbox list's CN18; this is a retained wiring note, not a different
physical device.

## Ball storage and returns

The game uses three balls. Outhole switch 10 reports the drain catch; coil 25 returns that ball to
the trough. Trough contacts 11-13 report its three positions, and 26 feeds the manual shooter lane 14.
The table incorrectly routes its nudge TiltSwitch to Slam Tilt 7 instead of Plumb Tilt 1;
this is a recreation defect, not a change to the physical cabinet contacts.

The table initially sets three balls in `bsTrough` (13/12/11 active), transfers drain balls directly
into that virtual stack and subscribes 25 to its stack-input handler. Its direct 26 subscription is
overwritten by `ballreleasehack`, which suppresses the last trough ball unless the left stack holds
two balls. Preserve the useful startup state while recognizing that this is a table workaround,
not a physical electrical interlock or a fourth trough sensor.

The left VUK/lock has two ball contacts 28/29 and release 27. The table keeps them in `bsSaucer`,
releases one ball per command through sw28 and uses `Kicker1` to raise it into the left wire ramp.
That helper adds no physical actuator. The two physical sensor centers are not both established
by the single retained kicker coordinate.

The organ/cavern and Magic Mirror route through below-playfield subway assemblies. Top super VUK
switch 36/output 28 and right super VUK switch 44/output 29 are separate occupied catch/eject pairs.
Organ Cave 37 and Mirror Ramp 45 are path contacts. The table implements the hidden passages with
enabled invisible triggers and `DestroyBall/CreateBall` transfers through helpers; these approximate
continuous physical ball travel. It clears 36/44 as an eject begins and raises the new ball before
kicking it. Table heights, increments, angles and velocities are recreation tuning.

The left-outlane Laser Kick uses switch 17 and coil 16. Its `Plunger1` object returns a sensed ball
only when the ROM commands it; a switch closure alone is no causal assertion that the coil fires.
The three standup banks contain left 33-35, organ 41-43 and right 49-51. These are nine standups,
not drop targets. Spinner 23 reports a rotating target on the right; 30/31 detect the catwalk ramp
at its top and bottom. The hanging Magic Mirror uses a spring return and leads to the subway;
its gate and the spinner are passive physical parts, not extra solenoid outputs.

## Raising organ

The organ is a hinged ramp/hood in the upper-right playfield. A 25 VAC motor drives a rotary crank
on assembly 500-5212-00-08. Q25/public 14 energizes its relay board; the machine exposes no separate
motor-direction output. Two 180-5052-00 switches report Open 52 and Closed 53, closing just before
their respective endpoints. Both open midway; simultaneous closure is a fault. The manual's
Organ Test pulses the relay repeatedly while Start is held and displays the two contact states.
The complete Playfield Parts list (PDF 33 / printed 29), transcribed as all 74 rows in its own
excerpt, identifies the Organ Motor as 041-5001-00. The motor/bracket drawing separately names
motor assembly 515-5256-00-08 and the complete mechanism assembly; these are different part levels.

The retained script initializes the organ down/closed with 53 active and 52 clear. Each energizing
callback alternates animation direction. At its raised limit it asserts 52 and clears 53, disables
ramp collision and opens the cavern shot; at its lowered limit it asserts 53 and clears 52 and
restores collision. Initialization comments call the endpoints backwards; the executable values
agree with the manual. Its 0-60 animation counter is not measured motor travel or cam geometry.

Completing the three organ targets or the lit shooter-lane skill shot opens the organ. The manual
describes a first capture/release, then locking two balls before a countdown expires for three-ball
play; serving the third ball releases both stored balls. During three-ball play an organ-target
hit opens the organ for a timed jackpot shot. These rules and operator-dependent timing remain
ROM-owned. Five fresh-state reactive probes now exercise two candidate cam widths/speeds from closed and
midway starts, plus a jam model with both limit contacts open. Closed startup does not move the
motor; midway startup drives until Closed 53. Completing the organ bank drives until Open 52,
then a timed return stops on Closed 53. The jam probe produced three automatic attempts, each
stopping after about six host-clock seconds. In Organ Test, Start held still produces repeated
short pulses independent of the limits. These are ROM observations against synthetic host
feedback; the model's phase, cam widths and motor speed are not physical measurements. The raw
traces, scenarios, exact adapter hash, binary/ROM hashes and computed stop summaries are retained
in the compact organ evidence. Do not infer additional undocumented failure modes from this probe.

## Lamps, flashers and GI

The manual enumerates 63 fitted matrix lamp positions and unused 56. The generic schematic draws
all 64 symbols and the location drawing prints a leader-less 56 on the organ; neither overrides the
explicit unused lists. Lamp 25 is Left Circle in the two description lists and drawing, despite the
matrix printing Right Circle. Lamps 39/40/47/48 belong to the backbox insert panel. Lamps 49-55 spell
PHANTOM on the upright rear playfield panel; they are not backbox devices.

The table reads `ChangedLamps` into its fading arrays and explicitly binds its insert lights; it
does not use `vpmMapLights`. Its matrix lights have no shown bulb meshes. They are retained as
insert-center projection candidates. Rear f49-f55 are Flasher sprites and cannot establish sockets.
The extra `NfadeL53`,`S108b1` organ glow and direct animation writes are a lighting defect, not another
physical lamp 53. Its inactive pseudolamp 115 path and render helpers add no physical bulbs.

The own-game flash schematic establishes totals and the backbox inset separates 16 insert-panel
flasher sockets from the remaining playfield bulbs. Circuit 1 is all three backbox mask bulbs;
2/4/5/6/7/8/15 mix playfield and backbox, while 3/9/12/13 are playfield only. The exact per-circuit
totals and split live on each output. The table's few Light objects and five Flupper dome anchors
simplify those circuits. No glow or dome origin is counted as an additional socket.

The twelve observed VPX GI bulb-mesh placements are the shown-bulb members of paired table lights.
Odd-numbered glow doubles, lone `GI_25` and bumper glows are excluded. The source's 32 collection
members do not give a physical quantity. The full playfield, apron, cabinet, backbox and rear GI
socket survey is still missing. The manual's parallel bulb symbols on two fused branches are not
two bulbs per branch or an inventory.
The observed status applies to the retained table's visible meshes; it does not validate factory
socket identities, quantities or a complete physical inventory.

## Knocker and unused branches

Several owners independently inspected production machines and found no knocker, strike plate,
spare holes or wiring. That agrees with the game's PPB connector list marking the R08 destination
N.U. and drawing no load. The isolated R08 label on the coil-location drawing identifies no actual
knocker and does not outweigh the connector and direct inspection evidence. The table's 32 knocker
sound is a recreation addition. Physical absence is settled separately from the public address:
the ROM service sweep names R06/R07/R08 UNUSED COIL and pulses them, explaining public 30-32
without physical fitment. Public 20 remains unknown: no SP6 load is fitted and the recorded
service/gameplay probes did not publish it, but a quiet PIA line alone is not proof of a dead address.

A bounded static ROM pass now accounts for the known control-register writes. PIA1 CRA is `$2401`;
the normal configuration routine writes it from shadow `$0102`, initialized to `$38`. Its `$38/$3C`
values hold CA2 high/inactive. An adjacent indexed PIA test can toggle CA2, but its straight-line
sequence disables the special-solenoid gate first, and normal reset jumps over that test.
The remaining gap is indirect event dispatch at ROM `$45ED` (`JSR 0,X`) and indexed-store ranges
that could reach the shadow or CRA. The pinned ROM-analysis excerpt records the exact target,
tool, addresses, source contract, conditional inferences and unresolved frontier. This is static
analysis; it does not claim ROM execution, complete reachability, or a new unused classification.

## Retained evidence and reproduction

The manual is the original IPDB 1777 PDF, hash `1feebf59ab838056591fd67853bd2b54a9524447038e2a7a2c7ad3fe4765cd09`.
The exact VPU 1.25 VPX hashes to `e609fdfe0c358957ac2314f298cc6236523a62cd5cd6b979d0c1bc4f475e3bd9`;
its embedded script hashes to `e373bf66dab343166e954fb2a7ed9c1ee0d8627ae5e125b13e4339b46757d5f6`.
The full case-sensitive extraction manifest covers 2699 files/272164712 bytes and hashes to
`029e0bdb66b39060e5de73294a1f9cd5b72f5615ea1ecab2c10ec282091e0c12`. It is reproducibly recomputed
by `tools/build_external_evidence_manifest.py`, excluding only its manifest files. Full manuals,
tables, source-owned photographs and ROM bytes remain outside Git. The Pinside owner excerpt is a
paraphrase of the retained capture with named post locators, rather than a redistributed forum page.

Run `python -B tools/curate_phantom_of_the_opera.py` to reproduce the canonical definition, seed,
knowledge note, excerpts and blocker report; `--check` refuses drift and an existing author-ready
artifact. Optional evidence roots enable exact external hashes and full extraction reconciliation.
The compact service evidence retains both successful all-direct runs, raw display segments,
wire/bank frames and exact ROM, scenario, binary and manifest hashes. Drive host inputs only as
stimulus; host switch readback is not independent ROM evidence.

The focused tests additionally check identity, public enumeration, physical/type distinctions,
projections, rejected helpers, mechanism topology, provenance and guards that fail under mutation.
