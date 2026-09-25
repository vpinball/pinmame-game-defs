# Transcription: Krellan Kingpin lamp matrix B

Source: `human-review.krellan.kingpin` -- Krellan's unofficial "Capcom Kingpin \"Manual\"" web page,
http://www.krellan.com/pinball/kingpin/ (retained copy SHA-256
`d1aee4120403c311cafaa0252aaecf02b2fc357f610741bdadca5a31b425230e`, fetched 2026-09-25). The author states
no printed factory manual exists and that the lamp positions were "personally verified ... using operator
mode on a real Kingpin machine". Cells are extracted verbatim from the retained HTML table; the
right-hand "Public address" column is this project's derivation, not part of the source.

Krellan's chart is read column-major: heading `N0` is matrix column N, row label `r` is row r, so cell (`N0`, `r`) is lamp `NrB`. Public PinMAME lamp = (N - 1) * 8 + r + 64.

| Lamp | Public address | Krellan text |
| --- | --- | --- |
| 11B | 65 | Left Orbit Powerup |
| 12B | 66 | West $ (left orbit) |
| 13B | 67 | Jackpot (into slot machine) |
| 14B | 68 | Super Jackpot |
| 15B | 69 | K (top rollover lanes) |
| 16B | 70 | I |
| 17B | 71 | D |
| 18B | 72 | Gun (by left side of slot machine) |
| 21B | 73 | Gun (by right side of slot machine) |
| 22B | 74 | Backglass Jackpot Jump 2X |
| 23B | 75 | 4X |
| 24B | 76 | 6X |
| 25B | 77 | 8X |
| 26B | 78 | 10X |
| 27B | 79 | 12X |
| 28B | 80 | 14X |
| 31B | 81 | Left Jet Bumper |
| 32B | 82 | Bottom Jet Bumper |
| 33B | 83 | Right Jet Bumper |
| 34B | 84 | (behind KING targets, under "Flow" in "Flower Shop") |
| 35B | 85 | Left Flipper Return (x2) |
| 36B | 86 | Right Flipper Return (x2) |
| 37B | 87 | Lamppost ("Flower Shop", red) |
| 38B | 88 | (at bottom of divider between right orbit and lane to right gun standup, yellow) |
| 41B | 89 | (behind right gun standup in slot machine) |
| 42B | 90 | (behind above and red) |
| 43B | 91 | Top Lane Divider (left of K rollover lane) |
| 44B | 92 | (behind above and red) |
| 45B | 93 | (right of slot machine structure, between it and left jet bumper) |
| 46B | 94 | (behind above and red) |
| 47B | 95 | Left Slingshot (x2) |
| 48B | 96 | Right Slingshot (x2) |
| 51B | 97 | Top Lane (between K and I rollover lanes, x2) |
| 52B | 98 | Top Lane (between I and D rollover lanes, x2) |
| 53B | 99 | (left of base of captive ball) |
| 54B | 100 | (behind above and red) |
| 55B | 101 | (end of captive ball lane) |
| 56B | 102 | (behind above and red) |
| 57B | 103 | (behind left orbit, far back corner of playfield) |
| 58B | 104 | (behind above and red) |
| 61B | 105 | (behind and near end of right drop targets) |
| 62B | 106 | (behind above and red) |
| 63B | 107 | (behind far end of right drop targets) |
| 64B | 108 | (behind above and red) |
| 65B | 109 | (in front of right orbit, between it and right drop targets) |
| 66B | 110 | (behind above and red) |
| 67B | 111 | (behind right orbit, far back corner of playfield) |
| 68B | 112 | (behind above and red) |
| 71B | 113 | (under tracks at right ramp entrance) |
| 72B | 114 | (behind above and red) |
| 73B | 115 | (behind lamp #38B, between right orbit and lane to right gun standup, red) |
| 74B | 116 | (back of playfield, vertical, behind artwork on left side) |
| 75B | 117 | Between Left & Right Ramps (x2) |
| 76B | 118 | (behind above and red, x2) |
| 77B | 119 | (murder victim, center of vertical artwork at back of playfield, red) |
| 78B | 120 | (right side of vertical artwork) |
| 81B | 121 | Left Spin City (over spinner) |
| 82B | 122 | Right Spin City (over spinner) |
| 83B | 123 | NU |
| 84B | 124 | NU |
| 85B | 125 | NU |
| 86B | 126 | Jackpot Jump (text on backglass, above gun, x2) |
| 87B | 127 | (behind right gun standup and at corner between that lane and right orbit, x2) |
| 88B | 128 | (behind above and red, x2) |
