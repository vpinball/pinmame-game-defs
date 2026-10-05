# Domino's Spectacular Pinball Adventure (Spooky Pinball, 2016)

This definition covers the physical machine (IPDB 6418, 6586, model 00003) and its one
PinMAME driver, `dominos_006`, the V6 code update on the Spooky Pinball pinHeck board (PIC32MX795 game CPU, Parallax Propeller
display/sound/media CPU). It is partial: every controller address is enumerated and checked against the ROM's own service
tests, and all but the two cabinet optos are named, but the placements are measured on photographs, not a factory drawing, the mechanisms are inventoried
without their full behaviour, and some outputs keep an unknown fitment.

## Machine

Domino's was built under licence for Domino's Pizza; IPDB records about 60 Standard and 75 Limited Editions that differ only in the backglass art and the LE plaque. Its knocker and shaker are options. The GI_1 header names four outputs: pin 12 Right Flasher (41), 13 Left Flasher (42), 14 GI (43) and pin 15 Oven Flasher (44). Which of the two cabinet optos (95, 96) is the scoop opto and which the Noid loop opto is not printed anywhere: the switch chart calls both 'Opto', the ROM's Switch Edge test does not name them, and an exploratory game probe drew no ROM response from either.

Editions: IPDB 6418 Standard Edition (about 60 units, production from October 17, 2016); IPDB 6586 Limited Edition (75 units, November 2016; IPDB: exactly the same as the Standard Edition except the backglass art and the LE metal plaque).

## Running it

The romset is Spooky's DOM_v6.zip code update: DOM_V006.PRG, PRP_V008.BIN and the SD card's DMD/ and SFX/ folders, loaded as `dominos_006.zip`. PinMAME before 97aa922b
named it `dominos.zip`, and the retained harness scenarios still name that set. pinHeck also needs `pinheck.zip` holding the Propeller's 32 KB mask ROM (`p8x32a.rom`, CRC32 f99b3070).
On an empty NVRAM the ROM first programs its program flash and AV EEPROM from the romset (about eight emulated minutes), shows CODE UPDATE COMPLETE / PLEASE RESTART, and after the next start once more asks for a restart; from the third start it boots to attract mode. The harness runs started from a retained copy of that post-update NVRAM.

## Controller contract

The platform contract is `controllers/pinmame/pinheck.json`. In short: factory switch and lamp `n` (0-63) are public
`(n / 8 + 1) * 10 + n % 8 + 1` (11-88); cabinet inputs are 1-8 and 91-97; the host drives the flipper buttons at 112 (right) and 114
(left), which PinMAME copies to cabinet inputs 3 and 4; factory coil `n` is public `n + 1` (1-24); GI outputs 0-7 are 25-32 and 8-15
are 37-44; 51-56 are the on-board RGB LEDs, 57-61 the servos (0-255 position), 62-64 the external or third RGB LED; the Start lamp
is 91. On every switch public 1 is the closed contact; no switch is inverted. 45 inputs, 27 solenoid-group
outputs and 48 lamps are used.

## What the ROM itself proves

Every pinHeck game has the same operator menu (Enter, 6, opens it; the right flipper button steps; Back, 5, leaves). Its Switch
Edge test draws each closure in an 8x8 grid laid out like the factory chart, so closing every public address proved the
switch formula for all 64 matrix positions and the cabinet mapping for 2-8 and 91-97. The Solenoid test names each of the 24
coils, and pressing Enter fired exactly coil `n + 1` every time. The Lamp test names the sixteen GI outputs (the playfield group
44 down to 37, the backbox group 32 down to 25) and then every matrix lamp by its factory number, lighting only that address. The
Servo and RGB tests name the servos and LED channels the game uses. A game-start run (trough full, Start pressed) shows the ROM
pulsing its trough feed coil repeatedly while no ball reaches the shooter lane.

## Mechanisms

### Three-ball trough

Three balls rest on 12-14 (Trough Ball 1-3); the Ball Trough coil (18) feeds one to the shooter lane.

### Shooter lane and autolauncher

The Autolauncher (17) kicks the ball resting on the shooter lane switch 11 into play; PinMAME's simulator also offers a manual plunger here.

### Right flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 3 (host public 112), the ROM fires the Right Flipper High (21) winding to lift the bat and holds it on the Right Flipper Low (19) winding, and the matrix end-of-stroke contact 15 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 4 (host public 114), the ROM fires the Left Flipper High (10) winding to lift the bat and holds it on the Left Flipper Low (12) winding, and the matrix end-of-stroke contact 21 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left slingshot

Slingshot switch 22 closes and the ROM fires the Left Sling (11).

### Right slingshot

Slingshot switch 16 closes and the ROM fires the Right Sling (20).

### Lower pop bumper

Skirt switch 44, coil 3.

### Left pop bumper

Skirt switch 45, coil 4.

### Right pop bumper

Skirt switch 43, coil 5.

### Left scoop

The Left Scoop coil (9) ejects a ball held on 25.

### Right scoop

The Right Scoop coil (13) ejects a ball held on 48.

### Orbit up-post

The Up Post (7) between the orbits (36 right, 46 left) returns an orbit shot instead of letting it loop.

### The Noid

The Noid figure turns on servo 0 (57, the chart's Noid Orbit servo); 58 (Noid Home) closes when it is at home, and the Noid orbits 37/38 run past it. PinMAME's simulator models it as a continuous-rotation servo.

### Noid target bank

Noid Bank Right/Middle/Left (26-28) on the target bank that servo 1 (58, Target Bank) lowers into the playfield.

## Evidence and remaining work

Factory chart transcriptions, the ROM service-test tables and the IPDB identity are under `evidence/excerpts/spooky-pinball.domino-s-spectacular-pinball-adventure.2016/`; the runtime
summary is `tools/pinheck_runtime.json` (rebuilt by `tools/pinheck_runtime.py` from the retained runs), the scenarios are
`tools/harness-scenarios/pinheck/dominos-*.json`. Remaining: the placements are measured on photographs rectified at playfield level (`photo-placements.md` names the photographs, the frame and its uncertainty, and every device left out). They stay observed: no factory location drawing or recreation table checks them, a position can be off by a few percent, and raised parts, parts hidden under the apron or ramps, GI and the RGB strings are not placed;
the mechanism inventory names each mechanism's coils, switches and service-test positions, but no retained source gives its home and startup state, its timing, how the ROM resets it or how it fails, so mechanism behaviour stays open until a manual, a known-working table or a gameplay harness run supplies it. The outputs whose fitment stays unknown: 25 (Backbox GI Output 0), 26 (Backbox GI Output 1), 27 (Backbox GI Output 2), 28 (Backbox GI Output 3), 29 (Backbox GI Output 4), 30 (Backbox GI Output 5), 31 (Backbox GI Output 6), 32 (Backbox GI Output 7), 37 (Playfield GI Output 8), 38 (Playfield GI Output 9), 39 (Playfield GI Output 10), 40 (Playfield GI Output 11), 44 (Playfield GI Output 15), 62 (External RGB LED 0 red), 63 (External RGB LED 0 green), 64 (External RGB LED 0 blue).
