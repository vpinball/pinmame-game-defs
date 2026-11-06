# Xenon ROM observations

Service test: third Self Test press after25-second stabilization cycles18 selectors. Digits below are raw player0 cells; comma bits masked, only the final two digits are decoded. Every retained nonblank selector agrees with the mapping. Host switch readback is not ROM evidence; timestamps are host time, not calibrated physical timings. play-run.json was exploratory with a held release switch; play2 corrected that sequence and is the causal evidence.

| Selector | Public | Coil time | Display time | Raw segments |
| --- | --- | --- | --- | --- |
| 01 | 7 | 29.397796 | 29.431557 | [0, 0, 0, 0, 0, 63, 6] |
| 02 | 6 | 30.365726 | 30.366033 | [0, 0, 0, 0, 0, 63, 91] |
| 03 | 8 | 31.301244 | 31.36754 | [0, 0, 0, 0, 0, 63, 79] |
| 04 | 9 | 32.269992 | 32.303484 | [0, 0, 0, 0, 0, 63, 102] |
| 05 | 14 | 33.238261 | 33.306078 | [0, 0, 0, 0, 0, 63, 109] |
| 06 | 15 | 34.207447 | 34.241408 | [0, 0, 0, 0, 0, 63, 125] |
| 07 | 10 | 35.175997 | 35.242258 | [0, 0, 0, 0, 0, 63, 7] |
| 08 | 11 | 36.144629 | 36.17784 | [0, 0, 0, 0, 0, 63, 127] |
| 09 | 12 | 37.114795 | 37.181535 | [0, 0, 0, 0, 0, 63, 111] |
| 10 | 13 | 38.083078 | 38.116495 | [0, 0, 0, 0, 0, 6, 63] |
| 11 | 1 | 39.051878 | 39.051981 | [0, 0, 0, 0, 0, 6, 6] |
| 12 | 2 | 39.988123 | 40.054299 | [0, 0, 0, 0, 0, 6, 91] |
| 13 | 3 | 40.956672 | 40.98989 | [0, 0, 0, 0, 0, 6, 79] |
| 14 | 4 | 41.926336 | 41.926512 | [0, 0, 0, 0, 0, 6, 102] |
| 15 | 5 | 42.895119 | 42.929126 | [0, 0, 0, 0, 0, 6, 109] |
| 16 | 18 | 43.865422 | 43.86561 | [0, 0, 0, 0, 0, 6, 125] |
| 17 | 19 | 44.801365 | 44.868092 | [0, 0, 0, 0, 0, 6, 7] |
| 18 | 17 | 45.80247 | 45.802588 | [0, 0, 0, 0, 0, 6, 127] |
| 01 | 7 | 46.738878 | 46.806153 | [0, 0, 0, 0, 0, 63, 6] |
| 02 | 6 | 47.708888 | 47.741725 | [0, 0, 0, 0, 0, 63, 91] |
| 03 | 8 | 48.676378 | 48.743825 | [0, 0, 0, 0, 0, 63, 79] |
| 04 | 9 | 49.645552 | 49.679169 | [0, 0, 0, 0, 0, 63, 102] |
| 05 | 14 | 50.615445 | 50.682104 | [0, 0, 0, 0, 0, 63, 109] |
| 06 | 15 | 51.583975 | 51.617275 | [0, 0, 0, 0, 0, 63, 125] |
| 07 | 10 | 52.553433 | 52.553579 | [0, 0, 0, 0, 0, 63, 7] |
| 08 | 11 | 53.521798 | 53.555322 | [0, 0, 0, 0, 0, 63, 127] |
| 09 | 12 | 54.457239 | 54.491279 | [0, 0, 0, 0, 0, 63, 111] |
| 10 | 13 | 55.426437 | 55.426553 | [0, 0, 0, 0, 0, 6, 63] |
| 11 | 1 | 56.395829 | 56.429029 | [0, 0, 0, 0, 0, 6, 6] |
| 12 | 2 | 57.364632 | 57.364822 | [0, 0, 0, 0, 0, 6, 91] |
| 13 | 3 | 58.332969 | 58.36725 | [0, 0, 0, 0, 0, 6, 79] |
| 14 | 4 | 59.302651 | 59.302771 | [0, 0, 0, 0, 0, 6, 102] |
| 15 | 5 | 60.237188 | 60.304514 | [0, 0, 0, 0, 0, 6, 109] |
| 16 | 18 | 61.241054 | 61.241229 | [0, 0, 0, 0, 0, 6, 125] |
| 17 | 19 | 62.174195 | 62.241352 | [0, 0, 0, 0, 0, 6, 7] |
| 18 | 17 | 63.144164 | 63.177504 | [0, 0, 0, 0, 0, 6, 127] |
| 01 | 7 | 64.112539 | 64.179832 | [0, 0, 0, 0, 0, 63, 6] |
| 02 | 6 | 65.081484 | 65.115228 | [0, 0, 0, 0, 0, 63, 91] |
| 03 | 8 | 66.04994 | 66.050062 | [0, 0, 0, 0, 0, 63, 79] |
| 04 | 9 | 67.020401 | 67.053704 | [0, 0, 0, 0, 0, 63, 102] |
| 05 | 14 | 67.988597 | 67.988719 | [0, 0, 0, 0, 0, 63, 109] |
| 06 | 15 | 68.956379 | 68.99014 | [0, 0, 0, 0, 0, 63, 125] |
| 07 | 10 | 69.925144 | 69.925265 | [0, 0, 0, 0, 0, 63, 7] |
| 08 | 11 | 70.860763 | 70.927268 | [0, 0, 0, 0, 0, 63, 127] |
| 09 | 12 | 71.829273 | 71.863207 | [0, 0, 0, 0, 0, 63, 111] |
| 10 | 13 | 72.7988 | 72.865423 | [0, 0, 0, 0, 0, 6, 63] |
| 11 | 1 | 73.768277 | 73.802709 | [0, 0, 0, 0, 0, 6, 6] |
| 12 | 2 | 74.737566 | 74.737751 | [0, 0, 0, 0, 0, 6, 91] |
| 13 | 3 | 75.673199 | 75.74007 | [0, 0, 0, 0, 0, 6, 79] |
| 14 | 4 | 76.641825 | 76.675625 | [0, 0, 0, 0, 0, 6, 102] |
| 15 | 5 | 77.611694 | 77.677981 | [0, 0, 0, 0, 0, 6, 109] |
| 16 | 18 | 78.580022 | 78.613917 | [0, 0, 0, 0, 0, 6, 125] |
| 17 | 19 | 79.549075 | 79.616599 | [0, 0, 0, 0, 0, 6, 7] |
| 18 | 17 | 80.518554 | 80.552207 | [0, 0, 0, 0, 0, 6, 127] |
| 01 | 7 | 81.487263 | 81.487381 | [0, 0, 0, 0, 0, 63, 6] |
| 02 | 6 | 82.455058 | 82.488449 | [0, 0, 0, 0, 0, 63, 91] |
| 03 | 8 | 83.424706 | 83.424889 | [0, 0, 0, 0, 0, 63, 79] |
| 04 | 9 | 84.392479 | 84.426161 | [0, 0, 0, 0, 0, 63, 102] |
| 05 | 14 | 85.32762 | 85.361521 | [0, 0, 0, 0, 0, 63, 109] |
| 06 | 15 | 86.297134 | 86.364629 | [0, 0, 0, 0, 0, 63, 125] |
| 07 | 10 | 87.264769 | 87.298615 | [0, 0, 0, 0, 0, 63, 7] |
| 08 | 11 | 88.233811 | 88.233974 | [0, 0, 0, 0, 0, 63, 127] |
| 09 | 12 | 89.201861 | 89.234872 | [0, 0, 0, 0, 0, 63, 111] |
| 10 | 13 | 90.137441 | 90.171128 | [0, 0, 0, 0, 0, 6, 63] |
| 11 | 1 | 91.106167 | 91.173427 | [0, 0, 0, 0, 0, 6, 6] |
| 12 | 2 | 92.075056 | 92.108993 | [0, 0, 0, 0, 0, 6, 91] |
| 13 | 3 | 93.044748 | 93.111077 | [0, 0, 0, 0, 0, 6, 79] |
| 14 | 4 | 94.01202 | 94.04636 | [0, 0, 0, 0, 0, 6, 102] |
| 15 | 5 | 94.981303 | 94.98149 | [0, 0, 0, 0, 0, 6, 109] |
| 16 | 18 | 95.950368 | 95.983287 | [0, 0, 0, 0, 0, 6, 125] |
| 17 | 19 | 96.9177 | 96.984885 | [0, 0, 0, 0, 0, 6, 7] |
| 18 | 17 | 97.8863 | 97.920138 | [0, 0, 0, 0, 0, 6, 127] |
| 01 | 7 | 98.822032 | 98.855365 | [0, 0, 0, 0, 0, 63, 6] |
| 02 | 6 | 99.79031 | 99.858587 | [0, 0, 0, 0, 0, 63, 91] |
| 03 | 8 | 100.759379 | 100.792952 | [0, 0, 0, 0, 0, 63, 79] |
| 04 | 9 | 101.72934 | 101.729533 | [0, 0, 0, 0, 0, 63, 102] |
| 05 | 14 | 102.698041 | 102.731816 | [0, 0, 0, 0, 0, 63, 109] |
| 06 | 15 | 103.667429 | 103.667553 | [0, 0, 0, 0, 0, 63, 125] |
| 07 | 10 | 104.636116 | 104.669849 | [0, 0, 0, 0, 0, 63, 7] |
| 08 | 11 | 105.571538 | 105.605123 | [0, 0, 0, 0, 0, 63, 127] |

