# Tales of the Arabian Nights — Lamp Matrix and Lamp Locations

Transcribed from `Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf`, PDF pages 118-119, printed
pages 2-36 (Lamp Matrix) and 2-37 (Lamp Locations). The retained PDF carries a genuine OCR text
layer, but the layout extraction badly garbles multi-column tables, so this was re-verified against
the 300 dpi rendered page images, which are the source of record. Address = `column * 10 + row`. No
shading on this page (lamps are never opto).

| Row \ Column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 Jewel 1 (Left) | 21 Jackpot | 31 Magic Carpet | 41 Smoke 6 | 51 Smoke 14 (Top) | 61 Make A Wish | 71 Action 2 | 81 Extra Ball |
| 2 | 12 Jewel 2 | 22 (G)enie | 32 Action 3 | 42 Smoke 7 | 52 Lamp-15 | 62 (B)azaar | 72 Left Lock | 82 Action 5 |
| 3 | 13 Jewel 3 | 23 G(E)nie | 33 Ramp Arrow Right | 43 Smoke 8 | 53 Lamp-30 | 63 B(A)zaar | 73 Harem Advance | 83 Right Lock |
| 4 | 14 Jewel 4 | 24 Ge(N)ie | 34 Ramp Arrow Left | 44 Smoke 9 | 54 Lamp-60 | 64 Ba(Z)aar | 74 Left Tiger Loop | 84 Right Tiger Loop |
| 5 | 15 Jewel 5 | 25 Gen(I)e | 35 Smoke 1 (Bottom) | 45 Smoke 10 | 55 Smoke 4 | 65 Baz(A)ar | 75 Action 1 | 85 Captive Ball Right |
| 6 | 16 Jewel 6 | 26 Geni(E) | 36 Smoke 2 | 46 Smoke 11 | 56 Smoke 5 | 66 Baza(A)r | 76 Wish 1 | 86 Action 4 |
| 7 | 17 Jewel 7 (Right) | 27 Multiball | 37 Smoke 3 | 47 Smoke 12 | 57 Shoot Star Right | 67 Bazaa(R) | 77 Wish 2 | 87 Captive Ball Left |
| 8 | 18 Shoot Again | 28 Outlane Special (2) | 38 Amulet | 48 Smoke 13 | 58 Shoot Star Left | 68 Center Lock | 78 Wish 3 | 88 Start Button |

Lamp locations parts list (2-37) confirms bulb type per address: `24-6549 = #44` for 18, 27, 28, 38,
58, 68 (partial), 86, 87; `24-8768 = #555` for all others. Lamp 28 (Outlane Special) prints `(2)`,
matching the retained table's two Light objects `l28`/`l28a`. No other address carries a printed
quantity marker.
