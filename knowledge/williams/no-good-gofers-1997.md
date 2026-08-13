# No Good Gofers (Williams, 1997)

## Evidence and scope

This record describes the one physical Williams No Good Gofers playfield shared by `ngg_13`, `ngg_12`, `ngg_10`, and `ngg_p06`. The retained known-working VPX script binds `cGameName = "ngg_13"`; it is the runtime and recreation ground truth when it disagrees with lower-priority emulator scaffolding. The Williams operations manual is the physical-construction, wiring, part-number, quantity, and polarity authority. Pinned PinMAME source supplies WPC-95 public address topology. The retained VPX table supplies geometry only.

The manual SHA-256 is `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`. The retained table and embedded script are respectively `9f5b44285e3a10155fb0bf33a84626df45cc305f193d15963e39228355b91e59` and `fbb6914941bd542f38e1ae9c15a6147b552cd33a22f586c85c3139da08aee766`. The full `vpxtool` extraction is pinned by a 927-file, 127,738,302-byte canonical manifest (`caf93fabeb7b697f65f3314425286a1f8fa96a37811b51f1abc357eb176ead66`).

## WPC-95 controller contract

No Good Gofers is `GEN_WPC95`, with the standard 8x8 switch and lamp matrices, five GI strings, Fliptronic, the WPC-95 LPDC mirror behavior, and eight custom outputs. Its four ROM entries all describe the same physical machine. The manual's printed lower-right flipper circuits 29/30 appear at public outputs 45/46 and lower-left 31/32 at 47/48. Upper-right 33/34 already equal their public addresses. Printed upper-left power 35 is deliberately repurposed for the Ball Launch (slam) Ramp; printed hold 36 is unfitted. There is no physical upper-left flipper: F7/F8 are explicitly `NOT USED`.

All 64 matrix cells are enumerated, including the four manual `NOT USED` positions (11, 43, 87, 88). Switch 24 is a real printed `ALWAYS CLOSED` controller input, so a recreation must establish it active rather than treat it as an ordinary hit switch. The fifteen matrix optos are exactly 31-38, 41/42, 44-46, and 63/64. That exactly matches `nggGameData`'s inversion mask: column 3 `0xff` for 31-38, column 4 `0x3b` for 41/42/44-46, and column 6 `0x0c` for 63/64. Fliptronic's public input state is already normalized by the WPC-95 core; button optos F2/F4/F6 must not be re-inverted.

## Ball handling and headline mechanisms

- The **six-ball trough** has eject opto 31 plus ball positions 32-37. The retained `bsTrough` helper uses positions 32-37 and solenoid 9 (`Trough Eject`) pulses 31 before firing the `BallRelease` kicker. These are real individual physical optos even though the VPX representation only has one kicker anchor.
- **Auto Fire** (1) serves the shooter groove (18); the **Kickback** (2) returns from the left outlane. The **Clubhouse Kicker/Putt Out** (3) and **Underground Pass** (24) share the Putt Out route (44), with hole-in-one (68) and Behind Left Gofer (67) feeding that progression.
- **Bud** at left and **Buzz** at right are coupled gofer/ramp assemblies. Their high-power Up coils are 4/5, their low-power Down coils 15/16, and ramp-down coils 27/28 only act after their gofer is down. Respect the state ordering: the retained script and PinMAME both clear the down sensors before lifting and set them when lowering.
- The **Jet Popper** (6, switch 38), **Sand Trap/Left Eject** (7, switch 78), and **Upper Right Eject** (8, switches 45/46) are captured-ball kickers. The script has a separate right-popper jam transition rather than treating it as an additional generic target.
- The **Ball Launch Ramp** is a transient slam-ramp diverter driven through the repurposed upper-left Fliptronic power circuit 35. The script drops its collision surfaces and returns them after a timer; do not model it as a fourth flipper.
- The **wheel** is a reversible 14-7955-1 motor controlled through A-16120: 37 is counter-clockwise and 38 clockwise. A-22026 is one two-channel Motor 2-Opto Board for inner/outer wheel switches 63/64. The golf cart and its path switches 71/72/74 are separate physical/recreation behavior, not aliases for motor state.
- The two lower flippers and one upper-right flipper use the printed power/hold pairs. The physical cabinet opto boards share lower/upper channels by side, but only F6's right-hand upper channel is fitted; F8 is only a generic template channel and is not a machine device.

