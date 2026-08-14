# FunHouse — November 1990 operator handbook switch and G.I. evidence

Source: `Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf`, PDF pages 5 and 9-10, visually checked against 250 dpi full-page renders.

## General illumination

The handbook's Solenoid Table on PDF page 5 prints the following complete G.I. block:

| No. | Function | Wire | Connector | Transistor | Bulb |
| --- | --- | --- | --- | --- | --- |
| 01 | Upper Backglass | White-Brown | J120-7 | Q18 | #555 |
| 02 | Front Playfield | White-Violet | J119-1 | Q10 | #555 |
| 03 | Rear Playfield | White-Yellow | J121-9 | Q14 | #555 |
| 04 | Center Backglass / Right Rear Playfield | White-Orange | J120-8 | Q16 | #555 |
| 05 | Top Playfield | White-Green | J120-10 | Q12 | #555 |

PinMAME exposes those printed circuits as zero-based public addresses 0-4. All retained known-working FunHouse scripts agree on the modeled runtime playfield regions: address 1 controls Rudy, address 2 controls the upper/rear playfield, and address 4 controls the lower playfield; addresses 0 and 3 have no distinct playfield handler. The script remains runtime ground truth, while the printed names and wiring remain physical-construction ground truth. Printed circuit 04 proves a right-rear playfield branch exists, so public address 3 cannot be classified as cabinet-only. Because neither the scripts nor the retained table identify its individual emitters, that address is left spatially unresolved and is the record's sole remaining author-readiness blocker.

## Flipper inventory

The same PDF page prints the complete fitted flipper inventory:

| Function | Wire | Connector | Part |
| --- | --- | --- | --- |
| Lower Right | Blue-Yellow | J109-7 | FL-11630 |
| Lower Left | Gray-Yellow | J109-5 | FL-11630 |
| Upper Left | Gray-Yellow | J109-5 | FL-11753 |

There is no fitted upper-right flipper. This inventory resolves the generic four-position connector table in the operations manual: three positions are populated, and the upper-left row is real FunHouse hardware.

## Right trough switch 63

The Switch Matrix on PDF page 9 names address `63` `Right Trough`, and the Switch Locations drawing on PDF page 10 places callout 63 at the rightmost trough position. The retained script independently binds `Controller.Switch(63)` to the `ballrelease` kicker: `ballrelease_hit` asserts it, and `KickBallToLane` kicks the ball and clears it. The kicker center is therefore the validated spatial location for switch 63.
