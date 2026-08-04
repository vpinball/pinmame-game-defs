# Transformers Limited Edition (Stern, 2011)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers Limited Edition drivers `tf_088h`, `tf_100h`, `tf_120h`, `tf_130h`, `tf_140h`, `tf_150h`, and root `tf_180h`. Firmware dates in the PinMAME catalog extend into 2012/2013, but the physical product is the 2011 Limited Edition. The official Stern service charts govern complete I/O and wiring; the exact `tf_180h` harness validates the SAM address stream, native DMD, GI, and installed auxiliary output mapping; contemporary physical review supplies mechanism behavior that the diagnostic charts do not explain. No public proven LE VPX table was found, so no Pro-only table behavior is silently promoted to LE.

## Controller topology and auxiliary serialization

Matrix switches are public 1-64; dedicated controls are 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. Main outputs are 1-32, lamps 1-80, and GI 0. The installed 12-transistor auxiliary board uses physical Q41-Q46, which PinMAME serializes as public outputs 59-64. Public 51-56 represent unpopulated Q51-Q56 and 57/58 plus 65/66 are compatibility gaps; all ten are explicit unused entries. The exact-ROM boot run observes public 63 active, corroborating Q45 to public 63 rather than a naive Q45 to 55 mapping.

## Megatron system

The four-ball mini-trough is common with the Pro: switches 41, 40, 39, and 38 sense the stack, switch 42 senses the exit, and output 3 ejects one ball per pulse. The LE adds a motorized drop target at the entrance: switch 64 senses a hit, outputs 6/7 drive down/up, and switches 47/48 confirm those endpoints. Main output 26 powers movement of the Megatron figure. Auxiliary public 61/physical Q43 kicks the cannon in recoil as the trough ejects; the ball never travels through the barrel. The ball-trap assembly is `511-6977-00`.

## Starscream platform

The Starscream target platform rotates to alternately expose or block the target between the figure's legs. Public outputs 59/60 map to Q41/Q42 and supply motor power and direction relay. Dedicated limits D7/D8 appear to PinMAME as public 71/72 and stop left/right travel; switch 53 is the target. Model the two sensed endpoints and unsensed transit rather than treating output state as position. The manual identifies assembly `511-6979-00` and a 40-degree mechanical reference.

## Ironhide mini-playfield

Output 12 controls entry to the mini-playfield. During the feature, the player uses the flipper buttons to command public outputs 63/64 (physical Q45/Q46), tilting the surface left or right. Four optos sense the ball at public addresses 62, 59, 56, and 57; none is a surface endpoint. The exit rejoins the right-ramp route. A recreation must separately model the controlled gate, tilting body, ball-on-body motion, four opto zones, and fall-through/exit geometry.

## Optimus Prime and orbit gates

The Optimus ramp matches the Pro: output 30 drives the motor relay, switch 43 is full up, and 44 full down. Down routes the ball into the curved/right-orbit lane; up creates the jump into Optimus. Switch 51 senses the target in the left leg. Because LE main output 12 belongs to Ironhide, the Optimus rocking solenoid moves to auxiliary public 62/physical Q44. The LE also has two controlled gates: output 4 for the additional left rollover-lane gate and output 5 for the right/top orbit gate.

## Lamps and other playfield inventory

The LE service chart uses lamps 17-59 and 61-80; 1-16 and 60 are unused. Many feature and insert lights are implemented on dedicated LED boards, so preserve address identity even if a digital recreation renders a modern light source. The Allspark eject is switch/output 3/22, auto launch is 23/2, pops are 30-32 with outputs 9-11, slings are 26/27 with outputs 13/14, and the spinner is 34. The machine has two flippers on outputs 15/16; output 12 is the Ironhide gate, never a flipper.

## Author construction checklist

- Build every common Pro ball path plus the second orbit gate, Megatron drop target/figure/cannon, Starscream rotating platform, and Ironhide controlled/tilting mini-playfield.
- Implement the auxiliary address translation exactly: public 59-64 are physical Q41-Q46, with 51-58 and 65-66 explicit unused compatibility positions.
- Preserve the four-ball Megatron stack, all motor endpoints, Starscream limits, Ironhide ball optos, and Optimus route change as causal state, not cosmetic animation.
- Keep the official manual files in the external organized cache; both official URLs currently resolve to byte-identical 134-page PDFs and are retained under their separate machine identities.

## Spatial retrofit blocker register

The normalized playfield placement gate remains fail-closed. The ordered local search found only `Transformers (Stern 2011) SG1bsoN Mod.vpx` in the primary tables folder and `Transformers (Stern 2011) v1 mod 1.vpx` in the archive; both identify JP's **Pro** recreation and embed `tf_180`, so neither can provide LE geometry. The archived `Transformers G1 Generation One (TBA 2018).vpx` is unrelated community content and is excluded. Browser escalation identified the [VPUniverse detail mod](https://vpuniverse.com/files/file/6355-transformers-stern-2011-detail-mod/) and [VPForums JP table](https://www.vpforums.org/index.php?app=downloads&showfile=13612) as Pro candidates only; no exact LE VPX or LE controller script was identified.

The manual, exact `tf_180h` runtime harness, and physical review establish LE inventory, wiring, multiplicity, and custom-mechanism causality, but they do not establish normalized VPX/player-view coordinates for every LE sensor, effect, lamp/GI/flasher emitter, or moving assembly. In particular, Starscream, Ironhide, the Megatron drop-target/cannon assembly, and the additional LE gate cannot be located from the Pro frame without violating the edition boundary. Keep `coverage.status` as `partial` and `coverage.missing` as `spatial_placement` until an exact LE source with an LE driver identity and visibly matching playfield is acquired and reconciled.

## Sources

- `manual.transformers-pro-le.2011`: official combined Stern manual, SHA-256 `9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8`; LE switches/coils/lamps on PDF pages 60/62-63/65 and custom assemblies on 36-39.
- `review.pinball-news.transformers.2011`: detailed physical operation of Starscream, Megatron, Optimus, Ironhide, and the edition-only gate.
- `runtime.transformers-limited-edition.boot-start`: exact `tf_180h` ROM harness, SHA-256 `b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM auxiliary serialization, display, and driver family.
