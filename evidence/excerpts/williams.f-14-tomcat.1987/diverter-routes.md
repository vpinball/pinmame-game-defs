# F-14 launch-ramp gate routes

Method: mixed; curator review and independent source checks covered exact script-bound collision geometry; reviewed: true. The raw points/hashes below are a compact derived excerpt. No physical flight speed or timing is asserted.

```json
{
  "coordinate_frame": "Raw VPW 2025 table units; x left to right, y rear to front; bounds 952x1974. Do not mix with 964x2162 older tables.",
  "method": "Independent geometric reconstruction from script-bound collision walls, exact connected ramps and scoring switch objects; not a simulated ball-flight measurement.",
  "source_script": {
    "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/script.vbs",
    "sha256": "3a1ccbc51bbf3792d358bcb7b6d6dd053e099c015fc9334c41a1f0ef5b921750",
    "locators": "Sol21 lines 837-847, Sol22 lines 849-859; ramp trigger handlers 1375-1383; eject callbacks 876-906"
  },
  "route_table": [
    {
      "upper21": true,
      "lower22": "either",
      "first_gate": "Sol21wall at y = 320..382",
      "ramp_sensor": 32,
      "ramp": "upper",
      "end_sensor": 23,
      "end": "right center eject",
      "path": [
        "Ramp20",
        "Sol21wall",
        "Ramp13",
        "Ramp7"
      ]
    },
    {
      "upper21": false,
      "lower22": true,
      "first_gate": "Sol22wall at y = 480..542",
      "ramp_sensor": 31,
      "ramp": "middle",
      "end_sensor": 22,
      "end": "left center eject",
      "path": [
        "Ramp20",
        "Ramp14",
        "Sol22wall",
        "Ramp3"
      ]
    },
    {
      "upper21": false,
      "lower22": false,
      "first_gate": "neither; main channel continues",
      "ramp_sensor": 30,
      "ramp": "lower",
      "end_sensor": 21,
      "end": "right eject",
      "path": [
        "Ramp20",
        "Ramp14",
        "Ramp6",
        "Ramp19"
      ]
    }
  ],
  "limitations": "No physical flight timing or speed inferred. Source handles coil states directly: enabled raises matching collidable wall; disabled drops it. Ramp endpoint to eject connection is reconciled with positions and factory layout drawing, not source naming alone.",
  "files": [
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Wall.Sol21wall.json",
      "sha256": "24ca80c40d09ba22237cbc78250f17bad162b4d16f10f75b48907e5a68ee2552",
      "kind": "Wall",
      "name": "Sol21wall",
      "center": null,
      "height_bottom": 95.0,
      "height_top": 145.0,
      "points": [
        [
          36.82743,
          320.0117
        ],
        [
          36.91992,
          381.62836
        ],
        [
          91.692894,
          381.53598
        ],
        [
          80.69336,
          374.6897
        ],
        [
          70.72916,
          368.2902
        ],
        [
          59.4125,
          360.26672
        ],
        [
          47.419277,
          350.17307
        ],
        [
          39.86622,
          336.5952
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Wall.Sol22wall.json",
      "sha256": "50a246f639d9724f6d3f5390b57fcafe113b856755476ee25b06a13cd248360d",
      "kind": "Wall",
      "name": "Sol22wall",
      "center": null,
      "height_bottom": 95.0,
      "height_top": 145.0,
      "points": [
        [
          36.55007,
          480.1172
        ],
        [
          36.642563,
          541.73114
        ],
        [
          91.4156,
          541.6388
        ],
        [
          80.41608,
          534.79285
        ],
        [
          70.451866,
          528.39386
        ],
        [
          59.135174,
          520.371
        ],
        [
          47.14193,
          510.27856
        ],
        [
          39.58886,
          496.7007
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp20.json",
      "sha256": "a3cdd3aa539c5efe92e9b5b1ac397ed06fa00e3faddb74a372c6422cc6310f9b",
      "kind": "Ramp",
      "name": "Ramp20",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          64.32706,
          311.06247
        ],
        [
          65.718025,
          205.08347
        ],
        [
          74.70032,
          145.65845
        ],
        [
          93.19668,
          117.036736
        ],
        [
          117.23344,
          98.48302
        ],
        [
          148.2075,
          81.392006
        ],
        [
          178.50346,
          74.39482
        ],
        [
          194.72649,
          71.95649
        ],
        [
          209.69252,
          70.490074
        ],
        [
          217.09315,
          70.49702
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp14.json",
      "sha256": "d6bf28f4d850e7f63fe2da93980c94c63eeb4aa8862322cc0ee13d3075c685db",
      "kind": "Ramp",
      "name": "Ramp14",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          64.029335,
          542.09174
        ],
        [
          64.442184,
          311.7095
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp6.json",
      "sha256": "b6861d5d4364f3cbdad89df301666a6a8551b41fb49e5d0ffc6753c7c3310ec6",
      "kind": "Ramp",
      "name": "Ramp6",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          115.18311,
          687.0943
        ],
        [
          99.61255,
          679.7353
        ],
        [
          74.87573,
          656.1309
        ],
        [
          65.81815,
          628.92505
        ],
        [
          64.148315,
          605.95
        ],
        [
          64.09766,
          541.7097
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp13.json",
      "sha256": "2801459e2a89460c08caf3255587b9f606d4380755a56af45c9dc23952e7c2e8",
      "kind": "Ramp",
      "name": "Ramp13",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          508.71063,
          544.8442
        ],
        [
          122.890755,
          366.95816
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp7.json",
      "sha256": "d6948bf254ac6f318a1bd10e9573fd30d636f5b9a7defaebe5f52adc47a0f8df",
      "kind": "Ramp",
      "name": "Ramp7",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          545.98315,
          703.13403
        ],
        [
          560.89124,
          674.9229
        ],
        [
          568.3557,
          659.739
        ],
        [
          571.9733,
          637.57855
        ],
        [
          566.0953,
          602.72925
        ],
        [
          550.6362,
          576.05695
        ],
        [
          530.32806,
          555.9928
        ],
        [
          514.96204,
          547.6283
        ],
        [
          508.77133,
          544.8479
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp3.json",
      "sha256": "6cd3065dff63bc9460dff193bbbbfdc3afebfc64685a168739b48f3d36a68cad",
      "kind": "Ramp",
      "name": "Ramp3",
      "center": null,
      "height_bottom": 92.0,
      "height_top": 92.0,
      "points": [
        [
          383.20358,
          704.0874
        ],
        [
          372.6465,
          683.8479
        ],
        [
          359.1048,
          657.1842
        ],
        [
          344.8356,
          642.6825
        ],
        [
          328.85962,
          627.75806
        ],
        [
          313.7016,
          616.5232
        ],
        [
          297.25473,
          607.64246
        ],
        [
          123.19638,
          526.0805
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Ramp.Ramp19.json",
      "sha256": "8f470f655806141aea863cc69fb7a20e854496e5331635211980d0fbabae8d27",
      "kind": "Ramp",
      "name": "Ramp19",
      "center": null,
      "height_bottom": 93.0,
      "height_top": 93.0,
      "points": [
        [
          115.06183,
          687.03217
        ],
        [
          375.51566,
          805.1423
        ],
        [
          396.98636,
          815.3038
        ],
        [
          418.56268,
          822.31146
        ],
        [
          511.6652,
          836.5627
        ],
        [
          810.96246,
          873.70874
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw30.json",
      "sha256": "f1bc5859d5e4ae04a9f6d0987ad65bcabf6a7e43125e0b7b2d33ff29b42e00f5",
      "kind": "Trigger",
      "name": "sw30",
      "center": {
        "x": 134.47237,
        "y": 696.2346
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          104.47218,
          666.2346
        ],
        [
          104.47218,
          726.2346
        ],
        [
          164.47237,
          726.2346
        ],
        [
          164.47237,
          666.2346
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw31.json",
      "sha256": "036ae03bc49647d9c1a7d56ea1dda720e50822a1700ebda8b38946840140b829",
      "kind": "Trigger",
      "name": "sw31",
      "center": {
        "x": 131.62427,
        "y": 530.0029
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          101.62452,
          500.0043
        ],
        [
          101.62452,
          560.0029
        ],
        [
          161.62427,
          560.0029
        ],
        [
          161.62427,
          500.0043
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw32.json",
      "sha256": "384d68fcd74d67ea319c174aeb3aa65d8f66727840ac24f63ea46f3880756411",
      "kind": "Trigger",
      "name": "sw32",
      "center": {
        "x": 133.25818,
        "y": 371.7021
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          103.25837,
          341.7021
        ],
        [
          103.25837,
          401.7021
        ],
        [
          163.25818,
          401.7021
        ],
        [
          163.25818,
          341.7021
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw21.json",
      "sha256": "b0cbe3192da73039a94978789f96bc1a956d2df410280ceb7f57b345051c9de7",
      "kind": "Trigger",
      "name": "sw21",
      "center": {
        "x": 895.01276,
        "y": 1022.808
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          865.01276,
          992.808
        ],
        [
          865.01276,
          1052.8079
        ],
        [
          925.01276,
          1052.8079
        ],
        [
          925.01276,
          992.808
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw22.json",
      "sha256": "600282f6d85f68a400ea276ad606007817fd01fd54b75eed3555596bb2c85d80",
      "kind": "Trigger",
      "name": "sw22",
      "center": {
        "x": 405.53433,
        "y": 760.2239
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          380.6388,
          745.50916
        ],
        [
          380.6388,
          827.0919
        ],
        [
          430.46384,
          827.0919
        ],
        [
          430.31125,
          745.50916
        ]
      ]
    },
    {
      "path": "vpx-sources/williams/f-14-tomcat-1987/vpw-2025/extracted/gameitems/Trigger.sw23.json",
      "sha256": "ceb83ee4f58d2e8fbc7c3c5952615a01d6894d3029a00baa4911205654c295fc",
      "kind": "Trigger",
      "name": "sw23",
      "center": {
        "x": 513.7195,
        "y": 775.35004
      },
      "height_bottom": null,
      "height_top": null,
      "points": [
        [
          488.82507,
          760.6353
        ],
        [
          488.82507,
          842.2181
        ],
        [
          538.6486,
          842.2181
        ],
        [
          538.49603,
          760.6353
        ]
      ]
    }
  ]
}
```
