# Kiss — Auxiliary Lamp Driver A9, connector J2 functions

Transcribed from the Bally Kiss lamp chart as reproduced on PinWiki
(<https://pinwiki.com/wiki/index.php/Bally_Kiss>), page text retained at
`review-artifacts/kiss-1979/pinwiki-bally-kiss.txt`.

**This is a secondary source.** The chart is not in the 57-page manual scan retained for this
machine. It is used only for the twelve printed pin functions; the board wiring beside them comes
from the AS-2518-43 schematic, which is primary. See the note below on why the transcription is
trusted.

| SCR | J2 pin | lamp | wire | colour |
| --- | --- | --- | --- | --- |
| Q06 | A9J2-7 | Back Box K1 & K2 | 58 | Wht-Blk |
| Q05 | A9J2-6 | Back Box K3 & K4 | 54 | Wht-Grn |
| Q04 | A9J2-5 | Back Box K5 & K6 | 56 | Wht-Blk |
| Q01 | A9J2-1 | Back Box I1 | 43 | Grn-Yel |
| Q02 | A9J2-2 | Back Box I2 | 45 | Grn-Wht |
| Q03 | A9J2-3 | Back Box I3 | 47 | Grn-Orn |
| Q12 | A9J2-18 | Back Box SA1 & SA2 (Left) | 25 | Blu-Wht |
| Q11 | A9J2-19 | Back Box SA3 (Left) | 27 | Blu-Orn |
| Q10 | A9J2-20 | Back Box SA4 (Left) | 21 | Blu-Red |
| Q07 | A9J2-11 | Back Box SB1 & SB2 (Right) | 15 | Red-Wht |
| Q08 | A9J2-12 | Back Box SB3 (Right) | 13 | Red-Yel |
| Q09 | A9J2-17 | Back Box SB4 (Right) | 12 | Red-Blu |

## Why a secondary transcription is trusted here

Three independent checks, none of which relies on the chart itself:

1. **Its SCR-to-pin column reproduces the primary AS-2518-43 schematic exactly on all twelve
   circuits** — `Q06→7`, `Q05→6`, `Q04→5`, `Q01→1`, `Q02→2`, `Q03→3`, `Q12→18`, `Q11→19`,
   `Q10→20`, `Q07→11`, `Q08→12`, `Q09→17`. A twelve-for-twelve match on a column the transcriber
   had no reason to fabricate authenticates the transcription.
2. **The runtime trace groups the circuits exactly as the chart implies.** A boot-and-play harness
   run drives them in four groups of three — `{65,66,67}`, `{81,82,83}`, `{97,98,99}`,
   `{113,114,115}` — one group per letter of K-I-S-S.
3. **IPDB describes the same effect independently**, listing among the machine's notable features
   "Backglass light animation (letters in K-I-S-S light up when scored, animate during Game Over)".

Note the contrast with Centaur, whose equivalent chart leaves `A9J2-11` blank. On Kiss that pin is
named, and the naming is consistent with everything else observed.
