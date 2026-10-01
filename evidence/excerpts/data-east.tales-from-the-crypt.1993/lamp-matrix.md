# Tales from the Crypt (Data East 1993) - Lamp Matrix Chart and Lamp Matrix Locations and Descriptions

Transcribed by hand from native-resolution renders of printed pages 30 and 31 (PDF 34 and 35) of the GameEx-hosted scan `Data_East_1993_Tales_from_the_Crypt_Manual.pdf`. The scan has no text layer, so every cell was read from the render; OCR text was used only to locate the pages.

The printed text on page 30 says controlled lamps are an 8 x 8 matrix of columns (lamp drives) and rows (lamp returns). Both printed matrices are column-major: address = (column - 1) x 8 + row, the number printed in the lower right of each cell.

## Column drives (printed header row)

| Column | Drive transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q71 | YEL-BRN | CN7-1 |
| 2 | Q70 | YEL-RED | CN7-2 |
| 3 | Q69 | YEL-ORN | CN7-3 |
| 4 | Q68 | YEL-BLK | CN7-4 |
| 5 | Q67 | YEL-GRN | CN7-6 |
| 6 | Q66 | YEL-BLU | CN7-7 |
| 7 | Q65 | YEL-VIO | CN7-8 |
| 8 | Q64 | YEL-GRY | CN7-9 |

CN7 pin 5 is not used by any column; the printed header skips from CN7-4 to CN7-6.

## Row returns (printed header column)

| Row | Return transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q72 | RED-BRN | CN6-1 |
| 2 | Q73 | RED-BLK | CN6-2 |
| 3 | Q74 | RED-ORN | CN6-3 |
| 4 | Q75 | RED-YEL | CN6-5 |
| 5 | Q76 | RED-GRN | CN6-6 |
| 6 | Q77 | RED-BLU | CN6-7 |
| 7 | Q78 | RED-VIO | CN6-8 |
| 8 | Q79 | RED-GRY | CN6-9 |

CN6 pin 4 is not used by any row; the printed header skips from CN6-3 to CN6-5.

## Lamp Matrix Chart

Every one of the 64 positions carries a name; the chart prints no Not Used cell. Letters are printed as a single bold capital.

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Thunder Storm |
| 2 | 1 | 2 | Skull Crackin' |
| 3 | 1 | 3 | Door Prize Select |
| 4 | 1 | 4 | Frightmare |
| 5 | 1 | 5 | Psycho Pops |
| 6 | 1 | 6 | Robbing the Crypt |
| 7 | 1 | 7 | Extra Ball |
| 8 | 1 | 8 | Super Guillotine Targets |
| 9 | 2 | 1 | Werewolf Count-down |
| 10 | 2 | 2 | Video Mode |
| 11 | 2 | 3 | Electric Chair |
| 12 | 2 | 4 | Keeper Targets |
| 13 | 2 | 5 | Scoop |
| 14 | 2 | 6 | Buy-In Type |
| 15 | 2 | 7 | Launch |
| 16 | 2 | 8 | Start Button |
| 17 | 3 | 1 | Left/Right Outlane |
| 18 | 3 | 2 | Extra Ball |
| 19 | 3 | 3 | Skull Crush |
| 20 | 3 | 4 | K |
| 21 | 3 | 5 | E |
| 22 | 3 | 6 | E |
| 23 | 3 | 7 | Collect Creature Feature |
| 24 | 3 | 8 | Monster Jackpot |
| 25 | 4 | 1 | Multiball |
| 26 | 4 | 2 | Right/Left Return |
| 27 | 4 | 3 | Clone |
| 28 | 4 | 4 | R |
| 29 | 4 | 5 | E |
| 30 | 4 | 6 | P |
| 31 | 4 | 7 | Werewolf Count-down |
| 32 | 4 | 8 | Increase Jackpot |
| 33 | 5 | 1 | Lite Creature Feature |
| 34 | 5 | 2 | Fright-mare |
| 35 | 5 | 3 | Increase Double Jackpot |
| 36 | 5 | 4 | Lite Creature Feature |
| 37 | 5 | 5 | Rats |
| 38 | 5 | 6 | Goblins |
| 39 | 5 | 7 | Ghosts |
| 40 | 5 | 8 | Bats |
| 41 | 6 | 1 | Left Drop Trgt. |
| 42 | 6 | 2 | Middle Drop Trgt. |
| 43 | 6 | 3 | Right Drop Trgt. |
| 44 | 6 | 4 | T |
| 45 | 6 | 5 | P |
| 46 | 6 | 6 | Y |
| 47 | 6 | 7 | R |
| 48 | 6 | 8 | C |
| 49 | 7 | 1 | Mystery Door 1 |
| 50 | 7 | 2 | Mystery Door 2 |
| 51 | 7 | 3 | Mystery Door 3 |
| 52 | 7 | 4 | Double Jackpot |
| 53 | 7 | 5 | Living Dead |
| 54 | 7 | 6 | Grave-digger |
| 55 | 7 | 7 | Chainsaw Mode |
| 56 | 7 | 8 | Play the Organ |
| 57 | 8 | 1 | Left Turbo |
| 58 | 8 | 2 | Bottom Turbo |
| 59 | 8 | 3 | Right Turbo |
| 60 | 8 | 4 | Jackpot |
| 61 | 8 | 5 | Multiball |
| 62 | 8 | 6 | Left Ramp Enter |
| 63 | 8 | 7 | Right Ramp Enger |
| 64 | 8 | 8 | "Axe-tra" Ball |

