# Retained VPX 0.9 controller bindings

Read from the embedded script for 32assassin's Star Trek 25th Anniversary (Data East 1991). The table declares `trek_201` on line 9. These bindings describe the recreation.

- Lines 29–62 dispatch outhole, trough eject, turbo launch, left reset, ramp up/down, right reset, knocker, flash circuits 9 and 12, GI relay 11, right VUK 14, kickback, moving target motor, and gate 22. Output 13's backglass transporter handler is commented out. Solenoids 25–32 go to local light indices 125–132, and 37–39 to local indices 137–139. Those indices only address the table's lights.
- Lines 184–203 implement outhole 10, trough positions 13/12/11, a three-ball trough, VUK 40, and two four-target banks on 20–23 and 44–47. The table coils move the ball stack. The public switches represent the resulting occupancy.
- Lines 233–255 send cabinet launch switch 30 on the keyboard action and give the impulse plunger its own shooter-lane switch 14 at `swPlunger`. The table's automatic plunger responds to output 3.
- Lines 204–214 model the backbox transporter with output 13, switch 31 at the visible endpoint (step 0) and switch 32 at the hidden endpoint (step 9). The positional steps and timing belong to the simulation.
- Lines 264–313 cover the lower-left hole and central moving-target-hole routing. The table transfers balls to the simulated VUK. It uses several animation kickers for the target opening.
- Lines 471–633 map the matrix lights, flasher proxies and decorative tube-light segments. Lamp 36 is driven as a local playfield-side proxy although the factory chart also names it Backbox #5. Matrix lamp 50 drives six rendering objects. The factory drawing names two bumper bulbs, 50A and 50B. The crystal bank 53–61 is rendered with Flasher objects. The script's type and object count alone establish no socket identity.
