# Cactus Canyon — Solenoid/Flasher Locations

Transcribed from `Cactus_Canyon_Manual.pdf`, PDF page 94, printed page 2-36, the solenoid/flasher
locations parts list, together with the Flippers and Train Motor sub-blocks printed on the same page.
The retained PDF carries an OCR text layer, but it is garbled on this dense tabular page, so this is
confirmed against the rendered page, which is the source of record. The General Illumination block
printed on the same page is transcribed separately as `general-illumination.md`.

| Item | Assembly | Coil/Flasher part | Description |
| --- | --- | --- | --- |
| 01 | A-21022-1 | AE-23-800 | AUTOPLUNGER |
| 02 | A-22296-1 | AE-26-1500 | LEFT DROP TARGET |
| 03 | A-22296-2 | AE-26-1500 | LEFT CENTER DROP TARGET |
| 04 | A-22296-1 | AE-26-1500 | RIGHT CENTER DROP TARGET |
| 05 | A-22296-2 | AE-26-1500 | RIGHT DROP TARGET |
| 06 | A-22467 | AE-24-900 | MINE POPPER |
| 07 | ----- | ----- | NOT USED |
| 08 | A-22435 | AE-26-1500 | SALOON POPPER |
| 09 | A-19963 | AE-26-1500 | TROUGH EJECT |
| 10 | A-22207-2 | AE-26-1200 | LEFT SLINGSHOT |
| 11 | A-22206-2 | AE-26-1200 | RIGHT SLINGSHOT |
| 12 | A-22205-2 | AE-26-1200 | LEFT JET BUMPER |
| 13 | A-22205-2 | AE-26-1200 | RIGHT JET BUMPER |
| 14 | A-22465 | AE-26-1500 | LEFT GUNFIGHT POST |
| 15 | A-22465 | AE-26-1500 | RIGHT GUNFIGHT POST |
| 16 | A-22206-2 | AE-26-1200 | BOTTOM JET BUMPER |
| 17 | A-22404 | 14-8015 | MINE MOTOR |
| 18 | 04-12478-12 | 24-8802 | MINE FLASHER |
| 19 | 04-11221-12 | 24-8802 | FRONT LEFT FLASHER |
| 20 | 04-11221-12 | 24-8802 | FRONT RIGHT FLASHER |
| 21 | A-22482 | A-14406 | LEFT LOOP GATE |
| 22 | A-22482 | A-14406 | RIGHT LOOP GATE |
| 23 | ----- | ----- | NOT USED |
| 24 | A-17802 | 24-8802 | BEACON FLASHER - PLAYFIELD |
| 24 | ----- | 24-8802 | BEACON FLASHER - INSERT PANEL |
| 25 | ----- | 24-8802 | MIDDLE RIGHT FLASHER |
| 26 | ----- | 24-8802 | SALOON FLASHER - PLAYFIELD |
| 26 | ----- | 24-8802 | SALOON FLASHER - INSERT PANEL |
| 27 | ----- | 24-8802 | BACK RIGHT FLASHER - PLAYFIELD |
| 27 | ----- | 24-8802 | BACK RIGHT FLASHER - INSERT PANEL |
| 28 | ----- | 24-8802 | BACK LEFT FLASHER - PLAYFIELD |
| 28 | ----- | 24-8802 | BACK LEFT FLASHER - INSERT PANEL |

## Flippers

| Item | Assembly | Coil/Flasher part | Description |
| --- | --- | --- | --- |
| 29-30 | A-14876-R | FL-11630 | LOWER RIGHT FLIPPER |
| 31-32 | A-15849-L | FL-11630 | LOWER LEFT FLIPPER |
| 33 | A-22432 | AE-26-1500 | MOVE BART TOY |
| 34 | ----- | ----- | NOT USED |
| 35 | ----- | ----- | NOT USED |
| 36 | A-22432 | AE-26-1500 | BART TOY HAT |

## Train Motor

| Item | Assembly | Coil/Flasher part | Description |
| --- | --- | --- | --- |
| 37 | A-22271 | 14-8015 | TRAIN REVERSE |
| 38 | A-22271 | 14-8015 | TRAIN FORWARD |

## Solenoid public-address remapping (per `controllers/pinmame/wpc-95.json`)

The printed table numbers solenoids 1-38 directly, but only 1-28 are public WPC-95 addresses as
printed:

- Printed 29 (power)/30 (hold) = public 45/46 (Lower Right Flipper).
- Printed 31 (power)/32 (hold) = public 47/48 (Lower Left Flipper).
- Printed 33-36 are the Fliptronic upper-flipper circuit block, which happens to equal public 33-36
  directly (per the profile note); Cactus Canyon has no upper flippers, so this game repurposes 33
  (Move Bart Toy power) and 36 (Bart Toy Hat hold), leaving 34/35 genuinely unused.
- Printed 37/38 are WPC-95 LPDC outputs, public 37/38 directly, and PinMAME additionally mirrors them
  at public 41/42 (same physical H-bridge drive lines to the A-22271 train motor gates, not a second
  motor).
