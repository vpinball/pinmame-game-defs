# Mystery Castle spatial audit and blockers

Coverage: **partial**

Partial. The factory lamp-location drawing independently validates 55 of 57 checked feature anchors; excluded lamp controls: lamp.39, lamp.40; failed fit placements: lamp.59.p1, lamp.60.p1. GI physical-region assignment, wired socket grouping and missing flasher emitters remain unresolved. Validated feature anchors do not assert measured socket centers.

## Factory drawing check

Four independent source-only controls use two bumper circles and two lower flipper rounded heels. The heels are verified pivot estimates with 15px uncertainty; shaft dots are not drawn. Bumper centers have 10px uncertainty. The controls span the field; both control and callout leave-one-out fits are checked by the official helper. Source-only read corrections and all original ambiguities remain retained. Labels beside parts establish diagram feature locations, not exact sockets.

```json
{
  "checked": 57,
  "limit": 0.07,
  "not_validated": {
    "lamp.59.p1": {
      "callout_offset": 0.0714,
      "control_offset": 0.0662,
      "label": "59",
      "page": "3-5"
    },
    "lamp.60.p1": {
      "callout_offset": 0.0793,
      "control_offset": 0.0774,
      "label": "60",
      "page": "3-5"
    }
  },
  "pages": {
    "3-5": {
      "callout_fit_pairs": 55,
      "callout_loo_max": 0.0624,
      "callout_pairs": 57,
      "control_loo_max": 0.0616,
      "control_rms": 0.0104,
      "controls": 4,
      "image": {
        "height": 3055,
        "path": "by-machine/alvin-g.mystery-castle.1993/renders/page-029.png",
        "root": "manuals",
        "sha256": "321c4ff9cd1720941a0fc9ca5114f035f37656d52844c0c9d0fe250fb9ed8aa7",
        "width": 2142
      },
      "locator": "1993_Mystery_Castle_Manual.pdf PDF29, printed3-5: Lamp Locations"
    }
  },
  "read_by": {
    "transcription": "Independent source-only native drawing reader, without VPX data",
    "verification": "Curators independently checked native source and root controls; rounded flipper heel centers estimate pivots, uncertainty15px; bumper circle centers uncertainty10px. Independent reader controls were rejected: left_pop540,490 is a circle on an upper assembly; the four replacement controls come from independent root source-only crops, not transformed VPX coordinates. Lamps39/40 are excluded because the same bumper circles anchor the control fit. All read marks were inspected on the native-page overlay. Printed-number reads beside parts remain approximate diagram locations, not surveyed socket centers; their original ambiguity is preserved. Rounded flipper heels are accepted as estimated pivot centers with 15px uncertainty, not explicit shaft dots."
  },
  "retained_artifacts": {
    "directory": "alvin-g.mystery-castle.1993/callout-check",
    "manifest_sha256": "925a3873aff129474f82df4648c6aa71c40608a96b4bcd5ddb31f52729644a6e"
  },
  "rule": "A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it.",
  "seed": "tools/seeds/alvin-g/mystery-castle-1993-callouts.json",
  "seed_sha256": "6fb2d8f28e007639aaa3ecd7acc7f9f4db523660ab18e40b1632f4c19362567c",
  "validated": 55
}
```

## Evidence and transform

`x=raw_x/952`, `y=raw_y/2162`; x left-to-right, y rear-to-front; six decimals through the repository extractor.

