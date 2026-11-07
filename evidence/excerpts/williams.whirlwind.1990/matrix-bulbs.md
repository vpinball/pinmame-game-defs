# Matrix lamps: physical bulbs and renderer reconciliation

Method: exact VPX object/script extraction plus primary physical-image inspection; reviewed by repository curator, 2026-11-07. Factual data only. Complete 57 playfield-lamp inventory and raw objects/hashes are pinned in `tools/seeds/williams/whirlwind-1990-matrix-bulbs.json`.

Factory operations printed 76/77 enumerates all 64 physical matrix bulbs. Seven 2–8 are backbox awards. The 57 playfield bulbs have one bulb per named matrix address, from the lamp matrix, lamp-board assemblies and individual socket assemblies (jet Socket & Bulb Assembly A-11199, printed 60). Bloom objects, light maps and image-swap covers are not extra lamps. This count is physical construction, never a count of Light objects.

Original ordinary l1,l9–l32,l41–l64 are bulb-configured objects with meshes suppressed. The source script binds each retained center (lamp 9 omission is corroborated separately by Bigus). Physical original-stock underside pictures show individual ordinary bayonets and discrete twist-lock PCB holders at their locations; stripped wood and assembled views reconcile location, count and order. This physical correspondence is needed: a suppressed-mesh render helper alone does not prove a socket.

Twelve actual twist-lock axes (9,10,20,22,27,28,29,32,60,61,62,63) were withheld from the 18 non-lamp wood controls and 113 same-wood match alignment. The seed records each native read and apparent wood-plane projection: all agree within 0.024610 normalized, 11 within 0.0164. This is a check of model/socket correspondence with PCB-height parallax, not an optical survey and not a source for replacing precise model coordinates. Additional stock complete/sparse images show the distinct ordinary bulbs near 43/44 and 46/56/64. The ordinary diode/bayonet beside 44 cannot establish its wiring color through the separate switch loom. Occluded sites are not claimed as independently measured.

Six jets 33–38 use actual own `show_bulb_mesh=true` Bigus l33–l38 and agree exactly with original centers. The 4K larger bumper glow helpers are effects and do not move these bulbs.

Cellar 39/40 need different geometry. Original script uses colored `l39/l40` cover primitives, with `bulbcover1_red*`/`bulbcover1_yellow*` images. Their original world bounds confirm these are covers at approximately (0.143807,0.470758)/(0.345436,0.440059), not a raw-origin offset. The 4K script routes case 39 to CellarLeftNew and case 40 to CellarRightNew, then swaps `BulbLeft`/`BulbRight` images `simplelightwhiteN` (script 4359–4364,4507–4530). Each separate 261-vertex mesh is a single rounded glass bulb body with 24 VPU height. Its own world-bounds midpoint, not primitive origin or a centroid of several objects, supplies placement:

| Lamp | Own bulb | Bounds minimum VPU | Bounds maximum VPU | Normalized center (952x2164) |
| --- | --- | --- | --- | --- |
|39|BulbLeft|(148.28107,988.4647,-177.17503)|(170.72824,1011.73315,-152.85637)|(0.167547,0.462153)|
|40|BulbRight|(310.8419,953.7601,-177.17503)|(333.18295,976.96063,-152.85637)|(0.338248,0.446100)|

Export: vpxtool git:v0.33.3 `export obj --units vpu`. Retained `parent-4k-world/table.obj` SHA256 `65824201392067e7a6b055d5105c738629953caba5a4550710b90d75c42b446c`. Original world OBJ SHA256 `221896a5e72c3ec2bf0d06f20c1de041c5958da21028aebf98a6f8b06fb9afab`. The left cover differs about 0.0253 normalized from the bulb; the cover is rejected as bulb authority. The right cover also is replaced consistently. Original known-working script remains runtime authority. The 4K table supplements bulb modeling; it does not become independent hardware construction evidence.

The 4K lamp 43/44/46 insert light-map helpers and L55 companion effects have no shown bulb and different centers. Those are renderer discrepancies, not competing physical sockets. Ordinary physically corroborated original centers remain; no averaging with helpers. The source tables' immutable identities/extraction manifests are in their existing definition source records.

## Physical photograph sources

- `under-bare.jpg`,4032x2268, SHA256 `65d1725bd5f015ae346355da9e43e9cff7329ac37c5263c13a74f38305030ef2`, acquired `2026-11-07T04:08:42.339092+00:00`. Native https://lh3.googleusercontent.com/pw/AP1GczPaWa1wSZJOBsmHgQzYdYef_XuelmnpA2QxIrslz9KIIbMC5cCOZtvJ3tCiOsjj3aXge5AV8iVhwv81Np8DZB0h0LvANQDLQ30BsOd1f6y_JcobDM8=s0-d-ip ; photo https://photos.google.com/share/AF1QipNzrJHgP9BLLB02wpWCcNedqbYrZ-7gK-thqLpWC58RAPj1LI-ce-oyUNx3vEoz2Q/photo/AF1QipNsVFczp0lWyfWUnBzn2A_7TB0LvDUu-GWHtAeD?key=RXlKRjZlVGlyZ0x6T1FEUUFhR2U4eTdsNjBjR2h3 .

- `under-stock-complete.jpg`,4032x2268, SHA256 `6fcf9fee82605281b104c84d8f5cc4dcf6599562a3b5ff5a0f19b1ce2355d728`, acquired `2026-11-07T04:27:52.383422+00:00`. Native https://lh3.googleusercontent.com/pw/AP1GczOBH-bhguLTHEcaqI1L-5DfB50vAqZfXuNXKJqXHXmC7y3cfkmMaSskJOzNydZ7PViHqI2wTxeMXcTk-MfDY6dQmGQiGEmzHNj1xxsrJMJEtN-IQ2I=s0-d-ip ; photo https://photos.google.com/share/AF1QipNzrJHgP9BLLB02wpWCcNedqbYrZ-7gK-thqLpWC58RAPj1LI-ce-oyUNx3vEoz2Q/photo/AF1QipMyenRPbcF2beA9JdqY7gMu-x1dsDRLUvCN4I7Y?key=RXlKRjZlVGlyZ0x6T1FEUUFhR2U4eTdsNjBjR2h3 .

- `under-stock-sparse.jpg`,4032x2268, SHA256 `f9bba5bdc9091451c6879f3d1333b695f3a9dd0c75d85eca7ee4bf1e1f3b74c1`, acquired `2026-11-07T04:27:53.500235+00:00`. Native https://lh3.googleusercontent.com/pw/AP1GczM-yzB_zEknHcmrRbNRvpHQWUtAGKkaBxAl0xF9ZqC5J3rY-EfDvQ4RNcite9eULGciZJuvs74312PgpMuvdL11FA-QNb66AKMTgz2GA5QE5CJv3o0=s0-d-ip ; photo https://photos.google.com/share/AF1QipNzrJHgP9BLLB02wpWCcNedqbYrZ-7gK-thqLpWC58RAPj1LI-ce-oyUNx3vEoz2Q/photo/AF1QipNjr_PiT0F3LtDkyiWO0s0q6leKulHRHPDGdJ6o?key=RXlKRjZlVGlyZ0x6T1FEUUFhR2U4eTdsNjBjR2h3 .

Read regions for the 12 held-out sockets are exact native centers in the seed. The six contact sheets `parent-gi-world-checks/matrix-stock-sample-0.jpg` through 5 retain coarse context for all 57; original photo axes, not crosshair predictions, establish visible hardware. Sheets are review aids, not independent sources or coordinate measurements.
