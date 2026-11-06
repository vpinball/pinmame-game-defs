# WWF Royal Rumble (Data East, 1994)

Coverage: **partial**. Production widebody game, model 500-5523-01, IPDB 2820,
OPDB G57y6-MLej6. All 64 matrix inputs, service controls, eight flipper-column
positions, 64 matrix lamps, 50 exposed solenoid slots, backbox display and the
mechanisms below are enumerated. The remaining blockers are physical bulb/socket
placement, the right diverter's physical motion contract, the configuration input
at PIA2 port A bit 7, and meaningful printer byte semantics. This is not an
author-ready definition.

## Identity and variants

IPDB's retained machine page identifies production from April 11 to June 17, 1994.
Pinned PinMAME 46e1a01a groups wwfr_106 (CPU 1.06 / display A1.02), wwfr_103
(CPU 1.03 / display wfdisp0.400) and wwfr_103f (CPU wwfcpuf.103 /
display wwfdspf.101). US 1.06 uses wwfcpua.106/wwfdispa.102; US 1.03 uses
wfcpuc5.512/wfdisp0.400. All share wfsndu7.512 and wfsndu17/21/36.400. Their game-data
initializer, GEN_DEDMD32, 128×32 display, DE2S sound hardware, FLIP6364 and printer
flag are shared. All three sets' members match the source's SHA-1 and sizes.
The French CPU/display archive was acquired from archived IPDB and assembled
externally with unchanged shared sound members from the authorized local set.
All three variants completed isolated switch, lamp and coil sweeps.
No physical hardware override is established for those firmware revisions.

IPDB documents early art/plastic variations, a test game with three lower-playfield
magnets, and an earlier narrowbody whitewood. Those are not silently folded into
the production inventory. Its recollection about possible Japanese cabinet magnets
is explicitly uncertain and supplies no production device or emulator binding.

## Evidence and authority

The complete English manual is retained externally, SHA-256
28764502c13c3db27dce6ea619bc5a0dea7a39c348d0d1844fb999a6667f62db. It has 90 scanned
pages and no text layer. Every page was rendered at resolution derived from its
embedded scan and OCRed through lossless native-pixel tiles using Windows.Media.Ocr.
OCR is a search aid. The factual excerpts under
`evidence/excerpts/data-east.wwf-royal-rumble.1994/` were visually checked by the
project curator. They preserve full switch/lamp/coil/flipper regions, blank and
unused cells, connectors and transistors, shared headings and printed disagreements.

The exact authorized table from `Tables Archive` is retained and extracted with
vpxtool git:v0.33.3. Bounds are 1093×2162 VPU, x left→right and y rear→front.
Its embedded script selects wwfr_103, loads de.vbs, uses HandleMechanics=0 and
HandleKeyboard=0. The extraction manifest's game label wwfr_106 identifies the
family's representative, not a claim that this table selects 1.06. The retained
table's own script, rather than similarly named corpus files, supplies its bindings.
Related scripts are ancestry evidence, not independent corroboration. The 1.10
corpus file has duplicate SW26_Hit declarations; the retained table is checked
separately. No claim of a new interactive VPX playtest is made in this session.

The newer VPU7733 2.0.3 VR release is also retained with its original ZIP and
1,482-file extraction manifest. Its embedded script selects wwfr_106; the public
page's wwfr_103 entry is stale metadata. HauntFreaks and 32assassin explicitly
describe ancestry from the 2017 table, so matching geometry only supplements
that source. The corrected parent inventory records scripting32assassin,
HauntFreaks and manufacturerDataEast. No acquisition timestamp was captured:
the source-page mtime and download-completion mtime are disclosed as file metadata.
Reuse requires author permission; table, script and artwork remain external.

The raw LibPinMAME traces and DMD frames are external. Fresh isolated state is used
for each run; exact visually read title bands checkpoint Active Switch Test,
Lamp Test and Cycling Coils. Unknown title frames match nothing. Public host writes
are stimuli, never ROM observations. The ROM's displayed names and output changes
are retained as separate observations with pixel hashes. No trace proves a socket
location, contact construction or physical fitment merely by toggling.

## Controller contract and physical wiring

The manual's N.O.–COM diode circuit and uninverted PIA switch-row read establish
the ordinary matrix contact convention. Public 1 is a closure; the zero per-game
inversion mask must not be reapplied by a consumer. No opto is fitted in the
documented trough: it has six subminiature contacts and a seventh release contact.
TAG is switch 62, separate from the Extra Ball button 8 and the shooter contact 16.
The VR corpus script reverses only one of its TAG key paths; that is not hardware
polarity evidence.

Drive the flipper buttons at public 84 (left) and 82 (right). PinMAME copies them
into 63/64 on every update, so writing the matrix copies directly is ineffective.
It synthesizes pairs 45/46 right and 47/48 left from button state while 23 enables
the flippers. Those pairs are simultaneous virtual states, not measured winding
timing or four independent flipper drives. The hardware has four flippers on two
SSFB boards, with distinct lower and upper coils, 50V DC power and 8V AC hold.
The retained table moves both same-side flippers together. Its upper-column writes
cannot supply independent upper-flipper state to this ROM.

