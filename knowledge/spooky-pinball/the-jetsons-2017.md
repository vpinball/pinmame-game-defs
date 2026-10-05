# The Jetsons (Spooky Pinball, 2017)

This definition covers the physical machine (IPDB 6577, 6608, model 00004) and its one
PinMAME driver, `jetsons_004`, the V4 code update on the Spooky Pinball pinHeck board (PIC32MX795 game CPU, Parallax Propeller
display/sound/media CPU). It is partial: every controller address is enumerated and checked against the ROM's own service
tests and named, but the placements are measured on photographs, not a factory drawing, the mechanisms are inventoried
without their full behaviour, and some outputs keep an unknown fitment.

## Machine

The Jetsons was built by Spooky Pinball for The Pinball Company: 75 Regular and 25 Special Editions, the Special Edition adding purple armour and the Orbitty backbox topper on servo 0. Its 128x64 colour display is the only one of its size on pinHeck. The trough mixes optos (92 trough, 93 jam) with matrix contacts, and the cabinet carries a Launch button (input 2). The GI_1 header names the ramp and scoop flashers (37, 38) and the left and right GI (39, 40).

Editions: IPDB 6577 Regular Edition (75 units (confirmed), charcoal grey armour); IPDB 6608 Special Edition (25 units (confirmed), purple armour and a backbox topper).

## Running it

The romset is Spooky's Jetsons_Code.zip code update: Jetsons/JET_V004.PRG, Jetsons/PRP_V002.BIN and the SD card's folders, loaded as `jetsons_004.zip`. PinMAME before 97aa922b
named it `jetsons.zip`, and the retained harness scenarios still name that set. pinHeck also needs `pinheck.zip` holding the Propeller's 32 KB mask ROM (`p8x32a.rom`, CRC32 f99b3070).
On an empty NVRAM the ROM first programs its program flash and AV EEPROM from the romset (about eight emulated minutes), shows CODE UPDATE COMPLETE / PLEASE RESTART, and after the next start once more asks for a restart; from the third start it boots to attract mode. The harness runs started from a retained copy of that post-update NVRAM.

## Controller contract

The platform contract is `controllers/pinmame/pinheck.json`. In short: factory switch and lamp `n` (0-63) are public
`(n / 8 + 1) * 10 + n % 8 + 1` (11-88); cabinet inputs are 1-8 and 91-97; the host drives the flipper buttons at 112 (right) and 114
(left), which PinMAME copies to cabinet inputs 3 and 4; factory coil `n` is public `n + 1` (1-24); GI outputs 0-7 are 25-32 and 8-15
are 37-44; 51-56 are the on-board RGB LEDs, 57-61 the servos (0-255 position), 62-64 the external or third RGB LED; the Start lamp
is 91. On every switch public 1 is the closed contact; no switch is inverted. 45 inputs, 24 solenoid-group
outputs and 36 lamps are used.

## What the ROM itself proves

Every pinHeck game has the same operator menu (Enter, 6, opens it; the right flipper button steps; Back, 5, leaves). Its Switch
Edge test draws each closure in an 8x8 grid laid out like the factory chart, so closing every public address proved the
switch formula for all 64 matrix positions and the cabinet mapping for 2-8 and 91-97. The Solenoid test names each of the 24
coils, and pressing Enter fired exactly coil `n + 1` every time. The Lamp test names the sixteen GI outputs (the playfield group
44 down to 37, the backbox group 32 down to 25) and then every matrix lamp by its factory number, lighting only that address. The
Servo and RGB tests name the servos and LED channels the game uses. A game-start run (trough full, Start pressed) shows the ROM
pulsing its trough feed coil repeatedly while no ball reaches the shooter lane.

## Mechanisms

### Three-ball trough with optos

Balls rest in the trough on the trough opto 92 (Opto6) and the Ball Trough 1-3 contacts 52-54, with the jam opto 93 (Opto5) watching the exit. LOAD COIL (5) feeds one to the shooter lane; in the game-start run the ROM pulsed it about every 1.8 s for 20 s, because no ball ever reached the shooter switch.

### Shooter lane and launcher

PLUNGER (6, the Ball Launch coil) fires the ball on the shooter lane switch 51; the cabinet Launch button is input 2.

### Right flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 3 (host public 112), the ROM fires the RFLIP HIGH (4) winding to lift the bat and holds it on the RFLIP LOW (3) winding, and the matrix end-of-stroke contact 55 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 4 (host public 114), the ROM fires the LFLIP HIGH (7) winding to lift the bat and holds it on the LFLIP LOW (8) winding, and the matrix end-of-stroke contact 26 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left slingshot

Switch 23, coil 10.

### Right slingshot

Switch 44, coil 11.

### Lower pop bumper

Skirt switch 34, coil 18 (BOTTOM POP).

### Left pop bumper

Skirt switch 35, coil 19.

### Right pop bumper

Skirt switch 36, coil 21.

### Scoop

The Scoop coil (9) ejects a ball held on 21; the scoop opto 96 (Opto - 3) sees it enter.

### Kickout hole

SAUCER (20, the Saucer Kick Out coil) ejects a ball held on 17 (Kickout Hole).

### Orbit up-post

BALL STOP (17, the chart's Up Post) between the orbits (11 right, 56 left) and the Elroy loop (16).

### Orbitty topper (Special Edition)

Servo 0 (57) drives the backbox topper, which IPDB lists only on the Special Edition, so the output is optional; the ROM's firmware has no Servo test, so its travel is not observed.

## Evidence and remaining work

Factory chart transcriptions, the ROM service-test tables and the IPDB identity are under `evidence/excerpts/spooky-pinball.the-jetsons.2017/`; the runtime
summary is `tools/pinheck_runtime.json` (rebuilt by `tools/pinheck_runtime.py` from the retained runs), the scenarios are
`tools/harness-scenarios/pinheck/jetsons-*.json`. Remaining: the placements are measured on photographs rectified at playfield level (`photo-placements.md` names the photographs, the frame and its uncertainty, and every device left out). They stay observed: no factory location drawing or recreation table checks them, a position can be off by a few percent, and raised parts, parts hidden under the apron or ramps, GI and the RGB strings are not placed;
the mechanism inventory names each mechanism's coils, switches and service-test positions, but no retained source gives its home and startup state, its timing, how the ROM resets it or how it fails, so mechanism behaviour stays open until a manual, a known-working table or a gameplay harness run supplies it. The outputs whose fitment stays unknown: 25 (Backbox GI Output 0), 26 (Backbox GI Output 1), 27 (Backbox GI Output 2), 28 (Backbox GI Output 3), 29 (Backbox GI Output 4), 30 (Backbox GI Output 5), 31 (Backbox GI Output 6), 32 (Backbox GI Output 7), 41 (Playfield GI Output 12), 42 (Playfield GI Output 13), 43 (Playfield GI Output 14), 44 (Playfield GI Output 15), 58 (Servo 1 (chart: Open)), 62 (External RGB LED 0 red), 63 (External RGB LED 0 green), 64 (External RGB LED 0 blue).
