# Rob Zombie's Spookshow International (Spooky Pinball, 2016)

This definition covers the physical machine (IPDB 6416, 6417, model 00002) and its one
PinMAME driver, `rzspook_026`, the V26 code update on the Spooky Pinball pinHeck board (PIC32MX795 game CPU, Parallax Propeller
display/sound/media CPU). It is partial: every controller address is enumerated and checked against the ROM's own service
tests and named, but the placements are measured on photographs, not a factory drawing, the mechanisms are inventoried
without their full behaviour, and some outputs keep an unknown fitment.

## Machine

Rob Zombie's Spookshow International has a seven-ball trough, three flippers, four slingshots, a drop target guarding a rail lock and an elevated mini-playfield behind the Spaulding gate. The GI_1 header names bottom playfield GI 1 and 2 (38, 39), red GI lamps (40), the purple and red flashers (41, 42) and white GI lamps (43); its pin 15 is a key position. The Living Dead Girl figure is lit by the external WS2801 chain's first LED, whose green and blue arrive on PinMAME's B (64) and G (63) slots, as the ROM's own RGB test shows.

Editions: IPDB 6416 Standard Edition (250 units (confirmed), February 2016); IPDB 6417 Limited Edition (50 units (confirmed); IPDB: a different backglass, different side rails and a numbered plaque).

## Running it

The romset is Spooky's rzupdate_V26.zip code update (Google Drive link on spookypinball.com): RZO_V026.PRG, PRP_V008.BIN and the SD card's DMD/ and sound folders, loaded as `rzspook_026.zip`. PinMAME before 97aa922b
named it `rzspook.zip`, and the retained harness scenarios still name that set. pinHeck also needs `pinheck.zip` holding the Propeller's 32 KB mask ROM (`p8x32a.rom`, CRC32 f99b3070).
On an empty NVRAM the ROM first programs its program flash and AV EEPROM from the romset (about eight emulated minutes), shows CODE UPDATE COMPLETE / PLEASE RESTART, and after the next start once more asks for a restart; from the third start it boots to attract mode. The harness runs started from a retained copy of that post-update NVRAM.

## Controller contract

The platform contract is `controllers/pinmame/pinheck.json`. In short: factory switch and lamp `n` (0-63) are public
`(n / 8 + 1) * 10 + n % 8 + 1` (11-88); cabinet inputs are 1-8 and 91-97; the host drives the flipper buttons at 112 (right) and 114
(left), which PinMAME copies to cabinet inputs 3 and 4; factory coil `n` is public `n + 1` (1-24); GI outputs 0-7 are 25-32 and 8-15
are 37-44; 51-56 are the on-board RGB LEDs, 57-61 the servos (0-255 position), 62-64 the external or third RGB LED; the Start lamp
is 91. On every switch public 1 is the closed contact; no switch is inverted. 52 inputs, 36 solenoid-group
outputs and 49 lamps are used.

## What the ROM itself proves

Every pinHeck game has the same operator menu (Enter, 6, opens it; the right flipper button steps; Back, 5, leaves). Its Switch
Edge test draws each closure in an 8x8 grid laid out like the factory chart, so closing every public address proved the
switch formula for all 64 matrix positions and the cabinet mapping for 2-8 and 91-97. The Solenoid test names each of the 24
coils, and pressing Enter fired exactly coil `n + 1` every time. The Lamp test names the sixteen GI outputs (the playfield group
44 down to 37, the backbox group 32 down to 25) and then every matrix lamp by its factory number, lighting only that address. The
Servo and RGB tests name the servos and LED channels the game uses. A game-start run (trough full, Start pressed) shows the ROM
pulsing its trough feed coil repeatedly while no ball reaches the shooter lane.

## Mechanisms

### Seven-ball trough

Seven balls rest on 12-18 (Trough 1-7); BALL LOAD (18) feeds one to the shooter lane. In the game-start run (all seven contacts closed, Start pressed) the ROM pulsed 18 every 6 s for 20 s, because no ball ever reached the shooter switch.

### Shooter lane and autolauncher

AUTOPLUNGER (17) kicks the ball resting on the shooter lane switch 11 into play; PinMAME's simulator also offers a manual plunger.

### Right flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 3 (host public 112), the ROM fires the RFLIP HIGH (20) winding to lift the bat and holds it on the RFLIP LOW (19) winding, and the matrix end-of-stroke contact 24 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 4 (host public 114), the ROM fires the LFLIP HIGH (14) winding to lift the bat and holds it on the LFLIP LOW (13) winding, and the matrix end-of-stroke contact 25 tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Upper flipper

The upper flipper on UFLIP HIGH (3) and UFLIP LOW (8) with its end-of-stroke contact 41; the ROM fires it from the right button.

### Left lower slingshot

Switch 26, coil 12 (LEFT SLING).

### Left upper slingshot

Switch 57, coil 11 (UL SLING).

### Right lower slingshot

Switch 23, coil 21 (RIGHT SLING).

### Right upper slingshot

Switch 32, coil 22 (UR SLING).

### Right pop bumper

Skirt switch 36, coil 6.

### Lower left pop bumper

Skirt switch 54, coil 9 (LLEFT POP).

### Upper left pop bumper

Skirt switch 55, coil 10 (ULEFT POP).

### Vertical up-kicker

The VUK (4) lifts a ball held on 43; 44 (Secret Passage) feeds it.

### Drop target and rail lock

A single drop target (48) guards the right inner orbit (35); the Drop Target coil (7) resets it. With it down, the orbit leads to a rail lock: Right Rail Lower (33) and Upper (34) hold balls behind the BALL STOP post (5, the chart's stop post on the right inner orbit), which drops to release one.

### Spaulding gate and upper playfield

Servo 0 (57, Spaulding) is the gate to the elevated mini-playfield: GATE OPEN and GATE CLOSE in the Servo test. Opto 95 sees the ball at the gate, 37/38 are the upper playfield's switches and opto 96 sees it leave.

### Captain Spaulding robot

The animated robot is servo 1 (58): ROBOT START and ROBOT END in the Servo test.

### Living Dead Girl

The Living Dead Girl figure with targets 46 (right) and 47 (left), lit by the first LED of the external WS2801 chain: LDG RED on 62, LDG GREEN on 64 and LDG BLUE on 63.

## Evidence and remaining work

Factory chart transcriptions, the ROM service-test tables and the IPDB identity are under `evidence/excerpts/spooky-pinball.rob-zombie-s-spookshow-international.2016/`; the runtime
summary is `tools/pinheck_runtime.json` (rebuilt by `tools/pinheck_runtime.py` from the retained runs), the scenarios are
`tools/harness-scenarios/pinheck/rzspook-*.json`. Remaining: the placements are measured on photographs rectified at playfield level (`photo-placements.md` names the photographs, the frame and its uncertainty, and every device left out). They stay observed: no factory location drawing or recreation table checks them, a position can be off by a few percent, and raised parts, parts hidden under the apron or ramps, GI and the RGB strings are not placed;
the mechanism inventory names each mechanism's coils, switches and service-test positions, but no retained source gives its home and startup state, its timing, how the ROM resets it or how it fails, so mechanism behaviour stays open until a manual, a known-working table or a gameplay harness run supplies it. The outputs whose fitment stays unknown: 25 (Backbox GI Output 0), 26 (Backbox GI Output 1), 27 (Backbox GI Output 2), 28 (Backbox GI Output 3), 29 (Backbox GI Output 4), 30 (Backbox GI Output 5), 31 (Backbox GI Output 6), 32 (Backbox GI Output 7), 37 (Playfield GI Output 8), 44 (Playfield GI Output 15).
