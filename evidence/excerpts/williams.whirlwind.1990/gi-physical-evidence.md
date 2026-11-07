# Whirlwind physical GI evidence

## Backbox: 35 sockets, 17 constant and 18 relay controlled

Harold Toler's GI OCD installation on his actual Whirlwind is published at
https://ledocd.com/install_sys11_gi_r2.html (2017), also Pinside user herg's
post 1 at https://pinside.com/pinball/forum/topic/gi-ocd-for-system-11-prototype-built-feedback-requested.
The retained official HTML, acquired by Stealth MCP on 2026-11-06T21:50:02Z,
has SHA-256 `9e2fc33553abb79326e468172120c5b3a88165f14a0aa8fe7e0636de8a2d2510`.
It describes three backbox portions: the top portion remains powered,
while the left and right portions pass through the backbox relay. It also
identifies three original relays total, two under the playfield and one
on the insert panel. This is an installation account on a physical
machine, rather than a socket-count assertion in a shopping list.

Before-modification original photograph:
https://o.pinside.com/f/66/be/f66beaefad8553aab06d7b9901cd4a07a7ac5359.jpg,
2048x1152, SHA-256
`de4b8f4ebe0409c304e9151185e69e903ed669fc939a122cfab9d5bfdf8d2d16`.
Retained at `external:pinmame-review-artifacts/whirlwind-20261106/parent-gi-ocd/original-photo-1.jpg`.
The repository curator inspected the original and bare-wire paths independently of the
annotated census. The following are approximate native pixel centers,
not normalized playfield coordinates:

| Physically traced portion | Socket centers (x,y), pixels |
| --- | --- |
| Upper, 17 | 496,106;586,86;681,85;795,64;910,64;1036,128;1124,67;1223,88;1316,94;1562,101;1454,188;1571,291;1373,297;1159,327;1100,250;874,251;816,323 |
| Lower left, 6 | 335,351;293,500;590,509;622,877;461,825;375,980 |
| Lower right, 12 | 977,470;1317,460;1486,559;1677,611;906,711;1134,682;1389,764;1633,743;1739,773;1699,862;1553,929;1410,1016 |

The photo proves the 17/6/12 physical socket partition. Operating membership
comes from the installer's description plus the factory Power Wiring
Diagram (PDF 106/printed 96), which assigns the insert-panel relay to
output 16. Thus 18 of these backbox sockets belong to 16, and 17 do not.
The photograph is a single physical example; the factory manual supplies
routing but does not enumerate individual backbox sockets.

## Six autonomous blinkers are within the controlled eighteen

The owner photograph in Pinside's
https://pinside.com/pinball/forum/topic/need-help-with-location-of-whirlwind-flashers-in-backbox,
post 3 by EEE, shows six large-globe bulbs. Post 4 identifies these as #455
bulbs. They blink autonomously when powered; they are not additional
CPU-addressed #906 flashers. The actual retained thread was read, including
the distinction between bulb type and the larger holes in the panel.

Original photo:
https://o.pinside.com/b/a7/20/ba72059ed81e316c2495754241ac842667cab0a7.jpg,
2560x1536, acquired 2026-11-06T22:47:27Z, SHA-256
`e7a264dac3bb7ea7b7a6c980c472a30cf53b85f547f0b1c1034ef96711311bf8`.
Retained at `external:pinmame-review-artifacts/whirlwind-20261106/parent-blinkers/owner-backbox.jpg`.
Both original photographs were visually checked by repository curator. The panel is
viewed from opposite sides: the notch, upper four-lamp diamond, side lamp
and lower lamps identify corresponding sockets. Nine ordinary lamp centers
were used as controls in a mirrored projective registration. The six large
globes were withheld. The following image-space matches are in inspection
copies resized to width 1200; multiply front coordinates by 2560/1200 and
back coordinates by 2048/1200 to recover approximate native reads.

| Large globe | Owner front (x,y) | Installer back (x,y) | Traced back string |
| --- | --- | --- | --- |
| 1 | 198,362 | 868,328 | Lower right, 12 |
| 2 | 327,288 | 770,270 | Lower right, 12 |
| 3 | 580,290 | 572,276 | Lower right, 12 |
| 4 | 842,308 | 345,296 | Lower left, 6 |
| 5 | 1024,298 | 173,294 | Lower left, 6 |
| 6 | 468,446 | 664,400 | Lower right, 12 |

The largest control error is 3.4 pixels and largest withheld match error
5.7 pixels at width 1200. This correspondence establishes socket identity,
not physical measurement precision. Exact controls, transform and source
hashes are retained in `parent-blinkers/front-to-back-registration.json`.
Directly following the installer photo's bare wires puts all six matched
sockets on the lower controlled strings: two on the six-socket string and
four on the twelve-socket string. The 35 sockets therefore comprise 17
ordinary constant-supply lamps and 18 controlled lamps, the latter including
12 ordinary lamps and six autonomous #455 blinkers in this stock type
allocation. The installer has replacement bulbs; their appearance alone
does not establish original type. No extra six sockets are added to 35.

## Playfield branches: feed identity is stronger than jumper insulation

The same installer shows a meter-checked white-yellow supply tap in
original photo 2 and a purple/white-purple-fed local branch in photo 3.
The original photo 3 is https://o.pinside.com/a/2e/f4/a2ef46a3409a0d8e4ab1d598e5a3ae1d4a542795.jpg.
The purple-fed sockets have yellow local jumpers. Therefore a yellow
insulated wire at a socket cannot by itself establish output 16 membership.
The installer had already added a plain white wire at the white-yellow
tap; that new conductor must not be mistaken for factory wiring.

The factory diagram routes VIO/WHT-VIO from 2J9-5/1 through 11 and
YEL/WHT-YEL from 2J9-6/7 through 16. The coin-door YEL/WHT-YEL branch at
2J10-10/9 bypasses these relays. The upper and lower model GI collections
are rendering choices and do not enumerate physical bulbs.

The separate reviewed `gi-playfield-inventory.md` now records the complete
playfield socket inventory, registration and branch membership from those
teardown and whole-underside photographs plus physical wiring/voltage
evidence. The older 21-bayonet owner shopping count remains a lead, not the
authority for that independently established physical inventory.
