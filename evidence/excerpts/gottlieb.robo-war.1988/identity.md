---
source: https://www.ipdb.org/machine.cgi?id=1975
source_sha256: a6ec7c26fac05f4680c58bfeed59f6f3ad63e5fb88eac5dc241bdb854e8638a8 (retained page-text capture, review-artifacts/gottlieb.robo-war.1988/session-20261113/ipdb-page/ipdb-1975-page-capture.json)
locator: IPDB machine page 1975, header and specification block; photo resources https://www.ipdb.org/images/1975/<name>.jpg
method: Page text captured through an interactive browser session on 2026-11-13; fields copied literally
transcribed_by: curator transcription
reviewed: true
---

# Robo-War identity

## IPDB 1975 specification block (literal)

    Robo-War / IPD No. 1975 / April, 1988 / 4 Players
    Manufacturer:	Premier Technology (1984-1996) [Trade Name: Gottlieb]
    Date Of Manufacture:	April, 1988
    Model Number:	714
    MPU:	Gottlieb System 80B
    Type:	Solid State Electronic (SS)
    Production:	2,130 units   (confirmed)
    Theme:	Outer Space
    Notable Features:	Flippers (2), Pop bumpers (3), Multiball (2), Spinning target (1), Ramp (1), 4-bank drop targets (1), 3-bank drop targets (1), 2-bank drop targets (1), Single drop target (1), Kick-out hole (1). Hand-drawn translite.
    Design by:	John Trudeau, Jon Norris
    Art by:	Constantino Mitchell, Jeanine Mitchell
    Software by:	John Buras

The title, maker, date and model number agree with the manual's own identity: the title block of every
wiring sheet reads `GAME #714`, the parts pages name Premier Technology, and the switch-matrix drawing
E-25886 is dated APR-2-88. The PinMAME root driver `robowars` is titled "Robo-War", 1988, Gottlieb,
with the comment `Robo-War (#714)`. OPDB group GryK3-MQrWk is the record's existing OPDB identity.

## Variants

- `robowars`: the production game ROMs (prom1.cpu CRC cd1587d8, prom2.cpu CRC 893177ed).
- `robowrfp`: Flipprojets free-play PROM1 (prom1_fp.cpu) on the same prom2 and sound ROMs.
- `robowarf`: French game ROMs (prom1f/prom2f, `// #714X`) on the same sound ROMs.
- `robowffp`: Flipprojets free-play build of the French PROM1.

All four share INITGAME(..., GEN_GTS80B, FLIP616, dispAlpha, SNDBRD_GTS80B, GTS80_DISPALPHA, 0) and the
gl_mGTS80BS2 machine, so they run on the same CPU, driver, display and sound hardware. The source notes
that a German version also exists; PinMAME has no driver for it. Only robowars.zip is in the authorized
ROM library, so the three clones are not runtime-tested.

## Photos retained (IPDB 1975, acquired 2026-11-13)

