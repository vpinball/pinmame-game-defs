# VPW world-mesh origin check

Exact retained VPW1.0.1 source table SHA256 `3ea276adc2a39ae3fbc05695a2925eefb3f77a52bdee4ad2811ed547312b595f`.
Export: `vpxtool git:v0.33.3 export obj --units vpu`; OBJ SHA256 `8cc29b5cb5dd42764d13573094277dbbaf60d162b3b5652fb83742a1336867a1`.

The primary curator independently streamed each selected object's world-space vertices, recomputed full x/y/z minima/maxima and checked every value against the compact register. OBJ z is reversed; x/y directly share the 952 by 1974 VPX plane. These are mesh bounds, not bulb counts.

| Object | World bounds midpoint x | y | Stored origin x | y |
|---|---:|---:|---:|---:|
| Flasherbase1 | 911.386350 | 1137.361700 | 911.386350 | 1137.302500 |
| Flasherbase2 | 898.991785 | 555.394000 | 899.019100 | 555.339660 |
| Flasherbase3 | 700.561980 | 238.981200 | 700.619930 | 238.981200 |
| Flasherbase4 | 40.230217 | 247.785135 | 40.267723 | 247.447080 |
| Flasherbase5 | 42.105841 | 647.002950 | 42.105843 | 646.872130 |
| Flasherbase6 | 56.655798 | 1155.261250 | 56.694782 | 1155.305800 |
| Flasherbase7 | 243.820955 | 514.901750 | 243.870220 | 514.793460 |
| Flasherbase8 | 427.751110 | 192.030180 | 427.844120 | 192.030180 |
| Flasherbase9 | 718.342650 | 699.631000 | 718.342650 | 699.574770 |
| Flasherbase10 | 575.518875 | 130.815720 | 575.522400 | 131.263230 |
| bumperbulb1 | 232.947435 | 327.781435 | 232.947430 | 327.781430 |
| bumperbulb4 | 457.278595 | 452.607730 | 457.278600 | 452.607730 |
| bumperbulb2 | 425.438775 | 268.169930 | 425.438780 | 268.169920 |
| bumperbulb3 | 256.533545 | 513.442070 | 256.533540 | 513.442100 |

The four `Bumper.Bumper1` through `Bumper.Bumper4` independent center fields are respectively (232.94743,327.78143), (425.43878,268.16992), (256.53354,513.4421), (457.2786,452.60773); they agree with each numbered bumperbulb world midpoint within 0.000001 normalized.

Every dome-base x/y origin is within 0.001 normalized of its own world-space bounds midpoint. Four independent Bumper centers agree with the respective bumperbulb midpoint within 0.000001 normalized. Retain shared-helper stored origins as observed dome anchors; this checks coordinate origin, not factory measurement or independent physical validation.

The callback-to-dome assignment remains the script evidence in `vpw-retained-bindings.md`; the compact bounds and exact selected-object hashes are in `tools/seeds/bally/radical-1990-spatial.json`. The OBJ remains external, verified when the VPX evidence root is configured.
