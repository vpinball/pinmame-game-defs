# Gorgar (Williams, 1979)

Coverage is **partial**. The Gorgar definition covers the System 6 controller, direct and matrix I/O, the six segment display groups, and the observed L-1 mechanism behavior. Physical switch and effect projections come from the retained VPinMAME tables. Some physical positions, L-2 hardware verification, and the firmware purpose of the unfitted lamp address 47 remain open.

## Machine and firmware

Gorgar is Williams model 496, a December 1979 four-player System 6 game. The factory documentation identifies the optional Speech Module and separates it from the sound board. PinMAME's six sets share `INITGAMEFULL(grgar,s6_6digit_disp,0,0,38,37,39,12,36,0)`, the System 6 speech-capable driver and the sound/speech ROMs. The production L-1 archive agrees with the pinned ROM member hashes. L-1FF and T-1FF change green flipper ROM 1 to retain the knocker in free play. T-1 and T-1FF use Ted Estes's green ROM 2 (divide-by-ten scoring per the source's C-1 bundle note). The aftermarket C-1 game ROM uses slam tilt as a lane-change trigger. Model a distinct user input for its repurposed line if supporting that mod. L-2 adds a guard before queuing the pit flash output. PinMAME does not verify that this version shipped or ran on a physical Gorgar.

## Ball path and reset

The single ball returns to the outhole when drained. Switch 9 remains closed while the ball rests there. Solenoid 1 feeds the shooter lane, and the player launches with a manual plunger. The embedded VPX relocates the ball from its Drain object to the shooter lane by creating the departing ball at BallRelease. Use the physical outhole as the device location. The separate left eject saucer holds a ball on 15 and releases it on 2. It awards 5,000 at base value, the flashing higher value, or an extra ball when lit. The GOR/GAR completion progression advances the saucer awards.

G-O-R on the left uses target switches 18–20, series switch 21 and reset coil 4. G-A-R uses 41–43, series switch 44 and reset coil 3. Individual switches stay closed while their target stays down. Close the matching series input only once all three targets are down, then open those inputs when the coil raises the bank. Rear standups 22 and 40 are separate scoring inputs behind the corresponding banks. G-O-R advances the Snake Pit awards. G-A-R advances the jets and the GAR scoring opportunity. A-E and targets 1–4 advance bonus, and A-B-C advances the multiplier.

## Snake Pit

The upper-left switch 23 is a leaf switch. On entry, solenoid address 5 controls playfield relay 8L5, whose contact switches the separate 20-8991 electromagnet to ground. The ball is held against the pit assembly and releases when the relay drops. Drive the stop magnet and the two 89 flash lamps separately. Solenoid output 6 reaches bulbs 8B65 and 8B66. Matrix lamps 33–37 display the pit award ladder from 5,000 to 50,000. The factory booklet gives 1,000 or the flashing value on the hit and returns awards of 20,000 or more to 1,000.

In the L-1 trace, relay 5 asserted about 15 ms after switch 23 closed and stayed on about 735 ms. The first flash transition followed about 719 ms after the closure, followed by further pulses. The host held switch 23 for four seconds; the trace settles the relay and flash timing for that event. SS20 identifies leaf bounce as a source of solenoid fuse failures. It gives the contact settings and isolates the early shared return of the flash lamps and magnet from the special switches. The retrofit preserves the logical outputs.

## Flippers, special solenoids, and illumination

- Game-on 23 enables the flipper relay Z1 and the five special drivers. The physical buttons and EOS contacts control the dual-wound flippers. In PinMAME, public buttons 82 and 84 drive 45/46 and 47/48 respectively, each pair asserted together. None is copied to a Gorgar matrix cell.
- Top, left and bottom pop bumpers and the left and right slings have separate direct-drive switches. The scoring closures 38, 37, 39, 12 and 36 model their timed effects on public 17–21 in that order. The harness verified those five pairings during play.
- General illumination runs from the 6.3 VAC winding to cabinet, playfield and backbox insert board. System 6 exposes no dedicated G.I. group. The newer VPX has 23 modelled playfield G.I. bulb locations, listed in the spatial audit. Playfield and backbox G.I. factory counts and positions still need physical verification. Cabinet G.I. shows three bulbs. Matrix outputs 50–55 and 57–64 are backbox inserts. Places where a legend shares multiple lamps use the insert diagram's quantity.
- Matrix position 47 is unfitted in both the booklet and the schematic. In the L-1 gameplay probe the ROM still pulsed 47 for 78 ms at G-A-R completion, shortly after switch 44 closed. The pulse's firmware purpose is open. The wiring gives it no physical emitter.
- The wired playfield credit lamp is public 56. The older archive VPX omits it and names the A rollover trigger `sw24` while writing public 26. The physical standup input 24 is separate. The newer [RetroRitchie and Darth Vito v2.0 release](https://vpuniverse.com/files/file/20315-gorgar-williams-1979/) maps 56, models standups 13, 22 and 24, and uses `sw26` for the A rollover. No matching loose VBS sidecar accompanies either file. Both embedded scripts were checked statically, and the ROM behavior was exercised in LibPinMAME without launching VPX.

## Retained evidence

The [factory excerpts](../../evidence/excerpts/williams.gorgar.1979/) cover the booklet, schematic and SS20. The [L-1 observations](../../evidence/runtime/williams.gorgar.1979/gameplay.json) pin the initial CMOS run, subsequent gameplay, ROM members and native library. The host supplies switch transitions for ball positions and target feedback. At Start and after drain, coils 3 and 4 reset the banks before coil 1 serves. Each bank remained down through three held contacts and reset only after its series input closed in this probe. The ball-roll tilt dropped game-on during play.

The [spatial report](../../reports/spatial/williams/gorgar-1979.md) records the VPX objects, normalization and remaining socket and contact evidence. The photographs establish layout and show mechanisms absent from the VPX. They have not been used as a calibrated socket survey. The newer build's lamp-mapped light sources are listed there for comparison with physical socket evidence.
