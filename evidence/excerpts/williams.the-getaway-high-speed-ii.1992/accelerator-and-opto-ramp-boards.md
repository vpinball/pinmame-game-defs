# The Getaway: High Speed II — opto driver board assemblies (switches 81-85)

Transcribed from `Getaway_HSII_OPS.pdf`: PDF page 117, printed page 3-12, "A-15189 Accelerator Board
Assembly"; and PDF page 119, printed page 3-14, "A-13901-1 Opto Ramp Switch Board Assembly". Rendered
at 300 dpi with `pdftoppm` and read directly. These two board-assembly pages are the construction
evidence that switches 81-85 are opto interrupters (LED/phototransistor pairs), independently
confirming the paired parts already recorded on the Switch Locations page.

## A-15189 Accelerator Board Assembly (switches 81, 82, 83)

Connector pin functions transcribed exactly as printed:

- J1-1/2: Gray-Yellow (+12V) from Power Driver Board J118-2 (looped J1-1 to J1-2); J1-4: Black
  (Ground) from Power Driver J118-3.
- J2-2/3/4: White-Orange/White-Red/White-Brown (Switch Rows 3/2/1) from CPU Board J209-3/2/1; J2-6:
  Green-Gray (Switch Column 8) from CPU Board J206-1.
- J4: Not Used.
- J5-1/2: Red / Green-Brown to Switch #81 Opto LED / Transistor. J5-3/4: Black / White-Brown to
  Switch #81 Opto LED / Transistor. J5-5/7: Red / Green-Red to Switch #82 Opto LED / Transistor.
  J5-8/9: Black / White-Red to Switch #82 Opto LED / Transistor. J5-10/11: Red / Green-Orange to
  Switch #83 Opto LED / Transistor. J5-12/13: Black / White-Orange to Switch #83 Opto Transistor.
- J6-1/2/3: Violet-Green (Power) to Solenoid #25/#26/#28. J6-5/6/7: Brown/Red/Orange (Drive) to
  Solenoid #25/#26/#28.
- J7-1: Violet-Green (Power) from Power Driver Board J107-1. J7-3/4: Black (Ground) from Power Driver
  Board J131-1, 4 (both pins).
- J8-1: Blue-Brown (Enable) from Power Driver Board J122-1. J8-2: Blue-Yellow (Enable) from Power
  Driver Board J122-4. J8-4: Blue-Red (Enable) from Power Driver Board J112-4.

The same physical board carries the switch-row/column return wiring for switches 81-83 (J2) *and* the
power/drive wiring for solenoids 25/26/28 (J6) *and* the three Enable lines from solenoids 25/26/28
routed back through Power Driver connectors J122-1/4 and J112-4 (J8) — i.e. this one board is the
combined opto-sensor-plus-motor-driver electronics for the three motorized accelerator wheels.

## A-13901-1 Opto Ramp Switch Board Assembly (switches 84, 85)

- J1-1: Black (Ground) from Power Driver Board J116-3. J1-2: Gray-Yellow (+12V) from Power Driver
  Board J116-2. J1-5/6/7: White-Green/White-Yellow/Green-Gray (Switch Row 5 / Switch Row 4 / Switch
  Column 8) from CPU Board J209-5 / J209-4 / J206-9.
- J2-1/2: Black / Red to Switch #84 Opto LED. J2-3: Green-Yellow to Switch #84 Opto Transistor.
  J2-5: White-Yellow to Switch #84 Opto Transistor.
- J3-1/2: Black / Red to Switch #85 Opto LED. J3-3: Green to Switch #85 Opto Transistor. J3-5:
  White-Green to Switch #85 Opto Transistor.
- J4 through J7: Not Used.

This board carries only switches 84 and 85 — no solenoid/motor wiring at all, unlike the Accelerator
Board above. Neither this page nor the Accelerator Board page states which physical location (ramp
entrance versus loop-completion point) corresponds to J2 (switch 84) versus J3 (switch 85); that
identity comes only from the Switch Locations parts list (`switch-locations.md`, "84 Opto Made Loop",
"85 Enter Left Ramp") and disagrees with the retained known-working script's own runtime grouping and
sound design (see `conflict.switch-84-85-manual-vs-script-semantics` in the machine definition).
