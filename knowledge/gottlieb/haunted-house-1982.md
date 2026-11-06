# Haunted House (Gottlieb, 1982)

This definition remains **partial**. The controller address space, production and firmware variants, physical switch assignments, controlled loads, displays and mechanisms are now documented from Haunted House's own sources. Public lamp 4 still pulses at ball serve without an explained fitted load. Several physical lamp/GI sockets lack defensible positions, and all current positions remain observed. The exact missing dimensions are in the definition; the companion spatial report lists the unplaced devices and projection limits.

## Physical identity and evidence

Gottlieb game 669 is the four-player, single-ball Haunted House released in June 1982, IPDB 1133. It uses System 80, four six-digit player displays in the lightbox, a four-digit credit/ball status display there, and a six-digit Monster Bonus display below the cellar window on the main playfield. The existing resolved OPDB identity G5BP6-MJK4Z remains unchanged.

The main floor, raised attic and opposite-playing-direction cellar are three physical levels of one machine. There are eight flippers, four pop bumpers, a four-drop attic bank, five-drop cellar bank, two separately controlled hole kickers, two up-kicker circuits, a hinged trap door and a passive roll-down Secret Passage target. The physical game has a manual shooter; a script impulse-plunger helper at the right-side kicker is not another shooter assembly.

Evidence retained outside Git:

- The final-edition instruction manual from Pinside, SHA-256 168a1bc2e2198b03154835d45471eb5b3910f1619930c5c3fd48f9b86ad8c21f, under `manuals/by-machine/gottlieb.haunted-house.1982/`. All 63 pages were rendered/OCRed. Mapping cells were visually checked on native renders; OCR was a search aid.
- Two separately copied/extracted local cyberpez VPXs under `vpx-sources/gottlieb/haunted-house-1982/`. Their filename labels do not establish release versions; embedded version metadata is blank. Both use 1116×2186 bounds. Exact original/table/script hashes and reproducible extraction manifests are pinned in the evidence seed and source records. The related builds supplement one another; they are not presumed independent physical measurements.
- The pinned VPW2.1.1 script corpus, standalone-script comparisons, pinned PinMAME 46e1a01a source, IPDB identity/photos and the modification authors' own documents.
- Fresh-state native ROM traces under `runtime-evidence/haunted-house-1982/`, with compact reproducible evidence in the repository. Exact emulator, ROM archive/member, run and scenario hashes are retained. No ROM, NVRAM, complete manual, VPX, source photograph or full trace is committed.

Reviewed factual transcriptions and drawing crops are under `evidence/excerpts/gottlieb.haunted-house.1982/`. The definition's source records link every excerpt and digest. Manual wiring establishes physical construction; scripts establish runtime bindings; PinMAME establishes public transport. A script helper's name is not physical evidence.

## System 80 contract and polarity

Switch numbers are decimal strobe/return pairs 00–77 with last digit 0–7. The game uses strobes 0–6; printed 37 explicitly says strobe 7 is not used. Cabinet return 7 carries 07 Self/Test, 17 left coin, 27 right coin, 37 centre coin, 47 Replay/Start and 57 tilt. Plumb-bob and ball-roll tilt contacts share 57. Keyboard handling must remain off when a host writes that cabinet return directly.

The switch matrix is unmasked and read without complement, so public 1 is the closed normally open leaf. Physical slam contacts are normally closed: PinMAME's dedicated-1 is 0 at rest and 1 when the contact opens/slams. Consume that delivered state without another controller-wide inversion. The sound-test button is dedicated-4. Video-only dedicated positions and unused flipper-column positions are explicitly enumerated as unused.

PinMAME's synthetic cabinet flipper buttons are 112 right and 114 left. The CPU never scans that column. While game-on 10 is true, core synthesizes 45/46 together for right and 47/48 together for left; these are virtual states, not four fitted driver transistors or measurements of power/hold timing. The separate green buttons and physical EOS contacts have no CPU addresses.

