# Factory mechanism and operation readings

Source: April 1991 operations manual SHA-256
`94d1bce9eaca3dd1b8df72d66050edba3310afdffd86a2a8927ceffb86b9820a`.
These are curator paraphrases of the complete cited drawing/operation regions,
visually checked against rendered pages, not a claim that OCR is authoritative.

PDF 7/printed A: one player presses any pitch button; in two-player mode the
pitcher selects fast, change-up, curve or screw. The batter uses BAT. Seven
targets score whichever result insert is lit. PDF 15/1-5 locates the DMD in
the upright speaker/display assembly, above the Bleachers Assembly; card
chute A-14796 mounts below the cabinet. PDF 16/1-6 specifies six balls and
approximately seven degrees of playfield pitch. PDF 14/1-4 gives service-button
normal and test functions; the control panel has separate one/two-player starts.

PDF 47/1-37 T.12: ramp test cycles the center ramp up and down; Enter chooses
Running/Repeat/Stopped, +/- select a sub-test and Escape exits. The ramp opto
normally has an unblocked beam. The display reports BLOCKED/UNBLOCKED, MOVING
while powered and ERROR on a fault. Ramp motor turns counter-clockwise viewed
from the left side and normally stops with the beam unblocked. The receiver
is about 0.1–0.7 V clear, 11–13 V blocked; transmitter about 1.4 V.
PDF 48/1-38 T.13: pitch test cycles the pitch unit with the same test controls;
PITCHING while powered, BLOCKED/UNBLOCKED feedback and ERROR on failure.
Pitch motor turns clockwise viewed from the left side. Its arm points toward
the front at the unblocked home state. The magnet is most effective on slow
pitches and does not significantly affect a fast ball. Same opto voltage ranges.

PDF 79/2-19 A-14356 pitcher exploded drawing: two curved ball-guide rails enclose
the pitch plate and drive. A shaft-mounted timing cam passes through the
separate opto mounting bracket. The drive assembly turns the pitch plate.
PDF 80/2-20 A-14290 ramp drawing: geared lift motor, mounting bracket, cam and
opto bracket/assembly; the cam both lifts the ramp and supplies optical timing.
These are single motors, not three independent pitch coils or a two-direction
ramp motor. PDF 81/2-21 A-14464 bat drawing shows solenoid/plunger, drive arm,
roller linkage to the bat shaft, adjustable stop/bumper and extension spring.
The spring provides mechanical return; bat button 26 is on the control panel,
not an EOS switch on this linkage. The solenoid table names bat A-14499 whereas
the exploded list calls the bat coil assembly A-14789; keep these source roles
separate rather than silently replacing either part identifier.

PDF 86/2-26 A-14150 target-board drawing: seven separate rotating target
assemblies A-14452-1 through -7, each with target switch A-14697 and switch
wire 12-6367; separate lamps and diodes illuminate results. A common rear
ball-guide wireform and ball deflector guide returns. The home-run bracket
A-14446 is a separate assembly at the rear. PDF 88/2-28 shows three distinct
opto paths in that bracket, one per left/middle/right return, with shaped
end/center ramps, A-14316 detector and A-14315 emitter. The lower drawing shows
one B-20-9608 magnet on pole/bracket assembly A-14696, associated A-14647.
PDF 90/2-30 A-14611 inside-light panel shows a separate A-14589 sixteen-lamp GI
board; do not count the VPX's backbox glow helpers as its bulb inventory.

PDF 56/1-46: balls must fall from the lowest trough into the pitcher; the trough
height is adjustable. Two spring-steel covers and a deflector constrain fast
pitches to the playfield; excess guide pressure prevents slow pitching.
PDF 58/1-48: cabinet trough must sit higher than the playfield trough with the
playfield clamped down so balls fall freely. These passive paths join the rear
return and strike return to the one pitcher; they do not create/destroy balls.

PDF 82–85/2-22–2-25 original A-14471 card dispenser: long magazine/trough above
base A-14473; gear motor A-14469, cable-and-pulley assembly A-14527, piston,
guide rod and extension spring form the feed mechanism. Opto
transmitter/detector and PCB A-14633 supply prize feedback; low-card switch and
operator unjammed pushbutton are independent. The card outlet/chute is below the cabinet,
not on the playfield. PDF 57–58/1-47–1-48: approximately 1,030 cards fit, about
30 remain when considered empty, around 1,000 are dispensable. Four slotted
motor-assembly screws adjust for card thickness so one card advances at a time.
Incorrect chute gap can let the next card retain the dispensed one; excess
humidity and reused or individually wrapped cards cause feed failures.
PDF 19–20/1-9–1-10 describes card, ticket and coin-op configurations; a ticket
dispenser is an operator conversion, not a second concurrently fitted mechanism.
It identifies 28 as a PCB pushbutton pressed after clearing jam/empty to resume
the remaining awards. The low lamp is normally off, on for low stock and blinks
for jam/empty. A.6.06 chooses stopping versus ignoring dispenser errors. A held
healthy-state 28 in the retained script is a table simplification, not hardware
feedback. Optional Deltronic DL-1275 conversion has no low switch/lamp unless
the operator separately adds them through the interface kit.

Timing windows, cam angular widths, motor speeds and delays in the retained
VPX script are recreation tuning unless independently measured on hardware.
