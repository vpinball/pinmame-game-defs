# Figure V coarse outhole measurement

Source: Bally_1981_Medusa_Manual.pdf SHA256
`6137807222d614505ac923df7acd24c091449cf45f1d4d383ab82939d0df6a7b`,
PDF18 printed18, full native render2388x3158, SHA256
`df53ba468752ce17ffd55f3e9ec83c19f88e550d7f5ad643c579e6f219497e61`.
The committed crop is the location drawing, not the tabular identification page.

Primary GPT Sol read mechanism centers on the native image using a100-pixel
grid for inspection. Approximate reading precision20pixels. These are coarse
visual reads, not inferred from table coordinates and not independent physical
socket measurements. Exact seed: tools/seeds/bally/medusa-1981-manual-geometry.json.
Frame corners(100,220),(1400,220),(1400,2720),(100,2720) are disclosed as the
drawing outline, never used as mechanism controls.

| Table control | Source pixel | Part read |
| --- | --- | --- |
| sw48 | 463,346 | Leftmost top target face |
| sw42 | 934,346 | Rightmost top target face |
| Bumper1 | 389,1138 | Upper left bumper cap |
| Bumper4 | 965,1138 | Upper right bumper cap |
| Bumper2 | 512,1404 | Bottom left bumper cap |
| Bumper3 | 840,1404 | Bottom right bumper cap |
| LeftFlipper | 510,2407 | Lower left flipper pivot, coarse |
| RightFlipper | 925,2407 | Lower right flipper pivot, coarse |

The measured outhole mouth is(680,2530), the drawn mouth below the post, not
the remote08 circle or square. Reconcile with least-squares affine fit from
tools/drawing_callouts.py over those eight independent pixel/table pairs.
Controls span0.790414 of playfield height. Maximum leave-one-out residual is
0.050198 normalized. The point extrapolates below the control hull and stays
an attempted cross-check. It is a coarse physical projection, never validated by the same
drawing used to measure it. The drawing and table are differently proportioned;
local detail should be refined from a physical survey.

Formula from seed: x=0.0007780489162578602*u-0.000018558472810651322*v-
0.05194520889640405; y=0.0000005187072290377556*u+
0.0003834527840216422*v-0.10050982292795038. Round the result to six decimals:
(0.430175,0.869978). **Reject this coordinate for canonical placement:** it
falls above the table's Shield post (y=0.889877), although the factory drawing
places the outhole below the post. The extrapolated fit and differently
proportioned drawing do not reconcile that part. No guessed correction is
applied. The measurement and failed result remain reviewable evidence.
The table's BallRelease at(0.872767,0.866680) is a
serve/routing anchor, and its Drain is a catcher. Neither is accepted as this
physical contact's position.
