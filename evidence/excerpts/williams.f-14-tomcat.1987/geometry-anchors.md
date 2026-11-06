# Exact VPW 1.0 contact, assembly and emitter anchors

Method: mixed; selected world OBJ bounds were independently recomputed and checked against the retained extraction inventory. Reviewed: true. Bounds 952 x 1974, x left to right, y rear to front; normalize once to six decimals. This is same-table geometry reconciliation, not an independent physical measurement. Flupper dome anchors use their own base centers; filaments and baked gate arms use world-space bounds. All locations stay observed. Under-insert overlays, radar lightmaps, ambient matrix-bulb doubles and the virtual center-target GI light are excluded.

World export: `vpxtool export obj --units vpu`, manifest SHA-256 `4947a4eafd30992625627bc01228470b25e71f5fdcf5cff0682c6b83d186c366`, 69 files. Primary independently checked 47 candidate bounds against the retained export. Raw points and file hashes:

```json
[
  {
    "device": "switch.outhole",
    "object": "sw10",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw10.json",
    "sha256": "1f24ba61e58443e35bf4290530787ca4b64dad1f332c7b49bbc06c3a984d9282",
    "raw_x": 475.19644,
    "raw_y": 1890.1433,
    "x": 0.499156,
    "y": 0.957519,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-ball-trough",
    "object": "sw11",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw11.json",
    "sha256": "f1b97d2dbf7fb9b65e6cb79d2a4aafa961d3b94960eeca0445571ab99fb11107",
    "raw_x": 802.5394,
    "raw_y": 1700.1243,
    "x": 0.843004,
    "y": 0.861259,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-center-ball-trough",
    "object": "sw12",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw12.json",
    "sha256": "71b1b1ea0af3eb2b71fde7b605023bf5ecf3f5469d90667b649b0ee713f7c010",
    "raw_x": 750.3106,
    "raw_y": 1730.2639,
    "x": 0.788141,
    "y": 0.876527,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-center-ball-trough",
    "object": "sw13",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw13.json",
    "sha256": "9bb59492460f8a265be2ce2d61c6396dafa187331245f67a07d6f05f20f374c8",
    "raw_x": 699.6439,
    "raw_y": 1762.5272,
    "x": 0.73492,
    "y": 0.892871,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-ball-trough",
    "object": "sw14",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw14.json",
    "sha256": "124e24f58a8aaec66f752356c7f7019511b3dfbfa7ccfdfe9aab384ead266ea7",
    "raw_x": 645.39557,
    "raw_y": 1793.2566,
    "x": 0.677937,
    "y": 0.908438,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.ball-shooter-lane",
    "object": "sw16",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw16.json",
    "sha256": "480ca71f222471ab9f02e90ab9b577806553de054bf14354757ddda1de128c99",
    "raw_x": 896.9828,
    "raw_y": 1716.3903,
    "x": 0.942209,
    "y": 0.869499,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.ramp-entry",
    "object": "sw20",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw20.json",
    "sha256": "205597c2fd9a0b745b281ab56dd994e97083d319e1418acd35fb1f1e1212540e",
    "raw_x": 895.89215,
    "raw_y": 635.5177,
    "x": 0.941063,
    "y": 0.321944,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-eject",
    "object": "sw21",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw21.json",
    "sha256": "b0cbe3192da73039a94978789f96bc1a956d2df410280ceb7f57b345051c9de7",
    "raw_x": 895.01276,
    "raw_y": 1022.808,
    "x": 0.940139,
    "y": 0.51814,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-center-eject",
    "object": "sw22",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw22.json",
    "sha256": "600282f6d85f68a400ea276ad606007817fd01fd54b75eed3555596bb2c85d80",
    "raw_x": 405.53433,
    "raw_y": 760.2239,
    "x": 0.425981,
    "y": 0.385118,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-center-eject",
    "object": "sw23",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw23.json",
    "sha256": "ceb83ee4f58d2e8fbc7c3c5952615a01d6894d3029a00baa4911205654c295fc",
    "raw_x": 513.7195,
    "raw_y": 775.35004,
    "x": 0.539621,
    "y": 0.392781,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.ball-popper",
    "object": "sw24",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw24.json",
    "sha256": "f3967b7d3846f646b3e920c1724ec47483dfdb3e40183731f781a2664589fb42",
    "raw_x": 858.929,
    "raw_y": 70.41359,
    "x": 0.902236,
    "y": 0.035671,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-center-target",
    "object": "sw25",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw25.json",
    "sha256": "51831e90aeb967bb539b1039337430b8e9cf9d1943e8abc881d2c66b052d9435",
    "raw_x": 429.1487,
    "raw_y": 905.271,
    "x": 0.450786,
    "y": 0.458597,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-center-target",
    "object": "sw26",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw26.json",
    "sha256": "8af38f7606b9cc9098327d38590a2d84a1f84d15028be79dd796014b20492a6a",
    "raw_x": 498.67953,
    "raw_y": 904.9336,
    "x": 0.523823,
    "y": 0.458426,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.jet-bumper",
    "object": "Bumper1",
    "kind": "Bumper",
    "file": "gameitems/Bumper.Bumper1.json",
    "sha256": "7eecce806dfc8872438c5749298ac5b151bfbea4d7929da7df514a333019fb8b",
    "raw_x": 465.5134,
    "raw_y": 643.65234,
    "x": 0.488985,
    "y": 0.326065,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.lower-ramp",
    "object": "sw30",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw30.json",
    "sha256": "f1bc5859d5e4ae04a9f6d0987ad65bcabf6a7e43125e0b7b2d33ff29b42e00f5",
    "raw_x": 134.47237,
    "raw_y": 696.2346,
    "x": 0.141252,
    "y": 0.352702,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.middle-ramp",
    "object": "sw31",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw31.json",
    "sha256": "036ae03bc49647d9c1a7d56ea1dda720e50822a1700ebda8b38946840140b829",
    "raw_x": 131.62427,
    "raw_y": 530.0029,
    "x": 0.138261,
    "y": 0.268492,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.upper-ramp",
    "object": "sw32",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw32.json",
    "sha256": "384d68fcd74d67ea319c174aeb3aa65d8f66727840ac24f63ea46f3880756411",
    "raw_x": 133.25818,
    "raw_y": 371.7021,
    "x": 0.139977,
    "y": 0.188299,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.lower-left-t-target",
    "object": "sw33",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw33.json",
    "sha256": "78cec7f2244d5c7918dc9d2ffcf2c95ed1652cec2a33610485062f95e48c5e76",
    "raw_x": 110.9118,
    "raw_y": 1030.0883,
    "x": 0.116504,
    "y": 0.521828,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.lower-left-o-target",
    "object": "sw34",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw34.json",
    "sha256": "6df11a487c17c202686ab9f1a3649b915ce6b96cc6f6f3cb278c81a8bbdcda2a",
    "raw_x": 117.76936,
    "raw_y": 966.1975,
    "x": 0.123707,
    "y": 0.489462,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.lower-left-m-target",
    "object": "sw35",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw35.json",
    "sha256": "b19d7ef63b35600adb31af0b536e65e3ade5fa00a68a3ddddd90c453f73dceea",
    "raw_x": 124.401825,
    "raw_y": 905.3691,
    "x": 0.130674,
    "y": 0.458647,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.lower-right-t-target",
    "object": "sw36",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw36.json",
    "sha256": "051854594bcb2825c28403ddae85452a97b4fc88314eccc12ca5141709f117e8",
    "raw_x": 796.0576,
    "raw_y": 1062.4956,
    "x": 0.836195,
    "y": 0.538245,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.lower-right-a-target",
    "object": "sw37",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw37.json",
    "sha256": "fd8b46149f4233aec7df558a2c25ef6c3c96a88914b5018018ce7427423f71a4",
    "raw_x": 790.78516,
    "raw_y": 1002.76526,
    "x": 0.830657,
    "y": 0.507986,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.lower-right-c-target",
    "object": "sw38",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw38.json",
    "sha256": "1ed8e55d764a285064cd3e015095aba535537d7f86a27d140f602e7e0b2bafd4",
    "raw_x": 785.14154,
    "raw_y": 938.1865,
    "x": 0.824729,
    "y": 0.475272,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.3-target",
    "object": "sw41",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw41.json",
    "sha256": "eec43b7ae3065f582bddac8940eab7155ec3f1128a22bd1d38a6677f5723f5e0",
    "raw_x": 393.6296,
    "raw_y": 839.04034,
    "x": 0.413476,
    "y": 0.425046,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.2-target",
    "object": "sw42",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw42.json",
    "sha256": "654c79da3dad2ee2f87bdd4bac6f1e8186a5607afe647f1c750fcfebaa71ecd3",
    "raw_x": 367.69894,
    "raw_y": 786.61884,
    "x": 0.386238,
    "y": 0.39849,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.1-target",
    "object": "sw43",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw43.json",
    "sha256": "95eec50fc39dbc065ce599f3f86a966143c35d3597122a42c78cdc388e8d76ad",
    "raw_x": 342.95908,
    "raw_y": 734.8223,
    "x": 0.360251,
    "y": 0.37225,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.4-target",
    "object": "sw44",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw44.json",
    "sha256": "84d4be49c41058f43cd8c11798565b6e3ed238dfe01db03ad4e76f07ecea1dff",
    "raw_x": 531.4959,
    "raw_y": 840.0965,
    "x": 0.558294,
    "y": 0.425581,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.5-target",
    "object": "sw45",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw45.json",
    "sha256": "fe5f0574c60c46a4356bfe41152a9e9663a093a705f01f51209312ead18c87ac",
    "raw_x": 559.14264,
    "raw_y": 786.86426,
    "x": 0.587335,
    "y": 0.398614,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.6-target",
    "object": "sw46",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw46.json",
    "sha256": "bf6269c02886ed7ba0ff5903d6d7757b9243f19a8c5be6b3006c9fc9ea6f28b1",
    "raw_x": 585.6897,
    "raw_y": 734.7429,
    "x": 0.61522,
    "y": 0.37221,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.top-right-loop",
    "object": "sw47",
    "kind": "Gate",
    "file": "gameitems/Gate.sw47.json",
    "sha256": "3d8ba9a93c5b46f3ced54c90ab1151f858f0522e6a5de5ddc4b43a74ca28c1f3",
    "raw_x": 750.7893,
    "raw_y": 198.314,
    "x": 0.788644,
    "y": 0.100463,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.spinner",
    "object": "sw48",
    "kind": "Spinner",
    "file": "gameitems/Spinner.sw48.json",
    "sha256": "8939a6220b5b1573cd799c72e9f49bb867bcd980ca2e5893c10d9e0a48ae4822",
    "raw_x": 746.994,
    "raw_y": 296.44162,
    "x": 0.784658,
    "y": 0.150173,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-left-t-target",
    "object": "sw49",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw49.json",
    "sha256": "3c9e25e7fcadf03af25d81be202b63e5efe4d47dd23cde0069117443b0e8795f",
    "raw_x": 297.2304,
    "raw_y": 340.98804,
    "x": 0.312217,
    "y": 0.17274,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-left-o-target",
    "object": "sw50",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw50.json",
    "sha256": "e0e5bb35ac253342a03635a91c020e67888ab6119b13befe66d7b5c5d10f0764",
    "raw_x": 325.7208,
    "raw_y": 291.27567,
    "x": 0.342144,
    "y": 0.147556,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-left-m-target",
    "object": "sw51",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw51.json",
    "sha256": "06a9ddc312a8bea0926ae850261eb341d7e3da0f562cd71bd068edce30a779b6",
    "raw_x": 354.44977,
    "raw_y": 240.04056,
    "x": 0.372321,
    "y": 0.121601,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-right-t-target",
    "object": "sw52",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw52.json",
    "sha256": "062a59bb6ced868815072d96d54015ddf576f7548edccbcbc80d7c08b7c59c1c",
    "raw_x": 641.6916,
    "raw_y": 344.17096,
    "x": 0.674046,
    "y": 0.174352,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-right-a-target",
    "object": "sw53",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw53.json",
    "sha256": "79ce17161ac9084f327a0e7f863ecc4c06f1f3aba71d79e401a61fec5cd14247",
    "raw_x": 609.3804,
    "raw_y": 293.73587,
    "x": 0.640105,
    "y": 0.148802,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.upper-right-c-target",
    "object": "sw54",
    "kind": "HitTarget",
    "file": "gameitems/HitTarget.sw54.json",
    "sha256": "26b04d8102949f7a38bda15fcec338159980bd0113e1cf94dd6ca2fa9d47171e",
    "raw_x": 577.5131,
    "raw_y": 243.63472,
    "x": 0.606631,
    "y": 0.123422,
    "note": "Observed physical standup target center from the script-bound HitTarget; its leaf contact lies behind the target."
  },
  {
    "device": "switch.line-of-death-kill-gen-yagov",
    "object": "sw55",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw55.json",
    "sha256": "04b48297396cb7b7f90c99fed076d3d97b746fa9978063756c364784f1c60e8d",
    "raw_x": 84.65718,
    "raw_y": 343.11734,
    "x": 0.088926,
    "y": 0.173818,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.top-left-loop",
    "object": "sw56",
    "kind": "Gate",
    "file": "gameitems/Gate.sw56.json",
    "sha256": "6731709a3d6ad63ec034c7d3460d1d6804200a883e40e54921e0b5951af82108",
    "raw_x": 210.95859,
    "raw_y": 301.76758,
    "x": 0.221595,
    "y": 0.152871,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-slingshot",
    "object": "LeftSlingShot",
    "kind": "Wall",
    "file": "gameitems/Wall.LeftSlingShot.json",
    "sha256": "1c5018fb0caafd321280f69a131f5e67eb8015ecce350a7da11aedd9166c7caa",
    "raw_x": 193.45966,
    "raw_y": 1394.0679625,
    "x": 0.203214,
    "y": 0.706215,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-slingshot",
    "object": "RightSlingShot",
    "kind": "Wall",
    "file": "gameitems/Wall.RightSlingShot.json",
    "sha256": "2b0306077baddd48b1f7c73bfd03cdf418d392d0689b33131f4db8fccd569003",
    "raw_x": 669.8747025,
    "raw_y": 1393.6700125,
    "x": 0.70365,
    "y": 0.706013,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-flipper-return",
    "object": "sw59",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw59.json",
    "sha256": "6dc1ef4ca1458ef05ef004d1d2c7ecd9374f4a8686c7ba08999b8b57f7478403",
    "raw_x": 118.74096,
    "raw_y": 1391.2539,
    "x": 0.124728,
    "y": 0.704789,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-flipper-return",
    "object": "sw60",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw60.json",
    "sha256": "9d43685d69745a22bb77d51a62f0ba3bcbba0fc231a561d708f6cf5bb745f079",
    "raw_x": 742.41907,
    "raw_y": 1393.3807,
    "x": 0.779852,
    "y": 0.705867,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.left-drain-rescue-kickback",
    "object": "sw61",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw61.json",
    "sha256": "6ae791d6366f8e2233938103f215666c1a256a3c25ff17904ddcae34946bf162",
    "raw_x": 54.38269,
    "raw_y": 1538.6794,
    "x": 0.057125,
    "y": 0.779473,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "switch.right-drain",
    "object": "sw62",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw62.json",
    "sha256": "1f70ec276cb0e86718546e1f2b4954682d9ae62b5d13b042fcad0368d47670ad",
    "raw_x": 808.372,
    "raw_y": 1439.3887,
    "x": 0.84913,
    "y": 0.729174,
    "note": "Observed table contact/event anchor, projected onto the playfield plane; not a measured leaf-blade or under-playfield contact center."
  },
  {
    "device": "device.outhole-kicker",
    "object": "sw10",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw10.json",
    "sha256": "1f24ba61e58443e35bf4290530787ca4b64dad1f332c7b49bbc06c3a984d9282",
    "raw_x": 475.19644,
    "raw_y": 1890.1433,
    "x": 0.499156,
    "y": 0.957519,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.ball-shooter-lane-feeder",
    "object": "sw11",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw11.json",
    "sha256": "f1b97d2dbf7fb9b65e6cb79d2a4aafa961d3b94960eeca0445571ab99fb11107",
    "raw_x": 802.5394,
    "raw_y": 1700.1243,
    "x": 0.843004,
    "y": 0.861259,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.ball-popper-launch-up-kicker",
    "object": "sw24",
    "kind": "Kicker",
    "file": "gameitems/Kicker.sw24.json",
    "sha256": "f3967b7d3846f646b3e920c1724ec47483dfdb3e40183731f781a2664589fb42",
    "raw_x": 858.929,
    "raw_y": 70.41359,
    "x": 0.902236,
    "y": 0.035671,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.center-right-eject",
    "object": "sw23",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw23.json",
    "sha256": "ceb83ee4f58d2e8fbc7c3c5952615a01d6894d3029a00baa4911205654c295fc",
    "raw_x": 513.7195,
    "raw_y": 775.35004,
    "x": 0.539621,
    "y": 0.392781,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.right-eject",
    "object": "sw21",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw21.json",
    "sha256": "b0cbe3192da73039a94978789f96bc1a956d2df410280ceb7f57b345051c9de7",
    "raw_x": 895.01276,
    "raw_y": 1022.808,
    "x": 0.940139,
    "y": 0.51814,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.center-left-eject",
    "object": "sw22",
    "kind": "Trigger",
    "file": "gameitems/Trigger.sw22.json",
    "sha256": "600282f6d85f68a400ea276ad606007817fd01fd54b75eed3555596bb2c85d80",
    "raw_x": 405.53433,
    "raw_y": 760.2239,
    "x": 0.425981,
    "y": 0.385118,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.line-of-death-kickback-yagov-kicker",
    "object": "LODkick",
    "kind": "Kicker",
    "file": "gameitems/Kicker.LODkick.json",
    "sha256": "2438e58806e5e323148fdd117f230954e3b229a8f7556cc1cb667c81396d39d6",
    "raw_x": 84.51501,
    "raw_y": 300.59494,
    "x": 0.088776,
    "y": 0.152277,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.rescue-kickback-left-outlane",
    "object": "LaserKick",
    "kind": "Kicker",
    "file": "gameitems/Kicker.LaserKick.json",
    "sha256": "f3ea2c811423a43f54b44305077bae8b425370c3aa64d341e8d638d31bba7c99",
    "raw_x": 53.729073,
    "raw_y": 1552.1558,
    "x": 0.056438,
    "y": 0.7863,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.left-slingshot",
    "object": "LeftSlingShot",
    "kind": "Wall",
    "file": "gameitems/Wall.LeftSlingShot.json",
    "sha256": "1c5018fb0caafd321280f69a131f5e67eb8015ecce350a7da11aedd9166c7caa",
    "raw_x": 193.45966,
    "raw_y": 1394.0679625,
    "x": 0.203214,
    "y": 0.706215,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.right-slingshot",
    "object": "RightSlingShot",
    "kind": "Wall",
    "file": "gameitems/Wall.RightSlingShot.json",
    "sha256": "2b0306077baddd48b1f7c73bfd03cdf418d392d0689b33131f4db8fccd569003",
    "raw_x": 669.8747025,
    "raw_y": 1393.6700125,
    "x": 0.70365,
    "y": 0.706013,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "device.jet-bumper",
    "object": "Bumper1",
    "kind": "Bumper",
    "file": "gameitems/Bumper.Bumper1.json",
    "sha256": "7eecce806dfc8872438c5749298ac5b151bfbea4d7929da7df514a333019fb8b",
    "raw_x": 465.5134,
    "raw_y": 643.65234,
    "x": 0.488985,
    "y": 0.326065,
    "note": "Disclosed assembly projection: the coil is below the named kicker, bumper or slingshot; this is a physical mechanism anchor, not a measured winding center."
  },
  {
    "device": "lamp.lock-top-ramp",
    "object": "pfil57",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil57.json",
    "sha256": "20360498cd94b0cce487981ba968ba37614b029c36656d041de50d623500b028",
    "raw_x": 114.61102,
    "raw_y": 284.16757,
    "x": 0.12039,
    "y": 0.143955,
    "mesh_bounds": {
      "name": "pfil57",
      "min": [
        109.751,
        283.16757,
        -164.67651
      ],
      "max": [
        119.47104,
        285.16757,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        114.61102,
        284.16757,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "lamp.lock-middle-ramp",
    "object": "pfil58",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil58.json",
    "sha256": "a4af5ab5600a97cf8e3c37fffe7b338520f1fdd9659138fc9e966bd551503356",
    "raw_x": 115.722448,
    "raw_y": 444.35266,
    "x": 0.121557,
    "y": 0.225103,
    "mesh_bounds": {
      "name": "pfil58",
      "min": [
        110.86243,
        443.35266,
        -164.67651
      ],
      "max": [
        120.582466,
        445.35266,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        115.722448,
        444.35266,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "lamp.lock-lower-ramp",
    "object": "pfil59",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil59.json",
    "sha256": "697f4f8e917eb83f7d3e24871ef7d40772e19ea6b3cc750e81227b1afe96b714",
    "raw_x": 114.30927,
    "raw_y": 603.09644,
    "x": 0.120073,
    "y": 0.30552,
    "mesh_bounds": {
      "name": "pfil59",
      "min": [
        109.44925,
        602.09644,
        -164.67651
      ],
      "max": [
        119.16929,
        604.09644,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        114.30927,
        603.09644,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "lamp.landing-top-ramp",
    "object": "pfil60",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil60.json",
    "sha256": "ade1dbbca70b48c0b5a876ef00dee238a9231afacd348b0482dfd2a6e0602e74",
    "raw_x": 114.70797999999999,
    "raw_y": 251.17955,
    "x": 0.120492,
    "y": 0.127244,
    "mesh_bounds": {
      "name": "pfil60",
      "min": [
        109.84796,
        250.17955,
        -164.67651
      ],
      "max": [
        119.568,
        252.17955,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        114.70797999999999,
        251.17955,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "lamp.landing-middle-ramp",
    "object": "pfil61",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil61.json",
    "sha256": "21c6fe813dc6c6ea77a5bd98ade9b62f436b2fc59f24140ac9ee380e761f93ee",
    "raw_x": 115.80524,
    "raw_y": 417.21622,
    "x": 0.121644,
    "y": 0.211356,
    "mesh_bounds": {
      "name": "pfil61",
      "min": [
        110.94522,
        416.21622,
        -164.67651
      ],
      "max": [
        120.66526,
        418.21622,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        115.80524,
        417.21622,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "lamp.landing-lower-ramp",
    "object": "pfil62",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pfil62.json",
    "sha256": "8e26c3943cfc3e9a9a3a50935ebbce9314fff3e1c530e16473649a28c991f004",
    "raw_x": 114.56046,
    "raw_y": 573.064,
    "x": 0.120337,
    "y": 0.290306,
    "mesh_bounds": {
      "name": "pfil62",
      "min": [
        109.70044,
        572.064,
        -164.67651
      ],
      "max": [
        119.42048,
        574.064,
        -148.35658
      ],
      "vertices": 160,
      "center": [
        114.56046,
        573.064,
        -156.516545
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "World-space filament bounds checked against the independently positioned light and bulb envelope; not the primitive origin."
  },
  {
    "device": "device.flasher-9-top-blue",
    "object": "Flasherbase1",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase1.json",
    "sha256": "7bf222a87b3bc0e514f90a3b16bf30443430356ba7f8a484f195235ddaae5e9d",
    "raw_x": 523.6186,
    "raw_y": 171.48221,
    "x": 0.55002,
    "y": 0.08687,
    "mesh_bounds": {
      "name": "Flasherbase1",
      "min": [
        469.6396,
        143.8822,
        -125.552666
      ],
      "max": [
        577.4663,
        199.08221,
        -74.862
      ],
      "vertices": 203,
      "center": [
        523.55295,
        171.48220500000002,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed socket/dome of the retained pre-SS41 four-dome geometry. The post-update circuit population differs as disclosed; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-10-top-right-red",
    "object": "Flasherbase2",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase2.json",
    "sha256": "f1326507cdf2d7e98c8e70245dd4337cc212bd629fe90c6459ca53bafcd41e6f",
    "raw_x": 624.1727,
    "raw_y": 284.75162,
    "x": 0.655644,
    "y": 0.144251,
    "mesh_bounds": {
      "name": "Flasherbase2",
      "min": [
        588.7987,
        237.31673,
        -125.552666
      ],
      "max": [
        659.4646,
        332.07825,
        -74.862
      ],
      "vertices": 203,
      "center": [
        624.13165,
        284.69749,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed socket/dome of the retained pre-SS41 four-dome geometry. The post-update circuit population differs as disclosed; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-1c-yagov-white",
    "object": "Flasherbase4",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase4.json",
    "sha256": "4ddea2121c353266956dc8ddac211e9a33121f666d9c081da547ad1ca371a120",
    "raw_x": 48.744755,
    "raw_y": 786.6675,
    "x": 0.051202,
    "y": 0.398514,
    "mesh_bounds": {
      "name": "Flasherbase4",
      "min": [
        21.203844,
        732.7192,
        -100.552666
      ],
      "max": [
        76.28565,
        840.7506,
        -49.862
      ],
      "vertices": 203,
      "center": [
        48.744747000000004,
        786.7348999999999,
        -75.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-1c-yagov-white",
    "object": "Flasherbase10",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase10.json",
    "sha256": "5a9ae5540ec02e83096018a7f2ffd9662d7fdb0cc9ea694999578d5f6b895cf8",
    "raw_x": 789.0739,
    "raw_y": -24.554413,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-2c-left-lane",
    "object": "Flasherbase8",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase8.json",
    "sha256": "029c2954274fd6ea7fb8c5bcc0a9e4f8c983f30a80bf3d444f8786e36e4f6c7e",
    "raw_x": 705.1084,
    "raw_y": -23.896719,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-2c-left-lane",
    "object": "pFiliment02c",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pFiliment02c.json",
    "sha256": "92b1ff47bc1468d6cf8ae5ba81cc5c855d4adb44e1bd49fb0a3007ee31d12c28",
    "raw_x": 140.548315,
    "raw_y": 1531.4605000000001,
    "x": 0.147635,
    "y": 0.775816,
    "mesh_bounds": {
      "name": "pFiliment02c",
      "min": [
        131.90828,
        1529.8605,
        -23.353016
      ],
      "max": [
        149.18835,
        1533.0605,
        9.28683
      ],
      "vertices": 160,
      "center": [
        140.548315,
        1531.4605000000001,
        -7.033093
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-3c-right-lane",
    "object": "Flasherbase7",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase7.json",
    "sha256": "3d21fcf9fdb0a937847048427789286a39103b60154a3ec90938a578e2c7160b",
    "raw_x": 625.93835,
    "raw_y": -23.526768,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-3c-right-lane",
    "object": "pFiliment03c",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pFiliment03c.json",
    "sha256": "76affe1caf568e1901abd21b671ac23e707ac8089b796dc19e8b8f4e84a73c39",
    "raw_x": 725.279035,
    "raw_y": 1524.79265,
    "x": 0.761848,
    "y": 0.772438,
    "mesh_bounds": {
      "name": "pFiliment03c",
      "min": [
        716.639,
        1523.1926,
        -23.353016
      ],
      "max": [
        733.91907,
        1526.3927,
        9.28683
      ],
      "vertices": 160,
      "center": [
        725.279035,
        1524.79265,
        -7.033093
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-4c-bottom-red",
    "object": "Flasherbase6",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase6.json",
    "sha256": "52d33e4de2cd192ba7b07774ca424e03f479003e005ca8ebc167e6f065a470d6",
    "raw_x": 545.7165,
    "raw_y": -23.214615,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-4c-bottom-red",
    "object": "Flasherbase14",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase14.json",
    "sha256": "96ad32b5cc7993e0c1ccca157f05ade344d8b67a9678eda542a4c653f23163e9",
    "raw_x": 831.83966,
    "raw_y": 1153.4113,
    "x": 0.873781,
    "y": 0.584302,
    "mesh_bounds": {
      "name": "Flasherbase14",
      "min": [
        804.2491,
        1100.2808,
        -125.552666
      ],
      "max": [
        859.43024,
        1206.4137,
        -74.862
      ],
      "vertices": 203,
      "center": [
        831.8396700000001,
        1153.34725,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-5c-bottom-white",
    "object": "Flasherbase5",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase5.json",
    "sha256": "bf75e71bf5ee857020b0301237f3e6d6374de189b11db86104365207cb28ffb3",
    "raw_x": 461.43622,
    "raw_y": -22.161144,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-5c-bottom-white",
    "object": "Flasherbase13",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase13.json",
    "sha256": "758a6e566e4d668872166aeeb19fcf1298914b31b121ad3739c80834cda81659",
    "raw_x": 822.23785,
    "raw_y": 1053.8524,
    "x": 0.863695,
    "y": 0.533866,
    "mesh_bounds": {
      "name": "Flasherbase13",
      "min": [
        794.6696,
        1000.96643,
        -125.552666
      ],
      "max": [
        849.8061,
        1106.6118,
        -74.862
      ],
      "vertices": 203,
      "center": [
        822.23785,
        1053.789115,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-6c-bottom-blue",
    "object": "Flasherbase11",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase11.json",
    "sha256": "94775198225f612b2bf434b4067232e05ac9970a4fec57e8d58bfd88f2455346",
    "raw_x": 379.65845,
    "raw_y": -22.753736,
    "excluded": "Outside playfield plane/frame; retained for audit, not clamped or emitted as a canonical placement."
  },
  {
    "device": "device.flasher-6c-bottom-blue",
    "object": "Flasherbase12",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase12.json",
    "sha256": "5f78fe9de98bd65977c816c5b52508446108e8802dfe1e3ba054ac7c4c727a48",
    "raw_x": 817.11127,
    "raw_y": 955.53455,
    "x": 0.85831,
    "y": 0.48406,
    "mesh_bounds": {
      "name": "Flasherbase12",
      "min": [
        778.9465,
        909.8601,
        -125.552666
      ],
      "max": [
        855.1857,
        1001.1066,
        -74.862
      ],
      "vertices": 203,
      "center": [
        817.0661,
        955.48335,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed physical socket/dome in the retained geometry. SS41 does not change this circuit; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-7c-top-white-top-red-left",
    "object": "Flasherbase3",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase3.json",
    "sha256": "6b215a0fa9351767b1883ba081a5d5354950449d6581ad9203ff6d42edda6d45",
    "raw_x": 295.87152,
    "raw_y": 290.16217,
    "x": 0.310789,
    "y": 0.146992,
    "mesh_bounds": {
      "name": "Flasherbase3",
      "min": [
        268.31592,
        235.82803,
        -125.552666
      ],
      "max": [
        323.42712,
        344.63144,
        -74.862
      ],
      "vertices": 203,
      "center": [
        295.87152000000003,
        290.229735,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed socket/dome of the retained pre-SS41 four-dome geometry. The post-update circuit population differs as disclosed; no backbox bulb is projected here."
  },
  {
    "device": "device.flasher-7c-top-white-top-red-left",
    "object": "Flasherbase9",
    "kind": "Primitive",
    "file": "gameitems/Primitive.Flasherbase9.json",
    "sha256": "ade463f2f26e41d4f99ccabb40569822dc624d7baad05c984271b5d98f3c64cc",
    "raw_x": 640.7093,
    "raw_y": 143.0627,
    "x": 0.673014,
    "y": 0.072474,
    "mesh_bounds": {
      "name": "Flasherbase9",
      "min": [
        588.8468,
        115.56772,
        -125.552666
      ],
      "max": [
        692.4423,
        170.55768,
        -74.862
      ],
      "vertices": 203,
      "center": [
        640.64455,
        143.0627,
        -100.207333
      ]
    },
    "point_method": "stored Flupper base center, independently checked against world mesh bounds",
    "note": "Observed socket/dome of the retained pre-SS41 four-dome geometry. The post-update circuit population differs as disclosed; no backbox bulb is projected here."
  },
  {
    "device": "device.upper-diverter-launch-ramp",
    "object": "pDiverter1",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pDiverter1.json",
    "sha256": "54efed711f4c60eee2ce2ec0f78fee75b54231759bbdb9bf8025d214511775ac",
    "raw_x": 23.234579500000002,
    "raw_y": 291.83474,
    "x": 0.024406,
    "y": 0.147839,
    "mesh_bounds": {
      "name": "pDiverter1",
      "min": [
        9.234579,
        230.2747,
        -143.72018
      ],
      "max": [
        37.23458,
        353.39478,
        -115.720184
      ],
      "vertices": 1458,
      "center": [
        23.234579500000002,
        291.83474,
        -129.720182
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Physical gate-arm world-mesh bounds provide an observed assembly projection; no off-playfield animation pivot is used."
  },
  {
    "device": "device.lower-diverter-launch-ramp",
    "object": "pDiverter2",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pDiverter2.json",
    "sha256": "9fd15cded390b44a3df4eda5d1f9453ef6fe462ac26b21d1ea7677f852bb53d3",
    "raw_x": 22.04882025,
    "raw_y": 449.40360999999996,
    "x": 0.023161,
    "y": 0.227661,
    "mesh_bounds": {
      "name": "pDiverter2",
      "min": [
        8.0488205,
        387.84357,
        -143.72018
      ],
      "max": [
        36.04882,
        510.96365,
        -115.720184
      ],
      "vertices": 1458,
      "center": [
        22.04882025,
        449.40360999999996,
        -129.720182
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Physical gate-arm world-mesh bounds provide an observed assembly projection; no off-playfield animation pivot is used."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb001",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb001.json",
    "sha256": "bf3ab51b2432641d7eae6153e5c9651da9a56b111c764714ab53554a7a1e4863",
    "raw_x": 204.05081,
    "raw_y": 1574.42285,
    "x": 0.214339,
    "y": 0.79758,
    "mesh_bounds": {
      "name": "pBulb001",
      "min": [
        194.56056,
        1564.9325,
        -24.717001
      ],
      "max": [
        213.54106,
        1583.9132,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        204.05081,
        1574.42285,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb002",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb002.json",
    "sha256": "e224f6f9012dfe3b6927ceb86e4d40870571ac1bc176fed31e36806ef7358dca",
    "raw_x": 206.35352,
    "raw_y": 1454.0686,
    "x": 0.216758,
    "y": 0.73661,
    "mesh_bounds": {
      "name": "pBulb002",
      "min": [
        196.86327,
        1444.5782,
        -24.717001
      ],
      "max": [
        215.84377,
        1463.559,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        206.35352,
        1454.0686,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb003",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb003.json",
    "sha256": "3f8eac475f700c2158fca39a10de89aed245ac6941acaadb2ed857a6f6c93e0c",
    "raw_x": 170.30678,
    "raw_y": 1314.20725,
    "x": 0.178894,
    "y": 0.665758,
    "mesh_bounds": {
      "name": "pBulb003",
      "min": [
        160.81653,
        1304.7169,
        -24.717001
      ],
      "max": [
        179.79703,
        1323.6976,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        170.30678,
        1314.20725,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb004",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb004.json",
    "sha256": "a4d125e9bafb9e5aaa25ee7000df6b5868942cac68e154599d210a2acacde079",
    "raw_x": 39.3850365,
    "raw_y": 830.316165,
    "x": 0.041371,
    "y": 0.420626,
    "mesh_bounds": {
      "name": "pBulb004",
      "min": [
        29.894787,
        820.82587,
        -24.717001
      ],
      "max": [
        48.875286,
        839.80646,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        39.3850365,
        830.316165,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb005",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb005.json",
    "sha256": "90766725c5e1747542eedad57ef248dcd3e3c9833ad785b6a9850d48032497a7",
    "raw_x": 161.94392,
    "raw_y": 523.4861450000001,
    "x": 0.170109,
    "y": 0.265191,
    "mesh_bounds": {
      "name": "pBulb005",
      "min": [
        152.45367,
        513.99585,
        -24.717001
      ],
      "max": [
        171.43417,
        532.97644,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        161.94392,
        523.4861450000001,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb006",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb006.json",
    "sha256": "d9b17dfb5f53f9a8f8448444d2432a6c0a6775ef564b11265a055f4ec4057abf",
    "raw_x": 146.66014,
    "raw_y": 395.1598,
    "x": 0.154055,
    "y": 0.200182,
    "mesh_bounds": {
      "name": "pBulb006",
      "min": [
        137.16989,
        385.6695,
        -24.717001
      ],
      "max": [
        156.15039,
        404.6501,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        146.66014,
        395.1598,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb007",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb007.json",
    "sha256": "ce1728a32e4b12411a8bb0c10c789e4e6343e72a4ec80a50e9e0ee61227e4d66",
    "raw_x": 248.87164,
    "raw_y": 298.328035,
    "x": 0.26142,
    "y": 0.151129,
    "mesh_bounds": {
      "name": "pBulb007",
      "min": [
        239.3814,
        288.83774,
        -24.717001
      ],
      "max": [
        258.36188,
        307.81833,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        248.87164,
        298.328035,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb008",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb008.json",
    "sha256": "5b34a8961d0c5c4c0dc3f47c9da4511b59fb047a71a7bb59b91a472f3c740569",
    "raw_x": 605.99933,
    "raw_y": 210.526075,
    "x": 0.636554,
    "y": 0.106649,
    "mesh_bounds": {
      "name": "pBulb008",
      "min": [
        596.5091,
        201.03578,
        -24.717001
      ],
      "max": [
        615.48956,
        220.01637,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        605.99933,
        210.526075,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb009",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb009.json",
    "sha256": "87c91c11ca92d1a64381fdb1e9339eeb9f0c6397f17edd6bb7a6033d191d554d",
    "raw_x": 307.28438,
    "raw_y": 113.707038,
    "x": 0.322778,
    "y": 0.057602,
    "mesh_bounds": {
      "name": "pBulb009",
      "min": [
        297.79413,
        104.216736,
        -24.717001
      ],
      "max": [
        316.77463,
        123.19734,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        307.28438,
        113.707038,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb010",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb010.json",
    "sha256": "36811aaa9cef1c414aaa7cde56e0919fe4a57beb72646cacd05094a2e4336f0e",
    "raw_x": 489.0941,
    "raw_y": 154.293275,
    "x": 0.513754,
    "y": 0.078163,
    "mesh_bounds": {
      "name": "pBulb010",
      "min": [
        479.60385,
        144.80298,
        -24.717001
      ],
      "max": [
        498.58435,
        163.78357,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        489.0941,
        154.293275,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb011",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb011.json",
    "sha256": "c7e12db7d0a0ffac4c062c40c826d47a3cee1e323b35f4d7dd4cc2482f38de2f",
    "raw_x": 325.82167,
    "raw_y": 209.046265,
    "x": 0.34225,
    "y": 0.1059,
    "mesh_bounds": {
      "name": "pBulb011",
      "min": [
        316.33142,
        199.55597,
        -24.717001
      ],
      "max": [
        335.31192,
        218.53656,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        325.82167,
        209.046265,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb012",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb012.json",
    "sha256": "84e7df3ee5bc7751a85ee1bba6f57e464dd3945c4d9b5e1b6aa0fa5f7aa1bec8",
    "raw_x": 510.20495,
    "raw_y": 51.966831,
    "x": 0.53593,
    "y": 0.026326,
    "mesh_bounds": {
      "name": "pBulb012",
      "min": [
        500.7147,
        42.476532,
        -24.717001
      ],
      "max": [
        519.6952,
        61.45713,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        510.20495,
        51.966831,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb013",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb013.json",
    "sha256": "c3670709f9bc75c2d3bb8978e0d093a7df399ab73f9146f9bba7d1c1914701d1",
    "raw_x": 248.93828000000002,
    "raw_y": 124.060282,
    "x": 0.26149,
    "y": 0.062847,
    "mesh_bounds": {
      "name": "pBulb013",
      "min": [
        239.44803,
        114.569984,
        -24.717001
      ],
      "max": [
        258.42853,
        133.55058,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        248.93828000000002,
        124.060282,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb014",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb014.json",
    "sha256": "32fe65d977b4041adf5856dbdbb27224d0e88a161cce7b63bf3db7b745f46f83",
    "raw_x": 348.71555,
    "raw_y": 57.734269999999995,
    "x": 0.366298,
    "y": 0.029247,
    "mesh_bounds": {
      "name": "pBulb014",
      "min": [
        339.2253,
        48.24397,
        -24.717001
      ],
      "max": [
        358.2058,
        67.22457,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        348.71555,
        57.734269999999995,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb015",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb015.json",
    "sha256": "953fbdccccf9c6c27aea1cd5d6b2472832700f46e38b180024524a5c77d66ced",
    "raw_x": 427.73003,
    "raw_y": 54.850519,
    "x": 0.449296,
    "y": 0.027786,
    "mesh_bounds": {
      "name": "pBulb015",
      "min": [
        418.23978,
        45.360218,
        -24.717001
      ],
      "max": [
        437.22028,
        64.34082,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        427.73003,
        54.850519,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb016",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb016.json",
    "sha256": "116b4770002f2c4aa59e6400a9dfee8f3bf1ec686a62918d8ac27255bd5929f2",
    "raw_x": 137.62592,
    "raw_y": 265.363465,
    "x": 0.144565,
    "y": 0.134429,
    "mesh_bounds": {
      "name": "pBulb016",
      "min": [
        128.13567,
        255.87317,
        -24.717001
      ],
      "max": [
        147.11617,
        274.85376,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        137.62592,
        265.363465,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb017",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb017.json",
    "sha256": "514144fb9abf309234daa6a9fbc405b85f047ed873c1c8c26feaf9a1dd3e065b",
    "raw_x": 754.7459249999999,
    "raw_y": 49.083121500000004,
    "x": 0.7928,
    "y": 0.024865,
    "mesh_bounds": {
      "name": "pBulb017",
      "min": [
        745.2557,
        39.592823,
        -24.717001
      ],
      "max": [
        764.23615,
        58.57342,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        754.7459249999999,
        49.083121500000004,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb018",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb018.json",
    "sha256": "b5d6bf496600ef16974c778723bab5943fce5bbfb7d4911150426ced82bfa618",
    "raw_x": 825.68597,
    "raw_y": 248.061,
    "x": 0.867317,
    "y": 0.125664,
    "mesh_bounds": {
      "name": "pBulb018",
      "min": [
        816.19574,
        238.5707,
        -24.717001
      ],
      "max": [
        835.1762,
        257.5513,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        825.68597,
        248.061,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb019",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb019.json",
    "sha256": "dcc5231d28cbd93a5cff32365333ece064d7d649563cebac5deed767c99d0954",
    "raw_x": 912.24275,
    "raw_y": 576.378355,
    "x": 0.958238,
    "y": 0.291985,
    "mesh_bounds": {
      "name": "pBulb019",
      "min": [
        902.7525,
        566.88806,
        -24.717001
      ],
      "max": [
        921.733,
        585.86865,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        912.24275,
        576.378355,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb020",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb020.json",
    "sha256": "81eb7611ead326ba5d145131ba766b2d39ceb0693e300ee94f1e4393aa14a5d9",
    "raw_x": 802.616075,
    "raw_y": 386.48053,
    "x": 0.843084,
    "y": 0.195785,
    "mesh_bounds": {
      "name": "pBulb020",
      "min": [
        793.12585,
        376.99023,
        -24.717001
      ],
      "max": [
        812.1063,
        395.97083,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        802.616075,
        386.48053,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb021",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb021.json",
    "sha256": "7d3fcff2098d0dd89bff781cee99c31300fdbc6aea26cd8122307be545b8bf62",
    "raw_x": 912.2428500000001,
    "raw_y": 649.629015,
    "x": 0.958238,
    "y": 0.329093,
    "mesh_bounds": {
      "name": "pBulb021",
      "min": [
        902.7526,
        640.13873,
        -24.717001
      ],
      "max": [
        921.7331,
        659.1193,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        912.2428500000001,
        649.629015,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb024",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb024.json",
    "sha256": "0d7ebd68f29b870b526c8ad82e66667c5c368c7ac5eb08e7010f7f1b70db4f68",
    "raw_x": 850.5227649999999,
    "raw_y": 1006.7484,
    "x": 0.893406,
    "y": 0.510004,
    "mesh_bounds": {
      "name": "pBulb024",
      "min": [
        841.03253,
        997.2581,
        -24.717001
      ],
      "max": [
        860.013,
        1016.2387,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        850.5227649999999,
        1006.7484,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb025",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb025.json",
    "sha256": "4cfd811b474ad91a2f0a3605610998194ae6c685d30444b465a4004beffc5f70",
    "raw_x": 695.95415,
    "raw_y": 1314.7318500000001,
    "x": 0.731044,
    "y": 0.666024,
    "mesh_bounds": {
      "name": "pBulb025",
      "min": [
        686.4639,
        1305.2415,
        -24.717001
      ],
      "max": [
        705.4444,
        1324.2222,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        695.95415,
        1314.7318500000001,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb026",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb026.json",
    "sha256": "6342eef620fc2735c3cb8c63b1353ee13d2319880fb9456bc427b335c7229482",
    "raw_x": 661.349365,
    "raw_y": 1446.80675,
    "x": 0.694695,
    "y": 0.732931,
    "mesh_bounds": {
      "name": "pBulb026",
      "min": [
        651.85913,
        1437.3164,
        -24.717001
      ],
      "max": [
        670.8396,
        1456.2971,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        661.349365,
        1446.80675,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "pBulb027",
    "kind": "Primitive",
    "file": "gameitems/Primitive.pBulb027.json",
    "sha256": "b57accc746ac30426f809c35a693642cb98dcea552698e004340365217b78726",
    "raw_x": 658.771125,
    "raw_y": 1576.0459,
    "x": 0.691986,
    "y": 0.798402,
    "mesh_bounds": {
      "name": "pBulb027",
      "min": [
        649.2809,
        1566.5555,
        -24.717001
      ],
      "max": [
        668.26135,
        1585.5363,
        4.9958005
      ],
      "vertices": 261,
      "center": [
        658.771125,
        1576.0459,
        -9.860600250000001
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  },
  {
    "device": "device.general-illumination-relay",
    "object": "bumperbulb1",
    "kind": "Primitive",
    "file": "gameitems/Primitive.bumperbulb1.json",
    "sha256": "965cd42a73b540fd8db0a98601aa538c2ea2706bec57f0d63ce03c94c97aa456",
    "raw_x": 465.19687,
    "raw_y": 642.8138,
    "x": 0.488652,
    "y": 0.32564,
    "mesh_bounds": {
      "name": "bumperbulb1",
      "min": [
        453.51627,
        631.1332,
        -71.247955
      ],
      "max": [
        476.87747,
        654.4944,
        -36.48414
      ],
      "vertices": 159,
      "center": [
        465.19687,
        642.8138,
        -53.8660475
      ]
    },
    "point_method": "world_mesh_bounds_center",
    "note": "Observed individual modelled GI bulb envelope; a subset, not a complete hardware socket census. No helper count is promoted to quantity."
  }
]
```
