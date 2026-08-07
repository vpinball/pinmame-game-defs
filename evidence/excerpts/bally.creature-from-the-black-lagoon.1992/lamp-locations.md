# Creature from the Black Lagoon — Lamp Locations parts list

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 100, printed page 2-40,
"LAMP LOCATIONS". Read directly from a 300 dpi `pdftoppm` render (this manual's OCR text layer garbles
the table, e.g. printing "P�(A)+O" for "P-(A)-I-D").

| Item | Bulb No. | Lamp Assy. No. | Description |
| --- | --- | --- | --- |
| 11 | 24-8768 | A-15731 | (P)-A-I-D |
| 12 | 24-8768 | A-15731 | P-(A)-I-D |
| 13 | 24-8768 | A-15731 | P-A-(I)-D |
| 14 | 24-8768 | A-15731 | P-A-I-(D) |
| 15 | 24-8768 | A-15727 | Left Jet |
| 16 | 24-8768 | A-15727 | Right Jet |
| 17 | 24-8768 | A-15727 | Bottom Jet |
| 18 | 24-6549 | A-11754 | Admit One |
| 21 | 24-8768 | A-15734 | (K)-I-S-S |
| 22 | 24-8768 | A-15734 | K-(I)-S-S |
| 23 | 24-8768 | A-15734 | K-I-(S)-S |
| 24 | 24-8768 | A-15734 | K-I-S-(S) |
| 25 | 24-8768 | A-15734 | 10 Million |
| 26 | 24-8768 | A-15734 | 20 Million |
| 27 | 24-6549 | A-11271 | 30 Million |
| 28 | 24-6549 | A-11271 | Specials |
| 31 | 24-6549 | A-11754 | Start Mega Menu |
| 32 | 24-6549 | A-8882 | Playground Award |
| 33 | 24-6549 | A-11754 | Lite Big Millions |
| 34 | 24-6549 | A-8882 | Slide |
| 35 | 24-8768 | A-15728 | Right Search |
| 36 | 24-8768 | A-15728 | Right Video |
| 37 | 24-8768 | A-15728 (also A-11271) | Right Start Movie |
| 38 | 24-6549 | A-8882 | Mega Menu |
| 41 | 24-8768 | A-15730 | Lips |
| 42 | 24-8768 | A-15730 | Left Search |
| 43 | 24-8768 | A-15730 | Left Video |
| 44 | 24-8768 | A-15730 (also A-11271) | Left Start Movie |
| 45 | 24-8768 | A-15733 | Combo Award |
| 46 | 24-8768 | A-15733 | Parking O.K. |
| 47 | 24-8768 | A-15733 | Move Your Car |
| 48 | 24-8768 | A-15733 | Extra Ball |
| 51 | 24-6549 | A-11733 | Snack Bar |
| 52 | 24-6549 | A-11754 | Center Search |
| 53 | 24-6549 | A-11754 | Cola |
| 54 | 24-6549 | A-11754 | Hotdog |
| 55 | 24-8768 | A-14305 | Super Jackpot |
| 56 | 24-8768 | A-14305 | Jackpot |
| 57 | 24-8768 | A-14305 | Rescue |
| 58 | 24-8768 | A-14305 | Multiball Restart |
| 61 | 24-6549 | A-11754 | Free Pass |
| 62 | 24-6549 | A-11271 | Build Combo |
| 63 | 24-8768 | C-12709 | Unlimited Millions |
| 64 | 24-8768 | C-12709 | Creature Feature |
| 65 | 24-8768 | C-12709 | Extra Ball Countdown |
| 66 | 24-8768 | C-12709 | Big Millions |
| 67 | 24-8768 | C-12709 | Movie Madness |
| 68 | 24-8768 | C-12709 | Snack Attack |
| 71 | 24-8768 | --- | *C |
| 72 | 24-8768 | --- | *R |
| 73 | 24-8768 | --- | *E |
| 74 | 24-8768 | --- | *A |
| 75 | 24-8768 | --- | *T |
| 76 | 24-8768 | --- | *U |
| 77 | 24-8768 | --- | *R |
| 78 | 24-8768 | --- | *E |
| 81 | 24-8768 | A-15732 | (F)-I-L-M |
| 82 | 24-8768 | A-15732 | F-(I)-L-M |
| 83 | 24-8768 | A-15732 | F-I-(L)-M |
| 84 | 24-8768 | A-15732 | F-I-L-(M) |
| 85 | 24-6549 | A-11271 | Start Combo |
| 86 | 24-6549 | A-11754 | Popcorn |
| 87 | 24-6549 | A-11754 | Ice Cream |
| 88 | --- | 20-9663-1 | Start Button |

Footnote printed on the page: `*Located on backbox insert`. It is attached individually to items 71-78,
which spell C-R-E-A-T-U-R-E — the only lamp addresses this page marks as backbox rather than playfield
hardware. The retained VPX extraction independently confirms this split: `Light.L71`
through `Light.L78` sit at normalized x = -0.12 to -0.08, outside the table's own 0..1 playfield bounds,
while every other addressed lamp object sits inside them. No lamp address on this page is marked
"Not Used"; all 64 matrix positions (11-88) are populated, unlike the switch matrix.
