# F-14 Tomcat switch 9 derived runtime summary

This compact factual summary pins external harness artifacts. It is not a source-extractor evidence document. The retained traces, ROM and NVRAM remain outside Git. The two replay scenarios are committed separately.

```json
{
  "conclusion": "ROM Switch Levels names PLAYFLD TILT for public 9 held at 1 on both trials and returns to SWITCH LEVELS at 0, as the plumb-bob control 1 does. Combined with uninverted s11 pia4a_r and zero F-14 invSw, this resolves physical.normally_closed=false for fitted Playfield Tilt 9. Host readback is not used as the ROM evidence.",
  "driver": "f14_l1",
  "external_harness_manifest_path": "harness/manifest.json",
  "external_harness_manifest_sha256": "652a31e20abdd7979c2361d8149ca74adb558202ba380b0459898d13c6f100c4",
  "files": [
    {
      "path": "harness/nvram-init/run.json",
      "sha256": "da222048710ab9bb353ce3a19cf74b391e1d9024fd30d60a4989d66d9d295051",
      "size": 38984
    },
    {
      "path": "harness/switch9-levels/run.json",
      "sha256": "143992792d15ee0f0e33bcc679d04a3d857402a62d2d237f9244b9a7cba580fc",
      "size": 449166
    },
    {
      "path": "f14-nvram-init.json",
      "sha256": "eb992b14a66d32c9625ae22687f1a80531f404d30f9ceb7ae0f41ed735be16a8",
      "size": 506
    },
    {
      "path": "f14-switch9-levels.json",
      "sha256": "a2ecef7b4686ad7d73ff3217d61955e8043692e6730f20eeb825f94f4ef5d4d0",
      "size": 2232
    },
    {
      "path": "harness/nvram-init/state/nvram/f14_l1.nv",
      "sha256": "a6d476341d4b3793df62f4bbfc783cb4f816bf2ca7f98086ec505f197b66869d",
      "size": 2094
    }
  ],
  "library_sha256": "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5",
  "limitations": "One current-ROM run with repeated stimulus plus same-run control; no physical location or socket/winding claim. Initialized NVRAM copied from separately retained 30-second fresh-state initialization run into a new probe directory. Full traces and NVRAM stay outside Git; the two replay scenarios are committed separately.",
  "machine_id": "williams.f-14-tomcat.1987",
  "observations": [
    {
      "label": "all probe contacts open",
      "player1": " SWITCH",
      "player2": " LEVELS",
      "player3_segments": [
        0,
        63,
        109,
        0,
        0,
        0,
        0
      ],
      "time_s": 24.81844
    },
    {
      "label": "reference plumb-bob tilt 1 closed",
      "player1": " PLUMB ",
      "player2": " TILT  ",
      "player3_segments": [
        0,
        63,
        109,
        0,
        63,
        6,
        0
      ],
      "time_s": 27.81901
    },
    {
      "label": "reference plumb-bob tilt 1 open",
      "player1": " SWITCH",
      "player2": " LEVELS",
      "player3_segments": [
        0,
        63,
        109,
        0,
        0,
        0,
        0
      ],
      "time_s": 29.819619
    },
    {
      "label": "probe playfield tilt 9 closed",
      "player1": "PLAYFLD",
      "player2": " TILT  ",
      "player3_segments": [
        0,
        63,
        109,
        0,
        63,
        111,
        0
      ],
      "time_s": 32.82056
    },
    {
      "label": "probe playfield tilt 9 open",
      "player1": " SWITCH",
      "player2": " LEVELS",
      "player3_segments": [
        0,
        63,
        109,
        0,
        0,
        0,
        0
      ],
      "time_s": 34.821311
    },
    {
      "label": "repeat playfield tilt 9 closed",
      "player1": "PLAYFLD",
      "player2": " TILT  ",
      "player3_segments": [
        0,
        63,
        109,
        0,
        63,
        111,
        0
      ],
      "time_s": 37.821554
    },
    {
      "label": "repeat playfield tilt 9 open",
      "player1": " SWITCH",
      "player2": " LEVELS",
      "player3_segments": [
        0,
        63,
        109,
        0,
        0,
        0,
        0
      ],
      "time_s": 39.822082
    }
  ],
  "output_mode": "ordinary binary default; HandleMechanics=0, keyboard handling off",
  "pinmame_revision": "46e1a01a0f73dc5ce163d98db1ae435883ecc450",
  "rom_archive_sha256": "3be6ca9ececeed410af9b03784c1aa916c5a9b7927e88b626184c4afdcddc1f9",
  "rom_members": [
    {
      "name": "f14_u19.l1",
      "sha1": "46ecd5786653add47751cc56b38d9db7c4622377",
      "size": 32768
    },
    {
      "name": "f14_u21.l1",
      "sha1": "382d0cfa47abea295f0c7501bc0a010473e9d73b",
      "size": 32768
    },
    {
      "name": "f14_u22.l1",
      "sha1": "de3cb855d87033274cc912578b02d1593d2d69f9",
      "size": 32768
    },
    {
      "name": "f14_u26.l1",
      "sha1": "456ce0d1f74fa5e619c272880ba8ac6819848ddc",
      "size": 16384
    },
    {
      "name": "f14_u27.l1",
      "sha1": "1395a4f3891a043cfedc5426ec88af35eab8d4ea",
      "size": 32768
    },
    {
      "name": "f14_u4.l1",
      "sha1": "64b50dbff03cd556130d0cff47b951fdf37d397d",
      "size": 32768
    }
  ],
  "rom_verification": "All six archive member SHA-1 values match src/wpc/s11games.c at pinned revision."
}
```