All 42 DIP ordinals are enumerated. 1–32 are CPU switches, 33–40 sound/speech SB1, and 41–42 belong to the unfitted sound-only board. The complete printed pricing, German chute exceptions, fixed settings and sound-bank table are transcribed. Factory 31 is required OFF; 32 is labelled Background Tone, though the modification authors report it was not implemented in stock software. Modified ROMs reuse 31/32 for award difficulty; do not carry factory settings into them blindly.

## Controlled outputs and printed-number traps

The game's own Step 17 coil test agrees with its printed 14 Note A and printed 38 wiring:

| Public solenoid | Physical device |
| --- | --- |
| 1 | Main top-centre hole kicker, A-16570 |
| 2 | Main vertical up-kicker, A-5194 |
| 5 | Attic four-target reset, A-18102 |
| 6 | Cellar lower-hole kicker, A-16570 |
| 8 | Cabinet knocker, A-5195 |
| 9 | Outhole release, A-5195 |

Outputs 3/4/7 are optional mechanical coin counters: left/right/centre on ordinary wiring; German 4/7 interchange centre/right. Their omission from Step 17 is explicitly described by the manual. The gameplay coin probe exercises them; a pulse does not prove that a particular cabinet has a counter fitted. 10 is the synthetic game-on state from lamp 0 on with lamp 1 off; 11 is the synthetic copy of lamp 1. PinMAME does not publish 12–44. 45–48 are the synthetic flipper states above.

Many other actuators are on lamp drivers:

| Public lamp | Actual load |
| --- | --- |
| 0 | Q/game-over relay |
| 1 | T/tilt relay |
| 2 | Coin-lockout coil |
| 12 | Cellar K relay, A-20558 |
| 13 | Cellar five-drop reset, boosted by Q3 |
| 15 | Right-side help kicker, boosted by Q1 |
| 16 | Trap-door coil, boosted by Q2 |
| 17 | U/playfield selection relay |

The general coil chart on PDF 21/printed 17 lists A-5195 for knockers and A-16890 for Q, T and coin-lockout relays, but explicitly warns that coil usage varies by game. These general applications remain part candidates for the cabinet knocker and coin-lockout coil; their exact winding parts are omitted because the game-specific coil table does not assign them. That table does positively assign A-16890 to Q, T and U. The complete general chart and its qualification are retained in the parts excerpt. PDF 54/printed 50 independently places the Q, T and U relay assemblies among the middle-playboard underside components; assembly numbers MA-224/225/231 are distinct from winding part numbers.

The PDF 29/printed 25 Z1 Q3 driver region identifies the coin-lockout coil, A3 Q3 and A3J5-2, but omits the winding, wire and supply. The cabinet drawing on PDF 46/printed 42 shows A3J5-2 wire 877 continuing through A12J7/P7 pin 8 to the front-door coin-lockout coil; its other end connects to pin 7 and wire 222. The rectifier drawing on PDF 45/printed 41 labels wire 222 +24V DC. The winding part number remains unknown.

Lamp 12 does not directly drive the cellar up-kicker winding. K's normally open contact applies 38VDC to a separate A-21741 coil; the relay's own supply is 24V. Its scoring/occupancy switch is 31. The lower hole 41/public 6 is a different device. Keep this topology when simulating the return path.

Public 3 operates the main Shoot Again bulb and the lightbox bulb printed L2 through the common A3 Q4 collector; public 2 remains coin lockout. The driver sheet's printed L10/L11 names are reversed relative to latch order: public 10 is high game to date, public 11 game over. Their connector/legend and ROM behaviour settle that pairing. Public 9 is Sound16, not a lamp.

Public 48–51 are the complements of 44–47. Physical roll-down-arrow lamp 51 is on the real Q-bar output; it is complementary to roundabout 47, not an extra independent latch. 48–50 have no fitted load identified on the game drawing and are retained as virtual inverse states. 52–60 mirror solenoids 1–9 only in physical-output mode; binary lamp state stays 0. 61–63 are constant-zero reserved slots.

The all-driver test sweeps unfitted latch positions. Lamp 4/Q5/A3J2-2 also pulses during ordinary ball serve, with no load named by the game's wiring/assignment pages. Neither a lamp-test sweep nor an unexplained normal-play pulse establishes fitment, so this one address stays unknown rather than being silently called a bulb or unused.

