# America's Most Haunted V22 (amh_022)

The two downloads that make up PinMAME's amh_022 set, retained under the working root's roms/spooky-pinball/ and assembled as the V23 set is: the card with the Intel HEX added to its root.

| File | URL | Bytes | SHA-256 | Server Last-Modified | Acquired |
|---|---|---|---|---|---|
| AMH_SD.zip | https://www.benheck.com/Downloads/amh/AMH_SD.zip | 595918968 | 0bad77fd8c692fed60fe056c97a3a2362a38bd449409e43c6d8eb9002dd24964 | 2025-02-23T17:38:32Z | 2026-10-05T20:43:08Z |
| AMH_V022.hex | https://www.benheck.com/Downloads/pinball_update_hex/AMH_V022.hex | 612459 | b9271c8ea1df39f195a2946efa5af24b41d95abb042c73a56970de005776b82d | 2025-02-23T17:45:43Z | 2026-10-05T20:42:43Z |

## The card's VERSION.TXT (88 bytes, SHA-256 bfd9e8904b7dc3089d7d13ed4b5abaa836939e0f6de271b8beeb7545b5b175a2, CRLF line ends)

```
GAME: America's Most Haunted

CODE REVISION: 22

A/V REVISION: 22

DATE: 10/3/2015
```

## Checked against PinMAME's set

`src/wpc/sims/pinheck/amh.c` at 97aa922bf8e4b6970126192ec1ac1fb0305a4f62 declares `PINHECK_HEX_ROMSTART(amh_022, "AMH_V022.hex", 612459, CRC(B74F2A7B) SHA1(4a36e71ba9fcfcd5779645e849babeed5a842c0b), "PROP_022.BIN", CRC(53A6B98B) SHA1(6427841d9f3ac6a744bf86856dfd3faf58e43828))`.

| Image | Bytes | CRC32 | SHA-1 |
|---|---|---|---|
| AMH_V022.hex | 612459 | b74f2a7b | 4a36e71ba9fcfcd5779645e849babeed5a842c0b |
| AMH_SD.zip: DMD/PROP_022.bin | 32768 | 53a6b98b | 6427841d9f3ac6a744bf86856dfd3faf58e43828 |
