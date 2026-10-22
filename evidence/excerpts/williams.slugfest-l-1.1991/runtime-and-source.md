# Retained script and emulator contract

VPX original SHA-256 c75825c0c39fcd89cc9d6c7c60d18fe3257e2c0a07a6321f43306c6d8e244424;
embedded script 162f1067a1c0c1f72509b69cde2dc9381f26ccb425f56830e1c8792041fa1f25.
Credits name DancingCan, Roccodimarco, Tab, Destruk and the listed VPW physics
and sound contributors; v1.2 release date October 18 2026. Script line 33 selects
sf_l1; 99 loads WPC.VBS. Line 623 enables the documented PinMAME startup-test
bypass in the COM interface; the native harness has a separate unmodified boot.

Script 576–604 registers PWM output 1; binary 2,7,21–24,27,28; PWM flashers
17–20,25,26; one GICallback2. Line 654 maps collection AllLamps via vpmMapLights.
Membership and each Light.TimerInterval determine runtime identity, not names.
Collection has 59 lights:53 playfield inserts and 6 control-panel lights 81–86;
it omits the three physical bleacher lamps 11/21/31. Their omission is a table
gap, not proof of non-fitment.

736–754 releases direct controls and defines SetGameSwitch. 760–763 maps
buttons to 32,32,34,33,35,31,25,36. 916–995 binds bat 26, two coin inputs 1/2,
start 37/38; right-flipper handler also writes generic 112. The bat is moved by
BatPress/BatRelease (1554–1570), a table fallback, while SolBatOutput(1) records
ROM state without transform authority. This does not prove output 1 is unused
or that the physical bat lacks its documented coil.

1030–1047:21 moves ramp,22/23/24 request fast/medium/slow pitch profiles,
27 drives dispenser,28 records low-card illumination. 1128–1146 maps GI
callbacks 0–4 to InfieldTop/Backbox/PitchLamps/Outfield/InfieldBottom collections.
The script explicitly calls GI1/GI2 regional and GI4 provisional. It disables
GI5 corner helpers in its current visual configuration; those settings cannot
establish physical socket count or rewire the machine.

1462–1515 initializes ramp down, pitch home, target contacts clear, prize 23=0,
low 27=0 and unjammed 28=1. That last value substitutes a held acknowledgement
button; factory 1-9/1-10 says it is pressed after recovery, not a health sensor.
1618–1750 integrates a unidirectional ramp cam,
reports 55 from its occlusion and updates collision state only at endpoints.
2351–2456 animates the pitch unit and reports home 54. 2630–2698 pulses
41+targetIndex from seven left-to-right card-face contacts; rearTrigger1
uses shared X boundaries as fallback. This settles center 44/right-of-center 45
against the location table's transposition.

2706–2798: dispenser output 27 rising edge starts a cycle; prize 23 pulses only
on confirmed card advance, low 27 follows simulated stock, unjammed 28 stays
active unless faulted (a table simplification of the operator button). 15 initial cards and 120/180/60/140 ms windows are table
tuning, not factory measurements. 3230–3248 writes constant 24 and occupancy
51=return pulse,52=strike,61/62/63=three return routes. Six registered balls
are created once; hidden transport states conserve them through the pitcher,
playfield, rear return, strike return and three grandstand routes.

PinMAME 97aa922bf8e4b6970126192ec1ac1fb0305a4f62, src/wpc/bowlgames.c:477–502:
sfGameData uses GEN_WPCDMD, wpc_dispDMD, all-zero hardware/flipper fields and no custom
lamp/output/mechanism handler. Inversion bytes for columns 5/6 are 0x18/0x07,
so public 54,55,61,62,63 are masked. Root sf_l1 and clone sf_d1 share init_sf,
wpc_mDMDS and the same three sound ROMs. D1 is the LED Ghost Fix variant.

src/wpc/wpc.c:97–99 defines a 128x32 DMD;642–660 reads generic flipper column
complemented, dedicated coin-door column directly and the matrix through
core_getSwCol. sf has no security PIC. 506–530 publishes WPC_GILAMPS high bits
as outputs 29–31. Bits 5/6 are unconditionally mirrored into public 29/30,
defining used virtual register-state outputs independently of attached J111
loads or this game's physical use, which remain unproven. Bit 7 is the
pre-Fliptronic relay state at 31, not solenoid 19. The game's own fitted
A-12697-1 assembly and circuit independently establish its physical relay.
core.c:1778–1855 synthesizes lower-flipper states from generic buttons even
without physical flippers; sf's zero flipper declaration provides no copied
matrix flipper switch or modeled EOS. core_getSol remaps WPC 29–31 and upper
flipper callbacks. Public 32 is constant zero: only three high register bits
are copied into the remapped WPC state field. It is an unused virtual output,
not a fitted load. Other reserved holes must not acquire invented hardware.
The model's unclaimed generic inputs and any J111 physical function remain
explicit unknowns until a targeted probe or wiring source settles them.
