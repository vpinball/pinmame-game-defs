# Observed rear general-illumination fixtures

Three original playfield holes between the L, A, S and T rollover lanes were measured in Mathazar's `IMG_9922.jpg`, taken at the end of top-side teardown. In the same restorer's `IMG_0453.jpeg`, the first rebuilt GI test lights three corresponding fixtures. Existing IPDB photograph 15827 independently corroborates the rear layout. The test photograph shows LEDs on the rebuilt playfield and establishes the positions used in that rebuild. The holes in the old playfield supply the coordinate source.

| Fixture | Original photo pixel | Normalized playfield position |
| --- | --- | --- |
| Between L and A | (1656, 679.5) | (0.594498, 0.112410) |
| Between A and S | (1668, 746) | (0.682381, 0.113178) |
| Between S and T | (1682, 818) | (0.772752, 0.113400) |

The full input is 2048 × 1536. Rotate 90 degrees counterclockwise using `(u, v) = (y, 2047 − x)`. Fit a planar homography from sixteen separately read insert centers to the matching exact VPX objects in the 1122 × 2115 coordinate frame. The normalized fit RMS is 0.001972 and the largest leave-one-out residual is 0.007467. All three hole centers are inside the control convex hull. The retained `followup-mechanism-primary/followup-spatial/spatial-candidates.json` contains all control and measurement pixels, the homography matrix, asset hashes and residuals. `measure.py` reproduces it.

Each hole was picked within about five pixels in the source photo. Perspective, lens distortion and the VPX artwork geometry limit accuracy. The factory circuit shows the 6 VAC feed. These observed positions give a subset of the lamp inventory, with total quantity and per-socket wiring still open. [Old playfield, post 79](https://pinside.com/pinball/forum/topic/1980-stern-flight-2000-restoration#post-8913723) · [Rebuilt GI test](https://pinside.com/pinball/forum/topic/1980-stern-flight-2000-restoration#post-8996017)
