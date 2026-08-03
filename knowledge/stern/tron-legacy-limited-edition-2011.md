# TRON: Legacy Limited Edition (Stern, 2011)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical inventory, PinMAME bindings, custom mechanisms, wiring, initial state, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `trn_100h`, `trn_110h`, `trn_130h`, `trn_140h`, and `trn_174h`. The exact `trn_174h` VPW-derived script is ground truth for controller callbacks, initial state, motion, and ball routing. The official LE service charts govern physical inventory and wiring. Pinned PinMAME governs public SAM serialization, the custom tricolor column, GI 0, synthetic game-on 33, and the native 128x32 four-bit DMD. IPDB 5707 identifies the Limited Edition as model I-00C2.

## Initial balls, launcher, and eject

Four balls initialize on trough switches 18-21. Output 1 ejects through jam opto 22, output 2 auto-launches from shooter switch 23, and the manual plunger remains functional. Flynn's video-game eject holds at switch 11; output 4 uses the proven 200-degree, force-24, Z-0.4 path with variance 2.

## Four-drop bank and motorized Recognizer systems

TRON switches 1-4 are a resettable four-bank on LE and output 3 raises all four. Separately, output 6 toggles the three-target Recognizer bank on switches 49-51 between down switch 52 and up switch 53. The proven 29-step model initializes down, removes collisions near Z -76, and restores targets at Z -20. Output 23 runs the moving Recognizer toy: switch 54 activates near +18 degrees, 55 near center, and 56 near -18 while the toy oscillates between about ±20. Initialize the toy centered on 55 and the target bank down on 52.

## Spinning disc and orbit post

The Rinzler disc uses output 5 for power, output 22 for direction, and output 30 for its physical relay. The working table simplifies output 30 to a visual effect, but a physical recreation must retain it. Use the proven maximum speed 8, ±40 direction steps, 10 ms updates, and 0.1 coast-down as a motion baseline. The disc must impart velocity to balls; switch 41 is the disc-area opto. Output 7 raises the unsensed orbit post while active and drops it when clear.

## Three flippers and edition-specific controls

Outputs 15/16 drive lower left/right and output 12 drives upper-left. Lower button/EOS inputs are 84/83 and 82/81 with normally-closed EOS contacts. The official LE dedicated-switch chart on PDF page 55 leaves D13/D14 blank despite the upper flipper; the Pro chart on PDF page 49 explicitly populates them. The proven table stages the LE upper flipper from the left control by default or a separate authoring key. Its `SolCallback(34)` line is commented out and the key handlers call `SolULFlipper` directly, so public 34 is retained only as an explicit unused compatibility artifact. Do not invent physical public 88/87 contacts or a second output-34 coil for LE.

## Lighting

LE ordinary lamps are factory LEDs with its own map: 1-40, 42-43, and 45-66 are populated; 41, 44, and 67-80 are unused. The tricolor board adds right ramp public B/G/R 101/102/103 and left ramp B/G/R 104/105/106. The script proves channel order by passing each triplet in reverse to an RGB helper; PinMAME source proves which C/D strobe belongs to each side. A resolved source disagreement remains explicit: the official coil chart on PDF page 57 says 19 right domes and 25 left, while the proven VPX callbacks say 19 left and 25 right. Per the project-wide ground-truth policy the working script wins for controller-facing semantics, so this definition uses 19 left and 25 right while retaining both locators for physical orientation.

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
