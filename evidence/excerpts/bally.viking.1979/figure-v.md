# Viking Figure V geometry and symbol measurement

Factory manual PDF page 22, printed 18: circles are switch-identification numbers; squares are solenoid self-test numbers. The switch 33 circle marks the rebound behind the right bank. This is a coarse location symbol, not a measured contact.

Full retained render is 2550 x 3300 at source-native 300 dpi, SHA256 a30214afc6dffdeb0349c660ef08f25df00d45b940fe3bd955615c44c43e3055. Approximate printed frame corners (260,130),(1530,130),(1535,2650),(270,2650) are disclosed, not used as fabricated controls.

Independent primary manual reads, rounded to about 5 pixels with about 10 pixel reading uncertainty:

| Feature | Pixel x | Pixel y |
| --- | ---: | ---: |
| sw40 | 665 | 660 |
| sw39 | 985 | 660 |
| sw38 | 365 | 1620 |
| sw37 | 1290 | 1620 |
| LeftFlipper | 630 | 2250 |
| RightFlipper | 1030 | 2250 |

Switch 33 circle center: (1240,945). Fit independent x and y least-squares lines from these six source readings to the corresponding exact retained object centers. Result (0.781053,0.353894) is deliberately rounded to (0.78,0.35). Max normalized control residual is 0.019 horizontally and 0.012 vertically; estimated symbol/contact uncertainty is 0.02. Stored fit coefficients and exact control coordinates are in tools/seeds/bally/viking-1979-spatial.json. No value was obtained by mapping table coordinates backward onto the drawing. Placement stays observed.
