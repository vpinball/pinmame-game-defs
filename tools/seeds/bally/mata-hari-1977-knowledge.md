# Mata Hari (Bally, 1978)

**Partial.** The controller contract, mechanisms and six firmware variants
are documented. The complete factory GI socket inventory and validation of
observed playfield positions remain open.

## Identity and ROM hardware

Bally model **1104-E** is the solid-state Mata Hari, IPDB **4501** and OPDB
**G417e-MDvXz**. September 26, 1977 is the project date and April 1978 is the
production date. The definition uses 1978 as the physical year. The stable
machine ID uses 1977. The separately built electromechanical Mata Hari,
IPDB **1557**, has relay/score-reel hardware and is outside this ROM
definition. [Identity and ROM evidence](../../evidence/excerpts/bally.mata-hari.1977/identity-and-roms.md)

The factory MPU is the AS-2518-17. The FO 579 parts list gives the A4
assembly as AS-2887-6 and heads its module drawing AS-2518-17. The
supporting boards are A3 AS-2518-22 and A5 AS-2518-23. Sound comes from
four mechanical chimes and a knocker. There is one manual plunger and one
ball in play. The DIP setting for three or five balls is the number of
turns per player. [Factory parts and self-test](../../evidence/excerpts/bally.mata-hari.1977/self-test.md)

| PinMAME driver | Recreation and physical fit |
| --- | --- |
| `matahari` | Factory two 2 KiB U2/U6 images. Four six-digit scores. |
| `mataharc` | Quench Free Play+ uses two 2716-format images in the BY17 map. S18/S19 on enables free play. S17 off counts down and S17 on clears credits at Start. The credit field goes blank at zero and the indicator stays on. |
| `mataharb` | Oliver free play uses two 2732s. S17–19 on preserves at least one credit after the first coin. Player one displays revision 02 at power-up. |
| `matatest` | Oliver PCK-Bally revision 7 uses two 2732s and its own option assignments. S25 and S26 together replenish one credit from initialized zero, S27 shows credits, S28 enables Match and S31/S32 set 2–5 balls. S23 sets the initial saucer award. |
| `matahard` | Quench V22 uses two 4 KiB ROMs with BY35 addressing. S17/S18 enable 99-credit free play and S19 off selects six-digit virtual millions. S29 extends the award table. Settings 13–16 configure the modified rules. |
| `matahard7` | The same V22 program uses `dispBy7` and S19 on. Route the millions strobe from MPU J1-7 to each Bally player display J1-12 or Stern player display J1-11. The auxiliary module keeps its two two-digit fields. |

The BY17 and BY35 loader names describe ROM address maps. The game data
for all six drivers still uses GEN_BY17. The factory and Free Play+
images load at 0x1000 and 0x1800. The 4 KiB loaders continue the images
at 0x5000 and 0x5800 and reload U6 at 0xf000. PinMAME's Quench change
explicitly calls for -17 to -35 address compatibility. Bally's
service bulletin gives different settings for an AS-2518-35 and an
AS-2518-17 modified under F.O. 597, each with the factory U2 E-725-21
and U6 E-720-20 ROMs. The Quench EPROM configuration depends on the
board and chips being fitted. Its display strobe uses an additional
harness wire. [Bally MPU service bulletin](../../evidence/excerpts/bally.mata-hari.1977/mpu-service-bulletin.md) ·
[ROM evidence](../../evidence/excerpts/bally.mata-hari.1977/identity-and-roms.md)

Free Play+ and V22 both suppress repeat scoring when a down target
contact reopens and recloses. V22 also adds simultaneous-drop scoring,
operator-selectable tilt-through protection, higher bonus multipliers,
new A/B and outlane options, and extended diagnostics. In native play
the seven-digit variant displayed 1,172,400, while the six-digit variant
alternated 172400 and 117240 for that score. The
[variant operator charts](../../evidence/excerpts/bally.mata-hari.1977/firmware-variants.md)
include the exact DIP settings, awards and software options.
[Native follow-up](../../evidence/excerpts/bally.mata-hari.1977/native-followup.md)

