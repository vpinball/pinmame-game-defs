# Ripley's Believe It or Not! general illumination wiring

Source: `Ripleys_Manual.pdf`, PDF page 120 (printed page 103), right-hand portion of the `General Illumination Circuit Detailed Wiring Diagram`.

The diagram shows the 520-5137-01 I/O power-driver relay and four separately fused 5.7 V AC GI circuits. J15-P6/P1 is fuse F24 for the back panel; J15-P7/P2 is F25 for the upper-right and middle-right playfield; J15-P8/P3 is F26 for the upper-left playfield, back panel, and coin door; and J15-P9/P4 is F27 for the upper-right, middle-left, and lower playfield. The physical strings are separate circuits even though PinMAME exposes their common relay state as GI 0.