## Mechanisms, ball movement and recreation behaviour

The physical one-ball drain/outhole closes 67; 9 ejects it to the manual shooter lane. The script's Kicker1..6 transport chain and configurable MaxBalls are conveniences, not a fitted trough stack. Start a fresh controller with the single ball where the recreation actually places it, and move occupancy when the ball physically leaves. The retained probe deliberately starts with 67 closed; it does not prove that every saved machine state parks there.

Attic drops 2/12/22/32 hold down until reset 5. Cellar drops 0/10/20/30/40 hold down until lamp 13 raises them. Clear each leaf on physical reset, not immediately after a hit. A completed bank produced its own reset in the retained ROM probe. The four upper spot targets 3/13/23/33 and main five-step target sequence are separate from those banks.

Main-entry troughs 6 and 16, the secret-passage trough 26 and trap-door trough 36 lead toward cellar play. In the probe 6 raises U/lamp 17; cellar up-kicker 31 raises K/lamp 12 and returns U to the main-level state. The lower special hole 41 ejects on 6 back into the cellar. Main cup 45 ejects on 2; top-centre hole 46 ejects on 1. Hold each occupancy contact while the ball remains present; pulse scoring leaves only for the physical duration of contact. The older script clears some occupied switches in callback bodies and does not consistently check falling callback edges, so copy its mapping rather than treating every timing detail as hardware.

The Secret Passage target is passive: ball force rocks the face about its shaft/fulcrum, a spring returns it, and the ball enters the downstream trough 26. There is no reset solenoid or published target-position sensor. The hinged trap door is different: lamp 16 drives A-17875 through Q2 and a lever/link/plunger; springs provide return. Matrix 36 senses the trough after passage. The local normally closed TRAP DOOR SW. is part of the coil circuit and has no published matrix address; it must not turn matrix 36 into a normally closed switch. Factory adjustment makes the closed plate flush to 1/64 inch above the playfield. Timing, spring constants and geometry remain table-owned; sticky links or a plate that does not close flush can catch a ball, so recreate mechanical travel rather than a teleport.

Red cabinet buttons operate the four main flippers. Green buttons operate the attic pair and the cellar pair under relay enable. The later VPW script keeps those controls separate; its optional coupled-control mode is user convenience. The older retained table reroutes red callbacks by lamp 17, which must not override the physical apron instructions and factory four-button wiring. All eight windings and EOS contacts are locally switched hardware.

Four bumper boards react to local switches: two main bumpers share 44, attic 43 and cellar 1. Shared scoring 42 has two attic 10-point leaves; 51 has two cellar 10-point leaves plus a kicking-rubber contact; 66 has main 10-point and kicking-rubber contacts. Preserve all contacts and their different physical roles. These reflex coils have no individual CPU solenoid callback. Controller scoring state alone must not be used to fabricate a CPU driver.

## Illumination

Q/T control physical common supplies, and U changes main/cellar illumination. The cellar's eight #313 bulbs are mounted under the main board around the viewing glass; a lower-floor render light is not their socket count or position. Attic illumination, bumper lamps, coin-door lamps and backbox lamps remain distinct branches. The lightbox's autonomous A11 timer/counter/decoder produces its animation without extra CPU lamp addresses; its parts sheet names 55 #44 and 3 #455 bulbs.

At 46e1a01a PinMAME GI 0 is an inverted physical-GI model of the T relay; binary GI 0 stays 0. It does not encode U's three-level wiring or this game's T-controlled 6VDC lamp-supply cut. The driver explicitly leaves that controlled-lamp power interruption unemulated, so a recreation must apply the documented physical supply gating without inverting the public matrix twice.

## Production and modified firmware

Factory hh_1 is through serial 4999; hh is revision 2 from 5000 onward. Both use GEN_GTS80, standard six-digit layouts and the sound/speech board with vacant U14, producing sound only. All nine currently catalogued Haunted House drivers remain attached to this physical machine; no virtual-only or unrelated multiball hardware is imported.

