# Alien Poker multiball conversion (Williams / Oliver)

Coverage: **partial**. `alpok_b6` is a physical hardware conversion, separated from the six
production firmware variants. Its exact OPDB identity and manufacture date are unresolved.
PinMAME's catalog year 2006 dates firmware, not a second factory production game.

Oliver Kaegi's retained primary project page documents an added Firepower-style three-ball
trough and second ball-ramp coil, relocated right flipper assemblies and nearby lamp/bracket
hardware. Three trough contacts in series replace the playfield-tilt input 31, so the ROM sees
that input only when all three balls occupy the trough. The original outhole switch is replaced
with the donor assembly's switch. Knocker output 14 now drives the ball ramp. Credit lamp 56
is rewired to the right saucer arrow; the original credit bulb is removed. ROM capacity and the
CPU board addressing are modified. Production geometry cannot validate these relocated parts.

The modified rules light the upper lock after P-O-K, serve another ball once it locks, and then
use the right saucer for the second lock. A third ball starts multiball; a second-ball drain can
release the first lock. The author describes startup checking all three trough balls, altered
tilt/audit handling, leading-zero suppression and corrections across firmware revisions.
The exact retained version 320 needs its own ROM/installation checks; generic source init alone
does not validate every modification or the proposed alternative Gottlieb-style trough.

The immutable author-page capture, original/converted photographs and factual excerpt establish
the physical split. The new record deliberately does not inherit production positions or claim
the production OPDB ID. Conversion-specific full I/O, compatibility, mechanisms, display/rule
behavior and spatial verification remain open. This preserves one driver claimant without
misrepresenting a modified machine as production-compatible firmware.