```json
{
  "coil_service_retained_summary_sha256": "54e22973c337428abd42d57835290e565d8c14b40df0585b9164818eb60a5a80",
  "coil_service_run_sha256": "ee137a0ba7dcbd7da9699d7e3c6860f76f7463d9726ac75788527d44507590c2",
  "drawing_callouts_seed_sha256": "6fb2d8f28e007639aaa3ecd7acc7f9f4db523660ab18e40b1632f4c19362567c",
  "extraction_byte_count": 94419481,
  "extraction_file_count": 800,
  "extraction_manifest_algorithm": "SHA-256 of canonical_bytes(build_manifest(extracted,mystcast)) plus LF; case-sensitive sorted relative POSIX paths,size,SHA-256; manifest.json and manifest.sha256 excluded",
  "extraction_manifest_sha256": "164159268a87a15862a5f6c42d94dd1ce00d754e754934e0eb69370a6a8a01e5",
  "gi_native_drawing": {
    "height": 2542,
    "locator": "Manual PDF page 65, DOC-002 Solenoid Wiring; native 300-dpi upright render. Full GI contact/feed/return context including PP1-13 beyond the compact crop. Footer voltage digit remains uncertain between 5 and 6 VAC; special-insert count digit is uncertain between 4 and 6. Coin-door count 2-4 and pre-contact F21 feed checked directly.",
    "render": "review-artifacts/alvin-g.mystery-castle.1993/manual-native/page065-upright-300dpi.png",
    "sha256": "8c71a1b8b08c7e24f97e43e2cb67ae569383f4d6451c44d3191d50db072830ae",
    "width": 3309
  },
  "manual_sha256": "9fa91108ba60a181218c06420267a2f950109716c665385ac9b62daee329face",
  "mechanical_inventory_sha256": "7335f11c9106846f358d70427e3e83115e7c73efdccad9e897e07239352129db",
  "photo_surveys": [
    {
      "manifest": "review-artifacts/alvin-g.mystery-castle.1993/photos/provenance.json",
      "role": "Verified IPDB1647 photos, exact resource URLs/hashes/attributions retained; major features corroborated, no coordinates derived and no complete wired GI socket survey established.",
      "sha256": "a9e32f94c8866bfb8d2e795383dfc311ba8db50d607fcc9e92b593da03489790"
    },
    {
      "manifest": "review-artifacts/alvin-g.mystery-castle.1993/photos/pinside-provenance.json",
      "role": "Retained Pinside Mystery Castle gallery/bare-playfield photos, exact URLs/hashes/attributions; no coordinates derived and no GI branch assignment inferred from proximity.",
      "sha256": "29e21a9c4620c6c6e2c836474c94d3a89dbceff6445d274a7e3f82ec15ffb598"
    }
  ],
  "pinmame_license_excerpt_sha256": "95b3bc05a5755ee6e2254e0e372543ea2bc6549d3286894bf729912914f7b9a5",
  "pinmame_license_sha256": "21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e",
  "script_sha256": "8a14f0da893892d0bbc366c0dc2a1a8b56bf406102489423efa6089ad864b106",
  "table_sha256": "cf9a40e430a490428ca989a10fac4ac01aeac6cd8783e6da3d6c74f56f32cda5",
  "table_size": 89161728,
  "vpxtool_version": "git:v0.33.3"
}
```

## Projection classes

- trough sensor: 17/18 project onto Drain/BallRelease; under-apron switch brackets are not separately modeled.
- own mechanism actuator: Kicker,plunger,bumper,sling,bank reset and gate outputs project onto their own fixed mechanism; no measured under-playfield coil center is claimed.
- insert and billboard feature anchors: AllLights TimerInterval binds illumination objects. Independent factory drawing checks can validate feature anchors; they do not establish under-playfield socket centers. Bumper39/40 and billboard59/60 remain candidates.

## Excluded helpers and proxies

- GI groups: UpperGILights (25 objects) and LowerGILights (14 objects) cannot settle the conflicting physical regions or candidate branch counts; no GI placements are published.
- flasher helpers: a/b glow doubles collapse to b only when show_bulb_mesh; F23a/b lack bulb mesh. Sprites/dome skins are excluded.
- off-table helpers: F17a001/F17b001 lie far outside bounds and are excluded without clamping.
- invisible flipper: LeftFlipper1 is a real upper-left assembly: script motion and factory circuit/parts establish fitment.
- cabinet button lights: Only lamps47/48 illuminate cabinet Start/Shooter buttons;57-61 are playfield billboard lamps, as DOC-004 explicitly spells out.

## Device placements

