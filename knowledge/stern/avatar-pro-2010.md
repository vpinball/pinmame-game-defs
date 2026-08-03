# Avatar Pro (Stern, 2010)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical I/O inventory, PinMAME bindings, wiring, mechanism causality, variant boundary, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `avr_106`, `avr_110`, and `avr_200`, the Pro physical machine identified as IPDB 5618 and released on 2010-08-27. PinMAME roots these drivers under `avr_120h` for software lineage, but that does not add Limited Edition hardware. The exact known-working `avr_200` VPX script is ground truth for public addresses, contact polarity, initial state, ball routing, and shared mechanism causality. The official scanned manual governs Pro/common physical inventory and wiring, the exact ROM service tables govern localized labels, and pinned PinMAME governs SAM transport and display topology.

## Pro versus Limited Edition

The exact `avr_200` service table marks matrix switch 41 and transporter endpoints 47/48 unused. It leaves Q4, Q12, Q14, and Q27 as unnamed coil numbers; the physical Pro omits the marching AMP legs, transporter motor, and bottom-arch flashers installed on LE. Pro also omits physical inserts at lamp addresses 20 and 44-46 even though the localized ROM retains scoring labels. Shaker output 8 is optional on Pro. Do not project the ceramic Na'vi ball, metal detector D8/public 72, motorized transporter pod, marching legs, or LE bottom-arch window onto this machine.

## Ball path and shooter

The trough carries four steel balls on switches 18-21, with jam opto 22 and up-kicker output 1. Shooter switch 23 supports both the manual plunger and auto-launch output 2. Preserve real occupancy and ball identity through drains and ejections. Main travel sensors are left/right orbit 10/35, spinners 9/40, left ramp exit 52, top lanes 11-13, outlanes/returns 24/25/28/29, and left return-lane R input 1.

## Motorized AMP mechanisms

The AMP three-bank contains targets 42-44 and moves as one collision assembly. Switch 46 is fully raised and 45 fully lowered; output 5 changes the motor/relay state. The proven table travels from Z 25 to -24 in 25 steps and removes target collision below the playfield. The AMP suit uses motor output 19 and direction relay 13 with endpoints 57 down and 58 up. Output 3 is a non-centering magnet near the suit. Model moving collision geometry, endpoint transitions, and magnetic force rather than only animating artwork.

## Link lock, captive ball, and standard devices

Switch 14 reports Link lock occupancy. Output 6 raises the lock pins and output 7 controls the retaining latch; preserve the physical barriers even if the Jake/Link cover is animated with them. One captive ball pulses inverted/normally-closed switch 39. Flippers are outputs 15/16 with button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 17/26 and 18/27. Fixed targets are NAVI 2-5, right bank 7/8, center 17, AMP standups 36-38, and moving-bank faces 42-44.

## Lamps and controlled devices

Bind Q1-Q32, synthetic game-on 33, explicit unused SAM auxiliary compatibility addresses 51-66, lamp matrix 1-80, GI 0, and the 128x32 four-bit DMD. Manual PDF page 41 proves eight J13 lamp-column drives against ten J12 lamp returns; the JSON records both wires/pins for every address. Q20-23 and Q25-32 are flashers rather than insert lamps. Lamp 25 and 65-80 are unused on both editions; Pro additionally leaves 20 and 44-46 physically unused. Public solenoids 34-36 are a legacy `PinmameGetSolenoid` alias of game-on 33 and must not become physical outputs.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, AMP bank with moving collision targets and both endpoints, motorized suit with direction relay and endpoints, suit magnet, Link lock/latch, one captive ball, flippers, pops, slings, spinners, ramps/orbits, lanes, and fixed targets.
- Initialize switches 18-21, 46, and 58 active. Keep normally-closed captive switch 39 and flipper EOS switches 83/81 electrically correct.
- Bind all explicit JSON inputs and outputs, including unused channels, DIPs, service controls, GI, and DMD. Never turn synthetic or auxiliary compatibility addresses into playfield devices.
- Use the exact working VPX behavior as the runtime tie-breaker and the official manual for construction/wiring when recreating geometry and mechanisms.

## Sources

- `manual.avatar-pro-le.2010`: official 55-page Stern manual, SHA-256 `afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b`; relevant scanned pages are organized in the external manual cache.
- `vpx.avatar-pro-lw-vpumod-1.12`: exact known-working `avr_200` script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29`.
- `rom.avatar-pro.avr-200`: exact localized service tables from ROM archive SHA-256 `576f70929705761a78a0272a6fb72cd17656e0feb75cccb904a4080e7e5b9bd7`; ROM bytes remain external.
- `runtime.avatar-pro.boot-start`: corrected callback-state harness evidence SHA-256 `d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7`.