The A/B relay is solenoid 10. Drivers 1–8 switch between left coils and right
flash circuits 25–32; they are not independent physical transistors. The game's
own Cycling Coils observations pair 17–22 with left/bottom/right turbo, left/right
sling and upper-right diverter, respectively. This is specific to WWF: the
Data East special-line permutation is not sequential and no invented SP1–SP6
aliases are introduced. 23 is game-on/auxiliary enable, 24 and 33–36 are gaps,
37–44 expose the printer byte, 45–48 are synthetic and 49/50 are simulator/reserved
slots on a game with no simulator. WWF declares no custom outputs at 51 and up.

General illumination is the relay-controlled circuit at 11, not a GI callback.
The exact script darkens its GI collection while 11 is energized. The relay is on
the power supply; the emitters span the game and their complete quantity is unknown.
The complete physical chart identifies 14 and 15 as unfitted even though a coil
test may sweep their drivers. A pulse is not fitment evidence.

Each flasher circuit includes backbox insert-panel bulbs as well as playfield bulbs.
All eight circuits fit four bulbs each, 32 No.89 bulbs in total. The 8R chart
misprints one playfield and two insert bulbs, while its own schematic draws four
and labels two playfield/two insert, the socket parts table lists 32 bulbs, and the
ROM prints “2-INS 2-R/UPPER”. The definition follows those agreeing regions and
preserves the literal chart misprint. The manual chart calls Q30 PPB while its
schematic draws CPU; VUK assembly pages specify 24-940 where the coil chart says
23-800, and the right-VUK contact part also differs. These are part/wiring notes,
not unresolved semantic conflicts.
ROM service descriptions are functional labels, not a physical socket survey:
for example output 27 says 3-INS/1-MACHOMAD while the manual schematic and chart
specify two playfield/two insert. The total agrees; the manual controls fitment.

Bounded static evidence improves the configuration/printer explanation without
settling their physical semantics. All three CPU members have identical reviewed
reset, normal PIA setup, IRQ and fatal-blink regions. Normal setup writes
DDRA=$FF, so the 6821 direction mask removes external PA7. Reviewed IRQ reads
discard PA; the fault blink loop uses DDRA=$10 and only bit4 survives its output
mask. Indexed calls, the scheduler and indexed-memory aliases remain gaps, so
this is not a whole-program unused-input proof or a WWF jumper identity.

Actual buffered printer code reads $0A00 and writes PIA2 PB only after CRA IRQ2
reports input CA2 ready. Stock s11 supplies CA1/CB1 service inputs but no CA2 ready
transition. The reviewed helper therefore times out before its PB write from
fresh reset, explaining the silent adjustment53 probes. PA7 does not supply that
separate handshake. No runtime printer transaction, complete protocol or global
absence claim follows. `pia2-static.md` and `tools/wwf_static_evidence.json` retain
the compact facts; the original 23-file analysis stays external and immutable.

## Ball paths, mechanisms and physical behavior

Six free balls start in the trough; a separate captive ball is permanently on the
playfield. The table initializes trough switches in 14→9 order, feeds a release
station on 15 with output 1 and ejects it with output 2. Physical lock-ball cam,
trough release and shooter auto-launch are separate assemblies and actuators.
The shooter contact is 16 and output 3 launches the ball. The script's plunger key
operates TAG, so do not invent a manual-plunger switch from that key name.

Output 4 ejects the upper-ring saucer at 28. Output 5 is the right VUK detected
at 20 and sends the ball into the wire ramp. Left/middle scoop balls pass under
trough switch 39 before reaching contact 40 and output 6's VUK. The script's
destroy/create transfer and 200 ms pulse of 39 approximate the subway. They are
not a measured ball travel time. Preserve contact occupancy and ball motion;
do not wire a reset/eject coil directly to a ball contact.

The lower four-target D-A-E-D bank has contacts 21–24 and common reset 7; the upper
WWF bank has 30–32 and reset 9. Target-down contacts stay closed until their common
lift restores them. The two three-standup TAG banks use 33–38, and the captive-ball
contact is 47. The manual's generic two-target-bank parts are shaded as not fitted.

There are three diverters: rear panel 12, upper left 13, upper right 22. Each has
a coil, plunger/linkage, paddle and spring, and no enumerated position sensor.
The table uses level-following rear/left callbacks and a timer-driven alternating
right paddle with two collision walls. The physical right paddle's home and whether
the real action is held or toggled are not established by a drawing of the parts.
The script's initial divstate=false, dropped TRDiv2, angles and animation speed are
table-owned facts. Observe an operating production assembly synchronized with 22
before replacing this uncertainty with a physical state machine.

