# Williams FunHouse (1990)

Physical machine ID: `williams.funhouse.1990`. Manufacturer Williams, released 1990, design by
Pat Lawlor. FunHouse is a Williams WPC-Alpha machine: two sixteen-character sixteen-segment
alphanumeric displays (`GEN_WPCALPHA_2`, `wpc_dispAlpha`), not a dot-matrix display, and it
predates Fliptronics — its flipper coils are wired directly through a dedicated flipper driver
board rather than through the CPU-addressable solenoid matrix. This is the first WPC-Alpha
machine curated in this project.

## Identity and driver family

Pinned PinMAME's `fh_l9` clone tree has fifteen drivers: the production `fh_l9` (L-9, SL-3, 1992)
parent plus fourteen clones spanning firmware revisions L-2 through L-9/9.05H/9.06H/9.07H, LED
ghost-fix variants (D-3/D-4/D-5/D-9), an unofficial German translation MOD (L-9b/D-9b), a
community LED-fix-plus-ball-saver MOD (9.07H), a FreeWPC 0.91 community firmware (`fh_f91`), and
one genuinely distinct-generation prototype (`fh_pa1`, "L-2, Prototype PA-1 system 11 sound").

`fh_pa1` deserves a specific note: pinned `init_fh` dispatches between two different
`core_tGameData` structs by driver name — `fhGameData` (`GEN_WPCALPHA_2`) for every production
driver, and `fhpa1GameData` (`GEN_WPCALPHA_1`) only for `fh_pa1`. The two structs are otherwise
identical field-for-field (same `FLIP_SWNO(12,11)`, same mechanism handlers, same lamp-position
table, same inverted-switch mask), so `fh_pa1` is the same physical playfield running on an
earlier WPC-Alpha-1/System-11 sound-board generation rather than a different machine — the same
class of relationship this project already established for BY35 firmware clones, just expressed
through a second `core_tGameData` rather than a shared one.

The retained known-working table's own script binds `fh_905h` (`Const cGameName="fh_905h"`, line
64) — note the line above it, `'Const cGameName="fh_905"` (no trailing "h"), is commented out and
is not the active binding. `fh_905h` is a clone of the production `fh_l9` parent with an identical
I/O inventory, so this definition's production-driver evidence transfers directly.

## Controller platform

`controllers/pinmame/wpc-alpha.json` was reused unchanged. Its address rules (switches 1-8 and
11-88/111-118 matrix, solenoids 1-50, lamps 11-88, five G.I. strings 0-4) match `fhGameData`
exactly. FunHouse itself never uses the 111-118 Fliptronic column at all — both flipper switches
(11 Right Flipper, 12 Left Flipper) sit in the ordinary 8x8 matrix, confirmed directly by
`FLIP_SWNO(12,11)`'s explicit switch-number override.

## FunHouse has no CPU-controlled flipper solenoid

This is the single most important structural fact about this machine's I/O model, and it
generalizes to every future WPC-Alpha/WPC-DMD (pre-Fliptronics) machine this project curates.
`fhGameData`'s flipper field is `FLIP_SWNO(12,11)` alone — no `FLIP_SOL()` call. Pinned
`core_getSol`/`core_updateSw` only route a public solenoid address to a flipper-coil position
(`CORE_FIRSTLFLIPSOL`=45, `CORE_FIRSTUFLIPSOL`=33) when the driver's own `hw.flippers` bitmask
declares `FLIP_SOL(...)`; FunHouse's bitmask never does. The printed Flipper Circuits wiring page
(manual page 3-17) independently confirms the physical construction: Left/Right Flipper Power and
four Upper/Lower Flipper positions are wired through a dedicated flipper driver board (connectors
`J109`/`J110`) straight to the flipper buttons and end-of-stroke switches, with no printed solenoid
address anywhere on that page. `GENWPC_HASFLIPTRON` in pinned `wpc.c` excludes both
`GEN_WPCALPHA_1`/`GEN_WPCALPHA_2` *and* `GEN_WPCDMD` — i.e. every WPC generation before true
Fliptronics lacks CPU flipper-coil control entirely, not just the alphanumeric-display machines.
A curator working a WPC-DMD (monochrome DMD, still pre-Fliptronics) machine should check this
exact same fact rather than assuming a WPC-generation DMD game has Fliptronic addresses.

## Switch matrix: a clean two-opto sweep

