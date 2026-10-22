# Baywatch load-bearing drawing regions

Source: Sega Pinball, Inc., `Baywatch_Manual.pdf`, SHA-256 `9545ae03f7ef1bcc41f3e5e08b6be996d581f9141b1f70228fe9969ba9ace400`. Curator visually checked both the native-resolution pages and these derived regions. These are drawing excerpts, not substitute images of printed tables. The source record carries each crop's exact derivation and digest.

## Upper flipper control, PDF 109 / printed 105

The lower-left control region shows CPU Q26, CPU CN12-6, BRN/GRN entering two isolation diodes beside the flipper board. One branch joins upper left enable, the other upper right enable. Both parallel cabinet flipper switches are explicitly N.O. The 520-5080-00 board has enable inputs at CN1-10 and CN1-7. The drawing ties the upper EOS inputs to their enables; it does not show two physical upper EOS contacts. The complete flipper table separately prints both upper EOS cells `Not Used`.

## Auto Ball Launch, PDF 70 / printed 66

The upper assembly drawing is titled Auto Ball Launch Assembly `500-5969-00-33`. Its coil body is explicitly marked `23-800`; a microswitch is attached to the shooter bracket. This establishes which production assembly the mislabeled circuit 3L represents, together with the complete driver table and retained table callback. The adjacent printed parts table is not reproduced as a raster.

## Upper Ball Launch, PDF 70 / printed 66

The lower drawing is titled Upper Ball Launch (Kick Big) Assembly `500-5862-06-33`. Its separate plunger-and-frame construction has a coil explicitly marked `24-940`. It is distinct from the Auto Ball Launch above it. The drawing supports physical construction and part identity; the runtime binding comes from the complete electrical table and working script.

## Playfield flasher locations, PDF 43 / printed 39

The complete right-hand playfield drawing marks two 1R sockets along the rear panel, two 2R sockets, two 3R sockets, three 4R sockets, two 5R sockets, two 6R sockets, three 7R sockets and two 8R sockets. Those are separate physical socket symbols, not glow origins. The backbox drawing and complete circuit table supply the other sockets; this playfield region alone does not give a whole-machine total. There is no 1R socket drawn at the drop bank. Circuit 1R's schematic wording on PDF 45 disagrees, as retained in `coils.md`; the production drawing agrees with the exact VPX domes and physical photograph.

## Detailed flasher bulb composition, PDF 88 / printed 84

The eight boxed branches have four parallel sockets apiece. The complete literal branch annotations are transcribed in `coils.md`. Six boxes specify mixed #89/#906 populations; 2R and 7R specify four #89 bulbs each. This crop retains the shared feed and all eight return wires. It supports the existence of a physical bulb-type disagreement with the general chart; it does not settle which source describes the fitted production revision.

## Service contact construction, PDF 86 / printed 82

The cabinet wiring diagram draws STEP and FOR/REV as separate normally-open contacts sharing a common. STEP goes through coin-door connector pin 5 and the GRN line to CPU CN14-1; FOR/REV goes through pin 4 and BLU to CN14-2. Their common passes through pin 6 and WHT to CN14-3. A separate memory-lock contact is drawn from that common to CN14-4, BLK/RED; it is not another exposed service input. The old STEP/FOR-REV names describe the same black and green physical switches later renamed Begin Test/Enter and Service Credits/Select in Bulletin 74. This establishes electrical contact construction independently of whether the green button mechanically latches. After the bulletin's modification both buttons are momentary and rest open.
