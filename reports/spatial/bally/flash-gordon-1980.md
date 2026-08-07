# Flash Gordon (Bally, 1980) spatial review

Status: incomplete. Three addresses carry no placement and two carry a deliberately reversed one, so the machine record stays `partial` at `machines/partial/bally/flash-gordon-1980.json`.

The matching source is the retained known-working `Flash Gordon (Bally 1981) 2.0.vpx` at SHA-256 `b2c5ea9eac7e4b7b6cf8f81809482b3d31ee9f1cb23a8242df0e7c2bf2790b0e`. Its embedded script at SHA-256 `e440f644ee509f392aa2340f652918144728bd8fe6f306eec7b5ed6441d10c2c` is the runtime address and causality authority. Exact playfield bounds are `left=0 top=0 right=952.9412 bottom=1976.471`, and every canonical coordinate is x/952.9412 and y/1976.471 rounded to at most six fractional places. That y divisor is far shorter than the 2162 of the WPC machines curated elsewhere in this project, which is what an early-1980s playfield looks like; the lower flippers land at y = 0.833 and the outhole at y = 0.952.

## Evidence decisions

- The embedded script owns runtime addresses and causality, the Bally game #1215 manual owns physical construction, wiring, quantity and device presence, pinned PinMAME owns controller topology, and the retained table supplies geometry.
- The public solenoid mapping is the retained script's own printed cross-reference, not the manual's Self Test # column, which is a test order. The manual says so itself. The two continuous outputs are corroborated independently by `src/lisy/lisy35.c`, which names continuous bit 1 the coin lockout and bit 2 the flipper-enable relay - public 18 and 19.
- Lamp bindings come from the script's own `Lampz.MassAssign` calls, not from object-name patterns, and every one of them was checked against the function this game's A5 or A9 connector sheet prints against the pin the address reaches.
- General illumination is not a device on this machine. The Playfield A6 sheet draws it as a 5.9 VAC transformer circuit with no driver-board connection, and the BY35 controller profile declares no general-illumination group, so the retained table's `GI_*` Light objects are excluded rather than bound to an invented address.
- Three flipper coils are fitted (parts list `Flipper (3)`), driven through the K1 relay at public 19 rather than by driver-board outputs, so they have no address and no placement. The retained table models the same three: two lower flippers and an upper right flipper that its own key handler drives from the right flipper button.

## Explicit projections

- Solenoid 1: Projected onto the left four-bank drop target assembly it resets (the mean of the retained table's own four target objects sw17-sw20). The reset coil is mounted under the bank and has no object of its own in the extraction.
- Solenoid 2: Projected onto the upper-left three-bank drop target assembly it resets (the mean of the retained table's own target objects sw21-sw23).
- Solenoid 3: Projected onto the right in-line drop target assembly it resets (the mean of the retained table's own target objects sw25-sw27).

## Counts

- Placements: 115
- Located input addresses: 31
- Located output bindings: 77
- Inputs with a controlled `cabinet_or_service` record: 6
- Inputs with a controlled `dip_switch` record: 32
- Inputs with a controlled `unused` record: 1
- Outputs with a controlled `cabinet_or_service` record: 16
- Outputs with a controlled `unused` record: 13
- Inputs with no spatial key at all: 2 (5, 29)
- Outputs with no spatial key at all: 1 (100)

## Blockers

- Public switches 5 (Drop Target 50 Point Rebound) and 29 (10 Point Rebound) are real, fitted two-contact rebound addresses that the retained table implements as collidable Primitives named phys_sw5 and phys_sw29, both of which sit at a zero position with a zero rot_and_tra and no axis-aligned bounds recorded in the extraction. There is no usable coordinate for either, so the spatial key is omitted rather than a position invented.
- Public lamp 100 has no spatial key because the manual marks its circuit N/U in two places while the retained table binds it to the two left-hand rollover buttons of switch 1; see conflict.aux-lamp-100-left-rollover-fitment.
- Switches 12 and 15 are placed on the two right-rail standup targets according to the printed self-test table and Figure V, which means their placements are deliberately the reverse of the retained table's own object names; see conflict.right-side-target-upper-lower-transposition.

## Promotion decision

Promotion to `author_ready` is refused. Two addresses that are certainly fitted - public switches 5 and 29, the two rebound-rubber pairs - have no coordinate anywhere in the retained extraction, and two first-class conflicts remain open: which of the two right-rail standup targets is switch 12 and which is switch 15, and whether auxiliary lamp circuit 100 is fitted at all. The record stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/flash-gordon-1980/extracted-vpxtool.manifest.json`, SHA-256 `50810dd697738d98061624512a948cec08ca6eaad037d5dd61d3a7d9935fc775`, 1447 files, 168438120 bytes.
- Object-centre dump of every extracted game item, raw and normalized, at `external:pinmame-review-artifacts/flash-gordon-1980/vpx-geometry.txt`.
- Manual `Flash Gordon Bally 1981 English Manual.pdf`, SHA-256 `179536aa00448188602ce0ac7e7d5c729b8649f8638358b4b4c9a065c2adb63a`, with eight transcribed excerpts under `evidence/excerpts/bally.flash-gordon.1980/`.
