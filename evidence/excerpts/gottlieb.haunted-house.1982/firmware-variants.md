# Haunted House: modification authors' documentation

Retained official Flipprojets pages by François & Thierry Davroux, captured 2026-11-06 under external `review-artifacts/haunted-house-1982/firmware-docs/`. Each source record pins its own capture digest and timestamp. These are paraphrased factual extracts; the captures remain outside Git.

## PROMs for Haunted House

Source: https://www.flipprojets.fr/PromHH_EN.php, article sections 669-3/669-4, A/B variants, improvements and installation.

669-3 is the replacement game PROM for the stock, non-speaking System 80 machine. 669-4 adds speech commands for a modified sound board. Installation replaces the 2KB game PROM; both share improvements. The authors distinguish the differently wired pre-production 669-S from production 669-1 and final 669-2.

Both updates restore the missing delay during the between-ball high-score display and repurpose CPU DIPs 31/32 for extra-ball/special difficulty. The authors report that factory DIP 32's documented background-tone function was not implemented. They also add a previously unrequested sound 9 to selected game events.

A variants correct brief unintended Extra Ball LED flashes. B variants include that correction and change only the secret-passage rule: without the arrow lit, the ball still physically enters the cellar but the ROM immediately returns it to the main playfield. This is not evidence of an added passage gate or new tunnel switch.

## Speaking Haunted House

Source: https://www.flipprojets.fr/HHparlant_EN.php, sound-card changes and uses.

The voice conversion fills the factory's vacant U14 with a Votrax SC-01 and replaces sound PROMs with a 28C64 plus an adapter and board configuration changes. The authors require their single-memory arrangement for supported operation. The new game PROM 669-4 enables the complete event speech; an unmodified game PROM permits only attract speech. This sound-board modification does not establish multiball hardware: a separately developed multiball conversion is described as a different external project.

Pinned PinMAME declares the rev 4 sound files NO_DUMP. That emulator limitation does not turn the stock production machine into a speech-equipped build, nor justify inventing a sound recording or successful rev 4 runtime test.

## Original author PDFs, visually checked regions

`HH669_34_EN.pdf` (June 2013), SHA-256 `24adb92a3f6e078c58e35a2a52b9e22395d35e13a6d3f8a26feb533c6af70e0c`, PDF 2 and 4 were visually checked against rendered pages. PDF 2's complete new-feature DIP region:

| CPU DIP | Function | OFF | ON |
| --- | --- | --- | --- |
| 31 | Extra-Ball difficulty | Conservative, normal/default: main-level contacts alternate the lit award | Liberal: award stays lit |
| 32 | Special difficulty | Conservative, normal/default: a qualifying sequence cannot be reused after its Special | Liberal: reset the qualifying sequence after its Special, permitting repeated awards |

The three Special sequences are attic bank three times, cellar bank twice, or main 1–5 in order. If the cellar Special was doubly qualified, both relevant sequences reset. PDF 4 explicitly permits A/B ROMs with ordinary bulbs as well as LEDs. B starts with Secret Passage arrow lit and roll-under arrow off; passing the passage exchanges them, and an enabled roll-under opens the trap door and restores the passage arrow. The ball still traverses the passive target when the arrow is off; the ROM suppresses cellar play and returns it.

`HHParlant_EN.pdf` (v2.1, September 2012), SHA-256 `c22f9c86cbc85f3543c3832f2b547454cd380eef6e9766ee1dd9e685dfb6cf36`, PDF 4 and 6 were visually checked. PDF 4 specifies MA-216 plus SC-01 and 8KB 2764/2864 decoding; the upper 4KB retains patched factory sounds and lower 4KB holds added voices/program. PDF 6's complete configuration region:

| Sound SB1 switch | Function on the speech conversion |
| --- | --- |
| 3, 4 | Attract interval, unchanged |
| 5 | Background sound ON/OFF, unchanged |
| 6 | Speech ON/OFF |
| 7 | Extended mode: replace Tilt/Slam sounds with voices |
| 1 | Multiball message-set ON/OFF |

The same page distinguishes normal 669-4 hardware from a separately converted Pascal Janin multiball machine requiring launcher, rewiring and added relays. This stock-machine record does not import those modifications. The older document permits two 2732 devices but does not recommend them; the authors' later 2023 webpage supports their single-memory arrangement only. The canonical compatibility notes retain the sound-board hardware distinction rather than treating all sound PROM choices as factory fitment.