FunHouse's manual identifies opto construction by a plain `"(opto)"` suffix directly in a switch's
printed description — never by matrix-cell shading (unlike Monster Bash's shaded "OPTO, TYPICALLY
CLOSED" cells). Sweeping every printed cell on both the switch-locations page (2-38) and the
switch-matrix wiring page (2-39) finds exactly two: switch 51 (Dummy Jaw) and switch 55 (Steps
Superdog). Pinned `fhGameData`'s inverted-switch mask is `{0x00,0x00,0x00,0x00,0x00,0x11,0x00,
0x00,0x00,0x00,0x00,0x00}` — column 5 = `0x11` = binary `00010001` = bits 1 and 5 set = row 1
(address 51) and row 5 (address 55). Zero disagreement: both printed optos are the exact two
PinMAME normalizes, and nothing else in the matrix is opto construction on either page.

## Two unresolved conflicts

**`conflict.gangway-lamp-12-value`.** The lamp-locations page (2-36) prints lamp 12 as "Gangway
10,000"; the lamp-matrix wiring page (2-37) prints the same address as "Gangway 100,000". Both
were confirmed at 600 dpi — this is a genuine cross-page disagreement, not a misread. Lamps 11,
13, 14, 15, 16 print an unambiguous ascending ladder (75,000 / 150,000 / 200,000 / 250,000 / Extra
Ball) on both pages, which only 100,000 continues monotonically. The promoted definition's label
uses "Gangway 100,000" on the strength of that pattern, but the underlying print disagreement is
recorded as unresolved rather than silently discarded — a plain "10,000" reading has not been
independently ruled out (e.g. by a lower-value early-ladder step that just isn't the value the
neighbors suggest).

**`conflict.gi-region-naming`.** The manual's G.I. locations page (2-40) labels string 02 "Front
Playfield" and string 05 "Top Playfield". The retained known-working script's own `UpdateGI`/
`UpdateGI2` region-header comment labels the same two addresses (0-based Case 1, Case 4) "Rudy"
and "Lower Playfield" — and its actual implemented behavior matches the script's own labels
exactly: Case 1 drives only the `RudySign1`/`RudySign2`/`RudyShade` collection (not a generic
playfield wash), and Case 4 drives the `GI_Lower` collection (the opposite end of the table from
"Top"). String 01 ("Upper Backglass"/Case 0) agrees between both sources, and string 03 ("Rear
Playfield"/Case 2 "Upper Playfield") is a plausible reconciliation under this project's
`y=0`-is-rear coordinate convention (the "upper" screen direction and the "rear" physical
direction describe the same end of the table), but strings 02 and 05 remain a direct, unreconciled
contradiction about which physical region each address illuminates. The promoted definition names
each G.I. device from the manual (physical-construction authority) while using the script's real
implemented light collections for spatial placement (runtime authority), and discloses the
disagreement on both affected devices.

## Rudy: three independent mechanisms sharing one figure

Rudy the animated dummy is genuinely three separate drive systems packed into one head assembly
(`A-13718 Head Assembly`), not one:

1. **Jaw** — solenoids 21 (Mouth Motor, `A-13997` DC gearmotor) and 22 (Up/Down Driver, direction
   relay) together, through a worm gear/sector pair (`A-13752 Jaw Drive Assembly`). Pinned
   `fh_handleMech`: jaw open + (21 energized, 22 not) → close; jaw closed + (21 and 22 both
   energized) → open. This is a motor-plus-direction-relay mechanism, the same structural pattern
   this project has already documented for Monster Bash's Dracula motor and Tales of the Arabian
   Nights' Ringmaster — check for it whenever a manual lists two solenoids with "Motor"/"Driver" or
   "Forward"/"Backward"/"Up"/"Down" naming on a mechanism.
2. **Eyelid latch** — solenoids 26 (open) / 27 (close), a persistent two-state latch independent
   of jaw position.
3. **Eye left/right** — solenoids 25 (right) / 28 (left), read as a momentary position signal each
   mechanics tick rather than a latch; neither held means eyes-straight.

None of the five eye/jaw-adjacent solenoids (21, 22, 25-28) has a dedicated VPX mechanism object
distinct from the head figure itself in the retained extraction, so all five are spatially
projected onto switch 51 (Dummy Jaw), the only fixed point recorded for the assembly.

## Trap door: switch state read from the door's own rotation, not a contact switch

The retained script's `TrapMover_Timer` sets `Controller.Switch(76) = 1` (Trap Door Closed) once
the door primitive's `RotX` falls to 90 degrees and clears it once the door opens past 90 —
exactly the "sensor state derived from a continuous mechanism position, not a discrete switch
object" pattern this project has repeatedly documented (Dracula's position optos, the Up/Down
Bank, the Frankenstein table). Solenoid 5 opens and solenoid 6 closes the door; both are projected
onto the same trap-door primitive as switch 76 for the same reason.

## Two addresses named "Kickbig" that are not typos of each other

The manual prints "Kickbig" as a real term twice: solenoid 3 ("Kickbig", Rudy's Hideout kicker)
and solenoid 4 ("Tunnel Kickbig", the tunnel kickout coil). These are two distinct, unrelated
circuits — not a duplicated label or an OCR artifact — and the manual is internally consistent
about it (the parts list, the switch table, and the schematic pages all use the same spelling).
Do not silently "correct" this to "Kickback" without independent evidence; it is transcribed
verbatim here.

## Flasher solenoid quantities are disclosed, not individually placed

The solenoid table prints explicit bulb counts for six flasher circuits: 17 (3 Blue Flashers), 18
(Dummy Flashers, read as 1), 19 (2 Clock Flashers), 20 (2 Superdog Flashers), 23 (3 Red Flashers),
24 (3 Clear Flashers). Each is treated as one physical dome/flasher fixture location (using the
retained table's primary dome/flasher render object) with the printed bulb count recorded in
`physical.quantity` and `physical.notes`, rather than attempting to place each individual bulb —
a flasher dome with multiple bulbs bundled together is a single fixture location in a way a
lamp-matrix insert with `(x N)` spread across the playfield is not (compare lamps 53/61/82 below,
which genuinely are spread across the playfield and get one placement per bulb).

## Lamp matrix is fully populated; three multi-bulb addresses confirmed by geometry

Unlike the switch and solenoid tables (which both list several unfitted positions), the 64-address
lamp matrix has no "Not Used" row at all — every position lights a real bulb. Three addresses
carry an explicit `(x 2)` marker on the lamp-matrix page: 53 (Superdog Lamp), 61 (Left & Inside Rt
Flipper Lanes), and 82 (Special Outlanes). The retained table's own object geometry independently
confirms this is a real quantity, not a rendering artifact: `l53`/`l53a` sit roughly 48 units
apart, and `l61`/`l61a` and `l82`/`l82a` sit on opposite sides of the table entirely (over 580
units apart for 61, matching its printed "Left & Inside Rt" description literally). By contrast,
addresses 51, 52, and 72 (all "Jet Bumper" lamps) carry a second or third same-named object in the
retained table (`l51a`/`l51b`, etc.) that sits within about 15-25 units of the primary object —
the same bumper's own cap-plus-skirt lighting layers rather than a second physical bulb — and the
manual prints no quantity marker for any of the three, so each gets exactly one placement.

## Three lamps with a real bulb but no resolved coordinate

Addresses 54 (Steps Lights Frenzy), 55 (Steps Lights Ex. Ball), and 56 (Steps 500,000) are each
modeled in the retained table by four separate "finger"-shaped Light objects (`Bot_finger_1-4`,
`Mid_finger_1-4`, `Top_finger_1-4`) forming a chase-lit arrow icon, not by one bulb at one fixed
coordinate. The manual states a single `#555`/`#44` bulb per address with no quantity marker.
Rather than guess which of the four finger segments is "the" bulb (or invent a centroid, which
this project's own Centaur lamp-113 lesson already established as the worst kind of fabrication),
spatial placement for these three addresses is left unresolved and named in `coverage.missing`.

## G.I. strings 2 and 4: real light collections, individual bulbs not yet extracted

G.I. address 2 ("Rear Playfield") drives the retained script's `GI_Upper` collection (19 Light
objects); address 4 ("Top Playfield") drives `GI_Lower` (45 objects). Both are genuine playfield
lighting circuits with real implemented geometry, but per-bulb spatial extraction for these two
collections was not completed in this curation pass — recorded as a named spatial gap rather than
either skipped silently or approximated. G.I. address 1 ("Front Playfield"/script "Rudy") drives
only three objects (`RudySign1`, `RudySign2`, `RudyShade`) and was fully placed. G.I. addresses 0
and 3 have no case handler in the retained script at all (no playfield lighting effect
implemented for either), matching their manual descriptions as backbox/insert-panel circuits.

## Outstanding work

- `switch.matrix-63` (Right Trough) has no dedicated VPX trigger/target object in the retained
  extraction.
- Lamps 54/55/56 and G.I. strings 2/4's individual bulbs (see above).
- The two unresolved conflicts above.
- The recreation knowledge is source-reconciled and complete; only the spatial gaps and two explicit conflicts above remain in `coverage.missing`.
