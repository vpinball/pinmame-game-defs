# Data East Laser War (1987)

## Identity and controller

Laser War is Data East's first pinball machine. Pinned PinMAME defines its three-driver clone tree with `lwar_a83` as root and assigns `GEN_DE` (`0x1000`), `de_dispAlpha1`, `FLIP4746`, `SNDBRD_DE1S`, no custom solenoids, and Left/Right mux solenoid 10. `GEN_DE` is included in `GEN_ALLS11` and the driver uses the shared `MACHINE_INIT(s11)` path, so the already-upstream `pinmame.system-11` profile is reused unchanged. The profile deliberately expresses platform outer ranges: this machine narrows its actual service controls to Data East `DE_COMPORTS` addresses -7 Advance and -6 Up/Down, its actual solenoid enumeration to 1-50 because `custSol=0`, and its machine-specific display topology in `displays`; the adjacent Williams-only -5/-4 diagnostics and the profile's 51-64 custom-solenoid capacity are not claimed as fitted Laser War addresses.

The display board is Laser War's 520-5004-00 topology: two seven-character 16-segment alphanumeric player rows, two seven-character numeric player rows, and a shared four-digit numeric credit/ball module. PinMAME exposes that last physical module as four one-digit layout entries, so the definition enumerates all eight controller layout entries. Displays are backbox devices and therefore use controlled `not_applicable` spatial records.

## Address model

All 64 switch and 64 lamp matrix addresses are present in the definition, including every printed NOT USED switch position. The switch and lamp matrices are column-major: address `1 + row + 8*column`. Solenoids are enumerated through public address 50 because `custSol=0`. Public 1-8 are the left side of eight shared transistor drives and public 25-32 are their relay-selected right side. Address 10 is the Left/Right power relay, address 23 is Game On, 33-44 are inert for this GameData, 45-48 are synthesized lower-flipper power/hold bits, 49 is the simulator shooter slot, and 50 is reserved.

## Ball handling and causality

The retained known-working script, not printed label proximity, supplies runtime causality. It initializes trough switches 10-12 active, moves the front ball from switch 12 through coil 9 to the shooter lane, sends the outhole at switch 13 through coil 16 into the trough, and binds the red/yellow/blue eject saucers to switch/coil pairs 25/12, 33/13 and 38/14. The Laser Kick relay at output 15 arms the kickback; switch 17 triggers the local kick only while armed. Slings and pop bumpers have real sensors and physical mechanisms, but their special-coil address mapping is deliberately absent because the scan loses the decisive schematic half.

## Spatial reconstruction

The retained table's asserted playfield bounds are left 0, top 0, right 964, bottom 2162. Coordinates use `x=raw_x/964`, `y=raw_y/2162`. Primary `lN` Light objects are bulb observations; `lNa` and related suffix objects are render helpers and are excluded. Lamp 41 has two primary bulbs and therefore two placements. The cannon tower groups are helper-only aggregates, so lamps 9-11 are not assigned their many visual helper coordinates. Insert-flasher helper-group centroids are marked candidate. Cabinet relays, backbox flashers, service controls, displays, and internal nonvisual sensors receive controlled `not_applicable` dispositions.

## Evidence limits and conflicts

The manual is a 42-page ClearScan/OCR scan. Every decisive matrix/coil cell on PDF pages 19-24 (printed pages 17-22) was re-read cell-by-cell from fresh 400 dpi Poppler renders; the OCR text was not treated as a transcription. Pages 25-34 are missing their right halves. That damage blocks the address-to-device mapping for switched-coil circuits 17-22 and a complete flipper/EOS polarity circuit.

Six disagreements are recorded as first-class conflicts. Four remain unresolved: switch 17 is `Laser Kick` in the matrix but `Kick Back` in the location illustration/runtime; switches 46/47 are printed as physical right/left E.O.S. switches while PinMAME and the script use those addresses for flipper-button state; and printed lamp 8 is `Return to Base` while the retained script has no lamp-8 callback and reuses its l8 tower helpers for solenoid 5. Two have documented resolutions without rewriting the printed evidence: the Coil I.D. Chart's duplicated `2L` Ramp Multiplier row is `1R`/public 25 by Q46 wire pairing, the following printed location list and `SolCallback(25)`; and Mars Yellow remains semantically a flasher even though both manual lists print `COIL: 23-800`, because its red/blue partners are `#89 BULBS` and pinned `s11.c` calls all three Mars colours flashers. The chart's `WARRIIRS` spelling is retained in the excerpt and normalized only in the semantic label because the following printed list spells `WARRIORS`. Lamp 49 (`Ion Cannon (Tip)`) is printed but has no retained runtime binding; that is an unresolved placement/runtime omission, not silently converted into a different device.

## What would complete the record

A complete Laser War schematic scan (especially special-solenoid and flipper pages), a traced original harness or bench capture for circuits 17-22 and flipper/EOS polarity, and a socket-level survey of the cannon tower and lamps 8/49 would remove the named blockers. Until then this definition remains partial.
