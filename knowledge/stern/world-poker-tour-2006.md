# World Poker Tour (Stern, 2006)

Coverage: **partial**. The full public address space and factory wiring are recorded, but the unresolved SW54/SW56 fitment, playfield mini-display placement, sensor polarity, and several socket placements prevent author-ready status.

## Identity and source order

All 46 pinned `wpt_*` drivers represent firmware/language versions of the same 2006 SAM game. The factory manual is authoritative for device parts, wiring, and physical mechanisms; the pinned known-working VPX v2.3.1 script explains ball routes and controller causality; PinMAME defines the public namespace. ROM Switch Test independently confirms SW3, SW21 and SW63 labels and their active public level. ROM switching alone does not prove a factory sensor's normal contact state. Bulletin 165 identifies a rule change: before v1.11, three dropped targets during serve auto-launched the ball; v1.11 and later spot the targets without an automatic launch. Recreate that behavior by ROM revision, rather than adding hardware.

## Ball transport and banked targets

Four ball seats SW18–SW21 are ordered left to right, with an extra stacking opto SW22. Q1 kicks one ball to shooter switch SW23. Player plunge or Q2 auto-launch sends it into play; a separate shooter-lane VUK has SW3/Q3 and exit gate SW51. The eject popper is SW49/Q21 and Q21 has its own 50 V step-up board. The left/backpanel VUK is SW55/Q4; SW56 and SW59 observe upper exit/transfer points, but SW56's printed construction conflicts with its chart entry. Maintain actual ball containment through both vertical tubes and the backpanel transfer. A sensor staying occupied after coil fire is a jam, not a successful transfer.

The right and middle four-banks have independent reset coils Q8 and Q7 and optical switches SW4–7 and SW10–13. The left eight-bank has individual optos SW33–40 and two reset coils Q5/Q6, one per four-target lift. Drops latch down until the matching lift raises them; keep each target's own hit state and collide with its raised blade. Weak springs, a bad lift bracket, or a blocked opto can strand a target down.

## Moving assemblies and routes

The Ace-in-the-Hole jail-bar/mouse-trap assembly uses Q12 to lift and Q19 to latch. SW57 reports bash, SW58 rest, and SW63 up. The bar and latch are physically distinct moving parts; move collision geometry with them and hold a sensed rest/up state at endpoints. Right ramp SW9 leads to SW52, with Q32 operating its down-post stop. Left ramp Q20 raises a ball-routing post. The factory left ramp made opto is labelled SW54, yet a distinct transfer-trough assembly and the VPX ScoopTrigger handler also claim SW54. Leave that circuit unresolved until a board-level continuity map or discriminating ROM trace establishes whether the labels are a drawing error or intentional shared line.

Four independent flippers use Q13–Q16 and dedicated D9–D16 button/EOS contacts. The two side buttons are double-stacked: halfway press closes lower normally-open D9/D11, full press additionally closes upper normally-open D13/D15. All four EOS D10/D12/D14/D16 are normally closed and open about 1/16 inch into travel. Factory p.129 specifies a 40 ms kick then 1 ms hold pulses every 12 ms, with a fresh kick on high-velocity forced rebound. The pinned working script enables both upper callbacks; the older embedded table comments them out. Each lower slingshot Q17/Q18 is fed by two leaf contacts sharing SW26/SW27. Pop bumper skirt/coil pairs are SW30/Q9, SW31/Q10 and SW32/Q11. The remaining orbit, spinner, target and lane switches are individually enumerated in JSON.

## Lighting and display

The factory chart enumerates Q22/Q23 and Q25–Q31 as nine flashers, five on the backpanel. Lamp matrix 1–80 has explicit unused 77; 1/2 are cabinet buttons, 3 is apron, and 67/68/75/76 are backpanel stand-up lamps. GI has four factory circuits on J15: upper playfield six bulbs, left edge/lower-right twelve, backpanel/coin door a production-dependent nine*, and lower-right six. LibPinMAME exposes only aggregate GI 0; circuit-to-output address assignment cannot be invented. The backbox DMD is 128×32. PinMAME registers fourteen 5×7 miniature DMD blocks physically on the playfield card display; the schema currently allows only nonlocated display spatial records, so their locations are intentionally incomplete.

## Spatial and authority limits

The 952×2250 VPX table gives exact stored object centres and six-place normalized coordinates. Each retained `lN` light and `swN` trigger/wall point is recorded only where its name and factory placement agree in broad region. A rendered glow, lightmap helper, or primitive stored offset is not proof of a physical bulb or sensor seat. Missing points include the apron Deal Again lamp 3, GI bulbs, flasher sockets, trough sensors and part of the ball mechanism; no guessed coordinates were filled. Five backpanel flashers and four backpanel matrix lamps are marked outside playfield space.

## Concrete blockers

- SW54 has two physically separate manual assemblies and two VPX assertions; SW56's grid and footnote disagree. Q32's chart/schematic and its specific assembly drawing name different coils. ROM and board schematic settle Q32's orange J6-P10 supply against the chart's brown error, but an installed-coil inspection must settle its part. Confirm factory wiring or inspect installed assemblies.
- Most switch factory contact polarity, especially optos, is not established by the sampled active-high ROM test; a wiring/ROM inversion trace must settle physical normally-closed claims.
- The playfield poker-card mini-DMD layout cannot be represented as located displays by the current schema. Its 14 blocks need a schema-supported projection with manual/table cross-check.
- VPX light/trigger coordinates are modelled centres, not all bulb sockets or sensor contacts. GI, flashers, trough, and complex assemblies require further measured placements before author readiness.

## Evidence

- Factory PDF SHA-256 `4cf31702805e75d37aef1c0c1624426000fec6cabf71a47e27691f5d5f8b6d01`, pp. 6–11, 98–119, 125, 168; corrected, hashed excerpt files are in `evidence/excerpts/stern/`.
- Pinned known-working script SHA-256 `d44738c5fa4693a8b096f226399f3ea2f81c985a1e780c33d012acf7d2bc390a`; retained 2018 VPX SHA-256 `baa4e6e2ec618ed667afc397dea2ee6cdc5c444f811395b42dd537cfec98c443`.
- Fresh wpt_140a Switch Test trace SHA-256 `610553661d3dd533f5a2216f67ca1aca9b63013257fe23b2b8453c6d2cd4caf1` and Single Coil Test sweep SHA-256 `f9b0b3b4899309d4ff2d30a704ee6c1663e283667e5fff6c8a732d5679b0ea82`; ROM archive SHA-256 `b4f98abae8cecb80a603285357c39688182b90ef376c46c80de5facb4e302463`.
