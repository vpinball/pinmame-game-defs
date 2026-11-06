# Radical lamp-location measurements

Source: Bally / Midway Radical! Operator Handbook 16-2015-101, April 1990, PDF page 80, printed 2-26. Original PDF SHA256 a5085eb4c9088f3cba48949dba9f30a72c8aa3f30208d4f65150cc6e1f777cb6. Verified machine page https://www.ipdb.org/machine.cgi?id=1904; direct source https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf. Manufacturer copyright; no redistribution license established. Only a tight factual diagram crop is included.

Method: manual visual reading by primary curator, 2026-11-06, against the original 880x1856-pixel crop at native scan resolution. Pixel origin is the crop upper left. Source image hash: c8abeed55a3729c2768f077a60681fe540289be7668f3f12ba39a77e51818b02. Crop derivation: Bally_1990_Radical_Operator_Handbook.pdf page 80, crop box 0.48,0.13,0.86,0.69, scanned page rendered at its native resolution (embedded image xref 395, 2312px across 7.71in), rendered at 300 dpi, grayscale, 880x1856 WebP quality 10.

Visually read each numbered insert center from the retained drawing crop, not from the VPX insert lights. Coordinates are projections of the lamp onto its printed insert center; the drawing does not expose the socket below the playfield. Six independently read bumper-ring centers/flipper pivots reconcile the page with the exact table. tools/drawing_callouts.py least-squares affine fit; positions rounded to 0.001 to match drawing precision. All remain observed, including measurements outside the convex hull of controls. This is not a socket survey.

## Control measurements

| Physical landmark / retained object | Crop pixel x | Crop pixel y | Normalized x | Normalized y |
| --- | ---: | ---: | ---: | ---: |
| Bumper1 | 166 | 318 | 0.244834 | 0.166166 |
| Bumper2 | 309 | 264 | 0.447584 | 0.135781 |
| Bumper3 | 185 | 479 | 0.270026 | 0.259989 |
| Bumper4 | 334 | 423 | 0.480854 | 0.229214 |
| LeftFlipper | 239 | 1445 | 0.338454 | 0.84245 |
| RightFlipper | 490 | 1445 | 0.678851 | 0.84245 |

Affine coefficients (x = a*u + b*v + c, y = d*u + e*v + f), recomputed with tools/drawing_callouts.py fit():

`[[0.0013793162623121401,-1.1430470609091732e-05,0.022339659746724926],[6.542446274879965e-06,0.0005992375958445042,-0.026047979859246534]]`

Control leave-one-out errors: `[0.004730157173862583,0.004303883260131412,0.0043511597343009484,0.004066588331908415,0.013502683077285575,0.014407985334685755]`. The controls span 0.135781 to 0.84245 normalized y. All measured points remain observed; points outside the convex hull are extrapolated. The 0.07 callout limit is disclosed as a comparison convention and does not validate these insert projections.

## Whole numbered playfield lamp region

The region contains 1-56,63,64. Lamps 57-62 are named Insert lamps in the printed inventory and have no playfield symbol in this region; their backbox placement is sourced separately. Every visible numbered playfield insert is transcribed. The narrow number 36 is partly obscured by the drawn ramp; the source inventory and the numbered region identify it, and its center is approximate. Numbers denote illuminated inserts, not exposed sockets.

| Lamp | Crop pixel x | Crop pixel y | Projected x | Projected y |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 365 | 1473 | 0.509 | 0.859 |
| 2 | 302 | 1247 | 0.425 | 0.723 |
| 3 | 308 | 1218 | 0.433 | 0.706 |
| 4 | 333 | 1199 | 0.468 | 0.695 |
| 5 | 363 | 1188 | 0.509 | 0.688 |
| 6 | 394 | 1199 | 0.552 | 0.695 |
| 7 | 416 | 1218 | 0.582 | 0.707 |
| 8 | 423 | 1246 | 0.592 | 0.723 |
| 9 | 153 | 1046 | 0.221 | 0.602 |
| 10 | 235 | 1034 | 0.335 | 0.595 |
| 11 | 274 | 488 | 0.395 | 0.268 |
| 12 | 339 | 542 | 0.484 | 0.301 |
| 13 | 442 | 753 | 0.623 | 0.428 |
| 14 | 513 | 864 | 0.72 | 0.495 |
| 15 | 588 | 761 | 0.825 | 0.434 |
| 16 | 339 | 593 | 0.483 | 0.332 |
| 17 | 252 | 1291 | 0.355 | 0.749 |
| 18 | 289 | 1291 | 0.406 | 0.749 |
| 19 | 326 | 1291 | 0.457 | 0.75 |
| 20 | 363 | 1291 | 0.508 | 0.75 |
| 21 | 401 | 1291 | 0.561 | 0.75 |
| 22 | 438 | 1291 | 0.612 | 0.75 |
| 23 | 474 | 1291 | 0.661 | 0.751 |
| 24 | 363 | 1245 | 0.509 | 0.722 |
| 25 | 110 | 828 | 0.165 | 0.471 |
| 26 | 99 | 866 | 0.149 | 0.494 |
| 27 | 97 | 905 | 0.146 | 0.517 |
| 28 | 101 | 944 | 0.151 | 0.54 |
| 29 | 115 | 980 | 0.17 | 0.562 |
| 30 | 468 | 418 | 0.663 | 0.227 |
| 31 | 431 | 385 | 0.612 | 0.207 |
| 32 | 397 | 356 | 0.566 | 0.19 |
| 33 | 198 | 1124 | 0.283 | 0.649 |
| 34 | 425 | 845 | 0.599 | 0.483 |
| 35 | 446 | 505 | 0.632 | 0.279 |
| 36 | 441 | 241 | 0.628 | 0.121 |
| 37 | 29 | 1218 | 0.048 | 0.704 |
| 38 | 114 | 1302 | 0.165 | 0.755 |
| 39 | 597 | 1321 | 0.831 | 0.769 |
| 40 | 640 | 1354 | 0.89 | 0.79 |
| 41 | 30 | 1304 | 0.049 | 0.756 |
| 42 | 196 | 1038 | 0.281 | 0.597 |
| 43 | 257 | 1015 | 0.365 | 0.584 |
| 44 | 315 | 884 | 0.447 | 0.506 |
| 45 | 310 | 924 | 0.439 | 0.53 |
| 46 | 310 | 780 | 0.441 | 0.443 |
| 47 | 242 | 263 | 0.353 | 0.133 |
| 48 | 482 | 914 | 0.677 | 0.525 |
| 49 | 294 | 1342 | 0.413 | 0.78 |
| 50 | 342 | 1342 | 0.479 | 0.78 |
| 51 | 387 | 1342 | 0.541 | 0.781 |
| 52 | 433 | 1342 | 0.604 | 0.781 |
| 53 | 326 | 1391 | 0.456 | 0.81 |
| 54 | 402 | 1391 | 0.561 | 0.81 |
| 55 | 341 | 1425 | 0.476 | 0.83 |
| 56 | 388 | 1425 | 0.541 | 0.83 |
| 63 | 458 | 792 | 0.645 | 0.452 |
| 64 | 517 | 808 | 0.726 | 0.462 |
