# Embryon (Bally, 1981)

Coverage is **partial**. The primary reviewed the [page 22 switch and coil tables](../../evidence/excerpts/bally.embryon.1981/manual-page-22.md)
and the machine's wiring, but the auxiliary high-selector semantics, some physical
emitter counts and some placements remain unresolved. This note distinguishes the physical game from behavior
implemented by the retained VPX table; neither the table's filename year nor its visual
helpers establish machine identity or wiring.

## Identity and displays

Embryon is Bally model 1222, June 1981, IPDB 783 and OPDB G4qk7-MNEjx. The pinned
PinMAME source (`by35games.c:1207-1259`, revision 46e1a01a0f73dc5ce163d98db1ae435883ecc450)
declares six drivers. The physical root `embryon` uses six-digit player displays starting
at segment positions 2, 10, 18 and 26; `embryona` through `embryone` use seven-digit
player displays starting at 1, 9, 17 and 25. Credits and match/ball-in-play are two-digit
at 35 and 38 in both layouts. The five conversions are compatible, not identical display
hardware. Their differences beyond this display layout remain to be reviewed.

## Inputs and outputs

The factory switch identification table lists all 40 matrix positions. The shared inputs
include four rebound contacts at 1, three rollover buttons at 2, two contacts left and
right of the outhole at 5, three tilt contacts at 7 and two slam contacts at 16. The
single-drop target has a normally-open target-down contact in series with a normally-closed
back-target contact; composite switch 17 rests open and the back hit breaks it with the
drop down. Both contacts belong to the same public input ([wiring](../../evidence/excerpts/bally.embryon.1981/switch17-series.md)). PinMAME's `FLIP_SW(FLIP_L)` does not copy
the synthetic column into matrix 3: a right-button action must assert matrix 3 as well
as synthetic 82; synthetic 84 is the left button. The other generic flipper bits have no
ROM read path. Matrix 41–48 is unwired on this machine: the
[page 22 list](../../evidence/excerpts/bally.embryon.1981/manual-page-22.md)
enumerates forty positions and [Embryon's W-1192-29c wiring](../../evidence/excerpts/bally.embryon.1981/switch-column-fitment.md)
fits only ST0–ST4. PinMAME can read a sixth column via PB7, but that line drives
the fitted Flipsave coil 20 here; transport capability does not establish contacts.

The [reviewed option-switch transcription](../../evidence/excerpts/bally.embryon.1981/manual-pages-10-12.md)
assigns S1–5, S9–13 and S17–20 to the three coin chutes; the other switches select
game-feature memory, credit limits and display, match, replay limits, attract voice and
ball count. The primary checked every table cell against the native scans, including
the dense 32-row coin-pricing table and its printed blank cells.

The raw, fresh-state native run `review-artifacts/embryon-1981/harness/solenoid-run-1.json`
(SHA-256 `afdc30c3cd55e345e1b1bb53f158967599840bc5277945f75dbaa7ea96ada3ba`)
shows the factory self test mapping 01–15 to public 14, 15, 10, 11, 12, 13, 6, 5,
1, 2, 3, 4, 18, 19 and 20 respectively. `tools/embryon_runtime.py` checks the recorded
display samples and public rising edges against that run. All four retained fresh
runs show a startup pulse on the whole continuous bank 17–20, including coin lockout
18, flipper enable 19 and Flipsave 20. Each set of rising callbacks and each set of
falling callbacks spans less than 1 ms during the initial wait, before scenario
switch actions; exact per-address timestamps and raw hashes are in
`tools/seeds/bally/embryon-1981-solenoid-self-test.json:startup_continuous_bank`.
The service run's 17 rises at 5.755705 s and falls at 5.822109 s as part of that bank.
No later output-17 transitions occur in any of the four retained runs.
These are host callback times, not measured emulated or physical coil timing.
Pinned `by35.c:357–359` complements PIA1:B's high nibble with `data ^= 0xf0` and
maps it to all four continuous outputs via `(data & 0xf0)<<12` (source SHA-256
`91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2`).
This explains the shared-bank public state; the exact firmware instruction and
why the ROM initializes the bank remain untraced. [Embryon's solenoid sheet](../../evidence/excerpts/bally.embryon.1981/solenoid-fitment.md)
independently shows PB4/CONT.2 (public 17) with no load. That absence plus the
explained bank pulse supports `unused` 17; transitions establish no physical fitment.
The same sheet marks decoder outputs 7–9 N/U.
The right synthetic output pair 45/46 and left pair 47/48 are held together. They do
not measure the power and hold windings or EOS timing. Output 46 represents the lower
and upper right flippers and 48 the lower left flipper; 45 and 47 are duplicates.

The [factory coil list](../../evidence/excerpts/bally.embryon.1981/manual-parts.md)
specifies AQ-25-500/34-4500 for those three flippers and AO-27-1300 for Flipsave.
The three-bank resets use the printed NO26-1900; the single reset, saucer and outhole
use AO-27-1300. Bumpers use AN-26-1200, slings AO-26-1200, the knocker AR-26-1200,
and coin lockout FO-36-7000. Lockout is a coil; output 19 operates the flipper-enable
relay. These part numbers do not imply a voltage or an emulator power/hold waveform.

The machine's GI is fixed 5.9 VAC and has no public GI channel. The newer corpus script
uses solenoids 18 and 19 for visual backglass and playfield GI, but those public outputs
are coin lockout and flipper enable on this machine. Treat those script bindings as a
visual convenience, not physical wiring.

## Ball path and mechanisms

The exact retained table's embedded script initializes a two-ball trough (`InitSw 0, 8,
5`), serves through `BallRelease` on output 5, and models a saucer at switch 4 released
by output 4. The [factory rules](../../evidence/excerpts/bally.embryon.1981/manual-rules.md) describe locking a ball in that saucer and releasing it
with the single-target back contact; a subsequent player may release a locked ball with
the right button. Startup resets the drop targets. An empty trough or a stuck outhole,
saucer or switch can prevent the expected serve or release; switch 5 represents two
physical contacts, not two separately addressable inputs.

The script creates three drop assemblies: top switches 20–22 reset on output 3, left
switches 25–27 on output 2, and the single target at 17 on output 1. It also creates
five captive or messenger balls at `k28`, `k3433`, `k34`, `k33` and `k17`; its central
trigger transfers motion to two inside balls, and its outer triggers act only with the
corresponding drop target down. The physical arrangement uses four messenger balls, two
behind individual drops and two moved by a fifth shared ball. The exact motion and speed
are table tuning, not timing measured from the physical mechanism. Making A and B enables
Flipsave; the right outlane switch 14 then starts the five-second flipper on output 20.

Two free balls and five captive balls give seven physical balls in total. The left outer
ball sits behind the upper target of the left bank and works switch 28; the right ball
behind the single drop works its back contact at 17. In the central assembly a shared
messenger transfers momentum to two inside balls, sensed at 34 and 33. The four outside
contacts 29–32 are standups rather than separate captive-ball sensors. Completing them
enables the spots-letter feature; inside hits then add letters, with two letters and
a flash for simultaneous hits. S21/S22 control how many outside lamps light and their
memory. Recreate the physical containment and momentum paths rather than using five
freely rolling balls. A captive ball that escapes its cage, a sticking standup or a
misaligned inside ball breaks this causal chain; the table's speed thresholds are tuning.

On switch 17 the retained table queues a TRUE-then-FALSE pulse and manually raises the
target. The physical sequence is: target up and switch 17 open; target falls and closes
17; the back hit breaks the NC contact and its return closes 17 again; the ROM fires
reset coil 1, whose raised target clears 17. Two fresh-state runs, each with two breaks,
confirm the reset pulses after restoration. Their compact evidence is
`tools/seeds/bally/embryon-1981-single-drop.json`; the reproducible stimulus is
`tools/harness-scenarios/by35/embryon-single-drop.json`. The 150 ms break is a test
stimulus, not a physical contact or coil specification. The table's TRUE/FALSE pulse
and forced raise simplify that sequence; see the [script and library excerpt](../../evidence/excerpts/bally.embryon.1981/runtime-bindings.md).
If a drop target sticks up or down, its switch or the shared series contact can prevent a
feature from advancing; a stuck trough, outhole or saucer contact likewise prevents the
expected ball routing. Reset, contact closures and the physical ball's location must be
reconciled at startup. The manual's five-second Flipsave is a rules time, not a measured
coil travel or animation speed.

The [manual's play rules](../../evidence/excerpts/bally.embryon.1981/manual-rules.md)
describe bonus beginning at 1,000 and advancing through targets and lanes; outlanes add
two advances. Making lanes 1 and 2 progresses the multiplier and top-center lane awards.
The top three-bank collects the currently lit feature, with operator switch 6 affecting
whether its first completion collects or flashes it. The left and right outer captive
targets advance their respective values when the associated drop targets are made; the
central target group advances the letter feature. Spelling EMBRYON lights the lock saucer.
A tilt forfeits the ball's bonus and disables flippers and bumpers; slam ends the game.
The option switches govern memory, coin pricing, replay limits, match and balls per game.

The generic library's stale `BallRollTilt` switch 2 convention is wrong for this game:
the retained script sets its nudge tilt switch to 7, while 2 is the rollover buttons.
Detailed travel, tuning, recovery after jams and some exact physical placements remain open.

## Lamp and spatial limitations

The [reviewed main-board mapping](../../evidence/excerpts/bally.embryon.1981/main-lamp-map.md)
has only 52 and 63 unfitted; a board connector's N/U may describe one branch of an SCR
that drives a backbox lamp on another branch. Public 56 drives the A10 flasher board with
four #921 flasher lamps and one #44 lamp in the A10 control circuit. The #44 lamp's
physical purpose, visibility and socket location are unknown. The total quantity of five
does not establish that all five are visible flashers. Public 59 is the apron credit indicator.
The seven playfield letters and seven backbox letters have separate addresses.
The four #921 lamps are in series, so one open bulb interrupts that whole flasher
string.

The A9 auxiliary schematic has 27 fitted loads; 117 and selectors 7 (72, 88, 104,
120) are unfitted. The four selector-7 positions have no SCR, while `by35_lampStrobe`
suppresses only selector 15 and captures shared data writes on this blank row.
Their startup and normal-operation pulses therefore do not add physical bulbs.
Native non-service traces also activate main 52/63 and auxiliary 117. Although their
loads are N/U, their firmware use is not established, so public availability stays
unknown. Their firmware use remains distinct from the explained 17–20 bank pulse
and the independently unfitted continuous output 17.
Selectors 8–14 alias physically because A9 does not receive AD3, but PinMAME stores
separate bits; their semantics stay unknown. A9 and W-1255 disagree over whether the
right/left captive-ball lamp counts at 70/86 are 2/1 or 1/2. Owner tracing of A9J2-6
and A9J2-13 and counting their bulbs is needed; photographs did not identify circuit
membership. No bulb position is inferred from an insert overlay, reflection
or script-only light. See the [spatial report](../../reports/spatial/bally/embryon-1981.md).

The exact v2.0.2 table supplies 65 separately modeled bulb anchors on 64 circuits,
including the two blue-shield lamps and the four bumper bulbs. These are observed
coordinates, not an independently calibrated factory layout. The remaining socket
gaps are the three star rollover lamps, apron indicators, captive-ball circuits and
all five loads on circuit 56. Switches 1/5/8 also lack defensible individual anchors:
the older table adds virtual rebounds and its trough abstraction does not identify
the real below-apron contacts. A drawing fit or clearly attributable socket photos
are needed before promotion; retained IPDB photographs did not resolve the circuit
membership or those missing anchors.

The standard runtime bundle is `evidence/runtime/by35/embryon-1981-harness.json`.
It records each raw-run/scenario hash, the native binary and ROM archive fingerprints,
fresh-state conditions, service mapping and run-attributed action observations. Detailed
segment pairings, held-state samples and reset edges remain in the pinned JSON seeds.
Committed scenarios differ from the retained, hashed originals only by CRLF-to-LF
normalization; the evidence tests compare those exact normalized bytes.
