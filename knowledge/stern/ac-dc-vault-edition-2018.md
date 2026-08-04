# AC/DC Vault Edition recreation knowledge

## Identity

This record covers the 2018 1.70 and 1.70 colored PinMAME drivers on the AC/DC Vault Edition physical product. It retains the Pro ball paths and passive swinging-bell product line but changes artwork and removes lamp inserts 14, 15, and 17.

## Ground truth and differences

The known-working AC/DC Pro Vault 1.0 script is ground truth. Switch 36 is a physical swinging-bell hit contact, not the original Pro's standup target. The bell has no controller actuator. Lamps 14, 15, and 17 are absent and explicitly unused; every other Pro switch, lamp, flasher, coil, trough, shooter, cannon, gate, ramp, orbit, pop, sling, flipper, and spinner binding is retained.

## Cannon and ball devices

Start four balls on trough switches 18-21 and the cannon at home on 61. Output 1 ejects, output 2 launches, output 12 clears Jukebox switch 37, output 4 routes into the cannon, output 32 rotates, and output 3 fires the ball held on 45. Switch 62 is the cannon timing mark. The right control gate is output 5.

## Spatial reconstruction

Every physical playfield switch, effect, insert, flasher, and GI emitter has a reviewed normalized placement in VPX/player view (`x=0` left, `x=1` right, `y=0` rear, `y=1` apron). Coordinates come from the exact working `AC-DC Pro Vault-1.0.vpx` table and were checked against the official switch, lamp, and coil location sheets. Switches 18-22 follow the real under-apron trough assembly from drain end to eject/jam end rather than collapsing onto the table's two simulated kicker objects. Cannon switches 61 and 62 share the rotating assembly's projected center because their physical contacts differ by cam state, not playfield position. Rear-panel lamp addresses 53-56 and 65-72 and rear-panel flasher solenoid 22 retain physical quantities and construction notes but intentionally have no normalized playfield coordinates.

Solenoid 25 has three emitter placements, one at each pop bumper. GI 0 has 38 normalized playfield emitter placements; its physical quantity is 45 because the back-panel parts diagram corroborates another seven bulbs that are intentionally left without playfield coordinates. Cosmetic reflection and desktop-render helper objects are not duplicate physical emitters. Cabinet/start/tournament/FIRE lamps, cabinet/service switches, the shaker, knocker, and optional ticket hardware are explicitly marked `cabinet_or_service` instead of being forced into playfield coordinates.

## Evidence

- Vault script SHA-256 88101e2184729f952d196fdfe5885f9d7e81ec211b7b1b675d724419fcb6a7f1.
- Exact working VPX SHA-256 10a460c6b84fc1b8b372bf7b3d92b1904ee5eed9d5aad29fe384e7a6502fa328; 79,429,632 bytes; verified and extracted with vpxtool git:v0.33.3. The source table is retained in the organized external VPX cache and is not redistributed by this repository.
- Official Pro manual SHA-256 987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5 supplies the unchanged base wiring.
- Exact acd_170 run SHA-256 f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511; exact ROM archive remains external.
