# Star Trek Pro (Stern, 2013)

Coverage: **author-ready - physical inventory, public PinMAME bindings, lamp semantics, mechanisms, and edition differences validated**

## Identity and evidence precedence

This definition covers all non-`h` Star Trek drivers: `st_120`, `st_130`, `st_140`, `st_150`, `st_160`, `st_161`, `st_161c`, `st_162`, and `st_162c`. PinMAME declares them as clones of an `h` firmware root for software lineage, while this separate definition describes the physically different Pro playfield they run. The extracted working Pro table runs `st_161` and is ground truth for playfield controller causality, ball state, device behavior, and lamp-object bindings. The official Pro manual governs the physical inventory, service wiring, and diagnostic numbering. Pinned PinMAME and `sam.vbs` govern public address serialization and the native 128x32 four-bit DMD.

## Controller topology and edition boundary

The Pro uses main solenoid outputs 1-32, the ordinary lamp matrix at public addresses 1-80, aggregate GI 0, matrix switches 1-64, dedicated switches D1-D24, and eight board DIP switches. It does not have the Premium/LE 12-transistor auxiliary board, four RGB node boards, motorized Vengeance dive/latch, switch 53 crash opto, output 51/52 orbit gates, output 53 ship actuator, output 54 drain kickback, output 55 rotating VUK, or output 56 ship latch. Manual PDF pages 68-70 describe Premium/LE RGB lamps and page 117 explicitly identifies the auxiliary board as LE-only; neither is part of this Pro definition.

## Switch inventory and ball state

The four-ball trough occupies switches 18-21 from left to right and jam opto 22 is downstream. The proven table creates four balls on 18-21; output 1 ejects the ball at switch 21 and briefly drives switch 22. Shooter lane is 23 and output 2 is the auto launcher. Switches 33/34 are bottom/top center-lock optos. Ramp optos are warp entrance/exit 13/36, left entrance/exit 14/35, and right entrance/exit 37/38. Orbits are right 51 and left 52. Pops are left/right/bottom 30/31/32, center bank top/center/bottom 39/40/41, left bank top/bottom 42/43, and the six red targets are 45-50. Switch 53 is unused on Pro.

The dedicated controls use public PinMAME addresses rather than the manual's D labels: fire is 71/D7; lower-left button/EOS are 84/D9 and 83/D10; lower-right are 82/D11 and 81/D12; upper-right button is 86/D15. EOS contacts 83 and 81 are normally closed. Cabinet tilt/service inputs use PinMAME's negative and zero public values as recorded in the JSON.

## Lamp matrix

All 80 public lamp callbacks are explicit. Physical unused channels are 1, 2, 6, 31, 39, 47, 58, and 77-79. Lamps 25-30, 33-38, and 41-46 are the red, green, and blue channels for six physical emblems: left orbit, left ramp, right orbit, right ramp, left eject, and center lane. The JSON records each channel and the exact VPX playfield coordinates. The remaining inserts are named from the working table and playfield artwork, including the four TREK letters at 4/5/7/8, status ladder 17-24, six red-target inserts at 50/57/59/60/68/69, six Enterprise arrows, the banks, missions, locks, and awards. Address 80 is the right-side blue playfield spotlight represented by table objects `l80`/`f80`. Script-only visual aliases 119, 120, 129, and 131 are driven from solenoids and are not physical/public lamp addresses, so they are intentionally excluded.

## Center target, lock, and Vengeance

The single center memory target reports switch 11; output 4 raises it and output 5 lowers it. A direct hit drops it, shakes the passive Vengeance toy, and can release a held ball when it rises. Output 3 controls the center magnet; the proven table uses a radius-55 centered grab field and optos 33/34 track the lock path. The Pro Vengeance is a bash toy with output 7 as its super-speed ball return. When enabled, the table kicks at 175 degrees and force 40. Do not reproduce the Premium/LE motor, latch, crash sensor, or dive state machine on this edition.

