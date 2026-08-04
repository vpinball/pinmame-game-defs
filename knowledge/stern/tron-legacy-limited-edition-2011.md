# TRON: Legacy Limited Edition (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, initial state, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `trn_100h`, `trn_110h`, `trn_130h`, `trn_140h`, and `trn_174h`. The exact `trn_174h` VPW-derived script is ground truth for controller callbacks, initial state, motion, and ball routing. The official LE service charts govern physical inventory and wiring. Pinned PinMAME governs public SAM serialization, the custom tricolor column, GI 0, synthetic game-on 33, and the native 128x32 four-bit DMD. IPDB 5707 identifies the Limited Edition as model I-00C2.

## Initial balls, launcher, and eject

Four balls initialize on trough switches 18-21. Output 1 ejects through jam opto 22, output 2 auto-launches from shooter switch 23, and the manual plunger remains functional. Flynn's video-game eject holds at switch 11; output 4 uses the proven 200-degree, force-24, Z-0.4 path with variance 2.

## Four-drop bank and motorized Recognizer systems

TRON switches 1-4 are a resettable four-bank on LE and output 3 raises all four. Separately, output 6 toggles the three-target Recognizer bank on switches 49-51 between down switch 52 and up switch 53. The exact V11 MotorBank primitive is x=448.69107 in the 952-wide frame, giving the canonical x=0.471314 assembly anchor used for switches 52/53 and output 6; its reviewed y remains 0.208014. The proven 29-step model initializes down, removes collisions near Z -76, and restores targets at Z -20. Output 23 runs the moving Recognizer toy: switch 54 activates near +18 degrees, 55 near center, and 56 near -18 while the toy oscillates between about ±20. Initialize the toy centered on 55 and the target bank down on 52.

## Spinning disc and orbit post

The Rinzler disc uses output 5 for power, output 22 for direction, and output 30 for its physical relay. The working table simplifies output 30 to a visual effect, but a physical recreation must retain it. Use the proven maximum speed 8, ±40 direction steps, 10 ms updates, and 0.1 coast-down as a motion baseline. The disc must impart velocity to balls; switch 41 is the disc-area opto. Output 7 raises the unsensed orbit post while active and drops it when clear.

## Three flippers and edition-specific controls

Outputs 15/16 drive lower left/right and output 12 drives upper-left. Lower button/EOS inputs are 84/83 and 82/81 with normally-closed EOS contacts. The official LE dedicated-switch chart on PDF page 55 leaves D13/D14 blank despite the upper flipper; the Pro chart on PDF page 49 explicitly populates them. The proven table stages the LE upper flipper from the left control by default or a separate authoring key. Its `SolCallback(34)` line is commented out and the key handlers call `SolULFlipper` directly, so public 34 is retained only as an explicit unused compatibility artifact. Do not invent physical public 88/87 contacts or a second output-34 coil for LE.

## Lighting

LE ordinary lamps are factory LEDs with its own map: 1-40, 42-43, and 45-66 are populated; 41, 44, and 67-80 are unused. The tricolor board adds right ramp public B/G/R 101/102/103 and left ramp B/G/R 104/105/106. The script proves independent color-channel control by passing each BGR triplet in reverse to an RGB helper; PinMAME source proves which C/D strobe belongs to each side. Source conflict: the official Stern manual (`manual.tron-legacy-pro-le.2011`, PDF page 57) maps Q19 to `FLASH: RIGHT DOMES (X2)` and Q25 to `FLASH: LEFT DOMES (X2)`, the opposite left/right mapping from the selected known-working V11 embedded script. V11 maps Q19 to setlampmod 125, whose LampMod 125 drives Flasher5/Flasher6 left-dome anchors, and Q25 to setlampMod 119, whose LampMod 119 drives Flasher1/Flasher2 right-dome anchors. The comparison VPW Mod 0.24 revision (`candidate-scripts/vpw-0.24.vbs`, script SHA-256 `ecea74df1775bd39cfd8838955adfefb544b5907d345223847369710fc4dac7d`; candidate VPX SHA-256 `ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4`) maps Q19 to its right-blue Flasher5/Flasher6 pair and Q25 to its left-yellow Flasher3/Flasher4 pair. The retained V11 embedded script remains the controller/behavior tie-breaker; the disagreement is preserved rather than reported as concordant.

## Routes and remaining devices

Ramps use 34/35/37/38, right inner loop 39, left/right orbits 43/46, and spinners 36/44. The physical location drawing and sustained VPX handlers identify CLU L/C/U 14/25/28 as lanes; ZUSE standup targets are 7/8/13/48, Zen rollover 12, and outlanes 24/29. Pops pair 9/30, 10/31, 11/32; slings 13/26 and 14/27. Output 8 is an optional 16 VAC shaker and output 24 an optional 5 V coin meter.

## Author construction checklist

