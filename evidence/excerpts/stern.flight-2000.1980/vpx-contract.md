# bord Flight 2000 2.0, embedded script and geometry

The archive table identifies bord as author and reports update 2.0, August 2018. Its embedded script loads the Stern VPinMAME library and declares flight2k at line 731. The pinned script corpus file has different raw bytes. The exact embedded script controls the geometry crosswalk.

| Script lines | Contract observed in the script |
| --- | --- |
| 835–857 | 7 raises the left bank; 8, 11, 12, 13, 14 trip targets 5, 4, 3, 1, 2. 9 invokes the lock release; 10 serves the trough; 15 raises the right bank. 17 operates the right kickout and 20 the left. The two lower flippers use the standard Stern library callbacks. |
| 859–891 | Three virtual trough positions report 33, 34, 35; the stack starts with three balls and serves at BallRelease. The two impulse plungers have separate contact addresses 15 and 16. |
| 898–904 | Targets 28–32 form the left bank, 25–27 the right. |
| 1294–1312 | Drain adds the ball to the trough. Lock3 hit sets 39. SolBallLock clears 39, releases three stop walls and kicks all three virtual balls together. |
| 1326–1376 | Bank resets, pulses for two thumpers, level closures for rollover wires and separately pulsed stand-ups and spinners. The second stand-up handler is named sw17c, while the retained right-hand target is sw17a1. The real address-sharing comes from the factory switch chart. |
| 1388–1472 | Four distinct slingshot surfaces pulse addresses 12, 10, 11, 9. Their animation is local to each hit. |
| 1794–1857 | Active Lights(n) assignments position playfield insert effects. High Score, Game Over, Tilt and Match are commented or omitted from the playfield map. Both First Stage and both Second Stage lamp locations have their own effects in this recreation. |
| 1893–1914 | DIP editor exposes pricing-independent play, scoring and audio settings. |

The extracted game coordinate frame is (0,0)–(1122,2115) VP units. The playfield texture and factory artwork establish the labeled insert apertures. VPX insert lights render onto the playfield image. Their centers remain aperture candidates in the spatial report. Physical socket placement requires an independent view of the bulbs or fittings.