## Ball devices and standard mechanisms

Left eject switch 10 remains active while occupied; output 6 ejects at 184 degrees, force 22, Z 55, with variation 2 in the proven table. Auto-launch output 2 uses direction 40 degrees, power 40, random variation 0.3, and a 0.6-second full-plunge time. The spinner pulses switch 12. Outputs 9-11 drive the three pops, 13/14 the slings, 15/16 the lower flippers, and 12 the upper-right flipper. Output 22 drives the unsensed laser projector. Outputs 17-21, 23, and 25-32 are named flashers; output 8 is the optional shaker and output 24 the optional coin meter.

The complete target inventory is three BEAM ME UP standups at 1/2/4, four TREK standups at 24/25/28/29, the right three-bank at 7-9, center three-bank at 39-41, left two-bank at 42/43, and six red standups at 45-50. The ramp/orbit sensor pairings and all corresponding insert/arrow addresses are encoded in the JSON mechanisms and outputs.

## Resolved upper-right flipper discrepancy

The legacy Pro table writes public switch 90 and visually couples the upper-right flipper to lower-right output 16. The service manual's dedicated-input table, coil chart, and PinMAME `sam.vbs` agree that the physical machine instead uses public switch 86/D15 and output 12. The author-ready definition therefore uses 86/12 and preserves the table discrepancy here as a portability warning. The rest of the table remains the proven behavioral source; this narrow exception is resolved by concordant physical and controller documentation rather than guessed.

## Recreation checklist

- Create four trough balls on switches 18-21, keep jam opto 22 clear until ejection, and bind shooter lane 23.
- Implement all main outputs 1-32, standard lamps 1-80, GI 0, the native 128x32 DMD, every matrix/dedicated input, and optional shaker/coin-meter hardware.
- Build the center memory target, center magnet and two lock optos, passive Vengeance bash/kickback, left eject, auto launcher, laser, three physical flippers, pops, slings, spinner, every target bank, and all ramp/orbit paths.
- Do not add Premium/LE auxiliary outputs, node-board lamps, switch 53, rotating VUK, controlled orbit gates, bottom-drain kickback, or motorized Vengeance hardware.
- Use the proven table's angle, force, timing, capture, and state-transition values as authoring baselines while using the manual for physical placement and wiring.
- Bind the upper-right flipper to physical public switch 86 and output 12; treat the table's 90/16 coupling only as a documented legacy-table simplification.

## Sources

- `manual.star-trek-pro`: official Stern `Star-Trek-Pro-Manual.pdf`, SHA-256 `23cb9e6683d7b357ada48678a8e157a8b64102ea012821c350a3f033fae66b28`; switch matrix on PDF pages 66-67, coil chart 114, GI/wiring 116, LE-only auxiliary declaration 117, and opto boards 151-154.
- `vpx.star-trek-pro-fss`: extracted working `Star Trek Pro (Stern 2013)-[D&N][FSS][DMD].vbs`, SHA-256 `abc5dbb6ead12f16886143a50cfd2534c9baf855b070924dd7d82e404b4d69bf`; runs `st_161` and supplies initialization, switch handlers, outputs, lamps, and mechanism behavior.
- `vpx-table.star-trek-pro-fss`: archived VPX, SHA-256 `2976e3313a6fa1ee6f26709d515661b81ade8f01894a847b907a5e608e5bb9e7`; containing archive SHA-256 `eaa577d4514b4945f6d98195a161c3de59d67c61f2b4d75e4c99169c9b6c1a34`; lamp objects and artwork were inspected read-only.
- `runtime.star-trek-pro.boot-start`: exact `st_161c` LibPinMAME run, SHA-256 `a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7`; ROM archive SHA-256 `f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0` remains external.
- `pinmame.core.4ec52ff0ac13`: pinned SAM driver, switch serialization, dedicated-input constants, and display implementation.
