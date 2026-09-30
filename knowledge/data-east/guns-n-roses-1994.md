# Guns N' Roses (Data East, 1994)

This definition describes the production machine and all three pinned 3.00 ROM
variants. It remains partial for the explicit socket/geometry and upper-coil
blockers in the spatial report; address enumeration is complete.

Six balls circulate and one remains captive. Initialize trough switches 9-14
active before starting the controller. Switch 15 is a real seventh/right trough
sensor; VPW's virtual
staging is an implementation convenience. Boot/missing-ball diagnostics must
not be confused with a phantom contact. Gun switch 62, right shooter switch 16
and auto-launch coil 3 are separate from the rose-handle spring plunger and left
shooter switch 24.

The two three-drop banks latch independently; reset coil 12 clears switches
33/34/59 and reset coil 9 clears 36/35/57. Four captive DUFF standups 17-20 and
JAM lanes 21-23 are distinct. Special drivers 17-22 are CPU/PIA-driven; GnR has
no ssSw host autofire mapping. All 64 matrix lamps are fitted, including cabinet
lamp 63 Extra-Ball and 64 Credit; 55 has two playfield bulbs. Three center-playfield
magnets 51-53 mirror 37-39 and use the
factory latch permutation. Do not add three duplicate magnets at raw addresses.

Flippers use the SSFB, with timed 50 V power and lower 8 V holding circuits.
Physical EOS contacts are normally closed knockback retriggers outside the ROM
matrix. Consumer buttons 82 (right) and 84 (left) are copied to matrix 64/63;
direct writes to 63/64 cannot operate them. Active Switch Test calls those matrix
addresses RIGHT/LEFT END OF STROKE, but the pinned core proves they receive the
button copies. Public outputs 45-48 are synthetic controller states. Public 36
never drives a GnR coil. The upper staged flipper works through de.vbs/core.vbs
cvpmFlips2 direct callback capture while 23 enables flippers. A recreation must
provide the third physical flipper and staged host control without inventing
a CPU coil 36 or ROM switch 88. Upper coil factory chart 25-1100 versus BOM 23-1100
is recorded honestly.

Output 10 selects the PPB left/right mux: 1-8 are mechanical left loads and 25-32
are right flasher banks. Output 11 is a physical GI relay, despite PinMAME's
reversed #44 brightness model. Asserted binary 11 cuts GI; release restores it.
No separate Data East GI output namespace exists. Each flasher bank has four
bulbs, distributed between playfield and backbox: 14 playfield and 18 backbox
bulbs in total. The older Team PP script shares glow objects, reverses output 31
and has bad l2/l3 timer bindings.
Those implementation defects stay in notes; they do not change factory wiring.

The exact retained geometry has bounds 1000x1902. Positions use player view,
x left-to-right and y rear-to-front. Collidable walls use polygon area centroid;
coil effects project to their actual mechanism. Factory drawing leaders check
identity, not exact socket offsets. Primitive origins, Flasher sprites,
lightmaps, blooms and reflections are excluded. The local old tables contain
three flipper pivots. The upper-left is LeftFlipper1; the older embedded script
moves it with the lower-left, while VPW supplies staged control. No per-contact
trough geometry is present. Each sling has two physical leaf contacts; one VPX
impact-region wall cannot locate both. The retained visual helpers cannot establish
every fitted GI/flasher socket.

ROM evidence uses the verified pinned DLL and US 3.00 in new empty state.
The bounded DMD adapter matches exact header pixels and waits for game-on 23
after transient service titles. Holding Start cycles all three magnets; in Laser
Kick Test, switch 54 fires 14, 37 fires 4, 39 fires 5 and 38 fires 6. Host left/right
buttons generate 47/48 and 45/46. Active Switch Test screenshots display bumper,
sling, trough and trigger names; public readback alone is never counted as proof.