| Device | State | Placements (x,y) |
| --- | --- | --- |
| switch.17 | observed | 0.484244,0.962997 |
| switch.18 | observed | 0.87074,0.866706 |
| switch.21 | observed | 0.94043,0.891588 |
| switch.23 | observed | 0.492265,0.266883 |
| switch.24 | observed | 0.089268,0.556678 |
| switch.25 | observed | 0.313751,0.140753 |
| switch.26 | observed | 0.487012,0.206626 |
| switch.27 | observed | 0.220122,0.731218 |
| switch.28 | observed | 0.674833,0.731668 |
| switch.29 | observed | 0.904149,0.086957 |
| switch.30 | observed | 0.039612,0.592966 |
| switch.31 | observed | 0.620536,0.106152 |
| switch.32 | observed | 0.115208,0.23339 |
| switch.33 | observed | 0.83825,0.438573 |
| switch.34 | observed | 0.843466,0.462693 |
| switch.35 | observed | 0.849118,0.48851 |
| switch.36 | observed | 0.855916,0.526283 |
| switch.37 | observed | 0.862022,0.553692 |
| switch.38 | observed | 0.867456,0.580006 |
| switch.39 | observed | 0.56827,0.262421 |
| switch.41 | observed | 0.217622,0.305537 |
| switch.42 | observed | 0.352635,0.292858 |
| switch.43 | observed | 0.538432,0.338693 |
| switch.44 | observed | 0.580768,0.389445 |
| switch.45 | observed | 0.122892,0.740691 |
| switch.46 | observed | 0.049387,0.80561 |
| switch.47 | observed | 0.774863,0.738379 |
| switch.48 | observed | 0.850929,0.762196 |
| switch.49 | observed | 0.177748,0.548472 |
| switch.50 | observed | 0.177504,0.568833 |
| switch.51 | observed | 0.177929,0.590797 |
| switch.52 | observed | 0.62559,0.439684 |
| switch.53 | observed | 0.048333,0.119395 |
| switch.54 | observed | 0.751313,0.247687 |
| switch.55 | observed | 0.855563,0.148936 |
| lamp.01 | validated | 0.451034,0.877895 |
| lamp.02 | validated | 0.40267,0.606064 |
| lamp.03 | validated | 0.466827,0.596511 |
| lamp.04 | validated | 0.531654,0.587954 |
| lamp.05 | validated | 0.366468,0.660341 |
| lamp.06 | validated | 0.431879,0.649703 |
| lamp.07 | validated | 0.495572,0.639758 |
| lamp.08 | validated | 0.559932,0.631664 |
| lamp.09 | validated | 0.339442,0.712839 |
| lamp.10 | validated | 0.403135,0.701969 |
| lamp.11 | validated | 0.466445,0.692256 |
| lamp.12 | validated | 0.53052,0.684393 |
| lamp.13 | validated | 0.370046,0.754341 |
| lamp.14 | validated | 0.433454,0.745216 |
| lamp.15 | validated | 0.496239,0.736197 |
| lamp.16 | validated | 0.56165,0.72764 |
| lamp.17 | validated | 0.238821,0.531969 |
| lamp.18 | validated | 0.244634,0.564826 |
| lamp.19 | validated | 0.236386,0.594952 |
| lamp.20 | validated | 0.157521,0.620859 |
| lamp.21 | validated | 0.217867,0.665054 |
| lamp.22 | validated | 0.050202,0.758052 |
| lamp.23 | validated | 0.125543,0.68867 |
| lamp.24 | validated | 0.052468,0.718191 |
| lamp.25 | validated | 0.774479,0.462766 |
| lamp.26 | validated | 0.778368,0.487828 |
| lamp.27 | validated | 0.783773,0.512051 |
| lamp.28 | validated | 0.788697,0.53699 |
| lamp.29 | validated | 0.793551,0.56009 |
| lamp.30 | validated | 0.799224,0.58461 |
| lamp.31 | validated | 0.779366,0.687903 |
| lamp.32 | validated | 0.853937,0.715847 |
| lamp.33 | validated | 0.237396,0.345905 |
| lamp.34 | validated | 0.373409,0.333913 |
| lamp.35 | validated | 0.492176,0.361987 |
| lamp.36 | validated | 0.527638,0.406874 |
| lamp.37 | validated | 0.401278,0.267444 |
| lamp.38 | validated | 0.419403,0.292695 |
| lamp.39 | candidate | 0.312139,0.141943 |
| lamp.40 | candidate | 0.490228,0.209587 |
| lamp.41 | validated | 0.323123,0.378778 |
| lamp.42 | validated | 0.184828,0.38252 |
| lamp.43 | validated | 0.512477,0.384259 |
| lamp.44 | validated | 0.455553,0.443406 |
| lamp.45 | validated | 0.699076,0.462025 |
| lamp.46 | validated | 0.727165,0.60624 |
| lamp.49 | validated | 0.306821,0.338488 |
| lamp.50 | validated | 0.16623,0.341421 |
| lamp.51 | validated | 0.579973,0.354812 |
| lamp.52 | validated | 0.542474,0.42615 |
| lamp.53 | validated | 0.737125,0.424764 |
| lamp.54 | validated | 0.661141,0.499062 |
| lamp.55 | validated | 0.202943,0.424169 |
| lamp.56 | validated | 0.618209,0.463545 |
| lamp.57 | validated | 0.295479,0.333536 |
| lamp.58 | validated | 0.144085,0.346428 |
| lamp.59 | candidate | 0.556841,0.334407 |
| lamp.60 | candidate | 0.62676,0.369147 |
| lamp.61 | validated | 0.716804,0.413105 |
| solenoid.01 | observed | 0.857484,0.194237 |
| solenoid.02 | observed | 0.313751,0.140753 |
| solenoid.03 | observed | 0.487012,0.206626 |
| solenoid.04 | observed | 0.220122,0.731218 |
| solenoid.05 | observed | 0.674833,0.731668 |
| solenoid.06 | observed | 0.089268,0.556678 |
| solenoid.09 | observed | 0.947284,0.936382 |
| solenoid.10 | observed | 0.042708,0.841153 |
| solenoid.11 | observed | 0.843466,0.462693 |
| solenoid.12 | observed | 0.862022,0.553692 |
| solenoid.13 | observed | 0.484244,0.962997 |
| solenoid.17 | observed | 0.080534,0.018138 |
| solenoid.18 | observed | 0.23838,0.206758 |
| solenoid.19 | observed | 0.651006,0.206461 |
| solenoid.20 | observed | 0.75995,0.067381 |
| solenoid.21 | observed | 0.937169,0.021115 |
| solenoid.22 | observed | 0.837229,0.287567 |
| solenoid.30 | observed | 0.87074,0.866706 |
| solenoid.32 | observed | 0.265232,0.00864 |
| solenoid.46 | observed | 0.615878,0.847574 |
| solenoid.48 | observed | 0.282978,0.847658; 0.133269,0.452348 |