- Build the typed four-ball state, launcher and manual plunger, Flynn eject, TRON drop bank, moving three-target bank, independent moving Recognizer with three sensors, disc power/direction/relay and physical ball contact, orbit post, three staged flippers, all routes/targets, flashers, ordinary LEDs, and both tricolor ramp assemblies.
- Preserve held-ball states, target-bank collision gating, endpoint cutoff, Recognizer transit, disc friction/throw and coast-down, and the upper-flipper shot. Do not collapse the two Recognizer mechanisms into one animation.
- Bind the complete explicit input/output spaces, including unused contacts, public RGB 101-106, synthetic game-on 33, GI 0, and the DMD.

## Sources

- `manual.tron-legacy-pro-le.2011`: official Stern manual, SHA-256 `1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84`; LE switches/coils/lamps PDF pages 55/57/59 and location maps 56/58/60.
- `vpx.tron-legacy-le-vpm-1.1.4`: exact known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc`.
- `runtime.tron-legacy-limited-edition.boot-start`: exact `trn_174h` harness, SHA-256 `92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM transport, custom lamp column, driver family, DMD, GI, and game-on output.

## Spatial coordinate model

Every normalized playfield placement uses the exact selected LE VPX's 952 by 2115 playfield frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron end. Direct object centers come from the retained `vpxtool git:v0.33.3` extraction and candidate report. The working LE script establishes controller semantics before any object is promoted. The official Stern manual remains physical truth for installed quantities, cabinet/back-panel locations, and assembly identity.

The exact LE table exposes direct points for all ordinary lamps 1-40, 42, 43, and 45-64, 35 GI authoring lights, both 23/29-point ramp RGB paths, direct flasher objects, switches, bumpers, flippers, kickers, and visible target faces. Render-only helpers (`lNa` overlays, reflective/material objects, `GIWhite`, `gibleed`, and similar) are not promoted. Lamp addresses 65/66 are cabinet button lamps; unused matrix lamps and absent LE dedicated contacts are explicit non-applicable records.

The official LE switch map proves four individual trough contacts and a jam opto, while this exact VPX models the trough as one BallRelease/kicker assembly. Switches 18-20 and 22 therefore retain manual-map regional projections with disclosure; switch 21 uses the exact BallRelease anchor. Slingshot contacts/coils, recognizer target-bank contacts, motorized Recognizer endpoints, the three internal Recognizer-toy contacts, EOS leaves, and target-bank reset are likewise distinct controller devices with assembly anchors where the VPX does not expose an internal component center. No helper/render object is used as a physical switch or coil.

Source conflict: the official Stern manual (`manual.tron-legacy-pro-le.2011`, PDF page 57) maps Q19 to `FLASH: RIGHT DOMES (X2)` and Q25 to `FLASH: LEFT DOMES (X2)`, the opposite left/right mapping from the selected known-working V11 embedded script. V11 maps Q19 to setlampmod 125, whose LampMod 125 drives Flasher5/Flasher6 left-dome anchors, and Q25 to setlampMod 119, whose LampMod 119 drives Flasher1/Flasher2 right-dome anchors. The comparison VPW Mod 0.24 revision (`candidate-scripts/vpw-0.24.vbs`, script SHA-256 `ecea74df1775bd39cfd8838955adfefb544b5907d345223847369710fc4dac7d`; candidate VPX SHA-256 `ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4`) maps Q19 to its right-blue Flasher5/Flasher6 pair and Q25 to its left-yellow Flasher3/Flasher4 pair. The retained V11 embedded script remains the controller/behavior tie-breaker; the disagreement is preserved rather than reported as concordant. Outputs 20/21 retain their distinct left/right bottom-arch semantics; 20 is manual-only because `Linkerflasher` is outside the table frame, while 21 keeps exact in-bounds `Lanelight` and documents the outside-bounds companion. GI output 0 is the aggregate physical GI circuit and has 35 exact direct emitters, not a second compatibility lamp. RGB outputs 101-103 and 104-106 are independent blue/green/red controller channels that co-locate on one physical 29-module right-ramp or 23-module left-ramp RGB emitter string respectively; each channel repeats the shared coordinate set for channel addressability and is not a separate physical string.

The selected exact table is retained at `external:pinmame-vpx-sources/stern/tron-legacy-limited-edition-2011/VR Room Tron Legacy (Limited Edition) (Stern 2011) V11.vpx` with VPX SHA-256 `56ad2f5318c33dbc12f3aa2515a41d819eb8b95b2ffcd94ebe1044cec4281ae5`. The deterministic candidate report is `evidence/vpx/tron-legacy-limited-edition-2011-v11-spatial-candidates.json` with SHA-256 `318297fb178098929d62078075f891ee301067cff58ad778f683b577f83b8ff4`. Rejected local alternatives include the explicitly re-themed `TRON Classic (Original 2018) Mod v1.02.vpx`; Pro/non-LE candidates were not promoted.
