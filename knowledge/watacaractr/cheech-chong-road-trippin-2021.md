# Cheech & Chong: Road-Trip'pin (watacaractr, 2021)

Coverage: **author-ready - complete controller inventory, virtual mechanisms, displays, and recreation behavior validated**

## Identity and evidence precedence

This is a 2021 virtual-original table by watacaractr, not a manufactured Bally machine and not a physical Harley-Davidson conversion. PinMAME describes it as an unofficial Harley-Davidson MOD because `che_cho` imports the 1991 game's WPC alphanumeric machine driver, input ports, sound ROMs, and simulator base. The recreated playfield, theme, rules text, semantic I/O, art, and script-only mechanisms are specific to Road-Trip'pin.

The known-working `Cheech & Chong - Road-Trippin.vbs` script is ground truth for every controller binding and mechanism. Pinned PinMAME source defines the public WPC topology, display layout, base output constants, and ROM identity. The custom ROM's string table and repeatable live scenarios validate the rethemed semantics. Public release screenshots resolve the playfield labels. Harley service-test labels describe the inherited firmware address slots only and must never override the custom script, ROM text, or Road-Trip'pin playfield art.

## Controller topology

The public WPC switch and lamp addresses are matrix notation, not sequential indices: `11..18`, `21..28`, through `81..88`. Coin/service inputs are `1..8`; the generic flipper column is `111..118`. The table uses cabinet buttons 112 right and 114 left, while its pre-Fliptronics EOS contacts are matrix switches 11 right and 12 left. The harness had to retain ChangedLamps' matrix addresses; polling sequential lamp indices would silently mislabel WPC evidence.

Standard WPC outputs are enumerated through 50 even though the table binds only selected positions. Outputs 1-28 are the standard driver bank, 29-31 are state lines including game-on 31, and generic flipper callbacks include upper-right 34, upper-left 36, lower-right 46, and lower-left 48. Road-Trip'pin deliberately drives its upper-left and lower-left flippers together from 48, leaving 36 unused. Outputs 17-26 are custom flashers; 27 has no callback and 28's renderer line is commented out. Every unused controller position remains explicit in the JSON.

All five WPC GI callbacks, channels 0-4, are active. The proven script intentionally applies every channel to one shared `aGiLights` collection. Recreate that compatibility behavior unless a future table revision proves distinct GI regions.

## Ball lifecycle and ejects

Initialize three balls in the trough on switches 16, 17, and 18. The outhole is 15. Output 1 transfers a drained ball to the trough and output 2 sends the rightmost trough ball toward the manual shooter at angle 45 and force 7. Shooter switch 75 is held while the ball waits; there is no launch coil.

The left eject captures on 36 and output 11 kicks at 90 degrees, force 20, with angle and force variation 3. The right eject captures on 35 and output 10 kicks at 0 degrees, force 27, with the same variation. The bottom eject captures on 28; output 9 kicks at 243 degrees, force 24, Z offset 1.5, and variation 3. Switch 28 UnHit is also the return cue for the motorcycle cop animation.

## Targets, rollovers, lamps, and route

The top drop bank uses switches 51-53, reset output 3, and lamps 23-25 to spell A-N-D. The middle bank uses switches 54-56, reset output 4, and lamps 26-28 to spell T-H-E. Stand-ups 57, 58, and 61-66 light 31-38 in order to spell P-E-D-R-O and M-A-N. Live ROM scenarios prove these one-to-one progress-lamp sequences.

Rollover switches 31-34 light lamps 41-44 and complete B-O-N-G. Top rollovers 41-43 light 56-58 for Cheech, ampersand, and Chong. Switches 67/68 are right/left Road-Trip advance triggers; 71/72 are loop rollovers; 73/74 are outlanes. Matrix lamps 17, 18, 21, 22, 83, and 84 exist in the inherited matrix but are parked off-playfield by the working table and must not be represented as visible inserts.

The ROM string table fixes the ten route names and matrix order: 11 Pedro's House, 12 Drive-In Theater, 13 Upholstery Factory, 14 Hollywood Hotel, 15 Car Wash, 16 Police Station, 86 Our Lady of 13th Street (the display abbreviates this as `SCHOOL`), 87 Boardwalk, 88 Strawberry's House, and 85 Battle of the Bands (`B-O-B` in ROM text). A clean live game begins with 11 and 12 already lit and announces Factory onward as route progress accumulates; preserve the actual ROM state rather than inventing an alternative starting location.

