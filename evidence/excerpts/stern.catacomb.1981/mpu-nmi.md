# Catacomb on-board S33 NMI circuit

Source: Stern Electronics Catacomb schematics, PDF7, MPU-200 drawing `340-602-S`, original SHA-256 `45fd3691ca719eab243553b98967aef4fb7cbe6c1ce7340e3342ecf0a1d24294`. Method: curator visual tracing of the native scan, corroborated against the same board's clearer circuit drawing; game-specific fitment and location come from Catacomb's own manual. Rights: NOASSERTION; Stern Electronics, Inc.; original retained locally.

The on-board S33 pushbutton is drawn open at rest between ground and the line to U9 6800 pin6, NMI. R13 (1.2K) pulls that line up to +5V. This is board-internal wiring, with no external harness pin asserted. Catacomb's own [assembly drawing](service-locations.md) places a MEMORY CLEAR button on the MPU. The [pinned emulator source](core-runtime.md) maps CPU Diagnostic, public -6, to the CPU NMI line.

The independent door MEMORY CLEAR contact uses A4J3-5 in the [cabinet drawing](door-service.md). It is retained as physical direct input 3 with no inferred public transport. The two paths are not merged merely because the assembly drawing calls both S33. No firmware clearing result is claimed.

The crop preserves U9 and the on-board button circuit. Image derivation is recorded verbatim in the source record and can be reproduced with `tools/render_excerpt_image.py`.