Gameplay isolated switch-to-coil rises: {"17": [], "18": [], "19": [], "20": [2], "35": [15], "36": [14], "37": [13], "38": [12], "39": [11], "40": [10]}. Holding21-24 completes the bank and fires1;34 fires17;33 fires9;7 drops19. Physical labels/fitment come from the manual. Output20 rises briefly on reset while its A3J2-15 load is N/U.

Main public lamp1 remains physically N/U at both factory endpoints. Its raw public activity is:

| Retained run | Startup on-off (s) | Later activity |
| --- | --- | --- |
| selftest-run.json | 4.878353-4.941057 | Four additional pulses during the service sequence, from 25.054694 to 28.465893 |
| aux-run.json | 4.874833-4.946345 | None after stabilization |
| play2-run.json | 4.880320-4.941875 | None after stabilization |

Pinned by35.c:134-148 and 151-165 decode selected strobes into the temporary lamp matrix without checking physical fitment; lines387-390 publish that matrix. This generic publication explains why a public lamp address can pulse without a fitted load. The retained runs establish the startup/service observations, not the ROM-level cause of the startup transient, which remains unestablished. No fitted lamp or new circuit is inferred.

ROM archive and complete member hashes (the pinned by35games.c SHA1s were compared before boot):

| Member | Bytes | SHA1 | SHA256 |
| --- | --- | --- | --- |
| 720-40_6.732 | 4096 | 4e0b901645e509bcb59bf81a6ffc1612b4fb16ee | 84088af65823cf028ae667327dbe05266b0743b3e8c46c1a959c4bb22b0b4bc1 |
| 811-22_1.532 | 4096 | 86680e8cbb82e69c232313e5fdd7a0058b7eef13 | 71275c1211a3b10d95a0134a58f7cd11a51caa5481887718a2e82f000252dc91 |
| 811-23_2.532 | 4096 | 78fa3782ee9f32d14cf41a96a60f708087e97bb9 | 3bbc916a22d7032aa5d5bc2a7641a21b37347a5dc3c5e4d81dcff1eba2e04419 |
| 811-24_3.532 | 4096 | edb63b6d36524ae17ec40cfc02d5cf9985f0477f | abc8c070dfe202d22264749d500b3b5151357e338bdc1ded9c1991ca513abe8b |
| 811-25_4.532 | 4096 | a1f9a732fdb498a71caf61ec8cf3d105cf7e114e | b8f4272de45b417b6502ec219d9f6a686b6c9750ff40e0086819dcc8feba3ec4 |
| 811-26_5.532 | 4096 | e557b1bbbc68a6884edebe779df4529116031e00 | eb8d89512d50ad6f841d5b264998d89b9dfa785febea9d709aafb2a9a8341b3e |
| 811-27_6.532 | 4096 | 3f4d4a562e46c162b80660eec8d9af6efe165dd6 | 47f9aaaf0f1d32dc7cf549dc03f4bd5d12da8c18129bbd3601c7c0830a445830 |
| 811-28_7.532 | 4096 | 2678ffb5e8e2fcff07f029f14a9e0bf1fb95f7bc | 0a42f56dce2051080ba29a8769be53a09c5234d111b3e046c704f71c26073fea |
| 811-35_4.532 | 4096 | e2e09ac738c48342212bf38687299876b40cecbb | d5b07f0382c85f6784fb1c3c9bb52170e054cc16f18c4749d933067f05eb2a97 |
| 811-40_1.716 | 2048 | 52bc0ef65507f0f7422c319d0dc2059e12deab6d | ff10c9134a8573d4b7a22fd51145374a5b9c267f275dc6044af949d3769b2949 |
| 811-41_2.716 | 2048 | 98cd8cfed5c0f437d2b9423b31205f1e8b7436f9 | 1f6923c8a0441c05daa67fc95dacfad86379e9ab847e4a8a3cb4f66e87441624 |

Auxiliary output-7 observations (complete raw runs remain external):

| Run | First public72 rise (s) | Public72 event count | Events at each of88/104/120 | Post-stabilization snapshots with all four on |
| --- | --- | --- | --- | --- |
| selftest-run.json | 8.352897 | 7 | one rise each, no fall | 5/5 |
| aux-run.json | 8.352082 | 7 | one rise each, no fall | 22/22 |
| play2-run.json | 8.350408 | 7 | one rise each, no fall | 30/30 |

Public72 toggles during startup and ends high; 88/104/120 rise once and never fall in these retained event streams. All four are high before entry into Self Test and throughout the gameplay snapshots, so lamp-test sweeping alone cannot explain them. No upper-selector8-14 transitions or active snapshots occur in these three runs. W-1207-3 positively shows output7 N/U with no SCR; the generic publication path in pinned by35.c is not proof of a parked-decoder ROM cause or virtual meaning. Availability remains unknown with observed provenance; no physical lamp or spatial coordinate is inferred.