French CPU/DMD and Dutch CPU differ; Dutch DMD contents match US under a
different filename. Sound images, controller transport and physical I/O are
shared. US DMD header templates are not verified for localized firmware.
Prototype extra standup/insert, captive rest-rollover and mini-loop contact are
not production fitment; historical unbuilt stage-lock ideas are not mechanisms.
Optional factory headphone jacks do not add PinMAME I/O.

Factory SB63 (October 4, 1994) addresses auto-launch failures; SB64 (November 1, 1994)
changes shooter-ramp mounting. Retained primary documents and secondary
prototype description stay external, hashed and attributable. No physical
ball-path force, animation timer or magnet radius is inferred from VPX tuning.

## Six-ball trough and lockout

Six active balls rest on 9-14; 15 is the seventh/right staging contact. Lock-ball assembly 500-5684-01 and trough are separate cooperating assemblies. Driver 1 operates the 25-1240 lockout linkage; driver 2 ejects with 23-800 toward shooter 16. VPW initializes 9-14 active, shifts its six kicker objects on a 300 ms timer, asserts 15 after SolTrough and clears it after SolRelease. Those local kicks are a surrogate, not proof of physical coil timing. Unexpected occupancy invokes ball search / missing-ball diagnostics.

## Gun trigger and right auto launch

Spring-return 22-600 striker auto launches the right shooter lane when the gun microswitch 62 requests launch. Gun 500-5834-00 has a trigger spring and no separate solenoid. The rose plunger is physically separate. SB63 addresses electrical launch failures: failed climbs can accumulate balls and overheat the coil. It describes a 3.00 watchdog disabling auto launch on repeated shooter-switch closures. SB64 lowers the rear ramp mount approximately half an inch and advances its entrance in the routed slots.

## Left rose handle manual shooter

Manual long-shaft spring plunger returns from pulled to released, propelling the left shooter lane. No CPU coil drives the rose handle. VPW shares a host plunger key with gun trigger, and permits rose pull/fire only when no ball is in the right shooter; do not merge those two physical controls.

## Upper-left ball eject

24-940 coil pulls a plunger/link and pivots an eject cam; spring restores it. Switch 37 reports an occupied cup. Driver 4 ejects, validated in the ROM kick test. Legacy upper-left VUK ID stays stable although the factory calls it Eject.

## Upper-right vertical up-kicker

25-1240 vertical striker lifts the captured ball into the upper wireform; 39 detects occupancy. Spring restores the plunger. Driver 5 fires in ROM kick test. VPW destroys/creates a ball on the wireform as a simulation technique.

## Center power scoop and Kick Big

Power scoop and 500-5740-00 Kick Big are separate assemblies working together. 38 is the scoop microswitch, driver 6 is a 50V 23-800 striker. VPW can retain up to three balls before kicking; destroy/create and timer logic implement a virtual stack, not additional sensors. ROM kick test confirms 38 to 6.

## G-ramp trap door and snake-pit route

28-1050 plunger, linkage pin and flap control a hole in the G ramp. VPW starts SolTrapDoor 0 closed; assertion opens the drop route and release restores the ramp route. The ramp enter/exit and funnel switches detect balls, not door position. No home/limit sensor is fitted in the complete switch chart.

## Right three-drop bank

Each target latches down on impact and closes its own switch; one 23-800 reset lifts all three. Bottom/middle/top are 36/35/57, not numeric order. Script holds closure until bank reset; stock BOM on page61 includes unused 2/4-bank options that do not make this game a larger bank.

## Left three-drop bank

Each target latches down; one 23-800 reset lifts the whole bank. Bottom/middle/top 33/34/59. The exact scripts reset through driver 12.

## Left outlane Laser Kick

A 50V 23-800 striker returns a left-outlane ball to play; spring restores it. Outlane closure 54 fires 14 in the dedicated ROM test after game-on 23 enables outputs. It is distinct from manual shooter 24, though the retained table kicks its left-lane plunger for the effect.

## Captive DUFF ball and four standups