| File | SHA-256 | Resource |
| --- | --- | --- |
| ipdb-1975-1975f1.jpg | bdea08f2a3c00c382dd50f5e9552ec0b0d34437976c0f18f46e16f903871a6fb | https://www.ipdb.org/images/1975/1975f1.jpg |
| ipdb-1975-1975f2.jpg | 280f723c19b945a3748adb9306a9587543588e5d224298df66e53fc4c29d2524 | https://www.ipdb.org/images/1975/1975f2.jpg |
| ipdb-1975-image-1.jpg | 89959f7b59e82516bc84d3cb354ec44bc1d8c463bf2eef205ff2069512f1e18b | https://www.ipdb.org/images/1975/image-1.jpg |
| ipdb-1975-image-10.jpg | 91b2dc0bbf02d5606c0817abc018f59c35227d23707589daf33c23378bd3fc55 | https://www.ipdb.org/images/1975/image-10.jpg |
| ipdb-1975-image-11.jpg | d1766aca6f66651bb7e5a685b0647f651a54e4ee3af528fa00809ec6f2486a57 | https://www.ipdb.org/images/1975/image-11.jpg |
| ipdb-1975-image-12.jpg | ec60ba20a7d84ddf852ef6b4cd7ce06c8daef93de49ba3a6f60bea4924f5c15d | https://www.ipdb.org/images/1975/image-12.jpg |
| ipdb-1975-image-13.jpg | 3365be83e754790a88627601c9d58396cd778a181b5e035a3e18ac826b40267a | https://www.ipdb.org/images/1975/image-13.jpg |
| ipdb-1975-image-14.jpg | 868b2155683526dbefdc3fff6f81e98cab8dfd35de027223ee5bb4db1a74be4f | https://www.ipdb.org/images/1975/image-14.jpg |
| ipdb-1975-image-15.jpg | 1295a815e9e88a516cb968e21142df10227ef15517ff8e4ff9b1482447df9349 | https://www.ipdb.org/images/1975/image-15.jpg |
| ipdb-1975-image-16.jpg | 81ce0d70be8842e893203400e465c3c62d62220f28725acdc99689d6599aa389 | https://www.ipdb.org/images/1975/image-16.jpg |
| ipdb-1975-image-17.jpg | 1be2d6707bbee9dad364292507b69b3967d5f4f1eb523dca31a837b0983405c1 | https://www.ipdb.org/images/1975/image-17.jpg |
| ipdb-1975-image-18.jpg | fcb4e427333334e79c4c5d39b1a9fd67d741954ef18a0b957716d95b74842d0a | https://www.ipdb.org/images/1975/image-18.jpg |
| ipdb-1975-image-2.jpg | 8e0e0980afc8664858962e690882bd852405cf40ebe3e1d54b7cae9f4e62b696 | https://www.ipdb.org/images/1975/image-2.jpg |
| ipdb-1975-image-3.jpg | 435d4b011cc23ce17af409e8173427a4ff30b9b65c9e797830c6d4b2be18a856 | https://www.ipdb.org/images/1975/image-3.jpg |
| ipdb-1975-image-4.jpg | 3551407ffabda48fa8caa03ec9159fe9c31ce9e7fe87b5dd30e5b210be6527a6 | https://www.ipdb.org/images/1975/image-4.jpg |
| ipdb-1975-image-5.jpg | f3a5adee9fe4d49be93ffa045120810cae60c2cff1c7bfce9cbaf2e93a16d9df | https://www.ipdb.org/images/1975/image-5.jpg |
| ipdb-1975-image-6.jpg | 110b67d968c145615fef0d26a1d6fac6bc3a9cd2f4205d82cf27b083955ceffd | https://www.ipdb.org/images/1975/image-6.jpg |
| ipdb-1975-image-7.jpg | 60ab163e49659b78a00a7563514f316ad77b583fd3a2e32274c0351997e75789 | https://www.ipdb.org/images/1975/image-7.jpg |
| ipdb-1975-image-8.jpg | 66bc18b6c7a351cd9906b6a55c229dc9f1bb654839e71569acfcfbf04db181fe | https://www.ipdb.org/images/1975/image-8.jpg |
| ipdb-1975-image-9.jpg | bbd6dc98c7696e25440cda744e4f6772655ee57203c6515a87d5e116baf297c5 | https://www.ipdb.org/images/1975/image-9.jpg |

Photo observations used by the record: the lower-playfield photo (image-12) shows two right-hand lanes
beside the right kicking rubber, the outer one under an `ADV. X` insert and the inner one under a round
red insert. The factory lamp list names L41 "Right Return Rollover, Advance Multiplier" and L38
"Right Out Rollover, Special", and the factory drawing puts L41 and SW 75 on the outer lane and L38 and
SW 65 on the inner one, so the factory calls the outer right lane the return lane and the inner one the
out lane. The photos are not used for coordinates.
