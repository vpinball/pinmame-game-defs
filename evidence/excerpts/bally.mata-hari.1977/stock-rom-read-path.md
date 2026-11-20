# Factory Mata Hari ROM read and write paths

The authorized `matahari.zip` (SHA-256 `93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d`) contains the pinned U2 E-725-21 and U6 E-720-20 images. The listing uses PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450` and its `src/cpu/m6800/6800dasm.c` opcode table. The stock loader maps U2 at `$1000`, U6 at `$1800` and the U6 vector mirror at `$f800`. The walkthrough follows the CPU vectors and game dispatch tables, including the indexed destinations from `$129d`, `$1308`, `$13cc` and `$1401`–`$1466`. The ROM diagnostic's optional `$2000` callback points outside the loaded factory program. The listing and decoder are retained in `review-artifacts/bally.mata-hari.1977/online-followup/`.

Run `python -B trace-stock-code.py <authorized-matahari.zip> <pinned-source>/src/cpu/m6800/6800dasm.c` to replay the address and mnemonic listing. The decoder, listing and opcode table have SHA-256 `1ede08510521a2f619fa04e4fef13e5e04b839a282be6955cf9a0526b527503a`, `0f0f74e3eab34edd6b7ee974c0ebca6ec758bb7e9b1d7b653438cba31a30a2c7` and `c2bd5d12fa01b9543529471f83b3cfd966a956e50bdcf1cec80b1353de0557a2`, respectively. The REA archive inventory record `ev_667df849da5646deb68609270672d866c5f7d453efe6bf98e1f730cca6c5ebc6` is preserved in `matahari-stock.rea.json`.

## Stock DIP cache

U6 `$1a81`–`$1aa2` reads complete bytes through U10 PIA0-B (`$8a`). It selects the first three banks with PIA0-A masks `$20`, `$40`, `$80` and the final bank via PIA0 CB2. It caches the four bytes at `$4d`–`$50`, in bank order. The matrix scan beginning at `$1866` uses lower RAM through `$4c` and selects switch columns instead. PinMAME's `by35.c` uses the same bank selectors in `pia0b_r`.

| Stock bank and cache | Documented uses and consumption of the spare bits |
| --- | --- |
| S9–16, `$4e` | `$1ecc`–`$1ed1` shifts bit 0 into carry and masks bits 1–4 into the coin ratio. `$12d8` and `$1603` branch on the sign bit for S16. S14/S15 are bits 5/6 and do not feed these paths. |
| S17–24, `$4f` | `$1f4b`–`$1f4d` masks `$07` for credits, `$1f5e`–`$1f60` masks `$08` for credit display and `$1f8a`–`$1f8c` masks `$10` for Match. `$1768`–`$176b` shifts once then branches on original bit 6 for the saucer schedule, and `$12cd`–`$12cf` uses sign bit 7 for the A/B schedule. None select S22, bit 5. |
| S25–32, `$50` | `$14fa`–`$14fc` masks `$0f` for the centre chute ratio, `$14e8`–`$14ea` masks `$60` for the Special award dispatch, and `$1513`–`$1515` tests sign bit 7 for the score award. None select S29, bit 4. Quench V22 assigns it separately. |

Bally FO 579 gives no stock assignment for S14, S15, S22 or S29. The stock program samples those bits as part of the bank bytes and its option consumers exclude them. A control trace and a fresh run with all four bits changed match at every sampled gameplay checkpoint and have the same solenoid transition sequences after boot. A separate S16 control changes lower bumper lamp behavior.

See the [exact derivative read paths](derivative-dip-read-path.md) for the V22 S29 award selector, the revision-7 S14/S15 startup effect, and the limits of the S22 audit.

## Stock spare continuous outputs

At `$19eb`–`$19ee`, U6 calls the PIA register test with X=`$93`. The test steps the U11 PIA control registers and sweeps the associated direction and port data registers through the full 8-bit range (`$1a0b`–`$1a3f`). The PIA adapter sends changed direction and port output values to PinMAME's `pia1b_w`. That callback inverts the high nibble to publish PB4–PB7 as solenoids 17–20. The boot setup finishes by writing `$ff` to PIA1-B at `$1a73`. The normal coil writers at `$13df` and `$1d43` preserve the high nibble, with mask operations at `$1d5a` and `$1d5e` for PB5 and PB6 (lockout and K1). Both native stock runs show an initial assertion on all four outputs during power-up. Neither unfitted line 17 nor 20 occurs in the subsequent 17-step service coil sequence. Factory W-1187-1c and W-1192-1c identify the unfitted branches.

## Stock spare feature lamps

The lamp refresh loop at `$1847`–`$185e` scans the low-nibble decoder addresses using bytes from `$0200` onward. The active-low high nibble at `$0203` holds the four outputs of decoder slot 3: public 4, 20, 36 (B) and 52 (A). Attract code at `$17bd`–`$17c8` complements or clears the entire byte. Ball setup at `$1755`–`$1766` clears it after general lamp initialization (`$1b9a` returns with X=`$01ff`). The A/B logic at `$132c`–`$1344` updates the wired bits with `$c3` to reset both lanes. The low two positions in the emitted high nibble are physically unfitted on the A5/A6 harness. They follow whole-byte changes even though the individual A/B operations target bits 6 and 7. The separate stock lamps test also sweeps both spare addresses.

The [26-run native follow-up](native-followup.md#spare-outputs-across-all-six-drivers) documents the same lamp coupling and boot-only solenoid pulses across the six exact drivers in the tested scenarios.
