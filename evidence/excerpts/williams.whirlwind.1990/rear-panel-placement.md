# Whirlwind rear-panel socket projections

Method: the repository curator independently inspected the factory elevation, native board
and plastic photographs, four mount correspondences, second assembled view,
mounted stock panel and the numerical checks. The accepted product is a
documented projection onto the lamp assembly's own front plastic plane.
It does not claim measured PCB depth, filament height or emitter Z.

## Source chain

The complete D13356 front/side elevations, printed 5-37 in Williams Red Parts
Catalog 16-9190-B, establish the rigid ten-socket pattern. Original JPEG
SHA-256 `9b6351d58ed5405a776d9f585ea1c5852cde6aa1b9ee4b08d5ada840836b8338`
and publisher URL are in `rear-panel-lamp-assembly.md`. The native upright
1358x1050 derivative has SHA-256
`118044399c4afe5c95e2df6b6b8ac7e057e9c7f4dc42116245a3bad08b2f6d38`.
Measurements below are physical socket-symbol centres, not leaders or globes.

Andrew Burch's [repair log 1](https://www.enteryourinitials.com/2017/03/07/whirlwind-repair-service-log-1/)
shows the same actual PCB and four actual mounting holes, then the same
PCB attached to its plastic by standoffs. Three original 600x450 photographs
are retained under `whirlwind-20261106/web/eyi-images/`:

- [whirlwind_rear_storm_lamp_board_start.jpg](http://www.enteryourinitials.com/images/whirlwind/whirlwind_rear_storm_lamp_board_start.jpg), SHA-256 `4e8543f7cb1b57296a84e865b1478a7cde80507f2902a0f7f325ecb290199f7e`.
- [whirlwind_rear_storm_lamp_board_dirty.jpg](http://www.enteryourinitials.com/images/whirlwind/whirlwind_rear_storm_lamp_board_dirty.jpg), SHA-256 `e6892411527eb8a56c0b8b747ccb00113bf80eb4ee9ee44146ca20f64fd895ea`.
- [whirlwind_rear_storm_lamp_board_plastic_clean.jpg](http://www.enteryourinitials.com/images/whirlwind/whirlwind_rear_storm_lamp_board_plastic_clean.jpg), SHA-256 `198bfe85e3b8a3d6566cfd980922dc6b7c4d23ea5d00f4369d79ffaa5d7bfb26`.

The independently retained mounted stock example is PantherCityPins,
[Rescuing a Whirlwind, post 4](https://pinside.com/pinball/forum/topic/rescuing-a-whirlwind),
[original 1536x2048 photograph](https://o.pinside.com/8/3e/b6/83eb6dff93d28b6a4dfefbed1ea362cedb539f83.jpeg),
acquired 2026-11-07T02:56:59.353607+00:00, SHA-256 `51b51680bb1c72b45bede10fc4b1e424e38dd5aa7b2bc2f6ca913cd53bb5b334`.
It is retained as `parent-gi-voltage-and-rescue/rescue-selected-4.jpeg`.

All source copyright remains with Williams and the photographers.
License/redistribution rights are NOASSERTION. Only factual measurements
are transcribed. Complete retained originals remain outside the repository.

## Reproducible registration

Bigus world OBJ SHA-256
`508cd48008db552c3a8c5b76281ee254d38ef687cd5f3b85aa31d5051649859a`
is the `vpxtool git:v0.33.3 export obj --units vpu` geometry. Primitive2's
world bounds are X 4.6560974..960.9023, Y 242.21863..243.96722 and
OBJ Z -320.9017..-215.4538. Negative OBJ Z is above the playfield.
Its front face supplies projection Y 243.96722/2162=0.112843.
A baked primitive's stored origin is not used.

The plastic-only artwork fit mirrors the rear photograph in X, with four
post regions masked, then uses 27 SIFT inliers. Four independently read
withheld feet have X errors 0.005278,-0.000153,-0.007849,-0.003379 normalized.
This registers the plastic; it does not by itself register the lamp PCB.

The dirty-board photograph's nine independently read socket bases reconcile
its plane with factory pixels. Its four actual mount-hole centres are
(60,311),(184,210),(333,197),(471,138). The resulting factory X coordinates
are 1179.450806,1002.575623,810.343384,548.253845. The corresponding physical
plastic posts have model-world X 867.1560974,718.6560974,556.1560974,326.1560974.
The least-squares relation is worldX=0.8569323033212868*factoryX-141.48759904524903.
Its worst leave-one-post-out X error is 0.009678 normalized. Socket identity
and artwork/post controls have separate roles; sockets are not claimed as
independent held-out checks of the fit that used them.

A second registration of the board photograph uses the PCB edges, visible
corner and nine header-pin centres rather than sockets. Four corner-included
variants, allowing header height offset and pin uncertainty, hold out every
socket. All ten derived X values agree with the first chain within 0.008330
normalized. The partially clipped LMP10 base is a further holdout: actual
approximately (11,276), header/edge prediction (11.88,276.32). Omitting the
visible corner produces ill-conditioned fits; those variants are rejected.

The separate assembled PCB+plastic photograph then checks all five #906
bases, held out of its camera fit. Independent artwork/bolt controls, actual
PCB upper-edge runs and nine PCB-facing header-pin feet calibrate that view.
Across nine art/standoff-weight variants, all five held-out X values agree
within 0.010137 normalized. The native 2D residual reaches 13.28 px, mainly in
the first bulb's vertical component. This is an X-layout check for the
defined projection; it is not a claim that the model recovers true emitter Z.

Finally, the mounted stock photograph checks the front-plastic projection
plane against playfield artwork and seven actual front bolt heads. It uses
66-248 independently matched non-panel features plus 15 manual floor reads.
A centered optical axis, square pixels, one radial coefficient and relative
artwork dimensions are explicit camera assumptions. Twenty-eight held-out
screw variants have errors at most 4.53 native px. Twenty-seven yield panel Y
0.1057..0.1124; one weakly constrained far-left-screw holdout reaches 0.1216
and a tilt bound. All remain within 0.009 of the exact model plane 0.112843.
This corroborates the chosen projection plane rather than actual PCB depth.

LMP1,2,6,7,10 lie outside the original four-post X interval. They are not
promoted from that extrapolation alone: the full rigid-board edge/header
registration covers their pitch, the second assembled elevation checks both
outer flashers, and LMP10's clipped actual base is independently checked.
The retained diagnostic files deliberately keep their earlier accepted:false
flags. This committed seed records the primary curator's combined-evidence
decision after the later independent checks, with the limitations preserved.

## Published projected locations

X is rounded to three decimals because it is a measured registration.
Y retains the exact retained-model plane's six-decimal normalization.
The seed retains all raw pixels, transforms, checks and reproduction-input
hashes. The curator recomputes the four-control affine map before placement.

| Physical socket | Factory upright pixel | Output | x | y |
| --- | --- | ---: | ---: | ---: |
| LMP1 | 300,274 | 37 | 0.12 | 0.112843 |
| LMP2 | 414,274 | 37 | 0.221 | 0.112843 |
| LMP3 | 612,274 | 39 | 0.397 | 0.112843 |
| LMP4 | 866,274 | 40 | 0.623 | 0.112843 |
| LMP5 | 1117,274 | 40 | 0.846 | 0.112843 |
| LMP6 | 236,330 | 11 | 0.063 | 0.112843 |
| LMP7 | 444,330 | 11 | 0.248 | 0.112843 |
| LMP8 | 734,330 | 11 | 0.506 | 0.112843 |
| LMP9 | 1057,330 | 11 | 0.793 | 0.112843 |
| LMP10 | 1215,330 | 11 | 0.933 | 0.112843 |

Outputs 37/39/40 use the documented left-pair/middle/right-pair arrangement
(2/1/2), established by factory construction, handbook counts and physical
ordered socket pattern. Output 11 also includes these five GI emitters and
its ten separately placed playfield bayonets. These ten panel projections
are separate emitters; none is a backglass/VR glow proxy.
