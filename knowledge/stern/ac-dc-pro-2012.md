# AC/DC Pro (original) recreation knowledge

## Identity and variants

This record is the original 2012 Pro playfield and owns non-h firmware revisions 1.21 through 1.65. Later 1.68 software is assigned to the separately documented 2014 LED Pro, and 1.70 to the Vault Edition. The split is intentional: the original has a conventional standup Hell's Bell target at switch 36, while the later products use a passive swinging bell.

## Ground truth and startup

The known-working AC/DC Pro 1.0 script is ground truth for PinMAME bindings and behavior; the Pro manual supplies wiring and construction. Initialize four trough balls on 18-21 and the empty cannon at home on switch 61. Output 1 ejects through stack opto 22, output 2 auto-launches from switch 23, and output 12 clears the Jukebox/top saucer at 37.

## Playfield and mechanisms

The Pro replaces Premium drop banks with standup AC/DC, ROCK, and TNT targets and omits the lower mini-playfield, bell saucer/magnet, band animation, detonator actuator, crossover diverter, and auxiliary 8-coil board. The motorized cannon still captures on 45, reports home 61 and mark 62, and fires through output 3. Output 4 selects the cannon route at the right ramp and output 5 controls the right gate. Three pops, two slings, two main flippers, top lanes, both ramps, both orbits, and spinner 33 complete the active playfield.

## Lamps and controller notes

Only the 1-80 lamp matrix and GI 0 are controller outputs. The service manual marks matrix positions 14, 15, 16, and 17 unused, but the proven Pro VPX script actively binds l14, l15, and l17 and the Vault script explicitly comments those same three bindings out as removed in the Vault Edition. Preserve 14, 15, and 17 as VPX-visible original/LED-Pro playfield inserts, preserve 16 as unused, and treat their artwork semantics as table-asset-defined rather than inventing manual names. The VPX script's 177-191 values are private flasher mirror indices fed by solenoid callbacks and are not lamps. Flashers remain solenoid outputs 17 and 20-31. Public dedicated flipper switches are 84/83 left and 82/81 right; lower-playfield dedicated slots are unused.

PinMAME public solenoid 33 is the synthetic SAM game-on/fast-flip state, not a Q33 ticket driver. Optional physical ticket-service identities 33-35 are preserved in the untransported `physical.output.ticket` group.

## Timing and service

The working script sweeps the cannon from roughly 110 degrees to 20 and back, asserts 62 at about 80 degrees, and will fire only before the cannon returns near home. Auto-launch uses an implementation impulse near 65 and the Jukebox eject uses the saucer route at switch 37. Keep these state boundaries; tune physical velocities to the target simulation.

## Evidence

- Official Pro manual SHA-256 987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5 is organized under E:/_vpe-2025/pinmame-manuals.
- Working Pro script SHA-256 e0fdef84892ea8bce6eae179509ac8262f103bac0173c2e822a4fe10aafcf7fa.
- Exact acd_170 topology run SHA-256 f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511; ROM archive SHA-256 e55c7386950272568dd639f3c8d70beff6fbd584ed49601d4196b46cb1e66ca5 remains external.