One captive ball strikes four DUFF standups; six other balls circulate. D/U/F/F are four distinct contacts, not duplicates. The historical prototype rest-rollover, mini-loop sensor and extra Time To Rock standup were removed before production and are not silently populated into unused addresses.

## Three center-playfield electromagnets

Three separately switched magnetic fields disturb rolling balls; no position marks, limit contacts or fourth magnet. Board Q1/Q2/Q3 map to center/left/right via the factory latch permutation and exact script. Hold Start in Magnet Test to cycle all three. They begin deenergized; GrabCenter=False means no scripted ball pinning. SB63 states that 3.00 turns the magnets off in multiball when a 50 V coil fires, reducing shared supply loading; the service-test traces do not independently exercise that gameplay condition. The 16 force radius is table tuning, not a factory measurement.

## Lower-left flipper

Cabinet-wired SSFB coil 22-1080: timed 50V actuation, 8VAC-derived holding power, spring return. Normally-closed physical EOS can retrigger power on knockback; it has no GnR ROM-readable address. Output 23 enables the host flipper controller; 47/48 are synthetic states, not additional physical coils.

## Lower-right flipper

Same SSFB timed power/hold topology with a right cabinet button. Host 82 copies to matrix64 and fabricates45/46 while23 is enabled. Lower physical EOS belongs to the SSFB circuit and is not host81.

## Staged upper-left flipper

Third physical flipper, driven directly by a staged cabinet contact through SSFB channel C. No upper EOS in the factory flipper chart. VPW cvpmFlips2 captures the callback keyed by36 and invokes it from the host staged input; core cannot publish36. Factory chart25-1100 conflicts with assembly23-1100; retain that unresolved part difference and do not invent an active ROM coil.

## Left turbo bumper

Ball impact tilts the skirt and closes the leaf contact; the ROM drives the 23-800 coil, pulling the plunger/yoke and rod/ring down to repel the ball. The spring restores the resting ring. GnR has no ssSw array; do not add host autofire bypasses.

## Bottom turbo bumper

Ball impact tilts the skirt and closes the leaf contact; the ROM drives the 23-800 coil, pulling the plunger/yoke and rod/ring down to repel the ball. The spring restores the resting ring. GnR has no ssSw array; do not add host autofire bypasses.

## Right turbo bumper

Ball impact tilts the skirt and closes the leaf contact; the ROM drives the 23-800 coil, pulling the plunger/yoke and rod/ring down to repel the ball. The spring restores the resting ring. GnR has no ssSw array; do not add host autofire bypasses.

## Left slingshot

Two leaf contacts detect rubber deflection through one matrix circuit. The ROM drives the 23-800 coil; its plunger/link pivots the arm and tip into the rubber to repel the ball, and the spring restores the resting arm. The top assembly rotates the coil 90 degrees. GnR has no ssSw array; do not add host autofire bypasses.

## Right slingshot

Two leaf contacts detect rubber deflection through one matrix circuit. The ROM drives the 23-800 coil; its plunger/link pivots the arm and tip into the rubber to repel the ball, and the spring restores the resting arm. The top assembly rotates the coil 90 degrees. GnR has no ssSw array; do not add host autofire bypasses.

## Top slingshot

Two leaf contacts detect rubber deflection through one matrix circuit. The ROM drives the 23-800 coil; its plunger/link pivots the arm and tip into the rubber to repel the ball, and the spring restores the resting arm. The top assembly rotates the coil 90 degrees. GnR has no ssSw array; do not add host autofire bypasses.

## Cabinet knocker

23-800 striker hits the cabinet stop and spring returns; no position sensor or playfield emitter.

## Evidence and remaining work

Factory transcriptions: evidence/excerpts/data-east/guns-n-roses-1994/. Exact object locators/hashes: tools/guns_n_roses_geometry.json. Runtime hashes and expected transitions: tools/guns_n_roses_runtime.json and reusable tools/harness-scenarios/gnr-300-magnet-laser.json. Complete originals, extraction manifests, ROM inventory, fresh-state traces and native renders remain under the external working root.