## Coils, flashers, flippers, and gates

Pop switches 25, 26, and 27 map to outputs 5, 6, and 8. Left/right sling switches 37/38 map to outputs 15/16. The Road Closed target has no dedicated controller address: its hit event pulses both 37 and 38, then a local timer restores the target. Output 12 opens the right one-way gate and 13 the left. Output 7 is the knocker. Game-on 31 enables gameplay/flippers.

Flasher 21 illuminates Jade and Debbie; 22 drives the Chong jackpot and bird-cage group; 23 covers Checkpoint and Cheech/Chong plastics; 24 drives the Cheech and Chong spotlights. Outputs 17, 18, 19, 20, 25, and 26 retain the script object-group names where the public evidence supplies no more durable semantic label. These are still exact controller bindings; do not split one output's multiple VPX objects into fictional additional outputs.

## Script-only custom mechanisms

The motorcycle cop is a local timer animation, not a PinMAME motor. Its hit trigger advances from 0 to 725 by 5 units every 10 ms; after the bottom-eject ball leaves switch 28, it returns by 2.5 units per tick. The van uses hidden local kickers to transfer a ball through its animation and exposes no controller switch or coil. The clown decoration shakes on pop hits. Cheech/Chong heads, the bird cage, projectors, and character lights use target-hit counters, random sound branches, and local timers. Preserve these behaviors as authored but do not allocate controller addresses for them.

The Road Closed target is similarly local despite looking like a conventional drop target. It momentarily reports both sling switches and self-resets; there is no reset solenoid. Cul-de-sac contacts reuse bottom-bumper switch 27. These deliberate multiplexed semantics are necessary for ROM rules compatibility.

## Displays and sound

The exact display contract is two rows of sixteen `CORE_SEG16R` characters: row 0 begins at segment 0 and row 1 begins at segment 20. The harness decodes these rows for service menus and rule correlation. The game ROM reuses Harley-Davidson U15/U18 sound ROMs but the intended table experience also requires the separately distributed `che_cho` altsound package. Altsound files are media, not playfield devices, and are not stored in this repository.

## Recreation checklist

- Create every JSON switch, output, matrix lamp, GI string, DIP/configuration bit, and both 16-character displays; retain explicit unused positions.
- Initialize the three-ball trough exactly and implement all three eject vectors, the manual shooter, both drop-bank reset relationships, gates, pops, slings, and the combined left-flipper callback.
- Build the ten route inserts at their exact matrix addresses and preserve the ROM's initially lit route state.
- Implement Road Closed, motorcycle cop, van transfer, clown shake, character heads, bird cage, and projector effects as script-local mechanisms with no invented PinMAME I/O.
- Treat the public VPX script as ground truth whenever inherited Harley diagnostics disagree with the custom table.

## Sources

- `vpx.che-cho.watacaractr.1.0`: pinned known-working table script, SHA-256 `1893c13b913b987984144fd1d072e6b3c4f4c0df324298722449176f95164b29`.
- `screenshot.che-cho.playfield`: public full-playfield screenshot SHA-256 `339a2bc5a4bc8b87453d23cf2031a510cffedc4a0ba927ac4920b0bbe0b4424b` and companion perspective screenshot SHA-256 `5c024f765af406f32aeb4cf18b8543cb87258a500bab8619d8d02f9e3c936cf1`.
- `rom.che-cho.static`: exact external `che_cho.zip` SHA-256 `34d1f6a3fc31b988fe4c0a38904df2d533e3cb0735995134d113dcb7f96157c2`; extracted main ROM SHA-256 `1a8e89cdd6a280e803028a9b70a5e89471455fa9712813421449ffae8bb5d0af`. ROM bytes remain outside the repository.
- `runtime.che-cho.harness`: isolated game-start, target/lamp, B-O-N-G/top-rollover, route, display, GI, and service scenarios. Exact raw-run hashes are recorded in the source locator and compact runtime evidence.
- `pinmame.wpc.che-cho.4ec52ff0ac13`: pinned driver declaration, WPC address conversion, inherited Harley simulator contract, output topology, and two-row display layout.
