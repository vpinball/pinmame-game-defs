# R03 single-coil selector visual readings

Complete compact reading of the retained successful run. This JSON block preserves every selector, name, public transition and source-frame identity. It normalizes CRLF to LF; the external original summary SHA-256 is 54e22973c337428abd42d57835290e565d8c14b40df0585b9164818eb60a5a80. The raw run remains pinned independently.

```json
{
  "game": "mystcasa",
  "method": "Runtime reviewer visually read retained R03 DMD snapshot names/numbers and paired each with same-step public solenoid transitions. Not OCR-derived; no negative runtime observation establishes physical non-fitment.",
  "source_run_sha256": "ee137a0ba7dcbd7da9699d7e3c6860f76f7463d9726ac75788527d44507590c2",
  "scenario_sha256": "04b99d6e83af087e6de96ad95ed33f925327d53574539395328932c1ecd10f86",
  "adapter_sha256": "7cb963d1adf3f9fd2714ab4976707d3e013180ea74db3eb65ef51897f5f7d64f",
  "library_sha256": "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead",
  "rom_archive_sha256": "721b2a1027655aab321e74233a37ae5290c308e964419b301901de0b00b3e107",
  "boot_wait_s": 15,
  "keyboard_handling": false,
  "handle_mechanics": 0,
  "clean_state": true,
  "title_checkpoints": [
    "T TESTS",
    "SINGLE COILS"
  ],
  "stabilization_after_each_checkpoint_s": 2,
  "entries": [
    {
      "selector_ordinal": 1,
      "displayed_number": 1,
      "visually_read_name": "SECRET DOOR",
      "public_solenoid": 1,
      "step_label": "fire-selected-1",
      "snapshot": "dmd/008-fire-selected-1-display-0.pgm",
      "file_sha256": "dc6750140b580eec241fc20fb6fbee5d49aa8d86ef3f3a2b37b2edefab853060",
      "pixel_sha256": "c01020bde5b0800ad2509886bc2f25c015cc85a1b777115f3320bc8424c8aa54",
      "observed_transitions": [
        {
          "number": 1,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 2,
      "displayed_number": 2,
      "visually_read_name": "BUMPER LEFT",
      "public_solenoid": 2,
      "step_label": "fire-selected-2",
      "snapshot": "dmd/010-fire-selected-2-display-0.pgm",
      "file_sha256": "70d0c17d8aafb940759617b43e99acad847da9ea2a77553415f9bbdafc73767c",
      "pixel_sha256": "15086c6e185c8fe0ca7d0bb71109b692e485f119ecf473f2757fab09c93e5680",
      "observed_transitions": [
        {
          "number": 2,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 3,
      "displayed_number": 3,
      "visually_read_name": "BUMPER RIGHT",
      "public_solenoid": 3,
      "step_label": "fire-selected-3",
      "snapshot": "dmd/012-fire-selected-3-display-0.pgm",
      "file_sha256": "2a8d6670808db529a9c4f0b686c2689df38cd430674b79a73ec5236afb6e5f21",
      "pixel_sha256": "0ebc14a2ef7fa3951f51571eca1fb58151fbf4cafde9c6b4ae064b32c0af1c5d",
      "observed_transitions": [
        {
          "number": 3,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 4,
      "displayed_number": 4,
      "visually_read_name": "SLING LEFT",
      "public_solenoid": 4,
      "step_label": "fire-selected-4",
      "snapshot": "dmd/014-fire-selected-4-display-0.pgm",
      "file_sha256": "66d8d1f756d23cebe40123593d99b2de5c0556a2321058e2d7bc3d72673d4cc5",
      "pixel_sha256": "8287fd788eb4bc13c80a8b3c2dda8007dd7c85b7532325e80eaae6f368ff0b64",
      "observed_transitions": [
        {
          "number": 4,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 5,
      "displayed_number": 5,
      "visually_read_name": "SLING RIGHT",
      "public_solenoid": 5,
      "step_label": "fire-selected-5",
      "snapshot": "dmd/016-fire-selected-5-display-0.pgm",
      "file_sha256": "ed4cc86c54447b71195b5491fbd7309c2697a638182714ff6603df636da9dbdf",
      "pixel_sha256": "c354620d04d1cb42b5654d0dc9627cda256ad993983a864cff319151cad37004",
      "observed_transitions": [
        {
          "number": 5,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 6,
      "displayed_number": 6,
      "visually_read_name": "MEGAMODE",
      "public_solenoid": 6,
      "step_label": "fire-selected-6",
      "snapshot": "dmd/018-fire-selected-6-display-0.pgm",
      "file_sha256": "356f60456e8c7f053980944832be0962c65a7840984de21d070f091ae2b589c2",
      "pixel_sha256": "18ce217c324aeb4d656586a42373a8a1b508e4841ab285c14e1dcd54af3a6fe6",
      "observed_transitions": [
        {
          "number": 6,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 7,
      "displayed_number": 9,
      "visually_read_name": "PLUNGER",
      "public_solenoid": 9,
      "step_label": "fire-selected-7",
      "snapshot": "dmd/020-fire-selected-7-display-0.pgm",
      "file_sha256": "b17d98fc37db99891003d1a8a520134a9ef540e6ff8fc9d6ff152a7df2bd6191",
      "pixel_sha256": "bb25ea21cfb2016dff88b70469a63bbe1c22a4fe6fdc56e55ec53d802859c04d",
      "observed_transitions": [
        {
          "number": 9,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 8,
      "displayed_number": 10,
      "visually_read_name": "CATAPULT",
      "public_solenoid": 10,
      "step_label": "fire-selected-8",
      "snapshot": "dmd/022-fire-selected-8-display-0.pgm",
      "file_sha256": "6f129edc9a8e9bfea231e72cea904c812b6e9fc9c64aff0bc7591b6bd47c850c",
      "pixel_sha256": "073cacfb2837983566b106c5d76c8395754c2dfc831a198a5521083006051098",
      "observed_transitions": [
        {
          "number": 10,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 9,
      "displayed_number": 11,
      "visually_read_name": "DTS C-A-S",
      "public_solenoid": 11,
      "step_label": "fire-selected-9",
      "snapshot": "dmd/024-fire-selected-9-display-0.pgm",
      "file_sha256": "4de4d6693234b69b358b220fd6266ec098a0cfc42b70ae935951b04b01968b19",
      "pixel_sha256": "dabb7d1095d9989db59456530b437dd9de8aa69f21963b5ce75c06a77246a7a7",
      "observed_transitions": [
        {
          "number": 11,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 10,
      "displayed_number": 12,
      "visually_read_name": "DTS T-L-E",
      "public_solenoid": 12,
      "step_label": "fire-selected-10",
      "snapshot": "dmd/026-fire-selected-10-display-0.pgm",
      "file_sha256": "7abe6647c6e577c70ff1ab772d9809fec96e26f69cba77ad89693aef46bb5b2c",
      "pixel_sha256": "b7beebd938b4d619c5feee8fc65c940941c43955882de804f7c8ab8300eca607",
      "observed_transitions": [
        {
          "number": 12,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 11,
      "displayed_number": 13,
      "visually_read_name": "OUTHOLE",
      "public_solenoid": 13,
      "step_label": "fire-selected-11",
      "snapshot": "dmd/028-fire-selected-11-display-0.pgm",
      "file_sha256": "99715041ea218e586be76182a7869c74e5bcb2c3dbad7e8acfe8aa0319e661d2",
      "pixel_sha256": "262daa30139b73f39a143fb83996ff138f68e6866f1bbe739fb1831a7e219d24",
      "observed_transitions": [
        {
          "number": 13,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 12,
      "displayed_number": 14,
      "visually_read_name": "KNOCKER",
      "public_solenoid": 14,
      "step_label": "fire-selected-12",
      "snapshot": "dmd/030-fire-selected-12-display-0.pgm",
      "file_sha256": "c71e55f2a4c4f42fd832047de1e7073229382f0e9457a7f14661c1d610c4fa42",
      "pixel_sha256": "f1880427b6bb3b39474b4cd1d3ecaafa2c3b1fdebd48fa4307dad225bb0e2d44",
      "observed_transitions": [
        {
          "number": 14,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 13,
      "displayed_number": 15,
      "visually_read_name": "FLASHER RELAY",
      "public_solenoid": 15,
      "step_label": "fire-selected-13",
      "snapshot": "dmd/032-fire-selected-13-display-0.pgm",
      "file_sha256": "c110c444f3d4f5727b1a8c3213cce445dfb2007b84d4726bac5346a47bfde87b",
      "pixel_sha256": "f986ecbc44340afd6ba158fb5ded23e1c3751d3ff54631ebdaa45f80d31e1f6d",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 14,
      "displayed_number": 16,
      "visually_read_name": "FIELD RELAY BOT",
      "public_solenoid": 16,
      "step_label": "fire-selected-14",
      "snapshot": "dmd/034-fire-selected-14-display-0.pgm",
      "file_sha256": "2404afda163a050f6df544265b8bc82b23e3dc7847477f759d663f84eac63ed4",
      "pixel_sha256": "bc53df6a915531b1fc45c3b1a1b6acf7b0be73a23d1589fcd531c6c5d03fb2c4",
      "observed_transitions": [
        {
          "number": 16,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 15,
      "displayed_number": 17,
      "visually_read_name": "FLASHER DUNGEON",
      "public_solenoid": 17,
      "step_label": "fire-selected-15",
      "snapshot": "dmd/036-fire-selected-15-display-0.pgm",
      "file_sha256": "74c22101e2e00f019d50d3fc770f1733ac71323a27d364130053a58f58199ebe",
      "pixel_sha256": "76ae2301df4ab0f42ba48b63e3ac9f2cf3f6bf4a0b223178ad5f42bb1af35769",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 17,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 16,
      "displayed_number": 18,
      "visually_read_name": "FLASHER BRIDGE",
      "public_solenoid": 18,
      "step_label": "fire-selected-16",
      "snapshot": "dmd/038-fire-selected-16-display-0.pgm",
      "file_sha256": "9398f3d6c03569a8587eccbb6b3f8800c8778e62d403469ed71cf95fa23b3dcd",
      "pixel_sha256": "357938dd3486359aaf56b9149ca98e5048d70cc9121e246f7720d49c7e298890",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 18,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 17,
      "displayed_number": 19,
      "visually_read_name": "FLASHER TOWER",
      "public_solenoid": 19,
      "step_label": "fire-selected-17",
      "snapshot": "dmd/040-fire-selected-17-display-0.pgm",
      "file_sha256": "b8cd7b90829d459eb92524df3a56d8b4fc8f43c15ef88527f95e072022a2e207",
      "pixel_sha256": "d54acd593d939031ae7e45604abff2f585555c3f06aeb44140666cf0ff8c2ff5",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 19,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 18,
      "displayed_number": 20,
      "visually_read_name": "FLASHER BALLROOM",
      "public_solenoid": 20,
      "step_label": "fire-selected-18",
      "snapshot": "dmd/042-fire-selected-18-display-0.pgm",
      "file_sha256": "7a559cdc2574317192cb149a9974642324c57e19090a635cd679ccb7b4f3da2e",
      "pixel_sha256": "20b5064df0cd0b850f618f7f8372786823a178fa542d3b08f4641c6495f4fdac",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 20,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 19,
      "displayed_number": 21,
      "visually_read_name": "FLASHER SECRET",
      "public_solenoid": 21,
      "step_label": "fire-selected-19",
      "snapshot": "dmd/044-fire-selected-19-display-0.pgm",
      "file_sha256": "6c7eea2497568153fef4d7ba297d88b6e301047ed26d8ee7aa2d6c788a1c3bd7",
      "pixel_sha256": "053ee74c3639f83a83c622abb2db37248a7aac5703753f4e138b95540fea1f1c",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 21,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 20,
      "displayed_number": 22,
      "visually_read_name": "FLASHER CATWALK",
      "public_solenoid": 22,
      "step_label": "fire-selected-20",
      "snapshot": "dmd/046-fire-selected-20-display-0.pgm",
      "file_sha256": "366dcb27dc8ab08436d36e7360c0567e60379488dc08f6029413b7bb83a1ae70",
      "pixel_sha256": "7c24f34babd25d40425974bdaacb1325800b5d2ba159b0017b806e7d851ca6ff",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 22,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 21,
      "displayed_number": 23,
      "visually_read_name": "FLASHER LOCK",
      "public_solenoid": 23,
      "step_label": "fire-selected-21",
      "snapshot": "dmd/048-fire-selected-21-display-0.pgm",
      "file_sha256": "b014cdbc63eeb0bfcce1d33f51a168b6955421864ac46da093833fd3afc09e7a",
      "pixel_sha256": "1b1779d5fd04d73d1141fe7a72f7b4409a10b4ea51065c04d96d2c8d4bb5b862",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 23,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 22,
      "displayed_number": 24,
      "visually_read_name": "FLASHER BACKBOX",
      "public_solenoid": 24,
      "step_label": "fire-selected-22",
      "snapshot": "dmd/050-fire-selected-22-display-0.pgm",
      "file_sha256": "210be59b62855d63d6214b0174eb4cf15f8a9d54a550e07a5a1f7b08e2daa0a1",
      "pixel_sha256": "db6802985de3dd43eb375bfed40bc751836ab68ceca465d397867cbaaa7fd65d",
      "observed_transitions": [
        {
          "number": 15,
          "states": [
            1,
            0
          ]
        },
        {
          "number": 24,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 23,
      "displayed_number": 26,
      "visually_read_name": "FIELD RELAY TOP",
      "public_solenoid": 26,
      "step_label": "fire-selected-23",
      "snapshot": "dmd/052-fire-selected-23-display-0.pgm",
      "file_sha256": "ca0a1aba26f0fa32826e325a6d82751cbecbf938ec07214274f0a3707024df88",
      "pixel_sha256": "580ce0213627aec754fc8dbcf8bd8fcbdaf71fb6698ce28394c3c64c6588b8ff",
      "observed_transitions": [
        {
          "number": 26,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 24,
      "displayed_number": 27,
      "visually_read_name": "FLIPPER RELAY",
      "public_solenoid": 27,
      "step_label": "fire-selected-24",
      "snapshot": "dmd/054-fire-selected-24-display-0.pgm",
      "file_sha256": "7ca0c05cacf6a59f094f89a31ae506555aee6c15fcfc53be23a4f8c4fb8cc3d1",
      "pixel_sha256": "930815608ab8ed2a8b9ea2984f9033957ee1a6cafaf9e1f056d21494d44ee42e",
      "observed_transitions": [
        {
          "number": 27,
          "states": [
            1
          ]
        }
      ]
    },
    {
      "selector_ordinal": 25,
      "displayed_number": 29,
      "visually_read_name": "BACK RELAY NORM",
      "public_solenoid": 29,
      "step_label": "fire-selected-25",
      "snapshot": "dmd/056-fire-selected-25-display-0.pgm",
      "file_sha256": "b19bd15a4510fc37888a7948fb21c90cb19147dd2952d659cd82ed6b5f4dfd19",
      "pixel_sha256": "ffea2267fd7322bf43adc9d2c1599afbe187ea8854dfa52120e9769bb92bd18b",
      "observed_transitions": [
        {
          "number": 27,
          "states": [
            0
          ]
        },
        {
          "number": 29,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 26,
      "displayed_number": 30,
      "visually_read_name": "EJECT 2 PLAYFIELD",
      "public_solenoid": 30,
      "step_label": "fire-selected-26",
      "snapshot": "dmd/058-fire-selected-26-display-0.pgm",
      "file_sha256": "42c95472a1a6cd57fe00d6b41c30e0ec9f47366bb4ce552ecb9e49ddd200a1d9",
      "pixel_sha256": "19ba9e2cb37a3c2b8a16e8ce97c1c44f009a2b45f9bf6a8fb16ebb0b66636586",
      "observed_transitions": [
        {
          "number": 30,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 27,
      "displayed_number": 31,
      "visually_read_name": "BACK RELAY DOOM",
      "public_solenoid": 31,
      "step_label": "fire-selected-27",
      "snapshot": "dmd/060-fire-selected-27-display-0.pgm",
      "file_sha256": "b266a46154a1b3649437bb0c9c39f1699c26761265849aaf8b162ef790ceb1c8",
      "pixel_sha256": "3faab6f21c2f065c50c34c39a84be3aa7b984bf61a2e9bdbbe679e36b3a92342",
      "observed_transitions": [
        {
          "number": 31,
          "states": [
            1,
            0
          ]
        }
      ]
    },
    {
      "selector_ordinal": 28,
      "displayed_number": 32,
      "visually_read_name": "GATE",
      "public_solenoid": 32,
      "step_label": "fire-selected-28",
      "snapshot": "dmd/062-fire-selected-28-display-0.pgm",
      "file_sha256": "d5c033ac15e778cf204023b869f2097ff01c8e18c69aac3743cd1527c95ba788",
      "pixel_sha256": "2c915bbf8e832626617a8c04277644ededc8454bd134a216963244885a518e24",
      "observed_transitions": [
        {
          "number": 32,
          "states": [
            1,
            0
          ]
        }
      ]
    }
  ],
  "conclusions": [
    "The28named selectors wrap from32to01 and skip7,8,25,28. All28publicoutputs paired with displayed number.",
    "Flasher selectors17-24 also pulse flasher relay15.",
    "16is namedFIELD RELAY BOT and26FIELD RELAY TOP byR03; this agrees withprintedcoiltable but does not override physical wiring DOC-002.",
    "Public27relay washeldafterselectedfire; releasing occurredatnexttestfire.",
    "Public7,8,25,28notselected in fullwrap; completefactoryloadschematic needed separately to substantiate unfittedstatus."
  ]
}
```
