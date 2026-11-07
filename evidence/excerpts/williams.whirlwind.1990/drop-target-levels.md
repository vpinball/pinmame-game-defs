# Whirlwind drop-target matrix contact levels

This is a factual derivation from retained source code and a ROM service test,
not an inference from an opto beam or host switch readback.

## Read path and working script

PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`:

- `src/wpc/s11.c:644-652`, `pia4a_r`, returns
  `core_getSwCol(locals.swCol)` without complementing it.
- `src/wpc/s11games.c:33-36`, `INITGAME`, initializes the inversion array
  as `{{0}}`. The Whirlwind invocation at line 1189 uses this macro,
  `GEN_S11B`, `FLIP_SWNO(58,57)`, and `S11_MUXSW2|S11_SNDOVERLAY`.

The retained working embedded `script.vbs`, SHA-256
`e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2`,
binds `dtT.InitDrop sw26,26` at line 1229 and
`dtL.InitDrop Array(sw27,sw28,sw29),Array(27,28,29)` at line 1233.
The dropped handlers at lines 1678–1682 call `Hit` for their target;
callbacks 7/8 at lines 853–854 call `SolDropUp`.

In the retained `core.vbs` (digest declared on the VPM script-library source),
`cvpmDropTarget.Hit` at lines 1280–1294 sets the target's matrix switch
`True`; `SolDropUp` at lines 1321–1328 sets every switch in that bank
`False`. These are the runtime dropped and raised states.

## ROM-side proof

Scenario: `tools/harness-scenarios/system-11/whirlwind-switch-levels.json`,
SHA-256 `24b2fe74839e9501d98ef6ee89fb72ecd8cea555e3cc74c12856700d264dd61a`.
Raw run: `external:pinmame-review-artifacts/whirlwind-20261106/harness-levels-repeat.json`,
SHA-256 `cbf0f2f6ddd0160abbe39902e66444c9fad1362231d9ea284798242a1d66054e`.

The run uses `whirl_l3`, keyboard and mechanics disabled, a newly created
state directory containing only factory-initialized NVRAM, and manual
diagnostic switch addresses. The ROM's own `SWITCH LEVELS` checkpoint is
required before changing a target. Display decoder `?` below is retained
literally; the target numbers and parenthesized names are legible.

| Host level / snapshot | ROM upper display | ROM lower display |
| --- | --- | --- |
| All matrix inputs 0 | `SWITCH LEVELS` | `O6` |
| Control 15 = 1 | `RIGHT RETURN` | `O6 1S` |
| 26 = 1 | `TOP SINGLE DROP` | `O6 26` |
| 27 = 1 (three successive frames) | `? DROP (BOTTOM)` | `O6 27` |
| 28 = 1 | `? DROP (MIDDLE)` | `O6 28` |
| 29 = 1 | `? DROP (TOP)` | `O6 29` |
| Each target returned to 0 | `SWITCH LEVELS` | `O6` |
| Control 15 = 1 at end | `RIGHT RETURN` | `O6 1S` |

The ROM calls level 1 active for each target, and level 0 inactive. With
the uninverted matrix read path and zero inversion mask, level 1 is the
matrix closure. Therefore each target's matrix contact rests open:
`normally_closed=false`. This describes the matrix-facing contact, not
the phototransistor's conduction or the beam's physical state.

Reproduction: run `tools/run_pinmame_harness.py` with the pinned native
library, `--game whirl_l3`, the authorized ROM library, an isolated empty
work directory, and `bk2k-nvram-init.json` (a game-neutral factory
initialization wait). Copy only its `nvram/whirl_l3.nv` into a new work
directory and run the scenario above. Both runs completed with no failure.

| Retained input | SHA-256 |
| --- | --- |
| Native `pinmame64.dll`, pinned revision above | `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5` |
| Authorized `whirl_l3.zip` | `2cab7f620275391cc0cdba0f58f115fd7cbe07aa2613f1427a512101034a953b` |
| Factory initialization raw run | `8026ec64fecd5bceeb5a414a775c33df61c2363ef7790a0098fdf7b50deb7a65` |
| Initial NVRAM copied into diagnostic run | `38e163fc5debe3abb3b734262955cfbbc1e04d7e9dc59246e33b0664fc10b392` |

ROM bytes and NVRAM remain outside Git. The raw run and its input-identity
manifest are retained under `whirlwind-20261106` in the review-artifacts root.