## Concrete remaining evidence

- Unresolved conflict gi-region-16-26: same-manual load drawing versus coil-table physical-region assignments; no source is silently promoted. Resolution: Owner/technician wired socket survey or physical-machine service video linking both public selectors to actual bulbs.
- The special-insert drawing count digit is degraded and uncertain between 4 and 6, followed by BULBS. A separate parallel branch has two unlabelled bulb symbols; the count annotation scope also does not settle the total. The footer voltage digit remains uncertain between 5 and 6 VAC. No typed quantity or voltage is promoted. Resolution: Clearer factory source or original-machine backbox socket survey settling the count and its scope; verified machine supply information is needed for the degraded footer voltage digit.
- The load drawing assigns 16 to 26 top-playfield bulbs and 26 to 12 bottom-playfield bulbs, while the coil table, observed ROM labels and VPX assign opposite regions. Another 2-4 coin-door bulbs share the F21 supply before its relay contact and are unswitched cabinet context. Per-address controlled playfield regions, quantities and wired socket groups remain unresolved. Resolution: Original-machine wired socket survey or physical-machine service video linking selectors 16/26 to all their controlled playfield bulbs; another virtual ROM label trace cannot settle physical wiring.
- Two-bulb branches17/18/19/22 have only one modeled bulb center each; Pit/Lock23 has glow helpers but no modeled bulb. Resolution: Socket-level photos or factory geometry identifying every emitter, reconciled against the exact table.
- Bumper lamps39/40 are excluded from the drawing check because their outlines are fit controls. Billboard59/60 fail one or both independent drawing-fit limits; their table anchors remain candidates. Resolution: Independent physical lamp positions or a clearer factory socket layout; preserve failed fit results instead of moving pixels toward VPX.
