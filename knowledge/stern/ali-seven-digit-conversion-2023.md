# Ali seven-digit conversion (Stern, 2023 software on the 1980 playfield)

Coverage: **partial — normalized spatial placements pending.**
Previously validated non-spatial scope: **complete physical inventory, controller bindings, wiring, mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers PinMAME `alib` revision 76 and `alic` revision 85. They are seven-digit free-play software conversions for the physical Stern Ali playfield (IPDB 43), not newly manufactured 2023 tables. Both PinMAME declarations use Stern MPU-200, the same switch-port definition, ST300 sound, and the seven-digit `dispst7` layout. The original six-digit `ali`/`alifp` drivers will receive their own definition because their score displays differ.

The known-working `Ali-v1.0.1.vbs` script is ground truth for controller-facing semantics and mechanism behavior. The Ali technical chart is authoritative for physical inventory, board connectors, wire colors, driver transistors, coil types, and diagnostic numbers. Pinned PinMAME source is authoritative for driver identity and public controller topology. The repeatable ROM harness used the available original `ali` image to validate the unchanged MPU-200 public-address translation; the conversion ROM archives were not present locally, so the harness is not used to infer conversion-only rules.

## Controller address translations

The 19 physical service solenoids do not line up numerically with PinMAME callbacks. The service sweep proves this physical-to-public sequence: `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18`. Public output 16 is an unaddressable decoder slot. Lower flippers are generic callbacks 46 right and 48 left, gated by public output 19.

The LDA-100 has sixty discrete SCR outputs, not a lamp matrix. The JSON maps each public address to its physical Q-number, connector, wire, and SCR type. Public 16, 32, 48, and 64 are unaddressable decoder slots and therefore are not devices. The ROM lamp test exercised every other address, including unused Q01, Q20, Q24, Q25, Q54, and Q58. The manual leaves Q15 unnamed, but the working script identifies its public address 29 as Ball in Play; script semantics win.

## Switches and shared contacts

The switch matrix is five strobes by eight returns, public addresses 1-40. Addresses 4, 10, 17, 18, and 40 are physically unused. Two separate middle rollover buttons share address 11 and must be wired in parallel. The technical chart calls address 9 a top-left rollover button, while the proven recreation pulses it from the spinner; build the spinner shown by the working table and bind it to 9. Service controls are -7 self-test, -6 CPU diagnostic, and -5 sound diagnostic. Cabinet flipper inputs are 82 right and 84 left; 81/83 are unused upper positions. All 32 MPU option switches are retained as configuration inputs.

## Ball lifecycle and saucers

Ali is a single-ball game with no trough stack. Initialize one ball in the outhole on switch 33. Public output 11/service solenoid 9 sends it toward the shooter lane at 115 degrees with nominal force 3; launching from the shooter lane is manual.

Top saucer switches 30, 31, and 32 share one physical eject output: public 7/service solenoid 4. The working table fires every occupied top cup toward 180 degrees at force 10 with force and angle variation 3, and resets its visual cup state after 200 ms. The middle-right cup holds on switch 38 and ejects through public 10/service solenoid 14 with the same vector and variation. The physical chart names switch 39 Middle Left Saucer, but the working table gives it no kicker or capture stack; model the known passive geometry and do not invent an output.

## Drop targets, bumpers, and slings

The top bank holds switches 19-21 while down and resets all three from public 8/service solenoid 8. The left bank holds switches 22-24 and resets from public 9/service solenoid 13. Stand-ups 25-29 spell GREAT and pulse individually.

The public callback mapping for direct playfield coils is intentionally non-obvious. Left slingshot switch 16 uses public output 1/service solenoid 2; right switch 15 uses public 2/service 1. Left thumper switch 13 uses public 3/service 5, middle switch 14 uses public 4/service 6, and right switch 12 uses public 5/service 7. Preserve the JSON public addresses in the controller integration and the service numbers only as physical aliases.

## Flippers, relays, and illumination

Output 19 drives the 48 V flipper-enabling relay. The two J-25-450/34-4500 assemblies are hard-wired dual-winding circuits: public 48 represents the left coil and public 46 the right, with local normally-closed EOS contacts transferring from power to hold windings. The manual preserves power, coil, and button wire colors and connectors in the JSON.

Public 14/service 11 is the physical general-illumination relay. The working VPX table turns GI on whenever a ball exists and off when none exists rather than subscribing to that callback. Build the relay-controlled GI circuit from the physical chart; treat the script's ball-count behavior as a compatibility fallback, not extra ROM I/O. Public 18/service 19 is the coin-lockout coil. Public 12, 13, 15, 17, and 20 are wired diagnostic positions with no installed device and remain explicitly unused.

## Displays and sound

The conversion uses four seven-digit player score displays, a two-digit credit display, and a two-digit ball/match display. PinMAME `dispst7` is the exact layout contract. The original Ali hardware used six-digit player displays, which is why original and conversion drivers must not be merged. Sound is Stern ST300; sound-command behavior belongs to PinMAME and does not add playfield devices.

## Recreation checklist

- Build every JSON input and output, including unused wired positions, both physical EOS contacts, shared switch 11, all sixty valid SCR lamp outputs, and the two seven-digit-conversion auxiliary displays.
- Initialize one ball at switch 33; initialize both drop banks raised and every saucer empty.
- Use PinMAME public bindings for runtime callbacks and retain physical service numbers/Q-numbers as diagnostic aliases.
- Reproduce shared top-saucer actuation, passive switch-39 geometry, manual shooter launch, hard-wired dual-winding flippers, GI relay, and coin lockout.
- Treat the working VPX force, angle, variance, and 200 ms visual reset values as validated authoring starting points; refine only geometry-dependent tuning without changing controller causality.

## Sources

- `manual.ali.tech-chart`: organized external `Stern_Ali_Tech_Chart.pdf`, SHA-256 `455ea85f99eff031ffcca75489ab4dfea0a587a864522fb2fa30a4bfd160d78b`; one-page switch, lamp, coil, flipper, board, and fuse chart.
- `vpx.ali.jp-salas.1.0.1`: pinned known-working script, SHA-256 `6dbde0131a367c643ae87fe511052d28d83ed0cb6b74b87ba731a900678f1849`.
- `vpx-table.ali.jp-salas.1.0.1`: locally available working VPX used only for embedded playfield art/object-position confirmation, SHA-256 `14137b288aee843e834f509b467dd288fcf0e3269afcbd397e2276d31c24533f`.
- `runtime.ali.service-lamp-test` and `runtime.ali.service-solenoid-test`: isolated harness captures from exact `ali.zip` SHA-256 `bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b`; ROM bytes and raw mutable NVRAM remain outside the repository.
- `pinmame.core.4ec52ff0ac13`: pinned driver declarations, MPU-200 implementation, public-address conversion, and display layouts.
