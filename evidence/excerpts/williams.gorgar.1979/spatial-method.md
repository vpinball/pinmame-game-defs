# Gorgar retained geometry

The local VPX is drumndav/daveboy6's Gorgar v1.0 as identified by its embedded splash line. It loads S6.vbs and runs grgar_l1. The exact archive VPX and vpxtool extraction are retained. The script maps individual drop leaves and each all-down switch, the kicker and drain, the magnet trigger and callbacks 1–6, and the matrix lights.

Use VPX bounds 0, 0 to 952, 1974. Figure 4 in the instruction booklet supplies the player-view check for switch sides and target order. Wall centroids and active sling-edge midpoints locate the ball interaction. Outhole, saucer, magnet relay/magnet, bank reset, bumper and sling drives are projected to the effect location when the underlying component is absent from the VPX. In particular, the script's shooter-lane BallRelease is a virtual ball-stack exit, separated from the lower drain capture point.

The matrix `LightN` objects bound to inserts are image lights. The bumper callbacks use Light70, Light71 and Light69, respectively; those lights represent the effect on the caps. The pit callback acts on three bulbs in VPX, whereas the wiring identifies two physical 89 bulbs. Do not pick an arbitrary two.

The [RetroRitchie and Darth Vito release v2.0](https://vpuniverse.com/files/file/20315-gorgar-williams-1979/) is a separate retained VPX with the same bounds and L-1 ROM. Its embedded table version reads 1.6. Its standup handlers pulse 13, 22 and 24 from three walls missing in the older file. The `AllLamps` collection goes through `vpmMapLights`, which uses each member's `TimerInterval`. That maps 38/39/40 to l70/l71/l69 and adds L56. These are hidden VLM sources with no bulb mesh. Its pit callback drives GI_PIT and optionally the decorative eyes. The geometry audit keeps these light candidates distinct from hardware.

The VLM build groups physical-looking G.I. fixtures in BM_Parts. The world-space OBJ resolves 23 repeated bulb envelopes under the G.I. light sources, including the slings and lane guides. The audit records their mesh-derived centers and the offset from each render light. The pit light has no such match. The factory drawing confirms the G.I. circuit but does not enumerate its sockets.

IPDB's stripped playfield #45065 (Mark Johnson) and underside #43263 (Michael Nyberg) cross-check the hardware layout. The underside shows the flipper and drop-bank mechanisms, inserts and socket strips, with portions hidden by harness routing. The Pinside Gorgar gallery has further playfield views. No calibrated photo measurements are used in the canonical placements.
