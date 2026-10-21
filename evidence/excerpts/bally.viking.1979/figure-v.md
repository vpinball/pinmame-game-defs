# Viking Figure V geometry and symbol measurement

Factory manual PDF22, printed18: circles are switch-identification numbers; squares are solenoid self-test numbers. The switch33 circle marks the rebound behind the right bank. This is a coarse location symbol, not a measured contact.

Full retained render is2550x3300 at source-native300dpi, SHA256 a30214afc6dffdeb0349c660ef08f25df00d45b940fe3bd955615c44c43e3055. Approximate printed frame corners (260,130),(1530,130),(1535,2650),(270,2650) are disclosed, not used as fabricated controls.

Independent primary manual reads, rounded to about5pixels with about10pixel reading uncertainty:

| Feature | Pixel x | Pixel y |
| --- | ---: | ---: |
| sw40 | 665 | 660 |
| sw39 | 985 | 660 |
| sw38 | 365 | 1620 |
| sw37 | 1290 | 1620 |
| LeftFlipper | 630 | 2250 |
| RightFlipper | 1030 | 2250 |

Switch33 circle center:(1240,945). Fit independent x and y least-squares lines from these six source readings to the corresponding exact retained object centers. Result(0.781053,0.353894) is deliberately rounded to(0.78,0.35). Max normalized control residual is0.019 horizontally and0.012 vertically; estimated symbol/contact uncertainty is0.02. Stored fit coefficients and exact control coordinates are in tools/seeds/bally/viking-1979-spatial.json. No value was obtained by mapping table coordinates backward onto the drawing. Placement stays observed.