The ordinary but author-relevant scoring hardware remains explicit: left/right slings (10/11, 51/52), three jet bumpers (12-14, 53-55), three skill targets (56-58), two spinners (61/62), two cart paths (71/72), K-I-C-K Advance plus the four K-I-C-K letters (81-85), Advance Trap (77), and captive ball (86).

## Lamps, flashers, and GI

The printed lamp matrix has all 64 fitted addresses. Lamp quantities are physical, not effect counts: 13, 28, and 68 each have two lamps; 55 and 71 each have a #44 and a #555 assembly; the other positions have one. Lamp 88 is the illuminated cabinet start button and therefore deliberately has no playfield coordinate. The retained script's `UpdateLamps` maps each matrix address to its named lamp object; overlay lights are presentation effects and are not additional physical bulbs.

Main flashers are 17-21 and 25/26. Notice that printed controller-bank labels do not define device kind: 24 (`Underground Pass`) is in the manual's “Flasher” driver bank but is a coil, while 25/26 are in “Gen. Purpose” and are physical flashers. Drivers 22/23 are truly unfitted, not missing evidence.

GI is five physical circuits. Manual wiring settles their destinations:

- GI 0: left-side playfield string (`WHT-BRN`);
- GI 1: right-side playfield string (`WHT-ORG`);
- GI 2: Gofer Spotlight, split between playfield and insert panel (`WHT-YEL`);
- GI 3: insert-panel-only Illumination String 4 (`WHT-GRN`), always on;
- GI 4: insert panel plus coin-door Illumination String 5 (`WHT-VIO`), always on.

The manual's solenoid table transposes J105/J106 *designators* for the first three strings. Its wire colors and the complete interboard wiring list settle the physical destinations; do not copy the transposed connector names. The VPX script runs `UseGI = 0`, and its GI collections are visual proxies, so they are intentionally not used to assert a physical bulb count or invented GI coordinates.

## Auxiliary eight-driver public mapping

The physical A-21773 auxiliary board's J4 drives manual solenoids 42-49: upper-right flashers 1/2/3, the two two-bulb upper-playfield flashers, then upper-left 3/2/1. The retained known-working script binds them sequentially to public callbacks 51-58 (and explicitly uses 54/55 for the upper-playfield pair). `nggGameData` declares eight custom outputs, also giving 51-58.

Pinned `wpc.c` separately assigns No Good Gofers *PWM flasher types* at `42 + 14` through `49 + 14`, or public 56-63. That block only calls `core_set_pwm_output_type`; it neither maps nor drives public state, and it extends beyond this driver's declared 58-output span. The actual public mapping is independently fixed at 51-58 by `hw.custSol = 8`, `CORE_CUSTSOLNO(1) = 51`, and `ngg_getSol` indexing `WPC_EXTBOARD2` from that boundary. The definition therefore preserves manual 42-49 as aliases and uses public 51-58. The 56-63 type table is retained as a pinned PinMAME metadata defect, not promoted to a false second address map or unresolved machine conflict.

## Spatial handling and promotion state

The only coordinate system is the retained VPX table: bounds `(0,0)-(964,2162)`, normalized as x=0 left/x=1 right and y=0 rear/y=1 apron. Direct named script objects provide coordinates for all matrix lamps except the cabinet start lamp, the directly handled switches, flippers, named kickers, named gofers, and directly bound flashers. A manual callout, a broad mechanism object, a hidden trough helper, or a VPX visual overlay is not enough to manufacture a point for an individual physical component.

The definition is consequently intentionally `partial` with `missing = [spatial_placement]`. Remaining spatial gaps include individual trough positions, ramp-down sensors, unrepresented gofer hits, both wheel optos, several coils, motor directions, and GI bulb positions. Lamps 13, 28, and 68 and flashers 20 and 25 each have two printed physical bulbs but only one directly bound retained-table emitter; those five placement sets are explicitly observed and incomplete. This is fail-closed: it is a strong physical/electrical definition, but is not author-ready.

## Sources

- `manual.williams.no-good-gofers.1997`: visual manual transcriptions under `evidence/excerpts/williams.no-good-gofers.1997/`.
- `vpx-table.ngg-bodydump` / `vpx-script.ngg-bodydump`: retained known-working table, runtime binding and directly named geometry.
- `pinmame.core.4ec52ff0ac13` and `controller-profile.pinmame-wpc-95`: WPC-95 topology, inversion, Fliptronic, LPDC, custom-output and display behavior.