hh7 is Oliver's 2008 seven-digit conversion: player display widths become 7 at starts 2/9/22/29; credit/ball entries 40–43 and the six-digit bonus at 50 remain unchanged. It is compatible with the physical machine after the display conversion, not an identical stock display inventory.

Flipprojets 669-3 targets the non-speaking stock System 80 machine; 669-4 adds speech commands and needs the documented SC-01/sound-memory board conversion. Both restore the high-score inter-ball pause and reuse CPU 31/32 for extra-ball/special difficulty. A variants correct unwanted brief Extra Ball flashes when using LEDs. B includes that correction and changes the secret-passage rule: with the arrow unlit, the ball still physically enters the cellar but is immediately returned by software. It adds no new tunnel door or sensor. Revision 4's sound files are NO_DUMP in pinned PinMAME; no successful speech-ROM run is claimed. The authors' separate System 80A 669-z and the unrelated replacement-board multiball conversion are not drivers of this record.

For the modified ROMs, 31 OFF is conservative Extra Ball behaviour (main contacts alternate the award), 31 ON keeps it lit; 32 OFF allows each Special sequence only once, 32 ON resets it after the award. A/B work with ordinary bulbs too. The speech board additionally uses sound SB1-6 for speech enable and SB1-7 for Tilt/Slam voices; SB1-1 selects the normal/multiball message set and must select normal for this record. CPU and sound-bank ordinals are separate. These option differences are documented in the authors' current English PDFs as well as the retained website captures.

The official author sources are [PROM revisions](https://www.flipprojets.fr/PromHH_EN.php) and [speech hardware](https://www.flipprojets.fr/HHparlant_EN.php). Hash-pinned retained captures and concise factual extracts accompany the definition.

## Spatial evidence and remaining work

Global normalized coordinates use x0 left/x1 right and y0 rear/y1 apron. Exact bound collision objects supply observed sensor/mechanism anchors. Cellar items are projected vertically into that same global plan view, despite the opposite local playing direction. Reset effects are projected onto their own bank; they are not observations of winding centres.

Independent factory-drawing reads reconcile each physical level separately. Main controls span more than half the full field; inset control spans and all extrapolations are disclosed. Only distinct lamp symbols are measured; circled or leaderless L labels do not locate a socket. A separately documented display rectangle locates the Monster Bonus; the outhole sensor/effect use their own drawn bar, not Kicker1. Drawing measurements are rounded to three decimals and remain observed. The report retains all raw pixels, control objects, affine coefficients, errors and exclusions.

The manual's L8 balloon between the flippers disagrees with the physical Shoot Again legend and runtime binding; it is excluded. Local animation numbers 100/111, insert/glow centres, desktop-only lower-light offsets, out-of-bounds TrapDoor helpers and the GILower singleton are also excluded. No clamp, average or reflection is presented as a physical socket.

To promote: explain lamp 4's ball-serve pulse and physical fitment from a game-specific wiring/firmware proof; resolve all remaining controlled-lamp/GI socket positions and quantities against physical evidence; and validate the observed spatial records against the runbook's independent-table/drawing requirements. An emulator transition cannot identify an unseen lamp socket. The definition must remain partial until these requirements are met.

The coordinator also retained the official VPW2.1 table and a world-space OBJ export as supplementary evidence. Its 368 Light records have no `show_bulb_mesh` flag set. The exported Parts meshes contain many welded pieces whose physical roles are unclassified; neither a nearby lightmap nor an unclassified mesh fragment proves a socket. That source is pinned as a supplementary lead, without using it to fill the remaining lamp/GI positions.

The trap-door effect is an observed projection onto the specifically animated BM_pTrapDoor plate/linkage model, whose world-space bounds centre is recomputed from the OBJ. Four bumper-skirt/collision controls verify the coordinate frame. Manual construction and the physical photo identify the mechanism; the coordinate is explicitly its effect anchor, never an observed coil winding or the primitive's stored pivot. This follows the same mechanism-projection policy used for the K relay and bank resets.