The shaker is a cabinet motor at 16 with no position sensor; the script comments
out its callback, while the manual and coil test establish it. The cabinet knocker
is 8. The three turbo bumpers and two slings use local contact physics plus
ROM-controlled auxiliary coil outputs; PinMAME does not synthesize them through
ssSw. Starts and resets initialize raised targets and the six-ball stack in the
retained recreation. Contacts remaining occupied after an eject/reset indicate a
jam or failed transfer; no unsourced universal timeout or mechanical speed is imposed.

## Spatial audit and remaining work

The report and `tools/wwf_places.json` disclose each raw object, transformation,
projection, excluded proxy and unplaced address. Table-bound target, gate, bumper,
trigger and kicker objects support observed sensor locations. An actuator may
project onto its own mechanism's ball seat or target-bank midpoint with that role
stated. The rear collision flipper lies outside the playfield and is excluded;
primitive positions are not trusted without their world-space mesh bounds.

One additional observed placement is the actual L61 bulb mesh at the left turbo
bumper, matching the manual's physical location drawing and fitment. L62/L63 are
actual modeled bulb bodies too, but their script addresses exchange the manual's
lamp-location drawing: printed 31 places62 front/bottom and 63 rear/right, whereas
both related tables bind 62 rear/right and 63 front/bottom. Printed page 29 separately
places switch 50 rear/right and 51 front/bottom, matching the table despite the
Bottom/Right switch labels. Do not force lamp wiring to match those names or
sensor addresses. The two explicit spatial conflicts need production lamp 62/63
test illumination or socket matrix wire pairs. Their raw bulb geometry remains
in the lighting audit; disputed physical coordinates are withheld. The compact
lamp/switch drawing excerpts make this distinction reviewable. There are 65
observed placements; coverage remains partial with unresolved_conflicts added
to the other four missing dimensions. The generated score is 69%, not progress
credit for uncertain coordinates.

`tools/wwf_lighting_audit.json` separately records the newer GI collection's 77
members and 38 own meshes, versus 36/36 in the older table, including added
GI_034/GI_036. Neither the collection nor a generic bulb flag establishes a
physical socket and electrical membership. The seven old flash mesh objects at
29/30/32 overlap or lie near GI render bulbs, and the newer table removes their
bulb meshes during its lighting overhaul. No socket-specific reconciliation
settles those bodies. They remain explicit candidates; no bulb is counted twice
or discarded from physical fitment merely because the newer model hides it.
The newer table adds cabinet lamp 15, keeps the same alternating right-diverter
implementation, and reverses just its plunger TAG path after key-handler guards.
These are source-specific notes, not new physical devices or polarity evidence.

IPDB identity/manual and Pinside's full 29-image archive were checked. Pinside
includes upper-ring, underside, cabinet and backbox views, some with aftermarket
lighting. They corroborate layout and assembly presence but do not expose every
production socket or establish all G.I. wiring membership. No whole manual or
community table is committed. Their copyright remains with the original owners.

Four concrete blockers remain:

- Complete physical emitter count and locations, especially G.I., all mixed
  flash circuits and matrix lamps represented only by insert polygons/glow. A
  calibrated underside/upper-ring socket survey with wire colours, or a complete
  factory socket layout, can settle them. The available partial photos cannot.
- An operating production right diverter observed against output 22, including
  home/startup and successive commands, to settle its physical behavior.
- WWF printer-interface observations or ROM analysis establishing meaningful
  data at 37–44. The initializer exposes the byte. US 1.03 and 1.06 reached
  adjustment 53 and pressed Start, as printed on manual page 24, without a
  printer-byte transition. The DIP=1 successor probe was also silent. This
  bounded absence cannot make the addresses unused or establish a fitted load.
  The verified CA2-ready guard now explains silence in the reviewed send helper;
  it does not exhaust all indexed/scheduled firmware paths or reconstruct the
  physical printer protocol.
- The WWF-specific meaning of the shared core's DIP bank 0, read into PIA2
  port A bit 7. DE_COMPORTS does not declare System 11's Country DIP. A raw
  DIP=1 probe neither identifies a physical jumper nor proves a country setting.
  Verified normal DDRA=$FF and the reviewed discarded/masked reads narrow the
  uncertainty, while indexed/scheduler gaps prevent an exhaustive unused claim.

Normal-play probes must wait for the start presentation before transferring the
exit-most trough contact 14 to release contact 15 and shooter contact 16. Earlier
successors changed occupancy during that presentation and are diagnostic only.
Successful successors on all three variants establish switch 49/50/51 → coil 17/18/19 and
19/27 → 20/21, plus cabinet 82 → simultaneous synthetic 45/46 and 84 → 47/48.
Host ball transfers remain stimuli, not observations of a simulated mechanism.
The French default pricing needed ten coin6 pulses before Start; the earlier
two-coin French probe remained in attract and proves no normal-play response.

The deterministic curator reproduces the definition, identical seed, this note and
spatial report. Tests pin excerpts, source roots, retained bytes/manifests, topology,
addresses, title checkpoint behavior, coordinates and fail-closed partial status.
