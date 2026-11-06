# Embryon service and flipper contacts

Bally Manufacturing schematics, retained from IPDB machine 783's `embryon_schematics.zip`
(SHA-256 `c92a259d772ae57e6e99e3b62135307c76e71f281536ce0e7daa8fa01aa67029`):

| Sheet and retained member (SHA-256) | Drawing observation |
| --- | --- |
| W-1186-12c, `switch1.tif` (`8395c33a4cd59785f39b546e5dca73b35a6049e2463062606980997a0e041496`) | TEST SW., A4J3-1 to TEST SW. RETURN / A3J2-7, is a normally open pushbutton. RIGHT FLIPPER SWITCH, A3J2-1 to A2J2-2, and LEFT FLIPPER SWITCH, A3J2-2 to A2J2-2, are open blade contacts. These are the cabinet buttons, not the flipper-enable relay contact. |
| W-1181-3c, `mpu.tif` (`edb79950e418341c862666e69eef28f8292bbd641a8eb8622fbaca9a485477f3`) | S33 ACTIVITY above U9 is an open contact between the pulled-up NMI node and ground. |
| W-1230-1, `sound.tif` (`d364f4e7c2483f200d96e484c4ce3fd20c9799ac760fa71bd542fc0dd77410d8`) | SW1 TEST SW beside U1 is an open contact between the pulled-up U1 NMI pin 6 and ground. |

The retained color manual (SHA-256 `55c800db586661821e84300aaf57fa24d825a492e78a94d41130b5916dcbe07b`) places the cabinet on PDF page 39, Squawk & Talk on page 45 and the MPU on page 46. The accompanying crops show the contact gaps, pull-ups and NMI endpoints. Page 46 labels the S33 pull-up R13; the separate `mpu.tif` labels it R14. Both draw the same normally-open S33-to-NMI construction.

The ARC manual's printed page 30 (PDF page 35, render `page-035.png`) names the sound module AS 2518-61A. That heading does not print 61B; the driver sound-type name below is separate emulator metadata.

PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450` maps the diagnostics in `src/wpc/by35.h:229-231` and `by35.c:475-484`: -7 self test, -6 CPU diagnostic and -5 sound diagnostic. `by35games.c:1207` selects `SNDBRD_BY61B`; `by35snd.c:464-465,591-593` routes its `by61Intf` diagnostic to sound-CPU NMI. The shared SW1-to-NMI construction is compatible with this mapping. `core.h:332` identifies the flipper column, its right/left button bits are `0x02`/`0x08`, and `core.c:2209` converts their rows to public 82/84. These source mappings identify the public inputs; the drawn contacts establish their physical construction independently of delivered levels.