V22 Audit 12 retains the highest end-of-game credit balance before
Match in free-play Credit Reset (S17/S18 on and setting 13:3 = 0).
With S20 on, High Game to Date shows the record in the credit field,
including between balls. The self-test sequence shows the saved value
on the player displays in every credit mode, including with S20 off.
[Audit 12 read paths and native controls](../../evidence/excerpts/bally.mata-hari.1977/firmware-variants.md#v22-audit-12)

Oliver's revision-7 chart resets the saucer progression after the 5X
bonus countdown. It changes the A/B ladder, advances twice on the A+B
skill shot, lights the lower caps separately and awards 50,000 at the
right outlane with 3X lit or the left with 2X lit. The retained
erased-CMOS test needed a first coin. With previously initialized
memory and S25/S26 both on, the ROM replenished a zero credit balance
and served a ball without a coin. Each of the other three settings
left the initialized zero balance at 00. With the tested coin pricing,
each of the three chutes capped at 25 credits across all four S25/S26
settings. The ROM's credit-limit lookup uses an incoming register
value separately from the DIP check for the floor.
[Oliver operator evidence](../../evidence/excerpts/bally.mata-hari.1977/firmware-variants.md)

## Recreation

- **Serve and drain.** The ball returns below the centre drain to the
  normally-open outhole wire (8). Start with the ball on the wire.
  Public 7 moves the ball to the right shooter alley and 8 opens as the
  ball clears it. The manual shooter sends the ball up the right arch
  past the passive one-way ball gate. Upper returns and the side
  guides feed the A/B lane switches and the bumper field. Lower feeder
  lanes 25/26 feed the flippers and the two outer lanes 33/34 drain.
  The VPX hides the transfer behind its `Drain` and `BallRelease`
  objects. Physical serve travel and timing are unmeasured.
- **Top saucer.** The centre cup holds the ball on 32. Public 1 kicks
  it back into the upper field. The VPX's always-on `Umagnet` models
  the cup lip. The physical assembly has a switch and a kicker.
  The conservative native run awarded 3,000 per visit and attained 2X,
  3X and 5X on visits two through four. Kick vector and cup dwell are
  table tuning. [Wiring and parts](../../evidence/excerpts/bally.mata-hari.1977/solenoid-wiring.md)
- **Drop banks.** Each angled bank has four independently scored
  targets. The right bank is 17–20 and the left 21–24, each ordered
  D, C, B, A from bottom to top. A target stays down with its contact
  held closed and the reset drive releases its latch. Reset outputs
  are 13 left and 15 right. The stock probe closed the eight switches
  cumulatively. The first complete bank stayed down. Completing the
  second pulsed both resets and lit 51. FO 579 gives 50,000 for the
  first full completion and the Special on the second, subject to
  award-mode DIPs. The VPX delays the graphical reset 500 ms. That
  figure is a script delay. Release the four inputs when the bank
  has returned up. Each bank has one NO-26-1900 coil and plunger
  at its outer end. The plunger lifts one common reset arm on the
  bank. A target spring draws the face forward onto its catch, then
  pulls it down when a ball pushes it back. An obstructed reset can
  leave a contact closed. A6 draws two symbols per reset branch.
  The parts lists, production underside and Charlton's teardown settle
  the fitted quantity. Both older VPX scripts number the physical right targets from top to
  bottom. Use Bally's bottom-to-top numbers when binding a
  recreation. [Factory drawing](../../evidence/excerpts/bally.mata-hari.1977/factory-locations.md) ·
  [Bank construction](../../evidence/excerpts/bally.mata-hari.1977/drop-bank-restoration.md)
- **Upper rebounds.** Each rubber behind a bank has a 10-point contact.
  The two contacts are wired in parallel into 27. The VPX uses two
  upper sling-style collision handlers, while the factory drawing
  shows passive scoring rebounds.
- **Thumpers and slings.** Round bumper skirts operate 37/38/39/40
  and the two lower slings use 35/36. The isolated ROM closures fired
  11/8/10/9 and 14/12 respectively. This defines the public pairing.
  The physical switch is a short action. Bind the lower right cap
  to factory lamp 41 (Q42, A5J3-21) and the left to 57 (Q56,
  A5J3-10). In the stock three-ball run, the first A/B completion
  lit both public addresses and each lower bumper went from 100
  to 1,000 points. Both lamps stayed on through the next two
  completions. With S16 on the five-ball trace lit the left cap on the
  first pair and added the right cap on the second. The same-lineage
  tables and UnclePaulie's v2.0.0 drive both caps from 41.
  Keep the two bindings separate to preserve Bally's behavior.
  [Native runs](../../evidence/excerpts/bally.mata-hari.1977/native-runs.md) ·
  [VPX bindings](../../evidence/excerpts/bally.mata-hari.1977/vpx-bindings.md)
  Bally specifies yellow cap part A-3713-35 for the two
  upper, 100-point bumpers and A-3713-29 for the lower pair.
- **Flippers and tilt.** Public buttons 82 and 84 drive the
  synthetic 45/46 and 47/48 pairs through the enable condition.
  Relay 19 is held in play and fell on tilt 7 in the stock probe.
  Each physical dual-winding coil has a local EOS switch. The
  cabinet button and K1 are outside the switch matrix, and the
  synthetic pair has no winding or EOS timing. The cabinet plumb
  bob, roll cage and under-playfield tilt share 7. The service
  drawings show two possible slam contacts on 16, while the
  operator text specifies one factory door contact and permits
  extras. A regular tilt forfeits a ball and its bonus. A slam
  stops the game and restarts the power-up sequence.
- **Lane and operator adjustments.** Top and side rollovers let the
  player make either A or B via two routes. Each lane letter has two
  lamps on one address. The central bonus ladder runs through 1K–10K
  and 20K. The A/B ladder, saucer potential and achieved multipliers
  have separate lamp circuits. Figure II shows adjustable post
  positions at outlanes and slings. The FO 579 switch tables separate
  cabinet option switches S1–S32 from public matrix positions.
  [Options and panel parts](../../evidence/excerpts/bally.mata-hari.1977/parts-and-options.md)

## Controller and evidence limits

GEN_BY17 uses five fitted switch columns on this game and the
shared native driver can select a sixth. The factory has no
sixth-column harness. Diagnostic -7 is the door test, -6 the MPU
button, and -5 reaches the sound diagnostic hook without a fitted
sound board. The public matrix uses active-high closures with a
zero inversion mask. This driver declares `FLIP_SW(FLIP_L)` with
zero `FLIP_SWNO` fields, so the core does not copy the cabinet
buttons into the game matrix. Its zero `lampCol` leaves 60
addressable feature lamp drivers across four strobe groups of 15
on the main board. The physical GI branches
are transformer-fed and unaddressed. The virtual game's relay-driven
GI state is a visual choice. [Switch wiring](../../evidence/excerpts/bally.mata-hari.1977/switch-wiring.md) ·
[Lamp wiring](../../evidence/excerpts/bally.mata-hari.1977/lamp-wiring.md)

The ROM's all-lamps service test exercised all sixty available addresses.
The coil sweep confirmed FO 579's printed-to-public mapping. The stock
PIA register test explains the brief boot assertion on unfitted 17 and
20. The stock ROM's whole-byte writes to the A/B strobe also drive
unfitted lamp lines 4 and 20 in attract and play. In `matatest`, the
revision 7 attract handler at `$13c2`–`$13ca` complements the entire
strobe byte at `$0203`, including both unfitted bits.
[Stock ROM read path](../../evidence/excerpts/bally.mata-hari.1977/stock-rom-read-path.md) ·
[Revision 7 attract handler](../../evidence/excerpts/bally.mata-hari.1977/derivative-dip-read-path.md#revision-7-first-attract-interval)

All 26 follow-up traces show lamps 4 and 20 changing together and one
boot pulse per spare solenoid. In all 17 traces for drivers other than
`matatest`, every spare lamp edge shares a callback timestamp with at
least one fitted A/B lamp (36 or 52), and some A/B events occur separately.
In the nine `matatest` traces, the overlap is 12 of 42 spare-edge timestamps
in seven runs and 15 of 51 in the other two.
[Per-driver trace accounting](../../evidence/excerpts/bally.mata-hari.1977/native-followup.md#spare-outputs-across-all-six-drivers)

S14, S15, S22 and S29 are fitted MPU DIP switches that the stock option
routines mask out. In Oliver's exact revision-7 `matatest` program, S14
and S15 seed the first A/B attract interval. Quench V22 uses S29 in its
award selector on `matahard` and `matahard7`. The checked derivative
paths show no S22 effect, and its use across unresolved indexed paths
leaves input semantics partial. [Exact derivative read paths](../../evidence/excerpts/bally.mata-hari.1977/derivative-dip-read-path.md)

The production underside photo gives an observed panel tilt mount and
coarse reset actuator anchors. Nine feature-lamp circuits now have
observed socket anchors from the registered photographs and independent
VPX models. The factory drawing validates the drop-target and rollover
anchors. Four lower side-guide GI positions have visible sockets on the
production underside. The 3,000 arrow and upper caps light on a restored
machine and are plausible GI loads. Their factory routing, the complete
GI socket inventory and the remaining placement validation also keep
the definition partial. [Spatial report](../../reports/spatial/bally/mata-hari-1977.md)
