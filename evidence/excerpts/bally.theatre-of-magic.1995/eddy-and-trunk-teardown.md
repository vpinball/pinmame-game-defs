# Theatre of Magic — Eddy Sensor Calibration and Magic Trunk teardown

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 45 (printed 1-45, Eddy Sensor Calibration) and
PDF page 50 (printed 1-50, Magic Trunk teardown, Fig. 1) — the board/assembly pages that fix the
physical construction of the eddy-current sensors and the rotating trunk/cube mechanism. The retained
PDF carries a Paper Capture OCR text layer, but per project policy every page was verified against a
300 dpi render regardless of the text layer's presence.

## Eddy Sensor Calibration (printed 1-45)

"Theatre of Magic uses Eddy Current Sensors to detect the pinball without the use of a mechanical
switch. One eddy device can be found in the front of the trunk. The other two are located in the
outlane areas." This directly confirms switch 85 (Trunk Hit) and switches 45/48 (Left/Right Drain
Eddy) are eddy-current proximity sensors (illustrated as "Auto Magna-Save Eddy (Hocus Pocus)" for
45/48), not opto or mechanical-leaf switches. `switch_type` is recorded as `other` with the
construction documented in `physical.notes`, matching the WPC-DCS-generation Star Trek: TNG
proximity-sensor precedent.

## Magic Trunk teardown (printed 1-50, Fig. 1)

"The Magic Trunk Assembly can be easily disassembled to replace parts if required. The upper box must
be removed first and lifted off." Labeled parts: Molded Trunk, Ball Trough, Motor Bracket, Hex
Spacers, Motor, Stop Collar, Opto Board, Cable, Opto Interrupter. This is the primary
photographic/diagram evidence that the four Cube Position switches (55-58) are opto interrupters
mounted on a dedicated "Opto Board" inside the rotating trunk mechanism, and that a single DC
gearmotor with a mechanical stop collar drives the rotation.
