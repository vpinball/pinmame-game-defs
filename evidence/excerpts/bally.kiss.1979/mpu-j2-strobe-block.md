# Kiss — corrected MPU J2 connector block

Transcribed from `Bally_1979_Kiss_Omissions_to_Schematic_Diagrams_user_submitted.pdf`, PDF page 2. The page compares the MPU J2 block “As Is” in schematic W1187-10 with the block “Should Be Added”. The corrected block adds wire number `93` beside J2 pin 2; the yellow highlight is why this excerpt is retained in color.

Both blocks show the following connector signals. “TO PLAY-FIELD SW STROBE” is one destination label spanning ST0 through ST4, not a separate destination fragment for each row.

| J2 pin | wire number in corrected block | signal |
| ---: | ---: | --- |
| 1 | 51 | ST0 |
| 2 | 93 | ST1 |
| 3 | 52 | ST2 |
| 4 | 53 | ST3 |
| 5 | 31 | ST4 |
| 6 | — | KEY |
| 7 | — | N/U |

The page footnote identifies ST1 as a gray wire with a yellow trace. This correction documents the J2 connector and its missing wire number only. It does not prove that the game lacks a separate ST5 connection elsewhere on the MPU or in the cabinet, and is retained as connector-correction context rather than as a device-address binding.
