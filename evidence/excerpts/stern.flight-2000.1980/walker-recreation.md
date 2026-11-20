# Ball walker construction and stock I/O

The factory manual identifies the B-758 launcher on PDF page 17, its contact at matrix 39 on page 18 and its J-26-1500 coil at Q13 on pages 16 and 20. The switch chart separately identifies 15, 16 and 40. Page 10 describes 40 as the release rollover for a qualified BLASTOFF and countdown. The p10 launcher number 29 disagrees with the detailed switch chart, circuit and exact VPX, which all use 39. PinMAME publishes Q13 at 9, the left kickout at 20, right kickout at 17 and outhole at 10.

## Physical assembly

Owner Mathazar's dismantled launcher photograph shows one retracting coil and plunger driving a common bar. Pivoted metal fingers alternate along that bar and a return spring biases the mechanism back to rest. The entry finger stands fully up with no ball and must return upright after the first ball stages. The photograph shows a J-28-2300 on this machine. The factory's J-26-1500 remains the reference part. The manufacturing changeover or repair history of the pictured coil is unverified.

In the separate entry-contact photos, the restored wireform clears the ball once it is parked against the first finger. The launcher therefore reports arrival on 39 without holding that switch closed while a ball remains locked. The clipped wireform is also described on three machines by Idleman in posts 105–107. A contact that remains down or misses the arrival edge makes the firmware lose track of staged balls. Mathazar documented another failure where the first finger caught behind a bowed bar and let an incoming ball overshoot the detent. The next coil stroke released the finger and sent the ball back down the entrance. Reorienting the bar restored twenty consecutive complete cycles on that unit. [Restoration, posts 105–107 and 141](https://pinside.com/pinball/forum/topic/1980-stern-flight-2000-restoration/page/3)

The retained IPDB maze views show two balls parked between fingers and the two subsequent kickout lanes. Build one linked assembly that meters balls through those positions into the first kickout, then route the ball through the second and out into the rear arch. The separate release rollover is in the top path. The two photographed trough mountings share one three-contact occupancy arrangement and one shooter feed. The photos and controller traces leave precise linkage travel and hidden contact or coil centers to measurement.

## Stock ROM observations

The stock gameplay run used the authorized production `flight2k` archive and pinned LibPinMAME with fresh state. All three occupied trough contacts were set for startup. There was no recovery sequence during its 18-second boot wait. Start triggered the bank resets at 7 and 15, serve at 10, and flipper enable at 19. The scenario then reduced trough occupancy and manually gave the ROM ball and target contacts. [Compact runtime evidence](../../runtime/stern/flight-2000-stock.json)

The fresh stock boot observation started with 33 and 34 closed and 35 open. The host then only waited, with no coin, Start or other switch input. After the power-on output check, the trace shows seven repetitions of right kickout 17, left kickout 20 and walker 9, starting at 8.73–36.89 s on the host clock. The last walker release was at 39.99 s. No further sequence was observed through the end of the 65-second wait. This records the behavior for the tested occupancy and time window. A general retry limit and the conditions for starting a game remain unverified. [Compact runtime evidence](../../runtime/stern/flight-2000-stock.json)

| Scenario input | Observed public command |
| --- | --- |
| First arrival at 39 | 9 turned on about 0.24 s later, for about 1.24 s. |
| Second arrival at 39 | 9 turned on about 0.22 s later, for about 1.24 s. |
| 39 held for four further seconds each time | The walker command ended while the contact was still closed. |
| 40 pulsed during each unqualified serve window | No new walker pulse in either step. |
| Third arrival after two captures and ordered countdown closures | 9 pulsed during the release window. |
| The host exercised the two stage contacts | 20 and 17 fired during that sequence. Some pulses overlap. |

These are host-clock timings from a synthetic switch sequence. The trace records controller decisions. Mechanical finger travel, phase durations and ball transit remain table tuning. The exact VPX collapses the walker into three kickers and releases their walls together on 9. The original bar, fingers, return spring and separate release contact are necessary for a physical-style reconstruction.
