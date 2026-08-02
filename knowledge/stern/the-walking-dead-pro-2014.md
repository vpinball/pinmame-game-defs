# The Walking Dead Pro (Stern, 2014)

Coverage: **author-ready - complete Pro I/O, wiring, lighting, mechanisms, initial state, and controller bindings validated**

## Identity and evidence precedence

This definition covers all non-`h` `twd_*` drivers from `twd_105` through `twd_160c`. The colored `c` ROMs alter DMD presentation but do not alter physical I/O. IPDB record 6155 identifies the Pro model; record 6156 is the physically different Limited Edition and must not be used for this machine. The exact JP Salas Pro table runs `twd_160` and is ground truth for PinMAME addresses, callbacks, initial switch state, ball routing, and mechanism causality. The Stern Pro manual governs physical construction, service addresses, wiring, part numbers, and the distinction between installed and blank driver positions. The isolated `twd_156` run uses a firmware revision that is physically compatible with the same Pro playfield and validates the native 128x32 four-bit DMD, public GI address 0, lamp activity, and runtime availability without redistributing ROM content.

## Four-ball trough and launcher

Build a four-ball trough with positions 18, 19, 20, and exit position 21 plus entrance/jam opto 22. Initialize all four position switches active. The proven VPX stack orders the exit at 21, ejects with output 1 at angle 90 and force 4, and pulses 22 during release. A ball then rests at shooter-lane switch 23; output 2 fires the automatic plunger with power 50, duration 0.6, and randomness 1.5.

## Prison doors and magnet

The two doors move together through dual-winding outputs 3 and 4. In the exact Pro script, asserting power output 3 opens the doors and clears switch 4; de-asserting hold output 4 closes them and sets switch 4. This Pro polarity is the opposite of the behavior represented by the known-working Premium/LE table, so keep it edition-specific. Switch 46 is the ball-passage opto. Output 7 drives a radius-30 centered capture magnet; when it releases a ball within radius 15, apply a random full-circle direction with speed from 15 up to 20.

## Drop bank and bash toys

The left bank contains maintained drop switches 9, 10, and 11. Output 12 resets the complete bank. The Well Walker is a passive spring-return bash target in Pro: switch 2 is active at rest, clears on impact, and becomes active again when the target returns. Do not add the Premium/LE well magnet at output 6, because Pro output 6 is physically blank. The Prison Walker is a separate spring-return bash target whose hit pulses switch 3.

## Standard devices and ball routes

The three pops use switches 30-32 and outputs 9-11. The slings use switches 26/27 and outputs 13/14. Lower flippers use outputs 15/16, dedicated buttons 84/82, and normally-closed EOS contacts 83/81. Star rollovers are matrix switches 12 and 13; dedicated D6-D8 are unused. The remaining manual matrix entries identify both ramp entrances/exits, top lanes, returns, outlanes, center lane, prison standups, tower standup, right loop, and other ball routes directly in the machine JSON. The Pro has no right spinner, left-loop spinner, right drop target, crossbow, or Bicycle Girl mechanism present on Premium/LE.

## Lighting and physical output boundaries

Instantiate conventional lamps 1-80 and one GI channel at public address 0. The exact table consumes the matrix directly; it omits the table render object for lamp 2 and comments out 73-75, but the Pro manual proves those physical lamps exist. This is a rendering omission in that VPX recreation, not permission to remove cabinet hardware.

The installed coil/flasher devices are outputs 1-4, 7-16, 19, 21, 24-29, 31, and 32, with output 8 and 24 optional. Keep 5, 6, 17, 18, 20, 22, 23, and 30 explicitly unused. The JP table attaches decorative fish-tank flasher callbacks to public 17, 18, 22, and 23 even though the model-specific Pro manual leaves those physical driver positions blank; those virtual table decorations must not become physical coils or flashers in the canonical definition. The isolated ROM run likewise observes output 23 activity, demonstrating that activity alone does not prove installed hardware.

## Recreation checklist

- Build the four-ball trough, matrix shooter lane, paired prison doors, prison capture magnet, three-target drop bank, two spring-return bash figures, three pops, two slings, and two lower flippers with the proven initial states and causality above.
- Recreate all manual-listed switches, 80 lamps, GI 0, and installed coil/flasher positions; keep every manual blank explicit so unknown data cannot be confused with absent hardware.
- Preserve sustained and modulated behavior for the door hold winding, magnet, flashers, GI, and flippers instead of converting every output to a fixed pulse.
- Do not copy the Premium/LE crossbow, right drop target, Bicycle Girl ramp and target, ramp/well magnets, RGB GI channels, auxiliary output board, spinners, or edition-specific switch polarity.
- Use the script's numeric forces and timing as known-working authoring baselines, then align geometry to the manual drawings and real playfield without changing controller causality.

## Sources

- `manual.walking-dead-pro`: Stern `WD-PRO-MAN.pdf` cached from Internet Archive, SHA-256 `03bbf27093ad8b851ffe5b6284b1f14a4ccbce1ca0a68e79800db728bc92a5ae`; switch chart PDF page 12, coil chart page 15, lamp chart page 18, and wiring/assembly pages 39-43.
- `vpx.walking-dead-pro.jp-salas-v5.5.0`: exact JP Salas Pro script from `LegendsUnchained/vpx-standalone-alp4k` revision `bfc4e21042b59e7c6495604166e9219d52c6b813`, SHA-256 `18d92b612f8d4f0fe1c0f20131fbeb3588d8393502330ca321deb36c9fcbcac4`; initialization and mechanisms at lines 1-165 and 322-525, lamp handling at 661-770.
- `runtime.walking-dead-pro.boot-start`: isolated `twd_156.zip` run, raw SHA-256 `ffb741cfa5f1238d756035c4c113b77ad94fdd2a9e015c21a92af0813595bccb`; ROM archive SHA-256 `9f0fa7803236c566829037612c9d7732c153e5fa35681b7513324d3ae380a716` remains external.
- IPDB records 6155 and 6156: model identity cross-check performed against the live IPDB pages; 6155 is Pro and 6156 is Limited Edition.
