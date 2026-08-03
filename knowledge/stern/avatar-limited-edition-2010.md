# Avatar Limited Edition (Stern, 2010)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical I/O inventory, PinMAME bindings, wiring, custom mechanism causality, variant boundary, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `avr_101h` and `avr_120h`, the 250-unit Limited Edition/Premium physical machine identified as IPDB 5653, model I-00B6, released on 2010-12-02. The exact `avr_120h` ROM service tables and real-machine diagnostic dump establish LE-specific names. The exact known-working Pro VPX script is ground truth for shared controller behavior and mechanisms; no independently proven LE VPX table was found, so LE-only causality is additionally validated through exact-ROM service tests, owner/service documentation, and the physical edition record. The official manual controls common wiring and construction facts.

## Four-ball set and ceramic Na'vi detection

The LE still uses four balls, not five: three steel balls and one ceramic Na'vi ball. Trough switches are 18-21, jam opto 22, up-kicker output 1, and shooter switch 23 with manual plunger plus auto-launch output 2. Two exposed metal rails at the bottom of the shooter lane are dedicated D8/public switch 72. A steel ball bridges and closes them; the nonconductive ceramic ball leaves them open, which tells the ROM to begin Na'vi double scoring. Preserve per-ball material identity through every drain, trough shift, and serve so detector and magnet response remain correct.

## AMP three-bank, suit, magnet, and marching legs

The AMP bank moves targets 42-44 together between switch 46 up and 45 down under output 5. Exact diagnostics show output 5 asserted from 46 while moving toward 45; the proven table supplies the 25-step Z range and collision gating. The AMP suit uses motor 19 plus direction relay 13 between switch 58 up and 57 down. Starting at 58, the exact service test asserts 13 and 19 and reports movement toward 57. Magnet output 3 influences steel balls without centering them. LE adds unsensed right/left marching-leg actuators on outputs 4/12; alternate their pulses so the suit physically walks rather than treating them as lamps.

## Motorized transporter pod

The transporter is a separate LE playfield mechanism, not the Link lock animation. One motor is driven through reversing relay output 14. Switch 47 is down and switch 48 up. Exact `avr_120h` service tests prove both directions: from 48/up, output 14 deasserts while moving toward 47/down; from 47/down, it asserts while moving toward 48/up. Endpoint switches stop travel. Build the pod's moving collision/cover geometry with a single reversible motor path; do not invent a second motor output or an auxiliary-board channel.

## Link lock and shared playfield

Switch 14 reports the Link lock. Output 6 raises its pins and output 7 controls the latch; this ball-retention mechanism is separate from transporter output 14. One captive ball uses inverted/normally-closed switch 39. LE adds left ramp entrance switch 41 before common ramp exit 52. Spinners are 9/40, orbits 10/35, flippers outputs 15/16 with public button/EOS pairs 84/83 and 82/81, pops 9/30, 10/31, 11/32, and slings 17/26, 18/27.

## Lamps, flashers, and controller capacity

LE makes previously unused scoring inserts 20 and 44-46 physical and adds bottom-arch flashers on output 27. Manual PDF page 41 proves eight J13 lamp-column drives against ten J12 lamp returns; the JSON records both wires/pins for every matrix address. Output 8 is the factory-included shaker. Lamp 25 and 65-80 remain unused. Q20-23 and Q25-32 are flashers. The common scanned manual is Pro-only for Q4/Q12/Q14/Q27: its board schematic proves their Q/control pins but its coil chart leaves their power feeds blank, so the definition does not invent LE wire colours or voltages. PinMAME declares `SAM_GAME_AUXSOL12`, but exact diagnostics and physical evidence show no installed Avatar auxiliary controlled devices; public 51-66 are explicit unused emulator capacity. Synthetic game-on 33 has no coil, and legacy public queries 34-36 alias it rather than naming separate devices.

## Author construction checklist

- Build the typed four-ball trough, metal-rail shooter detector, manual/auto shooter, motorized AMP bank and suit, non-centering magnet, alternating marching legs, reversible transporter with both endpoints, Link lock/latch, captive ball, flippers, pops, slings, ramps/orbits, spinners, lanes, targets, shaker, and LE flashers/inserts.
- Initialize switches 18-21, 46, 48, and 58 active. Keep ceramic material identity, switch 39 polarity, EOS polarity, motor endpoint exclusion, and moving collision geometry accurate.
- Bind every matrix/dedicated/DIP input, Q1-Q32, game-on 33, explicit unused auxiliary 51-66, lamp 1-80, GI 0, and the DMD. Do not add a physical aux board or device merely because PinMAME reserves address capacity.
- Use the proven Pro script for shared runtime behavior, exact LE service diagnostics for added mechanism direction/endpoints, and the manual/IPDB records for physical construction boundaries.

## Sources

- `manual.avatar-pro-le.2010`: official Stern manual, SHA-256 `afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b`; organized under the external Avatar manual cache.
- `service.avatar-le.real-machine-dmd-1.2`: authenticated real-machine diagnostic archive SHA-256 `9ed7b04692e5891305ae17f6f1685a2a95901b26bf987328e4d6769eafffc85b`; decoded diagnostic stream SHA-256 `d5334e30dc52cd989aee65188e47f514c09e87384b635d2b442fdce57481b7cf`.
- `rom.avatar-le.avr-120h`: exact LE ROM archive SHA-256 `264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269`; ROM bytes remain external.
- `runtime.avatar-le.boot-start`: corrected callback-state evidence SHA-256 `6d00f26380ed4c71b7a921a38fe241bf3a675e472be884c742ee35ac4e8f99e8`.
- Transporter, suit, and three-bank exact service-test hashes are recorded in the definition sources and mechanism-diagnostic evidence file.
