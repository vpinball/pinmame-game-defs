# 1104-E identity and firmware installation evidence

IPDB #4501 identifies the Bally solid-state game and distinguishes
the September 26, 1977 project date from April 1978 manufacture.
Pinside's solid-state entry and IPSND agree on April 1978, and IPDB
#1557 and Pinside's EM entry identify the separate 1977
electromechanical machine. OPDB G417e-MDvXz identifies #4501 and
uses the September 1977 date.

- https://www.ipdb.org/machine.cgi?id=4501
- https://www.ipdb.org/machine.cgi?id=1557
- https://pinside.com/pinball/machine/mata-hari
- https://pinside.com/pinball/machine/mata-hari-bally
- https://www.ipsnd.net/View.aspx?id=4501
- https://opdb.org/machines/236

PinMAME 46e1a01a0f73dc5ce163d98db1ae435883ecc450,
`src/wpc/by35games.c:195–235` and `src/wpc/by35.h` ROM start
macros. SHA-1s are the pinned source's ROM-member identities.
The two Quench drivers use identical program files.

| Driver | Loader | U2 filename and SHA-1 | U6 filename and SHA-1 |
| --- | --- | --- | --- |
| matahari | BY17_ROMSTARTx88 | 725-21_2.716 2347342f1281c097ea39c79236d85b00a1dfc7b2 | 720-20_6.716 729e61a29691857112579efcdb96a35e8e5b1279 |
| mataharb | BY35_ROMSTARTx00 | mata2732.u2 7ccce6633fe16ec82ad387cd7e0913cf89be0cb1 | 72132fn.u6 66046454d3b56aac52fcb303fd7bb7ef33296982 |
| mataharc | BY17_ROMSTARTx88 | MataHari_U2.2716 a8e9b7366d79685a96b7552e6c76ba0efafc3124 | System-17_U6.2716 7997a8733a29d0f2f883e02f9b635799f8d679f5 |
| matahard / matahard7 | BY35_ROMSTARTx00 | mataharif_U2_V22.2732 1f1b3c3397040618da70c12072daee0ea9ce8dd2 | mataharif_U6_V22.2732 05b670c1571c2db2a865e1728d405b8f41db66a3 |
| matatest | BY35_ROMSTARTx00 | matat0n.u2 ced5fcd18009106ac3c7b42e36cdc10ce410eeeb | ptestn.u6 8defbe8e11a75d26daf1351f439dd409f1efc608 |

## Installation authorities

- Bally's service bulletin revised 8/12/78 documents separate
  service setups for an AS-2518-35 board and an AS-2518-17
  modified per F.O. 597. Both Mata Hari rows carry U2 E-725-21
  and U6 E-720-20, and refer to the Evel Knievel jumper cell in
  their respective tables. The tables describe the original
  ROM pair. Quench's replacement EPROMs have their own setup.
  See the [service-bulletin excerpt](mpu-service-bulletin.md).
- PinMAME commit 841c714dc1171e8c4bf959a5674e18c236949c9d describes
  the -17 to -35 addressing modification for Quench's ROMs. That
  addressing distinction leaves the driver generation at GEN_BY17.
  https://github.com/vpinball/pinmame/commit/841c714dc1171e8c4bf959a5674e18c236949c9d
- Oliver Kaegi's PCK-Bally page identifies Mata Hari revision 7,
  dated 010205, as a two-2732 set and names DIP 25/26 free play and
  a skill shot. The `mataharb` archive's `info.txt` is a generic
  Oliver patch readme. It lists `MATA2732.U2`, 2732 EPROMs and
  S17–19 on for that free-play patch. The readme's listed U6
  filename differs from the driver, so the CRC and member digest
  identify the actual set.
  https://pinball4you.ch/okaegi/pro_soft.html
- Quench's V22 file `MataHari_2732_Update_2025-04-13.txt`, in
  `matahard.zip` and `matahard7.zip`, instructs fitting two
  2532/2732 EPROMs and modifying the MPU for the selected chips
  where needed. It describes DIP 19 off for six-digit virtual
  millions and on for seven-digit player hardware. The separate
  millions strobe runs from MPU J1-7 to each Bally player display
  J1-12 or each Stern player display J1-11. The two fields on
  the credits/match assembly keep the same wiring. The public
  V22 readme matches both retained local text members.
  https://nvram.weebly.com/uploads/5/4/2/5/54255141/matahari.v22.2025.04.13.txt
- Quench's February 2019 Free Play+ `MataHari_Update.txt`
  identifies both active PinMAME ROM CRCs. The author settings,
  device compatibility and local native validation are in the
  [variant excerpt](firmware-variants.md).

| Authorized archive | SHA-256 |
| --- | --- |
| `matahari.zip` | `93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d` |
| `mataharb.zip` | `3f287eb0b89055537f8689a780d87fc9d34dd47cbfd9bc1faf1451725f1d52ad` |
| `mataharc.zip` | `066693d3a9a953d529bf1deddc3d7f6793eef92a063f2399d15d49b945a622d4` |
| `matahard.zip` and `matahard7.zip` | `94ab62eabd52ba20c17c6c932c509ccdf73da3466c6da95788fd4492bd7703ee` |
| `matatest.zip` | `f41dedbc954dd74be51c3652f429cd9a71de4dc6465e150bf2fe5c62733bf5c9` |

Read-only archive text SHA-256:
`info.txt` 0eaa1a58ec17117f420e1e0757daa068ff786ebcbab889ceff62598ee973ad0c.
Quench V22 text 1ad9d45bed92c1c0d526cfd87c0c8cb3f1957dc9b473772d3193c60873c2706e.
