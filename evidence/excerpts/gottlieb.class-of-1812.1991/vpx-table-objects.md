# Class of 1812 retained-table objects

Source: `Class of 1812  - NZ&TT 1.0.vpx` (SHA-256 `27e1842e63714b2507aa828c1f8751a0324f756259b453ddc8c8d95583cc1500`), vpxtool git:v0.33.3 extraction (manifest SHA-256 `66c1a607486f804c3cdd14bf8f8c0e240b3ad42978280e5a7e63f408fcaa3f0f`) and `export obj --units vpu` (SHA-256 `72f51ce7240f8f21ad4d397831b86777d5a196d26f455cf1f09b2eafdeabc35c`).
Bounds left=0 top=0 right=952 bottom=1974; normalized x = x/952, y = y/1974, rounded to six places.

Each row is a placed object, the controller addresses placed on it, its coordinate as read from the extraction
(or the OBJ export for primitives whose stored position is not the part's centre), and the first lines of the
embedded script (CRLF, SHA-256 `ff98cc7740b1b81cedf0322090034879fc66ce8906759f8d5e897c00e1ac1914`) that name it outside comments. The embedded script is
the 2017 script before Thalamus's 2018 patch, so its line numbers differ from the pinned known-working script's,
which binds every listed address to the same object except switch 44, whose row says why.

Light rows also give the light's flags from its gameitem: `is_image_mode` with its image, otherwise whether
`show_bulb_mesh` draws a bulb, and its surface when it has one.

| Addresses | Object | x | y | Point | Normalized x | Normalized y | Script lines |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| switch 10, solenoid 1 | Bumper `sw10` | 431.34116 | 426.20593 | stored centre | 0.453089 | 0.21591 | 104, 361 |
| switch 11, solenoid 2 | Bumper `sw11` | 635.9831 | 350.3542 | stored centre | 0.668049 | 0.177484 | 104, 362 |
| switch 12, solenoid 3 | Bumper `sw12` | 597.2671 | 568.4282 | stored centre | 0.627381 | 0.287958 | 104, 363 |
| switch 13 | Wall `sw13` | 220.29066 | 1325.7377999999999 | drag-point mean | 0.231398 | 0.6716 | 104, 367, 378 |
| switch 14 | Wall `sw14` | 641.5223025 | 1322.159425 | drag-point mean | 0.673868 | 0.669787 | 104, 386, 397 |
| switch 15 | Spinner `sw15` | 132.31686 | 653.5003 | stored centre | 0.138988 | 0.331054 | 406, 790 |
| switch 16 | HitTarget `sw16` | 104.72444 | 988.6161 | stored position | 0.110005 | 0.500819 | 125, 409 |
| switch 17 | HitTarget `sw17` | 744.3315 | 816.7936 | stored position | 0.781861 | 0.413776 | 132, 414 |
| switch 20 | HitTarget `sw20` | 83.70397 | 951.2443 | stored position | 0.087924 | 0.481887 | 420 |
| switch 21 | HitTarget `sw21` | 373.22195 | 593.64136 | stored position | 0.39204 | 0.30073 | 424 |
| switch 22 | HitTarget `sw22` | 773.78577 | 840.2449 | stored position | 0.8128 | 0.425656 | 428 |
| switch 23 | Trigger `sw23` | 123.56657 | 1352.0946 | stored centre | 0.129797 | 0.684952 | 433, 434 |
| switch 24 | Trigger `sw24` | 738.4374 | 1348.905 | stored centre | 0.77567 | 0.683336 | 435, 436 |
| switch 25 | Trigger `sw25` | 431.4655 | 201.02963 | stored centre | 0.45322 | 0.101839 | 437, 438 |
| switch 26 | HitTarget `sw26` | 108.99944 | 933.6987 | stored position | 0.114495 | 0.472998 | 125, 410 |
| switch 27 | HitTarget `sw27` | 749.2642 | 874.25946 | stored position | 0.787042 | 0.442887 | 132, 415 |
| switch 30 | HitTarget `sw30` | 88.12606 | 894.06934 | stored position | 0.092569 | 0.452923 | 421 |
| switch 31 | HitTarget `sw31` | 386.1557 | 562.2307 | stored position | 0.405626 | 0.284818 | 425 |
| switch 32 | HitTarget `sw32` | 778.58075 | 894.0025 | stored position | 0.817837 | 0.452889 | 429 |
| switch 33 | Trigger `sw33` | 57.548492 | 1350.0902 | stored centre | 0.06045 | 0.683936 | 440, 441 |
| switch 34 | Trigger `sw34` | 804.45544 | 1350.9094 | stored centre | 0.845016 | 0.684351 | 442, 443 |
| switch 35 | Trigger `sw35` | 506.73105 | 201.02965 | stored centre | 0.532281 | 0.101839 | 444, 445 |
| switch 36 | HitTarget `sw36` | 113.60331 | 876.4794 | stored position | 0.119331 | 0.444012 | 125, 411 |
| switch 37 | HitTarget `sw37` | 754.1969 | 930.9856 | stored position | 0.792224 | 0.471624 | 132, 416 |
| switch 40 | HitTarget `sw40` | 91.71574 | 842.3048 | stored position | 0.09634 | 0.426699 | 422 |
| switch 41 | HitTarget `sw41` | 399.70538 | 532.05206 | stored position | 0.419859 | 0.26953 | 426 |
| switch 42 | HitTarget `sw42` | 784.057 | 957.0473 | stored position | 0.823589 | 0.484826 | 430 |
| switch 43 | Trigger `sw43` | 891.02606 | 1682.1818 | stored centre | 0.935952 | 0.852169 | 446, 447 |
| switch 44 | Kicker `Slot2` | 665.3572 | 1727.1392 | stored centre | 0.698905 | 0.874944 | 214, 220, 231; the trough's second position. The script writes 44 from Slot1, the release; the ROM's trough probes and the table's 3.0.21 update place 44 here |
| switch 45 | Trigger `sw45` | 582.67847 | 201.00935 | stored centre | 0.612057 | 0.101828 | 448, 449 |
| switch 46 | HitTarget `sw46` | 119.1937 | 816.6293 | stored position | 0.125203 | 0.413693 | 125, 412 |
| switch 47 | HitTarget `sw47` | 758.883 | 987.7117 | stored position | 0.797146 | 0.500361 | 132, 417 |
| switch 50 | Trigger `sw50` | 698.5091 | 124.301994 | stored centre | 0.733728 | 0.06297 | 453 |
| switch 51 | Trigger `sw51` | 61.133293 | 130.25858 | stored centre | 0.064216 | 0.065987 | 454 |
| switch 52, solenoid 6 | Kicker `sw52` | 548.87244 | 718.1749 | stored centre | 0.576547 | 0.363817 | 109, 111, 297, 304 |
| switch 53, solenoid 7 | Kicker `sw53k` | 308.4339 | 461.5646 | stored centre | 0.323985 | 0.233822 | 117, 119 |
| switch 54, solenoid 29 | Kicker `Drain` | 440.50513 | 1855.7125 | stored centre | 0.462715 | 0.940077 | 148, 235, 236, 241 |
| switch 55 | Trigger `sw55` | 343.77905 | 160.14267 | stored centre | 0.361112 | 0.081126 | 450, 451 |
| solenoid 4 | Primitive `SLING1` | 212.92339 | 1324.87335 | OBJ mesh centre | 0.223659 | 0.671162 | 372, 380, 381 |
| solenoid 5 | Primitive `SLING2` | 647.80165 | 1324.5705 | OBJ mesh centre | 0.680464 | 0.671008 | 391, 399, 400 |
| solenoid 8 | left drop-target bank (HitTargets `sw16`, `sw26`, `sw36`, `sw46`) | 111.630223 | 903.855875 | mean of the four stored positions | 0.117259 | 0.45788 | sw16: 125, 409; sw26: 125, 410; sw36: 125, 411; sw46: 125, 412 |
| solenoid 9 | right drop-target bank (HitTargets `sw17`, `sw27`, `sw37`, `sw47`) | 751.6689 | 902.43759 | mean of the four stored positions | 0.789568 | 0.457162 | sw17: 132, 414; sw27: 132, 415; sw37: 132, 416; sw47: 132, 417 |
| solenoid 10 | Primitive `DiverterP` | 332.0 | 272.0 | stored position | 0.348739 | 0.137791 | 315, 321, 326, 327 |
| solenoid 11, solenoid 25 | Primitive `heart` | 489.313325 | -26.773487 | OBJ mesh centre; raw y/1974 = -0.013563, clamped to the rear edge | 0.513985 | 0.0 | 334, 336, 343, 344 |
| solenoid 12 | Primitive `BottomTeeth` | 227.10639 | -23.8483 | OBJ mesh centre; raw y/1974 = -0.012081, clamped to the rear edge | 0.238557 | 0.0 | 350, 352, 513 |
| solenoid 22 | Light `F22` | 251.58966 | 194.5473 | stored centre; no bulb mesh shown | 0.264275 | 0.098555 | 534 |
| solenoid 22 | Light `F22a` | 826.3066 | 80.932144 | stored centre; no bulb mesh shown | 0.867969 | 0.040999 | 538 |
| solenoid 23 | Light `F22x` | 299.58966 | 154.5473 | stored centre; no bulb mesh shown | 0.314695 | 0.078291 | 542, 569 |
| solenoid 23 | Light `F23` | 883.98517 | 440.43835 | stored centre; no bulb mesh shown | 0.928556 | 0.22312 | 546 |
| solenoid 24 | Light `F24a` | 674.6027 | 259.50006 | stored centre; no bulb mesh shown | 0.708616 | 0.131459 | 550 |
| solenoid 28 | Kicker `Slot1` | 724.0075 | 1700.1406 | stored centre | 0.760512 | 0.861267 | 213, 221, 222, 225 |
| solenoid 31 | Light `light1` | 671.5541 | 1518.3309 | stored centre; bulb mesh shown | 0.705414 | 0.769165 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light2` | 165.2394 | 1326.3037 | stored centre; bulb mesh shown | 0.173571 | 0.671886 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light3` | 689.97845 | 1329.0038 | stored centre; bulb mesh shown | 0.724767 | 0.673254 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light4` | 207.66902 | 1404.5614 | stored centre; bulb mesh shown | 0.21814 | 0.711531 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light5` | 149.83705 | 1495.7917 | stored centre; bulb mesh shown | 0.157392 | 0.757747 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light6` | 183.66376 | 1515.6309 | stored centre; bulb mesh shown | 0.192924 | 0.767797 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light7` | 808.7288 | 1097.3256 | stored centre; bulb mesh shown | 0.849505 | 0.555889 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light8` | 817.7317 | 871.0421 | stored centre; bulb mesh shown | 0.858962 | 0.441257 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light9` | 838.4946 | 616.6963 | stored centre; bulb mesh shown | 0.880772 | 0.312409 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light10` | 49.940567 | 1100.1002 | stored centre; bulb mesh shown | 0.052459 | 0.557295 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light11` | 52.527462 | 867.65497 | stored centre; bulb mesh shown | 0.055176 | 0.439542 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light12` | 52.36064 | 614.4766 | stored centre; bulb mesh shown | 0.055001 | 0.311285 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `Light13` | 596.94324 | 568.45056 | stored centre; bulb mesh shown | 0.627041 | 0.287969 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `Light14` | 432.59756 | 427.41354 | stored centre; bulb mesh shown | 0.454409 | 0.216522 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light15` | 647.5488 | 1407.2615 | stored centre; bulb mesh shown | 0.680198 | 0.712898 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `Light16` | 635.2643 | 351.1666 | stored centre; bulb mesh shown | 0.667294 | 0.177896 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light17` | 705.3808 | 1498.4918 | stored centre; bulb mesh shown | 0.740946 | 0.759114 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light19` | 353.53564 | 319.95084 | stored centre; bulb mesh shown | 0.371361 | 0.162082 | GI collection member (TiltRelay, GIRelay) |
| solenoid 31 | Light `light20` | 349.84024 | 524.42706 | stored centre; bulb mesh shown | 0.367479 | 0.265667 | GI collection member (TiltRelay, GIRelay) |
| lamp 0 | Light `l0` | 432.62592 | 1565.5332 | stored centre; image mode, image `1812 PFhole` | 0.454439 | 0.793077 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 2 | Primitive `TopTeeth` | 226.91764 | -9.49342 | OBJ mesh centre; raw y/1974 = -0.004809, clamped to the rear edge | 0.238359 | 0.0 | 512 |
| lamp 3 | Light `l3` | 56.288364 | 1245.1945 | stored centre; image mode, image `1812 PFhole` | 0.059126 | 0.630798 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 4 | Light `l4` | 806.70135 | 1242.3851 | stored centre; image mode, image `1812 PFhole` | 0.847375 | 0.629374 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 5 | Light `l5` | 435.05295 | 63.098286 | stored centre; image mode, image `1812 PFhole` | 0.456988 | 0.031965 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 6 | Light `l6` | 511.45892 | 61.27548 | stored centre; image mode, image `1812 PFhole` | 0.537247 | 0.031041 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 7 | Light `l7` | 592.11816 | 59.604572 | stored centre; image mode, image `1812 PFhole` | 0.621973 | 0.030195 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 10 | Primitive `bulb9` | 78.718412 | 260.80933 | OBJ mesh centre | 0.082687 | 0.132122 | 515 |
| lamp 11 | Primitive `bulb8` | 76.205145 | 258.12009 | OBJ mesh centre | 0.080047 | 0.13076 | 516 |
| lamp 12 | Primitive `bulb7` | 74.134227 | 254.53317 | OBJ mesh centre | 0.077872 | 0.128943 | 517 |
| lamp 13 | Primitive `bulb6` | 72.138805 | 251.076995 | OBJ mesh centre | 0.075776 | 0.127192 | 518 |
| lamp 14 | Primitive `bulb5` | 70.070594 | 247.49475 | OBJ mesh centre | 0.073604 | 0.125377 | 519 |
| lamp 15 | Light `l15` | 400.27554 | 86.02734 | stored centre; image mode, image `1812 PFhole` | 0.420457 | 0.04358 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 16 | Light `l16` | 479.73837 | 85.77101 | stored centre; image mode, image `1812 PFhole` | 0.503927 | 0.04345 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 17 | Light `l17` | 555.61273 | 86.02734 | stored centre; image mode, image `1812 PFhole` | 0.583627 | 0.04358 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 20 | Light `l20` | 434.20886 | 1326.2797 | stored centre; image mode, image `1812 PFhole` | 0.456102 | 0.671874 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 21 | Light `l21` | 392.3268 | 1368.0624 | stored centre; image mode, image `1812 PFhole` | 0.412108 | 0.693041 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 22 | Light `l22` | 478.21042 | 1367.7208 | stored centre; image mode, image `1812 PFhole` | 0.502322 | 0.692868 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 23 | Light `l23` | 435.46555 | 1409.1626 | stored centre; image mode, image `1812 PFhole` | 0.457422 | 0.713861 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 25 | Light `l25` | 448.60953 | 676.3314 | stored centre; image mode, image `1812 PFhole` | 0.471228 | 0.34262 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 26 | Light `l26` | 462.00897 | 631.8858 | stored centre; image mode, image `1812 PFhole` | 0.485304 | 0.320104 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 27 | Light `l27` | 478.87885 | 588.08905 | stored centre; image mode, image `1812 PFhole` | 0.503024 | 0.297917 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 30 | Light `l30` | 338.1512 | 829.82556 | stored centre; image mode, image `1812 PFhole` | 0.355201 | 0.420378 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 31 | Light `l31` | 321.9207 | 776.8954 | stored centre; image mode, image `1812 PFhole` | 0.338152 | 0.393564 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 32 | Light `l32` | 300.59225 | 716.8945 | stored centre; image mode, image `1812 PFhole` | 0.315748 | 0.363168 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 33 | Light `l33` | 706.9414 | 637.94476 | stored centre; image mode, image `1812 PFhole` | 0.742586 | 0.323174 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 34 | Light `l34` | 727.6915 | 580.62555 | stored centre; image mode, image `1812 PFhole` | 0.764382 | 0.294137 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 35 | Light `l35` | 746.42096 | 521.9746 | stored centre; image mode, image `1812 PFhole` | 0.784056 | 0.264425 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 36 | Primitive `bulb1` | 260.565765 | 674.27243 | OBJ mesh centre | 0.273704 | 0.341577 | 527 |
| lamp 37 | Primitive `bulb2` | 314.663605 | 654.91885 | OBJ mesh centre | 0.330529 | 0.331772 | 528 |
| lamp 40 | Light `l40` | 326.09283 | 1382.1764 | stored centre; image mode, image `1812 PFhole` | 0.342534 | 0.700191 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 41 | Light `l41` | 361.8379 | 1444.1362 | stored centre; image mode, image `1812 PFhole` | 0.380082 | 0.731579 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 42 | Light `l42` | 395.08524 | 1505.1084 | stored centre; image mode, image `1812 PFhole` | 0.415006 | 0.762466 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 43 | Light `l43` | 468.7622 | 1503.7908 | stored centre; image mode, image `1812 PFhole` | 0.492397 | 0.761799 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 44 | Light `l44` | 502.16522 | 1441.2941 | stored centre; image mode, image `1812 PFhole` | 0.527484 | 0.730139 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 45 | Light `l45` | 536.25995 | 1383.1566 | stored centre; image mode, image `1812 PFhole` | 0.563298 | 0.700687 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 46 | Primitive `bulb3` | 734.5213 | 461.706935 | OBJ mesh centre | 0.771556 | 0.233894 | 529 |
| lamp 47 | Primitive `bulb4` | 789.61653 | 481.392975 | OBJ mesh centre | 0.829429 | 0.243867 | 530 |
| lamp 50 | Light `l50` | 557.10394 | 803.04395 | stored centre; image mode, image `1812 PFhole` | 0.585193 | 0.406811 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 51 | Light `l51` | 674.4598 | 848.84607 | stored centre; image mode, image `1812 PFhole` | 0.708466 | 0.430013 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 52 | Light `l52` | 707.58215 | 907.0681 | stored centre; image mode, image `1812 PFhole` | 0.743259 | 0.459508 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 53 | Light `l53` | 684.50604 | 965.1782 | stored centre; image mode, image `1812 PFhole` | 0.719019 | 0.488945 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 54 | Light `l54` | 616.38403 | 865.38556 | stored centre; image mode, image `1812 PFhole` | 0.647462 | 0.438392 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 55 | Light `l55` | 624.19293 | 967.2836 | stored centre; image mode, image `1812 PFhole` | 0.655665 | 0.490012 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 56 | Light `l56` | 739.32916 | 1242.4644 | stored centre; image mode, image `1812 PFhole` | 0.776606 | 0.629415 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 57 | Light `l57` | 687.7615 | 700.9407 | stored centre; image mode, image `1812 PFhole` | 0.722439 | 0.355086 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 60 | Light `l60` | 474.97446 | 774.0489 | stored centre; image mode, image `1812 PFhole` | 0.498923 | 0.392122 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 61 | Light `l61` | 181.54128 | 966.95764 | stored centre; image mode, image `1812 PFhole` | 0.190695 | 0.489847 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 62 | Light `l62` | 162.11249 | 906.2718 | stored centre; image mode, image `1812 PFhole` | 0.170286 | 0.459104 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 63 | Light `l63` | 194.94383 | 851.1078 | stored centre; image mode, image `1812 PFhole` | 0.204773 | 0.431159 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 64 | Light `l64` | 250.57713 | 869.1375 | stored centre; image mode, image `1812 PFhole` | 0.263211 | 0.440293 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 65 | Light `l65` | 241.61302 | 967.548 | stored centre; image mode, image `1812 PFhole` | 0.253795 | 0.490146 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 66 | Light `l66` | 123.48255 | 1245.0107 | stored centre; image mode, image `1812 PFhole` | 0.129709 | 0.630705 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 67 | Primitive `bulb10` | 380.47393 | 57.895043 | OBJ mesh centre | 0.399657 | 0.029329 | 531 |
| lamp 70 | Light `l70` | 153.21771 | 1118.4634 | stored centre; image mode, image `1812 PFhole` | 0.160943 | 0.566597 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 71 | Light `l71` | 199.56506 | 1080.1902 | stored centre; image mode, image `1812 PFhole` | 0.209627 | 0.547209 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 72 | Light `l72` | 241.97615 | 1120.5436 | stored centre; image mode, image `1812 PFhole` | 0.254177 | 0.567651 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 73 | Light `l73` | 203.85461 | 1169.5598 | stored centre; image mode, image `1812 PFhole` | 0.214133 | 0.592482 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 74 | Light `l74` | 618.6954 | 1120.711 | stored centre; image mode, image `1812 PFhole` | 0.64989 | 0.567736 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 75 | Light `l75` | 666.23865 | 1072.1045 | stored centre; image mode, image `1812 PFhole` | 0.699831 | 0.543113 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 76 | Light `l76` | 709.05817 | 1113.912 | stored centre; image mode, image `1812 PFhole` | 0.744809 | 0.564292 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 77 | Light `l77` | 664.185 | 1160.5664 | stored centre; image mode, image `1812 PFhole` | 0.697673 | 0.587926 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 80 | Light `l80` | 327.23633 | 946.00433 | stored centre; image mode, image `1812 PFhole` | 0.343736 | 0.479232 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 81 | Light `l81` | 370.71365 | 901.4016 | stored centre; image mode, image `1812 PFhole` | 0.389405 | 0.456637 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 82 | Light `l82` | 431.5557 | 885.91223 | stored centre; image mode, image `1812 PFhole` | 0.453315 | 0.44879 | 269 |
| lamp 83 | Light `l83` | 492.33057 | 900.7248 | stored centre; image mode, image `1812 PFhole` | 0.517154 | 0.456294 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 84 | Light `l84` | 536.1028 | 946.5046 | stored centre; image mode, image `1812 PFhole` | 0.563133 | 0.479486 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 85 | Light `l85` | 433.08807 | 949.9709 | stored centre; image mode, image `1812 PFhole` | 0.454924 | 0.481242 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 86 | Light `l86` | 428.5661 | 1126.1685 | stored centre; image mode, image `1812 PFhole` | 0.450174 | 0.570501 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 90 | Light `l90` | 375.515 | 1071.5498 | stored centre; image mode, image `1812 PFhole` | 0.394449 | 0.542832 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 91 | Light `l91` | 435.2848 | 1067.7041 | stored centre; image mode, image `1812 PFhole` | 0.457232 | 0.540884 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 92 | Light `l92` | 490.88358 | 1065.6566 | stored centre; image mode, image `1812 PFhole` | 0.515634 | 0.539846 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 93 | Light `l93` | 373.29477 | 1128.6385 | stored centre; image mode, image `1812 PFhole` | 0.392116 | 0.571752 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 94 | Light `l94` | 488.40332 | 1126.3512 | stored centre; image mode, image `1812 PFhole` | 0.513029 | 0.570593 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 95 | Light `l95` | 371.91968 | 1189.6052 | stored centre; image mode, image `1812 PFhole` | 0.390672 | 0.602637 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 96 | Light `l96` | 430.2263 | 1186.5515 | stored centre; image mode, image `1812 PFhole` | 0.451918 | 0.60109 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 97 | Light `l97` | 490.19122 | 1187.877 | stored centre; image mode, image `1812 PFhole` | 0.514907 | 0.601761 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 100 | Light `l100` | 313.73447 | 1006.4357 | stored centre; image mode, image `1812 PFhole` | 0.329553 | 0.509846 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 101 | Light `l101` | 373.23828 | 1006.6065 | stored centre; image mode, image `1812 PFhole` | 0.392057 | 0.509932 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 102 | Light `l102` | 431.4203 | 1007.33514 | stored centre; image mode, image `1812 PFhole` | 0.453173 | 0.510301 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 103 | Light `l103` | 489.59927 | 1005.33997 | stored centre; image mode, image `1812 PFhole` | 0.514285 | 0.509291 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 104 | Light `l104` | 548.25543 | 1007.5129 | stored centre; image mode, image `1812 PFhole` | 0.575899 | 0.510392 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 105 | Light `l105` | 315.285 | 1067.2394 | stored centre; image mode, image `1812 PFhole` | 0.331182 | 0.540648 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 106 | Light `l106` | 547.7653 | 1066.8965 | stored centre; image mode, image `1812 PFhole` | 0.575384 | 0.540474 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 107 | Light `l107` | 315.89224 | 1128.0178 | stored centre; image mode, image `1812 PFhole` | 0.33182 | 0.571438 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 110 | Light `l110` | 546.45654 | 1128.1582 | stored centre; image mode, image `1812 PFhole` | 0.574009 | 0.571509 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 111 | Light `l111` | 314.8806 | 1190.2338 | stored centre; image mode, image `1812 PFhole` | 0.330757 | 0.602955 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 112 | Light `l112` | 546.3275 | 1188.6406 | stored centre; image mode, image `1812 PFhole` | 0.573873 | 0.602148 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 113 | Light `l113` | 315.5375 | 1251.7742 | stored centre; image mode, image `1812 PFhole` | 0.331447 | 0.634131 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 114 | Light `l114` | 374.35388 | 1250.2395 | stored centre; image mode, image `1812 PFhole` | 0.393229 | 0.633353 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 115 | Light `l115` | 432.41827 | 1250.0884 | stored centre; image mode, image `1812 PFhole` | 0.454221 | 0.633277 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 116 | Light `l116` | 490.15097 | 1248.9454 | stored centre; image mode, image `1812 PFhole` | 0.514864 | 0.632698 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |
| lamp 117 | Light `l117` | 548.9427 | 1250.0431 | stored centre; image mode, image `1812 PFhole` | 0.57662 | 0.633254 | InitLamps binds Light L<n> to lamp n through Execute (line 498) |

## Lights in the script's bindings that are not placements

| Object | Drawn for | x | y | Flags | Why not placed |
| --- | --- | ---: | ---: | --- | --- |
| Light `L36` | lamp 36 | 260.67282 | 673.9188 | no bulb mesh shown | sits on Primitive `bulb1`, the placement |
| Light `L37` | lamp 37 | 314.89874 | 654.9652 | no bulb mesh shown | sits on Primitive `bulb2`, the placement |
| Light `L46` | lamp 46 | 734.1385 | 461.4291 | no bulb mesh shown | sits on Primitive `bulb3`, the placement |
| Light `L47` | lamp 47 | 790.86084 | 480.39175 | no bulb mesh shown | sits on Primitive `bulb4`, the placement |
| Light `L67` | lamp 67 | 382.2024 | 53.84225 | no bulb mesh shown | sits on Primitive `bulb10`, the placement |
| Light `L67a` | lamp 67 | 381.6098 | 71.02742 | no bulb mesh shown | a second light on lamp 67 beside Primitive `bulb10`, the placement |
| Light `light18` | solenoid 31 (GI collection) | 161.06955 | 456.0633 | no bulb mesh shown | render light, no socket |
| Light `light21` | solenoid 31 (GI collection) | 737.85236 | 263.2888 | no bulb mesh shown | render light, no socket |
| Light `light22` | solenoid 31 (GI collection) | 245.13869 | 195.13016 | no bulb mesh shown | render light, no socket |
| Light `light23` | solenoid 31 (GI collection) | 160.1457 | 313.79218 | no bulb mesh shown | render light, no socket |
| Light `F24` | solenoid 24 (line 548) | 190.12376 | 502.51755 | no bulb mesh shown, surface `RuinsFlash` | render light under the ramp, no dome over it |

Control: the OBJ export's pop bumper body `BBody1` centres at (431.34122, 426.205935), within 0.0001 units of
Bumper `sw10`'s stored centre (431.34116, 426.20593), so OBJ x and y are playfield x and y.

The GI collection's 23 members are the lights the script's `GIRelay` and `TiltRelay` switch with
`for each xx in GI` (embedded script and pinned script alike); the table's grouping is not the machine's wiring. The
19 that show a bulb mesh are placed; the 4 that show none are listed above.