Normalization: the printed cell breaks a name across lines and the transcription joins those lines with a single space; `Count-` / `down` is joined as `Count-down`, `Fright-` / `mare` as `Fright-mare`, `Grave-` / `digger` as `Grave-digger`. Address 63 is printed `Right Ramp Enger`, an evident misspelling of `Enter` that the location table below prints correctly; it is transcribed literally here. Address 28 prints `R` and 29 prints `E` and 30 prints `P`; the location table below prints the same letters.

## Lamp Matrix No. & Description (location table, printed page 31)

The table is printed in three panels. Two addresses carry two entries each, `17A`/`17B` and `26A`/`26B`; every other address carries one. A note under the table reads `General Illumination Lamps Not Shown` and `For Bulb Type & Part Number, see Page 39`.

| No. | Description |
| --- | --- |
| 01 | Thunderstorm |
| 02 | Skull Crackin' |
| 03 | Door Prize Select |
| 04 | Frightmare |
| 05 | Psycho Pops |
| 06 | Robbing the Crypt |
| 07 | Lite Extra Ball |
| 08 | Super GuillotineTargets |
| 09 | Werewolf Countdown |
| 10 | Video Mode |
| 11 | Electric Chair |
| 12 | Keeper Targets |
| 13 | Over Scoop |
| 14 | Buy-In Type |
| 15 | Launch |
| 16 | Start Button |
| 17A | Crypt Kick(Left Outlane) |
| 17B | Scared to Death(Rt.Outln.) |
| 18 | Extra Ball |
| 19 | Skull Crush |
| 20 | ....K |
| 21 | ....E |
| 22 | ....E |
| 23 | Collect CreatureFeature |
| 24 | Monster Jackpot |
| 25 | Multiball |
| 26A | Lite Mystery Door (Lt.Return) |
| 26B | Chop Pops (Right Return) |
| 27 | Clone |
| 28 | ....R |
| 29 | ....E |
| 30 | ....P |
| 31 | Werewolf Countdown |
| 32 | Increase Jackpot |
| 33 | Lite CreatureFeature |
| 34 | Frightmare |
| 35 | Increase Double Jackpot |
| 36 | Lite CreatureFeature |
| 37 | Rats |
| 38 | Goblins |
| 39 | Ghosts |
| 40 | Bats |
| 41 | Guillotine DropTarget Left |
| 42 | Guillotine Drop Target Mid |
| 43 | Guillotine Drop Target Right |
| 44 | ....T |
| 45 | ....P |
| 46 | ....Y |
| 47 | ....R |
| 48 | ....C |
| 49 | Mystery Door 1 |
| 50 | Mystery Door 2 |
| 51 | Mystery Door 3 |
| 52 | Double Jackpot |
| 53 | Living Dead |
| 54 | Gravedigger |
| 55 | Chainsaw Mode |
| 56 | Play the Organ |
| 57 | Left Turbo Bumper |
| 58 | Bottom Turbo Bumper |
| 59 | Right Turbo Bumper |
| 60 | Jackpot |
| 61 | Multiball |
| 62 | Left Ramp Enter |
| 63 | Right Ramp Enter |
| 64 | "Axe-tra" Ball |

Reading the letter groups: lamps 20, 21, 22 (K, E, E) lie on the left side of the lower playfield and 30, 29, 28 (P, E, R) on the right side, so taken in that order they spell K E E P E R; lamps 48, 47, 46, 45, 44 (C, R, Y, P, T) spell C R Y P T.

On the drawing, the callouts 14 and 16 sit below the playfield outline beside the `In Front` marker, and the callout 15 sits in the shooter lane beside the plunger; every other callout is inside the playfield outline.
