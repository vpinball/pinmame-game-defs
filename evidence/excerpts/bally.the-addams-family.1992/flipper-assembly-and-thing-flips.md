# The Addams Family — Flipper Assembly parts breakdown and "Thing Flips" rules text

Transcribed from `Bally_1992_The_Addams_Family_Operations_Manual_January_1992_includes_schematics_OCR_searchable.pdf`,
three printed pages that together settle whether both upper mini-flippers are genuine fitted
hardware and what each one does: the illustrated Flipper Assembly parts breakdown (printed page
~2-74), the "'Thing Flips' Automatic Calibration" rules section (printed page 6), and a ball-path
narrative reference (printed page ~2-14). Visual re-transcription from the rendered pages, not the
OCR text layer.

## Illustrated parts breakdown (printed page ~2-74, "Flipper Assembly Notes")

A full, detailed, item-numbered bill of materials for **`A-15205-R` "Flipper Assembly - Upper
Right"** (20 line items: base assembly, EOS switch `SW-1A-193`, flipper coil `FL-11630` "Flipper
Coil - Red", crank link assembly "Right", bumper plug, etc.) sits directly beside the equally
detailed **`A-15205-L-1` "Flipper Assembly - Upper Left"** breakdown. Both are itemized exactly like
the lower-flipper assemblies (`A-15205-L-4`, plain `A-15205-R`), not blank template pages.

## "'Thing Flips' Automatic Calibration" (printed page 6)

Describes the upper-left mini-flipper (public solenoid 35/36, switch 117/118) as "an exclusive
Williams/Bally pinball innovation" — an AI-calibrated automatic flip, not a normal player-controlled
flipper:

> the ball will be diverted to the upper left mini-flipper and the game ('Thing') will attempt to
> shoot the ball into the swamp... between 50-60% of the time.

The manual also names the feature's own calibration switches: "the opto (switch 57, above the upper
left mini-flipper), the 3 Swamp Targets (switches 45, 47, and 48), and the upper 'Swamp Lock' switch
(switch 71)."

## Ball-path narrative (printed page ~2-14)

Calls the same device "THING'S MINI-FLIPPER" outright.

## What this settles

The upper-right mini-flipper (public solenoid 33/34, switch 115/116) is never named in this rules
text at all — only the upper-left one is. Combined with `tafGameData.hw.flippers` setting both
`FLIP_SW(FLIP_U)` and `FLIP_SOL(FLIP_U)` (unlike Monster Bash, where only `FLIP_SOL(FLIP_L)` is set
despite `FLIP_SW(FLIP_L|FLIP_U)`), and the retained known-working VPX script wiring
`SolCallback(sURFlipper) = "SolURFlipper"` and `SolCallback(sULFlipper) = "SolULFlipper"` to two
independent, physically animated flipper objects (`Flipper1` "rightUPPERflipper_gi*" and `Flipper2`
"thingflipper_gi*", i.e. "The Thing"), all three independent sources agree: both upper mini-flippers
are real, fitted hardware, not a repurposed or unfitted position, but they serve different gameplay
roles. The upper-left one is the AI-calibrated automatic "Thing Flips" flipper described above; the
upper-right one is documented as ordinary Fliptronic flipper hardware with its own EOS/button pair
and coil, driven by the WPC core exactly like any other flipper output.
